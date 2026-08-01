#!/usr/bin/env python3
"""Independent V72 checks using masks and Boolean assignment semantics."""
from __future__ import annotations

import itertools
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "v70"))

from v70_frontier_ordering import compile_system
from v72_branch_residual import (
    balanced_branch_tree,
    boundary_variables,
    branch_residual_dp,
    branch_tree_subset,
    exact_linear_width_dp,
    padded_binary_tree_specs,
)


def independent_frontier(edges, mask):
    answer = set()
    for vertex in {v for edge in edges for v in edge}:
        processed = any((mask >> i) & 1 and vertex in edge for i, edge in enumerate(edges))
        unprocessed = any(not ((mask >> i) & 1) and vertex in edge for i, edge in enumerate(edges))
        if processed and unprocessed:
            answer.add(vertex)
    return answer


def independent_width(edges, order):
    mask = 0
    width = 0
    for edge in order:
        mask |= 1 << edge
        width = max(width, len(independent_frontier(edges, mask)))
    return width


def brute_width(edges):
    return min(
        independent_width(edges, order)
        for order in itertools.permutations(range(len(edges)))
    )


def exact_width_random_suite(seed=720073, samples=160):
    rng = random.Random(seed)
    checked = 0
    for _ in range(samples):
        n = rng.randint(3, 6)
        m = rng.randint(1, 7)
        supports = [
            tuple(sorted(rng.sample(range(n), rng.randint(1, min(3, n)))))
            for _ in range(m)
        ]
        exact = exact_linear_width_dp(supports)
        assert exact["width"] == brute_width(supports)
        assert independent_width(supports, exact["order"]) == exact["width"]
        checked += 1
    return checked


def padding_suite(seed=720074, samples=120):
    rng = random.Random(seed)
    cut_checks = 0
    for _ in range(samples):
        n = rng.randint(3, 7)
        possible = list(itertools.combinations(range(n), 2))
        chosen = rng.sample(possible, rng.randint(1, min(8, len(possible))))
        padded = [edge + (n + i,) for i, edge in enumerate(chosen)]
        for mask in range(1 << len(chosen)):
            graph_boundary = independent_frontier(chosen, mask)
            padded_boundary = independent_frontier(padded, mask)
            assert padded_boundary == graph_boundary
            cut_checks += 1
        assert exact_linear_width_dp(chosen)["width"] == exact_linear_width_dp(padded)["width"]
    return {"graphs": samples, "cut_checks": cut_checks}


def satisfies_equations(equations, assignment, n):
    coefficient_mask = (1 << n) - 1
    for equation in equations:
        left = (equation & coefficient_mask & assignment).bit_count() & 1
        right = (equation >> n) & 1
        if left != right:
            return False
    return True


def compact_pattern(assignment, boundary):
    value = 0
    for position, vertex in enumerate(sorted(boundary)):
        if (assignment >> vertex) & 1:
            value |= 1 << position
    return value


def basis_semantics(basis, n, boundary):
    patterns = set()
    boundary = sorted(boundary)
    for compact in range(1 << len(boundary)):
        assignment = 0
        for position, vertex in enumerate(boundary):
            if (compact >> position) & 1:
                assignment |= 1 << vertex
        if satisfies_equations(basis, assignment, n):
            patterns.add(compact)
    return frozenset(patterns)


def independent_direct_semantics(n, specs, subset, boundary):
    gates = compile_system(n, specs)
    subset = sorted(subset)
    residuals = set()
    for choices in itertools.product((0, 1), repeat=len(subset)):
        equations = []
        for gate, choice in zip(subset, choices):
            equations.extend(gates[gate]["cells"][choice])
        patterns = set()
        for assignment in range(1 << n):
            if satisfies_equations(equations, assignment, n):
                patterns.add(compact_pattern(assignment, boundary))
        if patterns:
            residuals.add(frozenset(patterns))
    return residuals


def walk_nodes(tree):
    yield tree
    if not isinstance(tree, int):
        yield from walk_nodes(tree[0])
        yield from walk_nodes(tree[1])


def semantic_branch_suite(seed=720075, systems=36):
    rng = random.Random(seed)
    checked_nodes = 0
    for _ in range(systems):
        n = rng.randint(4, 5)
        m = rng.randint(3, 6)
        specs = [
            {"support": rng.sample(range(n), 3), "partition": rng.randrange(3)}
            for _ in range(m)
        ]
        order = list(range(m))
        rng.shuffle(order)
        tree = balanced_branch_tree(order)
        for node in walk_nodes(tree):
            subset = branch_tree_subset(node)
            boundary = boundary_variables(specs, subset)
            primary = branch_residual_dp(n, specs, node, validate_direct=False)["root_states"]
            primary_semantics = {
                basis_semantics(basis, n, boundary) for basis in primary
            }
            direct_semantics = independent_direct_semantics(
                n, specs, subset, boundary
            )
            assert primary_semantics == direct_semantics
            checked_nodes += 1
    return {"systems": systems, "nodes": checked_nodes}


def main():
    exact = exact_width_random_suite()
    padding = padding_suite()
    semantic = semantic_branch_suite()

    for height, expected in ((1, 1), (2, 1), (3, 2)):
        _, specs = padded_binary_tree_specs(height)
        assert exact_linear_width_dp([item["support"] for item in specs])["width"] == expected

    results = json.loads((HERE / "RESULTS.json").read_text())
    assert results["scientific_status"]["rank3_width_decision_np_complete"] is True
    assert results["scientific_status"]["bounded_treewidth_forces_small_Gstar"] is False
    assert results["scientific_status"]["p_vs_np_resolved"] is False

    metadata = "\n".join(
        path.read_text().lower()
        for path in HERE.iterdir()
        if path.suffix in {".md", ".json", ".tex"}
    )
    for forbidden in (
        "p versus np is solved",
        "accepted by eccc",
        "peer reviewed theorem",
        "bounded treewidth implies small g*_proj",
    ):
        assert forbidden not in metadata

    print(
        "V72 independent verification passed: "
        f"{exact} random exact-width instances; "
        f"{padding['cut_checks']} padding cut identities; "
        f"{semantic['nodes']} semantic branch nodes; zero failures."
    )


if __name__ == "__main__":
    main()
