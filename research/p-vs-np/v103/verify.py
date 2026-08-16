from __future__ import annotations

import json
import random
from itertools import combinations, permutations, product

from affine_hull_rank import (
    Gate, avoid_by_affine_hulls, canonical_hull_proper, canonical_target,
    essential, fiber, hull_rank_for_targets, in_range,
    local_affine_hull_equations, strict_family,
)


def affine_truth(mask: int, arity: int) -> bool:
    vals = [(mask >> i) & 1 for i in range(1 << arity)]
    constant = vals[0]
    coeff = [vals[1 << j] ^ constant for j in range(arity)]
    for idx in range(1 << arity):
        expected = constant
        for j in range(arity):
            expected ^= coeff[j] & ((idx >> j) & 1)
        if vals[idx] != expected:
            return False
    return True


def local_strong_affine(g: Gate, chosen: set[int]) -> bool:
    fixed = [j for j, v in enumerate(g.support) if v in chosen]
    free = [j for j in range(g.arity) if j not in fixed]
    for fixed_bits in product((0, 1), repeat=len(fixed)):
        values = []
        for free_bits in product((0, 1), repeat=len(free)):
            local = [0] * g.arity
            for j, b in zip(fixed, fixed_bits):
                local[j] = b
            for j, b in zip(free, free_bits):
                local[j] = b
            values.append(g.value_local(tuple(local)))
        mask = sum(v << i for i, v in enumerate(values))
        if not affine_truth(mask, len(free)):
            return False
    return True


def check_census() -> dict:
    essential_masks = [m for m in range(256) if essential(m)]
    proper = [m for m in essential_masks if canonical_hull_proper(m)]
    full = [m for m in essential_masks if not canonical_hull_proper(m)]
    assert len(essential_masks) == 218
    assert len(proper) == 162 and len(full) == 56
    for mask in full:
        g = Gate((0, 1, 2), mask)
        assert len(fiber(g, 0)) == 4 and len(fiber(g, 1)) == 4
        assert not affine_truth(mask, 3)
    g = Gate((0, 1, 2), 0x16)
    assert canonical_target(g) == 1
    eqs = local_affine_hull_equations(g, 1)
    assert eqs is not None and len(eqs) == 1
    coeff, rhs = eqs[0]
    assert coeff == 0b111 and rhs == 1
    return {"essential": 218, "proper_canonical_hull": 162, "full_canonical_hull": 56}


def check_random() -> int:
    rng = random.Random(103103)
    cases = 0
    for n in range(2, 8):
        for _ in range(180):
            gates = []
            for _i in range(n + 1):
                arity = min(3, n)
                support = tuple(rng.sample(range(n), arity))
                mask = rng.randrange(1 << (1 << arity))
                gates.append(Gate(support, mask))
            y, meta = avoid_by_affine_hulls(n, gates)
            assert len(y) == n + 1
            assert not in_range(n, gates, y), (n, gates, y, meta)
            cases += 1
    return cases


def check_strict_family() -> dict:
    for k in range(1, 5):
        n, gates = strict_family(k)
        y, meta = avoid_by_affine_hulls(n, gates)
        assert meta["case"] == "rank_enumeration"
        assert meta["rank"] == n - 1 and meta["nu"] == 1
        assert len(meta["selected"]) == n - 1
        assert len(meta["residual"]) == 2
        assert not in_range(n, gates, y)
    for k in range(1, 21):
        n, gates = strict_family(k)
        rank, consistent = hull_rank_for_targets(n, gates)
        assert consistent and rank == n - 1
        adjacency = [set() for _ in range(n)]
        degree = [0] * n
        for gate in gates:
            for v in gate.support:
                degree[v] += 1
            for u, v in combinations(gate.support, 2):
                adjacency[u].add(v)
                adjacency[v].add(u)
        seen = {0}
        stack = [0]
        while stack:
            u = stack.pop()
            for v in adjacency[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        assert len(seen) == n and min(degree) >= 2
    return {"bruteforce_k_through": 4, "symbolic_rank_k_through": 20}


def check_v101_mu_bound() -> dict:
    for order in permutations(range(4)):
        rank = {v: i for i, v in enumerate(order)}
        edges = [(0, 1, 2), (0, 1, 3), (0, 2, 3)]
        maxima = {max(edge, key=lambda v: rank[v]) for edge in edges}
        assert len(maxima) <= 2
    for k in range(1, 20):
        n = 4 * k
        arcs = []
        heads = set()

        def add_anchor(support, head):
            assert head not in heads
            heads.add(head)
            for v in support:
                if v != head:
                    arcs.append((v, head))

        add_anchor((0, 1, 2), 2)
        add_anchor((0, 1, 3), 3)
        for j in range(1, k):
            a, b, c, d = 4 * j, 4 * j + 1, 4 * j + 2, 4 * j + 3
            prev_d = 4 * (j - 1) + 3
            add_anchor((prev_d, b, c), c)
            add_anchor((a, b, c), a)
            add_anchor((a, b, d), d)
        assert len(heads) == 3 * k - 1
        indegree = [0] * n
        outgoing = [[] for _ in range(n)]
        for u, v in arcs:
            outgoing[u].append(v)
            indegree[v] += 1
        queue = [i for i, d in enumerate(indegree) if d == 0]
        count = 0
        while queue:
            u = queue.pop()
            count += 1
            for v in outgoing[u]:
                indegree[v] -= 1
                if indegree[v] == 0:
                    queue.append(v)
        assert count == n
        assert n - len(heads) == k + 1
        assert len(heads) == 2 * k + (k - 1)
    return {"mu_formula": "k+1", "checked_k_through": 19}


def check_v102_beta_bound() -> dict:
    for mask in (0x16, 0x17):
        gate = Gate((0, 1, 2), mask)
        good = []
        for r in range(4):
            for comb in combinations(range(3), r):
                if local_strong_affine(gate, set(comb)):
                    good.append(set(comb))
        assert all(len(s) >= 2 for s in good)
        assert all(local_strong_affine(gate, set(comb)) for comb in combinations(range(3), 2))
    edges = [{0, 1, 2}, {0, 1, 3}, {0, 2, 3}]
    feasible = []
    for r in range(5):
        for comb in combinations(range(4), r):
            selected = set(comb)
            if all(len(selected & edge) >= 2 for edge in edges):
                feasible.append(selected)
    assert min(map(len, feasible)) == 3
    for k in range(1, 20):
        _n, gates = strict_family(k)
        backdoor = {4 * j + t for j in range(k) for t in (1, 2, 3)}
        assert len(backdoor) == 3 * k
        assert all(local_strong_affine(g, backdoor) for g in gates)
    return {"beta_formula": "3k", "checked_k_through": 19}


def main() -> None:
    result = {
        "census": check_census(),
        "random_bruteforce_cases": check_random(),
        "strict_family": check_strict_family(),
        "v101_mu": check_v101_mu_bound(),
        "v102_beta": check_v102_beta_bound(),
        "failures": 0,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
