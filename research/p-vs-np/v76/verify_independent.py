#!/usr/bin/env python3
"""Independent V76 audit from raw incidence sets and tree clusters.

This verifier imports neither the Pareto engine nor the top-cluster auditor.
"""
from __future__ import annotations

import json
from functools import lru_cache
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent

WITNESS = (
    (0,),
    (1,),
    (0, 2),
    (0, 3),
    (1, 2),
    (1, 3),
    (2, 3),
)
Tree = int | tuple["Tree", "Tree"]


def tree_key(tree: Tree):
    if isinstance(tree, int):
        return 0, tree
    return 1, tree_key(tree[0]), tree_key(tree[1])


@lru_cache(None)
def trees(items: tuple[int, ...]) -> tuple[Tree, ...]:
    if len(items) == 1:
        return (items[0],)
    anchor = items[0]
    rest = items[1:]
    answer = {}
    for count in range(len(rest)):
        for extra in combinations(rest, count):
            left_items = (anchor,) + extra
            if len(left_items) == len(items):
                continue
            right_items = tuple(item for item in items if item not in left_items)
            for left in trees(tuple(sorted(left_items))):
                for right in trees(tuple(sorted(right_items))):
                    pair = tuple(sorted((left, right), key=tree_key))
                    answer[tree_key(pair)] = pair
    return tuple(answer[key] for key in sorted(answer))


def depths(tree: Tree) -> dict[int, int]:
    answer = {}

    def visit(node: Tree, depth: int) -> frozenset[int]:
        if isinstance(node, int):
            if node in answer:
                raise AssertionError("duplicate gate leaf")
            answer[node] = depth
            return frozenset((node,))
        return visit(node[0], depth + 1) | visit(node[1], depth + 1)

    visit(tree, 0)
    return answer


def boundary_variables(supports, chosen):
    selected = {
        variable
        for index, support in enumerate(supports)
        if index in chosen
        for variable in support
    }
    outside = {
        variable
        for index, support in enumerate(supports)
        if index not in chosen
        for variable in support
    }
    return frozenset(selected & outside)


def metrics(supports, tree):
    subsets = []

    def visit(node):
        if isinstance(node, int):
            chosen = frozenset((node,))
        else:
            chosen = visit(node[0]) | visit(node[1])
        subsets.append(chosen)
        return chosen

    assert visit(tree) == frozenset(range(len(supports)))
    ds = depths(tree)
    return (
        max(len(boundary_variables(supports, chosen)) for chosen in subsets),
        max(ds.values(), default=0),
        sum(ds.values()),
    )


def pareto(triples):
    return tuple(
        sorted(
            triple
            for triple in triples
            if not any(
                other != triple
                and all(left <= right for left, right in zip(other, triple))
                for other in triples
            )
        )
    )


def brute_frontier(supports):
    return pareto(
        {metrics(supports, tree) for tree in trees(tuple(range(len(supports))))}
    )


def unroot(tree):
    adjacency = {}
    labels = {}
    next_internal = 0

    def edge(a, b):
        adjacency.setdefault(a, set()).add(b)
        adjacency.setdefault(b, set()).add(a)

    def build(node):
        nonlocal next_internal
        if isinstance(node, int):
            key = ("L", node)
            adjacency.setdefault(key, set())
            labels[key] = node
            return key
        key = ("I", next_internal)
        next_internal += 1
        adjacency.setdefault(key, set())
        edge(key, build(node[0]))
        edge(key, build(node[1]))
        return key

    root = build(tree)
    if isinstance(tree, int):
        return adjacency, labels
    a, b = tuple(adjacency[root])
    adjacency[a].remove(root)
    adjacency[b].remove(root)
    del adjacency[root]
    edge(a, b)
    return adjacency, labels


def connected_subsets(adjacency):
    nodes = tuple(sorted(adjacency, key=repr))
    for mask in range(1, 1 << len(nodes)):
        chosen = frozenset(
            nodes[index] for index in range(len(nodes)) if mask >> index & 1
        )
        seen = {next(iter(chosen))}
        todo = list(seen)
        while todo:
            node = todo.pop()
            for neighbor in adjacency[node]:
                if neighbor in chosen and neighbor not in seen:
                    seen.add(neighbor)
                    todo.append(neighbor)
        if seen == set(chosen):
            yield chosen


