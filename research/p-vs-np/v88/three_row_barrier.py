#!/usr/bin/env python3
"""V88: lower barriers for three-row Eval_H obstructions."""
from __future__ import annotations

from collections import Counter
from itertools import combinations, product
from math import ceil, comb
from typing import Sequence

Support = tuple[int, int, int]


def validate_simple_ternary_supports(
    supports: Sequence[Sequence[int]], n: int
) -> tuple[Support, ...]:
    normalized: list[Support] = []
    for support in supports:
        if len(support) != 3 or len(set(support)) != 3:
            raise ValueError("supports must be simple ternary triples")
        triple = tuple(sorted(int(v) for v in support))
        if triple[0] < 0 or triple[-1] >= n:
            raise ValueError("support variable outside [0,n)")
        normalized.append(triple)
    if len(set(normalized)) != len(normalized):
        raise ValueError("support family must have no repeated triple")
    return tuple(normalized)


def bad_coloring_count(n: int) -> int:
    """Number of three-colorings violating one labeled ternary support."""
    if n < 3:
        raise ValueError("n must be at least three")
    return 2 * 3 ** (n - 3)


def bad_intersection_formula(
    n: int,
    support_a: Sequence[int],
    label_a: int,
    support_b: Sequence[int],
    label_b: int,
) -> int:
    """Exact intersection of two bad-coloring cylinders."""
    a, b = validate_simple_ternary_supports((support_a, support_b), n)
    if label_a not in (0, 1, 2) or label_b not in (0, 1, 2):
        raise ValueError("labels must lie in {0,1,2}")
    overlap = len(set(a) & set(b))
    if overlap == 0:
        return 4 * 3 ** (n - 6)
    common_bad_colors = 2 if label_a == label_b else 1
    union_size = 6 - overlap
    return common_bad_colors * 3 ** (n - union_size)


def exact_bad_intersection(
    n: int,
    support_a: Sequence[int],
    label_a: int,
    support_b: Sequence[int],
    label_b: int,
) -> int:
    a, b = validate_simple_ternary_supports((support_a, support_b), n)
    total = 0
    for coloring in product(range(3), repeat=n):
        color_a = coloring[a[0]]
        bad_a = (
            coloring[a[1]] == color_a
            and coloring[a[2]] == color_a
            and color_a != label_a
        )
        color_b = coloring[b[0]]
        bad_b = (
            coloring[b[1]] == color_b
            and coloring[b[2]] == color_b
            and color_b != label_b
        )
        total += bool(bad_a and bad_b)
    return total


def fourteen_output_moment_certificate(n: int) -> dict[str, int]:
    """Return the contradictory first/second moment bounds at q=14."""
    if n < 5:
        raise ValueError("the uniform pair bound is stated for n at least five")
    universe = 3**n
    single = bad_coloring_count(n)
    excess_if_cover = 14 * single - universe
    pair_lower = comb(14, 2) * 3 ** (n - 5)
    pair_upper = 7 * excess_if_cover
    assert excess_if_cover == 3 ** (n - 3)
    assert pair_lower > pair_upper
    return {
        "variables": n,
        "colorings": universe,
        "single_bad_colorings": single,
        "incidence_excess_if_cover": excess_if_cover,
        "pair_intersection_lower_bound": pair_lower,
        "pair_intersection_upper_bound_if_cover": pair_upper,
        "contradiction_gap": pair_lower - pair_upper,
    }


def target_stretch_scales() -> list[dict[str, int]]:
    rows: list[dict[str, int]] = []
    for n in range(5, 10):
        m = n + ceil(n ** (2 / 3))
        rows.append(
            {
                "n": n,
                "m": m,
                "simple_support_capacity": comb(n, 3),
                "covered_by_fourteen_output_theorem": int(m <= 14),
            }
        )
    return rows


FANO_SUPPORTS: tuple[Support, ...] = (
    (0, 1, 2),
    (0, 3, 4),
    (0, 5, 6),
    (1, 3, 5),
    (1, 4, 6),
    (2, 3, 6),
    (2, 4, 5),
)


