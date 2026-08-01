#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
import itertools
import random
from typing import Iterable, Sequence

from symbolic_prefix_circuit import (
    build_symbolic_prefix_circuit,
    caterpillar_branch_tree,
    coefficient,
    find_avoided_output_incremental,
    leaf_depths,
    prefix_count,
)

import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "v74"))
from two_fiber_model import balanced_branch_tree, brute_preimage_counts, make_gate, prefix_count as v74_prefix_count


def bits_of(value: int, width: int) -> list[int]:
    return [(int(value) >> index) & 1 for index in range(int(width))]


def brute_prefix_count(counts: Counter[int], prefix: Sequence[int], m: int) -> int:
    mask = (1 << len(prefix)) - 1
    target = sum((int(bit) & 1) << index for index, bit in enumerate(prefix))
    return sum(count for output, count in counts.items() if (output & mask) == target)


def all_prefixes(m: int) -> Iterable[list[int]]:
    for length in range(int(m) + 1):
        for value in range(1 << length):
            yield bits_of(value, length)


def exhaustive_binary_results() -> dict[str, object]:
    circuits = coefficient_checks = prefix_checks = avoidance_checks = 0
    operation_sum = operation_max = dynamic_sum = dynamic_max = 0
    cone_sum_total = 0
    for masks in itertools.product(range(16), repeat=3):
        gates = [make_gate([0, 1], mask) for mask in masks]
        model = build_symbolic_prefix_circuit(2, gates)
        counts = brute_preimage_counts(2, gates)
        assert model["circuit"].evaluate(model["root"]) == 4
        for output in range(8):
            assert coefficient(model, bits_of(output, 3)) == counts.get(output, 0)
            coefficient_checks += 1
        for prefix in all_prefixes(3):
            expected = brute_prefix_count(counts, prefix, 3)
            assert prefix_count(model, prefix) == expected
            assert v74_prefix_count(2, gates, prefix, model["tree"]) == expected
            prefix_checks += 1
        avoided = find_avoided_output_incremental(model)
        assert counts.get(avoided["target_integer"], 0) == 0
        assert avoided["dynamic_reevaluations"] <= 2 * model["dependency_cone_sum"]
        avoidance_checks += 1
        circuits += 1
        operations = int(model["arithmetic_operations"])
        dynamic = int(avoided["dynamic_reevaluations"])
        operation_sum += operations
        operation_max = max(operation_max, operations)
        dynamic_sum += dynamic
        dynamic_max = max(dynamic_max, dynamic)
        cone_sum_total += int(model["dependency_cone_sum"])
    return {
        "circuits": circuits,
        "coefficient_checks": coefficient_checks,
        "prefix_checks": prefix_checks,
        "avoidance_constructions": avoidance_checks,
        "arithmetic_operations_sum": operation_sum,
        "arithmetic_operations_max": operation_max,
        "dynamic_reevaluations_sum": dynamic_sum,
        "dynamic_reevaluations_max": dynamic_max,
        "dependency_cone_sum_total": cone_sum_total,
    }


def random_gate(rng: random.Random, n: int) -> dict[str, object]:
    arity = rng.randint(1, 3)
    support = sorted(rng.sample(range(n), arity))
    truth_mask = rng.randrange(1 << (1 << arity))
    return make_gate(support, truth_mask, rng.randrange(2))


