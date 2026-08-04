#!/usr/bin/env python3
"""V89/V90: exact obstructions to a naive 3-core peeling bridge.

The seven nonzero vectors of F_2^3 are encoded by integers 1..7. A support
triple is valid exactly when its labels are a basis, equivalently when they are
pairwise distinct and have nonzero XOR.
"""
from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, deque
from typing import Iterator, Sequence

Edge = tuple[int, int, int]

SMALL_OBSTRUCTION: tuple[Edge, ...] = (
    (0, 1, 3),
    (0, 1, 4),
    (1, 2, 6),
    (1, 5, 7),
    (2, 3, 4),
    (2, 5, 7),
    (3, 4, 6),
    (3, 5, 7),
    (4, 5, 7),
    (5, 6, 7),
)

LINEAR_OBSTRUCTION: tuple[Edge, ...] = (
    (0, 8, 11),
    (1, 4, 7),
    (1, 5, 9),
    (2, 4, 9),
    (2, 6, 11),
    (3, 4, 10),
    (3, 9, 11),
    (4, 5, 11),
    (4, 6, 8),
    (5, 6, 7),
    (5, 8, 10),
    (6, 9, 10),
    (7, 8, 9),
    (7, 10, 11),
)


def is_basis(a: int, b: int, c: int) -> bool:
    return len({a, b, c}) == 3 and (a ^ b ^ c) != 0


def maximum_codegree(edges: Sequence[Edge]) -> int:
    counts: Counter[tuple[int, int]] = Counter()
    for edge in edges:
        counts.update(
            tuple(sorted(pair)) for pair in itertools.combinations(edge, 2)
        )
    return max(counts.values(), default=0)


def peel_certificate(n: int, edges: Sequence[Edge]) -> list[dict]:
    incidence = [set() for _ in range(n)]
    for index, edge in enumerate(edges):
        for vertex in edge:
            incidence[vertex].add(index)
    active_edges = set(range(len(edges)))
    active_vertices = set(range(n))
    certificate: list[dict] = []
    while active_vertices:
        degrees = {
            vertex: len(incidence[vertex] & active_edges)
            for vertex in active_vertices
        }
        candidates = [
            vertex for vertex, degree in degrees.items() if degree <= 2
        ]
        if not candidates:
            return []
        vertex = min(candidates, key=lambda item: (degrees[item], item))
        removed = sorted(incidence[vertex] & active_edges)
        certificate.append(
            {
                "vertex": vertex,
                "active_degree": degrees[vertex],
                "removed_edges": [list(edges[index]) for index in removed],
            }
        )
        active_vertices.remove(vertex)
        active_edges.difference_update(removed)
    return certificate


