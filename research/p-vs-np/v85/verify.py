#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import random
import sys

import v85_core as core
from distance_semiring import (
    build_v75_model,
    distance_pair_count,
    hamming_ball_volume as v75_ball,
    remote_point_from_v75_model,
)

ROOT = Path(__file__).resolve().parent
V74 = str(ROOT.parent / "v74")
if V74 not in sys.path:
    sys.path.insert(0, V74)
from two_fiber_model import brute_preimage_counts, make_gate

PARAMETERS = ((8, 12), (27, 36), (64, 80), (125, 150), (216, 252), (343, 392), (512, 576), (1000, 1100))
REMOTE_CASES = ((4, 8, 851001), (4, 9, 851002), (5, 10, 851003), (5, 11, 851004), (6, 12, 851005), (6, 13, 851006), (5, 9, 851007), (6, 11, 851008))


def brute_pair_count(counts: dict[int, int], m: int, prefix: tuple[int, ...], radius: int) -> int:
    total = 0
    for output, multiplicity in counts.items():
        mismatch = sum(bit != ((output >> i) & 1) for i, bit in enumerate(prefix))
        total += multiplicity * v75_ball(m - len(prefix), radius - mismatch)
    return total


def verify_v75_distance_integration() -> tuple[int, int, int]:
    rng = random.Random(850075)
    models = pair_checks = remote_points = 0
    for _ in range(12):
        n, m = 4, 9
        gates = []
        for _ in range(m):
            arity = rng.randint(1, 3)
            support = sorted(rng.sample(range(n), arity))
            truth_mask = rng.randrange(1 << (1 << arity))
            gates.append(make_gate(support, truth_mask, rng.randrange(2)))
        model = build_v75_model(n, gates)
        counts = brute_preimage_counts(n, gates)
        for radius in (0, 1):
            for length in range(m + 1):
                for value in range(min(1 << length, 4)):
                    prefix = tuple((value >> i) & 1 for i in range(length))
                    expected = brute_pair_count(counts, m, prefix, radius)
                    assert distance_pair_count(model, prefix, radius) == expected
                    pair_checks += 1
        remote = remote_point_from_v75_model(model, 1)
        target = int(remote["target_integer"])
        assert min((output ^ target).bit_count() for output in counts) > 1
        assert remote["terminal_pair_count"] == 0
        models += 1
        remote_points += 1
    return models, pair_checks, remote_points


def main() -> None:
    expected = json.loads((ROOT / "RESULTS.json").read_text(encoding="utf-8"))["finite_audit"]

    census = core.classify_predicates()
    assert census["total"] == 256
    assert (census["affine_count"], census["nonaffine_unbalanced_count"], census["balanced_nonaffine_count"]) == (16, 184, 56)
    assert census["balanced_nonaffine_min_best_low_degree_correlation"] == 0.5
    assert census["balanced_nonaffine_max_best_low_degree_correlation"] == 0.5
    assert census["balanced_nonaffine_min_best_agreement"] == 0.75

    pair = core.verify_pair_embedding_exhaustively()
    assert pair["endpoint_cases"] == 4 and pair["all_endpoint_cases_constructed"]
    for n, m in PARAMETERS:
        bound = core.counting_list_bound(n, [3] * m)
        dims = core.eval_h_dimensions(n, [3] * m, bound.minimum_counting_list_size)
        assert bound.additive_stretch > 0
        assert dims["adaptive_query_depth"] == 4
        assert dims["nonadaptive_junta_bound"] == 11

    plane = core.affine_plane_order_three_supports()
    assert len(plane) == 12
    assert all(len(set(a) & set(b)) <= 1 for i, a in enumerate(plane) for b in plane[i + 1 :])
    total = 0
    violations = 0
    for mode, seeds in (("random", range(850000, 850256)), ("affine_heavy", range(851500, 851628))):
        for seed in seeds:
            masks = core.make_linear_probe_masks(seed, len(plane), mode)
            circuit = core.Circuit(9, tuple(core.Gate(s, mask) for s, mask in zip(plane, masks)))
            for selector in core.constant_syndrome_vectors(circuit):
                if not selector:
                    continue
                total += 1
                if any((selector >> i) & 1 and not core.is_affine_gate(g) for i, g in enumerate(circuit.gates)):
                    violations += 1
                assert core.syndrome_constant(circuit, selector)[0]
    assert total == expected["nonzero_constant_syndromes"] == 866
    assert violations == expected["syndrome_violations"] == 0

    counter, selector = core.counterexample_circuit()
    assert core.incidence_girth(counter) == 4
    assert core.syndrome_constant(counter, selector) == (True, 0)
    neighborhood = set().union(*(set(g.support) for i, g in enumerate(counter.gates) if selector & (1 << i)))
    assert len(neighborhood) == 6 >= selector.bit_count()
    assert all(s != selector for s, _ in core.hall_deficient_subsets(counter))

    for n, m, seed in REMOTE_CASES:
        circuit = core.make_remote_probe_circuit(seed, n, m)
        radius = -1
        for r in range(m + 1):
            if (1 << n) * core.hamming_ball_volume(m, r) < (1 << m):
                radius = r
            else:
                break
        target = core.remote_point_by_pair_count(circuit, radius)
        assert core.distance_to_range(circuit, target) > radius

    models, pair_checks, v75_remote_points = verify_v75_distance_integration()
    assert models == expected["V75_distance_models"] == 12
    assert pair_checks == expected["V75_distance_prefix_checks"] == 840
    assert v75_remote_points == expected["V75_remote_points"] == 12

    print("V85 primary verification passed: 256 predicates, 866 syndromes, 8 oracle remote points, and 12 source-level V75 distance models.")


if __name__ == "__main__":
    main()
