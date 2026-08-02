#!/usr/bin/env python3
"""Exact V82 census for Hall-neighborhood minima and transversal girth."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Sequence

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

Support = tuple[int, ...]

DEGREE_TWO_CONTROLS: dict[str, dict[str, object]] = {
    "theta_three_parallel_edges": {
        "n": 2,
        "topology": "theta",
        "supports": ((0, 1), (0, 1), (0, 1)),
    },
    "tight_handcuff_two_loops": {
        "n": 1,
        "topology": "tight_handcuff",
        "supports": ((0,), (0,)),
    },
    "loose_handcuff_two_loops_bridge": {
        "n": 2,
        "topology": "loose_handcuff",
        "supports": ((0,), (0, 1), (1,)),
    },
}


def support_masks(supports: Sequence[Support]) -> tuple[int, ...]:
    return tuple(sum(1 << variable for variable in support) for support in supports)


def neighborhood_profiles(supports: Sequence[Support]) -> list[int]:
    encoded = support_masks(supports)
    unions = [0] * (1 << len(encoded))
    for mask in range(1, 1 << len(encoded)):
        bit = mask & -mask
        unions[mask] = unions[mask ^ bit] | encoded[bit.bit_length() - 1]
    return unions


def matching_rank(supports: Sequence[Support], mask: int) -> int:
    variable_count = 1 + max(
        (variable for support in supports for variable in support),
        default=-1,
    )
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

    rank = 0
    for gate in range(len(supports)):
        if (mask >> gate) & 1 and augment(gate, [False] * variable_count):
            rank += 1
    return rank


def is_transversal_circuit(supports: Sequence[Support], mask: int) -> bool:
    size = mask.bit_count()
    if matching_rank(supports, mask) == size:
        return False
    remaining = mask
    while remaining:
        bit = remaining & -remaining
        proper = mask ^ bit
        if matching_rank(supports, proper) < proper.bit_count():
            return False
        remaining ^= bit
    return True


def audit_family(name: str, supports: Sequence[Support], n: int) -> dict[str, object]:
    supports = tuple(tuple(map(int, support)) for support in supports)
    m = len(supports)
    full = (1 << m) - 1
    unions = neighborhood_profiles(supports)

    deficient = [
        mask
        for mask in range(1, full + 1)
        if unions[mask].bit_count() < mask.bit_count()
    ]
    if not deficient:
        raise AssertionError("V82 census expects a dependent transversal presentation")

    hstar = min(unions[mask].bit_count() for mask in deficient)
    minimizers = [
        mask for mask in deficient if unions[mask].bit_count() == hstar
    ]
    inclusion_minimal = [
        mask
        for mask in minimizers
        if not any(
            proper != mask and (proper & mask) == proper
            for proper in minimizers
        )
    ]
    circuits = [
        mask for mask in range(1, full + 1) if is_transversal_circuit(supports, mask)
    ]
    girth = min(mask.bit_count() for mask in circuits)
    girth_circuits = [mask for mask in circuits if mask.bit_count() == girth]

    def indices(mask: int) -> list[int]:
        return [index for index in range(m) if (mask >> index) & 1]

    return {
        "name": name,
        "n": n,
        "m": m,
        "maximum_left_degree": max(map(len, supports)),
        "transversal_rank": matching_rank(supports, full),
        "subset_states_checked": full + 1,
        "minimum_hall_neighborhood": hstar,
        "transversal_girth": girth,
        "hstar_equals_girth_minus_one": hstar == girth - 1,
        "hstar_minimizer_count": len(minimizers),
        "inclusion_minimal_hstar_minimizer_count": len(inclusion_minimal),
        "all_inclusion_minimal_hstar_minimizers_have_deficiency_one": all(
            mask.bit_count() - unions[mask].bit_count() == 1
            for mask in inclusion_minimal
        ),
        "girth_circuit_count": len(girth_circuits),
        "total_circuit_count": len(circuits),
        "one_inclusion_minimal_hstar_minimizer": indices(inclusion_minimal[0]),
        "one_girth_circuit": indices(girth_circuits[0]),
    }


def load_v80_examples() -> dict[str, dict[str, object]]:
    data = json.loads((ROOT / "v80" / "RESULTS.json").read_text(encoding="utf-8"))
    return data["examples"]


def build_results() -> dict[str, object]:
    v80_examples = load_v80_examples()
    census = {
        name: audit_family(
            name,
            tuple(tuple(map(int, support)) for support in example["supports"]),
            int(example["n"]),
        )
        for name, example in v80_examples.items()
    }
    controls = {
        name: {
            **audit_family(
                name,
                specification["supports"],
                int(specification["n"]),
            ),
            "bicircular_topology": specification["topology"],
        }
        for name, specification in DEGREE_TWO_CONTROLS.items()
    }
    target_ranks = sorted(row["transversal_rank"] for row in census.values())
    target_girths = sorted(row["transversal_girth"] for row in census.values())
    return {
        "laboratory": "V82",
        "scope": "literature-first transversal-girth complexity boundary",
        "theorems": {
            "hall_girth_equivalence": (
                "For every dependent transversal presentation, "
                "h*=min{|N(S)|:|N(S)|<|S|}=girth(T(G))-1."
            ),
            "minimal_minimizer_deficiency": (
                "Every inclusion-minimal h*-minimizer is a transversal circuit "
                "and has deficiency exactly one."
            ),
            "degree_two_boundary": (
                "Presentations of left degree at most two are bicircular; "
                "their girth is the length of a shortest bicycle and is "
                "polynomial-time computable from the presenting graph."
            ),
        },
        "literature_map": {
            "general_transversal_girth": {
                "status": "NP-hard",
                "verified_primary_source": (
                    "Colbourn and Elmallah, Discrete Mathematics 114 (1993), "
                    "Theorem 2.1, DOI 10.1016/0012-365X(93)90360-6"
                ),
                "reduction_source": "Clique",
                "stockmeyer_provenance": (
                    "secondary attribution only; not used as the primary citation"
                ),
            },
            "degree_two_presentations": {
                "status": "polynomial from bicircular graph representation",
                "matroid_class": "bicircular",
                "circuit_topologies": [
                    "theta",
                    "tight handcuff",
                    "loose handcuff",
                ],
                "reference_boundary": (
                    "Matthews characterization as cited in later bicircular-matroid "
                    "literature; V82 supplies the algorithmic consequence."
                ),
            },
            "parameterized_girth": {
                "source": (
                    "Panolan, Ramanujan, and Saurabh, WADS 2015, "
                    "DOI 10.1007/978-3-319-21840-3_47"
                ),
                "rank_plus_field_size_fpt_for_linear_matroids": True,
                "special_transversal_algorithms_avoid_exponential_field_size": True,
                "useful_for_target_regime": False,
                "reason": (
                    "The audited target presentations have transversal rank n, "
                    "and their girths also grow with n; the audited parameters "
                    "are not bounded in the target regime."
                ),
                "audited_target_ranks": target_ranks,
                "audited_target_girths": target_girths,
            },
            "left_degree_three": {
                "polynomial_time_known_from_located_sources": False,
                "np_hardness_known_from_located_sources": False,
                "status": "open within the V82 audit",
            },
        },
        "route_decision": {
            "next_exact_question": (
                "transversal girth / minimum Hall neighborhood for left degree at most three"
            ),
            "preferred_first_attack": (
                "hardness gadgets replacing the high-degree incidence used by the "
                "general Clique reduction"
            ),
            "algorithmic_route_remains_valid": True,
            "stop_rule": (
                "After three focused mathematical iterations without a closed "
                "degree-three reduction or algorithm, promote the extended structural "
                "census and switch the next laboratory to explicit-obstruction tests."
            ),
            "fallback_census": [
                "sunflower core and petal profiles",
                "affine-cell rank or a precise replacement invariant",
                "G*_proj all-orders growth",
                "counterexamples to proposed monotone inequalities",
            ],
            "apc1_priority": (
                "deferred; V56 affine certificate only after a demonstrated blocker"
            ),
        },
        "v80_rank_three_census": census,
        "degree_two_controls": controls,
        "scientific_status": {
            "degree_three_transversal_girth_polynomial_time": None,
            "degree_three_transversal_girth_np_hard": None,
            "deterministic_FP_NP_target_solved": False,
            "all_orders_obstruction_proved": False,
            "p_vs_np_resolved": False,
            "p_vs_np_route_active": False,
            "novelty_confirmed": False,
            "peer_reviewed": False,
        },
    }


if __name__ == "__main__":
    print(json.dumps(build_results(), indent=2, sort_keys=True))
