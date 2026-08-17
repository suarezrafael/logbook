from __future__ import annotations

import json
import random
from itertools import product


def majority(bits):
    return 1 if sum(bits) >= 2 else 0


def family(r, randomize=False, rng=None):
    a0, a1, a2 = 0, 1, 2
    path_internal = list(range(3, 3 + r))
    b0, b1, b2 = 3 + r, 4 + r, 5 + r
    n = r + 6
    gates = []

    def add(support, polarity=(0, 0, 0)):
        if randomize:
            q = rng.randrange(2)
            polarity = (q, q, rng.randrange(2))
        gates.append((tuple(support), tuple(polarity)))

    if randomize:
        add((a0, a1, a2))
    else:
        add((a0, a1, a2), (0, 0, 1))
    add((a1, a2, a0))
    add((a2, a0, a1))

    path = [a0] + path_internal + [b0]
    for i in range(len(path) - 1):
        third = path[i + 2] if i + 2 < len(path) else b1
        add((path[i], path[i + 1], third))

    add((b0, b1, b2))
    add((b1, b2, b0))
    add((b2, b0, b1))
    assert len(gates) == n + 1
    return n, gates


def value(gate, x):
    support, polarity = gate
    return majority(tuple(x[v] ^ p for v, p in zip(support, polarity)))


def implication_graph(n, gates, targets):
    # Literal node 2*v+b means proposition x_v=b.
    graph = [[] for _ in range(2 * n)]
    for gate, target in zip(gates, targets):
        support, polarity = gate
        good = [target ^ p for p in polarity]
        bad = [1 ^ g for g in good]
        for i in range(3):
            for j in range(i + 1, 3):
                u, v = support[i], support[j]
                # The target-majority condition forbids both endpoint bad values.
                graph[2 * u + bad[i]].append(2 * v + good[j])
                graph[2 * v + bad[j]].append(2 * u + good[i])
    return graph


def strongly_connected_components(graph):
    n = len(graph)
    reverse = [[] for _ in range(n)]
    for u, outs in enumerate(graph):
        for v in outs:
            reverse[v].append(u)

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
            for v in reverse[u]:
                if comp[v] == -1:
                    comp[v] = cid
                    stack.append(v)
        cid += 1
    return comp


def unsat_2sat(n, gates, targets):
    graph = implication_graph(n, gates, targets)
    comp = strongly_connected_components(graph)
    return any(comp[2 * v] == comp[2 * v + 1] for v in range(n))


def alternating_target(m):
    return tuple(1 if i % 2 == 0 else 0 for i in range(m))


def brute_missing(n, gates, target):
    for x in product((0, 1), repeat=n):
        if tuple(value(g, x) for g in gates) == target:
            return False
    return True


def deterministic_family_checks():
    brute = []
    for r in range(2, 10):
        n, gates = family(r)
        target = alternating_target(n + 1)
        assert unsat_2sat(n, gates, target)
        assert brute_missing(n, gates, target)
        brute.append(n)

    symbolic = []
    for r in range(2, 101):
        n, gates = family(r)
        target = alternating_target(n + 1)
        assert unsat_2sat(n, gates, target)
        symbolic.append(n)
    return {"complete_range_n": brute, "implication_scc_n_through": symbolic[-1]}


def randomized_checks():
    rng = random.Random(505105)
    cases = 0
    for r, trials in ((2, 120), (3, 90), (4, 30)):
        for _ in range(trials):
            n, gates = family(r, randomize=True, rng=rng)
            targets = [0] * len(gates)

            def apply(edge_ids, vertices, start_value):
                value_now = start_value
                for j, ei in enumerate(edge_ids):
                    support, polarity = gates[ei]
                    source = vertices[j]
                    pos = support.index(source)
                    targets[ei] = 1 ^ polarity[pos] ^ value_now
                    p0, p1 = polarity[0], polarity[1]
                    value_now ^= 1 ^ p0 ^ p1
                return value_now

            end_left = apply([0, 1, 2], [0, 1, 2, 0], 0)
            assert end_left == 1
            path_len = r + 1
            path_vertices = [0] + list(range(3, 3 + r)) + [3 + r]
            b = apply(list(range(3, 3 + path_len)), path_vertices, 1)
            base = 3 + path_len
            b0, b1, b2 = 3 + r, 4 + r, 5 + r
            end_right = apply([base, base + 1, base + 2], [b0, b1, b2, b0], b)
            assert end_right == (b ^ 1)

            target = tuple(targets)
            assert unsat_2sat(n, gates, target)
            assert brute_missing(n, gates, target)
            cases += 1
    assert cases == 240
    return cases