def edge_side_labels(adjacency, labels, start, blocked):
    seen = {blocked}
    todo = [start]
    answer = set()
    while todo:
        node = todo.pop()
        if node in seen:
            continue
        seen.add(node)
        if node in labels:
            answer.add(labels[node])
        todo.extend(adjacency[node] - seen)
    return frozenset(answer)


def independent_cluster_audit(supports, tree):
    adjacency, labels = unroot(tree)
    states = 0
    maximum_cover = 0
    for vertices in connected_subsets(adjacency):
        available = tuple(labels[node] for node in vertices if node in labels)
        omissions = [tuple()]
        omissions.extend((label,) for label in available)
        omissions.extend(combinations(available, 2))
        for omitted in omissions:
            included = frozenset(set(available) - set(omitted))
            if not included:
                continue
            omitted_vertices = {
                node
                for node in vertices
                if node in labels and labels[node] not in included
            }
            boundary_vertices = {
                node
                for node in vertices
                if any(neighbor not in vertices for neighbor in adjacency[node])
            } | omitted_vertices
            if len(boundary_vertices) > 2:
                continue

            cover = set()
            for node in vertices:
                for neighbor in adjacency[node]:
                    if neighbor not in vertices:
                        cover.add((node, neighbor))
            for node in omitted_vertices:
                assert len(adjacency[node]) == 1
                neighbor = next(iter(adjacency[node]))
                cover.add(tuple(sorted((node, neighbor), key=repr)))
            assert len(cover) <= 4

            union_middle = set()
            for a, b in cover:
                side = edge_side_labels(adjacency, labels, a, b)
                union_middle.update(boundary_variables(supports, side))
            assert boundary_variables(supports, included) <= union_middle
            maximum_cover = max(maximum_cover, len(cover))
            states += 1
    return states, maximum_cover


def verify_posimodularity(supports):
    m = len(supports)
    all_sets = [
        frozenset(i for i in range(m) if mask >> i & 1)
        for mask in range(1 << m)
    ]
    full = frozenset(range(m))
    for left in all_sets:
        assert boundary_variables(supports, left) == boundary_variables(
            supports, full - left
        )
        for right in all_sets:
            assert len(boundary_variables(supports, left - right)) + len(
                boundary_variables(supports, right - left)
            ) <= len(boundary_variables(supports, left)) + len(
                boundary_variables(supports, right)
            )


def main() -> None:
    results = json.loads((HERE / "RESULTS.json").read_text(encoding="utf-8"))

    universe = tuple(
        support
        for arity in (1, 2, 3)
        for support in combinations(range(4), arity)
    )
    instances = 0
    tree_evaluations = 0
    for m in range(1, 5):
        count = len(trees(tuple(range(m))))
        for supports in combinations(universe, m):
            assert brute_frontier(supports)
            instances += 1
            tree_evaluations += count
    assert instances == 1470
    assert tree_evaluations == 16212

    witness_trees = trees(tuple(range(7)))
    assert len(witness_trees) == 10395
    assert brute_frontier(WITNESS) == ((2, 4, 21), (3, 3, 20))
    verify_posimodularity(WITNESS)

    audited_states = 0
    maximum_cover = 0
    for tree in witness_trees[:256]:
        states, cover = independent_cluster_audit(WITNESS, tree)
        audited_states += states
        maximum_cover = max(maximum_cover, cover)
    assert audited_states > 0
    assert maximum_cover == 4

    listed = results["exhaustive_n4_simple_rank3"]["inflated_families"]
    assert len(listed) == 6
    for item in listed:
        supports = tuple(tuple(support) for support in item["supports"])
        assert brute_frontier(supports) == ((2, 4, 21), (3, 3, 20))

    private = results["private_vertex_tree_regression"][-1]
    assert private["gate_count"] == 14
    assert [tuple(entry) for entry in private["exact"]["frontier"]] == [
        (2, 5, 55),
        (3, 4, 54),
    ]

    status = results["scientific_status"]
    assert status["top_tree_log_height_is_prior_art"] is True
    assert status["four_cut_cover_lemma_proved"] is True
    assert status["width_2b_centroid_transfer_claimed"] is False
    assert status["width_preserving_O_log_m_refuted"] is False
    assert status["p_vs_np_resolved"] is False

    print(
        "V76 independent verification passed: raw support posimodularity; "
        "1,470 small families and 16,212 brute trees; exact 10,395-tree witness; "
        "independent two-boundary four-cut audits on 256 source trees; six "
        "tradeoff families; zero failures."
    )


if __name__ == "__main__":
    main()
