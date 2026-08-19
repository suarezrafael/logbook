from __future__ import annotations

import json
import random
import sys
from collections import defaultdict
from itertools import combinations, product
from pathlib import Path

V109_DIR = Path(__file__).resolve().parents[1] / "v109"
sys.path.insert(0, str(V109_DIR))
from mux_gate_flow import MuxGate  # noqa: E402


K3_CENTRAL_PATTERN = (
    ((1, 1, 1), 0),
    ((0, 1, 1), 0),
)
K3_FIRST_PATTERN = (
    ((0, 1, 0), 0),
    ((1, 0, 1), 0),
    ((1, 0, 1), 0),
    ((1, 1, 0), 0),
    ((1, 0, 1), 1),
    ((1, 0, 0), 0),
)
K3_BLOCK_PATTERN = (
    ((0, 0, 1), 0),
    ((1, 1, 1), 1),
    ((1, 1, 1), 0),
    ((1, 0, 1), 0),
    ((1, 1, 1), 1),
    ((1, 1, 1), 1),
    ((1, 1, 0), 1),
)


def strict_family(depth: int):
    if depth < 1:
        raise ValueError(depth)
    k = 3
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
    base = [
        MuxGate(0, layers[0][0][0], layers[0][1][0]),
        MuxGate(0, layers[0][0][1], layers[0][1][1]),
    ]

    def add_lobes(pair, exit_hub):
        for lobe in pair:
            for i, selector in enumerate(lobe):
                base.append(MuxGate(
                    selector,
                    lobe[i + 1] if i + 1 < k else exit_hub,
                    exit_hub if i + 1 < k else lobe[0],
                ))

    add_lobes(layers[0], hubs[1])
    shared = []
    for j in range(1, depth + 1):
        left, right = layers[j]
        shared.append(len(base))
        base.append(MuxGate(hubs[j], left[0], right[0]))
        exit_hub = hubs[j + 1] if j < depth else 0
        add_lobes(layers[j], exit_hub)

    gates = []
    for i, gate in enumerate(base):
        if i < 2:
            polarity, out_flip = K3_CENTRAL_PATTERN[i]
        elif i < 8:
            polarity, out_flip = K3_FIRST_PATTERN[i - 2]
        else:
            polarity, out_flip = K3_BLOCK_PATTERN[(i - 8) % 7]
        gates.append(MuxGate(
            gate.selector,
            gate.data0,
            gate.data1,
            polarity,
            out_flip,
        ))
    n = next_var
    assert n == 7 * (depth + 1)
    assert len(gates) == n + 1
    return n, gates, tuple(shared)


def target_word(gates, cycle0, cycle1):
    targets = [0] * len(gates)
    assigned = {}
    for cycle in (cycle0, cycle1):
        initial = gates[cycle[0][0]].branch(cycle[0][1])[2]
        for pos, (gi, branch) in enumerate(cycle):
            if pos + 1 < len(cycle):
                ngi, nb = cycle[pos + 1]
                desired = gates[ngi].branch(nb)[2]
            else:
                desired = 1 ^ initial
            target = gates[gi].target_for_arrival(branch, desired)
            if gi in assigned and assigned[gi] != target:
                return None
            assigned[gi] = target
            targets[gi] = target
    return tuple(targets)


def explicit_good_cycles(depth):
    c0 = [(0, 0), (2, 1)]
    c1 = [(1, 0), (3, 0), (4, 0)]
    for j in range(depth):
        h = 8 + 7 * j
        c0.extend(((h, 0), (h + 1, 0), (h + 2, 0), (h + 3, 0)))
        c1.extend(((h, 1), (h + 4, 1)))
    return tuple(c0), tuple(c1)


def explicit_bad_cycles(depth):
    c0 = [(0, 0), (2, 1)]
    c1 = [(1, 0), (3, 0), (4, 0)]
    for j in range(depth):
        h = 8 + 7 * j
        c0.extend(((h, 0), (h + 1, 0), (h + 2, 0), (h + 3, 0)))
        c1.extend(((h, 1), (h + 4, 0), (h + 5, 0), (h + 6, 0)))
    return tuple(c0), tuple(c1)


