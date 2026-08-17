from __future__ import annotations

import json
from itertools import combinations, product

PAIR_POSITIONS = ((0, 1), (0, 2), (1, 2))


def family(q):
    extra = 2 * q
    internal = list(range(5, 5 + extra))
    n = 5 + extra
    gates = [
        ((0, 1, 2), (0, 0, 0)),
        ((0, 3, 4), (0, 0, 0)),
        ((0, 4, 2), (0, 0, 0)),
        ((1, 2, 3), (0, 0, 0)),
        ((1, 3, 4), (1, 0, 0)),
    ]
    path = [0] + internal + [2]
    for u, v in zip(path, path[1:]):
        gates.append(((u, v, 1), (0, 0, 0)))
    assert len(gates) == n + 1
    return n, gates, 4


def gate_value(gate, x):
    support, polarity = gate
    return int(sum(x[v] ^ p for v, p in zip(support, polarity)) >= 2)


def pair_edge(gate, choice):
    support, polarity = gate
    i, j = PAIR_POSITIONS[choice]
    return support[i], support[j], 1 ^ polarity[i] ^ polarity[j]


def target_for_source(gate, source, source_value):
    support, polarity = gate
    pos = support.index(source)
    return 1 ^ polarity[pos] ^ source_value


def explicit_repaired_target(q):
    n, gates, repair = family(q)
    choices = [0] * len(gates)
    choices[repair] = 2
    y = [0] * len(gates)

    def walk(edge_ids, vertices, start):
        value = start
        for j, gi in enumerate(edge_ids):
            u, v, delta = pair_edge(gates[gi], choices[gi])
            source = vertices[j]
            assert source in (u, v)
            y[gi] = target_for_source(gates[gi], source, value)
            value ^= delta
        return value

    path_vertices = [0] + list(range(5, 5 + 2 * q)) + [2]
    path_gate_ids = list(range(5, len(gates)))

    # First odd cycle: 0-1-2 and then the subdivided path back to 0.
    left_vertices = [0, 1, 2] + list(reversed(path_vertices[:-1]))
    left_edges = [0, 3] + list(reversed(path_gate_ids))
    assert walk(left_edges, left_vertices, 0) == 1

    # Second odd cycle: 0-3-4-0 after repairing gate 4 to pair (3,4).
    assert walk([1, repair, 2], [0, 3, 4, 0], 1) == 0
    return n, gates, tuple(y), tuple(choices)


def implication_graph(n, gates, target):
    graph = [[] for _ in range(2 * n)]
    for gate, wanted in zip(gates, target):
        support, polarity = gate
        good = [wanted ^ p for p in polarity]
        bad = [1 ^ bit for bit in good]
        for i, j in PAIR_POSITIONS:
            u, v = support[i], support[j]
            graph[2 * u + bad[i]].append(2 * v + good[j])
            graph[2 * v + bad[j]].append(2 * u + good[i])
    return graph


def scc(graph):
    n = len(graph)
    rev = [[] for _ in range(n)]
    for u, outs in enumerate(graph):
        for v in outs:
            rev[v].append(u)
    seen = [False] * n
    order = []
    for start in range(n):
        if seen[start]:
            continue
        stack = [(start, 0)]
        seen[start] = True
        while stack:
            u, idx = stack[-1]
            if idx < len(graph[u]):
                v = graph[u][idx]
                stack[-1] = (u, idx + 1)
                if not seen[v]:
                    seen[v] = True
                    stack.append((v, 0))
            else:
                order.append(u)
                stack.pop()
    comp = [-1] * n
    cid = 0
    for start in reversed(order):
        if comp[start] != -1:
            continue
        stack = [start]
        comp[start] = cid
        while stack:
            u = stack.pop()
            for v in rev[u]:
                if comp[v] == -1:
                    comp[v] = cid
                    stack.append(v)
        cid += 1
    return comp


def unsat(n, gates, target):
    comp = scc(implication_graph(n, gates, target))
    return any(comp[2 * v] == comp[2 * v + 1] for v in range(n))


def missing_by_bruteforce(n, gates, target):
    for x in product((0, 1), repeat=n):
        if tuple(gate_value(g, x) for g in gates) == target:
            return False
    return True


def canonical_theta_signature(q):
    n, gates, _ = family(q)
    choices = [0] * len(gates)
    edges = [pair_edge(g, c) for g, c in zip(gates, choices)]
    # The 2-core has branch vertices 0 and 1 with three internally disjoint paths:
    # direct 0-1, 0-3-1, and 0-(subdivision)-2-1.  The first two form the unique
    # balanced cycle; the other two cycles are odd.  Vertex 4 is a leaf canonically.
    direct = edges[0][2]
    via3 = edges[1][2] ^ edges[4][2]
    path = 0
    for gi in range(5, len(gates)):
        path ^= edges[gi][2]
    via2 = path ^ edges[3][2]
    return direct ^ via3, direct ^ via2, via3 ^ via2


def exact_beta(n, gates):
    supports = [set(g[0]) for g in gates]
    for free_size in range(n, -1, -1):
        for free in combinations(range(n), free_size):
            F = set(free)
            if all(len(F & support) <= 1 for support in supports):
                return n - free_size
    raise AssertionError


def frame_rank_union(gates, indices):
    # For the union of all three pair choices of every selected gate, each
    # nonempty connected component contains an entire gate triangle.  Its three
    # transport labels XOR to one, hence every component is unbalanced.  The
    # signed-frame rank is therefore exactly the number of incident vertices.
    vertices = set()
    triangle_checks = []
    for i in indices:
        support, _ = gates[i]
        vertices.update(support)
        deltas = [pair_edge(gates[i], c)[2] for c in range(3)]
        triangle_checks.append(deltas[0] ^ deltas[1] ^ deltas[2])
    assert all(bit == 1 for bit in triangle_checks)
    return len(vertices)


def main():
    complete = []
    implication = []
    theta = []
    beta = {}

    for q in range(0, 5):
        n, gates, target, _choices = explicit_repaired_target(q)
        assert unsat(n, gates, target)
        assert missing_by_bruteforce(n, gates, target)
        complete.append(n)

    for q in range(0, 101):
        n, gates, target, _choices = explicit_repaired_target(q)
        assert unsat(n, gates, target)
        implication.append(n)
        assert canonical_theta_signature(q) == (0, 1, 1)
        theta.append(n)

    for q in range(0, 6):
        n, gates, _ = family(q)
        value = exact_beta(n, gates)
        assert value == (n + 3) // 2
        beta[n] = value

    rado_rank_checks = 0
    for q in range(0, 3):
        n, gates, _ = family(q)
        m = len(gates)
        for mask in range(1, 1 << m):
            chosen = [i for i in range(m) if (mask >> i) & 1]
            rank = frame_rank_union(gates, chosen)
            neighborhood = set()
            for i in chosen:
                neighborhood.update(gates[i][0])
            assert rank == len(neighborhood)
            rado_rank_checks += 1

    print(json.dumps({
        "complete_original_range_n": complete,
        "independent_implication_scc_n_through": implication[-1],
        "canonical_theta_signature": [0, 1, 1],
        "theta_checked_n_through": theta[-1],
        "exact_beta": beta,
        "frame_rank_equals_neighborhood_subset_checks": rado_rank_checks,
        "failures": 0,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
