#!/usr/bin/env python3
"""V81 exact census for support-width/deficiency conservation and Minimum p-Union."""
from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from math import ceil, floor
from typing import Sequence

Support = tuple[int, ...]

V80_EXAMPLES: dict[str, tuple[Support, ...]] = {
    "seven_variables": (
        (0, 5, 6), (1, 3, 6), (0, 2, 4), (0, 4, 6),
        (2, 3, 5), (0, 3, 6), (0, 1, 2), (3, 4, 5),
        (2, 4, 5), (1, 5, 6), (2, 4, 6),
    ),
    "eight_variables": (
        (0, 1, 3), (0, 1, 4), (1, 2, 6), (2, 4, 7),
        (2, 3, 5), (0, 3, 7), (0, 3, 5), (1, 3, 6),
        (1, 2, 5), (0, 2, 4), (2, 6, 7), (0, 4, 7),
    ),
    "nine_variables": (
        (2, 3, 7), (2, 5, 7), (4, 5, 8), (0, 3, 6),
        (0, 5, 8), (3, 4, 7), (1, 2, 6), (1, 2, 4),
        (2, 6, 7), (5, 7, 8), (3, 4, 6), (1, 4, 8),
        (0, 1, 5), (0, 5, 6),
    ),
}

STRUCTURED_EXAMPLES: dict[str, tuple[Support, ...]] = {
    "rank_one_concentrated": tuple([(0,)] * 6 + [(i,) for i in range(1, 9)]),
    "rank_one_half_tight": ((0,), (0,), (0,), (2,), (1,), (1,), (1,), (3,)),
}


def support_masks(supports: Sequence[Support]) -> tuple[int, ...]:
    return tuple(sum(1 << variable for variable in support) for support in supports)


def subset_profiles(supports: Sequence[Support]) -> tuple[list[int], list[int], list[int]]:
    encoded = support_masks(supports)
    m = len(encoded)
    full = (1 << m) - 1
    unions = [0] * (1 << m)
    connectivity = [0] * (1 << m)
    deficiency = [0] * (1 << m)
    for mask in range(1, 1 << m):
        low = mask & -mask
        index = low.bit_length() - 1
        unions[mask] = unions[mask ^ low] | encoded[index]
    for mask in range(1 << m):
        connectivity[mask] = (unions[mask] & unions[full ^ mask]).bit_count()
        deficiency[mask] = mask.bit_count() - unions[mask].bit_count()
    return unions, connectivity, deficiency


def exact_support_branchwidth(supports: Sequence[Support]) -> int:
    _unions, connectivity, _deficiency = subset_profiles(supports)
    m = len(supports)
    dynamic = [0] * (1 << m)
    for index in range(m):
        dynamic[1 << index] = connectivity[1 << index]
    for size in range(2, m + 1):
        for indices in combinations(range(m), size):
            mask = sum(1 << index for index in indices)
            anchor = mask & -mask
            best = 10**9
            subset = (mask - 1) & mask
            while subset:
                if subset & anchor and subset != mask:
                    best = min(
                        best,
                        max(connectivity[mask], dynamic[subset], dynamic[mask ^ subset]),
                    )
                subset = (subset - 1) & mask
            dynamic[mask] = best
    return dynamic[-1]


def minimum_union_curve(supports: Sequence[Support]) -> tuple[list[int], list[int]]:
    unions, _connectivity, _deficiency = subset_profiles(supports)
    m = len(supports)
    values = [10**9] * (m + 1)
    witnesses = [0] * (m + 1)
    values[0] = 0
    for mask in range(1, 1 << m):
        p = mask.bit_count()
        value = unions[mask].bit_count()
        if value < values[p]:
            values[p] = value
            witnesses[p] = mask
    return values, witnesses


def min_neighborhood_hall(supports: Sequence[Support]) -> tuple[int, int, int]:
    values, witnesses = minimum_union_curve(supports)
    candidates = [(values[p], p, witnesses[p]) for p in range(1, len(values)) if values[p] < p]
    if not candidates:
        raise AssertionError("m>n family has no deficient set")
    return min(candidates)


def lagrangian_supported_cardinalities(values: Sequence[int]) -> list[dict[str, object]]:
    """Return p for which U(p)-lambda*p is optimal for some lambda>=0."""
    points = [(p, int(values[p])) for p in range(len(values))]
    supported: list[dict[str, object]] = []
    for p, up in points:
        lower = Fraction(0, 1)
        upper: Fraction | None = None
        feasible = True
        for q, uq in points:
            if q == p:
                continue
            coefficient = q - p
            rhs = uq - up
            if coefficient > 0:
                bound = Fraction(rhs, coefficient)
                upper = bound if upper is None else min(upper, bound)
            elif coefficient < 0:
                lower = max(lower, Fraction(rhs, coefficient))
            elif up > uq:
                feasible = False
                break
        lower = max(lower, Fraction(0, 1))
        if feasible and (upper is None or lower <= upper) and (upper is None or upper >= 0):
            supported.append(
                {
                    "p": p,
                    "minimum_union": up,
                    "deficiency": p - up,
                    "lambda_interval": [
                        [lower.numerator, lower.denominator],
                        None if upper is None else [upper.numerator, upper.denominator],
                    ],
                }
            )
    return supported


