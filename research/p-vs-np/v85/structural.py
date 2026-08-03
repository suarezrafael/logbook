#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
from math import comb
from typing import Iterable, Sequence


@dataclass(frozen=True)
class Gate:
    support: tuple[int, ...]
    truth_mask: int


@dataclass(frozen=True)
class Circuit:
    n: int
    gates: tuple[Gate, ...]

    @property
    def m(self) -> int:
        return len(self.gates)


def truth_from_anf(arity: int, monomials: Iterable[int]) -> int:
    monomials = tuple(monomials)
    truth = 0
    for x in range(1 << arity):
        value = 0
        for monomial in monomials:
            if (x & monomial) == monomial:
                value ^= 1
        truth |= value << x
    return truth


def anf_coefficients(truth_mask: int, arity: int) -> tuple[int, ...]:
    coeff = [(truth_mask >> x) & 1 for x in range(1 << arity)]
    for bit in range(arity):
        for mask in range(1 << arity):
            if mask & (1 << bit):
                coeff[mask] ^= coeff[mask ^ (1 << bit)]
    return tuple(coeff)


def essential_mask(truth_mask: int, arity: int) -> int:
    result = 0
    for bit in range(arity):
        for x in range(1 << arity):
            if ((truth_mask >> x) ^ (truth_mask >> (x ^ (1 << bit)))) & 1:
                result |= 1 << bit
                break
    return result


def gate_global_anf(gate: Gate) -> tuple[int, set[frozenset[int]]]:
    coeff = anf_coefficients(gate.truth_mask, len(gate.support))
    constant = coeff[0]
    monomials: set[frozenset[int]] = set()
    for local_mask, value in enumerate(coeff):
        if local_mask == 0 or not value:
            continue
        monomials.add(
            frozenset(
                gate.support[j]
                for j in range(len(gate.support))
                if local_mask & (1 << j)
            )
        )
    return constant, monomials


def is_affine_gate(gate: Gate) -> bool:
    _, monomials = gate_global_anf(gate)
    return all(len(monomial) <= 1 for monomial in monomials)


def linear_row(gate: Gate, n: int) -> int:
    _, monomials = gate_global_anf(gate)
    row = 0
    for monomial in monomials:
        if len(monomial) == 1:
            row ^= 1 << next(iter(monomial))
    return row


def nonconstant_feature_rows(circuit: Circuit) -> tuple[list[int], tuple[frozenset[int], ...]]:
    all_features: set[frozenset[int]] = set()
    gate_features: list[set[frozenset[int]]] = []
    for gate in circuit.gates:
        _, features = gate_global_anf(gate)
        gate_features.append(features)
        all_features.update(features)
    ordered = tuple(sorted(all_features, key=lambda s: (len(s), tuple(sorted(s)))))
    index = {feature: j for j, feature in enumerate(ordered)}
    rows = []
    for features in gate_features:
        row = 0
        for feature in features:
            row ^= 1 << index[feature]
        rows.append(row)
    return rows, ordered


def dependency_basis(rows: Sequence[int]) -> tuple[int, ...]:
    """Return a basis of GF(2) dependencies among the supplied row vectors."""
    pivots: dict[int, tuple[int, int]] = {}
    dependencies: list[int] = []
    for index, original in enumerate(rows):
        value = original
        combination = 1 << index
        while value:
            pivot = value.bit_length() - 1
            if pivot in pivots:
                value ^= pivots[pivot][0]
                combination ^= pivots[pivot][1]
            else:
                pivots[pivot] = (value, combination)
                break
        if value == 0:
            dependencies.append(combination)
    return tuple(dependencies)


def span(basis: Sequence[int]) -> tuple[int, ...]:
    values = [0]
    for vector in basis:
        values += [value ^ vector for value in values]
    return tuple(values)


def xor_rows(rows: Sequence[int], selector: int) -> int:
    result = 0
    for i, row in enumerate(rows):
        if selector & (1 << i):
            result ^= row
    return result


