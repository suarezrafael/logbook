#!/usr/bin/env python3
"""Independent V89 audit without importing the primary implementation."""
from __future__ import annotations

import itertools
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent

V80 = {
    "seven_variables": (
        (0, 5, 6), (1, 3, 6), (0, 2, 4), (0, 4, 6),
        (2, 3, 5), (0, 3, 6), (0, 1, 2), (3, 4, 5),
        (2, 4, 5), (1, 5, 6), (2, 4, 6),
    ),
    "eight_variables": (
        (0, 1, 3), (0, 1, 4), (1, 2, 6), (2, 4, 7),
        (2, 3, 5), (0, 3, 7), (0, 3, 5), (1, 3, 6),
        (1, 2, 5), (0, 2, 4), (2, 6, 7), (0, 4, 7),
    ),
    "nine_variables": (
        (2, 3, 7), (2, 5, 7), (4, 5, 8), (0, 3, 6),
        (0, 5, 8), (3, 4, 7), (1, 2, 6), (1, 2, 4),
        (2, 6, 7), (5, 7, 8), (3, 4, 6), (1, 4, 8),
        (0, 1, 5), (0, 5, 6),
    ),
}
SAMPLES = (
    (10, 15, 88000),
    (10, 15, 88001),
    (12, 18, 88200),
    (12, 18, 88201),
    (14, 20, 88400),
    (14, 20, 88401),
    (16, 23, 88600),
    (16, 23, 88601),
)


def supports_for_sample(
    n: int, m: int, seed: int
) -> tuple[tuple[int, int, int], ...]:
    rng = random.Random(seed)
    return tuple(
        rng.sample(tuple(itertools.combinations(range(n), 3)), m)
    )


def adjacency(
    n: int, supports: tuple[tuple[int, int, int], ...]
) -> list[set[int]]:
    graph = [set() for _ in range(n)]
    for support in supports:
        for left, right in itertools.combinations(support, 2):
            graph[left].add(right)
            graph[right].add(left)
    return graph


def coloring_valid(graph: list[set[int]], coloring: list[int]) -> bool:
    return all(
        coloring[left] != coloring[right]
        for left in range(len(graph))
        for right in graph[left]
        if left < right
    )


def colorable_with(graph: list[set[int]], colors: int) -> bool:
    assigned = [-1] * len(graph)

    def search(done: int) -> bool:
        if done == len(graph):
            return True
        vertex = max(
            (v for v in range(len(graph)) if assigned[v] < 0),
            key=lambda v: (
                len(
                    {
                        assigned[u]
                        for u in graph[v]
                        if assigned[u] >= 0
                    }
                ),
                len(graph[v]),
            ),
        )
        forbidden = {
            assigned[u] for u in graph[vertex] if assigned[u] >= 0
        }
        used = max(assigned)
        for color in range(min(colors, used + 2)):
            if color in forbidden:
                continue
            assigned[vertex] = color
            if search(done + 1):
                return True
            assigned[vertex] = -1
        return False

    return search(0)


def basis(a: int, b: int, c: int) -> bool:
    return (
        len({a, b, c}) == 3
        and all(1 <= value <= 7 for value in (a, b, c))
        and (a ^ b ^ c) != 0
    )


def dot(left: int, right: int) -> int:
    return (left & right).bit_count() & 1


def basis_witness_valid(
    labels: list[int], supports: tuple[tuple[int, int, int], ...]
) -> bool:
    for u, v, w in supports:
        if not basis(labels[u], labels[v], labels[w]):
            return False
        addresses = {
            (
                dot(labels[u], row),
                dot(labels[v], row),
                dot(labels[w], row),
            )
            for row in range(8)
        }
        if len(addresses) != 8:
            return False
    return True


def oa_rows_direct() -> list[list[int]]:
    columns = [
        tuple((word >> coordinate) & 1 for coordinate in range(4))
        for word in range(16)
        if word.bit_count() % 2 == 0
    ]
    return [[column[row] for column in columns] for row in range(4)]


def main() -> None:
    committed = json.loads(
        (ROOT / "RESULTS.json").read_text(encoding="utf-8")
    )

    rows = oa_rows_direct()
    assert len(rows) == 4 and all(len(row) == 8 for row in rows)
    for chosen in itertools.combinations(range(4), 3):
        assert len(
            {
                tuple(rows[row][column] for row in chosen)
                for column in range(8)
            }
        ) == 8

    families: list[
        tuple[str, int, tuple[tuple[int, int, int], ...]]
    ] = []
    for name, supports in V80.items():
        n = max(max(support) for support in supports) + 1
        families.append((name, n, supports))
    for n, m, seed in SAMPLES:
        families.append(
            (f"v87_seed_{seed}", n, supports_for_sample(n, m, seed))
        )

    committed_rows = (
        committed["finite_audit"]["v80_controls"]
        + committed["finite_audit"]["v87_samples"]
    )
    assert len(committed_rows) == len(families) == 11

    observed = []
    for (name, n, supports), row in zip(families, committed_rows):
        assert row["name"] == name
        graph = adjacency(n, supports)
        witness = row["one_primal_coloring"]
        chromatic = row["primal_chromatic_number"]
        assert coloring_valid(graph, witness)
        assert max(witness) + 1 <= chromatic
        assert not colorable_with(graph, chromatic - 1)
        assert basis_witness_valid(row["one_basis_coloring"], supports)
        observed.append(chromatic)

    assert observed == [6, 5, 5, 5, 6, 5, 5, 5, 5, 5, 6]
    assert not committed["scientific_status"][
        "v87_random_model_basis_colorable_whp"
    ]
    assert not committed["scientific_status"][
        "support_only_universal_list_lower_bound_nine"
    ]

    print(
        "V89 independent verification passed: direct even-parity OA, "
        "11 exact chromatic lower checks, and 11 affine basis-address "
        "witnesses."
    )


if __name__ == "__main__":
    main()
