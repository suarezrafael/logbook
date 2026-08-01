#!/usr/bin/env python3
"""Deterministic V76 top-tree transfer result generator."""
from __future__ import annotations

import json
import random
from itertools import combinations
from pathlib import Path

from decomposition_pareto import (
    all_rooted_binary_trees,
    balanced_branch_tree,
    brute_pareto_frontier,
    exact_pareto_frontier,
    exact_pareto_metrics,
    frontier_greedy_order,
    support_lookahead_order,
    tree_metrics,
)
from cluster_cut_cover import audit_all_two_boundary_clusters

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


def simple_rank3_universe(n: int = 4) -> tuple[tuple[int, ...], ...]:
    return tuple(
        support
        for arity in (1, 2, 3)
        for support in combinations(range(int(n)), arity)
    )


def frontier_triples(result: dict[str, object]) -> list[list[int]]:
    return [
        [
            int(item["width"]),
            int(item["height"]),
            int(item["external_path_length"]),
        ]
        for item in result["frontier"]
    ]


def compact_exact(result: dict[str, object]) -> dict[str, object]:
    return {
        "m": int(result["m"]),
        "log_height_cap": int(result["log_height_cap"]),
        "minimum_width": int(result["minimum_width"]),
        "minimum_width_at_log_height": int(result["minimum_width_at_log_height"]),
        "width_inflation_at_log_height": int(result["width_inflation_at_log_height"]),
        "minimum_height_at_minimum_width": int(
            result["minimum_height_at_minimum_width"]
        ),
        "frontier": frontier_triples(result),
    }


def exact_dp_bruteforce_validation() -> dict[str, int]:
    universe = simple_rank3_universe(4)
    instances = 0
    tree_evaluations = 0
    for m in range(1, 5):
        tree_count = len(all_rooted_binary_trees(tuple(range(m))))
        for supports in combinations(universe, m):
            dynamic = exact_pareto_frontier(supports)
            brute = brute_pareto_frontier(supports)
            dynamic_triples = tuple(
                (
                    int(item["width"]),
                    int(item["height"]),
                    int(item["external_path_length"]),
                )
                for item in dynamic["frontier"]
            )
            if dynamic_triples != brute:
                raise AssertionError((supports, dynamic_triples, brute))
            instances += 1
            tree_evaluations += tree_count
    return {
        "instances": instances,
        "rooted_tree_evaluations": tree_evaluations,
        "maximum_gate_count": 4,
    }


def exhaustive_n4_classification() -> dict[str, object]:
    universe = simple_rank3_universe(4)
    by_m: dict[str, dict[str, int]] = {}
    inflated: list[dict[str, object]] = []
    total = 0
    maximum_inflation = 0
    for m in range(1, 8):
        instances = 0
        inflated_count = 0
        for supports in combinations(universe, m):
            result = exact_pareto_frontier(supports)
            inflation = int(result["width_inflation_at_log_height"])
            total += 1
            instances += 1
            if inflation:
                inflated_count += 1
                maximum_inflation = max(maximum_inflation, inflation)
                inflated.append(
                    {
                        "supports": supports,
                        "minimum_width": result["minimum_width"],
                        "minimum_width_at_height_cap": result[
                            "minimum_width_at_log_height"
                        ],
                        "height_cap": result["log_height_cap"],
                        "frontier": frontier_triples(result),
                    }
                )
        by_m[str(m)] = {
            "instances": instances,
            "perfect_height_width_inflations": inflated_count,
        }
    return {
        "variables": 4,
        "support_universe_size": len(universe),
        "maximum_gate_count": 7,
        "instances": total,
        "by_gate_count": by_m,
        "inflated_instances": len(inflated),
        "maximum_additive_inflation": maximum_inflation,
        "inflated_families": inflated,
    }


