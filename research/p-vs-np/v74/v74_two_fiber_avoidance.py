#!/usr/bin/env python3
"""Deterministic result generator for Laboratory V74."""
from __future__ import annotations

import itertools
import json
import random
from pathlib import Path

from or_path_family import endpoint_order_profile, verify_all_order_lower_bound
from two_fiber_model import (
    affine_cell_masks,
    brute_preimage_counts,
    effective_truth_mask,
    evaluate_gate,
    fiber_mask,
    find_avoided_output,
    make_gate,
    minimum_affine_partition,
    weighted_target_dp,
)

HERE = Path(__file__).resolve().parent


def affine_catalogue_audit() -> dict[str, object]:
    counts = {str(arity): len(affine_cell_masks(arity)) for arity in (1, 2, 3)}
    partition_histogram: dict[str, int] = {}
    three_cell_masks: list[int] = []
    exact_fiber_checks = 0
    for mask in range(256):
        partition = minimum_affine_partition(mask, 3)
        size = len(partition)
        partition_histogram[str(size)] = partition_histogram.get(str(size), 0) + 1
        if size == 3:
            three_cell_masks.append(mask)
        union = 0
        for cell in partition:
            if union & cell:
                raise AssertionError("minimum partition cells must be disjoint")
            union |= cell
        if union != mask:
            raise AssertionError((mask, partition, union))
        exact_fiber_checks += 1
    if max(map(int, partition_histogram)) != 3:
        raise AssertionError(partition_histogram)
    expected_worst = [127, 191, 223, 239, 247, 251, 253, 254]
    if three_cell_masks != expected_worst:
        raise AssertionError((three_cell_masks, expected_worst))
    return {
        "affine_cells_by_arity": counts,
        "ternary_subset_partition_histogram": partition_histogram,
        "maximum_cells_per_ternary_fiber": 3,
        "worst_case_fiber_masks": three_cell_masks,
        "exact_ternary_subset_checks": exact_fiber_checks,
    }


def exhaustive_binary_circuit_audit() -> dict[str, int]:
    circuits = 0
    target_checks = 0
    avoidance_checks = 0
    prefix_partition_checks = 0
    maximum_states = 0
    for masks in itertools.product(range(16), repeat=3):
        gates = [make_gate((0, 1), mask) for mask in masks]
        brute = brute_preimage_counts(2, gates)
        for target_integer in range(8):
            target = [(target_integer >> index) & 1 for index in range(3)]
            dynamic = weighted_target_dp(2, gates, target)
            expected = brute.get(target_integer, 0)
            if dynamic["preimage_count"] != expected:
                raise AssertionError((masks, target_integer, dynamic, brute))
            maximum_states = max(
                maximum_states,
                max(record["state_count"] for record in dynamic["records"]),
            )
            target_checks += 1
        avoided = find_avoided_output(2, gates)
        if brute.get(int(avoided["target_integer"]), 0) != 0:
            raise AssertionError((masks, avoided, brute))
        for step in avoided["trace"]:
            if step["count_zero"] + step["count_one"] < step["chosen_count"]:
                raise AssertionError(step)
            prefix_partition_checks += 1
        avoidance_checks += 1
        circuits += 1
    return {
        "circuits": circuits,
        "target_checks": target_checks,
        "avoidance_constructions": avoidance_checks,
        "prefix_partition_checks": prefix_partition_checks,
        "maximum_residual_states_observed": maximum_states,
    }


def polarity_audit() -> dict[str, int]:
    checks = 0
    for mask in range(256):
        gate = make_gate((0, 1, 2), mask, output_flip=1)
        if effective_truth_mask(gate) != (mask ^ 0xFF):
            raise AssertionError(mask)
        if fiber_mask(gate, 0) != mask:
            raise AssertionError(mask)
        if fiber_mask(gate, 1) != (mask ^ 0xFF):
            raise AssertionError(mask)
        for assignment in range(8):
            if evaluate_gate(gate, assignment) != (1 - ((mask >> assignment) & 1)):
                raise AssertionError((mask, assignment))
            checks += 1
    return {"flipped_truth_table_point_checks": checks}