def constant_syndrome_vectors(circuit: Circuit) -> tuple[int, ...]:
    rows, _ = nonconstant_feature_rows(circuit)
    return span(dependency_basis(rows))


def linear_cokernel_vectors(circuit: Circuit) -> tuple[int, ...]:
    rows = [linear_row(gate, circuit.n) for gate in circuit.gates]
    return span(dependency_basis(rows))


def supports_are_linear(gates: Sequence[Gate]) -> bool:
    return all(
        len(set(a.support) & set(b.support)) <= 1
        for a, b in combinations(gates, 2)
    )


def incidence_girth(circuit: Circuit) -> int:
    size = circuit.m + circuit.n
    adjacency = [[] for _ in range(size)]
    for i, gate in enumerate(circuit.gates):
        for variable in gate.support:
            adjacency[i].append(circuit.m + variable)
            adjacency[circuit.m + variable].append(i)
    best = 10**9
    from collections import deque
    for source in range(size):
        distance = [-1] * size
        parent = [-1] * size
        distance[source] = 0
        queue = deque([source])
        while queue:
            current = queue.popleft()
            for nxt in adjacency[current]:
                if distance[nxt] < 0:
                    distance[nxt] = distance[current] + 1
                    parent[nxt] = current
                    queue.append(nxt)
                elif parent[current] != nxt:
                    best = min(best, distance[current] + distance[nxt] + 1)
    return 0 if best == 10**9 else best


def syndrome_constant(circuit: Circuit, selector: int) -> tuple[bool, int]:
    constants = 0
    feature_xor: set[frozenset[int]] = set()
    for i, gate in enumerate(circuit.gates):
        if not (selector & (1 << i)):
            continue
        constant, features = gate_global_anf(gate)
        constants ^= constant
        for feature in features:
            if feature in feature_xor:
                feature_xor.remove(feature)
            else:
                feature_xor.add(feature)
    return not feature_xor, constants


def evaluate_gate(gate: Gate, assignment: int) -> int:
    local = 0
    for j, variable in enumerate(gate.support):
        local |= ((assignment >> variable) & 1) << j
    return (gate.truth_mask >> local) & 1


def evaluate_circuit(circuit: Circuit, assignment: int) -> int:
    output = 0
    for i, gate in enumerate(circuit.gates):
        output |= evaluate_gate(gate, assignment) << i
    return output


def hall_deficient_subsets(circuit: Circuit) -> tuple[tuple[int, int], ...]:
    bad: list[tuple[int, int]] = []
    for selector in range(1, 1 << circuit.m):
        neighborhood: set[int] = set()
        for i, gate in enumerate(circuit.gates):
            if selector & (1 << i):
                neighborhood.update(gate.support)
        if selector.bit_count() > len(neighborhood):
            bad.append((selector, len(neighborhood)))
    return tuple(bad)


def affine_plane_order_three_supports() -> tuple[tuple[int, int, int], ...]:
    supports: list[tuple[int, int, int]] = []
    for a in range(3):
        for b in range(3):
            supports.append(tuple(sorted(3*x + ((a*x+b) % 3) for x in range(3))))
    for b in range(3):
        supports.append(tuple(3*b+y for y in range(3)))
    return tuple(supports)


def counterexample_circuit() -> tuple[Circuit, int]:
    supports = (
        (0, 1, 2),
        (0, 1, 3),
        (2, 4, 5),
        (3, 4, 5),
        (0, 1, 4),
        (0, 1, 5),
        (0, 2, 3),
    )
    masks = (
        truth_from_anf(3, (0b011, 0b100)),
        truth_from_anf(3, (0b011, 0b100)),
        truth_from_anf(3, (0b001, 0b010, 0b100)),
        truth_from_anf(3, (0b001, 0b010, 0b100)),
        truth_from_anf(3, (0b001, 0b010, 0b100)),
        truth_from_anf(3, (0b001, 0b010, 0b100)),
        truth_from_anf(3, (0b001, 0b010, 0b100)),
    )
    circuit = Circuit(6, tuple(Gate(s, t) for s, t in zip(supports, masks)))
    return circuit, 0b0001111