def witness_audit() -> dict[str, object]:
    exact = exact_pareto_frontier(WITNESS)
    brute = brute_pareto_frontier(WITNESS)
    exact_triples = tuple(
        (
            int(item["width"]),
            int(item["height"]),
            int(item["external_path_length"]),
        )
        for item in exact["frontier"]
    )
    if exact_triples != brute:
        raise AssertionError((exact_triples, brute))
    orders = {
        "natural": list(range(7)),
        "frontier_greedy": frontier_greedy_order(WITNESS),
        "support_lookahead_2": support_lookahead_order(WITNESS, 2),
    }
    heuristics = {}
    for name, order in orders.items():
        metrics = tree_metrics(WITNESS, balanced_branch_tree(order))
        heuristics[name] = {
            "order": order,
            "width": int(metrics["width"]),
            "height": int(metrics["height"]),
            "external_path_length": int(metrics["external_path_length"]),
        }
    return {
        "supports": WITNESS,
        "rank": 2,
        "gate_count": 7,
        "rooted_binary_trees": len(all_rooted_binary_trees(tuple(range(7)))),
        "exact": compact_exact(exact),
        "brute_frontier": [list(item) for item in brute],
        "heuristics": heuristics,
        "interpretation": (
            "Width 2 requires height at least 4, whereas the minimum possible "
            "leaf height ceil(log2 7)=3 requires width 3. This does not refute "
            "width-preserving O(log m) balancing."
        ),
    }


def top_cluster_cover_validation(seed: int = 760076) -> dict[str, object]:
    universe = simple_rank3_universe(4)
    exact_sources = 0
    labelled_states = 0
    connected_clusters = 0
    maximum_cover_edges = 0

    for m in range(1, 5):
        for supports in combinations(universe, m):
            exact = exact_pareto_frontier(supports)
            source = min(
                exact["frontier"],
                key=lambda item: (
                    int(item["width"]),
                    int(item["height"]),
                    int(item["external_path_length"]),
                ),
            )["tree"]
            audit = audit_all_two_boundary_clusters(supports, source)
            exact_sources += 1
            labelled_states += audit["labelled_cluster_states"]
            connected_clusters += audit["connected_vertex_clusters"]
            maximum_cover_edges = max(maximum_cover_edges, audit["maximum_cover_edges"])

    witness_trees = all_rooted_binary_trees(tuple(range(7)))
    witness_tree_checks = 128
    for tree in witness_trees[:witness_tree_checks]:
        audit = audit_all_two_boundary_clusters(WITNESS, tree)
        labelled_states += audit["labelled_cluster_states"]
        connected_clusters += audit["connected_vertex_clusters"]
        maximum_cover_edges = max(maximum_cover_edges, audit["maximum_cover_edges"])

    rng = random.Random(seed)
    random_instances = 64
    for _ in range(random_instances):
        n = rng.randint(2, 7)
        m = rng.randint(2, 7)
        supports = tuple(
            tuple(sorted(rng.sample(range(n), rng.randint(1, min(3, n)))))
            for _ in range(m)
        )
        order = list(range(m))
        rng.shuffle(order)
        audit = audit_all_two_boundary_clusters(
            supports, balanced_branch_tree(order)
        )
        labelled_states += audit["labelled_cluster_states"]
        connected_clusters += audit["connected_vertex_clusters"]
        maximum_cover_edges = max(maximum_cover_edges, audit["maximum_cover_edges"])

    if maximum_cover_edges != 4:
        raise AssertionError("the audit should exercise the full four-cut cover")
    return {
        "seed": seed,
        "exact_optimal_source_instances_n4_m_le_4": exact_sources,
        "sampled_witness_source_trees": witness_tree_checks,
        "seeded_random_instances": random_instances,
        "connected_vertex_clusters": connected_clusters,
        "labelled_cluster_states": labelled_states,
        "maximum_cover_edges": maximum_cover_edges,
        "all_states_covered": True,
    }


def or_path_regression() -> list[dict[str, object]]:
    answer = []
    for edge_count in range(1, 9):
        supports = tuple((index, index + 1) for index in range(edge_count))
        answer.append(
            {
                "edge_count": edge_count,
                "exact": compact_exact(exact_pareto_frontier(supports)),
            }
        )
    return answer


