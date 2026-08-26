from __future__ import annotations

import json
import sys
from collections import defaultdict, deque
from itertools import combinations
from pathlib import Path

from mux_branch_image_bank import (
    BranchImageBudgetOneCertificate,
    fixed_pair_branch_image_budget_one_certificate,
    strict_branch_image_delta_one_family,
)

V109_DIR = Path(__file__).resolve().parents[1] / "v109"
V113_DIR = Path(__file__).resolve().parents[1] / "v113"
V118_DIR = Path(__file__).resolve().parents[1] / "v118"
sys.path.insert(0, str(V109_DIR))
sys.path.insert(0, str(V113_DIR))
sys.path.insert(0, str(V118_DIR))
from mux_gate_flow import MuxGate, in_range  # noqa: E402
from mux_dominator_dp import fixed_pair_minimum_overlap_certificate  # noqa: E402
from mux_clone_bank import fixed_pair_clone_bank_budget_one_certificate  # noqa: E402


def target_word(gates, cycle0, cycle1):
    target = [0] * len(gates)
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
            target[gi] = bit
    return tuple(target)


def enumerate_gate_simple_paths(n, gates, root, start, limit=100000):
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
    compatible = len(gates) + 1
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
                compatible = min(compatible, overlap)
    return best, None if compatible > len(gates) else compatible


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


def exact_feedback_number_controls():
    checked = []
    for width in range(2, 5):
        n, gates, (_g0, _g1, _common, _extra, forward, backward) = (
            strict_branch_image_delta_one_family(0, width)
        )
        cycle_resources = tuple(forward + backward)
        assert stage_acyclic(n, gates, set(forward))
        assert stage_acyclic(n, gates, set(backward))
        for size in range(width):
            for removed in combinations(cycle_resources, size):
                assert not stage_acyclic(n, gates, set(removed)), (width, removed)
        checked.append(width)
    return checked


def strict_family_checks():
    rows = []
    for width in range(2, 9):
        for depth in (0, 1, 3, 7):
            n, gates, (g0, g1, common, extra, forward, backward) = (
                strict_branch_image_delta_one_family(depth, width)
            )
            assert len(gates) == n + 1
            assert fixed_pair_minimum_overlap_certificate(
                n, gates, 0, g0, 0, g1, 0
            ) is None
            try:
                fixed_pair_clone_bank_budget_one_certificate(
                    n, gates, 0, g0, 0, g1, 0
                )
            except ValueError:
                pass
            else:
                raise AssertionError(
                    ("V118 unexpectedly accepts its structural promise", width, depth)
                )

            cert = fixed_pair_branch_image_budget_one_certificate(
                n, gates, 0, g0, 0, g1, 0, image_bound=2
            )
            assert isinstance(cert, BranchImageBudgetOneCertificate)
            assert cert.delta == 1
            assert set(cert.overlap) == {common, extra}
            assert any(len(D) == 2 for D in cert.image_sets)
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


def signed_private_variants():
    """Vary only private data signs/out flips; selector phases stay fixed."""
    compared = 0
    seen_signatures = set()
    for seed in range(32):
        n, base, (g0, g1, common, extra, forward, backward) = (
            strict_branch_image_delta_one_family(0, 2)
        )
        gates = list(base)
        private = tuple(forward + backward)
        for pos, gi in enumerate(private):
            gate = gates[gi]
            ps, _p0, _p1 = gate.polarity
            shift = 3 * pos
            p0 = (seed >> shift) & 1
            p1 = (seed >> (shift + 1)) & 1
            out_flip = (seed >> (shift + 2)) & 1
            gates[gi] = MuxGate(
                gate.selector,
                gate.data0,
                gate.data1,
                (ps, p0, p1),
                out_flip,
            )
        signature = tuple(
            (gates[gi].polarity[1], gates[gi].polarity[2], gates[gi].out_flip)
            for gi in private
        )
        assert signature not in seen_signatures, ("duplicate private-sign seed", seed)
        seen_signatures.add(signature)
        brute = brute_fixed_pair(n, gates, 0, g0, 0, g1, 0)
        assert brute == (1, 2), (seed, brute)
        cert = fixed_pair_branch_image_budget_one_certificate(
            n, gates, 0, g0, 0, g1, 0, image_bound=2
        )
        assert cert is not None
        assert set(cert.overlap) == {common, extra}
        assert target_word(gates, cert.cycle0, cert.cycle1) == cert.target
        compared += 1
    assert len(seen_signatures) == 32
    return compared


def smaller_image_bound_rejection():
    n, gates, (g0, g1, _common, _extra, _forward, _backward) = (
        strict_branch_image_delta_one_family(0, 2)
    )
    try:
        fixed_pair_branch_image_budget_one_certificate(
            n, gates, 0, g0, 0, g1, 0, image_bound=1
        )
    except ValueError:
        return True
    raise AssertionError("image_bound=1 unexpectedly accepted the strict family")


def main():
    result = {
        "strict_branch_image_family": strict_family_checks(),
        "exact_feedback_number_controls": exact_feedback_number_controls(),
        "private_signed_variants": signed_private_variants(),
        "smaller_image_bound_rejection": smaller_image_bound_rejection(),
        "certificate": "bounded_branch_image_loop_erasure_budget_one_dp",
        "failures": 0,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
