#!/usr/bin/env python3
"""Core routines for Laboratory V58.

V58 studies adaptive reorientation for the bijunctive ternary NPN orbit 0x07.
It formalizes orientation depth as distance to the vertex boundary of the circuit
image, implements polynomial 2-CNF entailment, and audits the one-flip
conjecture around the canonical small-fiber orientation.
"""
from __future__ import annotations

import itertools
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable, Sequence

Literal = tuple[int, bool]  # (variable, positive); False means negated literal.
Clause = tuple[Literal, ...]
Gate = tuple[int, tuple[int, int, int]]
Descriptor = tuple[int, int, int, int]  # pinned,left,right,forbidden pair in {1,2,3}


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


def eval_literal(literal: Literal, assignment: int) -> bool:
    variable, positive = literal
    bit = (assignment >> variable) & 1
    return bool(bit) if positive else not bool(bit)


def eval_clause(clause: Clause, assignment: int) -> bool:
    return any(eval_literal(literal, assignment) for literal in clause)


def local_2cnf_for_fiber(mask: int, value: int) -> tuple[Clause, ...]:
    """Return a canonical complete unit/binary CNF description of a local fiber.

    For a bijunctive relation, the conjunction of all unit and binary clauses
    valid on the relation is exactly the relation. The 0x07 orbit has this
    property for both output fibers.
    """
    points = fiber(mask, value)
    if not points:
        return ((),)  # explicit contradiction sentinel
    candidates: list[Clause] = []
    for v in range(3):
        for sign in (False, True):
            candidates.append(((v, sign),))
    for a, b in itertools.combinations(range(3), 2):
        for sa in (False, True):
            for sb in (False, True):
                candidates.append(((a, sa), (b, sb)))
    valid = [c for c in candidates if all(eval_clause(c, x) for x in points)]
    described = {
        x for x in range(8)
        if all(eval_clause(c, x) for c in valid)
    }
    if described != set(points):
        raise ValueError(f"fiber of 0x{mask:02x} value {value} is not bijunctive")
    # Remove clauses entailed by the remaining local clauses; constant size.
    reduced = list(valid)
    changed = True
    while changed:
        changed = False
        for i, clause in enumerate(tuple(reduced)):
            others = reduced[:i] + reduced[i + 1:]
            models = {x for x in range(8) if all(eval_clause(c, x) for c in others)}
            if all(eval_clause(clause, x) for x in models):
                reduced.pop(i)
                changed = True
                break
    return tuple(reduced)


def globalize_clauses(local_clauses: Sequence[Clause], support: Sequence[int]) -> tuple[Clause, ...]:
    return tuple(
        tuple((support[v], sign) for v, sign in clause)
        for clause in local_clauses
    )


def gate_clauses(gate: Gate, output_value: int) -> tuple[Clause, ...]:
    mask, support = gate
    return globalize_clauses(local_2cnf_for_fiber(mask, output_value), support)


def negate_literal(literal: Literal) -> Literal:
    return literal[0], not literal[1]


def two_sat_satisfiable(n: int, clauses: Sequence[Clause]) -> bool:
    """Linear-time SCC test for unit/binary CNF satisfiability."""
    nodes = 2 * n
    graph = [[] for _ in range(nodes)]
    reverse = [[] for _ in range(nodes)]

    def node(lit: Literal) -> int:
        v, positive = lit
        return 2 * v + int(positive)

    def add_edge(a: int, b: int) -> None:
        graph[a].append(b)
        reverse[b].append(a)

    for clause in clauses:
        if len(clause) == 0:
            return False
        if len(clause) == 1:
            a = clause[0]
            add_edge(node(negate_literal(a)), node(a))
        elif len(clause) == 2:
            a, b = clause
            add_edge(node(negate_literal(a)), node(b))
            add_edge(node(negate_literal(b)), node(a))
        else:
            raise ValueError("only unit and binary clauses are supported")

    seen = [False] * nodes
    order: list[int] = []

    def dfs(v: int) -> None:
        seen[v] = True
        for w in graph[v]:
            if not seen[w]:
                dfs(w)
        order.append(v)

    for v in range(nodes):
        if not seen[v]:
            dfs(v)

    comp = [-1] * nodes

    def rdfs(v: int, cid: int) -> None:
        comp[v] = cid
        for w in reverse[v]:
            if comp[w] < 0:
                rdfs(w, cid)

    cid = 0
    for v in reversed(order):
        if comp[v] < 0:
            rdfs(v, cid)
            cid += 1
    return all(comp[2 * v] != comp[2 * v + 1] for v in range(n))