def basis_colorable(n: int, edges: Sequence[Edge]) -> bool:
    """Deterministic exact CSP solver with GL(3,2) symmetry normalization."""
    edges = tuple(tuple(edge) for edge in edges)
    incidence = [[] for _ in range(n)]
    for edge in edges:
        for vertex in edge:
            incidence[vertex].append(edge)

    assignment = [0] * n
    domains = [set(range(1, 8)) for _ in range(n)]
    trail: list[tuple] = []

    def restore(mark: int) -> None:
        while len(trail) > mark:
            item = trail.pop()
            if item[0] == "assignment":
                assignment[item[1]] = 0
            else:
                domains[item[1]] = item[2]

    def restrict(vertex: int, allowed: set[int]) -> bool:
        reduced = domains[vertex] & allowed
        if not reduced:
            return False
        if reduced == domains[vertex]:
            return True
        trail.append(("domain", vertex, domains[vertex].copy()))
        domains[vertex] = reduced
        if len(reduced) == 1 and assignment[vertex] == 0:
            value = next(iter(reduced))
            assignment[vertex] = value
            trail.append(("assignment", vertex))
            return propagate(vertex)
        return True

    def propagate(changed: int) -> bool:
        pending = deque(incidence[changed])
        while pending:
            edge = pending.popleft()
            unassigned = [
                vertex for vertex in edge if assignment[vertex] == 0
            ]
            if not unassigned:
                if not is_basis(*(assignment[vertex] for vertex in edge)):
                    return False
                continue
            if len(unassigned) == 1:
                vertex = unassigned[0]
                fixed = [
                    assignment[item]
                    for item in edge
                    if assignment[item] != 0
                ]
                allowed = {
                    value
                    for value in domains[vertex]
                    if is_basis(fixed[0], fixed[1], value)
                }
                previous = domains[vertex].copy()
                if not restrict(vertex, allowed):
                    return False
                if domains[vertex] != previous:
                    pending.extend(
                        other for other in incidence[vertex] if other != edge
                    )
            elif len(unassigned) == 2:
                fixed = next(
                    assignment[item]
                    for item in edge
                    if assignment[item] != 0
                )
                left, right = unassigned
                left_allowed = {
                    a
                    for a in domains[left]
                    if any(
                        is_basis(fixed, a, b) for b in domains[right]
                    )
                }
                right_allowed = {
                    b
                    for b in domains[right]
                    if any(
                        is_basis(fixed, a, b) for a in domains[left]
                    )
                }
                if not restrict(left, left_allowed) or not restrict(
                    right, right_allowed
                ):
                    return False
        return True

    def assign(vertex: int, value: int) -> bool:
        if assignment[vertex]:
            return assignment[vertex] == value
        if value not in domains[vertex]:
            return False
        trail.append(("domain", vertex, domains[vertex].copy()))
        domains[vertex] = {value}
        assignment[vertex] = value
        trail.append(("assignment", vertex))
        return propagate(vertex)

    def search() -> bool:
        remaining = [
            vertex for vertex in range(n) if assignment[vertex] == 0
        ]
        if not remaining:
            return True
        vertex = min(
            remaining,
            key=lambda item: (
                len(domains[item]),
                -len(incidence[item]),
                item,
            ),
        )
        for value in sorted(domains[vertex]):
            mark = len(trail)
            if assign(vertex, value) and search():
                return True
            restore(mark)
        return False

    if not edges:
        return True
    first = edges[0]
    mark = len(trail)
    if not (
        assign(first[0], 1)
        and assign(first[1], 2)
        and assign(first[2], 4)
    ):
        restore(mark)
        return False
    return search()


def normalized_assignment_census(
    n: int, edges: Sequence[Edge]
) -> dict:
    first = edges[0]
    fixed = {first[0]: 1, first[1]: 2, first[2]: 4}
    free = [vertex for vertex in range(n) if vertex not in fixed]
    checked = 0
    satisfying = 0
    for values in itertools.product(range(1, 8), repeat=len(free)):
        labels = [0] * n
        for vertex, value in fixed.items():
            labels[vertex] = value
        for vertex, value in zip(free, values):
            labels[vertex] = value
        checked += 1
        if all(
            is_basis(*(labels[vertex] for vertex in edge))
            for edge in edges
        ):
            satisfying += 1
    return {
        "normalization": {
            "edge": list(first),
            "labels": [1, 2, 4],
            "justification": "GL(3,2) acts transitively on ordered bases",
        },
        "assignments_checked": checked,
        "satisfying_assignments": satisfying,
    }


def maximal_ordered_two_degenerate_hypergraphs(
    n: int,
) -> Iterator[tuple[Edge, ...]]:
    choices = []
    for owner in range(n - 2):
        pairs = tuple(itertools.combinations(range(owner + 1, n), 2))
        load = min(2, len(pairs))
        choices.append(tuple(itertools.combinations(pairs, load)))
    for selected in itertools.product(*choices):
        yield tuple(
            (owner, pair[0], pair[1])
            for owner, owner_pairs in enumerate(selected)
            for pair in owner_pairs
        )


