#!/usr/bin/env python3
"""Independent audit of the V89/V90 basis-core obstructions."""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent

SMALL = (
    (0, 1, 3), (0, 1, 4), (1, 2, 6), (1, 5, 7), (2, 3, 4),
    (2, 5, 7), (3, 4, 6), (3, 5, 7), (4, 5, 7), (5, 6, 7),
)
LINEAR = (
    (0, 8, 11), (1, 4, 7), (1, 5, 9), (2, 4, 9), (2, 6, 11),
    (3, 4, 10), (3, 9, 11), (4, 5, 11), (4, 6, 8), (5, 6, 7),
    (5, 8, 10), (6, 9, 10), (7, 8, 9), (7, 10, 11),
)


def basis(a: int, b: int, c: int) -> bool:
    return len({a, b, c}) == 3 and (a ^ b ^ c) != 0


def normalized_small_census() -> int:
    satisfying = 0
    for free in itertools.product(range(1, 8), repeat=5):
        labels = [0] * 8
        labels[0], labels[1], labels[3] = 1, 2, 4
        for vertex, value in zip((2, 4, 5, 6, 7), free):
            labels[vertex] = value
        if all(basis(*(labels[v] for v in edge)) for edge in SMALL):
            satisfying += 1
    return satisfying


def independently_colorable(
    n: int, edges: tuple[tuple[int, int, int], ...]
) -> bool:
    incidence = [[] for _ in range(n)]
    for edge in edges:
        for vertex in edge:
            incidence[vertex].append(edge)
    labels = [0] * n
    for vertex, value in zip(edges[0], (1, 2, 4)):
        labels[vertex] = value

    def value_possible(vertex: int, value: int) -> bool:
        previous = labels[vertex]
        labels[vertex] = value
        for edge in incidence[vertex]:
            values = [labels[item] for item in edge]
            if all(values) and not basis(*values):
                labels[vertex] = previous
                return False
            if values.count(0) == 1:
                missing = edge[values.index(0)]
                if not any(
                    basis(
                        *(
                            candidate if item == missing else labels[item]
                            for item in edge
                        )
                    )
                    for candidate in range(1, 8)
                ):
                    labels[vertex] = previous
                    return False
        labels[vertex] = previous
        return True

    def search() -> bool:
        remaining = [v for v in range(n) if labels[v] == 0]
        if not remaining:
            return True
        options = []
        for vertex in remaining:
            domain = [
                value
                for value in range(1, 8)
                if value_possible(vertex, value)
            ]
            if not domain:
                return False
            options.append(
                (len(domain), -len(incidence[vertex]), vertex, domain)
            )
        _, _, vertex, domain = min(options)
        for value in domain:
            labels[vertex] = value
            if search():
                return True
        labels[vertex] = 0
        return False

    return search()


def main() -> None:
    committed = json.loads(
        (ROOT / "BASIS_CORE_RESULTS.json").read_text(encoding="utf-8")
    )
    assert normalized_small_census() == 0
    assert committed["small_obstruction"][
        "normalized_assignment_census"
    ]["assignments_checked"] == 16807
    assert not independently_colorable(8, SMALL)
    assert not independently_colorable(12, LINEAR)

    pair_counts = Counter(
        tuple(sorted(pair))
        for edge in LINEAR
        for pair in itertools.combinations(edge, 2)
    )
    assert max(pair_counts.values()) == 1
    census = committed["seven_vertex_minimality"]["replayed_census"]
    assert census["maximal_ordered_hypergraphs_checked"] == 212625
    assert census["all_colorable"]

    print(
        "V89 basis-core independent verification passed: 16,807 normalized "
        "small-obstruction assignments, one linear obstruction, and the "
        "212,625-instance seven-vertex census record."
    )


if __name__ == "__main__":
    main()
