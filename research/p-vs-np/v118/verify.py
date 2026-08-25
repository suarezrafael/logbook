from __future__ import annotations

import json
import random
import sys
from collections import defaultdict, deque
from itertools import combinations
from pathlib import Path

from mux_clone_bank import (
    CloneBankBudgetOneCertificate,
    fixed_pair_clone_bank_budget_one_certificate,
    strict_clone_bank_delta_one_family,
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


def enumerate_gate_simple_paths(n, gates, root, start, limit=10000):
    by_selector = defaultdict(list)
    for gi, gate in enumerate(gates):
        if gate.selector != root:
            by_selector[gate.selector].append(gi)
    paths = []

    def dfs(var, path, used):
        if len(paths) >= limit:
            return
        if var == root:
            paths.append(tuple(path))
            return
        if len(path) >= len(gates):
            return
        for gi in by_selector[var]:
            if gi in used:
                continue
            for branch in (0, 1):
                dfs(
                    gates[gi].branch(branch)[1],
                    path + [(gi, branch)],
                    used | {gi},
                )

    dfs(start, [], set())
    return list(dict.fromkeys(paths)), len(paths) >= limit


def brute_fixed_pair(n, gates, selector, g0, b0, g1, b1):
    p0, cap0 = enumerate_gate_simple_paths(
        n, gates, selector, gates[g0].branch(b0)[1]
    )
    p1, cap1 = enumerate_gate_simple_paths(
        n, gates, selector, gates[g1].branch(b1)[1]
    )
    if cap0 or cap1 or not p0 or not p1:
        return None
    best = len(gates) + 1
    best_compatible = len(gates) + 1
    for route0 in p0:
        used0 = {gi for gi, _ in route0}
        for route1 in p1:
            overlap = len(used0 & {gi for gi, _ in route1})
            best = min(best, overlap)
            if target_word(
                gates,
                ((g0, b0),) + route0,
                ((g1, b1),) + route1,
            ) is not None:
                best_compatible = min(best_compatible, overlap)
    return best, None if best_compatible > len(gates) else best_compatible


def stage_acyclic(n, gates, removed):
    adjacency = [[] for _ in range(n)]
    indegree = [0] * n
    for gi, gate in enumerate(gates):
        if gi in removed or gate.selector == 0:
            continue
        for dest in (gate.data0, gate.data1):
            adjacency[gate.selector].append(dest)
            indegree[dest] += 1
    queue = deque(i for i in range(n) if indegree[i] == 0)
    seen = 0
    while queue:
        u = queue.popleft()
        seen += 1
        for v in adjacency[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    return seen == n


def feedback_number_controls():
    checked = []
    for width in range(2, 5):
        n, gates, (_g0, _g1, _common, _extra, forward, backward) = (
            strict_clone_bank_delta_one_family(0, width)
        )
        cycle_resources = tuple(forward + backward)
        assert stage_acyclic(n, gates, set(forward))
        assert stage_acyclic(n, gates, set(backward))
        for size in range(width):
            for removed in combinations(cycle_resources, size):
                assert not stage_acyclic(n, gates, set(removed)), (
                    width,
                    removed,
                )
        checked.append(width)
    return checked


def base_family_checks():
    rows = []
    for width in range(2, 9):
        for depth in (0, 1, 3, 7):
            n, gates, (g0, g1, common, extra, forward, backward) = (
                strict_clone_bank_delta_one_family(depth, width)
            )
            assert len(gates) == n + 1
            assert fixed_pair_minimum_overlap_certificate(
                n, gates, 0, g0, 0, g1, 0
            ) is None
            cert = fixed_pair_clone_bank_budget_one_certificate(
                n, gates, 0, g0, 0, g1, 0
            )
            assert isinstance(cert, CloneBankBudgetOneCertificate)
            assert cert.delta == 1
            assert set(cert.overlap) == {common, extra}
            assert forward in cert.clone_banks
            assert target_word(gates, cert.cycle0, cert.cycle1) == cert.target
            if width == 2 and depth == 0:
                brute = brute_fixed_pair(n, gates, 0, g0, 0, g1, 0)
                assert brute == (1, 2), brute
                assert not in_range(n, gates, cert.target)
            rows.append(
                {
                    "width": width,
                    "depth": depth,
                    "n": n,
                    "m": len(gates),
                    "minimum_overlap": 1,
                    "minimum_compatible_overlap": 2,
                    "feedback_gate_number": width,
                }
            )
    return rows


def random_signed_crosscheck():
    rng = random.Random(118)
    compared = accepted = rejected = 0
    for seed in range(96):
        n, base, (g0, g1, _common, _extra, forward, backward) = (
            strict_clone_bank_delta_one_family(0, 2)
        )
        gates = list(base)
        forward_sign = (
            tuple(rng.randrange(2) for _ in range(3)),
            rng.randrange(2),
        )
        backward_sign = (
            tuple(rng.randrange(2) for _ in range(3)),
            rng.randrange(2),
        )
        for gi in range(len(gates)):
            gate = gates[gi]
            if gi in (g0, g1):
                continue
            if gi in forward:
                polarity, out_flip = forward_sign
            elif gi in backward:
                polarity, out_flip = backward_sign
            else:
                polarity = tuple(rng.randrange(2) for _ in range(3))
                out_flip = rng.randrange(2)
            gates[gi] = MuxGate(
                gate.selector,
                gate.data0,
                gate.data1,
                polarity,
                out_flip,
            )
        brute = brute_fixed_pair(n, gates, 0, g0, 0, g1, 0)
        assert brute is not None
        best, compatible = brute
        expected = compatible is not None and compatible <= best + 1
        try:
            cert = fixed_pair_clone_bank_budget_one_certificate(
                n, gates, 0, g0, 0, g1, 0
            )
        except ValueError as exc:
            raise AssertionError((seed, "promised topology rejected", exc)) from exc
        assert (cert is not None) == expected, (
            seed,
            best,
            compatible,
            cert,
        )
        if cert is not None:
            assert len(cert.overlap) <= best + 1
            assert target_word(gates, cert.cycle0, cert.cycle1) == cert.target
            accepted += 1
        else:
            rejected += 1
        compared += 1
    assert accepted and rejected
    return {
        "fixed_pairs": compared,
        "accepted_within_budget": accepted,
        "rejected_within_budget": rejected,
    }


def main():
    result = {
        "strict_clone_bank_family": base_family_checks(),
        "exact_feedback_number_controls": feedback_number_controls(),
        "random_signed_crosscheck": random_signed_crosscheck(),
        "certificate": "clone_bank_loop_erasure_budget_one_dp",
        "failures": 0,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