def formula_satisfiable(n: int, blocks: Sequence[Sequence[Clause]]) -> bool:
    return two_sat_satisfiable(n, [c for block in blocks for c in block])


def entails_clause(n: int, clauses: Sequence[Clause], target: Clause) -> bool:
    assumptions = [((v, not sign),) for v, sign in target]
    return not two_sat_satisfiable(n, list(clauses) + assumptions)


def redundant_blocks_2cnf(n: int, blocks: Sequence[Sequence[Clause]]) -> list[int]:
    result = []
    for i, target_block in enumerate(blocks):
        others = [c for j, block in enumerate(blocks) if j != i for c in block]
        if all(entails_clause(n, others, clause) for clause in target_block):
            result.append(i)
    return result


def orientation_blocks(gates: Sequence[Gate], orientation: Sequence[int]) -> list[tuple[Clause, ...]]:
    return [gate_clauses(gate, value) for gate, value in zip(gates, orientation)]


def baseline_small_orientation(gates: Sequence[Gate]) -> tuple[int, ...]:
    return tuple(small_fiber_value(mask) for mask, _ in gates)


def find_boundary_within_radius(
    n: int,
    gates: Sequence[Gate],
    baseline: Sequence[int] | None = None,
    max_radius: int = 1,
) -> dict | None:
    """Search orientations in a Hamming ball using only polynomial 2-CNF tests."""
    m = len(gates)
    if baseline is None:
        baseline = baseline_small_orientation(gates)
    baseline = tuple(baseline)
    for radius in range(max_radius + 1):
        for flipped in itertools.combinations(range(m), radius):
            orientation = list(baseline)
            for i in flipped:
                orientation[i] ^= 1
            blocks = orientation_blocks(gates, orientation)
            if not formula_satisfiable(n, blocks):
                return {
                    "kind": "inconsistent_orientation",
                    "orientation": tuple(orientation),
                    "target": tuple(orientation),
                    "search_radius": radius,
                    "flipped": flipped,
                }
            redundant = redundant_blocks_2cnf(n, blocks)
            if redundant:
                coordinate = redundant[0]
                target = list(orientation)
                target[coordinate] ^= 1
                return {
                    "kind": "boundary_redundancy",
                    "orientation": tuple(orientation),
                    "target": tuple(target),
                    "search_radius": radius,
                    "flipped": flipped,
                    "redundant_coordinate": coordinate,
                    "all_redundant_coordinates": tuple(redundant),
                }
    return None


def local_assignment(global_assignment: int, support: Sequence[int]) -> int:
    value = 0
    for i, variable in enumerate(support):
        value |= ((global_assignment >> variable) & 1) << i
    return value


def circuit_output(n: int, gates: Sequence[Gate], assignment: int) -> tuple[int, ...]:
    return tuple((mask >> local_assignment(assignment, support)) & 1 for mask, support in gates)


def circuit_image(n: int, gates: Sequence[Gate]) -> set[tuple[int, ...]]:
    return {circuit_output(n, gates, x) for x in range(1 << n)}


