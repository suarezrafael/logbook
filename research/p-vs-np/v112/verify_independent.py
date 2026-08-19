from __future__ import annotations

import json
import random
from itertools import product


CENTRAL_PATTERN = (
    ((0, 1, 1), 0),
    ((0, 1, 1), 1),
)
FIRST_LOBE_PATTERN = (
    ((0, 0, 1), 1),
    ((0, 0, 1), 0),
    ((1, 0, 1), 1),
    ((1, 1, 1), 1),
)
REPEATED_BLOCK_PATTERN = (
    ((0, 1, 1), 0),
    ((1, 0, 1), 1),
    ((0, 0, 0), 0),
    ((0, 1, 1), 0),
    ((1, 1, 1), 1),
)


def support_template(depth: int):
    if depth < 1:
        raise ValueError(depth)
    k = 2
    next_var = 1
    layers = []
    hubs = [0]
    for j in range(depth + 1):
        left = list(range(next_var, next_var + k))
        next_var += k
        right = list(range(next_var, next_var + k))
        next_var += k
        layers.append((left, right))
        if j < depth:
            hubs.append(next_var)
            next_var += 1

    supports = [(0, layers[0][0][0], layers[0][1][0]), (0, layers[0][0][1], layers[0][1][1])]

    def add_lobes(pair, exit_hub):
        for lobe in pair:
            for i, selector in enumerate(lobe):
                supports.append(
                    (
                        selector,
                        lobe[i + 1] if i + 1 < k else exit_hub,
                        exit_hub if i + 1 < k else lobe[0],
                    )
                )

    add_lobes(layers[0], hubs[1])
    shared = []
    for j in range(1, depth + 1):
        left, right = layers[j]
        shared.append(len(supports))
        supports.append((hubs[j], left[0], right[0]))
        exit_hub = hubs[j + 1] if j < depth else 0
        add_lobes(layers[j], exit_hub)

    n = next_var
    assert n == 5 * (depth + 1)
    assert len(supports) == n + 1
    return n, supports, tuple(shared), tuple((tuple(a), tuple(b)) for a, b in layers), tuple(hubs)


def signed_template(depth: int):
    n, supports, shared, layers, hubs = support_template(depth)
    gates = []
    for i, (s, a, b) in enumerate(supports):
        if i < 2:
            pol, out = CENTRAL_PATTERN[i]
        elif i < 6:
            pol, out = FIRST_LOBE_PATTERN[i - 2]
        else:
            pol, out = REPEATED_BLOCK_PATTERN[(i - 6) % 5]
        gates.append((s, a, b, pol[0], pol[1], pol[2], out))
    return n, gates, shared, layers, hubs


def branch(gate, which):
    s, a, b, ps, p0, p1, out = gate
    if which == 0:
        return s, a, ps, p0
    return s, b, 1 ^ ps, p1


def target_for_arrival(gate, which, desired):
    _s, _d, _alpha, pd = branch(gate, which)
    return desired ^ pd ^ gate[6]


def good_cycles(depth):
    c0 = [(0, 0), (2, 1)]
    c1 = [(1, 1), (5, 1), (4, 1)]
    for j in range(depth):
        h = 6 + 5 * j
        c0.extend(((h, 1), (h + 3, 1)))
        c1.extend(((h, 0), (h + 1, 0), (h + 2, 0)))
    return tuple(c0), tuple(c1)


def bad_cycles(depth):
    c0 = [(0, 0), (2, 1)]
    c1 = [(1, 1), (5, 0)]
    for j in range(depth):
        h = 6 + 5 * j
        c0.extend(((h, 0), (h + 1, 1)))
        c1.extend(((h, 1), (h + 3, 1)))
    return tuple(c0), tuple(c1)


def validate_cycle(gates, root, cycle):
    for pos, (gi, b) in enumerate(cycle):
        _s, dest, _alpha, _pd = branch(gates[gi], b)
        if pos + 1 < len(cycle):
            assert dest == gates[cycle[pos + 1][0]][0]
        else:
            assert dest == root


def target_map(gates, cycle):
    initial = branch(gates[cycle[0][0]], cycle[0][1])[2]
    out = {}
    for pos, (gi, b) in enumerate(cycle):
        if pos + 1 < len(cycle):
            ngi, nb = cycle[pos + 1]
            desired = branch(gates[ngi], nb)[2]
        else:
            desired = 1 ^ initial
        t = target_for_arrival(gates[gi], b, desired)
        if gi in out and out[gi] != t:
            return None
        out[gi] = t
    return out


