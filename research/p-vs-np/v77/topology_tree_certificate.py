#!/usr/bin/env python3
"""Static topology-tree certificates for subcubic leaf-labelled trees.

The existence and logarithmic-height theorem are prior art (Frederickson;
Alstrup--Holm--de Lichtenberg--Thorup). This module provides a deterministic
static constructor and a strict certificate verifier used by Laboratory V77.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence

Adjacency = dict[int, set[int]]
Support = tuple[int, ...]
GateTree = int | tuple["GateTree", "GateTree"]


@dataclass(frozen=True)
class Cluster:
    cluster_id: int
    vertices: frozenset[int]
    children: tuple[int, ...]
    level: int
    boundary_edges: tuple[tuple[int, int], ...]


def adjacency_from_edges(edges: Iterable[tuple[int, int]]) -> Adjacency:
    adjacency: Adjacency = {}
    for raw_left, raw_right in edges:
        left, right = int(raw_left), int(raw_right)
        if left == right:
            raise ValueError("tree edges cannot be loops")
        adjacency.setdefault(left, set()).add(right)
        adjacency.setdefault(right, set()).add(left)
    validate_subcubic_tree(adjacency)
    return adjacency


def validate_subcubic_tree(adjacency: Mapping[int, set[int]]) -> None:
    if not adjacency:
        raise ValueError("a source tree is required")
    for vertex, neighbors in adjacency.items():
        if len(neighbors) > 3:
            raise ValueError("the source tree must be subcubic")
        for neighbor in neighbors:
            if vertex not in adjacency.get(neighbor, set()):
                raise ValueError("adjacency must be symmetric")
    edge_count = sum(len(neighbors) for neighbors in adjacency.values()) // 2
    if edge_count != len(adjacency) - 1:
        raise ValueError("the source graph must be a tree")
    start = next(iter(adjacency))
    seen: set[int] = set()
    stack = [start]
    while stack:
        vertex = stack.pop()
        if vertex in seen:
            continue
        seen.add(vertex)
        stack.extend(adjacency[vertex] - seen)
    if len(seen) != len(adjacency):
        raise ValueError("the source graph must be connected")


def boundary_edges(
    adjacency: Mapping[int, set[int]], vertices: Iterable[int]
) -> tuple[tuple[int, int], ...]:
    chosen = set(int(vertex) for vertex in vertices)
    return tuple(
        sorted(
            (vertex, neighbor)
            for vertex in chosen
            for neighbor in adjacency[vertex]
            if neighbor not in chosen
        )
    )


def _allowed_merge(quotient: Mapping[int, set[int]], left: int, right: int) -> bool:
    return len(quotient[left]) + len(quotient[right]) - 2 <= 2


def _maximum_allowed_matching(
    quotient: Mapping[int, set[int]],
) -> set[tuple[int, int]]:
    """Maximum matching in the forest of legal topology-tree merges."""
    root = min(quotient)
    parent: dict[int, int | None] = {root: None}
    order = [root]
    for vertex in order:
        for neighbor in sorted(quotient[vertex]):
            if neighbor != parent[vertex]:
                parent[neighbor] = vertex
                order.append(neighbor)

    free: dict[int, int] = {}
    blocked: dict[int, int] = {}
    choice: dict[int, int | None] = {}
    for vertex in reversed(order):
        children = [
            child
            for child in sorted(quotient[vertex])
            if parent.get(child) == vertex
        ]
        baseline = sum(free[child] for child in children)
        best_value = baseline
        best_child: int | None = None
        for child in children:
            if not _allowed_merge(quotient, vertex, child):
                continue
            value = baseline - free[child] + 1 + blocked[child]
            if value > best_value or (
                value == best_value
                and best_child is not None
                and child < best_child
            ):
                best_value = value
                best_child = child
        free[vertex] = best_value
        blocked[vertex] = baseline
        choice[vertex] = best_child

    matching: set[tuple[int, int]] = set()

    def reconstruct(vertex: int, matched_to_parent: bool) -> None:
        selected = None if matched_to_parent else choice[vertex]
        if selected is not None:
            matching.add(tuple(sorted((vertex, selected))))
        for child in sorted(quotient[vertex]):
            if parent.get(child) == vertex:
                reconstruct(child, child == selected)

    reconstruct(root, False)
    return matching


def build_topology_certificate(
    adjacency: Mapping[int, set[int]],
) -> dict[str, object]:
    """Build a deterministic restricted topology hierarchy.

    This constructor is an audit implementation. The asymptotic existence
    theorem used by V77 is the prior-art topology-tree theorem.
    """
    validate_subcubic_tree(adjacency)
    source = {int(vertex): set(map(int, neighbors)) for vertex, neighbors in adjacency.items()}
    clusters: dict[int, Cluster] = {}
    next_id = 0
    current: list[int] = []
    owner: dict[int, int] = {}
    for vertex in sorted(source):
        cluster = Cluster(
            cluster_id=next_id,
            vertices=frozenset((vertex,)),
            children=tuple(),
            level=0,
            boundary_edges=boundary_edges(source, (vertex,)),
        )
        clusters[next_id] = cluster
        current.append(next_id)
        owner[vertex] = next_id
        next_id += 1

    quotient: dict[int, set[int]] = {cluster_id: set() for cluster_id in current}
    for vertex, neighbors in source.items():
        for neighbor in neighbors:
            if vertex < neighbor:
                left, right = owner[vertex], owner[neighbor]
                quotient[left].add(right)
                quotient[right].add(left)

    rounds: list[dict[str, int]] = []
    level = 0
    while len(quotient) > 1:
        level += 1
        matching = _maximum_allowed_matching(quotient)
        if not matching:
            raise AssertionError("a nontrivial quotient tree must have a legal merge")
        mate: dict[int, int] = {}
        for left, right in matching:
            mate[left] = right
            mate[right] = left

        old_to_new: dict[int, int] = {}
        new_ids: list[int] = []
        consumed: set[int] = set()
        for cluster_id in sorted(quotient):
            if cluster_id in consumed:
                continue
            if cluster_id in mate:
                partner = mate[cluster_id]
                consumed.update((cluster_id, partner))
                children = tuple(sorted((cluster_id, partner)))
            else:
                consumed.add(cluster_id)
                children = (cluster_id,)
            vertices = frozenset(
                vertex
                for child in children
                for vertex in clusters[child].vertices
            )
            parent_cluster = Cluster(
                cluster_id=next_id,
                vertices=vertices,
                children=children,
                level=level,
                boundary_edges=boundary_edges(source, vertices),
            )
            clusters[next_id] = parent_cluster
            new_ids.append(next_id)
            for child in children:
                old_to_new[child] = next_id
            next_id += 1

        new_quotient: dict[int, set[int]] = {cluster_id: set() for cluster_id in new_ids}
        for left, neighbors in quotient.items():
            for right in neighbors:
                if left < right:
                    parent_left = old_to_new[left]
                    parent_right = old_to_new[right]
                    if parent_left != parent_right:
                        new_quotient[parent_left].add(parent_right)
                        new_quotient[parent_right].add(parent_left)

        for cluster_id in new_ids:
            cluster = clusters[cluster_id]
            external_degree = len(cluster.boundary_edges)
            if external_degree > 3:
                raise AssertionError("topology cluster exceeds external degree three")
            if external_degree == 3 and len(cluster.vertices) != 1:
                raise AssertionError("external-degree-three clusters must be singletons")
        rounds.append(
            {
                "level": level,
                "clusters_before": len(quotient),
                "merged_pairs": len(matching),
                "clusters_after": len(new_quotient),
            }
        )
        quotient = new_quotient

    root = next(iter(quotient))
    certificate = {
        "source_adjacency": {vertex: tuple(sorted(neighbors)) for vertex, neighbors in source.items()},
        "clusters": clusters,
        "root": root,
        "rounds": tuple(rounds),
        "height": level,
    }
    verify_topology_certificate(certificate)
    return certificate


def verify_topology_certificate(certificate: Mapping[str, object]) -> None:
    raw_adjacency = certificate["source_adjacency"]
    assert isinstance(raw_adjacency, Mapping)
    adjacency = {
        int(vertex): set(map(int, neighbors))
        for vertex, neighbors in raw_adjacency.items()
    }
    validate_subcubic_tree(adjacency)
    clusters = certificate["clusters"]
    assert isinstance(clusters, Mapping)
    root = int(certificate["root"])
    if root not in clusters:
        raise AssertionError("certificate root is missing")

    all_vertices = frozenset(adjacency)
    for raw_id, raw_cluster in clusters.items():
        cluster_id = int(raw_id)
        if not isinstance(raw_cluster, Cluster) or raw_cluster.cluster_id != cluster_id:
            raise AssertionError("malformed cluster record")
        cluster = raw_cluster
        if not cluster.vertices:
            raise AssertionError("clusters must be nonempty")
        if cluster.boundary_edges != boundary_edges(adjacency, cluster.vertices):
            raise AssertionError("boundary-edge certificate mismatch")
        external_degree = len(cluster.boundary_edges)
        if external_degree > 3:
            raise AssertionError("external degree exceeds three")
        if external_degree == 3 and len(cluster.vertices) != 1:
            raise AssertionError("degree-three topology cluster is not a singleton")
        if not cluster.children:
            if len(cluster.vertices) != 1 or cluster.level != 0:
                raise AssertionError("base topology clusters must be singleton vertices")
            continue
        if len(cluster.children) not in (1, 2):
            raise AssertionError("topology hierarchy must be unary/binary")
        child_vertices: set[int] = set()
        child_level = None
        for child_id in cluster.children:
            child = clusters[child_id]
            if child_level is None:
                child_level = child.level
            elif child.level != child_level:
                raise AssertionError("children must lie on one topology level")
            if child.vertices & child_vertices:
                raise AssertionError("topology children must be vertex-disjoint")
            child_vertices.update(child.vertices)
        if frozenset(child_vertices) != cluster.vertices:
            raise AssertionError("parent vertices must equal the child union")
        if child_level is None or cluster.level != child_level + 1:
            raise AssertionError("topology levels must increase by one")
        if len(cluster.children) == 2:
            left = clusters[cluster.children[0]].vertices
            right = clusters[cluster.children[1]].vertices
            connecting = sum(
                1 for vertex in left for neighbor in adjacency[vertex] if neighbor in right
            )
            if connecting != 1:
                raise AssertionError("binary children must be adjacent by one tree edge")
    if clusters[root].vertices != all_vertices:
        raise AssertionError("root cluster must contain the whole source tree")


def prune_to_gate_tree(
    certificate: Mapping[str, object],
    label_by_vertex: Mapping[int, int],
) -> dict[str, object]:
    """Delete unlabeled topology leaves and suppress unary nodes."""
    clusters = certificate["clusters"]
    assert isinstance(clusters, Mapping)
    labels = {int(vertex): int(label) for vertex, label in label_by_vertex.items()}
    if len(set(labels.values())) != len(labels):
        raise ValueError("gate labels must be unique")
    if not labels:
        raise ValueError("at least one gate label is required")

    records: list[dict[str, object]] = []

    def visit(cluster_id: int) -> tuple[GateTree, frozenset[int], int] | None:
        cluster = clusters[cluster_id]
        assert isinstance(cluster, Cluster)
        if not cluster.children:
            vertex = next(iter(cluster.vertices))
            if vertex not in labels:
                return None
            label = labels[vertex]
            records.append(
                {
                    "cluster_id": cluster_id,
                    "labels": (label,),
                    "boundary_edges": cluster.boundary_edges,
                    "external_degree": len(cluster.boundary_edges),
                    "vertex_count": 1,
                }
            )
            return label, frozenset((label,)), cluster_id
        kept = [result for child in cluster.children if (result := visit(child)) is not None]
        if not kept:
            return None
        if len(kept) == 1:
            return kept[0]
        if len(kept) != 2:
            raise AssertionError("binary topology nodes have at most two retained children")
        tree: GateTree = (kept[0][0], kept[1][0])
        retained_labels = kept[0][1] | kept[1][1]
        records.append(
            {
                "cluster_id": cluster_id,
                "labels": tuple(sorted(retained_labels)),
                "boundary_edges": cluster.boundary_edges,
                "external_degree": len(cluster.boundary_edges),
                "vertex_count": len(cluster.vertices),
            }
        )
        return tree, retained_labels, cluster_id

    result = visit(int(certificate["root"]))
    if result is None:
        raise AssertionError("no labels survived topology pruning")
    expected = frozenset(labels.values())
    if result[1] != expected:
        raise AssertionError("pruned tree does not contain exactly the gate labels")
    for record in records:
        external_degree = int(record["external_degree"])
        if external_degree > 2:
            raise AssertionError(
                "retained label-bearing topology clusters must have at most two boundary edges"
            )
    return {
        "tree": result[0],
        "records": tuple(records),
        "height_upper_bound": int(certificate["height"]),
    }


def gate_tree_leaf_depths(tree: GateTree) -> dict[int, int]:
    depths: dict[int, int] = {}

    def visit(node: GateTree, depth: int) -> None:
        if isinstance(node, int):
            if node in depths:
                raise ValueError("gate-tree leaves must be unique")
            depths[node] = depth
            return
        visit(node[0], depth + 1)
        visit(node[1], depth + 1)

    visit(tree, 0)
    return depths


def source_edge_sides(
    adjacency: Mapping[int, set[int]], label_by_vertex: Mapping[int, int]
) -> dict[tuple[int, int], frozenset[int]]:
    labels = {int(vertex): int(label) for vertex, label in label_by_vertex.items()}
    answer: dict[tuple[int, int], frozenset[int]] = {}
    for left, neighbors in adjacency.items():
        for right in neighbors:
            if left >= right:
                continue
            seen = {left}
            stack = [left]
            while stack:
                vertex = stack.pop()
                for neighbor in adjacency[vertex]:
                    if (vertex == left and neighbor == right) or (
                        vertex == right and neighbor == left
                    ):
                        continue
                    if neighbor not in seen:
                        seen.add(neighbor)
                        stack.append(neighbor)
            answer[(left, right)] = frozenset(
                labels[vertex] for vertex in seen if vertex in labels
            )
    return answer


def support_boundary(
    supports: Sequence[Support], labels: Iterable[int]
) -> frozenset[int]:
    selected = set(map(int, labels))
    left: set[int] = set()
    right: set[int] = set()
    for index, support in enumerate(supports):
        (left if index in selected else right).update(support)
    return frozenset(left & right)


def middle_sets(
    adjacency: Mapping[int, set[int]],
    label_by_vertex: Mapping[int, int],
    supports: Sequence[Support],
) -> dict[tuple[int, int], frozenset[int]]:
    sides = source_edge_sides(adjacency, label_by_vertex)
    return {edge: support_boundary(supports, side) for edge, side in sides.items()}


def audit_two_edge_transfer(
    adjacency: Mapping[int, set[int]],
    label_by_vertex: Mapping[int, int],
    supports: Sequence[Support],
    pruned: Mapping[str, object],
) -> dict[str, object]:
    source_middle = middle_sets(adjacency, label_by_vertex, supports)
    source_width = max((len(middle) for middle in source_middle.values()), default=0)
    checked = 0
    maximum_transferred_width = 0
    maximum_cover_edges = 0
    for raw_record in pruned["records"]:
        record = dict(raw_record)
        labels = tuple(map(int, record["labels"]))
        boundary = support_boundary(supports, labels)
        cover_edges = []
        cover: set[int] = set()
        for oriented in record["boundary_edges"]:
            edge = tuple(sorted(map(int, oriented)))
            cover_edges.append(edge)
            cover.update(source_middle[edge])
        if not boundary <= cover:
            raise AssertionError("support boundary escaped the topology boundary-edge cover")
        checked += 1
        maximum_transferred_width = max(maximum_transferred_width, len(boundary))
        maximum_cover_edges = max(maximum_cover_edges, len(cover_edges))
    if maximum_transferred_width > 2 * source_width:
        raise AssertionError("topology transfer exceeded width 2b")
    return {
        "records_checked": checked,
        "source_width": source_width,
        "transferred_width": maximum_transferred_width,
        "maximum_cover_edges": maximum_cover_edges,
    }


def rooted_binary_source_tree(tree: GateTree) -> Adjacency:
    leaves: list[int] = []

    def collect(node: GateTree) -> None:
        if isinstance(node, int):
            leaves.append(node)
        else:
            collect(node[0])
            collect(node[1])

    collect(tree)
    if not leaves or len(set(leaves)) != len(leaves):
        raise ValueError("source leaves must be unique")
    next_vertex = max(leaves) + 1
    edges: list[tuple[int, int]] = []

    def build(node: GateTree) -> int:
        nonlocal next_vertex
        if isinstance(node, int):
            return node
        left = build(node[0])
        right = build(node[1])
        parent = next_vertex
        next_vertex += 1
        edges.extend(((parent, left), (parent, right)))
        return parent

    root = build(tree)
    adjacency = adjacency_from_edges(edges)
    if len(adjacency[root]) == 2:
        left, right = tuple(adjacency[root])
        adjacency[left].remove(root)
        adjacency[right].remove(root)
        del adjacency[root]
        adjacency[left].add(right)
        adjacency[right].add(left)
    validate_subcubic_tree(adjacency)
    return adjacency


def balanced_gate_tree(labels: Sequence[int]) -> GateTree:
    items = [int(label) for label in labels]
    if not items:
        raise ValueError("at least one label is required")
    if len(items) == 1:
        return items[0]
    middle = len(items) // 2
    return balanced_gate_tree(items[:middle]), balanced_gate_tree(items[middle:])


def ordered_full_binary_shapes(leaf_count: int) -> tuple[GateTree, ...]:
    """All ordered full binary shapes with leaves labelled left-to-right."""
    if leaf_count < 1:
        raise ValueError("leaf_count must be positive")

    @dataclass(frozen=True)
    class Key:
        size: int
        offset: int

    cache: dict[Key, tuple[GateTree, ...]] = {}

    def shapes(size: int, offset: int) -> tuple[GateTree, ...]:
        key = Key(size, offset)
        if key in cache:
            return cache[key]
        if size == 1:
            answer: tuple[GateTree, ...] = (offset,)
        else:
            items: list[GateTree] = []
            for left_size in range(1, size):
                for left in shapes(left_size, offset):
                    for right in shapes(size - left_size, offset + left_size):
                        items.append((left, right))
            answer = tuple(items)
        cache[key] = answer
        return answer

    return shapes(int(leaf_count), 0)
