#!/usr/bin/env python3
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def version_number(value: str) -> int:
    assert value.startswith("V") and value[1:].isdigit()
    return int(value[1:])


def independent_profiles(supports: list[list[int]]) -> tuple[list[int], list[int], list[int]]:
    encoded = [sum(1 << x for x in support) for support in supports]
    m = len(encoded)
    full = (1 << m) - 1
    unions = [0] * (1 << m)
    for mask in range(1, 1 << m):
        bit = mask & -mask
        unions[mask] = unions[mask ^ bit] | encoded[bit.bit_length() - 1]
    lambdas = [(unions[mask] & unions[full ^ mask]).bit_count() for mask in range(1 << m)]
    deltas = [mask.bit_count() - unions[mask].bit_count() for mask in range(1 << m)]
    return unions, lambdas, deltas


def supported(curve: list[int]) -> list[tuple[int, int]]:
    answer: list[tuple[int, int]] = []
    for p, value in enumerate(curve):
        lower = Fraction(0)
        upper: Fraction | None = None
        feasible = True
        for q, other in enumerate(curve):
            if p == q:
                continue
            coefficient = q - p
            rhs = other - value
            if coefficient > 0:
                bound = Fraction(rhs, coefficient)
                upper = bound if upper is None else min(upper, bound)
            elif coefficient < 0:
                lower = max(lower, Fraction(rhs, coefficient))
            elif value > other:
                feasible = False
                break
        lower = max(lower, Fraction(0))
        if feasible and (upper is None or lower <= upper) and (upper is None or upper >= 0):
            answer.append((p, value))
    return answer


def main() -> None:
    data = json.loads((HERE / "RESULTS.json").read_text(encoding="utf-8"))
    v80 = json.loads((ROOT / "v80" / "RESULTS.json").read_text(encoding="utf-8"))
    total_checks = 0
    for name, row in data["v80_census"].items():
        supports = v80["examples"][name]["supports"]
        unions, lambdas, deltas = independent_profiles(supports)
        m = len(supports)
        full = (1 << m) - 1
        active = unions[full].bit_count()
        stretch = m - active
        curve = [10**9] * (m + 1)
        curve[0] = 0
        for mask in range(1 << m):
            complement = full ^ mask
            assert deltas[mask] + deltas[complement] == stretch - lambdas[mask]
            curve[mask.bit_count()] = min(curve[mask.bit_count()], unions[mask].bit_count())
            total_checks += 1
        assert curve == row["minimum_union_curve"]
        deficient = [(curve[p], p) for p in range(1, m + 1) if curve[p] < p]
        minimum = min(deficient)
        assert minimum[0] == row["minimum_neighborhood_hall"]["neighborhood_size"]
        assert minimum[1] == row["minimum_neighborhood_hall"]["gate_count"]
        supported_deficient = [p for p, value in supported(curve) if value < p]
        assert supported_deficient == [m]

    half = data["structured_controls"]["rank_one_half_tight"]
    assert half["stretch"] == 4
    assert half["support_branchwidth"] == 1
    assert half["balanced_low_width_census"]["theorem_guaranteed_deficiency"] == 2

    status = json.loads((ROOT / "LAB_STATUS.json").read_text(encoding="utf-8"))
    promoted = status["promoted_version"]
    candidate = status.get("candidate_version")
    assert version_number(promoted) >= 81
    if candidate is None:
        assert status["highest_directory"] == promoted
        assert status["promotion_state"] == "promoted"
    else:
        assert version_number(candidate) == version_number(promoted) + 1
        assert status["highest_directory"] == candidate
        assert status["promotion_state"] == "candidate"
    assert status["scientific_status"]["minimum_neighborhood_hall_polynomial_time"] is None
    assert status["scientific_status"]["minimum_neighborhood_hall_np_hard"] is None
    assert status["scientific_status"]["p_vs_np_resolved"] is False

    print(
        f"V81 independent verification passed: {total_checks} cut states, complete "
        "minimum-union curves, and Lagrangian support intervals remain preserved."
    )


if __name__ == "__main__":
    main()