def seven_vertex_census() -> dict:
    # Every maximal ordered instance contains the final edge (4,5,6).
    # Normalize it to labels (1,2,4), enumerate only 7^4 assignments for
    # vertices 0..3, and represent each edge's satisfying assignments by one
    # 2401-bit Python integer. Each hypergraph is then checked by nine fast
    # bitwise intersections.
    assignments = []
    for prefix in itertools.product(range(1, 8), repeat=4):
        assignments.append(prefix + (1, 2, 4))

    edge_masks: dict[Edge, int] = {}
    for edge in itertools.combinations(range(7), 3):
        mask = 0
        for index, labels in enumerate(assignments):
            if is_basis(*(labels[vertex] for vertex in edge)):
                mask |= 1 << index
        edge_masks[edge] = mask

    checked = 0
    failures = 0
    all_assignments = (1 << len(assignments)) - 1
    for edges in maximal_ordered_two_degenerate_hypergraphs(7):
        checked += 1
        feasible = all_assignments
        for edge in edges:
            feasible &= edge_masks[edge]
            if feasible == 0:
                failures += 1
                break
        if failures:
            break
    return {
        "normalized_assignments": len(assignments),
        "maximal_ordered_hypergraphs_checked": checked,
        "expected_count": 212625,
        "noncolorable_found": failures,
        "all_colorable": failures == 0 and checked == 212625,
        "coverage_argument": (
            "Every empty-3-core hypergraph has a peeling order. Relabel that "
            "order increasingly and extend each owner to load two whenever "
            "possible. Basis colorability is inherited by subhypergraphs."
        ),
    }


def edge_critical(n: int, edges: Sequence[Edge]) -> bool:
    return all(
        basis_colorable(n, edges[:index] + edges[index + 1 :])
        for index in range(len(edges))
    )


def build_results() -> dict:
    small_peel = peel_certificate(8, SMALL_OBSTRUCTION)
    linear_peel = peel_certificate(12, LINEAR_OBSTRUCTION)
    small_census = normalized_assignment_census(8, SMALL_OBSTRUCTION)
    result = {
        "laboratory": "V89/V90",
        "module": "basis-coloring core-peeling obstruction",
        "small_obstruction": {
            "vertices": 8,
            "edges": [list(edge) for edge in SMALL_OBSTRUCTION],
            "edge_count": len(SMALL_OBSTRUCTION),
            "empty_three_core": len(small_peel) == 8,
            "peel_certificate": small_peel,
            "basis_colorable": basis_colorable(8, SMALL_OBSTRUCTION),
            "normalized_assignment_census": small_census,
            "edge_critical": edge_critical(8, SMALL_OBSTRUCTION),
            "analytic_certificate": {
                "common_pair": [5, 7],
                "common_neighbors": [1, 2, 3, 4, 6],
                "four_point_coset": True,
                "forced_relation": "label(1) is label(3) or label(4)",
                "contradicting_edges": [[0, 1, 3], [0, 1, 4]],
            },
        },
        "linear_obstruction": {
            "vertices": 12,
            "edges": [list(edge) for edge in LINEAR_OBSTRUCTION],
            "edge_count": len(LINEAR_OBSTRUCTION),
            "maximum_pair_codegree": maximum_codegree(LINEAR_OBSTRUCTION),
            "empty_three_core": len(linear_peel) == 12,
            "peel_certificate": linear_peel,
            "basis_colorable": basis_colorable(12, LINEAR_OBSTRUCTION),
            "edge_critical": edge_critical(12, LINEAR_OBSTRUCTION),
        },
        "seven_vertex_minimality": {
            "exact_census_registered_for_full_replay": True,
            "maximal_ordered_hypergraphs": 212625,
            "all_colorable": True,
            "conclusion": (
                "The eight-vertex obstruction is vertex-minimal among "
                "empty-3-core 3-uniform hypergraphs."
            ),
        },
        "scientific_status": {
            "empty_three_core_implies_basis_colorable": False,
            "linear_empty_three_core_implies_basis_colorable": False,
            "core_threshold_alone_closes_eight_row_bridge": False,
            "random_model_basis_colorable_whp": False,
            "support_only_universal_list_lower_bound_nine": False,
        },
        "interpretation": (
            "The 3-core threshold may still be useful probabilistically, but "
            "it cannot be converted into basis colorability by a universal "
            "reverse-peeling extension theorem, even for linear supports."
        ),
        "nonclaims": [
            "The obstructions do not show that the V87 random model is not basis-colorable with high probability.",
            "The fixed obstructions occur with vanishing probability in the sparse random model.",
            "No nine-row constructor lower bound follows.",
            "P versus NP remains unresolved.",
        ],
    }
    result["seven_vertex_minimality"][
        "replayed_census"
    ] = seven_vertex_census()
    return result


def main() -> None:
    argparse.ArgumentParser().parse_args()
    print(json.dumps(build_results(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
