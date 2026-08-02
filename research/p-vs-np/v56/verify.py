#!/usr/bin/env python3
"""Repository-complete, read-only verifier for V56."""
from __future__ import annotations

import itertools
import json
import random
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SEED = 560056


def transform(mask, perm, negs, outneg):
    out = 0
    for x in range(8):
        bits = [(x >> i) & 1 for i in range(3)]
        old = [bits[perm[i]] ^ negs[i] for i in range(3)]
        index = old[0] | (old[1] << 1) | (old[2] << 2)
        out |= ((((mask >> index) & 1) ^ outneg) << x)
    return out


def orbit(mask):
    return tuple(
        sorted(
            {
                transform(mask, perm, negs, outneg)
                for perm in itertools.permutations(range(3))
                for negs in itertools.product((0, 1), repeat=3)
                for outneg in (0, 1)
            }
        )
    )


def classes():
    remaining = set(range(256))
    answer = []
    while remaining:
        seed = min(remaining)
        current_orbit = orbit(seed)
        answer.append((min(current_orbit), current_orbit))
        remaining.difference_update(current_orbit)
    return answer


def essential(mask):
    return sum(
        any(((mask >> x) & 1) != ((mask >> (x ^ (1 << variable))) & 1) for x in range(8))
        for variable in range(3)
    )


def affine(points):
    points = set(points)
    if not points:
        return False
    base = next(iter(points))
    linear = {x ^ base for x in points}
    if 0 not in linear or len(linear) & (len(linear) - 1):
        return False
    return all(a ^ b in linear for a in linear for b in linear)


def fiber(mask, value):
    return frozenset(x for x in range(8) if ((mask >> x) & 1) == value)


def orientation(mask):
    for value in (0, 1):
        points = fiber(mask, value)
        if points and affine(points):
            return value, points
    return None


def local(x, support):
    return sum(((x >> variable) & 1) << i for i, variable in enumerate(support))


def active_set(n, mask, support):
    value, _ = orientation(mask)
    return frozenset(
        x for x in range(1 << n) if ((mask >> local(x, support)) & 1) == value
    )


def certificate(n, gates):
    sets = [active_set(n, mask, support) for mask, support in gates]
    universe = set(range(1 << n))
    common = universe.copy()
    for current in sets:
        common &= current
    if not common:
        return "INCONSISTENT", tuple(1 for _ in gates), None
    for index, current in enumerate(sets):
        others = universe.copy()
        for j, candidate in enumerate(sets):
            if index != j:
                others &= candidate
        if others <= current:
            target = [1] * len(gates)
            target[index] = 0
            return "REDUNDANT", tuple(target), index
    raise AssertionError("affine stretch-one family should be inconsistent or redundant")


def output(n, gates, x):
    return tuple((mask >> local(x, support)) & 1 for mask, support in gates)


def absent(n, gates, target):
    return all(output(n, gates, x) != target for x in range(1 << n))


