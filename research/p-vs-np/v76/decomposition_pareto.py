#!/usr/bin/env python3
"""Exact support-boundary width, height, and external-path Pareto analysis."""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations, permutations
from math import ceil, log2
from typing import Iterable, Sequence

Support = tuple[int, ...]
Tree = int | tuple["Tree", "Tree"]


def normalize_supports(supports: Iterable[Iterable[int]]) -> tuple[Support, ...]:
    answer: list[Support] = []
    for raw in supports:
        support = tuple(sorted(set(int(variable) for variable in raw)))
        if not 1 <= len(support) <= 3:
            raise ValueError("every gate support must have rank in 1..3")
        if support[0] < 0:
            raise ValueError("variables must be nonnegative")
        answer.append(support)
    if not answer:
        raise ValueError("at least one gate support is required")
    return tuple(answer)


def boundary_variables_mask(
    supports: Sequence[Support], mask: int
) -> tuple[int, ...]:
    left: set[int] = set()
    right: set[int] = set()
    for index, support in enumerate(supports):
        (left if (int(mask) >> index) & 1 else right).update(support)
    return tuple(sorted(left & right))


def boundary_profile(supports: Sequence[Support]) -> tuple[int, ...]:
    supports = normalize_supports(supports)
    return tuple(
        len(boundary_variables_mask(supports, mask))
        for mask in range(1 << len(supports))
    )


def tree_leaf_mask(tree: Tree) -> int:
    if isinstance(tree, int):
        return 1 << int(tree)
    return tree_leaf_mask(tree[0]) | tree_leaf_mask(tree[1])


def leaf_depths(tree: Tree) -> dict[int, int]:
    depths: dict[int, int] = {}

    def visit(node: Tree, depth: int) -> None:
        if isinstance(node, int):
            if node in depths:
                raise ValueError("tree leaves must be unique")
            depths[int(node)] = int(depth)
            return
        visit(node[0], depth + 1)
        visit(node[1], depth + 1)

    visit(tree, 0)
    return depths


def tree_metrics(supports: Sequence[Support], tree: Tree) -> dict[str, object]:
    supports = normalize_supports(supports)
    full_mask = (1 << len(supports)) - 1
    if tree_leaf_mask(tree) != full_mask:
        raise ValueError("tree leaves must be exactly the gate indices")
    node_masks: list[int] = []

    def visit(node: Tree) -> int:
        if isinstance(node, int):
            mask = 1 << int(node)
        else:
            mask = visit(node[0]) | visit(node[1])
        node_masks.append(mask)
        return mask

    visit(tree)
    depths = leaf_depths(tree)
    return {
        "width": max(
            len(boundary_variables_mask(supports, mask)) for mask in node_masks
        ),
        "height": max(depths.values(), default=0),
        "external_path_length": sum(depths.values()),
        "leaf_depths": depths,
        "node_masks": tuple(node_masks),
    }


def balanced_branch_tree(order: Iterable[int]) -> Tree:
    leaves = [int(index) for index in order]
    if not leaves:
        raise ValueError("a branch tree needs at least one leaf")
    if len(leaves) == 1:
        return leaves[0]
    middle = len(leaves) // 2
    return balanced_branch_tree(leaves[:middle]), balanced_branch_tree(leaves[middle:])


def caterpillar_branch_tree(order: Iterable[int]) -> Tree:
    leaves = [int(index) for index in order]
    if not leaves:
        raise ValueError("a branch tree needs at least one leaf")
    tree: Tree = leaves[0]
    for leaf in leaves[1:]:
        tree = (tree, leaf)
    return tree


def frontier_greedy_order(supports: Sequence[Support]) -> list[int]:
    supports = normalize_supports(supports)
    remaining = set(range(len(supports)))
    processed: set[int] = set()
    order: list[int] = []

    def boundary(chosen: set[int]) -> set[int]:
        mask = sum(1 << index for index in chosen)
        return set(boundary_variables_mask(supports, mask))

    while remaining:
        def key(gate: int) -> tuple[int, int, int, int, int]:
            after = remaining - {gate}
            frontier = boundary(processed | {gate})
            pressure = sum(
                sum(variable in supports[other] for other in after)
                for variable in frontier
            )
            closed = sum(
                1
                for variable in supports[gate]
                if all(variable not in supports[other] for other in after)
            )
            overlap = sum(
                len(set(supports[gate]) & set(supports[other]))
                for other in after
            )
            return len(frontier), pressure, -closed, -overlap, gate

        gate = min(remaining, key=key)
        order.append(gate)
        processed.add(gate)
        remaining.remove(gate)
    return order


