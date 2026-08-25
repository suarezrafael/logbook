from __future__ import annotations

import sys
from collections import deque
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
V109_DIR = ROOT / "v109"
sys.path.insert(0, str(V109_DIR))
from mux_gate_flow import MuxGate  # noqa: E402


def independent_family(depth):
    if depth < 0:
        raise ValueError(depth)
    root, d0, d1, common_selector, left, right, split, dead = range(8)
    chain = list(range(8, 8 + depth))
    n = 8 + depth
    gates = []
    first0 = len(gates)
    gates.append(MuxGate(root, d0, dead, (0, 0, 0), 0))
    first1 = len(gates)
    gates.append(MuxGate(root, d1, dead, (1, 0, 0), 0))
    gates.append(MuxGate(d0, chain[0] if chain else common_selector, dead))
    for pos, selector in enumerate(chain):
        nxt = chain[pos + 1] if pos + 1 < len(chain) else common_selector
        gates.append(MuxGate(selector, nxt, dead))
    gates.append(MuxGate(d1, common_selector, dead))
    common_gate = len(gates)
    gates.append(MuxGate(common_selector, left, right))
    feedback_extra = len(gates)
    gates.append(MuxGate(left, split, dead))
    right_gate = len(gates)
    gates.append(MuxGate(right, root, dead, (1, 0, 0), 0))
    exit0 = len(gates)
    gates.append(MuxGate(split, root, dead, (0, 0, 0), 0))
    cycle_gate = len(gates)
    gates.append(MuxGate(split, root, left, (0, 0, 0), 1))
    assert len(gates) == n + 1
    return n, gates, (
        first0,
        first1,
        common_gate,
        feedback_extra,
        right_gate,
        exit0,
        cycle_gate,
    )


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


def enumerate_returns(gates, root, start, cap=1000):
    by_selector = {}
    for gi, gate in enumerate(gates):
        if gate.selector != root:
            by_selector.setdefault(gate.selector, []).append(gi)
    out = []

    def dfs(vertex, used, path):
        if len(out) >= cap:
            return
        if vertex == root:
            out.append(tuple(path))
            return
        for gi in by_selector.get(vertex, ()):
            if gi in used:
                continue
            gate = gates[gi]
            for branch, dest in enumerate((gate.data0, gate.data1)):
                dfs(dest, used | {gi}, path + [(gi, branch)])

    dfs(start, set(), [])
    assert len(out) < cap
    return out


def exact_overlap_profile(gates, first0, first1):
    root = gates[first0].selector
    start0 = gates[first0].branch(0)[1]
    start1 = gates[first1].branch(0)[1]
    routes0 = enumerate_returns(gates, root, start0)
    routes1 = enumerate_returns(gates, root, start1)
    minimum = None
    compatible = None
    witness = None
    for route0 in routes0:
        used0 = {gi for gi, _ in route0}
        for route1 in routes1:
            overlap = len(used0 & {gi for gi, _ in route1})
            if minimum is None or overlap < minimum:
                minimum = overlap
            target = target_word(
                gates,
                ((first0, 0),) + route0,
                ((first1, 0),) + route1,
            )
            if target is not None and (
                compatible is None or overlap < compatible
            ):
                compatible = overlap
                witness = (route0, route1, target)
    return minimum, compatible, witness


def final_stage_acyclic(gates, ids, delete=None):
    (
        _first0,
        _first1,
        _common,
        feedback,
        right_gate,
        exit0,
        cycle_gate,
    ) = ids
    allowed = {feedback, right_gate, exit0, cycle_gate}
    if delete is not None:
        allowed.remove(delete)
    vertices = set()
    for gi in allowed:
        gate = gates[gi]
        vertices.add(gate.selector)
        vertices.add(gate.data0)
        vertices.add(gate.data1)
    root = gates[0].selector
    vertices.discard(root)
    indegree = {v: 0 for v in vertices}
    adj = {v: [] for v in vertices}
    for gi in allowed:
        gate = gates[gi]
        if gate.selector not in vertices:
            continue
        for dest in (gate.data0, gate.data1):
            if dest in vertices:
                adj[gate.selector].append(dest)
                indegree[dest] += 1
    queue = deque(v for v in vertices if indegree[v] == 0)
    seen = 0
    while queue:
        u = queue.popleft()
        seen += 1
        for v in adj[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    return seen == len(vertices)


def in_range(n, gates, target):
    return any(
        tuple(gate.value(x) for gate in gates) == target
        for x in product((0, 1), repeat=n)
    )


def main():
    for depth in range(61):
        n, gates, ids = independent_family(depth)
        (
            first0,
            first1,
            common_gate,
            feedback,
            _right,
            _exit0,
            cycle_gate,
        ) = ids
        assert len(gates) == n + 1
        assert not final_stage_acyclic(gates, ids)
        assert final_stage_acyclic(gates, ids, feedback)
        assert final_stage_acyclic(gates, ids, cycle_gate)
        minimum, compatible, witness = exact_overlap_profile(gates, first0, first1)
        assert minimum == 1
        assert compatible == 2
        assert witness is not None
        route0, route1, target = witness
        overlap = {gi for gi, _ in route0} & {gi for gi, _ in route1}
        assert overlap == {common_gate, feedback}
        assert cycle_gate not in {gi for gi, _ in route0}
        assert cycle_gate not in {gi for gi, _ in route1}
        assert target_word(
            gates,
            ((first0, 0),) + route0,
            ((first1, 0),) + route1,
        ) == target

    n, gates, ids = independent_family(0)
    first0, first1, *_rest = ids
    _minimum, _compatible, witness = exact_overlap_profile(gates, first0, first1)
    assert witness is not None
    assert not in_range(n, gates, witness[2])
    print(
        "V116 independent verifier passed: exact cyclic family audited "
        "through depth 60; feedback-gate deletion, Delta=1 separation, "
        "and an independent full-image target check all passed."
    )


if __name__ == "__main__":
    main()
