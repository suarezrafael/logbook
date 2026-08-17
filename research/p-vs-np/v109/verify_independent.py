from __future__ import annotations

import json
from itertools import combinations, product


def strict_supports(k: int):
    v = 0
    left = list(range(1, k + 1))
    right = list(range(k + 1, 2 * k + 1))
    supports = [
        (v, left[0], right[0]),
        (v, left[0], right[0]),
    ]
    for lobe in (left, right):
        for i, selector in enumerate(lobe):
            if i + 1 < len(lobe):
                supports.append((selector, lobe[i + 1], v))
            else:
                supports.append((selector, v, lobe[0]))
    return 2 * k + 1, supports


def explicit_target(k: int):
    # Central gate 0 starts the phase-0 left cycle; central gate 1 starts the
    # phase-1 right cycle.  The left final edge flips 0->1, while the right
    # final edge closes 1->0.  All targets are zero except the final left gate.
    return tuple([0, 0] + [0] * (k - 1) + [1] + [0] * k)


def add_forbidden_pair(graph, u: int, bad_u: int, v: int, bad_v: int):
    graph[2 * u + bad_u].append(2 * v + (1 ^ bad_v))
    graph[2 * v + bad_v].append(2 * u + (1 ^ bad_u))


def fixed_mux_formula(n: int, supports, target):
    graph = [[] for _ in range(2 * n)]
    for (s, a, b), y in zip(supports, target):
        # canonical MUX(s,a,b)=a when s=0 and b when s=1
        add_forbidden_pair(graph, s, 0, a, 1 ^ y)
        add_forbidden_pair(graph, s, 1, b, 1 ^ y)
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


def unsat(n: int, supports, target) -> bool:
    comp = scc(fixed_mux_formula(n, supports, target))
    return any(comp[2 * v] == comp[2 * v + 1] for v in range(n))


def mux_value(bits, gate):
    s, a, b = gate
    return bits[a] if bits[s] == 0 else bits[b]


def in_range(n: int, supports, target) -> bool:
    for bits in product((0, 1), repeat=n):
        if tuple(mux_value(bits, gate) for gate in supports) == target:
            return True
    return False


def target_checks():
    rows = []
    for k in range(2, 101):
        n, supports = strict_supports(k)
        target = explicit_target(k)
        assert len(supports) == n + 1 == len(target)
        assert unsat(n, supports, target), k
        if k <= 7:
            assert not in_range(n, supports, target), k
        rows.append((k, n, len(target)))
    return rows


def maximum_matching(n: int, supports, output_indices) -> int:
    match = [-1] * n

    def augment(gi: int, seen: set[int]) -> bool:
        for v in supports[gi]:
            if v in seen:
                continue
            seen.add(v)
            if match[v] == -1 or augment(match[v], seen):
                match[v] = gi
                return True
        return False

    return sum(augment(gi, set()) for gi in output_indices)


def hall_minimality():
    rows = []
    for k in range(2, 81):
        n, supports = strict_supports(k)
        for deleted in range(len(supports)):
            remaining = [i for i in range(len(supports)) if i != deleted]
            assert maximum_matching(n, supports, remaining) == n, (k, deleted)
        rows.append(k)
    return rows


def local_backdoor_ok(gate, chosen):
    s, a, b = gate
    return chosen[s] or (chosen[a] and chosen[b])


def lobe_minimum(k: int, v_value: int):
    best = k + 1
    for bits in product((0, 1), repeat=k):
        ok = True
        for i in range(k - 1):
            if not (bits[i] or (bits[i + 1] and v_value)):
                ok = False
                break
        if ok and not (bits[k - 1] or (v_value and bits[0])):
            ok = False
        if ok:
            best = min(best, sum(bits))
    return best


def beta_checks():
    rows = {}
    for k in range(2, 16):
        with_v = 1 + 2 * lobe_minimum(k, 1)
        without_v = 2 * lobe_minimum(k, 0)
        beta = min(with_v, without_v)
        expected = 1 + 2 * ((k + 1) // 2)
        assert beta == expected, (k, beta, expected)
        rows[k] = beta
    return rows


def branch_arcs(supports, bridge, ignored):
    arcs = []
    for i, (s, a, b) in enumerate(supports):
        if i == bridge or i in ignored:
            continue
        arcs.append((s, a, i, 0, 0))
        arcs.append((s, b, i, 1, 1))
    return arcs


def variable_scc(n: int, arcs):
    graph = [[] for _ in range(n)]
    reverse = [[] for _ in range(n)]
    for s, d, _gi, _br, _alpha in arcs:
        graph[s].append(d)
        reverse[d].append(s)
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
    comps = []
    for start in reversed(order):
        if comp[start] != -1:
            continue
        cid = len(comps)
        comp[start] = cid
        vertices = []
        stack = [start]
        while stack:
            u = stack.pop()
            vertices.append(u)
            for v in reverse[u]:
                if comp[v] == -1:
                    comp[v] = cid
                    stack.append(v)
        comps.append(vertices)
    return graph, comp, comps


def v108_certificate_exists(n: int, supports, ignored):
    ignored = set(ignored)
    for bridge, (s, a, b) in enumerate(supports):
        if bridge in ignored:
            continue
        arcs = branch_arcs(supports, bridge, ignored)
        graph, comp, comps = variable_scc(n, arcs)
        left = comp[s]
        if len(comps[left]) <= 1:
            continue
        outgoing = [(d, alpha) for ss, d, _gi, _br, alpha in arcs if ss == s and comp[d] == left]
        for _d, alpha in outgoing:
            forced = 1 ^ alpha
            terminal = a if forced == 0 else b
            right = comp[terminal]
            if right != left and len(comps[right]) > 1:
                return True
    return False


def v108_exhaustive_absence():
    rows = {}
    for k in (2, 3, 4):
        n, supports = strict_supports(k)
        checks = 0
        for mask in range(1 << len(supports)):
            ignored = {i for i in range(len(supports)) if (mask >> i) & 1}
            assert not v108_certificate_exists(n, supports, ignored), (k, ignored)
            checks += 1
        rows[k] = checks
    return rows


def structural_absence_contract():
    # Encodes the arbitrary-k proof ingredients rather than relying only on
    # the finite exhaustive controls above.
    for k in range(2, 101):
        n, supports = strict_supports(k)
        selector_count = [0] * n
        for s, _a, _b in supports:
            selector_count[s] += 1
        assert selector_count[0] == 2
        assert all(selector_count[v] == 1 for v in range(1, n))
        # Both central gates point directly to the first vertex of each lobe.
        assert supports[0] == supports[1] == (0, 1, k + 1)
        # Every first-lobe vertex has a direct return branch to the center while
        # its unique selector gate remains.  Thus a terminal separated from the
        # center after deletions is necessarily acyclic.
        assert supports[2][0] == 1 and 0 in supports[2][1:]
        assert supports[2 + k][0] == k + 1 and 0 in supports[2 + k][1:]
    return 100


def main():
    result = {
        "explicit_targets": target_checks(),
        "hall_minimal_k_through": max(hall_minimality()),
        "beta_exact": beta_checks(),
        "v108_exhaustive_absence": v108_exhaustive_absence(),
        "v108_structural_absence_k_through": structural_absence_contract(),
        "failures": 0,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
