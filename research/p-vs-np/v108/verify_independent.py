from __future__ import annotations

import json
from itertools import product


def strict_supports(k: int):
    left = list(range(k))
    right = list(range(k, 2 * k))
    supports = []
    for cycle in (left, right):
        for i, selector in enumerate(cycle):
            supports.append((selector, cycle[(i + 1) % k], cycle[(i + 2) % k]))
    supports.append((left[0], left[2], right[0]))
    return 2 * k, supports


def strict_target(k: int):
    # For each canonical branch-0 cycle, target 0 transports source phase 0
    # to the next source phase 0; the last target 1 closes 0 -> 1 and hence
    # forces the first selector to 1.  The bridge is then branch-1 active and
    # target 0 forces right[0]=0, contradicting the right cycle's right[0]=1.
    return tuple([0] * (k - 1) + [1] + [0] * (k - 1) + [1] + [0])


def add_forbidden_pair(graph, u: int, bad_u: int, v: int, bad_v: int):
    graph[2 * u + bad_u].append(2 * v + (1 ^ bad_v))
    graph[2 * v + bad_v].append(2 * u + (1 ^ bad_u))


def fixed_mux_formula(n: int, supports, target):
    graph = [[] for _ in range(2 * n)]
    for (s, a, b), y in zip(supports, target):
        # canonical MUX(s,a,b)=a for s=0 and b for s=1
        # y=target gives (s OR [a=y]) AND (!s OR [b=y]).
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


def independent_target_checks():
    rows = []
    for k in range(3, 101):
        n, supports = strict_supports(k)
        target = strict_target(k)
        assert len(supports) == n + 1
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

    size = 0
    for gi in output_indices:
        if augment(gi, set()):
            size += 1
    return size


def hall_minimality():
    rows = []
    for k in range(3, 81):
        n, supports = strict_supports(k)
        for deleted in range(len(supports)):
            remaining = [i for i in range(len(supports)) if i != deleted]
            assert maximum_matching(n, supports, remaining) == n, (k, deleted)
        rows.append(k)
    return rows


def valid_cycle_pattern(bits) -> bool:
    k = len(bits)
    return all(
        bits[i] or (bits[(i + 1) % k] and bits[(i + 2) % k])
        for i in range(k)
    )


def exact_beta_by_cycle_dp(k: int) -> int:
    # Enumerate each cycle independently, summarize only the bits touched by
    # the bridge, and combine.  This is independent of the V102 implementation.
    left_best = {}
    right_best = {}
    for bits in product((0, 1), repeat=k):
        if not valid_cycle_pattern(bits):
            continue
        weight = sum(bits)
        lk = (bits[0], bits[2])
        left_best[lk] = min(left_best.get(lk, k + 1), weight)
        rk = bits[0]
        right_best[rk] = min(right_best.get(rk, k + 1), weight)
    best = 2 * k + 1
    for (l0, l2), lw in left_best.items():
        for r0, rw in right_best.items():
            if l0 or (l2 and r0):
                best = min(best, lw + rw)
    return best


def beta_checks():
    rows = {}
    for k in (3, 6, 9, 12, 15):
        beta = exact_beta_by_cycle_dp(k)
        expected = 4 * k // 3
        assert beta == expected, (k, beta, expected)
        rows[k] = beta
    return rows


def main():
    result = {
        "explicit_targets": independent_target_checks(),
        "hall_minimal_k_through": max(hall_minimality()),
        "beta_exact": beta_checks(),
        "proof_identity": "beta=4k/3=2n/3 for k divisible by 3",
        "failures": 0,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
