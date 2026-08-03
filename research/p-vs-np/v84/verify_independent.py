#!/usr/bin/env python3
from __future__ import annotations

import json
from itertools import product
from math import ceil, log2
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def version_number(value: str) -> int:
    assert value.startswith("V") and value[1:].isdigit()
    return int(value[1:])


def matching_rank(supports: tuple[tuple[int, ...], ...], active: tuple[int, ...]) -> int:
    owner: dict[int, int] = {}

    def augment(left: int, seen: set[int]) -> bool:
        for right in supports[left]:
            if right in seen:
                continue
            seen.add(right)
            previous = owner.get(right)
            if previous is None or augment(previous, seen):
                owner[right] = left
                return True
        return False

    rank = 0
    for left in active:
        rank += int(augment(left, set()))
    return rank


def dependent(supports: tuple[tuple[int, ...], ...], active: tuple[int, ...]) -> bool:
    return matching_rank(supports, active) < len(active)


def circuits(supports: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    ground = tuple(range(len(supports)))
    answer = []
    for mask in range(1, 1 << len(ground)):
        subset = tuple(i for i in ground if mask & (1 << i))
        if dependent(supports, subset) and all(
            not dependent(supports, tuple(x for x in subset if x != e))
            for e in subset
        ):
            answer.append(subset)
    return tuple(answer)


class Oracle:
    def __init__(self, supports: tuple[tuple[int, ...], ...]) -> None:
        self.supports = supports
        self.queries = 0

    def ask(self, active: tuple[int, ...], threshold: int) -> bool:
        self.queries += 1
        for mask in range(1, 1 << len(active)):
            if mask.bit_count() > threshold:
                continue
            subset = tuple(active[i] for i in range(len(active)) if mask & (1 << i))
            if dependent(self.supports, subset):
                return True
        return False


def extract(supports: tuple[tuple[int, ...], ...], guaranteed: bool) -> tuple[int | None, tuple[int, ...] | None, int]:
    oracle = Oracle(supports)
    ground = tuple(range(len(supports)))
    if not ground:
        return None, None, 0
    if not guaranteed and not oracle.ask(ground, len(ground)):
        return None, None, oracle.queries
    low, high = 1, len(ground)
    while low < high:
        middle = (low + high) // 2
        if oracle.ask(ground, middle):
            high = middle
        else:
            low = middle + 1
    girth = low
    current = ground
    for element in ground:
        trial = tuple(x for x in current if x != element)
        if oracle.ask(trial, girth):
            current = trial
    return girth, current, oracle.queries


def path_circuit(length: int) -> tuple[tuple[int, ...], ...]:
    rows = []
    for i in range(length):
        row = []
        if i > 0:
            row.append(i - 1)
        if i < length - 1:
            row.append(i)
        rows.append(tuple(row))
    return tuple(rows)


def gate_value(support: tuple[int, ...], table: tuple[int, ...], assignment: tuple[int, ...]) -> int:
    index = sum(assignment[var] << offset for offset, var in enumerate(support))
    return table[index]


def truth_tables(arity: int):
    for mask in range(1 << (1 << arity)):
        yield tuple((mask >> i) & 1 for i in range(1 << arity))


def local_avoidance_audit(supports: tuple[tuple[int, ...], ...]) -> int:
    cs = circuits(supports)
    girth = min(map(len, cs))
    shortest = [c for c in cs if len(c) == girth]
    # Independent reference for fixed-order deletion: greedily prefer excluding
    # each early element whenever a shortest circuit permits it.
    candidates = [set(c) for c in shortest]
    for e in range(len(supports)):
        excluding = [c for c in candidates if e not in c]
        if excluding:
            candidates = excluding
    assert len(candidates) == 1
    chosen = tuple(sorted(candidates[0]))
    neighborhood = tuple(sorted({v for e in chosen for v in supports[e]}))
    assert len(neighborhood) == girth - 1
    all_tables = [tuple(truth_tables(len(row))) for row in supports]
    checked = 0
    input_count = max(neighborhood, default=-1) + 1
    for tables in product(*all_tables):
        image = set()
        for local_bits in product((0, 1), repeat=len(neighborhood)):
            assignment_map = dict(zip(neighborhood, local_bits))
            assignment = tuple(assignment_map.get(i, 0) for i in range(input_count))
            image.add(
                tuple(
                    gate_value(supports[e], tables[e], assignment) for e in chosen
                )
            )
        missing = next(
            z for z in product((0, 1), repeat=len(chosen)) if z not in image
        )
        target = [0] * len(supports)
        for e, bit in zip(chosen, missing):
            target[e] = bit
        for assignment in product((0, 1), repeat=input_count):
            output = tuple(
                gate_value(supports[e], tables[e], assignment)
                for e in range(len(supports))
            )
            assert output != tuple(target)
        checked += 1
    return checked


def main() -> None:
    committed = json.loads((HERE / "RESULTS.json").read_text(encoding="utf-8"))

    for length in range(2, 11):
        supports = path_circuit(length)
        cs = circuits(supports)
        assert cs == (tuple(range(length)),)
        girth, circuit, queries = extract(supports, guaranteed=True)
        assert girth == length
        assert circuit == tuple(range(length))
        assert queries <= ceil(log2(length)) + length
        neighborhood = {v for e in circuit for v in supports[e]}
        assert len(neighborhood) == length - 1
        for threshold in range(1, length):
            for mask in range(1, 1 << length):
                if mask.bit_count() > threshold:
                    continue
                subset = tuple(i for i in range(length) if mask & (1 << i))
                assert len({v for e in subset for v in supports[e]}) >= len(subset)

    # Multiple-shortest-circuit control: fixed-order deletion must select one
    # canonical circuit and remove all irrelevant elements.
    supports = ((0,), (0,), (1,), (1,))
    assert circuits(supports) == ((0, 1), (2, 3))
    girth, circuit, _queries = extract(supports, guaranteed=True)
    assert girth == 2
    assert circuit == (2, 3)

    assert local_avoidance_audit(((0,), (0,))) == 16
    assert local_avoidance_audit(((0,), (1,), (0, 1))) == 256

    assert committed["exhaustive_extraction_census"]["presentations_checked"] == 832
    assert committed["local_avoidance_census"]["avoided_outputs_verified"] == 272
    assert committed["complexity_boundary"]["unrestricted_NC0_3_avoid_solved"] is False

    status = json.loads((ROOT / "LAB_STATUS.json").read_text(encoding="utf-8"))
    promoted = status["promoted_version"]
    candidate = status.get("candidate_version")
    assert version_number(promoted) >= 84 or (
        candidate is not None and version_number(candidate) >= 84
    )
    if candidate is None:
        assert status["highest_directory"] == promoted
        assert status["promotion_state"] == "promoted"
    else:
        assert version_number(candidate) == version_number(promoted) + 1
        assert status["highest_directory"] == candidate
        assert status["promotion_state"] == "candidate"
    assert status["scientific_status"]["exact_degree_three_girth_in_FP_NP"] is True
    assert status["scientific_status"]["logarithmic_hall_expander_promise_reduction"] is True
    assert status["scientific_status"]["p_vs_np_resolved"] is False

    print(
        "V84 independent verification passed: deletion self-reduction, exact "
        "Hall neighborhoods, 272 local truth-table lifts, and long-girth "
        "Hall-expansion controls were independently checked."
    )


if __name__ == "__main__":
    main()
