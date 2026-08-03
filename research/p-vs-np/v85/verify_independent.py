#!/usr/bin/env python3
from __future__ import annotations

from itertools import combinations, product
from math import comb
from pathlib import Path
import sys

from distance_semiring import (
    build_v75_model,
    distance_polynomial,
    remote_point_from_v75_model,
)

ROOT = Path(__file__).resolve().parent
V74 = str(ROOT.parent / "v74")
if V74 not in sys.path:
    sys.path.insert(0, V74)
from two_fiber_model import brute_preimage_counts, make_gate

PARAMETERS = ((8, 12), (27, 36), (64, 80), (125, 150), (216, 252), (343, 392), (512, 576), (1000, 1100))
REMOTE_CASES = ((4, 8, 851001), (4, 9, 851002), (5, 10, 851003), (5, 11, 851004), (6, 12, 851005), (6, 13, 851006), (5, 9, 851007), (6, 11, 851008))


def bit(mask: int, x: int) -> int:
    return (mask >> x) & 1


def walsh(mask: int, subset: int) -> int:
    return sum((1 - 2 * bit(mask, x)) * (1 - 2 * (((x & subset).bit_count()) & 1)) for x in range(8))


def essential(mask: int, variable: int) -> bool:
    return any(bit(mask, x) != bit(mask, x ^ (1 << variable)) for x in range(8))


def xorshift(seed: int, count: int) -> list[int]:
    state = seed & 0xFFFFFFFF
    out = []
    for _ in range(count):
        state ^= (state << 13) & 0xFFFFFFFF
        state ^= state >> 17
        state ^= (state << 5) & 0xFFFFFFFF
        out.append(state & 0xFF)
    return out


def eval_gate(support: tuple[int, ...], truth: int, x: int) -> int:
    address = sum(((x >> v) & 1) << j for j, v in enumerate(support))
    return bit(truth, address)


def ball(m: int, r: int) -> int:
    return sum(comb(m, j) for j in range(r + 1)) if r >= 0 else 0


def exact_distance_coefficients(
    counts: dict[int, int], m: int, prefix: tuple[int, ...], radius: int
) -> tuple[int, ...]:
    exact = [0] * (radius + 1)
    remaining = m - len(prefix)
    for output, multiplicity in counts.items():
        mismatch = sum(bit_value != ((output >> i) & 1) for i, bit_value in enumerate(prefix))
        for tail_distance in range(remaining + 1):
            distance = mismatch + tail_distance
            if distance <= radius:
                exact[distance] += multiplicity * comb(remaining, tail_distance)
    return tuple(exact)


def verify_v75_semiring_independently() -> tuple[int, int, int]:
    supports = ((0,), (1,), (2,), (0, 1), (0, 2), (1, 2), (0, 1, 2))
    coefficient_checks = remote_points = 0
    for case in range(8):
        raw = xorshift(852000 + case, 21)
        gates = []
        for i, support in enumerate(supports):
            arity = len(support)
            truth_mask = raw[i] % (1 << (1 << arity))
            gates.append(make_gate(list(support), truth_mask, raw[7 + i] & 1))
        model = build_v75_model(3, gates)
        counts = brute_preimage_counts(3, gates)
        for length in range(8):
            for value in range(min(1 << length, 4)):
                prefix = tuple((value >> i) & 1 for i in range(length))
                expected = exact_distance_coefficients(counts, 7, prefix, 2)
                assert distance_polynomial(model, prefix, 2) == expected
                coefficient_checks += 1
        remote = remote_point_from_v75_model(model, 1)
        target = int(remote["target_integer"])
        assert min((output ^ target).bit_count() for output in counts) > 1
        remote_points += 1
    return 8, coefficient_checks, remote_points


def main() -> None:
    counts = [0, 0, 0]
    profiles: dict[tuple[int, int, tuple[int, ...]], int] = {}
    for mask in range(256):
        coeffs = [walsh(mask, subset) for subset in range(8)]
        affine = any(abs(value) == 8 for value in coeffs)
        balanced = mask.bit_count() == 4
        if affine:
            counts[0] += 1
        elif not balanced:
            counts[1] += 1
        else:
            counts[2] += 1
            low = [abs(coeffs[s]) for s in range(1, 8) if s.bit_count() <= 2 and coeffs[s]]
            assert max(low) == 4
            profile = (len(low), abs(coeffs[7]), tuple(sorted(low)))
            profiles[profile] = profiles.get(profile, 0) + 1
    assert counts == [16, 184, 56]
    assert profiles == {(3, 4, (4, 4, 4)): 32, (4, 0, (4, 4, 4, 4)): 24}

    for a, b in product((0, 1), repeat=2):
        assert any(bit(mask, 0) == a and bit(mask, 7) == b and all(essential(mask, v) for v in range(3)) for mask in range(256))
    for n, m in PARAMETERS:
        q = 8 * m
        k = q // (m - n) + 1
        assert k * (m - n) > q >= (k - 1) * (m - n)

    supports = ((0, 1, 2), (0, 1, 3), (2, 4, 5), (3, 4, 5), (0, 1, 4), (0, 1, 5), (0, 2, 3))

    def truth(terms: tuple[int, ...]) -> int:
        return sum((sum((x & term) == term for term in terms) & 1) << x for x in range(8))

    truths = (truth((0b011, 0b100)), truth((0b011, 0b100)), truth((1, 2, 4)), truth((1, 2, 4)), truth((1, 2, 4)), truth((1, 2, 4)), truth((1, 2, 4)))
    for x in range(1 << 6):
        assert sum(eval_gate(supports[i], truths[i], x) for i in range(4)) % 2 == 0
    for r in range(1, 7):
        for indices in combinations(range(7), r):
            assert len(set().union(*(set(supports[i]) for i in indices))) >= r

    for n, m, seed in REMOTE_CASES:
        triples = list(combinations(range(n), min(3, n)))
        masks = xorshift(seed, m)
        gates = [(triples[(seed * 17 + i * 7) % len(triples)], masks[i]) for i in range(m)]
        image = []
        for x in range(1 << n):
            y = sum(eval_gate(support, mask, x) << i for i, (support, mask) in enumerate(gates))
            image.append(y)
        radius = -1
        for r in range(m + 1):
            if (1 << n) * ball(m, r) < (1 << m):
                radius = r
            else:
                break
        assert any(min((y ^ z).bit_count() for y in image) > radius for z in range(1 << m))

    models, coefficient_checks, v75_remote_points = verify_v75_semiring_independently()
    assert (models, coefficient_checks, v75_remote_points) == (8, 248, 8)

    print("V85 independent verification passed: direct Walsh census, C4 witness, exhaustive remote existence, and 248 V75 distance coefficients.")


if __name__ == "__main__":
    main()
