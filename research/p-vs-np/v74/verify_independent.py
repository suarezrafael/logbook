#!/usr/bin/env python3
"""Independent semantic audit for Laboratory V74."""
from __future__ import annotations

import itertools
import random

from or_path_family import or_path_instance, residual_width_tables
from two_fiber_model import (
    brute_preimage_counts,
    effective_truth_mask,
    find_avoided_output,
    is_affine_mask,
    make_gate,
    minimum_affine_partition,
    weighted_target_dp,
)


def independent_fiber_audit() -> int:
    checks = 0
    for base_mask in range(256):
        for flip in (0, 1):
            gate = make_gate((0, 1, 2), base_mask, flip)
            effective = effective_truth_mask(gate)
            for output_bit in (0, 1):
                selected = effective if output_bit else effective ^ 0xFF
                partition = minimum_affine_partition(selected, 3)
                union = 0
                for cell in partition:
                    assert is_affine_mask(cell, 3)
                    assert not (union & cell)
                    union |= cell
                assert union == selected
                assert len(partition) <= 3
                checks += 1
    return checks


def independent_circuit_semantics(seed: int = 741174, samples: int = 80) -> tuple[int, int]:
    rng = random.Random(seed)
    target_checks = 0
    avoidance_checks = 0
    supports = [
        (0, 1, 2),
        (0, 1, 3),
        (0, 2, 3),
        (1, 2, 3),
    ]
    for _ in range(samples):
        n = 4
        m = 5
        gates = [
            make_gate(rng.choice(supports), rng.randrange(256), rng.randrange(2))
            for _ in range(m)
        ]
        direct = brute_preimage_counts(n, gates)
        for target_integer in range(1 << m):
            target = [(target_integer >> index) & 1 for index in range(m)]
            dynamic = weighted_target_dp(n, gates, target)
            assert dynamic["preimage_count"] == direct.get(target_integer, 0)
            target_checks += 1
        avoided = find_avoided_output(n, gates)
        assert direct.get(int(avoided["target_integer"]), 0) == 0
        assert len(avoided["trace"]) == m
        avoidance_checks += 1
    return target_checks, avoidance_checks


def independent_or_path_audit(max_edges: int = 7) -> int:
    checks = 0
    for edge_count in range(1, max_edges + 1):
        n, gates, target = or_path_instance(edge_count)
        widths, _ = residual_width_tables(n, gates, target)
        brute_optimum = None
        for order in itertools.permutations(range(edge_count)):
            mask = 0
            cost = 0
            for gate_index in order:
                cost += widths[mask]
                mask |= 1 << gate_index
            brute_optimum = cost if brute_optimum is None else min(brute_optimum, cost)
        formula = 1 if edge_count == 1 else 3 * edge_count - 3
        assert brute_optimum == formula
        checks += 1
    return checks


def main() -> None:
    fiber_checks = independent_fiber_audit()
    target_checks, avoidance_checks = independent_circuit_semantics()
    path_checks = independent_or_path_audit()
    print(
        "V74 independent verification passed: "
        f"{fiber_checks} two-fiber partitions; {target_checks} direct target counts; "
        f"{avoidance_checks} constructive witnesses; {path_checks} all-order path optima; "
        "zero failures."
    )


if __name__ == "__main__":
    main()
