#!/usr/bin/env python3
"""Independent V88 audit without importing the primary implementations."""
from __future__ import annotations

import json
import random
from collections import Counter
from itertools import combinations, product
from math import ceil, comb, log
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def target_matrix(k: int, m: int, bits: int) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple((bits >> (row * m + output)) & 1 for output in range(m))
        for row in range(k)
    )


def direct_consistent(
    supports: tuple[tuple[int, ...], ...],
    targets: tuple[tuple[int, ...], ...],
    n: int,
) -> bool:
    k = len(targets)
    for tail in product(range(1 << n), repeat=k - 1):
        witnesses = (0,) + tail
        valid = True
        for output, support in enumerate(supports):
            table: dict[int, int] = {}
            for row, witness in enumerate(witnesses):
                address = 0
                for position, variable in enumerate(support):
                    address |= ((witness >> variable) & 1) << position
                value = targets[row][output]
                previous = table.get(address)
                if previous is not None and previous != value:
                    valid = False
                    break
                table[address] = value
            if not valid:
                break
        if valid:
            return True
    return False


def pattern_consistent(
    supports: tuple[tuple[int, ...], ...],
    targets: tuple[tuple[int, ...], ...],
    n: int,
) -> bool:
    k = len(targets)
    for columns in product(range(1 << (k - 1)), repeat=n):
        valid = True
        for output, support in enumerate(supports):
            for left in range(k):
                for right in range(left + 1, k):
                    if targets[left][output] == targets[right][output]:
                        continue
                    separated = False
                    for variable in support:
                        left_bit = (
                            0
                            if left == 0
                            else (columns[variable] >> (left - 1)) & 1
                        )
                        right_bit = (
                            0
                            if right == 0
                            else (columns[variable] >> (right - 1)) & 1
                        )
                        if left_bit != right_bit:
                            separated = True
                            break
                    if not separated:
                        valid = False
                        break
                if not valid:
                    break
            if not valid:
                break
        if valid:
            return True
    return False


def labeled_three_color_consistent(
    supports: tuple[tuple[int, ...], ...],
    targets: tuple[tuple[int, ...], ...],
    n: int,
) -> bool:
    labels: list[int | None] = []
    for output in range(len(supports)):
        a, b, c = (targets[row][output] for row in range(3))
        if a == b == c:
            labels.append(None)
        elif a == b:
            labels.append(0)
        elif a == c:
            labels.append(1)
        else:
            labels.append(2)

    for coloring in product(range(3), repeat=n):
        valid = True
        for support, label in zip(supports, labels):
            if label is None:
                continue
            first = coloring[support[0]]
            if (
                all(coloring[variable] == first for variable in support)
                and first != label
            ):
                valid = False
                break
        if valid:
            return True
    return False


def bad_masks(
    n: int, supports: tuple[tuple[int, int, int], ...]
) -> tuple[tuple[int, int, int], ...]:
    masks = [[0, 0, 0] for _ in supports]
    for index, coloring in enumerate(product(range(3), repeat=n)):
        bit = 1 << index
        for support_index, support in enumerate(supports):
            color = coloring[support[0]]
            if coloring[support[1]] != color or coloring[support[2]] != color:
                continue
            for label in range(3):
                if label != color:
                    masks[support_index][label] |= bit
    return tuple(tuple(row) for row in masks)


def independent_pair_census(n: int = 6) -> dict:
    triples = tuple(combinations(range(n), 3))
    masks = bad_masks(n, triples)
    distribution: Counter[str] = Counter()
    mismatches = 0
    checked = 0
    minimum = 3**n
    for first, support_a in enumerate(triples):
        for second in range(first + 1, len(triples)):
            support_b = triples[second]
            overlap = len(set(support_a) & set(support_b))
            for label_a in range(3):
                for label_b in range(3):
                    exact = (
                        masks[first][label_a] & masks[second][label_b]
                    ).bit_count()
                    if overlap == 0:
                        formula = 4 * 3 ** (n - 6)
                    else:
                        common = 2 if label_a == label_b else 1
                        formula = common * 3 ** (n - (6 - overlap))
                    mismatches += exact != formula
                    minimum = min(minimum, exact)
                    key = (
                        f"overlap={overlap};"
                        f"same_label={str(label_a == label_b).lower()};"
                        f"intersection={exact}"
                    )
                    distribution[key] += 1
                    checked += 1

    return {
        "variables": n,
        "supports": len(triples),
        "labeled_distinct_support_pairs_checked": checked,
        "formula_mismatches": mismatches,
        "minimum_pair_intersection": minimum,
        "distribution": dict(sorted(distribution.items())),
    }


