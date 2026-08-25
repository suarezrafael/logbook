from __future__ import annotations

import json
import sys
from collections import defaultdict, deque
from itertools import combinations
from pathlib import Path

V109_DIR = Path(__file__).resolve().parents[1] / "v109"
sys.path.insert(0, str(V109_DIR))
from mux_gate_flow import MuxGate  # noqa: E402


def family(depth, width):
    root, d0, d1, common_selector, left, right, bank_in, bank_out, dead = range(9)
    chain = list(range(9, 9 + depth))
    n = 7 + depth + 2 * width
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
    common = len(gates)
    gates.append(MuxGate(common_selector, left, right))
    extra = len(gates)
    gates.append(MuxGate(left, bank_in, dead))
    gates.append(MuxGate(right, root, dead, (1, 0, 0), 0))
    forward = []
    for _ in range(width):
        forward.append(len(gates))
        gates.append(MuxGate(bank_in, bank_out, dead))
    ordinary = len(gates)
    gates.append(MuxGate(bank_out, root, dead, (0, 0, 0), 0))
    backward = []
    for _ in range(width):
        backward.append(len(gates))
        gates.append(MuxGate(bank_out, root, bank_in, (0, 0, 0), 1))
    assert len(gates) == n + 1
    return n, gates, (first0, first1, common, extra, tuple(forward), tuple(backward), ordinary)


def target_word(gates, cycle0, cycle1):
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
    return assigned


def paths(gates, root, start, limit=20000):
    by_selector = defaultdict(list)
    for gi, gate in enumerate(gates):
        if gate.selector != root:
            by_selector[gate.selector].append(gi)
    output = []

    def dfs(variable, path, used):
        if len(output) >= limit:
            return
        if variable == root:
            output.append(tuple(path))
            return
        for gi in by_selector[variable]:
            if gi in used:
                continue
            for branch in (0, 1):
                dfs(
                    gates[gi].branch(branch)[1],
                    path + [(gi, branch)],
                    used | {gi},
                )

    dfs(start, [], set())
    assert len(output) < limit
    return list(dict.fromkeys(output))


def brute(n, gates, g0, g1):
    p0 = paths(gates, 0, gates[g0].branch(0)[1])
    p1 = paths(gates, 0, gates[g1].branch(0)[1])
    best = len(gates) + 1
    compatible = len(gates) + 1
    for route0 in p0:
        used0 = {gi for gi, _ in route0}
        for route1 in p1:
            overlap = len(used0 & {gi for gi, _ in route1})
            best = min(best, overlap)
            if target_word(gates, ((g0, 0),) + route0, ((g1, 0),) + route1) is not None:
                compatible = min(compatible, overlap)
    return best, compatible, p0, p1


def acyclic(n, gates, removed):
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


def exact_feedback_controls():
    for width in range(2, 5):
        n, gates, (_g0, _g1, _common, _extra, forward, backward, _ordinary) = family(0, width)
        candidates = forward + backward
        assert acyclic(n, gates, set(forward))
        assert acyclic(n, gates, set(backward))
        for size in range(width):
            for subset in combinations(candidates, size):
                assert not acyclic(n, gates, set(subset))


def normalize_bank_route(gates, route, extra, forward, backward):
    if extra not in {gi for gi, _ in route}:
        return route
    qpos = next(i for i, (gi, _b) in enumerate(route) if gi == extra)
    prefix = route[: qpos + 1]
    suffix = route[qpos + 1 :]
    fpositions = [i for i, (gi, b) in enumerate(suffix) if gi in forward and b == 0]
    if len(fpositions) <= 1:
        return route
    first = fpositions[0]
    last_exit = None
    for pos in range(first + 1, len(suffix)):
        gi, branch = suffix[pos]
        if gi in backward and branch == 0:
            last_exit = suffix[pos]
        elif gi not in backward and gi not in forward:
            last_exit = suffix[pos]
    assert last_exit is not None
    return prefix + (suffix[first], last_exit)


def valid_route(gates, root, start, route):
    current = start
    used = set()
    for gi, branch in route:
        if gi in used or gates[gi].selector != current:
            return False
        used.add(gi)
        current = gates[gi].branch(branch)[1]
    return current == root


def loop_erasure_controls():
    _n, gates, (g0, _g1, _common, extra, forward, backward, _ordinary) = family(0, 3)
    start = gates[g0].branch(0)[1]
    audited = reduced = 0
    for route in paths(gates, 0, start):
        if extra not in {gi for gi, _ in route}:
            continue
        norm = normalize_bank_route(gates, route, extra, forward, backward)
        assert valid_route(gates, 0, start, norm)
        original_after_q = route[next(i for i, (gi, _b) in enumerate(route) if gi == extra) + 1]
        norm_after_q = norm[next(i for i, (gi, _b) in enumerate(norm) if gi == extra) + 1]
        assert gates[original_after_q[0]].branch(original_after_q[1])[2] == gates[norm_after_q[0]].branch(norm_after_q[1])[2]
        assert len({gi for gi, _ in norm if gi in forward}) <= 1
        audited += 1
        reduced += int(len(norm) < len(route))
    assert audited and reduced
    return audited, reduced


def main():
    rows = []
    for width in (2, 3):
        n, gates, (g0, g1, _common, _extra, _forward, _backward, _ordinary) = family(0, width)
        best, compatible, _p0, _p1 = brute(n, gates, g0, g1)
        assert (best, compatible) == (1, 2)
        rows.append({"width": width, "n": n, "m": len(gates), "minimum_overlap": best, "minimum_compatible_overlap": compatible})
    for width in range(2, 11):
        for depth in (0, 2, 6):
            n, gates, _ids = family(depth, width)
            assert len(gates) == n + 1
    exact_feedback_controls()
    audited, reduced = loop_erasure_controls()
    print(json.dumps({
        "bruteforce_family": rows,
        "exact_feedback_number_widths": [2, 3, 4],
        "loop_erasure_routes_audited": audited,
        "strictly_shortened_routes": reduced,
        "independent_of_v118_solver": True,
        "failures": 0,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
