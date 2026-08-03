from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import ceil, log2
from typing import Callable, Iterable, Mapping, Sequence

Presentation = tuple[tuple[int, ...], ...]
GirthOracle = Callable[[tuple[int, ...], int], bool]


def normalize_presentation(supports: Sequence[Iterable[int]]) -> Presentation:
    return tuple(tuple(sorted(set(row))) for row in supports)


def maximum_matching_size(
    supports: Presentation, active: Sequence[int]
) -> int:
    match_right: dict[int, int] = {}

    def augment(left: int, seen: set[int]) -> bool:
        for right in supports[left]:
            if right in seen:
                continue
            seen.add(right)
            owner = match_right.get(right)
            if owner is None or augment(owner, seen):
                match_right[right] = left
                return True
        return False

    rank = 0
    for left in sorted(active, key=lambda e: (len(supports[e]), e)):
        if augment(left, set()):
            rank += 1
    return rank


def is_dependent(supports: Presentation, active: Sequence[int]) -> bool:
    return maximum_matching_size(supports, active) < len(active)


def brute_circuits(
    supports: Presentation, active: Sequence[int] | None = None
) -> tuple[tuple[int, ...], ...]:
    ground = tuple(range(len(supports))) if active is None else tuple(active)
    circuits: list[tuple[int, ...]] = []
    for mask in range(1, 1 << len(ground)):
        subset = tuple(ground[i] for i in range(len(ground)) if mask & (1 << i))
        if not is_dependent(supports, subset):
            continue
        if all(
            not is_dependent(supports, tuple(x for x in subset if x != e))
            for e in subset
        ):
            circuits.append(subset)
    return tuple(circuits)


def brute_girth(
    supports: Presentation, active: Sequence[int] | None = None
) -> int | None:
    circuits = brute_circuits(supports, active)
    return min((len(circuit) for circuit in circuits), default=None)


@dataclass
class CountingD3GirthOracle:
    supports: Presentation
    queries: int = 0

    def __post_init__(self) -> None:
        if max((len(row) for row in self.supports), default=0) > 3:
            raise ValueError("left degree exceeds three")

    def __call__(self, active: tuple[int, ...], threshold: int) -> bool:
        self.queries += 1
        if threshold < 1:
            return False
        ground = tuple(active)
        for mask in range(1, 1 << len(ground)):
            if mask.bit_count() > threshold:
                continue
            subset = tuple(ground[i] for i in range(len(ground)) if mask & (1 << i))
            if is_dependent(self.supports, subset):
                return True
        return False


@dataclass(frozen=True)
class ExtractionResult:
    girth: int | None
    circuit: tuple[int, ...] | None
    neighborhood: tuple[int, ...] | None
    query_count: int


def exact_girth_with_oracle(
    element_count: int,
    oracle: GirthOracle,
    active: Sequence[int] | None = None,
    *,
    dependence_guaranteed: bool = False,
) -> int | None:
    ground = tuple(range(element_count)) if active is None else tuple(active)
    if not ground:
        return None
    if not dependence_guaranteed and not oracle(ground, len(ground)):
        return None
    low, high = 1, len(ground)
    while low < high:
        middle = (low + high) // 2
        if oracle(ground, middle):
            high = middle
        else:
            low = middle + 1
    return low


def deletion_canonical_shortest_circuit(
    element_count: int,
    girth: int,
    oracle: GirthOracle,
    active: Sequence[int] | None = None,
    order: Sequence[int] | None = None,
) -> tuple[int, ...]:
    current = list(range(element_count)) if active is None else list(active)
    processing_order = tuple(current) if order is None else tuple(order)
    current_set = set(current)
    for element in processing_order:
        if element not in current_set:
            continue
        trial = tuple(x for x in current if x != element)
        # Deletion cannot create a shorter circuit, so a yes answer at the
        # already-known girth means that the girth is preserved exactly.
        if oracle(trial, girth):
            current = list(trial)
            current_set.remove(element)
    return tuple(current)


