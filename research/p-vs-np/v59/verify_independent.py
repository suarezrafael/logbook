#!/usr/bin/env python3
"""Independent read-only V59 audit. Does not import v59_core."""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def local_mask(forbidden):
    mask = 0
    forbidden_left = forbidden & 1
    forbidden_right = (forbidden >> 1) & 1
    for local in range(8):
        pivot = local & 1
        left = (local >> 1) & 1
        right = (local >> 2) & 1
        if pivot == 0 and not (left == forbidden_left and right == forbidden_right):
            mask |= 1 << local
    return mask


def gate(description):
    pivot, left, right, forbidden = description
    return local_mask(forbidden), (pivot, left, right)


BASE = (
    (0, 1, 2, 1),
    (0, 1, 2, 2),
    (0, 1, 3, 1),
    (0, 1, 3, 2),
    (0, 2, 3, 3),
)


def family(k):
    descriptions = list(BASE)
    offset = 4
    for _ in range(k):
        descriptions.extend(
            [
                (offset + 2, offset, offset + 1, 1),
                (offset + 2, offset, offset + 1, 2),
                (offset + 2, offset, offset + 1, 3),
            ]
        )
        offset += 3
    return 4 + 3 * k, [gate(description) for description in descriptions]


def output(gates, x):
    bits = []
    for mask, support in gates:
        local = (
            ((x >> support[0]) & 1)
            | (((x >> support[1]) & 1) << 1)
            | (((x >> support[2]) & 1) << 2)
        )
        bits.append((mask >> local) & 1)
    return tuple(bits)


def neighbours(point):
    for index in range(len(point)):
        candidate = list(point)
        candidate[index] ^= 1
        yield tuple(candidate)


def forced(n, preimages):
    bitwise_and = (1 << n) - 1
    bitwise_or = 0
    for value in preimages:
        bitwise_and &= value
        bitwise_or |= value
    return n - (bitwise_and ^ bitwise_or).bit_count()


def main():
    cases = []
    for k in range(4):
        n, gates = family(k)
        preimages = {}
        for x in range(1 << n):
            preimages.setdefault(output(gates, x), []).append(x)
        image = set(preimages)
        boundary = {
            point for point in image if any(candidate not in image for candidate in neighbours(point))
        }
        interior = image - boundary
        all_ones = (1,) * len(gates)
        assert interior == {all_ones}
        assert len(preimages[all_ones]) == 1
        assert forced(n, preimages[all_ones]) == n
        for candidate in neighbours(all_ones):
            assert candidate in boundary
            assert len(preimages[candidate]) == 1
            assert forced(n, preimages[candidate]) == n
        cases.append(
            {
                "k": k,
                "n": n,
                "m": len(gates),
                "image_size": len(image),
                "boundary_size": len(boundary),
            }
        )

    constants = []
    for m in range(2, 25):
        value = math.comb(m, m // 2) / (1 << (m - 1))
        assert value * math.sqrt(m) > 1.25
        constants.append(value)

    computed = {
        "status": "passed",
        "direct_sum_cases": cases,
        "harper_checks": len(constants),
        "failures": 0,
    }
    committed = json.loads((ROOT / "INDEPENDENT_RESULTS.json").read_text(encoding="utf-8"))
    for key, value in computed.items():
        assert committed[key] == value, key

    primary = json.loads((ROOT / "RESULTS.json").read_text(encoding="utf-8"))
    assert primary["status"] == "passed"
    assert primary["validation"]["direct_sum_cases"] == len(cases)
    assert primary["direct_sum"] == [
        {
            **case,
            "unique_interior": [1] * case["m"],
            "interior_preimages": 1,
            "neighbor_preimages": [1] * case["m"],
            "interior_exact_forced": case["n"],
            "neighbor_exact_forced": [case["n"]] * case["m"],
            "interior_unit_forced": 0,
            "neighbor_unit_forced": [0] * case["m"],
            "strict_exact_forced_improvement_exists": False,
            "strict_unit_improvement_exists": False,
            "strict_smaller_fiber_exists": False,
        }
        for case in cases
    ]

    print("V59 independent verification passed:")
    print("  4 direct-sum families reconstructed from scratch;")
    print(f"  {len(constants)} central-binomial expansion constants checked;")
    print("  committed independent evidence matches without rewriting; zero failures.")


if __name__ == "__main__":
    main()
