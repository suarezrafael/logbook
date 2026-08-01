#!/usr/bin/env python3
"""Deterministic V77 generator: topology-tree 2b transfer and finite audits."""
from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
from json import dumps
from math import ceil, log2
from pathlib import Path
import random
from typing import Iterable, Sequence

from topology_tree_certificate import (
    adjacency_from_edges,
    audit_two_edge_transfer,
    balanced_gate_tree,
    boundary_edges,
    build_topology_certificate,
    gate_tree_leaf_depths,
    ordered_full_binary_shapes,
    prune_to_gate_tree,
    rooted_binary_source_tree,
    support_boundary,
    verify_topology_certificate,
)

HERE = Path(__file__).resolve().parent
Support = tuple[int, ...]


def gaussian_binomial_2(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    numerator = denominator = 1
    for index in range(k):
        numerator *= (1 << (n - index)) - 1
        denominator *= (1 << (k - index)) - 1
    return numerator // denominator


def affine_subspace_count(boundary_size: int) -> int:
    return sum(
        (1 << (boundary_size - codimension))
        * gaussian_binomial_2(boundary_size, codimension)
        for codimension in range(boundary_size + 1)
    )


def boundary_profile(supports: Sequence[Support]) -> tuple[int, ...]:
    m = len(supports)
    unions = [set() for _ in range(1 << m)]
    for mask in range(1, 1 << m):
        bit = mask & -mask
        index = bit.bit_length() - 1
        unions[mask] = unions[mask ^ bit] | set(supports[index])
    full = (1 << m) - 1
    return tuple(len(unions[mask] & unions[full ^ mask]) for mask in range(1 << m))


def _prune_metric_triples(
    triples: Iterable[tuple[int, int, int]],
) -> tuple[tuple[int, int, int], ...]:
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


def exact_pareto_metrics(supports: Sequence[Support]) -> tuple[tuple[int, int, int], ...]:
    m = len(supports)
    boundaries = boundary_profile(supports)
    dynamic: list[tuple[tuple[int, int, int], ...]] = [tuple() for _ in range(1 << m)]
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


def exact_summary(supports: Sequence[Support]) -> dict[str, int | list[list[int]]]:
    frontier = exact_pareto_metrics(supports)
    m = len(supports)
    cap = ceil(log2(m)) if m > 1 else 0
    minimum_width = min(item[0] for item in frontier)
    width_at_cap = min(item[0] for item in frontier if item[1] <= cap)
    return {
        "m": m,
        "log_height_cap": cap,
        "minimum_width": minimum_width,
        "minimum_width_at_log_height": width_at_cap,
        "width_inflation_at_log_height": width_at_cap - minimum_width,
        "frontier": [list(item) for item in frontier],
    }


def support_universe_masks(variable_count: int) -> tuple[int, ...]:
    return tuple(
        sum(1 << variable for variable in support)
        for rank in (1, 2, 3)
        for support in combinations(range(variable_count), rank)
    )


def _permutation_maps(variable_count: int, universe: Sequence[int]) -> tuple[dict[int, int], ...]:
    maps: list[dict[int, int]] = []
    for permutation in permutations(range(variable_count)):
        mapping: dict[int, int] = {}
        for support in universe:
            image = 0
            for variable in range(variable_count):
                if (support >> variable) & 1:
                    image |= 1 << permutation[variable]
            mapping[support] = image
        maps.append(mapping)
    return tuple(maps)


def canonical_support_family(
    family: Sequence[int], permutation_maps: Sequence[dict[int, int]]
) -> tuple[int, ...]:
    return min(
        tuple(sorted(mapping[support] for support in family))
        for mapping in permutation_maps
    )


def mask_family_to_supports(family: Sequence[int]) -> tuple[Support, ...]:
    return tuple(
        tuple(variable for variable in range(5) if (support >> variable) & 1)
        for support in family
    )


def five_variable_isomorphism_audit(max_gates: int = 6) -> dict[str, object]:
    universe = support_universe_masks(5)
    permutation_maps = _permutation_maps(5, universe)
    by_gate_count: dict[str, object] = {}
    orbit_total = raw_total = inflated_total = 0
    for gate_count in range(1, int(max_gates) + 1):
        canonical: set[tuple[int, ...]] = set()
        raw_count = 0
        for family in combinations(universe, gate_count):
            raw_count += 1
            canonical.add(canonical_support_family(family, permutation_maps))
        inflated = 0
        maximum_inflation = 0
        for family in sorted(canonical):
            summary = exact_summary(mask_family_to_supports(family))
            inflation = int(summary["width_inflation_at_log_height"])
            if inflation:
                inflated += 1
                maximum_inflation = max(maximum_inflation, inflation)
        by_gate_count[str(gate_count)] = {
            "raw_families": raw_count,
            "isomorphism_orbits": len(canonical),
            "perfect_height_width_inflations": inflated,
            "maximum_additive_inflation": maximum_inflation,
        }
        raw_total += raw_count
        orbit_total += len(canonical)
        inflated_total += inflated
    return {
        "variables": 5,
        "support_universe_size": len(universe),
        "maximum_gate_count": int(max_gates),
        "raw_families": raw_total,
        "isomorphism_orbits": orbit_total,
        "perfect_height_width_inflations": inflated_total,
        "by_gate_count": by_gate_count,
    }


def _serialize_certificate(certificate: dict[str, object], labels: dict[int, int]) -> dict[str, object]:
    clusters = certificate["clusters"]
    assert isinstance(clusters, dict)
    return {
        "source_adjacency": {
            str(vertex): list(neighbors)
            for vertex, neighbors in sorted(certificate["source_adjacency"].items())
        },
        "labels": {str(vertex): label for vertex, label in sorted(labels.items())},
        "root": int(certificate["root"]),
        "height": int(certificate["height"]),
        "rounds": list(certificate["rounds"]),
        "clusters": [
            {
                "cluster_id": cluster.cluster_id,
                "vertices": sorted(cluster.vertices),
                "children": list(cluster.children),
                "level": cluster.level,
                "boundary_edges": [list(edge) for edge in cluster.boundary_edges],
            }
            for _, cluster in sorted(clusters.items())
        ],
    }


def topology_shape_audit(max_leaves: int = 9) -> tuple[dict[str, object], dict[str, object]]:
    shape_count = 0
    source_vertices = 0
    topology_clusters = 0
    retained_clusters = 0
    max_height = 0
    max_retained_height = 0
    all_boundary_histogram: Counter[int] = Counter()
    retained_boundary_histogram: Counter[int] = Counter()
    representative: dict[str, object] | None = None

    for leaf_count in range(2, int(max_leaves) + 1):
        for shape_index, shape in enumerate(ordered_full_binary_shapes(leaf_count)):
            adjacency = rooted_binary_source_tree(shape)
            labels = {vertex: vertex for vertex in range(leaf_count)}
            certificate = build_topology_certificate(adjacency)
            verify_topology_certificate(certificate)
            pruned = prune_to_gate_tree(certificate, labels)
            depths = gate_tree_leaf_depths(pruned["tree"])
            shape_count += 1
            source_vertices += len(adjacency)
            topology_clusters += len(certificate["clusters"])
            retained_clusters += len(pruned["records"])
            max_height = max(max_height, int(certificate["height"]))
            max_retained_height = max(max_retained_height, max(depths.values(), default=0))
            for cluster in certificate["clusters"].values():
                all_boundary_histogram[len(cluster.boundary_edges)] += 1
            for record in pruned["records"]:
                retained_boundary_histogram[int(record["external_degree"])] += 1
            if leaf_count == max_leaves and shape_index == 0:
                representative = _serialize_certificate(certificate, labels)

    if representative is None:
        raise AssertionError("representative topology certificate was not produced")
    representative_bytes = (dumps(representative, indent=2, sort_keys=True) + "\n").encode()
    return (
        {
            "maximum_leaf_count": int(max_leaves),
            "ordered_source_shapes": shape_count,
            "source_vertices": source_vertices,
            "topology_clusters": topology_clusters,
            "retained_label_clusters": retained_clusters,
            "maximum_topology_height": max_height,
            "maximum_retained_gate_height": max_retained_height,
            "all_cluster_boundary_edge_histogram": {
                str(key): value for key, value in sorted(all_boundary_histogram.items())
            },
            "retained_cluster_boundary_edge_histogram": {
                str(key): value for key, value in sorted(retained_boundary_histogram.items())
            },
            "retained_degree_three_clusters": retained_boundary_histogram[3],
        },
        {
            "data": representative,
            "sha256": sha256(representative_bytes).hexdigest(),
            "bytes": len(representative_bytes),
        },
    )


def random_support(rng: random.Random, variable_count: int) -> Support:
    rank = rng.randint(1, min(3, variable_count))
    return tuple(sorted(rng.sample(range(variable_count), rank)))


def seeded_transfer_audit(seed: int = 770077, systems: int = 256) -> dict[str, object]:
    rng = random.Random(seed)
    checked_records = 0
    maximum_source_width = 0
    maximum_transferred_width = 0
    maximum_ratio_numerator = 0
    maximum_ratio_denominator = 1
    maximum_cover_edges = 0
    for system_index in range(int(systems)):
        leaf_count = rng.randint(3, 18)
        if system_index % 2:
            shape = balanced_gate_tree(list(range(leaf_count)))
        else:
            shape = next(iter(ordered_full_binary_shapes(min(leaf_count, 9))))
            if leaf_count > 9:
                shape = balanced_gate_tree(list(range(leaf_count)))
        adjacency = rooted_binary_source_tree(shape)
        labels = {vertex: vertex for vertex in range(leaf_count)}
        variable_count = rng.randint(3, max(3, leaf_count))
        supports = tuple(random_support(rng, variable_count) for _ in range(leaf_count))
        certificate = build_topology_certificate(adjacency)
        pruned = prune_to_gate_tree(certificate, labels)
        audit = audit_two_edge_transfer(adjacency, labels, supports, pruned)
        checked_records += int(audit["records_checked"])
        source_width = int(audit["source_width"])
        transferred_width = int(audit["transferred_width"])
        maximum_source_width = max(maximum_source_width, source_width)
        maximum_transferred_width = max(maximum_transferred_width, transferred_width)
        maximum_cover_edges = max(maximum_cover_edges, int(audit["maximum_cover_edges"]))
        if source_width and transferred_width * maximum_ratio_denominator > maximum_ratio_numerator * source_width:
            maximum_ratio_numerator = transferred_width
            maximum_ratio_denominator = source_width
    return {
        "seed": int(seed),
        "systems": int(systems),
        "retained_records_checked": checked_records,
        "maximum_source_width": maximum_source_width,
        "maximum_transferred_width": maximum_transferred_width,
        "maximum_observed_ratio": [maximum_ratio_numerator, maximum_ratio_denominator],
        "maximum_cover_edges": maximum_cover_edges,
    }


def two_edge_tightness_witness() -> dict[str, object]:
    adjacency = rooted_binary_source_tree(((0, 1), (2, 3)))
    labels = {vertex: vertex for vertex in range(4)}
    supports: tuple[Support, ...] = ((0, 1, 2), (0, 1, 2), (3, 4, 5), (3, 4, 5))
    internal_vertices = sorted(vertex for vertex in adjacency if vertex not in labels)
    cluster_vertices = frozenset((1, 2, *internal_vertices))
    crossing = boundary_edges(adjacency, cluster_vertices)
    inside_labels = tuple(sorted(labels[vertex] for vertex in cluster_vertices if vertex in labels))
    boundary = support_boundary(supports, inside_labels)
    from topology_tree_certificate import middle_sets

    source_middle = middle_sets(adjacency, labels, supports)
    source_width = max(len(value) for value in source_middle.values())
    cover = set()
    for oriented in crossing:
        cover.update(source_middle[tuple(sorted(oriented))])
    if source_width != 3 or len(crossing) != 2 or len(boundary) != 6 or boundary != cover:
        raise AssertionError("two-edge tightness witness failed")
    return {
        "source_width_b": source_width,
        "cluster_labels": list(inside_labels),
        "boundary_edges": [list(edge) for edge in crossing],
        "cluster_support_boundary": sorted(boundary),
        "cluster_width": len(boundary),
        "ratio": [len(boundary), source_width],
        "interpretation": "The two-edge cover inequality can attain 2b on a valid label-bearing cluster; this is not a lower bound for every logarithmic-height hierarchy.",
    }


def affine_cost_table(max_b: int = 4) -> list[dict[str, object]]:
    rows = []
    for b in range(1, int(max_b) + 1):
        a2 = affine_subspace_count(2 * b)
        a4 = affine_subspace_count(4 * b)
        rows.append(
            {
                "b": b,
                "A_2b": a2,
                "A_4b": a4,
                "squared_cost_ratio_A4b_over_A2b": [a4 * a4, a2 * a2],
            }
        )
    return rows


def v76_witness_regression() -> dict[str, object]:
    witnesses = (
        ((0,), (1,), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)),
        ((0,), (2,), (0, 1), (0, 3), (1, 2), (1, 3), (2, 3)),
        ((0,), (3,), (0, 1), (0, 2), (1, 2), (1, 3), (2, 3)),
        ((1,), (2,), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3)),
        ((1,), (3,), (0, 1), (0, 2), (0, 3), (1, 2), (2, 3)),
        ((2,), (3,), (0, 1), (0, 2), (0, 3), (1, 2), (1, 3)),
    )
    summaries = [exact_summary(witness) for witness in witnesses]
    if not all(
        summary["minimum_width"] == 2
        and summary["minimum_width_at_log_height"] == 3
        for summary in summaries
    ):
        raise AssertionError("V76 perfect-height witnesses drifted")
    return {
        "families": len(witnesses),
        "frontiers": [summary["frontier"] for summary in summaries],
        "all_minimum_width": 2,
        "all_perfect_height_width": 3,
        "interpretation": "The finite perfect-height tradeoff remains valid but does not contradict the 2b O(log m) topology-tree transfer.",
    }


