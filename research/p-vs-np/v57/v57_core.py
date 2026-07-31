#!/usr/bin/env python3
"""Core routines for Laboratory V57.

V57 studies bijunctive (2-CNF) output fibers in the ternary NPN orbit 0x07.
It proves that full-context forcing always exists existentially for every proper
Boolean image, but that the direct affine-style block-redundancy analogue is
false, already at n=4,m=5 and asymptotically at stretch one.
"""
from __future__ import annotations

import itertools
from collections import defaultdict
from typing import Iterable, Sequence


def npn_transform(mask: int, perm: Sequence[int], negs: Sequence[int], outneg: int) -> int:
    transformed = 0
    for x in range(8):
        new_bits = [(x >> i) & 1 for i in range(3)]
        old_bits = [new_bits[perm[i]] ^ negs[i] for i in range(3)]
        old_index = old_bits[0] | (old_bits[1] << 1) | (old_bits[2] << 2)
        bit = ((mask >> old_index) & 1) ^ outneg
        transformed |= bit << x
    return transformed


def npn_orbit(mask: int) -> tuple[int, ...]:
    return tuple(sorted({
        npn_transform(mask, perm, negs, outneg)
        for perm in itertools.permutations(range(3))
        for negs in itertools.product((0, 1), repeat=3)
        for outneg in (0, 1)
    }))


ORBIT_07 = npn_orbit(0x07)


def fiber(mask: int, value: int) -> frozenset[int]:
    return frozenset(x for x in range(8) if ((mask >> x) & 1) == value)


def small_fiber_value(mask: int) -> int:
    weight = mask.bit_count()
    if weight == 3:
        return 1
    if weight == 5:
        return 0
    raise ValueError(f"mask 0x{mask:02x} is not in the 3/5 orbit")


def small_fiber(mask: int) -> frozenset[int]:
    return fiber(mask, small_fiber_value(mask))


def local_assignment(global_assignment: int, support: Sequence[int]) -> int:
    value = 0
    for i, variable in enumerate(support):
        value |= ((global_assignment >> variable) & 1) << i
    return value


def gate_active_set(n: int, mask: int, support: Sequence[int], active_value: int | None = None) -> frozenset[int]:
    if active_value is None:
        active_value = small_fiber_value(mask)
    return frozenset(
        x for x in range(1 << n)
        if ((mask >> local_assignment(x, support)) & 1) == active_value
    )


def intersection(sets: Sequence[Iterable[int]], universe: Iterable[int]) -> set[int]:
    result = set(universe)
    for item in sets:
        result.intersection_update(item)
    return result


def redundant_blocks(sets: Sequence[set[int] | frozenset[int]], universe: Iterable[int]) -> list[int]:
    result: list[int] = []
    universe_set = set(universe)
    for i, target in enumerate(sets):
        others = universe_set.copy()
        for j, item in enumerate(sets):
            if i != j:
                others.intersection_update(item)
        if others.issubset(target):
            result.append(i)
    return result


def irredundancy_witnesses(sets: Sequence[set[int] | frozenset[int]], universe: Iterable[int]) -> list[int] | None:
    witnesses: list[int] = []
    universe_set = set(universe)
    for i, target in enumerate(sets):
        others = universe_set.copy()
        for j, item in enumerate(sets):
            if i != j:
                others.intersection_update(item)
        candidates = sorted(others.difference(target))
        if not candidates:
            return None
        witnesses.append(candidates[0])
    return witnesses


def block_set_containing_zero(n: int, pinned: int, left: int, right: int, forbidden: int) -> frozenset[int]:
    """Small 0x07-orbit fiber: x_pinned=0 and (x_left,x_right)!=forbidden."""
    f_left = forbidden & 1
    f_right = (forbidden >> 1) & 1
    points = []
    for x in range(1 << n):
        if ((x >> pinned) & 1) != 0:
            continue
        if ((x >> left) & 1) == f_left and ((x >> right) & 1) == f_right:
            continue
        points.append(x)
    return frozenset(points)


def normalized_blocks_containing_zero(n: int) -> list[tuple[tuple[int, int, int, int], frozenset[int]]]:
    unique: dict[frozenset[int], tuple[int, int, int, int]] = {}
    for pinned in range(n):
        others = [v for v in range(n) if v != pinned]
        for left, right in itertools.combinations(others, 2):
            for forbidden in (1, 2, 3):
                block = block_set_containing_zero(n, pinned, left, right, forbidden)
                unique[block] = (pinned, left, right, forbidden)
    return [(description, block) for block, description in sorted(unique.items(), key=lambda item: item[1])]


def local_mask_for_forbidden(forbidden: int) -> int:
    f_left = forbidden & 1
    f_right = (forbidden >> 1) & 1
    mask = 0
    for local in range(8):
        pinned = local & 1
        left = (local >> 1) & 1
        right = (local >> 2) & 1
        active = pinned == 0 and not (left == f_left and right == f_right)
        if active:
            mask |= 1 << local
    return mask


