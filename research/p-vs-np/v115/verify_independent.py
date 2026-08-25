from __future__ import annotations

import json
import sys
from collections import defaultdict, deque
from itertools import product
from pathlib import Path

V109_DIR = Path(__file__).resolve().parents[1] / "v109"
sys.path.insert(0, str(V109_DIR))
from mux_gate_flow import MuxGate  # noqa: E402


def build_family(depth: int):
    if depth < 0:
        raise ValueError(depth)
    root, d0, d1, common_selector, left, right, split, dead = range(8)
    chain = list(range(8, 8 + depth))
    n = 8 + depth
    gates = []
    first0 = len(gates); gates.append(MuxGate(root, d0, dead, (0, 0, 0), 0))
    first1 = len(gates); gates.append(MuxGate(root, d1, dead, (1, 0, 0), 0))
    gates.append(MuxGate(d0, chain[0] if chain else common_selector, dead))
    for j, selector in enumerate(chain):
        nxt = chain[j + 1] if j + 1 < len(chain) else common_selector
        gates.append(MuxGate(selector, nxt, dead))
    gates.append(MuxGate(d1, common_selector, dead))
    common = len(gates); gates.append(MuxGate(common_selector, left, right))
    extra = len(gates); gates.append(MuxGate(left, split, dead))
    gates.append(MuxGate(right, root, dead, (1, 0, 0), 0))
    gates.append(MuxGate(split, root, dead, (0, 0, 0), 0))
    gates.append(MuxGate(split, root, dead, (0, 0, 0), 1))
    assert len(gates) == n + 1
    return n, gates, (first0, first1, common, extra)


def target_word(gates, cycle0, cycle1):
    word = [0] * len(gates)
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
            word[gi] = bit
    return tuple(word)


def returns(n, gates, root, start, cap=5000):
    by = defaultdict(list)
    for gi, gate in enumerate(gates):
        if gate.selector != root:
            by[gate.selector].append(gi)
    out = []

    def dfs(var, used, path):
        if len(out) >= cap:
            return
        if var == root:
            out.append(tuple(path))
            return
        for gi in by[var]:
            if gi in used:
                continue
            used.add(gi)
            for branch in (0, 1):
                path.append((gi, branch))
                dfs(gates[gi].branch(branch)[1], used, path)
                path.pop()
            used.remove(gi)

    dfs(start, set(), [])
    if len(out) >= cap:
        raise AssertionError("independent route census exceeded cap")
    return list(dict.fromkeys(out))


def optimum(n, gates, root, g0, b0, g1, b1):
    p0 = returns(n, gates, root, gates[g0].branch(b0)[1])
    p1 = returns(n, gates, root, gates[g1].branch(b1)[1])
    best = len(gates) + 1
    best_compatible = len(gates) + 1
    witness = None
    for a in p0:
        sa = {gi for gi, _ in a}
        for b in p1:
            overlap = len(sa & {gi for gi, _ in b})
            best = min(best, overlap)
            target = target_word(gates, ((g0, b0),) + a, ((g1, b1),) + b)
            if target is not None and overlap < best_compatible:
                best_compatible = overlap
                witness = (a, b, target)
    return best, best_compatible, witness


def full_image_missing(n, gates, target):
    for x in product((0, 1), repeat=n):
        if tuple(g.value(x) for g in gates) == target:
            return False
    return True


def branch_graph_acyclic(n, gates, root):
    # For the family, delete root-selector outputs. Wrong branches end at a
    # dead sink, and the remaining graph must have no directed cycle.
    adjacency = [[] for _ in range(n)]
    indegree = [0] * n
    for gate in gates:
        if gate.selector == root:
            continue
        for dest in (gate.data0, gate.data1):
            adjacency[gate.selector].append(dest)
            indegree[dest] += 1
    queue = deque(i for i in range(n) if indegree[i] == 0)
    seen = 0
    while queue:
        u = queue.popleft(); seen += 1
        for v in adjacency[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    return seen == n


def family_census():
    rows = []
    for depth in range(0, 61):
        n, gates, (g0, g1, common, extra) = build_family(depth)
        best, compatible, witness = optimum(n, gates, 0, g0, 0, g1, 0)
        assert best == 1
        assert compatible == 2
        assert witness is not None
        a, b, target = witness
        overlap = {gi for gi, _ in a} & {gi for gi, _ in b}
        assert overlap == {common, extra}
        assert branch_graph_acyclic(n, gates, 0)
        if depth == 0:
            assert full_image_missing(n, gates, target)
        rows.append((depth, n, len(gates)))
    return rows


def cross_prefix_suffix_lemma_audit():
    # Every compatible minimum+1 witness in the family has one unique
    # non-dominator shared gate. Audit that no gate occurs on a prefix to that
    # gate and on either suffix after it, the finite shadow of the DAG lemma.
    checked = 0
    for depth in range(0, 31):
        n, gates, (g0, g1, common, extra) = build_family(depth)
        p0 = returns(n, gates, 0, gates[g0].branch(0)[1])
        p1 = returns(n, gates, 0, gates[g1].branch(0)[1])
        for a in p0:
            for b in p1:
                overlap = {gi for gi, _ in a} & {gi for gi, _ in b}
                if overlap != {common, extra}:
                    continue
                if target_word(gates, ((g0, 0),) + a, ((g1, 0),) + b) is None:
                    continue
                ia = next(i for i, (gi, _br) in enumerate(a) if gi == extra)
                ib = next(i for i, (gi, _br) in enumerate(b) if gi == extra)
                pre = {gi for gi, _ in a[:ia]} | {gi for gi, _ in b[:ib]}
                post = {gi for gi, _ in a[ia + 1:]} | {gi for gi, _ in b[ib + 1:]}
                assert not (pre & post)
                checked += 1
    assert checked >= 60
    return checked


def main():
    rows = family_census()
    result = {
        "independent_family_depths": len(rows),
        "largest_family_n": rows[-1][1],
        "largest_family_m": rows[-1][2],
        "prefix_suffix_lemma_witnesses": cross_prefix_suffix_lemma_audit(),
        "depth0_full_image_check": True,
        "imports_v115_code": False,
        "failures": 0,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