def support_lookahead_order(
    supports: Sequence[Support], depth: int = 2
) -> list[int]:
    supports = normalize_supports(supports)
    remaining = set(range(len(supports)))
    processed: set[int] = set()
    order: list[int] = []
    boundaries = boundary_profile(supports)

    def size(chosen: set[int]) -> int:
        return boundaries[sum(1 << index for index in chosen)]

    while remaining:
        look = min(int(depth), len(remaining))
        best: tuple[tuple[object, ...], tuple[int, ...]] | None = None
        for sequence in permutations(sorted(remaining), look):
            trial = set(processed)
            profile: list[int] = []
            for gate in sequence:
                profile.append(size(trial))
                trial.add(gate)
            profile.append(size(trial))
            score: tuple[object, ...] = (
                max(profile),
                sum(2**value for value in profile),
                sequence,
            )
            if best is None or score < best[0]:
                best = score, sequence
        assert best is not None
        gate = best[1][0]
        order.append(gate)
        processed.add(gate)
        remaining.remove(gate)
    return order


@dataclass(frozen=True)
class ParetoState:
    width: int
    height: int
    external_path_length: int
    tree: Tree


def _tree_key(tree: Tree) -> tuple[object, ...]:
    if isinstance(tree, int):
        return 0, int(tree)
    return 1, _tree_key(tree[0]), _tree_key(tree[1])


def _prune(states: Iterable[ParetoState]) -> tuple[ParetoState, ...]:
    best_by_metrics: dict[tuple[int, int, int], ParetoState] = {}
    for state in states:
        metrics = state.width, state.height, state.external_path_length
        previous = best_by_metrics.get(metrics)
        if previous is None or _tree_key(state.tree) < _tree_key(previous.tree):
            best_by_metrics[metrics] = state
    items = sorted(
        best_by_metrics.values(),
        key=lambda state: (
            state.width,
            state.height,
            state.external_path_length,
            _tree_key(state.tree),
        ),
    )
    frontier: list[ParetoState] = []
    for state in items:
        dominated = any(
            other is not state
            and other.width <= state.width
            and other.height <= state.height
            and other.external_path_length <= state.external_path_length
            and (
                other.width < state.width
                or other.height < state.height
                or other.external_path_length < state.external_path_length
            )
            for other in items
        )
        if not dominated:
            frontier.append(state)
    return tuple(frontier)


def _prune_metric_triples(
    triples: Iterable[tuple[int, int, int]],
) -> tuple[tuple[int, int, int], ...]:
    """Return the nondominated metric triples without retaining witness trees."""
    items = sorted(set(tuple(map(int, triple)) for triple in triples))
    return tuple(
        triple
        for triple in items
        if not any(
            other != triple
            and other[0] <= triple[0]
            and other[1] <= triple[1]
            and other[2] <= triple[2]
            for other in items
        )
    )


def exact_pareto_metrics(
    supports: Sequence[Support],
) -> tuple[tuple[int, int, int], ...]:
    """Compute exact Pareto triples in O(3^m poly(m)) without witness trees."""
    supports = normalize_supports(supports)
    m = len(supports)
    boundaries = boundary_profile(supports)
    dynamic: list[tuple[tuple[int, int, int], ...]] = [
        tuple() for _ in range(1 << m)
    ]
    for index in range(m):
        mask = 1 << index
        dynamic[mask] = ((boundaries[mask], 0, 0),)

    for size in range(2, m + 1):
        for indices in combinations(range(m), size):
            mask = sum(1 << index for index in indices)
            anchor = mask & -mask
            candidates: set[tuple[int, int, int]] = set()
            subset = (mask - 1) & mask
            while subset:
                if subset & anchor and subset != mask:
                    complement = mask ^ subset
                    for left in dynamic[subset]:
                        for right in dynamic[complement]:
                            candidates.add(
                                (
                                    max(boundaries[mask], left[0], right[0]),
                                    1 + max(left[1], right[1]),
                                    left[2] + right[2] + size,
                                )
                            )
                subset = (subset - 1) & mask
            dynamic[mask] = _prune_metric_triples(candidates)
    return dynamic[-1]


