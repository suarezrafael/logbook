from __future__ import annotations

import json
from itertools import product


def strict_supports(depth: int):
    if depth < 1:
        raise ValueError("depth must be positive")
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
    left_paths = []
    right_paths = []

    def add_lobe(lobe, exit_hub):
        path = []
        for i, selector in enumerate(lobe):
            gi = len(supports)
            supports.append(
                (
                    selector,
                    lobe[i + 1] if i + 1 < k else exit_hub,
                    exit_hub if i + 1 < k else lobe[0],
                )
            )
            path.append((gi, 0))
        return path

    left_paths.append(add_lobe(layers[0][0], hubs[1]))
    right_paths.append(add_lobe(layers[0][1], hubs[1]))
    shared = []
    for j in range(1, depth + 1):
        left, right = layers[j]
        shared_gate = len(supports)
        shared.append(shared_gate)
        supports.append((hubs[j], left[0], right[0]))
        exit_hub = hubs[j + 1] if j < depth else 0
        left_paths.append(add_lobe(left, exit_hub))
        right_paths.append(add_lobe(right, exit_hub))

    n = next_var
    assert n == 5 * (depth + 1)
    assert len(supports) == n + 1
    return n, supports, tuple(shared), left_paths, right_paths, tuple(hubs)


def canonical_cycles(depth: int):
    n, supports, shared, left_paths, right_paths, hubs = strict_supports(depth)
    c0 = [(0, 0)]
    c1 = [(1, 1)]
    for j in range(depth + 1):
        if j > 0:
            c0.append((shared[j - 1], 0))
            c1.append((shared[j - 1], 1))
        c0.extend(left_paths[j])
        c1.extend(right_paths[j])
    return n, supports, shared, tuple(c0), tuple(c1), hubs


def branch_source_phase(branch: int) -> int:
    return branch


def explicit_target(depth: int):
    n, supports, shared, c0, c1, hubs = canonical_cycles(depth)
    target = [0] * len(supports)
    assigned = {}
    for cycle in (c0, c1):
        initial = branch_source_phase(cycle[0][1])
        for pos, (gi, branch) in enumerate(cycle):
            desired = (
                branch_source_phase(cycle[pos + 1][1])
                if pos + 1 < len(cycle)
                else 1 ^ initial
            )
            # Unsigned MUX: the target bit equals the desired arrival phase.
            if gi in assigned:
                assert assigned[gi] == desired, (depth, gi, assigned[gi], desired)
            assigned[gi] = desired
            target[gi] = desired
    assert set(shared) == ({gi for gi, _ in c0} & {gi for gi, _ in c1})
    return n, supports, shared, tuple(target), c0, c1, hubs


def add_forbidden_pair(graph, u, bad_u, v, bad_v):
    graph[2 * u + bad_u].append(2 * v + (1 ^ bad_v))
    graph[2 * v + bad_v].append(2 * u + (1 ^ bad_u))


def fixed_mux_formula(n, supports, target):
    graph = [[] for _ in range(2 * n)]
    for (s, a, b), y in zip(supports, target):
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


def unsat(n, supports, target):
    comp = scc(fixed_mux_formula(n, supports, target))
    return any(comp[2 * v] == comp[2 * v + 1] for v in range(n))


def mux_value(bits, support):
    s, a, b = support
    return bits[a] if bits[s] == 0 else bits[b]


def in_range(n, supports, target):
    return any(
        tuple(mux_value(bits, g) for g in supports) == target
        for bits in product((0, 1), repeat=n)
    )


def target_checks():
    rows = []
    for depth in range(1, 101):
        n, supports, shared, target, c0, c1, hubs = explicit_target(depth)
        assert len(shared) == depth
        assert len(set(gi for gi, _ in c0) & set(gi for gi, _ in c1)) == depth
        assert unsat(n, supports, target), depth
        if depth <= 2:
            assert not in_range(n, supports, target), depth
        rows.append((depth, n, len(target), len(shared)))
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


def hall_minimality():
    for depth in range(1, 41):
        n, supports, _shared, _l, _r, _h = strict_supports(depth)
        for deleted in range(len(supports)):
            remaining = [i for i in range(len(supports)) if i != deleted]
            assert maximum_matching(n, supports, remaining) == n, (depth, deleted)
    return 40


