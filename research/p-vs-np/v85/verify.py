#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import v85_core as core

ROOT = Path(__file__).resolve().parent

PARAMETERS = ((8, 12), (27, 36), (64, 80), (125, 150), (216, 252), (343, 392), (512, 576), (1000, 1100))
REMOTE_CASES = ((4, 8, 851001), (4, 9, 851002), (5, 10, 851003), (5, 11, 851004), (6, 12, 851005), (6, 13, 851006), (5, 9, 851007), (6, 11, 851008))


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

    print("V85 primary verification passed: 256 predicates, 8 counting scales, 384 C4-free cases, 866 syndromes, and 8 remote points.")


if __name__ == "__main__":
    main()
