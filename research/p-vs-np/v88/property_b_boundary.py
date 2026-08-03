#!/usr/bin/env python3
"""V88: finite and arithmetic audits for the Property-B boundary."""
from __future__ import annotations

import itertools
import math
import random
from typing import Sequence

Support = tuple[int, int, int]

V80_SUPPORTS: dict[str, tuple[Support, ...]] = {
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

V87_RANDOM_SAMPLES = (
    (10, 15, 88000),
    (10, 15, 88001),
    (12, 18, 88200),
    (12, 18, 88201),
    (14, 20, 88400),
    (14, 20, 88401),
    (16, 23, 88600),
    (16, 23, 88601),
)


def sample_supports(n: int, m: int, seed: int) -> tuple[Support, ...]:
    rng = random.Random(seed)
    return tuple(rng.sample(tuple(itertools.combinations(range(n), 3)), m))


def proper_two_coloring_count(
    variable_count: int, supports: Sequence[Sequence[int]]
) -> tuple[int, int | None]:
    count = 0
    first: int | None = None
    for mask in range(1 << variable_count):
        valid = True
        for support in supports:
            a, b, c = support
            color = (mask >> a) & 1
            if ((mask >> b) & 1) == color and ((mask >> c) & 1) == color:
                valid = False
                break
        if valid:
            count += 1
            if first is None:
                first = mask
    return count, first


def decode_mask(mask: int | None, variable_count: int) -> list[int] | None:
    if mask is None:
        return None
    return [(mask >> vertex) & 1 for vertex in range(variable_count)]


def v80_property_b_census() -> list[dict]:
    rows = []
    for name, supports in V80_SUPPORTS.items():
        n = max(max(support) for support in supports) + 1
        count, first = proper_two_coloring_count(n, supports)
        rows.append(
            {
                "name": name,
                "variables": n,
                "supports": len(supports),
                "proper_two_colorings": count,
                "one_coloring": decode_mask(first, n),
            }
        )
    return rows


def v87_property_b_census() -> list[dict]:
    rows = []
    for n, m, seed in V87_RANDOM_SAMPLES:
        supports = sample_supports(n, m, seed)
        count, first = proper_two_coloring_count(n, supports)
        rows.append(
            {
                "n": n,
                "m": m,
                "seed": seed,
                "proper_two_colorings": count,
                "one_coloring": decode_mask(first, n),
            }
        )
    return rows


def density_calibration() -> dict:
    achlioptas_moore_lower = 3.5 * math.log(2) - 1
    coupling_density = 1.25
    assert coupling_density < achlioptas_moore_lower
    scales = []
    for n in (76, 125, 512, 4096, 32768):
        m = n + math.ceil(n ** (2 / 3))
        scales.append(
            {
                "n": n,
                "m": m,
                "density": m / n,
                "below_five_quarters": m <= 1.25 * n,
            }
        )
    assert all(row["below_five_quarters"] for row in scales)
    return {
        "random_3_uniform_two_colorability_lower_density": achlioptas_moore_lower,
        "coupling_density": coupling_density,
        "strict_margin": achlioptas_moore_lower - coupling_density,
        "target_density_limit": 1.0,
        "calibration_scales": scales,
    }


def build_property_b_results() -> dict:
    v80 = v80_property_b_census()
    v87 = v87_property_b_census()
    return {
        "theorem": (
            "The V87 random support model is two-colorable with high probability; "
            "therefore a target-stretch family simultaneously has the three V87 "
            "certificate barriers and covers every target list of at most three rows."
        ),
        "constructor_lower_bound": {
            "model": "support-only ordered target lists with at most three rows",
            "minimum_universal_rows": 4,
            "support_only_universal_triple_exists": False,
        },
        "density_calibration": density_calibration(),
        "finite_audit": {
            "v80_controls": v80,
            "v87_random_samples": v87,
            "v80_all_two_colorable": all(
                row["proper_two_colorings"] > 0 for row in v80
            ),
            "v87_samples_all_two_colorable": all(
                row["proper_two_colorings"] > 0 for row in v87
            ),
            "total_support_families_checked": len(v80) + len(v87),
        },
        "scientific_status": {
            "v87_random_model_two_colorable_whp": True,
            "same_family_three_certificates_plus_property_b_exists": True,
            "support_only_universal_triple_exists": False,
            "constructor_model_lower_bound": True,
            "four_row_obstruction_constructed": False,
        },
    }


if __name__ == "__main__":
    import json

    print(json.dumps(build_property_b_results(), indent=2, sort_keys=True))
