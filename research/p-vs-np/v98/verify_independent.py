#!/usr/bin/env python3
from __future__ import annotations

import json
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def bit(mask: int, x: tuple[int, ...]) -> int:
    idx = sum(x[i] << i for i in range(len(x)))
    return (mask >> idx) & 1


def mask3(fn) -> int:
    value = 0
    for x in product((0, 1), repeat=3):
        value |= fn(x) << (x[0] + 2 * x[1] + 4 * x[2])
    return value


def essential(mask: int, j: int) -> bool:
    for x in product((0, 1), repeat=3):
        if x[j]:
            continue
        y = list(x)
        y[j] = 1
        if bit(mask, x) != bit(mask, tuple(y)):
            return True
    return False


def direction(mask: int, j: int) -> int | None:
    up = down = False
    for x in product((0, 1), repeat=3):
        if x[j]:
            continue
        y = list(x)
        y[j] = 1
        a, b = bit(mask, x), bit(mask, tuple(y))
        up |= b > a
        down |= b < a
    if up and down:
        return None
    if not up and not down:
        return None
    return 0 if up else 1


def maj(x: tuple[int, int, int]) -> int:
    return int(sum(x) >= 2)


def strict_gate_mask(support: tuple[int, int, int]) -> int:
    local_flip = tuple(1 if v == 0 else 0 for v in support)
    return mask3(lambda x: maj(tuple(x[i] ^ local_flip[i] for i in range(3))))


def strict_output(n: int, assignment: tuple[int, ...]) -> tuple[int, ...]:
    supports = [(i, (i + 1) % n, (i + 2) % n) for i in range(n)]
    supports.append(supports[0])
    answer = []
    for support in supports:
        mask = strict_gate_mask(support)
        answer.append(bit(mask, tuple(assignment[v] for v in support)))
    return tuple(answer)


def transformed_output(n: int, assignment: tuple[int, ...]) -> tuple[int, ...]:
    z = list(assignment)
    z[0] ^= 1
    supports = [(i, (i + 1) % n, (i + 2) % n) for i in range(n)]
    supports.append(supports[0])
    return tuple(maj(tuple(z[v] for v in support)) for support in supports)


def parity_x_witness(ell: int, target: tuple[int, ...]) -> tuple[list[int], dict[int, int], int]:
    length = 2 * ell
    w = length
    private = {}
    cursor = length + 1
    for i in range(length):
        if i not in (0, 3):
            private[i] = cursor
            cursor += 1
    x = [0] * cursor
    x[0] = target[0]
    x[3] = target[3]
    for i in range(length):
        if i in (0, 3):
            continue
        x[private[i]] = target[i] ^ x[i] ^ x[(i + 1) % length]
    return x, private, w


def parity_x_output(ell: int, x: list[int], private: dict[int, int], w: int) -> tuple[int, ...]:
    length = 2 * ell
    out = []
    for i in range(length):
        third = w if i in (0, 3) else private[i]
        out.append(x[i] ^ x[(i + 1) % length] ^ x[third])
    return tuple(out)


def main() -> None:
    committed = json.loads((ROOT / "RESULTS.json").read_text(encoding="utf-8"))

    essential_count = 0
    unate_count = 0
    for mask in range(256):
        if not all(essential(mask, j) for j in range(3)):
            continue
        essential_count += 1
        if all(direction(mask, j) is not None for j in range(3)):
            unate_count += 1
    assert essential_count == committed["ternary_truth_table_audit"]["essential_ternary_masks"]
    assert unate_count == committed["ternary_truth_table_audit"]["essential_ternary_unate_masks"]

    for n in range(5, 9):
        raw = {strict_output(n, x) for x in product((0, 1), repeat=n)}
        switched = {transformed_output(n, x) for x in product((0, 1), repeat=n)}
        assert raw == switched

        supports = [(i, (i + 1) % n, (i + 2) % n) for i in range(n)]
        supports.append(supports[0])
        degrees = [sum(v in support for support in supports) for v in range(n)]
        assert min(degrees) >= 3
        assert any(direction(strict_gate_mask(support), j) == 1
                   for support in supports for j in range(3))

    for ell in range(3, 6):
        for target in product((0, 1), repeat=2 * ell):
            x, private, w = parity_x_witness(ell, target)
            assert parity_x_output(ell, x, private, w) == target

    print(
        "V98 independent verification passed: independent truth-table census, "
        "explicit MAJ switching, and constructive parity loose-X surjectivity."
    )


if __name__ == "__main__":
    main()