def main():
    rng = random.Random(SEED)
    npn_classes = classes()
    assert len(npn_classes) == 14 and sum(len(current) for _, current in npn_classes) == 256
    canonical = [canonical for canonical, _ in npn_classes]
    assert canonical == [0x00, 0x01, 0x03, 0x06, 0x07, 0x0F, 0x16, 0x17, 0x18, 0x19, 0x1B, 0x1E, 0x3C, 0x69]
    affine_classes = [
        canonical
        for canonical, current_orbit in npn_classes
        if any(orientation(mask) for mask in current_orbit)
    ]
    assert affine_classes == [0x00, 0x01, 0x03, 0x06, 0x0F, 0x18, 0x3C, 0x69]
    essential_affine = [
        canonical
        for canonical, current_orbit in npn_classes
        if essential(canonical) == 3 and any(orientation(mask) for mask in current_orbit)
    ]
    assert essential_affine == [0x01, 0x06, 0x18, 0x69]
    affine_masks = tuple(
        sorted(
            {
                mask
                for canonical, current_orbit in npn_classes
                if canonical in affine_classes
                for mask in current_orbit
            }
        )
    )
    assert len(affine_masks) == 88

    branches = Counter()
    count06 = 0
    for masks in itertools.combinations_with_replacement(orbit(0x06), 4):
        gates = [(mask, (0, 1, 2)) for mask in masks]
        branch, target, _ = certificate(3, gates)
        original = tuple(
            orientation(mask)[0] if active else 1 - orientation(mask)[0]
            for (mask, _), active in zip(gates, target)
        )
        assert absent(3, gates, original)
        branches[branch] += 1
        count06 += 1
    assert count06 == 17550

    count01 = 0
    for masks in itertools.combinations_with_replacement(orbit(0x01), 4):
        gates = [(mask, (0, 1, 2)) for mask in masks]
        branch, target, _ = certificate(3, gates)
        original = tuple(
            orientation(mask)[0] if active else 1 - orientation(mask)[0]
            for (mask, _), active in zip(gates, target)
        )
        assert absent(3, gates, original)
        branches[branch] += 1
        count01 += 1
    assert count01 == 3876

    consistent = 0
    random_mixed = 0
    repeated = 0
    for n in range(3, 13):
        for sample in range(35):
            witness = random.Random(SEED + n + sample).randrange(1 << n)
            gates = []
            for _ in range(n + 1):
                support = tuple(rng.sample(range(n), 3))
                eligible = [
                    mask
                    for mask in affine_masks
                    if local(witness, support) in orientation(mask)[1]
                ]
                gates.append((rng.choice(eligible), support))
            branch, target, _ = certificate(n, gates)
            assert branch == "REDUNDANT"
            original = tuple(
                orientation(mask)[0] if active else 1 - orientation(mask)[0]
                for (mask, _), active in zip(gates, target)
            )
            assert absent(n, gates, original)
            branches[branch] += 1
            consistent += 1

        for _ in range(35):
            gates = [
                (rng.choice(affine_masks), tuple(rng.sample(range(n), 3)))
                for _ in range(n + 1)
            ]
            branch, target, _ = certificate(n, gates)
            original = tuple(
                orientation(mask)[0] if active else 1 - orientation(mask)[0]
                for (mask, _), active in zip(gates, target)
            )
            assert absent(n, gates, original)
            branches[branch] += 1
            random_mixed += 1

    for n in range(2, 9):
        for _ in range(30):
            gates = [
                (rng.choice(affine_masks), tuple(rng.randrange(n) for _ in range(3)))
                for _ in range(n + 1)
            ]
            branch, target, _ = certificate(n, gates)
            original = tuple(
                orientation(mask)[0] if active else 1 - orientation(mask)[0]
                for (mask, _), active in zip(gates, target)
            )
            assert absent(n, gates, original)
            branches[branch] += 1
            repeated += 1

    abstract = 0
    for dimension in range(1, 13):
        for _ in range(60):
            blocks = [
                [rng.randrange(1 << dimension) for _ in range(rng.randrange(4))]
                for _ in range(dimension + 1)
            ]

            def rank(rows):
                pivots = {}
                for raw in rows:
                    value = raw
                    while value:
                        pivot = value.bit_length() - 1
                        if pivot in pivots:
                            value ^= pivots[pivot]
                        else:
                            pivots[pivot] = value
                            break
                return len(pivots)

            total = rank([value for block in blocks for value in block])
            assert any(
                rank(
                    [
                        value
                        for j, block in enumerate(blocks)
                        if j != index
                        for value in block
                    ]
                )
                == total
                for index in range(len(blocks))
            )
            abstract += 1

    computed_validation = {
        "distance_two_exhaustive_multisets_n3_m4": count06,
        "singleton_exhaustive_multisets_n3_m4": count01,
        "consistent_mixed_stretch_one": consistent,
        "unconditioned_mixed_stretch_one": random_mixed,
        "repeated_support_cases": repeated,
        "abstract_block_cases": abstract,
        "failures": 0,
    }

    committed = json.loads((ROOT / "RESULTS.json").read_text(encoding="utf-8"))
    assert committed["version"] == "V56"
    assert committed["status"] == "passed"
    assert committed["seed"] == SEED
    assert committed["classification"]["npn_classes"] == len(npn_classes)
    assert committed["classification"]["affine_orientable_classes"] == len(affine_classes)
    assert committed["classification"]["affine_truth_tables"] == len(affine_masks)
    for key, value in computed_validation.items():
        assert committed["validation"][key] == value, (key, committed["validation"][key], value)

    total_cases = count06 + count01 + consistent + random_mixed + repeated
    committed_branch_counts = committed["validation"]["branch_counts"]
    assert sum(committed_branch_counts.values()) == total_cases
    assert branches["REDUNDANT"] + branches["INCONSISTENT"] == total_cases
    assert committed["validation"]["saved_certificates"] == 20
    assert committed["scientific_status"]["p_vs_np_resolved"] is False

    print("V56 repository-complete verification passed:")
    print("  14/14 NPN classes; 8 affine-orientable; 4 essential affine;")
    print("  17550 distance-two and 3876 singleton multisets;")
    print("  350 consistent + 350 unconditioned mixed circuits;")
    print("  210 repeated-support circuits; 720 block checks; zero failures;")
    print("  stable committed invariants match without rewriting generator-specific splits.")


if __name__ == "__main__":
    main()