def validate_cycle(gates, root, cycle):
    assert cycle
    for pos, (gi, branch) in enumerate(cycle):
        dest = gates[gi].branch(branch)[1]
        if pos + 1 < len(cycle):
            assert dest == gates[cycle[pos + 1][0]].selector
        else:
            assert dest == root


def literal_id(var, value):
    return 2 * var + value


def fixed_target_unsat_2sat(n, gates, target):
    graph = [[] for _ in range(2 * n)]
    reverse = [[] for _ in range(2 * n)]

    def add_implication(a_var, a_val, b_var, b_val):
        a = literal_id(a_var, a_val)
        b = literal_id(b_var, b_val)
        na = literal_id(a_var, 1 ^ a_val)
        nb = literal_id(b_var, 1 ^ b_val)
        graph[a].append(b)
        reverse[b].append(a)
        graph[nb].append(na)
        reverse[na].append(nb)

    for gate, y in zip(gates, target):
        for branch in (0, 1):
            s, d, alpha, data_p = gate.branch(branch)
            desired = y ^ data_p ^ gate.out_flip
            add_implication(s, alpha, d, desired)

    seen = [False] * (2 * n)
    order = []
    for start in range(2 * n):
        if seen[start]:
            continue
        stack = [(start, 0)]
        seen[start] = True
        while stack:
            u, i = stack[-1]
            if i < len(graph[u]):
                v = graph[u][i]
                stack[-1] = (u, i + 1)
                if not seen[v]:
                    seen[v] = True
                    stack.append((v, 0))
            else:
                order.append(u)
                stack.pop()

    comp = [-1] * (2 * n)
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
    return any(comp[2 * v] == comp[2 * v + 1] for v in range(n))


def enumerate_paths(n, gates, root, start, cap=2500):
    by_selector = defaultdict(list)
    for gi, gate in enumerate(gates):
        if gate.selector != root:
            by_selector[gate.selector].append(gi)
    out = []

    def dfs(var, path, used):
        if len(out) >= cap:
            return
        if var == root:
            out.append(tuple(path))
            return
        for gi in by_selector[var]:
            if gi in used:
                continue
            for branch in (0, 1):
                dest = gates[gi].branch(branch)[1]
                dfs(dest, path + [(gi, branch)], used | {gi})

    dfs(start, [], set())
    return list(dict.fromkeys(out)), len(out) >= cap


def reachable_without_gate(n, gates, root, start, banned):
    if start == root:
        return True
    by_selector = defaultdict(list)
    for gi, gate in enumerate(gates):
        if gate.selector != root and gi != banned:
            by_selector[gate.selector].append(gate)
    seen = {start}
    stack = [start]
    while stack:
        u = stack.pop()
        for gate in by_selector[u]:
            for v in (gate.data0, gate.data1):
                if v == root:
                    return True
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
    return False


def common_dominators(n, gates, root, d0, d1):
    return {
        gi for gi, gate in enumerate(gates)
        if gate.selector != root
        and not reachable_without_gate(n, gates, root, d0, gi)
        and not reachable_without_gate(n, gates, root, d1, gi)
    }


def brute_pair(n, gates, root, g0, b0, g1, b1):
    d0 = gates[g0].branch(b0)[1]
    d1 = gates[g1].branch(b1)[1]
    p0, cap0 = enumerate_paths(n, gates, root, d0)
    p1, cap1 = enumerate_paths(n, gates, root, d1)
    if cap0 or cap1 or not p0 or not p1:
        return None
    best = len(gates) + 1
    compatible = False
    for a in p0:
        sa = {gi for gi, _ in a}
        for b in p1:
            overlap = len(sa & {gi for gi, _ in b})
            if overlap < best:
                best = overlap
                compatible = False
            if overlap == best and target_word(
                gates,
                ((g0, b0),) + a,
                ((g1, b1),) + b,
            ) is not None:
                compatible = True
    return best, compatible, len(common_dominators(n, gates, root, d0, d1))