def extract_girth_circuit_and_hall_witness(
    supports: Sequence[Iterable[int]],
    oracle: GirthOracle,
    *,
    dependence_guaranteed: bool = False,
) -> ExtractionResult:
    presentation = normalize_presentation(supports)
    before = getattr(oracle, "queries", 0)
    girth = exact_girth_with_oracle(
        len(presentation),
        oracle,
        dependence_guaranteed=dependence_guaranteed,
    )
    if girth is None:
        after = getattr(oracle, "queries", before)
        return ExtractionResult(None, None, None, after - before)
    circuit = deletion_canonical_shortest_circuit(
        len(presentation), girth, oracle
    )
    neighborhood = tuple(
        sorted({right for left in circuit for right in presentation[left]})
    )
    after = getattr(oracle, "queries", before)
    return ExtractionResult(girth, circuit, neighborhood, after - before)


def query_bound(element_count: int, dependence_guaranteed: bool) -> int:
    if element_count <= 0:
        return 0
    existence = 0 if dependence_guaranteed else 1
    return existence + ceil(log2(element_count)) + element_count


def is_hall_expanding_through(
    supports: Presentation, active: Sequence[int], threshold: int
) -> bool:
    ground = tuple(active)
    for mask in range(1, 1 << len(ground)):
        if mask.bit_count() > threshold:
            continue
        subset = tuple(ground[i] for i in range(len(ground)) if mask & (1 << i))
        neighborhood = {right for left in subset for right in supports[left]}
        if len(neighborhood) < len(subset):
            return False
    return True


@dataclass(frozen=True)
class LocalGate:
    support: tuple[int, ...]
    truth_table: tuple[int, ...]

    def __post_init__(self) -> None:
        if len(self.support) > 3:
            raise ValueError("gate support exceeds three")
        if len(self.truth_table) != 1 << len(self.support):
            raise ValueError("truth table has the wrong length")
        if any(bit not in (0, 1) for bit in self.truth_table):
            raise ValueError("truth table must be Boolean")

    def evaluate(self, assignment: Mapping[int, int]) -> int:
        index = 0
        for offset, variable in enumerate(self.support):
            index |= assignment[variable] << offset
        return self.truth_table[index]


@dataclass(frozen=True)
class AvoidWitness:
    circuit: tuple[int, ...]
    neighborhood: tuple[int, ...]
    missing_projection: tuple[int, ...]
    global_output: tuple[int, ...]
    local_assignments_enumerated: int


def local_enumeration_and_lift(
    gates: Sequence[LocalGate], circuit: Sequence[int]
) -> AvoidWitness:
    chosen = tuple(circuit)
    neighborhood = tuple(
        sorted({variable for gate_index in chosen for variable in gates[gate_index].support})
    )
    image: set[tuple[int, ...]] = set()
    for bits in product((0, 1), repeat=len(neighborhood)):
        assignment = dict(zip(neighborhood, bits))
        image.add(tuple(gates[index].evaluate(assignment) for index in chosen))
    missing = next(
        pattern
        for pattern in product((0, 1), repeat=len(chosen))
        if pattern not in image
    )
    global_output = [0] * len(gates)
    for gate_index, bit in zip(chosen, missing):
        global_output[gate_index] = bit
    return AvoidWitness(
        circuit=chosen,
        neighborhood=neighborhood,
        missing_projection=missing,
        global_output=tuple(global_output),
        local_assignments_enumerated=1 << len(neighborhood),
    )


def evaluate_circuit(gates: Sequence[LocalGate], input_bits: Sequence[int]) -> tuple[int, ...]:
    assignment = {index: bit for index, bit in enumerate(input_bits)}
    return tuple(gate.evaluate(assignment) for gate in gates)


def output_is_avoided(
    gates: Sequence[LocalGate], output: Sequence[int], input_count: int
) -> bool:
    target = tuple(output)
    return all(
        evaluate_circuit(gates, bits) != target
        for bits in product((0, 1), repeat=input_count)
    )


def private_path_circuit(length: int) -> Presentation:
    if length < 1:
        raise ValueError("length must be positive")
    supports: list[tuple[int, ...]] = []
    for index in range(length):
        row: list[int] = []
        if index > 0:
            row.append(index - 1)
        if index < length - 1:
            row.append(index)
        supports.append(tuple(row))
    return tuple(supports)