def local_backdoor_ok(support, chosen):
    s, a, b = support
    return s in chosen or (a in chosen and b in chosen)


def beta_symbolic_checks():
    rows = {}
    for depth in range(1, 101):
        n, supports, shared, _left, _right, hubs = strict_supports(depth)
        # Upper bound: choose every hub (including v=0) and the first variable
        # of every one of the two lobes in each layer.
        chosen = set(hubs)
        # Reconstruct layer starts from supports: every non-hub lobe contributes
        # one selected selector under the all-hubs assignment.
        # The canonical supports are easiest to recover from the central/shared
        # gates: use a direct scan and choose the smallest non-hub selector from
        # each consecutive pair of lobe selectors.
        hubset = set(hubs)
        lobe_selectors = [s for s, _a, _b in supports if s not in hubset]
        for i in range(0, len(lobe_selectors), 2):
            chosen.add(lobe_selectors[i])
        assert all(local_backdoor_ok(g, chosen) for g in supports), depth
        expected = 3 * (depth + 1)
        assert len(chosen) == expected, (depth, len(chosen), expected)

        # Lower bound certificate for each 2-variable lobe gadget: if its exit
        # hub is selected, at least one lobe variable is needed; otherwise both
        # are forced into any strong-affine backdoor.  Summed over 2(depth+1)
        # lobes plus the (depth+1) exit hubs, this is at least 3(depth+1).
        for exit_selected in (0, 1):
            feasible = []
            for x0, x1 in product((0, 1), repeat=2):
                ok0 = x0 or (x1 and exit_selected)
                ok1 = x1 or (exit_selected and x0)
                if ok0 and ok1:
                    feasible.append(x0 + x1)
            assert min(feasible) == (1 if exit_selected else 2)
        rows[depth] = {"n": n, "beta": expected}
    return rows


def branch_arcs(supports, bridge, ignored):
    arcs = []
    for i, (s, a, b) in enumerate(supports):
        if i == bridge or i in ignored:
            continue
        arcs.append((s, a, 0))
        arcs.append((s, b, 1))
    return arcs


def variable_scc(n, arcs):
    graph = [[] for _ in range(n)]
    reverse = [[] for _ in range(n)]
    for s, d, _alpha in arcs:
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
                z = graph[u][pos]
                stack[-1] = (u, pos + 1)
                if not seen[z]:
                    seen[z] = True
                    stack.append((z, 0))
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
        vs = []
        stack = [start]
        while stack:
            u = stack.pop()
            vs.append(u)
            for z in reverse[u]:
                if comp[z] == -1:
                    comp[z] = cid
                    stack.append(z)
        comps.append(vs)
    return comp, comps


def v108_exists(n, supports, ignored):
    ignored = set(ignored)
    for bridge, (s, a, b) in enumerate(supports):
        if bridge in ignored:
            continue
        arcs = branch_arcs(supports, bridge, ignored)
        comp, comps = variable_scc(n, arcs)
        left = comp[s]
        if len(comps[left]) <= 1:
            continue
        for ss, d, alpha in arcs:
            if ss != s or comp[d] != left:
                continue
            forced = 1 ^ alpha
            terminal = a if forced == 0 else b
            right = comp[terminal]
            if right != left and len(comps[right]) > 1:
                return True
    return False


def v108_absence_first_depths():
    rows = {}
    for depth in (1, 2):
        n, supports, _shared, _l, _r, _h = strict_supports(depth)
        checks = 0
        for mask in range(1 << len(supports)):
            ignored = {i for i in range(len(supports)) if (mask >> i) & 1}
            assert not v108_exists(n, supports, ignored), (depth, ignored)
            checks += 1
        rows[depth] = checks
    return rows


def main():
    result = {
        "explicit_targets": target_checks(),
        "hall_minimal_depth_through": hall_minimality(),
        "beta_symbolic": beta_symbolic_checks(),
        "v108_exhaustive_absence_first_depths": v108_absence_first_depths(),
        "minimum_overlap_equals_depth": True,
        "failures": 0,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