def random_graph_lemma_audit():
    rng = random.Random(9113)
    checked = 0
    compatible = 0
    for n in range(3, 7):
        for _ in range(90):
            gates = []
            for _j in range(n + 1):
                s, a, b = rng.sample(range(n), 3)
                gates.append(MuxGate(
                    s, a, b,
                    tuple(rng.randrange(2) for _k in range(3)),
                    rng.randrange(2),
                ))
            by_selector = defaultdict(list)
            for gi, gate in enumerate(gates):
                by_selector[gate.selector].append(gi)
            candidates = []
            for root, ids in by_selector.items():
                for g0, g1 in combinations(ids, 2):
                    for b0, b1 in product((0, 1), repeat=2):
                        if gates[g0].branch(b0)[2] != gates[g1].branch(b1)[2]:
                            candidates.append((root, g0, b0, g1, b1))
            rng.shuffle(candidates)
            for root, g0, b0, g1, b1 in candidates[:3]:
                brute = brute_pair(n, gates, root, g0, b0, g1, b1)
                if brute is None:
                    continue
                best, has_compatible, common = brute
                assert best == common, (n, best, common)
                compatible += int(has_compatible)
                checked += 1
    assert checked >= 300
    return {"fixed_pairs": checked, "compatible_optima": compatible}


def maximum_support_matching(n, gates, indices):
    match = [-1] * n

    def augment(gi, seen):
        gate = gates[gi]
        for v in (gate.selector, gate.data0, gate.data1):
            if v in seen:
                continue
            seen.add(v)
            if match[v] == -1 or augment(match[v], seen):
                match[v] = gi
                return True
        return False

    return sum(augment(gi, set()) for gi in indices)


def strict_family_audit():
    rows = []
    for depth in range(1, 101):
        n, gates, shared = strict_family(depth)
        good0, good1 = explicit_good_cycles(depth)
        bad0, bad1 = explicit_bad_cycles(depth)
        validate_cycle(gates, 0, good0)
        validate_cycle(gates, 0, good1)
        validate_cycle(gates, 0, bad0)
        validate_cycle(gates, 0, bad1)
        good = target_word(gates, good0, good1)
        bad = target_word(gates, bad0, bad1)
        assert good is not None
        assert bad is None
        assert fixed_target_unsat_2sat(n, gates, good), depth
        assert len({gi for gi, _ in good0} & {gi for gi, _ in good1}) == depth
        assert len({gi for gi, _ in bad0} & {gi for gi, _ in bad1}) == depth
        assert len(shared) == depth
        rows.append((depth, n, len(gates)))
    return rows


def hall_audit():
    for depth in range(1, 31):
        n, gates, _shared = strict_family(depth)
        for deleted in range(len(gates)):
            remaining = [gi for gi in range(len(gates)) if gi != deleted]
            assert maximum_support_matching(n, gates, remaining) == n
    return 30


def beta_depth_one_exact():
    n, gates, _ = strict_family(1)
    expected = 10
    for size in range(expected):
        for subset in combinations(range(n), size):
            chosen = set(subset)
            ok = all(
                g.selector in chosen or (g.data0 in chosen and g.data1 in chosen)
                for g in gates
            )
            assert not ok
    assert any(
        all(
            g.selector in set(subset) or (g.data0 in set(subset) and g.data1 in set(subset))
            for g in gates
        )
        for subset in combinations(range(n), expected)
    )
    assert expected * 7 == 5 * n
    return {"n": n, "beta": expected}


def main():
    result = {
        "random_graph_lemma_audit": random_graph_lemma_audit(),
        "strict_family_depth_through": strict_family_audit()[-1][0],
        "hall_depth_through": hall_audit(),
        "beta_depth_one_exact": beta_depth_one_exact(),
        "independent_2sat": True,
        "imports_v113": False,
        "failures": 0,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