FANO = (
    (0, 1, 2),
    (0, 3, 4),
    (0, 5, 6),
    (1, 3, 5),
    (1, 4, 6),
    (2, 3, 6),
    (2, 4, 5),
)


def independent_fano_census() -> dict:
    masks = bad_masks(7, FANO)
    total_colorings = 3**7
    counts = []
    for labels in product(range(3), repeat=7):
        bad_union = 0
        for edge, label in enumerate(labels):
            bad_union |= masks[edge][label]
        counts.append(total_colorings - bad_union.bit_count())
    return {
        "support_edges": 7,
        "labelings": len(counts),
        "satisfiable_labelings": sum(count > 0 for count in counts),
        "uncoverable_labelings": sum(count == 0 for count in counts),
        "minimum_satisfying_colorings": min(counts),
        "maximum_satisfying_colorings": max(counts),
        "total_satisfying_pairs": sum(counts),
    }


def independent_moment_certificates() -> list[dict[str, int]]:
    rows = []
    for n in (5, 6, 7, 8, 9):
        universe = 3**n
        single = 2 * 3 ** (n - 3)
        excess = 14 * single - universe
        lower = comb(14, 2) * 3 ** (n - 5)
        upper = 7 * excess
        rows.append(
            {
                "variables": n,
                "colorings": universe,
                "single_bad_colorings": single,
                "incidence_excess_if_cover": excess,
                "pair_intersection_lower_bound": lower,
                "pair_intersection_upper_bound_if_cover": upper,
                "contradiction_gap": lower - upper,
            }
        )
    return rows


def independent_target_scales() -> list[dict[str, int]]:
    return [
        {
            "n": n,
            "m": n + ceil(n ** (2 / 3)),
            "simple_support_capacity": comb(n, 3),
            "covered_by_fourteen_output_theorem": int(
                n + ceil(n ** (2 / 3)) <= 14
            ),
        }
        for n in range(5, 10)
    ]


