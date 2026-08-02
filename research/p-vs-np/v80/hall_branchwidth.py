#!/usr/bin/env python3
"""Exact finite audits for the V80 Hall/branchwidth dichotomy."""
from __future__ import annotations

from itertools import combinations
from math import ceil
from typing import Sequence

Support = tuple[int, ...]

EXAMPLES: dict[str, dict[str, object]] = {
    "seven_variables": {
        "n": 7, "search_seed": 130, "search_trials": 1000,
        "supports": (
            (0, 5, 6), (1, 3, 6), (0, 2, 4), (0, 4, 6),
            (2, 3, 5), (0, 3, 6), (0, 1, 2), (3, 4, 5),
            (2, 4, 5), (1, 5, 6), (2, 4, 6),
        ),
    },
    "eight_variables": {
        "n": 8, "search_seed": 131, "search_trials": 1000,
        "supports": (
            (0, 1, 3), (0, 1, 4), (1, 2, 6), (2, 4, 7),
            (2, 3, 5), (0, 3, 7), (0, 3, 5), (1, 3, 6),
            (1, 2, 5), (0, 2, 4), (2, 6, 7), (0, 4, 7),
        ),
    },
    "nine_variables": {
        "n": 9, "search_seed": 132, "search_trials": 1000,
        "supports": (
            (2, 3, 7), (2, 5, 7), (4, 5, 8), (0, 3, 6),
            (0, 5, 8), (3, 4, 7), (1, 2, 6), (1, 2, 4),
            (2, 6, 7), (5, 7, 8), (3, 4, 6), (1, 4, 8),
            (0, 1, 5), (0, 5, 6),
        ),
    },
}


def support_masks(supports: Sequence[Support]) -> tuple[int, ...]:
    return tuple(sum(1 << variable for variable in support) for support in supports)


def subset_profiles(supports: Sequence[Support]) -> tuple[list[int], list[int]]:
    masks = support_masks(supports)
    gate_count = len(masks)
    full = (1 << gate_count) - 1
    unions = [0] * (1 << gate_count)
    for mask in range(1, 1 << gate_count):
        bit = mask & -mask
        index = bit.bit_length() - 1
        unions[mask] = unions[mask ^ bit] | masks[index]
    connectivity = [
        (unions[mask] & unions[full ^ mask]).bit_count()
        for mask in range(1 << gate_count)
    ]
    return unions, connectivity


def minimum_hall_witness(supports: Sequence[Support]) -> tuple[int, tuple[int, ...], int]:
    unions, _ = subset_profiles(supports)
    best_size: int | None = None
    best_mask = 0
    for mask in range(1, 1 << len(supports)):
        size = mask.bit_count()
        if unions[mask].bit_count() < size and (best_size is None or size < best_size):
            best_size = size
            best_mask = mask
    if best_size is None:
        raise AssertionError("m>n example unexpectedly has no Hall witness")
    witness = tuple(index for index in range(len(supports)) if (best_mask >> index) & 1)
    return best_size, witness, unions[best_mask].bit_count()


def exact_support_branchwidth(supports: Sequence[Support]) -> int:
    _, connectivity = subset_profiles(supports)
    gate_count = len(supports)
    dynamic = [0] * (1 << gate_count)
    for index in range(gate_count):
        dynamic[1 << index] = connectivity[1 << index]
    for size in range(2, gate_count + 1):
        for indices in combinations(range(gate_count), size):
            mask = sum(1 << index for index in indices)
            anchor = mask & -mask
            best = 10**9
            subset = (mask - 1) & mask
            while subset:
                if subset & anchor and subset != mask:
                    complement = mask ^ subset
                    best = min(best, max(connectivity[mask], dynamic[subset], dynamic[complement]))
                subset = (subset - 1) & mask
            dynamic[mask] = best
    return dynamic[-1]


