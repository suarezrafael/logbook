from __future__ import annotations

import json
import random
import sys
from collections import defaultdict, deque
from itertools import combinations
from pathlib import Path

V109_DIR = Path(__file__).resolve().parents[1] / "v109"
sys.path.insert(0, str(V109_DIR))
from mux_gate_flow import MuxGate  # noqa: E402


def rebuild_family(depth: int, width: int):
    if depth < 0 or width < 2:
        raise ValueError
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
    for i in range(width):
        forward.append(len(gates))
        gates.append(
            MuxGate(
                bank_in,
                bank_out,
                dead,
                (0, i & 1, (i >> 1) & 1),
                (i >> 2) & 1,
            )
        )
    exit_gate = len(gates)
    gates.append(MuxGate(bank_out, root, dead))

    backward = []
    for i in range(width):
        backward.append(len(gates))
        gates.append(
            MuxGate(
                bank_out,
                root,
                bank_in,
                (0, i & 1, (i >> 1) & 1),
                1 ^ ((i >> 2) & 1),
            )
        )
    assert len(gates) == n + 1
    return n, gates, (
        first0,
        first1,
        common,
        extra,
        tuple(forward),
        tuple(backward),
        exit_gate,
        bank_in,
        bank_out,
        dead,
    )


def target_word(gates, cycle0, cycle1):
    assigned = {}
    out = [0] * len(gates)
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
            out[gi] = bit
    return tuple(out)


def enumerate_paths(gates, root, start, limit=200000):
    by = defaultdict(list)
    for gi, gate in enumerate(gates):
        if gate.selector != root:
            by[gate.selector].append(gi)
    paths = []

    def dfs(var, path, used):
        if len(paths) >= limit:
            return
        if var == root:
            paths.append(tuple(path))
            return
        if len(path) >= len(gates):
            return
        for gi in by[var]:
            if gi in used:
                continue
            for branch in (0, 1):
                dfs(
                    gates[gi].branch(branch)[1],
                    path + [(gi, branch)],
                    used | {gi},
                )

    dfs(start, [], set())
    if len(paths) >= limit:
        raise AssertionError("path cap reached")
    return list(dict.fromkeys(paths))


def brute_pair(n, gates, g0, g1):
    p0 = enumerate_paths(gates, 0, gates[g0].branch(0)[1])
    p1 = enumerate_paths(gates, 0, gates[g1].branch(0)[1])
    best = len(gates) + 1
    compatible = len(gates) + 1
    for route0 in p0:
        used0 = {gi for gi, _ in route0}
        for route1 in p1:
            overlap = len(used0 & {gi for gi, _ in route1})
            best = min(best, overlap)
            if target_word(
                gates,
                ((g0, 0),) + route0,
                ((g1, 0),) + route1,
            ) is not None:
                compatible = min(compatible, overlap)
    return best, compatible, len(p0), len(p1)


def acyclic_without(gates, removed):
    n = 1 + max(
        x for gate in gates for x in (gate.selector, gate.data0, gate.data1)
    )
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
    checked = []
    for width in range(2, 5):
        _n, gates, meta = rebuild_family(0, width)
        forward, backward = meta[4], meta[5]
        resources = tuple(forward + backward)
        assert acyclic_without(gates, set(forward))
        assert acyclic_without(gates, set(backward))
        for size in range(width):
            for removed in combinations(resources, size):
                assert not acyclic_without(gates, set(removed))
        checked.append(width)
    return checked


def exact_clone_rejection_controls():
    checked = []
    for width in range(2, 7):
        _n, gates, meta = rebuild_family(0, width)
        cycle_resources = set(meta[4] + meta[5])
        groups = defaultdict(set)
        for gi in cycle_resources:
            gate = gates[gi]
            groups[
                (
                    gate.selector,
                    gate.data0,
                    gate.data1,
                    gate.polarity,
                    gate.out_flip,
                )
            ].add(gi)
        assert len(groups) >= 4
        for group in groups.values():
            assert not acyclic_without(gates, group)
        checked.append((width, len(groups)))
    return checked


def branch_image_controls():
    rows = []
    for width in range(2, 7):
        _n, gates, meta = rebuild_family(0, width)
        forward, backward = meta[4], meta[5]
        bank_in, bank_out, dead = meta[7], meta[8], meta[9]
        D_forward = {bank_out, dead}
        detected = {
            gi
            for gi, gate in enumerate(gates)
            if gate.data0 in D_forward and gate.data1 in D_forward
        }
        assert set(forward) <= detected
        assert acyclic_without(gates, detected)
        D_backward = {0, bank_in}
        detected_back = {
            gi
            for gi, gate in enumerate(gates)
            if gate.data0 in D_backward and gate.data1 in D_backward
        }
        assert set(backward) <= detected_back
        assert acyclic_without(gates, detected_back)
        rows.append((width, len(detected), len(detected_back)))
    return rows


def erase_repeated_bank_destinations(gates, path, bank):
    path = list(path)
    while True:
        first = {}
        erased = False
        for pos, (gi, branch) in enumerate(path):
            if gi not in bank:
                continue
            dest = gates[gi].branch(branch)[1]
            if dest in first:
                i = first[dest]
                del path[i + 1 : pos + 1]
                erased = True
                break
            first[dest] = pos
        if not erased:
            return tuple(path)


def validate_path(gates, root, start, path):
    current = start
    used = set()
    for gi, branch in path:
        if gi in used or gates[gi].selector != current:
            return False
        used.add(gi)
        current = gates[gi].branch(branch)[1]
    return current == root


def loop_erasure_audit():
    rng = random.Random(9119)
    _n, base, meta = rebuild_family(0, 3)
    forward, backward, bank_in = meta[4], meta[5], meta[7]
    gates = list(base)
    for gi in tuple(forward + backward):
        gate = gates[gi]
        gates[gi] = MuxGate(
            gate.selector,
            gate.data0,
            gate.data1,
            tuple(rng.randrange(2) for _ in range(3)),
            rng.randrange(2),
        )

    paths = enumerate_paths(gates, 0, bank_in)
    bank = set(forward + backward)
    checked = shortened = 0
    for path in paths:
        normalized = erase_repeated_bank_destinations(gates, path, bank)
        assert validate_path(gates, 0, bank_in, normalized)
        if path:
            assert normalized and normalized[0] == path[0]
        destinations = [
            gates[gi].branch(branch)[1]
            for gi, branch in normalized
            if gi in bank
        ]
        assert len(destinations) == len(set(destinations))
        assert len(destinations) <= 2
        checked += 1
        shortened += len(normalized) < len(path)
    assert checked and shortened
    return {"routes": checked, "strictly_shortened": shortened}


def main():
    brute = []
    for width in (2, 3):
        n, gates, meta = rebuild_family(0, width)
        best, compatible, p0, p1 = brute_pair(n, gates, meta[0], meta[1])
        assert (best, compatible) == (1, 2)
        brute.append(
            {
                "width": width,
                "n": n,
                "m": len(gates),
                "minimum_overlap": best,
                "minimum_compatible_overlap": compatible,
                "route_counts": [p0, p1],
            }
        )

    result = {
        "imports_v119_code": False,
        "bruteforce_family": brute,
        "feedback_number": exact_feedback_controls(),
        "exact_clone_rejection": exact_clone_rejection_controls(),
        "branch_image_detection": branch_image_controls(),
        "loop_erasure": loop_erasure_audit(),
        "failures": 0,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
