#!/usr/bin/env python3
"""Core routines for Laboratory V59.

V59 studies boundary abundance and boundary localization for the bijunctive
ternary NPN orbit 0x07. It separates geometry, randomized localization and
deterministic localization. Only Python's standard library is used.
"""
from __future__ import annotations
import itertools, math, random
from collections import defaultdict
from functools import lru_cache
from typing import Iterable, Sequence

Literal = tuple[int, bool]
Clause = tuple[Literal, ...]
Gate = tuple[int, tuple[int, int, int]]
Descriptor = tuple[int, int, int, int]

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
    return tuple(sorted({npn_transform(mask, perm, negs, outneg)
        for perm in itertools.permutations(range(3))
        for negs in itertools.product((0, 1), repeat=3)
        for outneg in (0, 1)}))

ORBIT_07 = npn_orbit(0x07)

def local_assignment(assignment: int, support: Sequence[int]) -> int:
    return sum(((assignment >> variable) & 1) << i for i, variable in enumerate(support))

def circuit_output(gates: Sequence[Gate], assignment: int) -> tuple[int, ...]:
    return tuple((mask >> local_assignment(assignment, support)) & 1 for mask, support in gates)

def image_with_preimages(n: int, gates: Sequence[Gate]) -> dict[tuple[int, ...], list[int]]:
    preimages: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for assignment in range(1 << n):
        preimages[circuit_output(gates, assignment)].append(assignment)
    return dict(preimages)

def hamming_neighbors(word: Sequence[int]) -> Iterable[tuple[int, ...]]:
    word = tuple(word)
    for coordinate in range(len(word)):
        neighbor = list(word); neighbor[coordinate] ^= 1; yield tuple(neighbor)

def internal_boundary(image: set[tuple[int, ...]]) -> set[tuple[int, ...]]:
    return {word for word in image if any(neighbor not in image for neighbor in hamming_neighbors(word))}

