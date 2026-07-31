#!/usr/bin/env python3
"""Compact independent index verifier for Laboratory V25.

This script recomputes the complete NPN orbit partition of all four-input
Boolean functions and checks the machine-readable V25 summary. The full
research package contains a larger verifier that additionally recomputes
minimum finite-field zero-set degrees, checks all seven quadratic
nonexistence certificates, and exhaustively checks 100 complete circuits.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

VARIABLES = 4
FUNCTIONS = 1 << (1 << VARIABLES)
FULL_MASK = FUNCTIONS - 1
EXPECTED_HARD = {
    "0x017f": 64,
    "0x01bf": 192,
    "0x01ef": 192,
    "0x01fe": 64,
    "0x07f1": 192,
    "0x07f2": 384,
    "0x07f8": 192,
}


def input_maps() -> tuple[tuple[int, ...], ...]:
    maps: list[tuple[int, ...]] = []
    for permutation in itertools.permutations(range(VARIABLES)):
        for negation_mask in range(1 << VARIABLES):
            mapping: list[int] = []
            for source in range(1 << VARIABLES):
                source_bits = [(source >> index) & 1 for index in range(VARIABLES)]
                target = 0
                for position in range(VARIABLES):
                    bit = source_bits[permutation[position]] ^ (
                        (negation_mask >> position) & 1
                    )
                    target |= bit << position
                mapping.append(target)
            maps.append(tuple(mapping))
    return tuple(maps)


def transform_mask(mask: int, mapping: tuple[int, ...]) -> int:
    transformed = 0
    for source, target in enumerate(mapping):
        if (mask >> source) & 1:
            transformed |= 1 << target
    return transformed


def npn_classes() -> list[tuple[int, tuple[int, ...]]]:
    transformations = input_maps()
    remaining = set(range(FUNCTIONS))
    classes: list[tuple[int, tuple[int, ...]]] = []

    while remaining:
        seed = min(remaining)
        orbit: set[int] = set()
        for mapping in transformations:
            transformed = transform_mask(seed, mapping)
            orbit.add(transformed)
            orbit.add(transformed ^ FULL_MASK)
        canonical = min(orbit)
        sorted_orbit = tuple(sorted(orbit))
        classes.append((canonical, sorted_orbit))
        remaining.difference_update(orbit)

    return sorted(classes)


def main() -> None:
    results_path = Path(__file__).with_name("RESULTS.json")
    results = json.loads(results_path.read_text(encoding="utf-8"))
    classes = npn_classes()
    orbit_sizes = {f"0x{canonical:04x}": len(orbit) for canonical, orbit in classes}

    checks = {
        "npn_classes": len(classes) == results["classification"]["npn_classes"] == 222,
        "functions_covered": sum(len(orbit) for _, orbit in classes) == 65536,
        "orbits_disjoint": len({item for _, orbit in classes for item in orbit}) == 65536,
        "hard_masks_are_canonical": all(mask in orbit_sizes for mask in EXPECTED_HARD),
        "hard_orbit_sizes": all(orbit_sizes[mask] == size for mask, size in EXPECTED_HARD.items()),
        "degree_class_total": sum(results["classification"]["class_degree_counts"].values()) == 222,
        "degree_function_total": sum(results["classification"]["function_degree_counts"].values()) == 65536,
        "coverage_fraction": abs(
            results["classification"]["quadratic_or_lower_functions"] / 65536
            - results["classification"]["coverage_fraction"]
        ) < 1e-15,
        "scientific_caution": not results["status"]["peer_reviewed"]
        and not results["status"]["novelty_confirmed"]
        and not results["status"]["p_vs_np_resolved"],
    }

    payload = {
        "checks": checks,
        "all_passed": all(checks.values()),
        "recomputed_npn_classes": len(classes),
        "recomputed_functions": sum(len(orbit) for _, orbit in classes),
    }
    print(json.dumps(payload, indent=2))

    if not payload["all_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
