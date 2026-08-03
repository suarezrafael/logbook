#!/usr/bin/env python3
"""Independent V88 audit without importing the primary implementation."""
from __future__ import annotations

import json
from itertools import combinations, product
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
                        left_bit = 0 if left == 0 else (columns[variable] >> (left - 1)) & 1
                        right_bit = 0 if right == 0 else (columns[variable] >> (right - 1)) & 1
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
            if all(coloring[variable] == first for variable in support) and first != label:
                valid = False
                break
        if valid:
            return True
    return False


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

    print(
        "V88 independent verification passed: direct observed-table extension "
        "matches the pattern CSP and the three-color reduction on 7,264 instances."
    )


if __name__ == "__main__":
    main()