def coloring_satisfies_labels(
    supports: Sequence[Sequence[int]],
    labels: Sequence[int],
    coloring: Sequence[int],
) -> bool:
    if len(supports) != len(labels):
        raise ValueError("one label per support is required")
    for support, label in zip(supports, labels):
        a, b, c = (coloring[v] for v in support)
        if a == b == c and a != label:
            return False
    return True


def fano_labeling_census() -> dict[str, int]:
    colorings = tuple(product(range(3), repeat=7))
    satisfiable = 0
    minimum_witnesses = len(colorings)
    maximum_witnesses = 0
    total_witnesses = 0
    for labels in product(range(3), repeat=len(FANO_SUPPORTS)):
        witnesses = sum(
            coloring_satisfies_labels(FANO_SUPPORTS, labels, coloring)
            for coloring in colorings
        )
        satisfiable += witnesses > 0
        minimum_witnesses = min(minimum_witnesses, witnesses)
        maximum_witnesses = max(maximum_witnesses, witnesses)
        total_witnesses += witnesses
    labelings = 3 ** len(FANO_SUPPORTS)
    return {
        "support_edges": len(FANO_SUPPORTS),
        "labelings": labelings,
        "satisfiable_labelings": satisfiable,
        "uncoverable_labelings": labelings - satisfiable,
        "minimum_satisfying_colorings": minimum_witnesses,
        "maximum_satisfying_colorings": maximum_witnesses,
        "total_satisfying_pairs": total_witnesses,
    }


def pair_formula_census(n: int = 6) -> dict:
    triples = tuple(combinations(range(n), 3))
    distributions: Counter[str] = Counter()
    checked = 0
    mismatches = 0
    minimum = 3**n
    for index, support_a in enumerate(triples):
        for support_b in triples[index + 1 :]:
            overlap = len(set(support_a) & set(support_b))
            for label_a in range(3):
                for label_b in range(3):
                    exact = exact_bad_intersection(
                        n, support_a, label_a, support_b, label_b
                    )
                    formula = bad_intersection_formula(
                        n, support_a, label_a, support_b, label_b
                    )
                    mismatches += exact != formula
                    minimum = min(minimum, exact)
                    key = (
                        f"overlap={overlap};"
                        f"same_label={str(label_a == label_b).lower()};"
                        f"intersection={exact}"
                    )
                    distributions[key] += 1
                    checked += 1

    return {
        "variables": n,
        "supports": len(triples),
        "labeled_distinct_support_pairs_checked": checked,
        "formula_mismatches": mismatches,
        "minimum_pair_intersection": minimum,
        "distribution": dict(sorted(distributions.items())),
    }


def build_three_row_results() -> dict:
    moments = [
        fourteen_output_moment_certificate(n) for n in (5, 6, 7, 8, 9)
    ]
    return {
        "theorem": (
            "Every three-row target list on a simple 3-uniform support family "
            "with at most fourteen active output columns is coverable."
        ),
        "minimum_active_outputs_for_three_row_obstruction": 15,
        "proof_constants": {
            "single_bad_probability": "2/27",
            "minimum_distinct_pair_intersection_probability": "1/243",
            "fourteen_pair_lower_coefficient": 91,
            "fourteen_cover_upper_coefficient": 63,
        },
        "moment_certificates": moments,
        "pair_formula_census": pair_formula_census(),
        "fano_labeling_census": fano_labeling_census(),
        "target_stretch_scales": target_stretch_scales(),
        "scientific_status": {
            "three_row_obstruction_requires_fifteen_outputs": True,
            "three_row_target_stretch_n5_through_n9_coverable": True,
            "three_row_asymptotic_constructor": False,
            "four_row_obstruction_constructed": False,
        },
    }


if __name__ == "__main__":
    import json

    print(json.dumps(build_three_row_results(), indent=2, sort_keys=True))
