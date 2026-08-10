#!/usr/bin/env python3
"""Comparison-free range avoidance from a positive-surplus support component."""
from __future__ import annotations

import hashlib
from typing import Sequence


BitWord = tuple[int, ...]


def incidence_components(n: int, supports: Sequence[tuple[int, ...]]) -> list[dict]:
    """Connected components of the bipartite input/output incidence graph."""
    m = len(supports)
    total = n + m
    parent = list(range(total))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for output, support in enumerate(supports):
        assert len(set(support)) == len(support)
        assert len(support) <= 3
        assert all(0 <= variable < n for variable in support)
        output_node = n + output
        for variable in support:
            union(variable, output_node)

    groups: dict[int, dict[str, list[int]]] = {}
    for variable in range(n):
        root = find(variable)
        groups.setdefault(root, {"inputs": [], "outputs": []})["inputs"].append(variable)
    for output in range(m):
        root = find(n + output)
        groups.setdefault(root, {"inputs": [], "outputs": []})["outputs"].append(output)

    return [
        {"inputs": tuple(group["inputs"]), "outputs": tuple(group["outputs"])}
        for group in groups.values()
    ]


def surplus_component_parameter(n: int, supports: Sequence[tuple[int, ...]]) -> int:
    """Minimum input count among components having more outputs than inputs."""
    assert len(supports) >= n + 1
    positive = [
        len(component["inputs"])
        for component in incidence_components(n, supports)
        if len(component["outputs"]) > len(component["inputs"])
    ]
    assert positive, "global output surplus guarantees a positive component"
    return min(positive)


def evaluate_gate(
    support: tuple[int, ...], table: Sequence[int], assignment: Sequence[int]
) -> int:
    assert len(table) == 1 << len(support)
    index = 0
    for position, variable in enumerate(support):
        index |= assignment[variable] << position
    return int(table[index])


def evaluate_circuit(
    n: int,
    supports: Sequence[tuple[int, ...]],
    tables: Sequence[Sequence[int]],
    assignment: Sequence[int],
) -> BitWord:
    assert len(assignment) == n
    return tuple(
        evaluate_gate(support, table, assignment)
        for support, table in zip(supports, tables, strict=True)
    )


def surplus_component_avoider(
    n: int,
    supports: Sequence[tuple[int, ...]],
    tables: Sequence[Sequence[int]],
) -> dict:
    """Return an absent word in time O(2^rho poly(N)).

    rho is the minimum input size of a support-incidence component whose number
    of outputs exceeds its number of inputs.  Enumerate only that component's
    local inputs.  Its local range has at most 2^rho words but its output space
    has at least 2^(rho+1), so one of the first 2^rho+1 binary words is absent.
    """
    m = len(supports)
    assert m >= n + 1
    assert len(tables) == m
    components = incidence_components(n, supports)
    positive = [
        component
        for component in components
        if len(component["outputs"]) > len(component["inputs"])
    ]
    assert positive
    component = min(positive, key=lambda item: len(item["inputs"]))
    local_inputs = component["inputs"]
    local_outputs = component["outputs"]
    rho = len(local_inputs)
    out_count = len(local_outputs)
    assert out_count > rho

    local_range: set[BitWord] = set()
    for mask in range(1 << rho):
        assignment = [0] * n
        for position, variable in enumerate(local_inputs):
            assignment[variable] = (mask >> position) & 1
        word = tuple(
            evaluate_gate(supports[output], tables[output], assignment)
            for output in local_outputs
        )
        local_range.add(word)

    candidate_limit = (1 << rho) + 1
    missing_local = None
    for value in range(candidate_limit):
        candidate = tuple(
            (value >> (out_count - 1 - position)) & 1
            for position in range(out_count)
        )
        if candidate not in local_range:
            missing_local = candidate
            break
    assert missing_local is not None

    global_word = [0] * m
    for position, output in enumerate(local_outputs):
        global_word[output] = missing_local[position]

    return {
        "word": tuple(global_word),
        "rho": rho,
        "component_inputs": local_inputs,
        "component_outputs": local_outputs,
        "local_range_size": len(local_range),
        "candidate_limit": candidate_limit,
    }


def partitioned_supports(n: int) -> list[tuple[int, ...]]:
    """Deterministic audit family with one positive component of <=3 inputs."""
    assert n >= 3
    blocks: list[tuple[int, ...]] = []
    cursor = 0
    while cursor < n:
        size = min(3, n - cursor)
        blocks.append(tuple(range(cursor, cursor + size)))
        cursor += size

    supports: list[tuple[int, ...]] = []
    for block_index, block in enumerate(blocks):
        copies = len(block) + (1 if block_index == 0 else 0)
        support = block if len(block) <= 3 else block[:3]
        for _ in range(copies):
            supports.append(support)
    assert len(supports) == n + 1
    return supports


def deterministic_tables(
    supports: Sequence[tuple[int, ...]], case: int
) -> list[list[int]]:
    tables: list[list[int]] = []
    for output, support in enumerate(supports):
        table = []
        for row in range(1 << len(support)):
            digest = hashlib.sha256(
                f"V96-component:{case}:{output}:{row}".encode("utf-8")
            ).digest()
            table.append(digest[0] & 1)
        tables.append(table)
    return tables


def build_component_audit() -> dict:
    cases = 0
    absence_failures = 0
    rho_mismatches = 0
    brute_force_inputs = 0
    max_rho = 0
    for n in range(4, 11):
        supports = partitioned_supports(n)
        expected_rho = min(3, n)
        for case in range(8):
            tables = deterministic_tables(supports, case)
            result = surplus_component_avoider(n, supports, tables)
            max_rho = max(max_rho, result["rho"])
            if result["rho"] != expected_rho:
                rho_mismatches += 1
            target = result["word"]
            found = False
            for mask in range(1 << n):
                assignment = tuple((mask >> i) & 1 for i in range(n))
                brute_force_inputs += 1
                if evaluate_circuit(n, supports, tables, assignment) == target:
                    found = True
                    break
            if found:
                absence_failures += 1
            cases += 1

    return {
        "input_sizes": list(range(4, 11)),
        "cases_per_size": 8,
        "total_cases": cases,
        "brute_force_input_evaluations": brute_force_inputs,
        "maximum_surplus_component_parameter": max_rho,
        "rho_mismatches": rho_mismatches,
        "absence_failures": absence_failures,
        "runtime_formula": "O(2^rho * poly(N))",
        "polynomial_when": "rho=O(log N)",
    }


if __name__ == "__main__":
    import json

    print(json.dumps(build_component_audit(), indent=2, sort_keys=True))
