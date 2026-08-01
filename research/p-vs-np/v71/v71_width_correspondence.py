#!/usr/bin/env python3
"""V71 support-hypergraph width correspondence and finite validation.

No third-party packages are used. Hyperedges are tuples of integer variables.
"""
from __future__ import annotations

import itertools
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent


def normalize(edges):
    answer = tuple(tuple(sorted(set(edge))) for edge in edges)
    if any(not edge for edge in answer):
        raise ValueError("empty supports are excluded")
    return answer


def frontier(edges, processed):
    edges = normalize(edges)
    processed = set(processed)
    left, right = set(), set()
    for index, edge in enumerate(edges):
        (left if index in processed else right).update(edge)
    return left & right


def linear_width(edges, order):
    edges = normalize(edges)
    processed = set()
    width = 0
    profile = []
    for index in order:
        processed.add(index)
        value = len(frontier(edges, processed))
        profile.append(value)
        width = max(width, value)
    return width, profile


def exact_linear_width(edges):
    edges = normalize(edges)
    best = None
    best_order = None
    for order in itertools.permutations(range(len(edges))):
        value, _ = linear_width(edges, order)
        if best is None or value < best:
            best, best_order = value, order
    return int(best or 0), list(best_order or ())


def bags_from_edge_order(edges, order):
    """Construct the primal path decomposition B_i=F(S_{i-1}) union e_i."""
    edges = normalize(edges)
    processed = set()
    bags = []
    for index in order:
        bags.append(tuple(sorted(frontier(edges, processed) | set(edges[index]))))
        processed.add(index)
    return bags


def validate_path_decomposition(edges, bags):
    edges = normalize(edges)
    bags = [set(bag) for bag in bags]
    if not bags:
        return not edges
    if any(not any(set(edge) <= bag for bag in bags) for edge in edges):
        return False
    vertices = sorted({v for edge in edges for v in edge})
    for vertex in vertices:
        positions = [i for i, bag in enumerate(bags) if vertex in bag]
        if positions and positions != list(range(min(positions), max(positions) + 1)):
            return False
    return True


def primal_graph(edges):
    edges = normalize(edges)
    vertices = sorted({v for edge in edges for v in edge})
    adjacency = {v: set() for v in vertices}
    for edge in edges:
        for u, v in itertools.combinations(edge, 2):
            adjacency[u].add(v)
            adjacency[v].add(u)
    return adjacency


def vertex_separation(adjacency, order):
    prefix = set()
    width = 0
    all_vertices = set(adjacency)
    for vertex in order:
        prefix.add(vertex)
        suffix = all_vertices - prefix
        boundary = {u for u in prefix if adjacency[u] & suffix}
        width = max(width, len(boundary))
    return width


def exact_primal_pathwidth(edges):
    adjacency = primal_graph(edges)
    vertices = tuple(sorted(adjacency))
    if not vertices:
        return 0, []
    best = None
    best_order = None
    for order in itertools.permutations(vertices):
        value = vertex_separation(adjacency, order)
        if best is None or value < best:
            best, best_order = value, order
    return int(best or 0), list(best_order or ())


def order_from_path_decomposition(edges, bags):
    """Sort hyperedges by the rightmost bag containing the entire support."""
    edges = normalize(edges)
    bag_sets = [set(bag) for bag in bags]
    rightmost = []
    for index, edge in enumerate(edges):
        positions = [i for i, bag in enumerate(bag_sets) if set(edge) <= bag]
        if not positions:
            raise ValueError(f"support {edge} is not covered")
        rightmost.append((max(positions), index))
    return [index for _, index in sorted(rightmost)]


def affine_subspace_count(b):
    def gaussian(n, k):
        if k < 0 or k > n:
            return 0
        numerator = denominator = 1
        for i in range(k):
            numerator *= 2 ** (n - i) - 1
            denominator *= 2 ** (k - i) - 1
        return numerator // denominator
    return sum(2 ** (b - d) * gaussian(b, d) for d in range(b + 1))


def validate_instance(edges):
    edges = normalize(edges)
    rank = max(map(len, edges), default=0)
    q_star, q_order = exact_linear_width(edges)
    pathwidth, vertex_order = exact_primal_pathwidth(edges)
    bags = bags_from_edge_order(edges, q_order)
    assert validate_path_decomposition(edges, bags)
    constructed_width = max((len(bag) - 1 for bag in bags), default=0)
    assert constructed_width <= q_star + rank - 1
    path_bags = bags_from_vertex_order(primal_graph(edges), vertex_order)
    assert validate_graph_path_decomposition(primal_graph(edges), path_bags)
    induced_order = order_from_path_decomposition(edges, path_bags)
    induced_q, _ = linear_width(edges, induced_order)
    assert induced_q <= pathwidth + 1
    assert pathwidth <= q_star + rank - 1
    assert q_star <= pathwidth + 1
    return {
        "edges": [list(edge) for edge in edges],
        "rank": rank,
        "linear_branch_width": q_star,
        "linear_branch_order": q_order,
        "primal_pathwidth": pathwidth,
        "primal_vertex_order": vertex_order,
        "path_order_frontier_width": induced_q,
        "path_decomposition_bound": len(edges) * affine_subspace_count(pathwidth + 1),
    }


