#!/usr/bin/env python3
"""Independent V57 audit. Does not import v57_core."""
from __future__ import annotations

import itertools
import json
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def transform(mask, perm, negs, outneg):
    out = 0
    for x in range(8):
        new = [(x >> i) & 1 for i in range(3)]
        old = [new[perm[i]] ^ negs[i] for i in range(3)]
        idx = old[0] | (old[1] << 1) | (old[2] << 2)
        out |= ((((mask >> idx) & 1) ^ outneg) << x)
    return out


def orbit(mask):
    return sorted({transform(mask, p, n, o)
                   for p in itertools.permutations(range(3))
                   for n in itertools.product((0, 1), repeat=3)
                   for o in (0, 1)})


def small_set(mask):
    value = 1 if mask.bit_count() == 3 else 0
    return frozenset(x for x in range(8) if ((mask >> x) & 1) == value)


def redundant(sets, universe):
    result = []
    for i, target in enumerate(sets):
        other = set(universe)
        for j, item in enumerate(sets):
            if i != j:
                other &= item
        if other <= target:
            result.append(i)
    return result


def normalized_block(n, p, q, r, forbidden):
    fq, fr = forbidden & 1, (forbidden >> 1) & 1
    return frozenset(x for x in range(1 << n)
                     if ((x >> p) & 1) == 0
                     and not (((x >> q) & 1) == fq and ((x >> r) & 1) == fr))


def normalized_blocks(n):
    unique = {}
    for p in range(n):
        for q, r in itertools.combinations([v for v in range(n) if v != p], 2):
            for forbidden in (1, 2, 3):
                unique[normalized_block(n, p, q, r, forbidden)] = (p, q, r, forbidden)
    return [(desc, block) for block, desc in unique.items()]


def boundary_exists(image):
    m = len(next(iter(image)))
    for point in image:
        for i in range(m):
            neighbor = list(point)
            neighbor[i] ^= 1
            if tuple(neighbor) not in image:
                return True
    return False


def main():
    orbit07 = orbit(0x07)
    assert len(orbit07) == 48

    n3 = Counter()
    for masks in itertools.combinations_with_replacement(orbit07, 4):
        sets = [small_set(mask) for mask in masks]
        common = set(range(8))
        for item in sets:
            common &= item
        if not common:
            n3["inconsistent"] += 1
        elif redundant(sets, range(8)):
            n3["redundant"] += 1
        else:
            n3["irredundant"] += 1
    assert n3 == Counter({"inconsistent": 206280, "redundant": 43620, "irredundant": 0})

    blocks = normalized_blocks(4)
    assert len(blocks) == 36
    hist = Counter()
    for family in itertools.combinations(blocks, 5):
        sets = [item[1] for item in family]
        hist[len(redundant(sets, range(16)))] += 1
    assert hist == Counter({0: 12, 1: 228, 2: 8088, 3: 87804, 4: 194712, 5: 86148})

    descriptions = [(0,1,2,1),(0,1,2,2),(0,1,3,1),(0,1,3,2),(0,2,3,3)]
    sets = [normalized_block(4, *d) for d in descriptions]
    common = set(range(16))
    for item in sets:
        common &= item
    assert common == {0}
    assert redundant(sets, range(16)) == []
    expected_witnesses = [10,4,6,8,14]
    for i, witness in enumerate(expected_witnesses):
        assert witness not in sets[i]
        assert all(witness in sets[j] for j in range(5) if j != i)

    boundary_checks = 0
    for m in range(1,5):
        cube = [tuple((x >> i) & 1 for i in range(m)) for x in range(1 << m)]
        for subset_mask in range(1, (1 << (1 << m)) - 1):
            image = {cube[i] for i in range(1 << m) if (subset_mask >> i) & 1}
            assert boundary_exists(image)
            boundary_checks += 1
    assert boundary_checks == 65804

    primary = json.loads((ROOT / "RESULTS.json").read_text(encoding="utf-8"))
    assert primary["validation"]["proper_cube_subsets_checked"] == boundary_checks
    assert primary["validation"]["n4_normalized_families"]["consistent_irredundant_families"] == 12

    independent = {
        "status": "passed",
        "n3_multisets": math.comb(51,4),
        "n4_normalized_families": math.comb(36,5),
        "n4_irredundant": hist[0],
        "boundary_subsets": boundary_checks,
        "explicit_gadget_witnesses": expected_witnesses,
        "failures": 0,
    }
    (ROOT / "INDEPENDENT_RESULTS.json").write_text(json.dumps(independent, indent=2), encoding="utf-8")
    print("V57 independent verification passed:")
    print("  249900 n=3 orbit multisets independently rebuilt;")
    print("  376992 normalized n=4 families independently rebuilt; 12 irredundant;")
    print("  explicit five-block gadget and witnesses reconstructed;")
    print(f"  {boundary_checks} proper cube subsets checked; zero failures.")


if __name__ == "__main__":
    main()