def pair_clause_unsat(n, edges, signs, choices):
    # One canonical majority pair clause per edge.  `choices[i]=a` selects the
    # source polarity in x_u=a -> x_v=a XOR delta_e.
    graph = [[] for _ in range(2 * n)]
    for (u, v), delta, a in zip(edges, signs, choices):
        b = a ^ delta
        graph[2 * u + a].append(2 * v + b)
        graph[2 * v + (1 ^ b)].append(2 * u + (1 ^ a))
    comp = strongly_connected_components(graph)
    return any(comp[2 * x] == comp[2 * x + 1] for x in range(n))


def pair_support_has_unsat(n, edges, signs):
    for choices in product((0, 1), repeat=len(edges)):
        if pair_clause_unsat(n, edges, signs, choices):
            return True
    return False


def cycle_parity(edges, signs, cycle):
    index = {tuple(sorted(edge)): i for i, edge in enumerate(edges)}
    value = 0
    for edge in cycle:
        value ^= signs[index[tuple(sorted(edge))]]
    return value


def graphsat_obstruction_sign_census():
    # The four simple support obstructions are the Karve--Hirani forbidden
    # topological-minor skeletons.  Here we classify the stricter V105 setting
    # where each edge permits only the two complementary majority pair clauses.
    skeletons = {
        "K4": (
            4,
            [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)],
            [
                [(0,1),(0,2),(1,2)],
                [(0,1),(0,3),(1,3)],
                [(0,2),(0,3),(2,3)],
                [(1,2),(1,3),(2,3)],
            ],
        ),
        "Butterfly": (
            5,
            [(0,1),(0,2),(0,3),(0,4),(1,2),(3,4)],
            [
                [(0,1),(0,2),(1,2)],
                [(0,3),(0,4),(3,4)],
            ],
        ),
        "Bowtie": (
            6,
            [(0,1),(0,2),(1,2),(2,3),(3,4),(3,5),(4,5)],
            [
                [(0,1),(0,2),(1,2)],
                [(3,4),(3,5),(4,5)],
            ],
        ),
        "K113": (
            5,
            [(0,1),(0,2),(0,3),(0,4),(1,2),(1,3),(1,4)],
            [
                [(0,1),(0,2),(1,2)],
                [(0,1),(0,3),(1,3)],
                [(0,1),(0,4),(1,4)],
            ],
        ),
    }
    counts = {}
    for name, (n, edges, cycles) in skeletons.items():
        good = 0
        for signs in product((0, 1), repeat=len(edges)):
            actual = pair_support_has_unsat(n, edges, signs)
            parities = tuple(cycle_parity(edges, signs, cycle) for cycle in cycles)
            if name == "K4":
                expected = parities == (1, 1, 1, 1)
            elif name in ("Butterfly", "Bowtie"):
                expected = parities == (1, 1)
            else:
                expected = sum(parities) == 2
            assert actual == expected, (name, signs, parities, actual)
            good += int(actual)
        counts[name] = good
    assert counts == {"K4": 8, "Butterfly": 16, "Bowtie": 32, "K113": 48}
    return counts


def main():
    result = {
        "deterministic": deterministic_family_checks(),
        "independent_random_polarity_cases": randomized_checks(),
        "signed_graphsat_obstruction_good_signings": graphsat_obstruction_sign_census(),
        "failures": 0,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
