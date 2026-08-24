from __future__ import annotations

import json
import random
import sys
from collections import defaultdict
from itertools import combinations, product
from pathlib import Path

from mux_dag_budget_one import (
    DAGBudgetOneCertificate,
    fixed_pair_dag_budget_one_certificate,
    strict_dag_delta_one_family,
)

V109_DIR = Path(__file__).resolve().parents[1] / "v109"
V113_DIR = Path(__file__).resolve().parents[1] / "v113"
sys.path.insert(0, str(V109_DIR))
sys.path.insert(0, str(V113_DIR))
from mux_gate_flow import MuxGate, in_range  # noqa: E402
from mux_dominator_dp import fixed_pair_minimum_overlap_certificate  # noqa: E402


def target_word(gates, cycle0, cycle1):
    targets = [0] * len(gates)
    assigned = {}
    for cycle in (cycle0, cycle1):
        initial = gates[cycle[0][0]].branch(cycle[0][1])[2]
        for pos, (gi, branch) in enumerate(cycle):
            if pos + 1 < len(cycle):
                ngi, nb = cycle[pos + 1]
                desired = gates[ngi].branch(nb)[2]
            else:
                desired = 1 ^ initial
            bit = gates[gi].target_for_arrival(branch, desired)
            if gi in assigned and assigned[gi] != bit:
                return None
            assigned[gi] = bit
            targets[gi] = bit
    return tuple(targets)


def enumerate_gate_simple_paths(n, gates, root, start, limit=3000):
    allowed = [i for i, gate in enumerate(gates) if gate.selector != root]
    by_selector = defaultdict(list)
    for gi in allowed:
        by_selector[gates[gi].selector].append(gi)
    paths = []

    def dfs(var, path, used):
        if len(paths) >= limit:
            return
        if var == root:
            paths.append(tuple(path))
            return
        if len(path) >= len(allowed):
            return
        for gi in by_selector[var]:
            if gi in used:
                continue
            for branch in (0, 1):
                dest = gates[gi].branch(branch)[1]
                dfs(dest, path + [(gi, branch)], used | {gi})

    dfs(start, [], set())
    return list(dict.fromkeys(paths)), len(paths) >= limit


def brute_fixed_pair(n, gates, selector, g0, b0, g1, b1):
    d0 = gates[g0].branch(b0)[1]
    d1 = gates[g1].branch(b1)[1]
    paths0, capped0 = enumerate_gate_simple_paths(n, gates, selector, d0)
    paths1, capped1 = enumerate_gate_simple_paths(n, gates, selector, d1)
    if capped0 or capped1 or not paths0 or not paths1:
        return None
    best = len(gates) + 1
    best_compatible = len(gates) + 1
    for p0 in paths0:
        used0 = {gi for gi, _ in p0}
        for p1 in paths1:
            overlap = len(used0 & {gi for gi, _ in p1})
            best = min(best, overlap)
            if target_word(
                gates,
                ((g0, b0),) + p0,
                ((g1, b1),) + p1,
            ) is not None:
                best_compatible = min(best_compatible, overlap)
    return best, None if best_compatible > len(gates) else best_compatible


def random_mux(n, m, rng):
    gates = []
    for _ in range(m):
        s, a, b = rng.sample(range(n), 3)
        polarity = tuple(rng.randrange(2) for _ in range(3))
        gates.append(MuxGate(s, a, b, polarity, rng.randrange(2)))
    return gates


def random_dag_crosscheck():
    rng = random.Random(115)
    compared = 0
    accepted = 0
    rejected = 0
    for n in range(3, 7):
        for _ in range(1000):
            gates = random_mux(n, n + 1, rng)
            by_selector = defaultdict(list)
            for gi, gate in enumerate(gates):
                by_selector[gate.selector].append(gi)
            candidates = []
            for selector, ids in by_selector.items():
                for g0, g1 in combinations(ids, 2):
                    for b0, b1 in product((0, 1), repeat=2):
                        if gates[g0].branch(b0)[2] != gates[g1].branch(b1)[2]:
                            candidates.append((selector, g0, b0, g1, b1))
            rng.shuffle(candidates)
            for candidate in candidates[:3]:
                brute = brute_fixed_pair(n, gates, *candidate)
                if brute is None:
                    continue
                try:
                    cert = fixed_pair_dag_budget_one_certificate(
                        n, gates, *candidate
                    )
                except ValueError:
                    continue
                best, best_compatible = brute
                expected = (
                    best_compatible is not None
                    and best_compatible <= best + 1
                )
                assert (cert is not None) == expected, (
                    n,
                    candidate,
                    best,
                    best_compatible,
                    cert,
                )
                if cert is not None:
                    assert isinstance(cert, DAGBudgetOneCertificate)
                    assert len(cert.overlap) <= best + 1
                    assert target_word(gates, cert.cycle0, cert.cycle1) == cert.target
                    accepted += 1
                else:
                    rejected += 1
                compared += 1
    assert compared >= 2000
    return {
        "fixed_pairs": compared,
        "accepted_within_budget": accepted,
        "rejected_within_budget": rejected,
    }


def strict_family_checks():
    rows = []
    for depth in range(0, 41):
        n, gates, (g0, g1, common, extra) = strict_dag_delta_one_family(depth)
        assert len(gates) == n + 1
        assert fixed_pair_minimum_overlap_certificate(
            n, gates, 0, g0, 0, g1, 0
        ) is None, depth
        brute = brute_fixed_pair(n, gates, 0, g0, 0, g1, 0)
        assert brute == (1, 2), (depth, brute)
        cert = fixed_pair_dag_budget_one_certificate(
            n, gates, 0, g0, 0, g1, 0
        )
        assert cert is not None, depth
        assert cert.delta == 1
        assert set(cert.overlap) == {common, extra}
        if depth == 0:
            assert not in_range(n, gates, cert.target)
        rows.append(
            {
                "depth": depth,
                "n": n,
                "m": len(gates),
                "minimum_overlap": 1,
                "minimum_compatible_overlap": 2,
                "delta": 1,
            }
        )
    return rows


def cyclic_rejection_control():
    n, gates, (g0, g1, _common, _extra) = strict_dag_delta_one_family(0)
    # The extra gate is left->split. Repoint one split exit's dead branch back
    # to left, creating left->split->left in the non-common post-dominator stage.
    bad = list(gates)
    split_exit = len(bad) - 2
    gate = bad[split_exit]
    bad[split_exit] = MuxGate(
        gate.selector,
        gate.data0,
        4,
        gate.polarity,
        gate.out_flip,
    )
    try:
        fixed_pair_dag_budget_one_certificate(n, bad, 0, g0, 0, g1, 0)
    except ValueError:
        return 1
    raise AssertionError("cyclic-stage control was incorrectly accepted as DAG")


def main():
    result = {
        "random_dag_crosscheck": random_dag_crosscheck(),
        "strict_delta_one_family": strict_family_checks(),
        "cyclic_not_applicable_controls": cyclic_rejection_control(),
        "certificate": "dag_stage_dominator_budget_one_dp",
        "failures": 0,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