def harper_vertex_expansion_constant(m: int) -> float:
    if m <= 0: raise ValueError("m must be positive")
    return math.comb(m, m // 2) / (1 << (m - 1))

def boundary_sampling_lower_bound(n: int, m: int, image_size: int) -> float:
    if image_size <= 0: return 0.0
    if image_size > (1 << (m - 1)):
        raise ValueError("the Harper half-cube corollary requires image_size <= 2^(m-1)")
    return (image_size / (1 << n)) * harper_vertex_expansion_constant(m)

def eval_literal(literal: Literal, assignment: int) -> bool:
    variable, positive = literal; value = bool((assignment >> variable) & 1)
    return value if positive else not value

def eval_clause(clause: Clause, assignment: int) -> bool:
    return any(eval_literal(literal, assignment) for literal in clause)

def fiber(mask: int, value: int) -> frozenset[int]:
    return frozenset(x for x in range(8) if ((mask >> x) & 1) == value)

@lru_cache(maxsize=None)
def local_2cnf_for_fiber(mask: int, value: int) -> tuple[Clause, ...]:
    points = fiber(mask, value); candidates: list[Clause] = []
    for variable in range(3):
        for sign in (False, True): candidates.append(((variable, sign),))
    for first, second in itertools.combinations(range(3), 2):
        for first_sign in (False, True):
            for second_sign in (False, True): candidates.append(((first, first_sign), (second, second_sign)))
    valid = [clause for clause in candidates if all(eval_clause(clause, point) for point in points)]
    described = {point for point in range(8) if all(eval_clause(clause, point) for clause in valid)}
    if described != set(points): raise ValueError(f"fiber of 0x{mask:02x}, value {value}, is not bijunctive")
    reduced = list(valid); changed = True
    while changed:
        changed = False
        for index, clause in enumerate(tuple(reduced)):
            others = reduced[:index] + reduced[index + 1:]
            models = {point for point in range(8) if all(eval_clause(other, point) for other in others)}
            if all(eval_clause(clause, point) for point in models):
                reduced.pop(index); changed = True; break
    return tuple(reduced)

def global_clauses(gates: Sequence[Gate], orientation: Sequence[int]) -> tuple[Clause, ...]:
    clauses: list[Clause] = []
    for (mask, support), value in zip(gates, orientation):
        for local_clause in local_2cnf_for_fiber(mask, value):
            clauses.append(tuple((support[variable], sign) for variable, sign in local_clause))
    return tuple(clauses)

def unit_propagation_forced_count(n: int, clauses: Sequence[Clause]) -> tuple[int, bool]:
    values: list[int | None] = [None] * n; changed = True
    while changed:
        changed = False
        for clause in clauses:
            satisfied = False; undecided: list[Literal] = []
            for variable, positive in clause:
                if values[variable] is None: undecided.append((variable, positive))
                elif bool(values[variable]) == positive: satisfied = True; break
            if satisfied: continue
            if not undecided: return n + 1, True
            if len(undecided) == 1:
                variable, positive = undecided[0]; required = int(positive)
                if values[variable] is not None and values[variable] != required: return n + 1, True
                if values[variable] is None: values[variable] = required; changed = True
    return sum(value is not None for value in values), False

def exact_forced_variable_count(n: int, assignments: Sequence[int]) -> int:
    if not assignments: return n + 1
    bitwise_and = (1 << n) - 1; bitwise_or = 0
    for assignment in assignments: bitwise_and &= assignment; bitwise_or |= assignment
    return n - (bitwise_and ^ bitwise_or).bit_count()

def local_mask_for_forbidden(forbidden: int) -> int:
    forbidden_left = forbidden & 1; forbidden_right = (forbidden >> 1) & 1; mask = 0
    for local in range(8):
        pinned = local & 1; left = (local >> 1) & 1; right = (local >> 2) & 1
        if pinned == 0 and not (left == forbidden_left and right == forbidden_right): mask |= 1 << local
    return mask

def descriptor_to_gate(descriptor: Descriptor) -> Gate:
    pinned, left, right, forbidden = descriptor
    return local_mask_for_forbidden(forbidden), (pinned, left, right)

G4_DESCRIPTORS: tuple[Descriptor, ...] = ((0,1,2,1),(0,1,2,2),(0,1,3,1),(0,1,3,2),(0,2,3,3))

def stretch_one_direct_sum(k: int) -> tuple[int, tuple[Gate, ...]]:
    if k < 0: raise ValueError("k must be nonnegative")
    descriptors = list(G4_DESCRIPTORS); offset = 4
    for _ in range(k):
        descriptors.extend(((offset+2,offset,offset+1,1),(offset+2,offset,offset+1,2),(offset+2,offset,offset+1,3)))
        offset += 3
    return 4 + 3 * k, tuple(descriptor_to_gate(descriptor) for descriptor in descriptors)

def direct_sum_potential_audit(k: int) -> dict:
    n, gates = stretch_one_direct_sum(k); preimages = image_with_preimages(n, gates)
    image = set(preimages); boundary = internal_boundary(image); interior = image - boundary
    all_ones = (1,) * len(gates)
    if interior != {all_ones}: raise AssertionError("the direct-sum family should have the all-ones word as unique interior point")
    exact_forced = {word: exact_forced_variable_count(n, assignments) for word, assignments in preimages.items()}
    unit_forced = {word: unit_propagation_forced_count(n, global_clauses(gates, word))[0] for word in image}
    neighbor_words = tuple(hamming_neighbors(all_ones))
    return {"k":k,"n":n,"m":len(gates),"image_size":len(image),"boundary_size":len(boundary),
        "unique_interior":list(all_ones),"interior_preimages":len(preimages[all_ones]),
        "neighbor_preimages":[len(preimages[word]) for word in neighbor_words],
        "interior_exact_forced":exact_forced[all_ones],"neighbor_exact_forced":[exact_forced[word] for word in neighbor_words],
        "interior_unit_forced":unit_forced[all_ones],"neighbor_unit_forced":[unit_forced[word] for word in neighbor_words],
        "strict_exact_forced_improvement_exists":any(exact_forced[word] > exact_forced[all_ones] for word in neighbor_words),
        "strict_unit_improvement_exists":any(unit_forced[word] > unit_forced[all_ones] for word in neighbor_words),
        "strict_smaller_fiber_exists":any(len(preimages[word]) < len(preimages[all_ones]) for word in neighbor_words)}

def random_orbit_circuit(rng: random.Random, n: int) -> tuple[Gate, ...]:
    return tuple((rng.choice(ORBIT_07), tuple(rng.sample(range(n), 3))) for _ in range(n + 1))

def boundary_statistics(n: int, gates: Sequence[Gate]) -> dict:
    preimages = image_with_preimages(n, gates); image = set(preimages); boundary = internal_boundary(image); m = len(gates)
    input_boundary_probability = sum(len(preimages[word]) for word in boundary) / (1 << n)
    image_boundary_fraction = len(boundary) / len(image); alpha = len(image) / (1 << n)
    lower_bound = boundary_sampling_lower_bound(n, m, len(image))
    return {"n":n,"m":m,"image_size":len(image),"boundary_size":len(boundary),"occupancy_alpha":alpha,
        "uniform_image_boundary_fraction":image_boundary_fraction,"uniform_input_boundary_probability":input_boundary_probability,
        "harper_sampling_lower_bound":lower_bound,"ratio_to_lower_bound":input_boundary_probability/lower_bound if lower_bound else None}
