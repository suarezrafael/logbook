from __future__ import annotations

import json
import random
from itertools import combinations

from signed_bicyclic_barbell import (
    avoid_by_bicyclic_odd_barbell,
    find_bicyclic_odd_barbell,
)
from signed_majority_dumbbell import (
    Gate,
    SIGNED_MAJORITY_POLARITIES,
    avoid_by_odd_triangle_dumbbell,
    canonical_pair_edges,
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


def malformed_support_rejected() -> bool:
    mask = mask_from_polarity((0, 0, 0))
    for support in ((0, 1, 0), (0, 0, 1), (0, 1, 1)):
        try:
            canonical_pair_edges([Gate(support, mask)])
        except ValueError as exc:
            assert "three distinct variables" in str(exc)
        else:
            raise AssertionError(("repeated signed-majority support accepted", support))
    return True


def _gate_for_pair(n: int, u: int, v: int) -> Gate:
    third = next(w for w in range(n) if w not in (u, v))
    return Gate((u, v, third), mask_from_polarity((0, 0, 0)))


def long_barbell_family(left_len: int, right_len: int, internal: int):
    assert left_len >= 3 and right_len >= 3
    assert left_len % 2 == 1 and right_len % 2 == 1
    assert internal >= 0
    left = list(range(left_len))
    middle = list(range(left_len, left_len + internal))
    right = list(range(left_len + internal, left_len + internal + right_len))
    n = len(left) + len(middle) + len(right)
    pairs = []
    for cycle in (left, right):
        for i, u in enumerate(cycle):
            pairs.append((u, cycle[(i + 1) % len(cycle)]))
    path = [left[0]] + middle + [right[0]]
    for u, v in zip(path, path[1:]):
        pairs.append((u, v))
    assert len(pairs) == n + 1
    return n, [_gate_for_pair(n, u, v) for u, v in pairs]


def figure_eight_family(left_len: int, right_len: int):
    assert left_len >= 3 and right_len >= 3
    assert left_len % 2 == 1 and right_len % 2 == 1
    center = 0
    left = [center] + list(range(1, left_len))
    right = [center] + list(range(left_len, left_len + right_len - 1))
    n = left_len + right_len - 1
    pairs = []
    for cycle in (left, right):
        for i, u in enumerate(cycle):
            pairs.append((u, cycle[(i + 1) % len(cycle)]))
    assert len(pairs) == n + 1
    return n, [_gate_for_pair(n, u, v) for u, v in pairs]


def theta_family():
    n = 5
    pairs = [(0, 2), (2, 1), (0, 3), (3, 1), (0, 4), (4, 1)]
    assert len(pairs) == n + 1
    return n, [_gate_for_pair(n, u, v) for u, v in pairs]


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
        y2, meta2 = avoid_by_bicyclic_odd_barbell(n, gates)
        assert meta2["kind"] == "barbell"
        assert not in_range(n, gates, y2), (r, y2, meta2)
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


def general_bicyclic_checks() -> dict:
    tested = []
    for left, right, internal in ((5, 3, 0), (5, 3, 1), (5, 5, 1), (7, 3, 0)):
        n, gates = long_barbell_family(left, right, internal)
        y, meta = avoid_by_bicyclic_odd_barbell(n, gates)
        assert meta["kind"] == "barbell"
        assert meta["left_cycle_length"] in (left, right)
        assert meta["right_cycle_length"] in (left, right)
        assert not in_range(n, gates, y), (n, y, meta)
        tested.append((n, left, right, internal))

    figures = []
    for left, right in ((3, 3), (5, 3), (5, 5)):
        n, gates = figure_eight_family(left, right)
        y, meta = avoid_by_bicyclic_odd_barbell(n, gates)
        assert meta["kind"] == "figure_eight"
        assert not in_range(n, gates, y), (n, y, meta)
        figures.append((n, left, right))

    n, theta = theta_family()
    assert find_bicyclic_odd_barbell(n, theta) is None
    return {"barbells": tested, "figure_eights": figures, "theta_rejected": True}


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
            y2, meta2 = avoid_by_bicyclic_odd_barbell(n, gates)
            assert not in_range(n, gates, y2), (n, y2, meta2)
            cases += 1
    assert cases == 500
    return cases


def main() -> None:
    assert len(SIGNED_MAJORITY_POLARITIES) == 8
    result = {
        "signed_majority_masks": 8,
        "malformed_support_rejected": malformed_support_rejected(),
        "strict_family": strict_checks(),
        "general_bicyclic": general_bicyclic_checks(),
        "random_polarity_complete_range_cases": randomized_polarity_checks(),
        "failures": 0,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
