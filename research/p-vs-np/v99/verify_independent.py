#!/usr/bin/env python3
from __future__ import annotations

import json
from itertools import permutations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def bit(mask: int, x: tuple[int, ...]) -> int:
    return (mask >> sum(x[i] << i for i in range(len(x)))) & 1


def mask3(fn) -> int:
    value = 0
    for x in product((0, 1), repeat=3):
        value |= (fn(x) & 1) << (x[0] + 2 * x[1] + 4 * x[2])
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
    if up and down or (not up and not down):
        return None
    return 0 if up else 1


def transformed(mask: int, perm: tuple[int, int, int], flips: tuple[int, int, int], out: int) -> int:
    return mask3(lambda x: bit(mask, tuple(x[perm[j]] ^ flips[j] for j in range(3))) ^ out)


def canon(mask: int) -> int:
    return min(
        transformed(mask, perm, flips, out)
        for perm in permutations(range(3))
        for flips in product((0, 1), repeat=3)
        for out in (0, 1)
    )


def and_lit(signs: tuple[int, int, int]) -> int:
    return mask3(lambda x: int(all((x[j] ^ signs[j]) == 1 for j in range(3))))


def strict_singleton(n: int):
    supports = [(i, (i + 1) % n, (i + 2) % n) for i in range(n)]
    gates = [(s, and_lit((0, 0, 0))) for s in supports]
    gates.append((supports[0], and_lit((1, 0, 0))))
    return gates


def circuit_out(gates, x):
    return tuple(bit(mask, tuple(x[v] for v in support)) for support, mask in gates)


def strict_missing(n: int):
    target = [0] * (n + 1)
    target[0] = 1
    target[-1] = 1
    return tuple(target)


def mget(M: int, r: int, c: int) -> int:
    return (M >> (2 * r + c)) & 1


def bmul(A: int, B: int) -> int:
    out = 0
    for r in (0, 1):
        for c in (0, 1):
            value = any(mget(A, r, k) and mget(B, k, c) for k in (0, 1))
            out |= int(value) << (2 * r + c)
    return out


J, R0, R1, I2 = 0b1111, 0b0111, 0b1110, 0b1001
P01, P10 = 0b1011, 0b1101


def path(bits):
    M = I2
    for y in bits:
        M = bmul(M, R1 if y else R0)
    return M


def maj(a, b, c):
    return int(a + b + c >= 2)


def boundary(B, A, S, T, y0, y3):
    for v0, v1, v3, v4, w in product((0, 1), repeat=5):
        if not mget(S, v1, v3) or not mget(T, v4, v0):
            continue
        if maj(v0 ^ B, v1, w ^ A) != y0:
            continue
        if maj(v3, v4, w) != y3:
            continue
        return True
    return False


def abstract_feasible(target, B, A):
    return boundary(B, A, path(target[1:3]), path(target[4:]), target[0], target[3])


def simple_x(length: int):
    w = length
    private = {}
    cursor = length + 1
    for i in range(length):
        if i not in (0, 3):
            private[i] = cursor
            cursor += 1
    supports = []
    for i in range(length):
        supports.append((i, (i + 1) % length, w if i in (0, 3) else private[i]))
    return cursor, supports


def maj_mask(signs):
    return mask3(lambda x: maj(x[0] ^ signs[0], x[1] ^ signs[1], x[2] ^ signs[2]))


def maj_x_range(B, A):
    n, supports = simple_x(6)
    signs = [(0, 0, 0)] * 6
    signs[0] = (B, 0, A)
    gates = [(supports[i], maj_mask(signs[i])) for i in range(6)]
    return {circuit_out(gates, x) for x in product((0, 1), repeat=n)}


def main() -> None:
    committed = json.loads((ROOT / "RESULTS.json").read_text(encoding="utf-8"))

    groups = {}
    essential_count = unate_count = 0
    for mask in range(256):
        if not all(essential(mask, j) for j in range(3)):
            continue
        essential_count += 1
        if all(direction(mask, j) is not None for j in range(3)):
            unate_count += 1
            groups.setdefault(canon(mask), 0)
            groups[canon(mask)] += 1
    assert essential_count == 218
    assert unate_count == 72
    assert groups == {0x01: 16, 0x07: 48, 0x17: 8}

    for n in range(5, 9):
        gates = strict_singleton(n)
        target = strict_missing(n)
        assert all(circuit_out(gates, x) != target for x in product((0, 1), repeat=n))
        degrees = [sum(v in support for support, _ in gates) for v in range(n)]
        assert min(degrees) >= 3

    rels = {"J": J, "P01": P01, "P10": P10}
    bad = {}
    for B, A in product((0, 1), repeat=2):
        rows = []
        for sn, S in rels.items():
            for tn, T in rels.items():
                for y0, y3 in product((0, 1), repeat=2):
                    if not boundary(B, A, S, T, y0, y3):
                        rows.append([sn, tn, y0, y3])
        bad[f"{B}{A}"] = rows
    assert bad == committed["signed_majority_x"]["abstract_bad_boundary_types"]

    for B, A in product((0, 1), repeat=2):
        brute = maj_x_range(B, A)
        abstract = {y for y in product((0, 1), repeat=6) if abstract_feasible(y, B, A)}
        assert brute == abstract
        expected = 62 if (B, A) == (0, 0) else 64
        assert len(brute) == expected

    print(
        "V99 independent verification passed: independent NPN partition, "
        "singleton conflict family, and signed-MAJ transfer/range audit."
    )


if __name__ == "__main__":
    main()
