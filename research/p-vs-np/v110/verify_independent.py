from __future__ import annotations

import json
from itertools import product


def strict_supports(k: int):
    v = 0
    left = list(range(1, k + 1))
    right = list(range(k + 1, 2 * k + 1))
    w = 2 * k + 1
    post_left = list(range(2 * k + 2, 3 * k + 2))
    post_right = list(range(3 * k + 2, 4 * k + 2))
    supports = [(v, left[0], right[0]), (v, left[1], right[1])]
    for lobe in (left, right):
        for i, selector in enumerate(lobe):
            supports.append((selector, lobe[i + 1] if i + 1 < k else w, w if i + 1 < k else lobe[0]))
    shared = len(supports)
    supports.append((w, post_left[0], post_right[0]))
    for lobe in (post_left, post_right):
        for i, selector in enumerate(lobe):
            supports.append((selector, lobe[i + 1] if i + 1 < k else v, v if i + 1 < k else lobe[0]))
    return 4 * k + 2, supports, shared


def explicit_target(k: int):
    n, supports, shared = strict_supports(k)
    target = [0] * len(supports)
    target[2 * k + 1] = 1       # final pre-B gate arrives at shared branch-1 phase
    target[3 * k + 2] = 1       # final post-C gate flips phase 0 -> 1 at v
    assert target[shared] == 0   # both traversals require the same shared target
    return tuple(target)


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


def mux_value(bits, gate):
    s, a, b = gate
    return bits[a] if bits[s] == 0 else bits[b]


def in_range(n, supports, target):
    for bits in product((0, 1), repeat=n):
        if tuple(mux_value(bits, gate) for gate in supports) == target:
            return True
    return False


def target_checks():
    rows = []
    for k in range(2, 101):
        n, supports, shared = strict_supports(k)
        target = explicit_target(k)
        assert len(supports) == n + 1 == len(target)
        assert supports[0] != supports[1]
        assert target[shared] == 0
        assert unsat(n, supports, target), k
        if k <= 3:
            assert not in_range(n, supports, target), k
        rows.append((k, n, len(target), shared))
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
    rows = []
    for k in range(2, 61):
        n, supports, _shared = strict_supports(k)
        for deleted in range(len(supports)):
            remaining = [i for i in range(len(supports)) if i != deleted]
            assert maximum_matching(n, supports, remaining) == n, (k, deleted)
        rows.append(k)
    return rows


def lobe_summary(k, hub, prefix_len):
    best = {}
    for bits in product((0, 1), repeat=k):
        ok = True
        for i in range(k - 1):
            if not (bits[i] or (bits[i + 1] and hub)):
                ok = False
                break
        if ok and not (bits[k - 1] or (hub and bits[0])):
            ok = False
        if not ok:
            continue
        key = bits[:prefix_len]
        best[key] = min(best.get(key, k + 1), sum(bits))
    return best


def exact_beta_dp(k):
    best = 4 * k + 3
    for v in (0, 1):
        for w in (0, 1):
            pre = lobe_summary(k, w, 2)
            post = lobe_summary(k, v, 1)
            for akey, aw in pre.items():
                for bkey, bw in pre.items():
                    if not (v or (akey[0] and bkey[0])):
                        continue
                    if not (v or (akey[1] and bkey[1])):
                        continue
                    for ckey, cw in post.items():
                        for dkey, dw in post.items():
                            if not (w or (ckey[0] and dkey[0])):
                                continue
                            best = min(best, v + w + aw + bw + cw + dw)
    return best


def beta_checks():
    rows = {}
    for k in range(2, 16):
        beta = exact_beta_dp(k)
        expected = 2 + 4 * ((k + 1) // 2)
        assert beta == expected, (k, beta, expected)
        rows[k] = beta
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


def v108_absence():
    rows = {}
    for k in (2, 3):
        n, supports, _shared = strict_supports(k)
        checks = 0
        for mask in range(1 << len(supports)):
            ignored = {i for i in range(len(supports)) if (mask >> i) & 1}
            assert not v108_exists(n, supports, ignored), (k, ignored)
            checks += 1
        rows[k] = checks
    return rows


def structural_v109_bottleneck():
    for k in range(2, 101):
        n, supports, shared = strict_supports(k)
        w = 2 * k + 1
        selector_count = [0] * n
        for s, _a, _b in supports:
            selector_count[s] += 1
        assert selector_count[0] == 2
        assert selector_count[w] == 1
        assert all(selector_count[v] == 1 for v in range(1, n) if v != w)
        assert supports[shared][0] == w
        # Before the shared gate, every pre-lobe output stays within its lobe or w;
        # no pre output reaches v or the post region. Hence every central return
        # path to v must consume the shared output gate.
        post_start = 2 * k + 2
        for gi in range(2, shared):
            s, a, b = supports[gi]
            assert s < post_start and a < post_start and b < post_start
    return 100


def main():
    result = {
        "explicit_targets": target_checks(),
        "hall_minimal_k_through": max(hall_minimality()),
        "beta_exact": beta_checks(),
        "v108_exhaustive_absence": v108_absence(),
        "v109_forced_shared_gate_structure_k_through": structural_v109_bottleneck(),
        "shared_target": 0,
        "failures": 0,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
