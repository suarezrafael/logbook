#!/usr/bin/env python3
"""Independent read-only repository audit for V56."""
from __future__ import annotations

import itertools
import json
import random
from functools import reduce
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def transform(mask, permutation, negations, output_negation):
    out = 0
    for x in range(8):
        bits = [(x >> i) & 1 for i in range(3)]
        old = [bits[permutation[i]] ^ negations[i] for i in range(3)]
        index = old[0] | (old[1] << 1) | (old[2] << 2)
        out |= ((((mask >> index) & 1) ^ output_negation) << x)
    return out


def orbit(mask):
    return sorted(
        {
            transform(mask, permutation, negations, output_negation)
            for permutation in itertools.permutations(range(3))
            for negations in itertools.product((0, 1), repeat=3)
            for output_negation in (0, 1)
        }
    )


def affine(points):
    points = set(points)
    if not points:
        return False
    base = next(iter(points))
    linear = {x ^ base for x in points}
    return len(linear) & (len(linear) - 1) == 0 and all(
        x ^ y in linear for x in linear for y in linear
    )


def orientation(mask):
    for value in (0, 1):
        points = {x for x in range(8) if ((mask >> x) & 1) == value}
        if points and affine(points):
            return value, points
    return None


def active_set(mask):
    _, points = orientation(mask)
    return points


def good(masks):
    sets = [active_set(mask) for mask in masks]
    universe = set(range(8))
    common = universe.copy()
    for current in sets:
        common &= current
    if not common:
        return True
    for index, current in enumerate(sets):
        others = universe.copy()
        for j, candidate in enumerate(sets):
            if index != j:
                others &= candidate
        if others <= current:
            return True
    return False


def main():
    remaining = set(range(256))
    classes = []
    while remaining:
        current_orbit = orbit(min(remaining))
        classes.append((min(current_orbit), current_orbit))
        remaining -= set(current_orbit)
    assert len(classes) == 14
    assert [
        canonical for canonical, current_orbit in classes if any(orientation(mask) for mask in current_orbit)
    ] == [0, 1, 3, 6, 15, 24, 60, 105]

    count06 = sum(
        1
        for masks in itertools.combinations_with_replacement(orbit(6), 4)
        if good(masks)
    )
    count01 = sum(
        1
        for masks in itertools.combinations_with_replacement(orbit(1), 4)
        if good(masks)
    )
    assert count06 == 17550
    assert count01 == 3876

    rng = random.Random(5657)
    fresh = 0
    affine_masks = [mask for mask in range(256) if orientation(mask)]
    for _ in range(240):
        n = rng.randrange(3, 9)
        masks = [rng.choice(affine_masks) for _ in range(n + 1)]
        sets = [active_set(mask) for mask in masks]
        universe = set(range(8))
        common = universe.copy()
        for current in sets:
            common &= current
        assert (not common) or any(
            reduce(
                set.intersection,
                [sets[j] for j in range(len(sets)) if j != index],
                universe.copy(),
            )
            <= sets[index]
            for index in range(len(sets))
        )
        fresh += 1

    committed = json.loads((ROOT / "RESULTS.json").read_text(encoding="utf-8"))
    assert committed["status"] == "passed"
    assert committed["classification"]["npn_classes"] == len(classes)
    assert committed["validation"]["distance_two_exhaustive_multisets_n3_m4"] == count06
    assert committed["validation"]["singleton_exhaustive_multisets_n3_m4"] == count01
    assert committed["scientific_status"]["p_vs_np_resolved"] is False

    print(
        "V56 independent repository audit passed: 14 classes, 21426 exhaustive "
        "multisets, 240 fresh cases, committed evidence unchanged, zero failures."
    )


if __name__ == "__main__":
    main()