def exact_pareto_frontier(supports: Sequence[Support]) -> dict[str, object]:
    """Compute the exact nondominated width/height/EPL frontier in O(3^m poly)."""
    supports = normalize_supports(supports)
    m = len(supports)
    boundaries = boundary_profile(supports)
    full_mask = (1 << m) - 1
    dynamic: list[tuple[ParetoState, ...]] = [tuple() for _ in range(1 << m)]
    for index in range(m):
        mask = 1 << index
        dynamic[mask] = (ParetoState(boundaries[mask], 0, 0, index),)

    for size in range(2, m + 1):
        for indices in combinations(range(m), size):
            mask = sum(1 << index for index in indices)
            anchor = mask & -mask
            candidates: list[ParetoState] = []
            subset = (mask - 1) & mask
            while subset:
                if subset & anchor and subset != mask:
                    complement = mask ^ subset
                    for left in dynamic[subset]:
                        for right in dynamic[complement]:
                            left_tree, right_tree = left.tree, right.tree
                            if _tree_key(right_tree) < _tree_key(left_tree):
                                left_tree, right_tree = right_tree, left_tree
                            candidates.append(
                                ParetoState(
                                    max(boundaries[mask], left.width, right.width),
                                    1 + max(left.height, right.height),
                                    left.external_path_length
                                    + right.external_path_length
                                    + size,
                                    (left_tree, right_tree),
                                )
                            )
                subset = (subset - 1) & mask
            dynamic[mask] = _prune(candidates)

    frontier = dynamic[full_mask]
    logarithmic_height = ceil(log2(m)) if m > 1 else 0
    minimum_width = min(state.width for state in frontier)
    width_states = [state for state in frontier if state.width == minimum_width]
    minimum_width_at_log_height = min(
        state.width for state in frontier if state.height <= logarithmic_height
    )
    return {
        "m": m,
        "log_height_cap": logarithmic_height,
        "minimum_width": minimum_width,
        "minimum_height": min(state.height for state in frontier),
        "minimum_epl": min(state.external_path_length for state in frontier),
        "minimum_width_at_log_height": minimum_width_at_log_height,
        "width_inflation_at_log_height": minimum_width_at_log_height - minimum_width,
        "minimum_height_at_minimum_width": min(
            state.height for state in width_states
        ),
        "minimum_epl_at_minimum_width": min(
            state.external_path_length for state in width_states
        ),
        "frontier": [
            {
                "width": state.width,
                "height": state.height,
                "external_path_length": state.external_path_length,
                "tree": state.tree,
            }
            for state in frontier
        ],
    }


@lru_cache(None)
def _all_rooted_binary_trees_cached(items: tuple[int, ...]) -> tuple[Tree, ...]:
    if len(items) == 1:
        return (items[0],)
    anchor = items[0]
    rest = items[1:]
    trees: list[Tree] = []
    for extra_count in range(len(rest)):
        for extra in combinations(rest, extra_count):
            left_items = (anchor,) + extra
            if len(left_items) == len(items):
                continue
            right_items = tuple(item for item in items if item not in left_items)
            for left in _all_rooted_binary_trees_cached(tuple(sorted(left_items))):
                for right in _all_rooted_binary_trees_cached(tuple(sorted(right_items))):
                    left_tree, right_tree = left, right
                    if _tree_key(right_tree) < _tree_key(left_tree):
                        left_tree, right_tree = right_tree, left_tree
                    trees.append((left_tree, right_tree))
    unique = {_tree_key(tree): tree for tree in trees}
    return tuple(unique[key] for key in sorted(unique))


def all_rooted_binary_trees(leaves: tuple[int, ...]) -> tuple[Tree, ...]:
    """Enumerate canonical unordered rooted full binary trees on labelled leaves."""
    items = tuple(sorted(int(leaf) for leaf in leaves))
    if not items:
        raise ValueError("at least one leaf is required")
    return _all_rooted_binary_trees_cached(items)


def brute_pareto_frontier(
    supports: Sequence[Support],
) -> tuple[tuple[int, int, int], ...]:
    supports = normalize_supports(supports)
    states: list[ParetoState] = []
    for tree in all_rooted_binary_trees(tuple(range(len(supports)))):
        metrics = tree_metrics(supports, tree)
        states.append(
            ParetoState(
                int(metrics["width"]),
                int(metrics["height"]),
                int(metrics["external_path_length"]),
                tree,
            )
        )
    return tuple(
        (state.width, state.height, state.external_path_length)
        for state in _prune(states)
    )
