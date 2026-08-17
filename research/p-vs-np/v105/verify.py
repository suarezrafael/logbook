from __future__ import annotations

import json
import math
import random
from itertools import combinations

from signed_majority_dumbbell import (
    Gate,
    SIGNED_MAJORITY_POLARITIES,
    avoid_by_odd_triangle_dumbbell,
    in_range,
    majority_polarity,
    mask_from_polarity,
    strict_family,
)


def switching_balanced(n: int, gates: list[Gate]) -> bool:
    values: dict[tuple[str, int], int] = {}
    incidence: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for ei, gate in enumerate(gates):
        p = majority_polarity(gate)
        assert p is not None
        for pos, v in enumerate(gate.support):
            incidence[v].append((ei, p[pos]))

    for start in range(n):
        vnode = ("v", start)
        if vnode in values:
            continue
        values[vnode] = 0
        stack = [vnode]
        while stack:
            kind, idx = stack.pop()
            if kind == "v":
                for ei, parity in incidence[idx]:
                    enode = ("e", ei)
                    wanted = values[(kind, idx)] ^ parity
                    if enode in values and values[enode] != wanted:
                        return False
                    if enode not in values:
                        values[enode] = wanted
                        stack.append(enode)
            else:
                gate = gates[idx]
                p = majority_polarity(gate)
                assert p is not None
                for pos, v in enumerate(gate.support):
                    vnode2 = ("v", v)
                    wanted = values[(kind, idx)] ^ p[pos]
                    if vnode2 in values and values[vnode2] != wanted:
                        return False
                    if vnode2 not in values:
                        values[vnode2] = wanted
                        stack.append(vnode2)
    return True


def min_incidence_degree(n: int, gates: list[Gate]) -> int:
    degree = [0] * n
    for gate in gates:
        for v in gate.support:
            degree[v] += 1
    return min(degree)


def support_connected(n: int, gates: list[Gate]) -> bool:
    adjacency = [set() for _ in range(n)]
    for gate in gates:
        a, b, c = gate.support
        for u, v in ((a, b), (a, c), (b, c)):
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
    return len(seen) == n


def exact_beta(n: int, gates: list[Gate]) -> int:
    supports = [set(g.support) for g in gates]
    for size in range(n + 1):
        for chosen in combinations(range(n), size):
            B = set(chosen)
            if all(len(B & support) >= 2 for support in supports):
                return size
    raise AssertionError("full input set is always a strong affine backdoor")


def no_proper_positive_surplus(n: int, gates: list[Gate]) -> bool:
    m = len(gates)
    for subset_mask in range(1, (1 << m) - 1):
        count = subset_mask.bit_count()
        used = set()
        for i, gate in enumerate(gates):
            if (subset_mask >> i) & 1:
                used.update(gate.support)
        if count > len(used):
            return False
    return True


def strict_checks() -> dict:
    brute = []
    for r in range(2, 10):
        n, gates = strict_family(r)
        assert len(gates) == n + 1
        assert support_connected(n, gates)
        assert min_incidence_degree(n, gates) >= 2
        assert not switching_balanced(n, gates)
        y, meta = avoid_by_odd_triangle_dumbbell(n, gates)
        assert meta["case"] == "odd_triangle_dumbbell"
        assert tuple(y) == tuple(1 if i % 2 == 0 else 0 for i in range(n + 1))
        assert not in_range(n, gates, y), (r, y, meta)
        brute.append(n)

    exact_beta_cases = {}
    for r in range(2, 7):
        n, gates = strict_family(r)
        beta = exact_beta(n, gates)
        assert beta == (2 * n) // 3
        exact_beta_cases[n] = beta

    surplus_cases = []
    for r in range(2, 6):
        n, gates = strict_family(r)
        assert no_proper_positive_surplus(n, gates)
        surplus_cases.append(n)

    return {
        "complete_range_n": brute,
        "exact_beta_small": exact_beta_cases,
        "no_proper_positive_surplus_n": surplus_cases,
        "switching_balanced": False,
    }


def randomized_polarity_checks() -> int:
    rng = random.Random(105105)
    cases = 0
    for r, trials in ((2, 240), (3, 180), (4, 80)):
        n, base = strict_family(r)
        for _ in range(trials):
            gates = []
            for gate in base:
                # Keep canonical-pair transport odd by setting p0=p1; mutate
                # the common pair switch and third-literal sign independently.
                q = rng.randrange(2)
                p2 = rng.randrange(2)
                gates.append(Gate(gate.support, mask_from_polarity((q, q, p2))))
            y, meta = avoid_by_odd_triangle_dumbbell(n, gates)
            assert not in_range(n, gates, y), (n, y, meta)
            cases += 1
    assert cases == 500
    return cases


def main() -> None:
    assert len(SIGNED_MAJORITY_POLARITIES) == 8
    result = {
        "signed_majority_masks": 8,
        "strict_family": strict_checks(),
        "random_polarity_complete_range_cases": randomized_polarity_checks(),
        "failures": 0,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