def generate_results() -> tuple[dict[str, object], dict[str, object]]:
    topology_audit, static_certificate = topology_shape_audit()
    results = {
        "version": "V77",
        "status": "passed",
        "failures": 0,
        "transfer_theorem": {
            "name": "restricted topology-tree support-boundary transfer",
            "input": "a supplied width-b subcubic gate branch decomposition",
            "prior_art": "Frederickson restricted multilevel partitions/topology trees, as related to top trees by Alstrup-Holm-de Lichtenberg-Thorup",
            "cluster_property": "each non-singleton topology cluster has at most two boundary edges; an external-degree-three cluster is a singleton",
            "label_property": "gate labels lie at degree-one source leaves, so every retained label-bearing cluster has at most two boundary edges",
            "output_width": "at most 2b",
            "output_height": "O(log m)",
            "output_external_path_length": "O(m log m)",
            "v75_consequence": "O(m log m A(2b)^2 poly(n,m)) incremental prefix avoidance",
        },
        "topology_certificate_audit": topology_audit,
        "seeded_transfer_audit": seeded_transfer_audit(),
        "two_edge_tightness_witness": two_edge_tightness_witness(),
        "five_variable_isomorphism_audit": five_variable_isomorphism_audit(),
        "v76_witness_regression": v76_witness_regression(),
        "affine_cost_table": affine_cost_table(),
        "static_certificate": {
            "path": "STATIC_TOPOLOGY_CERTIFICATE.json",
            "sha256": static_certificate["sha256"],
            "bytes": static_certificate["bytes"],
        },
        "scientific_status": {
            "topology_tree_log_height_is_prior_art": True,
            "retained_cluster_two_edge_lemma_proved": True,
            "supplied_decomposition_width_2b_log_height_transfer_proved": True,
            "v76_width_4b_transfer_still_correct_but_dominated": True,
            "factor_two_known_optimal_for_all_hierarchies": False,
            "two_edge_cover_inequality_tight_for_one_cluster": True,
            "width_preserving_O_log_m_refuted": False,
            "unrestricted_nc0_3_avoid_solved": False,
            "standard_model_lower_bound_proved": False,
            "p_vs_np_route_active": False,
            "p_vs_np_resolved": False,
            "novelty_confirmed": False,
            "peer_reviewed": False,
        },
    }
    return results, static_certificate["data"]


def main() -> None:
    results, static_certificate = generate_results()
    (HERE / "RESULTS.json").write_text(dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (HERE / "STATIC_TOPOLOGY_CERTIFICATE.json").write_text(
        dumps(static_certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        "V77 generation passed: prior-art topology hierarchy; proved retained two-edge cover and 2b transfer; "
        f"{results['topology_certificate_audit']['ordered_source_shapes']} ordered source shapes; "
        f"{results['five_variable_isomorphism_audit']['isomorphism_orbits']} five-variable support orbits; zero failures."
    )


if __name__ == "__main__":
    main()
