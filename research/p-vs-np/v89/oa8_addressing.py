#!/usr/bin/env python3
"""V89: eight-row target-independent addressing via binary orthogonal arrays."""
from __future__ import annotations

import itertools
import random
from typing import Sequence

Support = tuple[int, int, int]

V80_SUPPORTS: dict[str, tuple[Support, ...]] = {
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

V87_RANDOM_SAMPLES = (
    (10, 15, 88000),
    (10, 15, 88001),
    (12, 18, 88200),
    (12, 18, 88201),
    (14, 20, 88400),
    (14, 20, 88401),
    (16, 23, 88600),
    (16, 23, 88601),
)


def sample_supports(n: int, m: int, seed: int) -> tuple[Support, ...]:
    rng = random.Random(seed)
    return tuple(rng.sample(tuple(itertools.combinations(range(n), 3)), m))


def dot3(left: int, right: int) -> int:
    return (left & right).bit_count() & 1


def basis_triple(a: int, b: int, c: int) -> bool:
    """Whether three nonzero vectors form a basis of F_2^3."""
    return (
        a in range(1, 8)
        and b in range(1, 8)
        and c in range(1, 8)
        and len({a, b, c}) == 3
        and (a ^ b ^ c) != 0
    )


def affine_pattern(vector: int) -> int:
    """Eight-bit truth table x -> <vector,x>, rows x=0,...,7."""
    pattern = 0
    for row in range(8):
        pattern |= dot3(vector, row) << row
    return pattern


def support_addresses(
    labels: Sequence[int], support: Sequence[int]
) -> tuple[int, ...]:
    u, v, w = support
    return tuple(
        (dot3(labels[u], row) << 2)
        | (dot3(labels[v], row) << 1)
        | dot3(labels[w], row)
        for row in range(8)
    )


def basis_coloring_valid(
    labels: Sequence[int], supports: Sequence[Sequence[int]]
) -> bool:
    return all(
        basis_triple(*(labels[vertex] for vertex in support))
        for support in supports
    )


def eight_row_addressing_valid(
    labels: Sequence[int], supports: Sequence[Sequence[int]]
) -> bool:
    return all(
        len(set(support_addresses(labels, support))) == 8
        for support in supports
    )


def four_color_oa_rows() -> tuple[int, int, int, int]:
    """Rows of OA(8,4,2,3), using the even-parity [4,3,2] code."""
    columns = tuple(
        word for word in range(16) if word.bit_count() % 2 == 0
    )
    return tuple(
        sum(
            ((column >> coordinate) & 1) << index
            for index, column in enumerate(columns)
        )
        for coordinate in range(4)
    )


def every_three_rows_injective(
    rows: Sequence[int], column_count: int = 8
) -> bool:
    for chosen in itertools.combinations(range(len(rows)), 3):
        addresses = {
            tuple((rows[row] >> column) & 1 for row in chosen)
            for column in range(column_count)
        }
        if len(addresses) != column_count:
            return False
    return True


def code_is_uniformly_three_separating(
    codewords: Sequence[int], length: int
) -> bool:
    """Any three codeword coordinates distinguish all columns."""
    if len(set(codewords)) != len(codewords):
        return False
    required_distance = length - 2
    return all(
        (left ^ right).bit_count() >= required_distance
        for left, right in itertools.combinations(codewords, 2)
    )


def maximum_uniform_code(length: int) -> tuple[int, tuple[int, ...]]:
    """Exact A_2(length,length-2) for the finite audit range 3..10."""
    if length < 3:
        raise ValueError("length must be at least three")
    words = tuple(range(1 << length))
    threshold = length - 2
    adjacency = {
        word: {
            other
            for other in words
            if other != word
            and (word ^ other).bit_count() >= threshold
        }
        for word in words
    }
    best: tuple[int, ...] = ()

    def expand(clique: tuple[int, ...], candidates: set[int]) -> None:
        nonlocal best
        if len(clique) + len(candidates) <= len(best):
            return
        if not candidates:
            if len(clique) > len(best):
                best = clique
            return
        while candidates:
            if len(clique) + len(candidates) <= len(best):
                return
            vertex = min(candidates)
            candidates.remove(vertex)
            expand(clique + (vertex,), candidates & adjacency[vertex])
        if len(clique) > len(best):
            best = clique

    # Complement symmetry lets us insist that zero is present.
    expand((0,), set(adjacency[0]))
    return len(best), tuple(sorted(best))


def primal_adjacency(
    variable_count: int, supports: Sequence[Sequence[int]]
) -> tuple[frozenset[int], ...]:
    adjacency = [set() for _ in range(variable_count)]
    for support in supports:
        for left, right in itertools.combinations(support, 2):
            adjacency[left].add(right)
            adjacency[right].add(left)
    return tuple(frozenset(row) for row in adjacency)


def maximum_clique(
    adjacency: Sequence[frozenset[int]],
) -> tuple[int, ...]:
    best: tuple[int, ...] = ()

    def bron_kerbosch(
        clique: tuple[int, ...], candidates: set[int], excluded: set[int]
    ) -> None:
        nonlocal best
        if len(clique) + len(candidates) <= len(best):
            return
        if not candidates and not excluded:
            if len(clique) > len(best):
                best = clique
            return
        union = candidates | excluded
        pivot = (
            max(
                union,
                key=lambda vertex: len(
                    candidates & set(adjacency[vertex])
                ),
            )
            if union
            else None
        )
        extension = candidates - (
            set(adjacency[pivot]) if pivot is not None else set()
        )
        for vertex in tuple(extension):
            bron_kerbosch(
                clique + (vertex,),
                candidates & set(adjacency[vertex]),
                excluded & set(adjacency[vertex]),
            )
            candidates.remove(vertex)
            excluded.add(vertex)

    bron_kerbosch((), set(range(len(adjacency))), set())
    return best


def k_colorable(
    adjacency: Sequence[frozenset[int]], color_count: int
) -> tuple[bool, tuple[int, ...] | None]:
    colors = [-1] * len(adjacency)

    def search(colored: int) -> bool:
        if colored == len(colors):
            return True
        uncolored = [
            vertex for vertex, color in enumerate(colors) if color < 0
        ]
        vertex = max(
            uncolored,
            key=lambda item: (
                len(
                    {
                        colors[neighbor]
                        for neighbor in adjacency[item]
                        if colors[neighbor] >= 0
                    }
                ),
                len(adjacency[item]),
            ),
        )
        forbidden = {
            colors[neighbor]
            for neighbor in adjacency[vertex]
            if colors[neighbor] >= 0
        }
        used_max = max(colors)
        for color in range(min(color_count, used_max + 2)):
            if color in forbidden:
                continue
            colors[vertex] = color
            if search(colored + 1):
                return True
            colors[vertex] = -1
        return False

    valid = search(0)
    return valid, tuple(colors) if valid else None


def exact_chromatic_number(
    variable_count: int, supports: Sequence[Sequence[int]]
) -> tuple[int, tuple[int, ...], tuple[int, ...]]:
    adjacency = primal_adjacency(variable_count, supports)
    clique = maximum_clique(adjacency)
    for colors in range(max(3, len(clique)), variable_count + 1):
        valid, witness = k_colorable(adjacency, colors)
        if valid and witness is not None:
            return colors, witness, clique
    raise AssertionError("finite graph must be colorable")


def find_basis_coloring(
    variable_count: int, supports: Sequence[Sequence[int]]
) -> tuple[int, ...] | None:
    """Deterministic exact CSP search over seven nonzero vectors of F_2^3."""
    normalized = tuple(
        tuple(int(vertex) for vertex in support) for support in supports
    )
    incident = [[] for _ in range(variable_count)]
    for support_index, support in enumerate(normalized):
        for vertex in support:
            incident[vertex].append(support_index)

    assignment: list[int | None] = [None] * variable_count
    domains = [set(range(1, 8)) for _ in range(variable_count)]
    first = normalized[0]
    for vertex, vector in zip(first, (1, 2, 4)):
        assignment[vertex] = vector
        domains[vertex] = {vector}

    def propagate(
        current_domains: list[set[int]],
        current_assignment: list[int | None],
    ) -> bool:
        changed = True
        while changed:
            changed = False
            for support in normalized:
                values = [current_assignment[vertex] for vertex in support]
                unknown = [
                    position
                    for position, value in enumerate(values)
                    if value is None
                ]
                if not unknown:
                    if not basis_triple(values[0], values[1], values[2]):
                        return False
                    continue
                if len(unknown) == 1:
                    position = unknown[0]
                    others = [
                        values[index]
                        for index in range(3)
                        if index != position
                    ]
                    allowed = {
                        vector
                        for vector in range(1, 8)
                        if basis_triple(
                            int(others[0]), int(others[1]), vector
                        )
                    }
                    vertex = support[position]
                    reduced = current_domains[vertex] & allowed
                    if not reduced:
                        return False
                    if reduced != current_domains[vertex]:
                        current_domains[vertex] = reduced
                        changed = True
                        if len(reduced) == 1:
                            current_assignment[vertex] = next(iter(reduced))
                elif len(unknown) == 2:
                    known = int(
                        next(
                            values[index]
                            for index in range(3)
                            if index not in unknown
                        )
                    )
                    left_vertex = support[unknown[0]]
                    right_vertex = support[unknown[1]]
                    left_domain = current_domains[left_vertex]
                    right_domain = current_domains[right_vertex]
                    reduced_left = {
                        left
                        for left in left_domain
                        if any(
                            basis_triple(known, left, right)
                            for right in right_domain
                        )
                    }
                    reduced_right = {
                        right
                        for right in right_domain
                        if any(
                            basis_triple(known, left, right)
                            for left in reduced_left
                        )
                    }
                    if not reduced_left or not reduced_right:
                        return False
                    if reduced_left != left_domain:
                        current_domains[left_vertex] = reduced_left
                        changed = True
                        if len(reduced_left) == 1:
                            current_assignment[left_vertex] = next(
                                iter(reduced_left)
                            )
                    if reduced_right != right_domain:
                        current_domains[right_vertex] = reduced_right
                        changed = True
                        if len(reduced_right) == 1:
                            current_assignment[right_vertex] = next(
                                iter(reduced_right)
                            )
        return True

    def search(
        current_domains: list[set[int]],
        current_assignment: list[int | None],
    ) -> tuple[int, ...] | None:
        if not propagate(current_domains, current_assignment):
            return None
        if all(value is not None for value in current_assignment):
            result = tuple(int(value) for value in current_assignment)
            return (
                result
                if basis_coloring_valid(result, normalized)
                else None
            )
        vertex = min(
            (
                index
                for index, value in enumerate(current_assignment)
                if value is None
            ),
            key=lambda index: (
                len(current_domains[index]),
                -len(incident[index]),
                index,
            ),
        )
        for vector in sorted(current_domains[vertex]):
            next_assignment = current_assignment.copy()
            next_domains = [domain.copy() for domain in current_domains]
            next_assignment[vertex] = vector
            next_domains[vertex] = {vector}
            result = search(next_domains, next_assignment)
            if result is not None:
                return result
        return None

    return search(domains, assignment)


def family_audit(
    name: str, variable_count: int, supports: Sequence[Support]
) -> dict:
    chromatic, coloring, clique = exact_chromatic_number(
        variable_count, supports
    )
    basis = find_basis_coloring(variable_count, supports)
    assert basis is not None
    assert basis_coloring_valid(basis, supports)
    assert eight_row_addressing_valid(basis, supports)
    adjacency = primal_adjacency(variable_count, supports)
    return {
        "name": name,
        "variables": variable_count,
        "supports": len(supports),
        "primal_edges": sum(len(row) for row in adjacency) // 2,
        "primal_clique_number": len(clique),
        "one_maximum_clique": list(clique),
        "primal_chromatic_number": chromatic,
        "one_primal_coloring": list(coloring),
        "four_colorable": chromatic <= 4,
        "basis_coloring_found": True,
        "one_basis_coloring": list(basis),
        "eight_row_addresses_injective": True,
    }


def build_results() -> dict:
    oa_rows = four_color_oa_rows()
    assert every_three_rows_injective(oa_rows)

    code_table = []
    for length in range(3, 11):
        maximum, witness = maximum_uniform_code(length)
        assert code_is_uniformly_three_separating(witness, length)
        code_table.append(
            {
                "colors": length,
                "maximum_target_rows": maximum,
                "one_code": [
                    format(word, f"0{length}b") for word in witness
                ],
            }
        )

    controls = [
        family_audit(
            name,
            max(max(support) for support in supports) + 1,
            supports,
        )
        for name, supports in V80_SUPPORTS.items()
    ]
    samples = [
        family_audit(
            f"v87_seed_{seed}",
            n,
            sample_supports(n, m, seed),
        )
        for n, m, seed in V87_RANDOM_SAMPLES
    ]

    return {
        "laboratory": "V89",
        "scope": (
            "target-independent eight-row addressing and the affine "
            "basis-coloring boundary"
        ),
        "theorems": {
            "basis_addressing": (
                "If vertices receive nonzero vectors of F_2^3 and every "
                "ternary support receives a basis, then the eight affine "
                "witness rows indexed by F_2^3 give distinct local addresses "
                "on every support; consequently every target matrix with at "
                "most eight rows is coverable."
            ),
            "four_color_corollary": (
                "A proper four-coloring of the primal graph implies the basis "
                "condition through the four-point cap {001,010,100,111}, "
                "hence covers every target matrix with at most eight rows."
            ),
            "uniform_ceiling": (
                "Eight is the exact ceiling for one target-independent "
                "witness family on ternary supports, because a support has "
                "only eight local addresses."
            ),
            "code_equivalence": (
                "A j-color uniform pattern table separates k target rows on "
                "every rainbow support iff its j binary codewords have "
                "minimum distance at least j-2."
            ),
        },
        "oa_8_4_2_3": {
            "rows": [format(row, "08b") for row in oa_rows],
            "every_three_rows_injective": True,
            "columns": 8,
        },
        "uniform_color_code_table": code_table,
        "finite_audit": {
            "v80_controls": controls,
            "v87_samples": samples,
            "families_checked": len(controls) + len(samples),
            "all_basis_colorable": all(
                row["basis_coloring_found"] for row in controls + samples
            ),
            "all_eight_row_injective": all(
                row["eight_row_addresses_injective"]
                for row in controls + samples
            ),
            "all_primal_four_colorable": all(
                row["four_colorable"] for row in controls + samples
            ),
            "primal_chromatic_numbers": [
                row["primal_chromatic_number"]
                for row in controls + samples
            ],
        },
        "scientific_status": {
            "eval_h_eight_row_basis_addressing_theorem": True,
            "primal_four_color_sufficient_for_eight_rows": True,
            "target_independent_ternary_addressing_ceiling_eight": True,
            "v80_controls_primal_four_colorable": False,
            "v87_samples_primal_four_colorable": False,
            "v80_and_v87_samples_basis_colorable": True,
            "v87_random_model_basis_colorable_whp": False,
            "support_only_universal_list_lower_bound_nine": False,
            "constructive_eval_h_list": False,
            "p_vs_np_resolved": False,
            "novelty_confirmed": False,
            "peer_reviewed": False,
        },
    }


if __name__ == "__main__":
    import json

    print(json.dumps(build_results(), indent=2, sort_keys=True))