def boundary_distance(image: set[tuple[int, ...]], baseline: Sequence[int]) -> int | None:
    if not image:
        return None
    baseline = tuple(baseline)
    if baseline not in image:
        return 0
    m = len(baseline)
    best = None
    for y in image:
        if any(y[:i] + (1 - y[i],) + y[i + 1:] not in image for i in range(m)):
            distance = sum(a != b for a, b in zip(y, baseline))
            best = distance if best is None else min(best, distance)
    return best


def hamming_ball(center: Sequence[int], radius: int) -> set[tuple[int, ...]]:
    center = tuple(center)
    m = len(center)
    result = set()
    for size in range(radius + 1):
        for flipped in itertools.combinations(range(m), size):
            y = list(center)
            for i in flipped:
                y[i] ^= 1
            result.add(tuple(y))
    return result


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


def descriptor_to_gate(desc: Descriptor) -> Gate:
    pinned, left, right, forbidden = desc
    return local_mask_for_forbidden(forbidden), (pinned, left, right)


def normalized_descriptors(n: int) -> list[Descriptor]:
    result = []
    for pinned in range(n):
        others = [v for v in range(n) if v != pinned]
        for left, right in itertools.combinations(others, 2):
            for forbidden in (1, 2, 3):
                result.append((pinned, left, right, forbidden))
    return result


def descriptor_active_mask(n: int, desc: Descriptor) -> int:
    pinned, left, right, forbidden = desc
    value = 0
    for x in range(1 << n):
        if (x >> pinned) & 1:
            continue
        pair = ((x >> left) & 1) | (((x >> right) & 1) << 1)
        if pair != forbidden:
            value |= 1 << x
    return value


def redundant_masks(sets: Sequence[int], full: int) -> list[int]:
    result = []
    for i, target in enumerate(sets):
        others = full
        for j, item in enumerate(sets):
            if i != j:
                others &= item
        if others & ~target == 0:
            result.append(i)
    return result


def family_isomorphism_signature(family: Sequence[Descriptor], n: int) -> tuple[Descriptor, ...]:
    best = None
    for perm in itertools.permutations(range(n)):
        transformed = []
        for pinned, left, right, forbidden in family:
            p, a, b = perm[pinned], perm[left], perm[right]
            f = forbidden
            if a > b:
                a, b = b, a
                f = {1: 2, 2: 1, 3: 3}[f]
            transformed.append((p, a, b, f))
        signature = tuple(sorted(transformed))
        if best is None or signature < best:
            best = signature
    assert best is not None
    return best


def v57_irredundant_families() -> list[tuple[Descriptor, ...]]:
    n = 4
    descriptors = normalized_descriptors(n)
    masks = [descriptor_active_mask(n, d) for d in descriptors]
    full = (1 << (1 << n)) - 1
    result = []
    for chosen in itertools.combinations(range(len(descriptors)), 5):
        sets = [masks[i] for i in chosen]
        if not redundant_masks(sets, full):
            result.append(tuple(descriptors[i] for i in chosen))
    return result


G4_DESCRIPTORS: tuple[Descriptor, ...] = (
    (0, 1, 2, 1),
    (0, 1, 2, 2),
    (0, 1, 3, 1),
    (0, 1, 3, 2),
    (0, 2, 3, 3),
)


def stretch_one_descriptors(k: int) -> tuple[int, tuple[Descriptor, ...]]:
    if k < 0:
        raise ValueError("k must be nonnegative")
    result = list(G4_DESCRIPTORS)
    offset = 4
    for _ in range(k):
        # Three clauses on one disjoint triple; common small-fiber assignment 000.
        result.extend((
            (offset + 2, offset, offset + 1, 1),
            (offset + 2, offset, offset + 1, 2),
            (offset + 2, offset, offset + 1, 3),
        ))
        offset += 3
    return 4 + 3 * k, tuple(result)


def universal_boundary_radius_bound(n: int, m: int) -> int:
    """Smallest r such that every non-surjective image has boundary distance <= r."""
    total = 0
    for d in range(m + 1):
        total += __import__("math").comb(m, d)
        if total > (1 << n):
            return d - 1
    return m - 1