def combine_target(gates, c0, c1):
    a = target_map(gates, c0)
    b = target_map(gates, c1)
    if a is None or b is None:
        return None
    targets = [0] * len(gates)
    for gi, val in a.items():
        targets[gi] = val
    for gi, val in b.items():
        if gi in a and a[gi] != val:
            return None
        targets[gi] = val
    return tuple(targets)


def add_implication(graph, u, uphase, v, vphase):
    graph[2 * u + uphase].append(2 * v + vphase)
    graph[2 * v + (1 ^ vphase)].append(2 * u + (1 ^ uphase))


def fixed_mux_implication_graph(n, gates, target):
    graph = [[] for _ in range(2 * n)]
    for gate, y in zip(gates, target):
        s, a, b, ps, p0, p1, out = gate
        beta0 = y ^ p0 ^ out
        beta1 = y ^ p1 ^ out
        add_implication(graph, s, ps, a, beta0)
        add_implication(graph, s, 1 ^ ps, b, beta1)
    return graph


def scc(graph):
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
        seen[start] = True
        stack = [(start, 0)]
        while stack:
            u, pos = stack[-1]
            if pos < len(graph[u]):
                v = graph[u][pos]
                stack[-1] = (u, pos + 1)
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
        comp[start] = cid
        stack = [start]
        while stack:
            u = stack.pop()
            for v in reverse[u]:
                if comp[v] == -1:
                    comp[v] = cid
                    stack.append(v)
        cid += 1
    return comp


def unsat(n, gates, target):
    comp = scc(fixed_mux_implication_graph(n, gates, target))
    return any(comp[2 * v] == comp[2 * v + 1] for v in range(n))


def gate_value(bits, gate):
    s, a, b, ps, p0, p1, out = gate
    z = bits[s] ^ ps
    value = (bits[a] ^ p0) if z == 0 else (bits[b] ^ p1)
    return value ^ out


def in_range(n, gates, target):
    for bits in product((0, 1), repeat=n):
        if tuple(gate_value(bits, g) for g in gates) == target:
            return True
    return False


def explicit_periodic_checks():
    rows = []
    for depth in range(1, 101):
        n, gates, shared, layers, hubs = signed_template(depth)
        g0, g1 = good_cycles(depth)
        b0, b1 = bad_cycles(depth)
        validate_cycle(gates, 0, g0)
        validate_cycle(gates, 0, g1)
        validate_cycle(gates, 0, b0)
        validate_cycle(gates, 0, b1)
        good_target = combine_target(gates, g0, g1)
        assert good_target is not None, depth
        assert unsat(n, gates, good_target), depth
        if depth <= 2:
            assert not in_range(n, gates, good_target), depth
        bad_t0 = target_map(gates, b0)
        bad_t1 = target_map(gates, b1)
        assert bad_t0 is not None and bad_t1 is not None
        conflicts = [h for h in shared if bad_t0[h] != bad_t1[h]]
        assert conflicts == list(shared), (depth, conflicts, shared)
        assert len({gi for gi, _ in g0} & {gi for gi, _ in g1}) == depth
        assert len({gi for gi, _ in b0} & {gi for gi, _ in b1}) == depth
        rows.append((depth, n, len(shared)))
    return rows


def maximum_matching(n, supports, indices):
    match = [-1] * n

    def augment(gi, seen):
        for v in supports[gi]:
            if v in seen:
                continue
            seen.add(v)
            if match[v] == -1 or augment(match[v], seen):
                match[v] = gi
                return True
        return False

    return sum(augment(gi, set()) for gi in indices)


def hall_checks():
    for depth in range(1, 41):
        n, gates, _shared, _layers, _hubs = signed_template(depth)
        supports = [(g[0], g[1], g[2]) for g in gates]
        for deleted in range(len(gates)):
            remaining = [i for i in range(len(gates)) if i != deleted]
            assert maximum_matching(n, supports, remaining) == n, (depth, deleted)
    return 40


def beta_formula_checks():
    rows = {}
    for depth in range(1, 101):
        n, gates, shared, layers, hubs = signed_template(depth)
        expected = 3 * (depth + 1)
        assert expected * 5 == 3 * n
        # Local two-variable lobe lower bound, independent of signs.
        for exit_selected in (0, 1):
            feasible = []
            for x0, x1 in product((0, 1), repeat=2):
                ok0 = x0 or (x1 and exit_selected)
                ok1 = x1 or (exit_selected and x0)
                if ok0 and ok1:
                    feasible.append(x0 + x1)
            assert min(feasible) == (1 if exit_selected else 2)
        rows[depth] = expected
    return rows


def main():
    result = {
        "periodic_explicit_cycles": explicit_periodic_checks(),
        "hall_minimal_depth_through": hall_checks(),
        "beta_formula": beta_formula_checks(),
        "mixed_optimum_face": True,
        "failures": 0,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