def maximum_matching_hall_witness(
    supports: Sequence[Support], variable_count: int
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    match_right = [-1] * variable_count

    def augment(gate: int, seen: list[bool]) -> bool:
        for variable in supports[gate]:
            if seen[variable]:
                continue
            seen[variable] = True
            matched_gate = match_right[variable]
            if matched_gate == -1 or augment(matched_gate, seen):
                match_right[variable] = gate
                return True
        return False

    for gate in range(len(supports)):
        augment(gate, [False] * variable_count)

    match_left = [-1] * len(supports)
    for variable, gate in enumerate(match_right):
        if gate != -1:
            match_left[gate] = variable

    left_reached = {gate for gate, variable in enumerate(match_left) if variable == -1}
    right_reached: set[int] = set()
    queue = list(left_reached)
    while queue:
        gate = queue.pop()
        for variable in supports[gate]:
            if match_left[gate] == variable or variable in right_reached:
                continue
            right_reached.add(variable)
            matched_gate = match_right[variable]
            if matched_gate != -1 and matched_gate not in left_reached:
                left_reached.add(matched_gate)
                queue.append(matched_gate)

    neighborhood = {variable for gate in left_reached for variable in supports[gate]}
    if neighborhood != right_reached or len(left_reached) <= len(neighborhood):
        raise AssertionError("alternating matching witness is not Hall deficient")
    return tuple(sorted(left_reached)), tuple(sorted(neighborhood))


def balanced_cut_audit(supports: Sequence[Support], active_variables: int) -> dict[str, object]:
    unions, connectivity = subset_profiles(supports)
    gate_count = len(supports)
    full = (1 << gate_count) - 1
    lower = ceil(gate_count / 3)
    upper = (2 * gate_count) // 3
    deficient = 0
    both_expanding = 0
    minimum_connectivity: int | None = None
    identity_checks = 0
    for mask in range(1, full):
        complement = full ^ mask
        identity_checks += 1
        assert connectivity[mask] == (
            unions[mask].bit_count() + unions[complement].bit_count() - active_variables
        )
        size = mask.bit_count()
        if lower <= size <= upper:
            left_expands = unions[mask].bit_count() >= size
            right_expands = unions[complement].bit_count() >= gate_count - size
            if not left_expands:
                deficient += 1
            if left_expands and right_expands:
                both_expanding += 1
                value = connectivity[mask]
                minimum_connectivity = value if minimum_connectivity is None else min(
                    minimum_connectivity, value
                )
                assert value >= gate_count - active_variables
    return {
        "balanced_range": [lower, upper],
        "balanced_deficient_subset_count": deficient,
        "balanced_cuts_with_both_sides_hall_expanding": both_expanding,
        "minimum_lambda_among_both_expanding_balanced_cuts": minimum_connectivity or 0,
        "cut_identity_checks": identity_checks,
    }


def local_expansion_union_bound() -> dict[str, object]:
    return {
        "support_rank": 3,
        "target_stretch": "m=n+ceil(n^(2/3))",
        "local_expansion_constant": "1/(16e^2)",
        "bad_event_geometric_base": [1, 8],
        "bad_event_sum_upper_bound": [8, 49],
        "conclusion": (
            "For all sufficiently large n, a rank-at-most-three support family "
            "exists with no Hall-deficient gate set of size at most n/(16e^2)."
        ),
    }


def audit_example(name: str, specification: dict[str, object]) -> dict[str, object]:
    variable_count = int(specification["n"])
    supports = tuple(tuple(map(int, support)) for support in specification["supports"])
    gate_count = len(supports)
    assert all(1 <= len(support) <= 3 for support in supports)
    assert gate_count == variable_count + ceil(variable_count ** (2 / 3))
    active = len({variable for support in supports for variable in support})
    assert active == variable_count

    minimum_size, minimum_witness, neighborhood_size = minimum_hall_witness(supports)
    matching_witness, matching_neighborhood = maximum_matching_hall_witness(
        supports, variable_count
    )
    return {
        "name": name,
        "n": variable_count,
        "m": gate_count,
        "stretch": gate_count - variable_count,
        "search_seed": int(specification["search_seed"]),
        "search_trials": int(specification["search_trials"]),
        "supports": [list(support) for support in supports],
        "minimum_hall_deficient_gate_count": minimum_size,
        "minimum_hall_neighborhood_size": neighborhood_size,
        "one_minimum_hall_witness": list(minimum_witness),
        "matching_hall_witness_gate_count": len(matching_witness),
        "matching_hall_neighborhood_size": len(matching_neighborhood),
        "support_branchwidth": exact_support_branchwidth(supports),
        **balanced_cut_audit(supports, active),
    }


def build_results() -> dict[str, object]:
    barrier = local_expansion_union_bound()
    return {
        "laboratory": "V80",
        "scope": "high-width Hall/branchwidth dichotomy audit",
        "theorems": {
            "hall_projection": (
                "A Hall-deficient gate set proves an avoided projection exists; "
                "deterministic construction is polynomial when its neighborhood is O(log n)."
            ),
            "randomized_np_oracle": (
                "For deficiency d>=1, uniform projection sampling plus an NP range-membership "
                "query succeeds with probability at least 1-2^{-d} per trial."
            ),
            "balanced_cut_inequality": (
                "lambda(S)=|N(S)|+|N(M\\S)|-|N(M)|; if both sides Hall-expand, "
                "lambda(S)>=m-|N(M)|."
            ),
            "local_expansion_barrier": barrier["conclusion"],
        },
        "algorithmic_boundary": {
            "global_hall_deficiency_is_automatic_when_m_gt_n": True,
            "counting_alone_implies_deterministic_FP_NP": False,
            "small_neighborhood_enumeration_is_deterministic_polynomial": True,
            "arbitrary_hall_witness_gives_randomized_expected_polynomial_with_NP_oracle": True,
        },
        "probabilistic_barrier": barrier,
        "examples": {
            name: audit_example(name, specification)
            for name, specification in EXAMPLES.items()
        },
        "scientific_status": {
            "p_vs_np_resolved": False,
            "p_vs_np_route_active": False,
            "unrestricted_NC0_3_avoid_solved": False,
            "deterministic_FP_NP_target_solved": False,
            "novelty_confirmed": False,
            "peer_reviewed": False,
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(build_results(), indent=2, sort_keys=True))