def bags_from_vertex_order(adjacency, order):
    """Vertex-separation layout to a path decomposition of equal width."""
    order = list(order)
    position = {v: i for i, v in enumerate(order)}
    bags = []
    for i, vertex in enumerate(order):
        active = {u for u in order[:i] if any(position[w] >= i for w in adjacency[u])}
        bags.append(tuple(sorted(active | {vertex})))
    return bags


def validate_graph_path_decomposition(adjacency, bags):
    bag_sets = [set(bag) for bag in bags]
    for u, neighbors in adjacency.items():
        if not any(u in bag for bag in bag_sets):
            return False
        for v in neighbors:
            if u < v and not any({u, v} <= bag for bag in bag_sets):
                return False
    for vertex in adjacency:
        positions = [i for i, bag in enumerate(bag_sets) if vertex in bag]
        if positions != list(range(min(positions), max(positions) + 1)):
            return False
    return True


def exhaustive_suite():
    supports = [edge for size in (1, 2, 3) for edge in itertools.combinations(range(4), size)]
    checked = 0
    maxima = {"gap_path_minus_linear": -10**9, "gap_linear_minus_path": -10**9}
    witnesses = {}
    for m in range(1, 6):
        for edges in itertools.combinations(supports, m):
            item = validate_instance(edges)
            checked += 1
            a = item["primal_pathwidth"] - item["linear_branch_width"]
            b = item["linear_branch_width"] - item["primal_pathwidth"]
            if a > maxima["gap_path_minus_linear"]:
                maxima["gap_path_minus_linear"] = a
                witnesses["path_minus_linear"] = item
            if b > maxima["gap_linear_minus_path"]:
                maxima["gap_linear_minus_path"] = b
                witnesses["linear_minus_path"] = item
    return checked, maxima, witnesses


def seeded_suite(seed=710071, samples=160):
    rng = random.Random(seed)
    checked = 0
    for _ in range(samples):
        n = 5
        supports = [edge for size in (2, 3) for edge in itertools.combinations(range(n), size)]
        m = rng.randint(2, 6)
        edges = rng.sample(supports, m)
        validate_instance(edges)
        checked += 1
    return checked


def generate_results():
    exhaustive_checked, maxima, witnesses = exhaustive_suite()
    seeded_checked = seeded_suite()
    return {
        "version": "V71",
        "status": "passed",
        "failures": 0,
        "theorems": {
            "exact_vocabulary": "support-frontier optimum equals the linear branch-width of the support hypergraph under the vertex-boundary connectivity function",
            "rank_r_pathwidth_sandwich": "q_star <= pw(primal)+1 and pw(primal) <= q_star+r-1",
            "ternary_specialization": "q_star <= pw(primal)+1 and pw(primal) <= q_star+2",
            "constructive_projected_dag_bound": "a supplied primal path decomposition of width p yields an order with G_proj <= m*A(p+1)",
            "tree_decomposition_scope": "tree decompositions yield an affine feasibility DP but do not by themselves bound the linear order parameter",
        },
        "exhaustive_hypergraphs_n4_m_le_5": exhaustive_checked,
        "seeded_hypergraphs_n5": seeded_checked,
        "seed": 710071,
        "observed_gap_maxima": maxima,
        "gap_witnesses": witnesses,
        "affine_subspace_counts": {str(i): affine_subspace_count(i) for i in range(9)},
        "scientific_status": {
            "standard_width_correspondence_proved": True,
            "constructible_pathwidth_order_proved": True,
            "bounded_treewidth_implies_bounded_linear_width": False,
            "general_polynomial_good_order_proved": False,
            "unrestricted_avoidance_algorithm_proved": False,
            "p_vs_np_route_active": False,
            "p_vs_np_resolved": False,
            "novelty_confirmed": False,
            "peer_reviewed": False,
        },
    }


def main():
    results = generate_results()
    (HERE / "RESULTS.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
    print(
        "V71 width verification passed: exact linear-branchwidth vocabulary; "
        f"{results['exhaustive_hypergraphs_n4_m_le_5']} exhaustive and "
        f"{results['seeded_hypergraphs_n5']} seeded hypergraphs; zero failures."
    )


if __name__ == "__main__":
    main()