def conservation_checks(supports: Sequence[Support]) -> int:
    unions, connectivity, deficiency = subset_profiles(supports)
    m = len(supports)
    full = (1 << m) - 1
    active = unions[full].bit_count()
    stretch = m - active
    checks = 0
    for mask in range(1 << m):
        complement = full ^ mask
        assert deficiency[mask] + deficiency[complement] == stretch - connectivity[mask]
        checks += 1
    return checks


def balanced_low_width_census(supports: Sequence[Support], width: int) -> dict[str, object]:
    unions, connectivity, deficiency = subset_profiles(supports)
    m = len(supports)
    full = (1 << m) - 1
    active = unions[full].bit_count()
    stretch = m - active
    lower = ceil(m / 3)
    upper = floor(2 * m / 3)
    records: list[tuple[int, int, int, int, int]] = []
    for mask in range(1, full):
        size = mask.bit_count()
        if lower <= size <= upper and connectivity[mask] <= width:
            complement = full ^ mask
            records.append(
                (
                    connectivity[mask],
                    deficiency[mask],
                    deficiency[complement],
                    size,
                    unions[mask].bit_count(),
                )
            )
    assert records
    guaranteed = max(0, ceil((stretch - width) / 2))
    assert all(max(left, right) >= ceil((stretch - lam) / 2) for lam, left, right, _s, _u in records)
    return {
        "balanced_range": [lower, upper],
        "low_width_balanced_cut_count": len(records),
        "theorem_guaranteed_deficiency": guaranteed,
        "minimum_observed_max_side_deficiency": min(max(r[1], r[2]) for r in records),
        "maximum_observed_max_side_deficiency": max(max(r[1], r[2]) for r in records),
        "distinct_conservation_triples": [
            list(item) for item in sorted(set((r[0], r[1], r[2]) for r in records))
        ],
    }


def family_census(name: str, supports: Sequence[Support]) -> dict[str, object]:
    unions, _connectivity, _deficiency = subset_profiles(supports)
    m = len(supports)
    active = unions[-1].bit_count()
    width = exact_support_branchwidth(supports)
    curve, witnesses = minimum_union_curve(supports)
    neighborhood, cardinality, witness = min_neighborhood_hall(supports)
    supported = lagrangian_supported_cardinalities(curve)
    deficient_supported = [row for row in supported if int(row["deficiency"]) > 0]
    return {
        "name": name,
        "n_active": active,
        "m": m,
        "stretch": m - active,
        "maximum_support_rank": max(len(support) for support in supports),
        "support_branchwidth": width,
        "conservation_checks": conservation_checks(supports),
        "minimum_union_curve": curve,
        "minimum_union_witness_masks": witnesses,
        "minimum_neighborhood_hall": {
            "neighborhood_size": neighborhood,
            "gate_count": cardinality,
            "deficiency": cardinality - neighborhood,
            "witness_mask": witness,
        },
        "lagrangian_supported_points": supported,
        "lagrangian_supported_deficient_cardinalities": [int(row["p"]) for row in deficient_supported],
        "minimum_neighborhood_witness_is_lagrangian_supported": any(
            int(row["p"]) == cardinality and int(row["minimum_union"]) == neighborhood
            for row in deficient_supported
        ),
        "balanced_low_width_census": balanced_low_width_census(supports, width),
    }


def build_results() -> dict[str, object]:
    v80 = {name: family_census(name, supports) for name, supports in V80_EXAMPLES.items()}
    structured = {name: family_census(name, supports) for name, supports in STRUCTURED_EXAMPLES.items()}

    for result in v80.values():
        assert result["minimum_neighborhood_witness_is_lagrangian_supported"] is False
        assert result["lagrangian_supported_deficient_cardinalities"] == [result["m"]]

    half_tight = structured["rank_one_half_tight"]
    assert [0, 2, 2] in half_tight["balanced_low_width_census"]["distinct_conservation_triples"]

    return {
        "laboratory": "V81",
        "scope": "deficiency conservation, exact census, and Minimum p-Union boundary",
        "theorems": {
            "deficiency_conservation": (
                "delta(S)+delta(M\\S)=stretch-lambda_C(S) for every gate cut."
            ),
            "balanced_edge_witness": (
                "Given a width-w branch decomposition, a balanced edge yields one side "
                "with deficiency at least ceil((stretch-w)/2)."
            ),
            "minimum_p_union_equivalence": (
                "If U(p)=min_{|S|=p}|N(S)|, then the minimum Hall-neighborhood is "
                "min{U(p): U(p)<p}."
            ),
            "lagrangian_limitation": (
                "Minimizing |N(S)|-lambda|S| exposes only supported points of the "
                "minimum-union curve and can miss the minimum-neighborhood Hall witness."
            ),
        },
        "v80_census": v80,
        "structured_controls": structured,
        "literature_audit": {
            "explicit_constant_degree_lossless_expanders_exist": True,
            "exact_left_degree_three_target_obtained_from_located_sources": False,
            "apc1_priority": "deferred; V56 certificate only after a demonstrated blocker",
        },
        "scientific_status": {
            "minimum_neighborhood_hall_polynomial_time": None,
            "minimum_neighborhood_hall_np_hard": None,
            "deterministic_FP_NP_target_solved": False,
            "all_orders_obstruction_proved": False,
            "p_vs_np_route_active": False,
            "p_vs_np_resolved": False,
            "novelty_confirmed": False,
            "peer_reviewed": False,
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(build_results(), indent=2, sort_keys=True))