def seeded_ternary_circuit_audit(seed: int = 740074, samples: int = 96) -> dict[str, int]:
    rng = random.Random(seed)
    target_checks = 0
    avoidance_checks = 0
    maximum_states = 0
    for _ in range(samples):
        n = 3
        m = 4
        gates = [
            make_gate((0, 1, 2), rng.randrange(256), rng.randrange(2))
            for _ in range(m)
        ]
        brute = brute_preimage_counts(n, gates)
        for target_integer in range(1 << m):
            target = [(target_integer >> index) & 1 for index in range(m)]
            dynamic = weighted_target_dp(n, gates, target)
            if dynamic["preimage_count"] != brute.get(target_integer, 0):
                raise AssertionError((target_integer, dynamic, brute))
            maximum_states = max(
                maximum_states,
                max(record["state_count"] for record in dynamic["records"]),
            )
            target_checks += 1
        avoided = find_avoided_output(n, gates)
        if brute.get(int(avoided["target_integer"]), 0) != 0:
            raise AssertionError((avoided, brute))
        avoidance_checks += 1
    return {
        "seed": seed,
        "circuits": samples,
        "target_checks": target_checks,
        "avoidance_constructions": avoidance_checks,
        "maximum_residual_states_observed": maximum_states,
    }


def or_path_audit(max_edges: int = 9) -> dict[str, object]:
    exact = []
    for edge_count in range(1, max_edges + 1):
        profile = endpoint_order_profile(edge_count)
        lower = verify_all_order_lower_bound(edge_count)
        if profile["G_proj"] != lower["Gstar"]:
            raise AssertionError((profile, lower))
        exact.append({**profile, **lower})
    return {
        "gate_mask": "0b1110",
        "selected_output": 1,
        "primal_graph": "path",
        "primal_treewidth": 1,
        "exact_formula": "G*_proj=1 for m=1 and G*_proj=3m-3 for m>=2",
        "checked_edge_counts": [1, max_edges],
        "instances": exact,
    }


def generate_results() -> dict[str, object]:
    catalogue = affine_catalogue_audit()
    exhaustive = exhaustive_binary_circuit_audit()
    polarity = polarity_audit()
    ternary = seeded_ternary_circuit_audit()
    or_path = or_path_audit()
    return {
        "version": "V74",
        "status": "passed",
        "failures": 0,
        "theorems": {
            "two_fiber_model": "truth_mask plus output_flip represents both exact gate fibers",
            "ternary_affine_partition": (
                "every subset of F2^3 is a disjoint union of at most three affine cells; "
                "seven-point fibers require three"
            ),
            "weighted_branch_counting": (
                "a supplied branch decomposition computes exact target preimage counts "
                "with at most A(b) residual keys per node"
            ),
            "constructive_avoidance": (
                "for m>n, m rounds of exact prefix counting construct an output with zero preimages"
            ),
            "parameterized_running_time": (
                "O(m^2 A(b)^2 poly(n,m)) for a supplied width-b branch decomposition"
            ),
            "bicriteria_price_bound": (
                "for prefix-feasible systems, C_B/G*_proj <= A(B); the bound is width-dependent, not rank-only"
            ),
            "bounded_treewidth_growth": (
                "the OR=1 path family has primal treewidth one and exact G*_proj=3m-3 for m>=2"
            ),
        },
        "affine_catalogue": catalogue,
        "exhaustive_binary_circuits": exhaustive,
        "polarity": polarity,
        "seeded_ternary_circuits": ternary,
        "or_path_family": or_path,
        "scientific_status": {
            "exact_both_fibers_encoded": True,
            "target_preimage_count_exact": True,
            "bounded_branchwidth_target_search_proved": True,
            "unrestricted_nc0_3_avoid_solved": False,
            "branch_decomposition_found_in_polynomial_time": False,
            "all_orders_superpolynomial_lower_bound_proved": False,
            "standard_model_simulation_proved": False,
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
        "V74 verification passed: 256 ternary fiber partitions; 4,096 exhaustive "
        "binary circuits and 32,768 target counts; 96 ternary circuits; exact "
        "prefix avoidance; OR-path G*=3m-3; zero failures."
    )


if __name__ == "__main__":
    main()