def seeded_ternary_results(seed: int = 750075, circuit_count: int = 48) -> dict[str, object]:
    rng = random.Random(seed)
    coefficient_checks = prefix_checks = avoidance_checks = 0
    balanced_operation_sum = caterpillar_operation_sum = 0
    balanced_dynamic_sum = caterpillar_dynamic_sum = 0
    balanced_cone_sum = caterpillar_cone_sum = 0
    representative: dict[str, object] | None = None
    for circuit_index in range(circuit_count):
        n, m = 5, 6
        gates = [random_gate(rng, n) for _ in range(m)]
        counts = brute_preimage_counts(n, gates)
        balanced = build_symbolic_prefix_circuit(n, gates, balanced_branch_tree(range(m)))
        caterpillar = build_symbolic_prefix_circuit(n, gates, caterpillar_branch_tree(range(m)))
        for output in range(1 << m):
            bits = bits_of(output, m)
            expected = counts.get(output, 0)
            assert coefficient(balanced, bits) == expected
            assert coefficient(caterpillar, bits) == expected
            coefficient_checks += 2
        for prefix in all_prefixes(m):
            expected = brute_prefix_count(counts, prefix, m)
            assert prefix_count(balanced, prefix) == expected
            assert prefix_count(caterpillar, prefix) == expected
            assert v74_prefix_count(n, gates, prefix, balanced["tree"]) == expected
            assert v74_prefix_count(n, gates, prefix, caterpillar["tree"]) == expected
            prefix_checks += 2
        avoided_balanced = find_avoided_output_incremental(balanced)
        avoided_caterpillar = find_avoided_output_incremental(caterpillar)
        assert counts.get(avoided_balanced["target_integer"], 0) == 0
        assert counts.get(avoided_caterpillar["target_integer"], 0) == 0
        assert avoided_balanced["dynamic_reevaluations"] <= 2 * balanced["dependency_cone_sum"]
        assert avoided_caterpillar["dynamic_reevaluations"] <= 2 * caterpillar["dependency_cone_sum"]
        avoidance_checks += 2
        balanced_operation_sum += int(balanced["arithmetic_operations"])
        caterpillar_operation_sum += int(caterpillar["arithmetic_operations"])
        balanced_dynamic_sum += int(avoided_balanced["dynamic_reevaluations"])
        caterpillar_dynamic_sum += int(avoided_caterpillar["dynamic_reevaluations"])
        balanced_cone_sum += int(balanced["dependency_cone_sum"])
        caterpillar_cone_sum += int(caterpillar["dependency_cone_sum"])
        if circuit_index == 0:
            representative = {
                "gates": gates,
                "output_counts": [counts.get(output, 0) for output in range(1 << m)],
                "balanced": {
                    "boundary_width": balanced["boundary_width"],
                    "arithmetic_operations": balanced["arithmetic_operations"],
                    "total_nodes": balanced["total_nodes"],
                    "external_path_length": balanced["external_path_length"],
                    "dependency_cone_sum": balanced["dependency_cone_sum"],
                    "avoided_output": avoided_balanced["target_integer"],
                    "target_bits": avoided_balanced["target_bits"],
                    "dynamic_reevaluations": avoided_balanced["dynamic_reevaluations"],
                },
                "caterpillar": {
                    "boundary_width": caterpillar["boundary_width"],
                    "arithmetic_operations": caterpillar["arithmetic_operations"],
                    "total_nodes": caterpillar["total_nodes"],
                    "external_path_length": caterpillar["external_path_length"],
                    "dependency_cone_sum": caterpillar["dependency_cone_sum"],
                    "avoided_output": avoided_caterpillar["target_integer"],
                    "target_bits": avoided_caterpillar["target_bits"],
                    "dynamic_reevaluations": avoided_caterpillar["dynamic_reevaluations"],
                },
            }
    assert representative is not None
    return {
        "seed": seed,
        "circuits": circuit_count,
        "coefficient_checks": coefficient_checks,
        "prefix_checks": prefix_checks,
        "avoidance_constructions": avoidance_checks,
        "balanced_arithmetic_operations_sum": balanced_operation_sum,
        "caterpillar_arithmetic_operations_sum": caterpillar_operation_sum,
        "balanced_dynamic_reevaluations_sum": balanced_dynamic_sum,
        "caterpillar_dynamic_reevaluations_sum": caterpillar_dynamic_sum,
        "balanced_dependency_cone_sum": balanced_cone_sum,
        "caterpillar_dependency_cone_sum": caterpillar_cone_sum,
        "representative": representative,
    }


def tree_shape_results() -> dict[str, object]:
    rows = []
    for m in (2, 4, 8, 16, 32, 64):
        balanced = leaf_depths(balanced_branch_tree(range(m)))
        caterpillar = leaf_depths(caterpillar_branch_tree(range(m)))
        rows.append(
            {
                "m": m,
                "balanced_height": max(balanced.values()),
                "balanced_external_path_length": sum(balanced.values()),
                "caterpillar_height": max(caterpillar.values()),
                "caterpillar_external_path_length": sum(caterpillar.values()),
            }
        )
    assert rows[-1] == {
        "m": 64,
        "balanced_height": 6,
        "balanced_external_path_length": 384,
        "caterpillar_height": 63,
        "caterpillar_external_path_length": 2079,
    }
    return {"instances": rows}


def generate_results() -> dict[str, object]:
    exhaustive = exhaustive_binary_results()
    seeded = seeded_ternary_results()
    shapes = tree_shape_results()
    return {
        "version": "V75",
        "status": "passed",
        "failures": 0,
        "exhaustive_binary_circuits": exhaustive,
        "seeded_ternary_circuits": seeded,
        "tree_shapes": shapes,
        "theorem_status": {
            "paired_generating_polynomial_exact": True,
            "monotone_arithmetic_translation_exact": True,
            "arithmetic_size_O_m_A_b_squared": True,
            "incremental_bound_depth_sensitive": True,
            "balanced_supplied_tree_bound_O_m_log_m_A_b_squared": True,
            "arbitrary_supplied_tree_improvement": False,
            "automatic_balancing_without_width_loss": False,
            "unrestricted_nc0_3_avoid_solved": False,
            "p_vs_np_resolved": False,
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(generate_results(), indent=2, sort_keys=True))