V80_PROPERTY_SUPPORTS = {
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

V87_PROPERTY_SAMPLES = (
    (10, 15, 88000),
    (10, 15, 88001),
    (12, 18, 88200),
    (12, 18, 88201),
    (14, 20, 88400),
    (14, 20, 88401),
    (16, 23, 88600),
    (16, 23, 88601),
)


def count_property_b(
    variable_count: int, supports: tuple[tuple[int, int, int], ...]
) -> int:
    count = 0
    for mask in range(1 << variable_count):
        valid = True
        for a, b, c in supports:
            color = (mask >> a) & 1
            if ((mask >> b) & 1) == color and ((mask >> c) & 1) == color:
                valid = False
                break
        count += valid
    return count


def coloring_is_proper(
    coloring: list[int], supports: tuple[tuple[int, int, int], ...]
) -> bool:
    return all(
        not (coloring[a] == coloring[b] == coloring[c])
        for a, b, c in supports
    )


def independent_property_b_counts() -> tuple[dict[str, int], dict[int, int]]:
    v80_counts: dict[str, int] = {}
    for name, supports in V80_PROPERTY_SUPPORTS.items():
        n = max(max(support) for support in supports) + 1
        v80_counts[name] = count_property_b(n, supports)

    sample_counts: dict[int, int] = {}
    for n, m, seed in V87_PROPERTY_SAMPLES:
        rng = random.Random(seed)
        supports = tuple(
            rng.sample(tuple(combinations(range(n), 3)), m)
        )
        sample_counts[seed] = count_property_b(n, supports)
    return v80_counts, sample_counts


def validate_property_b_results(committed: dict) -> None:
    lower_density = 3.5 * log(2) - 1
    calibration = committed["density_calibration"]
    assert abs(
        calibration["random_3_uniform_two_colorability_lower_density"]
        - lower_density
    ) < 1e-15
    assert calibration["coupling_density"] == 1.25
    assert calibration["coupling_density"] < lower_density
    assert calibration["target_density_limit"] == 1.0
    for row in calibration["calibration_scales"]:
        assert row["m"] == row["n"] + ceil(row["n"] ** (2 / 3))
        assert abs(row["density"] - row["m"] / row["n"]) < 1e-15
        assert row["below_five_quarters"] == (row["m"] <= 1.25 * row["n"])

    v80_counts, sample_counts = independent_property_b_counts()
    v80_rows = committed["finite_audit"]["v80_controls"]
    assert {row["name"]: row["proper_two_colorings"] for row in v80_rows} == v80_counts
    for row in v80_rows:
        supports = V80_PROPERTY_SUPPORTS[row["name"]]
        assert coloring_is_proper(row["one_coloring"], supports)

    sample_rows = committed["finite_audit"]["v87_random_samples"]
    assert {row["seed"]: row["proper_two_colorings"] for row in sample_rows} == sample_counts
    for row in sample_rows:
        rng = random.Random(row["seed"])
        supports = tuple(
            rng.sample(tuple(combinations(range(row["n"]), 3)), row["m"])
        )
        assert coloring_is_proper(row["one_coloring"], supports)

    assert committed["finite_audit"]["v80_all_two_colorable"]
    assert committed["finite_audit"]["v87_samples_all_two_colorable"]
    assert committed["finite_audit"]["total_support_families_checked"] == 11
    assert committed["constructor_lower_bound"]["minimum_universal_rows"] == 4
    assert not committed["constructor_lower_bound"][
        "support_only_universal_triple_exists"
    ]
    status = committed["scientific_status"]
    assert status["v87_random_model_two_colorable_whp"]
    assert status["same_family_three_certificates_plus_property_b_exists"]
    assert status["constructor_model_lower_bound"]
    assert not status["support_only_universal_triple_exists"]
    assert not status["four_row_obstruction_constructed"]


def main() -> None:
    committed = json.loads((ROOT / "RESULTS.json").read_text(encoding="utf-8"))
    triples = tuple(combinations(range(4), 3))
    totals: dict[tuple[int, int, bool], int] = {}
    checked = 0
    mismatches = 0
    coloring_mismatches = 0

    for mask in range(1, 1 << len(triples)):
        supports = tuple(
            triples[index] for index in range(len(triples)) if mask & (1 << index)
        )
        m = len(supports)
        for k in (1, 2, 3):
            for bits in range(1 << (k * m)):
                targets = target_matrix(k, m, bits)
                direct = direct_consistent(supports, targets, 4)
                patterned = pattern_consistent(supports, targets, 4)
                mismatches += direct != patterned
                if k == 3:
                    colored = labeled_three_color_consistent(supports, targets, 4)
                    coloring_mismatches += direct != colored
                key = (k, m, direct)
                totals[key] = totals.get(key, 0) + 1
                checked += 1

    expected = {
        (row["rows"], row["supports"], row["coverable"]): row["instances"]
        for row in committed["finite_audit"]["breakdown"]
    }
    assert checked == committed["finite_audit"]["target_instances"] == 7264
    assert totals == expected
    assert mismatches == 0
    assert coloring_mismatches == 0
    assert all(coverable for (_k, _m, coverable) in totals)

    barrier = committed["three_row_barrier"]
    assert independent_pair_census() == barrier["pair_formula_census"]
    assert independent_fano_census() == barrier["fano_labeling_census"]
    assert independent_moment_certificates() == barrier["moment_certificates"]
    assert independent_target_scales() == barrier["target_stretch_scales"]
    assert barrier["minimum_active_outputs_for_three_row_obstruction"] == 15

    property_b = json.loads(
        (ROOT / "PROPERTY_B_RESULTS.json").read_text(encoding="utf-8")
    )
    validate_property_b_results(property_b)

    print(
        "V88 independent verification passed: collision geometry, bad-cylinder "
        "moments, Fano labelings, 11 Property-B controls, and the universal "
        "three-row constructor lower bound."
    )


if __name__ == "__main__":
    main()
