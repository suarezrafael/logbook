#!/usr/bin/env python3
"""Independent four-cut certificates for labelled two-boundary clusters."""
from __future__ import annotations

from itertools import combinations
from typing import Iterable, Sequence

from decomposition_pareto import Support, Tree, normalize_supports


def unrooted_branch_tree(
    tree: Tree,
) -> tuple[dict[object, set[object]], dict[object, int]]:
    """Suppress the rooted degree-two node and label the gate leaves."""
    adjacency: dict[object, set[object]] = {}
    labels: dict[object, int] = {}
    next_internal = 0

    def add_edge(left: object, right: object) -> None:
        adjacency.setdefault(left, set()).add(right)
        adjacency.setdefault(right, set()).add(left)

    def build(node: Tree) -> object:
        nonlocal next_internal
        if isinstance(node, int):
            key = "leaf", int(node)
            adjacency.setdefault(key, set())
            if key in labels:
                raise ValueError("tree leaves must be unique")
            labels[key] = int(node)
            return key
        key = "internal", next_internal
        next_internal += 1
        adjacency.setdefault(key, set())
        add_edge(key, build(node[0]))
        add_edge(key, build(node[1]))
        return key

    root = build(tree)
    if isinstance(tree, int):
        return adjacency, labels
    neighbors = tuple(adjacency[root])
    if len(neighbors) != 2:
        raise AssertionError("a rooted binary root must have degree two")
    left, right = neighbors
    adjacency[left].remove(root)
    adjacency[right].remove(root)
    del adjacency[root]
    add_edge(left, right)
    if any(len(neighbors) > 3 for neighbors in adjacency.values()):
        raise AssertionError("the suppressed branch tree must be subcubic")
    return adjacency, labels


def connected_vertex_subsets(
    adjacency: dict[object, set[object]],
) -> tuple[frozenset[object], ...]:
    nodes = tuple(sorted(adjacency, key=repr))
    answer: list[frozenset[object]] = []
    for mask in range(1, 1 << len(nodes)):
        chosen = frozenset(
            nodes[index] for index in range(len(nodes)) if mask >> index & 1
        )
        start = next(iter(chosen))
        seen = {start}
        stack = [start]
        while stack:
            node = stack.pop()
            for neighbor in adjacency[node]:
                if neighbor in chosen and neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        if seen == set(chosen):
            answer.append(chosen)
    return tuple(answer)


def edge_component_labels(
    adjacency: dict[object, set[object]],
    labels: dict[object, int],
    start: object,
    blocked: object,
) -> frozenset[int]:
    seen = {blocked}
    stack = [start]
    answer: set[int] = set()
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        if node in labels:
            answer.add(labels[node])
        stack.extend(adjacency[node] - seen)
    return frozenset(answer)


def middle_variables(
    supports: Sequence[Support], gate_subset: Iterable[int]
) -> frozenset[int]:
    selected = frozenset(int(index) for index in gate_subset)
    left = {
        variable
        for index, support in enumerate(supports)
        if index in selected
        for variable in support
    }
    right = {
        variable
        for index, support in enumerate(supports)
        if index not in selected
        for variable in support
    }
    return frozenset(left & right)


def labelled_cluster_cover(
    supports: Sequence[Support],
    adjacency: dict[object, set[object]],
    labels: dict[object, int],
    vertices: frozenset[object],
    included_labels: frozenset[int],
) -> dict[str, object]:
    """Audit the four-cut cover for one connected labelled top-tree cluster.

    Labels are attached only to the original gate leaves. A label at a vertex
    inside the connected subtree may be omitted, in which case that vertex is
    a label boundary exactly as in the labelled-top-tree definition.
    """
    if not vertices:
        raise ValueError("a cluster needs at least one tree vertex")
    if any(label not in set(labels.values()) for label in included_labels):
        raise ValueError("unknown gate label")
    available = frozenset(labels[node] for node in vertices if node in labels)
    if not included_labels <= available:
        raise ValueError("included labels must be attached inside the cluster")

    edge_boundary_vertices = {
        node
        for node in vertices
        if any(neighbor not in vertices for neighbor in adjacency[node])
    }
    omitted_label_vertices = {
        node
        for node in vertices
        if node in labels and labels[node] not in included_labels
    }
    boundary_vertices = frozenset(edge_boundary_vertices | omitted_label_vertices)

    cover_edges: set[tuple[object, object]] = set()
    for node in vertices:
        for neighbor in adjacency[node]:
            if neighbor not in vertices:
                cover_edges.add((node, neighbor))
    for node in omitted_label_vertices:
        if len(adjacency[node]) != 1:
            raise AssertionError("gate labels must be attached to branch-tree leaves")
        neighbor = next(iter(adjacency[node]))
        edge = (
            (node, neighbor)
            if repr(node) <= repr(neighbor)
            else (neighbor, node)
        )
        cover_edges.add(edge)

    covered_variables: set[int] = set()
    cover_middle_sets: list[tuple[int, ...]] = []
    for left, right in sorted(
        cover_edges, key=lambda edge: (repr(edge[0]), repr(edge[1]))
    ):
        side = edge_component_labels(adjacency, labels, left, right)
        middle = middle_variables(supports, side)
        covered_variables.update(middle)
        cover_middle_sets.append(tuple(sorted(middle)))

    cluster_middle = middle_variables(supports, included_labels)
    return {
        "gate_labels": tuple(sorted(included_labels)),
        "boundary_vertices": tuple(sorted(boundary_vertices, key=repr)),
        "boundary_vertex_count": len(boundary_vertices),
        "cover_edges": tuple(
            (repr(left), repr(right))
            for left, right in sorted(
                cover_edges, key=lambda edge: (repr(edge[0]), repr(edge[1]))
            )
        ),
        "cover_edge_count": len(cover_edges),
        "cluster_middle": tuple(sorted(cluster_middle)),
        "cover_middle_sets": tuple(cover_middle_sets),
        "covered": cluster_middle <= covered_variables,
    }


def audit_all_two_boundary_clusters(
    supports: Sequence[Support], tree: Tree
) -> dict[str, int]:
    """Exhaust all connected labelled clusters with at most two boundaries."""
    supports = normalize_supports(supports)
    adjacency, labels = unrooted_branch_tree(tree)
    clusters = 0
    labelled_states = 0
    maximum_cover_edges = 0
    for vertices in connected_vertex_subsets(adjacency):
        available = tuple(labels[node] for node in vertices if node in labels)
        omission_choices = [tuple()]
        omission_choices.extend((label,) for label in available)
        omission_choices.extend(combinations(available, 2))
        cluster_counted = False
        for omitted in omission_choices:
            included = frozenset(set(available) - set(omitted))
            if not included:
                continue
            record = labelled_cluster_cover(
                supports, adjacency, labels, vertices, included
            )
            if int(record["boundary_vertex_count"]) > 2:
                continue
            if int(record["cover_edge_count"]) > 4:
                raise AssertionError(record)
            if not bool(record["covered"]):
                raise AssertionError(record)
            maximum_cover_edges = max(
                maximum_cover_edges, int(record["cover_edge_count"])
            )
            labelled_states += 1
            cluster_counted = True
        if cluster_counted:
            clusters += 1
    return {
        "connected_vertex_clusters": clusters,
        "labelled_cluster_states": labelled_states,
        "maximum_cover_edges": maximum_cover_edges,
    }