def padded_binary_tree_supports(height: int) -> tuple[tuple[int, ...], ...]:
    tree_vertices = (1 << (int(height) + 1)) - 1
    next_private = tree_vertices
    supports: list[tuple[int, ...]] = []
    for parent in range((1 << int(height)) - 1):
        for child in (2 * parent + 1, 2 * parent + 2):
            supports.append((parent, child, next_private))
            next_private += 1
    return tuple(supports)


def private_vertex_tree_regression() -> list[dict[str, object]]:
    answer: list[dict[str, object]] = []
    for height in range(1, 4):
        supports = padded_binary_tree_supports(height)
        if len(supports) <= 8:
            exact = compact_exact(exact_pareto_frontier(supports))
        else:
            metrics = exact_pareto_metrics(supports)
            logarithmic_height = (len(supports) - 1).bit_length()
            exact = {
                "m": len(supports),
                "log_height_cap": logarithmic_height,
                "minimum_width": min(item[0] for item in metrics),
                "minimum_width_at_log_height": min(
                    item[0] for item in metrics if item[1] <= logarithmic_height
                ),
                "width_inflation_at_log_height": (
                    min(item[0] for item in metrics if item[1] <= logarithmic_height)
                    - min(item[0] for item in metrics)
                ),
                "frontier": [list(item) for item in metrics],
                "witness_trees_retained": False,
            }
        answer.append(
            {
                "underlying_binary_tree_height": height,
                "gate_count": len(supports),
                "exact": exact,
            }
        )
    return answer


def generate_results() -> dict[str, object]:
    return {
        "version": "V76",
        "status": "passed",
        "failures": 0,
        "top_tree_prior_art": {
            "source": "Alstrup-Holm-de Lichtenberg-Thorup top trees",
            "cluster_property": (
                "binary hierarchy of connected labelled-tree clusters with at "
                "most two boundary vertices"
            ),
            "height": "O(log m) for the O(m)-size labelled branch tree",
            "implementation_status": (
                "standard external construction; V76 implements an independent "
                "cluster-certificate and cut-cover auditor, not a new top-tree library"
            ),
        },
        "transfer_theorem": {
            "name": "labelled top-tree support-boundary transfer",
            "input": "a supplied width-b subcubic gate branch decomposition",
            "output_width": "at most 4b",
            "output_height": "O(log m)",
            "output_external_path_length": "O(m log m)",
            "cover_lemma": (
                "each retained labelled top-tree cluster has at most two boundary "
                "vertices and its support boundary is covered by at most four "
                "original branch-edge middle sets"
            ),
            "v75_consequence": (
                "O(m log m A(4b)^2 poly(n,m)) incremental prefix avoidance"
            ),
        },
        "private_vertex_tree_regression": private_vertex_tree_regression(),
        "exact_dp_validation": exact_dp_bruteforce_validation(),
        "exhaustive_n4_simple_rank3": exhaustive_n4_classification(),
        "or_path_regression": or_path_regression(),
        "canonical_perfect_height_tradeoff": witness_audit(),
        "top_cluster_cover_validation": top_cluster_cover_validation(),
        "scientific_status": {
            "top_tree_log_height_is_prior_art": True,
            "four_cut_cover_lemma_proved": True,
            "supplied_decomposition_width_4b_log_height_transfer_proved": True,
            "v75_arbitrary_tree_depth_obstruction_removed_at_4b": True,
            "width_2b_centroid_transfer_claimed": False,
            "exact_width_preservation_at_height_ceil_log2_m": False,
            "width_preserving_O_log_m_refuted": False,
            "factor_four_known_optimal": False,
            "unrestricted_nc0_3_avoid_solved": False,
            "standard_model_lower_bound_proved": False,
            "p_vs_np_route_active": False,
            "p_vs_np_resolved": False,
            "novelty_confirmed": False,
            "peer_reviewed": False,
        },
    }


def main() -> None:
    results = generate_results()
    (HERE / "RESULTS.json").write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        "V76 generation passed: top-tree 4b transfer; 9,907 exhaustive n=4 "
        "support families; 10,395-tree perfect-height witness; cluster cut-cover "
        "audits; OR-path/private-tree regressions; zero failures."
    )


if __name__ == "__main__":
    main()