def hamming_ball_volume(m: int, radius: int) -> int:
    if radius < 0:
        return 0
    return sum(comb(m, j) for j in range(min(m, radius) + 1))


def pair_count_for_prefix(circuit: Circuit, prefix: tuple[int, ...], radius: int) -> int:
    remaining = circuit.m - len(prefix)
    total = 0
    for assignment in range(1 << circuit.n):
        output = evaluate_circuit(circuit, assignment)
        mismatch = 0
        for i, bit in enumerate(prefix):
            mismatch += bit != ((output >> i) & 1)
        total += hamming_ball_volume(remaining, radius - mismatch)
    return total


def remote_point_by_pair_count(circuit: Circuit, radius: int) -> int:
    if (1 << circuit.n) * hamming_ball_volume(circuit.m, radius) >= (1 << circuit.m):
        raise ValueError("volume condition is not strict")
    prefix: tuple[int, ...] = ()
    if pair_count_for_prefix(circuit, prefix, radius) >= (1 << circuit.m):
        raise AssertionError("initial counting invariant failed")
    for length in range(circuit.m):
        capacity = 1 << (circuit.m - length - 1)
        counts = [pair_count_for_prefix(circuit, prefix + (bit,), radius) for bit in (0, 1)]
        candidates = [bit for bit in (0, 1) if counts[bit] < capacity]
        if not candidates:
            raise AssertionError((prefix, counts, capacity))
        prefix += (min(candidates, key=lambda bit: (counts[bit], bit)),)
    result = sum(bit << i for i, bit in enumerate(prefix))
    if pair_count_for_prefix(circuit, prefix, radius) != 0:
        raise AssertionError("leaf must have zero nearby preimages")
    return result


def distance_to_range(circuit: Circuit, target: int) -> int:
    return min((evaluate_circuit(circuit, x) ^ target).bit_count() for x in range(1 << circuit.n))


def random_truth_masks(seed: int, count: int) -> tuple[int, ...]:
    state = seed & 0xFFFFFFFF
    values = []
    for _ in range(count):
        state ^= (state << 13) & 0xFFFFFFFF
        state ^= state >> 17
        state ^= (state << 5) & 0xFFFFFFFF
        values.append(state & 0xFF)
    return tuple(values)


def make_remote_probe_circuit(seed: int, n: int, m: int) -> Circuit:
    triples = list(combinations(range(n), min(3, n)))
    masks = random_truth_masks(seed, m)
    gates = []
    for i in range(m):
        support = triples[(seed * 17 + i * 7) % len(triples)]
        gates.append(Gate(tuple(support), masks[i]))
    return Circuit(n, tuple(gates))


def affine_truth_masks_arity3() -> tuple[int, ...]:
    masks = []
    for constant in (0, 1):
        for subset in range(8):
            terms = [1 << j for j in range(3) if subset & (1 << j)]
            if constant:
                terms.append(0)
            masks.append(truth_from_anf(3, terms))
    return tuple(masks)


def make_linear_probe_masks(seed: int, count: int, mode: str) -> tuple[int, ...]:
    raw = random_truth_masks(seed, max(count, 32))
    if mode == "random":
        return raw[:count]
    if mode != "affine_heavy":
        raise ValueError(mode)
    affine = affine_truth_masks_arity3()
    masks = [affine[raw[i] % len(affine)] for i in range(max(0, count - 2))]
    nonaffine = (truth_from_anf(3, (0b111,)), 0xE8)
    masks.extend(nonaffine[: min(2, count)])
    return tuple(masks[:count])
