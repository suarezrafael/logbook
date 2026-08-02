#!/usr/bin/env python3
"""Independent read-only audit for V58. Does not import v58_core."""
from __future__ import annotations

import itertools
import json
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def active_mask(n, description):
    pivot, left, right, forbidden = description
    value = 0
    for x in range(1 << n):
        if (x >> pivot) & 1:
            continue
        pair = ((x >> left) & 1) | (((x >> right) & 1) << 1)
        if pair != forbidden:
            value |= 1 << x
    return value


def descriptions(n):
    output = []
    for pivot in range(n):
        others = [variable for variable in range(n) if variable != pivot]
        for left, right in itertools.combinations(others, 2):
            for forbidden in (1, 2, 3):
                output.append((pivot, left, right, forbidden))
    return output


def redundant_indices(sets, full):
    answer = []
    for index, target in enumerate(sets):
        intersection = full
        for j, candidate in enumerate(sets):
            if index != j:
                intersection &= candidate
        if intersection & ~target == 0:
            answer.append(index)
    return answer


def canonical(family, n):
    best = None
    for permutation in itertools.permutations(range(n)):
        current = []
        for pivot, left, right, forbidden in family:
            pivot, first, second = permutation[pivot], permutation[left], permutation[right]
            if first > second:
                first, second = second, first
                forbidden = {1: 2, 2: 1, 3: 3}[forbidden]
            current.append((pivot, first, second, forbidden))
        candidate = tuple(sorted(current))
        best = candidate if best is None or candidate < best else best
    return best


def required(m, depth, zeros):
    if zeros > 2:
        return 0
    return sum(math.comb(m - depth, count) for count in range(3 - zeros))


def exact_no_ball2(n, canonical_type):
    m = n + 1
    all_descriptions = descriptions(n)
    first = (0, 1, 2, canonical_type)
    all_descriptions = [first] + [item for item in all_descriptions if item != first]
    masks = [active_mask(n, item) for item in all_descriptions]
    full = (1 << (1 << n)) - 1
    cells = {1: masks[0], 0: full ^ masks[0]}
    nodes = 0

    def recurse(depth, start, current_cells):
        nonlocal nodes
        nodes += 1
        if depth == m:
            return False
        for index in range(start, len(all_descriptions)):
            active = masks[index]
            next_cells = {}
            viable = True
            for prefix, rows in current_cells.items():
                zeros = depth - prefix.bit_count()
                yes = rows & active
                no = rows & ~active & full
                required_yes = required(m, depth + 1, zeros)
                required_no = required(m, depth + 1, zeros + 1)
                if yes.bit_count() < required_yes or no.bit_count() < required_no:
                    viable = False
                    break
                if required_yes:
                    next_cells[(prefix << 1) | 1] = yes
                if required_no:
                    next_cells[prefix << 1] = no
            if viable and not recurse(depth + 1, index + 1, next_cells):
                return False
        return True

    return recurse(1, 1, cells), nodes


def main():
    all_descriptions = descriptions(4)
    masks = [active_mask(4, item) for item in all_descriptions]
    full = (1 << 16) - 1
    families = []
    for indices in itertools.combinations(range(36), 5):
        sets = [masks[index] for index in indices]
        if not redundant_indices(sets, full):
            families.append(tuple(all_descriptions[index] for index in indices))
    assert len(families) == 12
    assert len({canonical(family, 4) for family in families}) == 1

    flips = 0
    for family in families:
        sets = [active_mask(4, item) for item in family]
        for index in range(5):
            oriented = [(full ^ value) if j == index else value for j, value in enumerate(sets)]
            intersection = full
            for value in oriented:
                intersection &= value
            assert intersection != 0
            assert redundant_indices(oriented, full)
            flips += 1

    exact_cases = []
    for n in range(3, 8):
        for canonical_type in (1, 3):
            passed, nodes = exact_no_ball2(n, canonical_type)
            assert passed
            exact_cases.append({"n": n, "canonical_type": canonical_type, "nodes": nodes})

    base = ((0, 1, 2, 1), (0, 1, 2, 2), (0, 1, 3, 1), (0, 1, 3, 2), (0, 2, 3, 3))
    direct_sum_cases = 0
    for k in range(6):
        direct_sum = list(base)
        offset = 4
        for _ in range(k):
            direct_sum.extend(
                (
                    (offset + 2, offset, offset + 1, 1),
                    (offset + 2, offset, offset + 1, 2),
                    (offset + 2, offset, offset + 1, 3),
                )
            )
            offset += 3
        n = 4 + 3 * k
        full_n = (1 << (1 << n)) - 1
        sets = [active_mask(n, item) for item in direct_sum]
        oriented = [(full_n ^ value) if index == 0 else value for index, value in enumerate(sets)]
        assert redundant_indices(oriented, full_n)
        direct_sum_cases += 1

    rng = random.Random(5858)
    boundary_checks = 0
    for m in range(2, 7):
        cube = list(range(1 << m))
        for _ in range(100):
            image = set(rng.sample(cube, rng.randrange(1, 1 << m)))
            base_point = rng.choice(tuple(image))
            distance = min(
                (
                    (candidate ^ base_point).bit_count()
                    for candidate in image
                    if any((candidate ^ (1 << coordinate)) not in image for coordinate in range(m))
                ),
                default=None,
            )
            assert distance is not None
            for radius in range(min(3, m)):
                ball = {
                    base_point ^ sum(1 << coordinate for coordinate in subset)
                    for size in range(radius + 2)
                    for subset in itertools.combinations(range(m), size)
                }
                assert (distance > radius) == ball.issubset(image)
            boundary_checks += 1

    computed = {
        "status": "passed",
        "v57_families": 12,
        "isomorphism_classes": 1,
        "single_flips": flips,
        "independent_exact_cases": exact_cases,
        "direct_sum_cases": direct_sum_cases,
        "boundary_checks": boundary_checks,
        "failures": 0,
    }
    committed = json.loads((ROOT / "INDEPENDENT_RESULTS.json").read_text(encoding="utf-8"))
    for key, value in computed.items():
        assert committed[key] == value, key

    primary = json.loads((ROOT / "RESULTS.json").read_text(encoding="utf-8"))
    for key, value in computed.items():
        assert primary["validation"]["independent"][key] == value, key

    print("V58 independent verification passed:")
    print("  12 V57 families collapsed to one isomorphism class;")
    print(f"  {flips} single flips independently checked;")
    print("  exact no-counterexample search independently rebuilt for n=3..7;")
    print(f"  {boundary_checks} boundary/ball checks;")
    print("  committed independent evidence matches without rewriting; zero failures.")


if __name__ == "__main__":
    main()