G4_DESCRIPTIONS = (
    (0, 1, 2, 1),
    (0, 1, 2, 2),
    (0, 1, 3, 1),
    (0, 1, 3, 2),
    (0, 2, 3, 3),
)
G4_MASK_SUPPORT = tuple(
    (local_mask_for_forbidden(forbidden), (pinned, left, right))
    for pinned, left, right, forbidden in G4_DESCRIPTIONS
)
G4_WITNESSES = (10, 4, 6, 8, 14)

G3_MASK_SUPPORT = (
    (0x07, (0, 1, 2)),
    (0x0B, (0, 1, 2)),
    (0x0D, (0, 1, 2)),
)
G3_WITNESSES = (3, 2, 1)


def gadget_sets(n: int, mask_support: Sequence[tuple[int, Sequence[int]]]) -> list[frozenset[int]]:
    return [gate_active_set(n, mask, support) for mask, support in mask_support]


def stretch_one_family(k: int) -> tuple[int, list[tuple[int, tuple[int, int, int]]]]:
    if k < 0:
        raise ValueError("k must be nonnegative")
    gates: list[tuple[int, tuple[int, int, int]]] = list(G4_MASK_SUPPORT)
    offset = 4
    for _ in range(k):
        for mask, support in G3_MASK_SUPPORT:
            gates.append((mask, tuple(offset + v for v in support)))
        offset += 3
    return 4 + 3 * k, gates


def circuit_output(n: int, gates: Sequence[tuple[int, Sequence[int]]], assignment: int) -> tuple[int, ...]:
    output = []
    for mask, support in gates:
        local = local_assignment(assignment, support)
        output.append((mask >> local) & 1)
    return tuple(output)


def circuit_image(n: int, gates: Sequence[tuple[int, Sequence[int]]]) -> set[tuple[int, ...]]:
    return {circuit_output(n, gates, x) for x in range(1 << n)}


def boundary_edge(image: set[tuple[int, ...]]) -> tuple[tuple[int, ...], int] | None:
    if not image:
        return None
    m = len(next(iter(image)))
    full_size = 1 << m
    if len(image) == full_size:
        return None
    for point in sorted(image):
        for coordinate in range(m):
            neighbor = list(point)
            neighbor[coordinate] ^= 1
            if tuple(neighbor) not in image:
                return point, coordinate
    raise AssertionError("proper nonempty cube subset must have a boundary edge")


def full_context_forcing_patterns(image: set[tuple[int, ...]]) -> list[dict]:
    if not image:
        return []
    m = len(next(iter(image)))
    patterns = []
    for i in range(m):
        buckets: dict[tuple[int, ...], set[int]] = defaultdict(set)
        for point in image:
            key = point[:i] + point[i + 1:]
            buckets[key].add(point[i])
        for key, values in buckets.items():
            if len(values) == 1:
                patterns.append({"coordinate": i, "context": key, "forced_value": next(iter(values))})
    return patterns


def implication_graph_sccs(n: int, clauses: Sequence[Sequence[tuple[int, bool]]]) -> list[list[tuple[int, bool]]]:
    literals = [(v, sign) for v in range(n) for sign in (False, True)]
    graph: dict[tuple[int, bool], list[tuple[int, bool]]] = {literal: [] for literal in literals}

    def neg(literal: tuple[int, bool]) -> tuple[int, bool]:
        return literal[0], not literal[1]

    for clause in clauses:
        if len(clause) == 1:
            graph[neg(clause[0])].append(clause[0])
        elif len(clause) == 2:
            a, b = clause
            graph[neg(a)].append(b)
            graph[neg(b)].append(a)
        else:
            raise ValueError("only unit and binary clauses supported")

    index = 0
    stack: list[tuple[int, bool]] = []
    on_stack: set[tuple[int, bool]] = set()
    indices: dict[tuple[int, bool], int] = {}
    lowlink: dict[tuple[int, bool], int] = {}
    components: list[list[tuple[int, bool]]] = []

    def strongconnect(vertex: tuple[int, bool]) -> None:
        nonlocal index
        indices[vertex] = index
        lowlink[vertex] = index
        index += 1
        stack.append(vertex)
        on_stack.add(vertex)
        for target in graph[vertex]:
            if target not in indices:
                strongconnect(target)
                lowlink[vertex] = min(lowlink[vertex], lowlink[target])
            elif target in on_stack:
                lowlink[vertex] = min(lowlink[vertex], indices[target])
        if lowlink[vertex] == indices[vertex]:
            component = []
            while True:
                target = stack.pop()
                on_stack.remove(target)
                component.append(target)
                if target == vertex:
                    break
            components.append(component)

    for literal in literals:
        if literal not in indices:
            strongconnect(literal)
    return components


G4_CLAUSE_BLOCKS = (
    (((0, False),), ((1, False), (2, True))),
    (((0, False),), ((1, True), (2, False))),
    (((0, False),), ((1, False), (3, True))),
    (((0, False),), ((1, True), (3, False))),
    (((0, False),), ((2, False), (3, False))),
)
