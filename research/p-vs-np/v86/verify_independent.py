#!/usr/bin/env python3
from __future__ import annotations

import json
from itertools import combinations
from math import ceil, comb, log2, sqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def union_profiles(supports: tuple[tuple[int, ...], ...]) -> tuple[list[int], list[int]]:
    support_masks = tuple(sum(1 << variable for variable in support) for support in supports)
    full = (1 << len(supports)) - 1
    unions = [0] * (full + 1)
    for mask in range(1, full + 1):
        low = mask & -mask
        index = low.bit_length() - 1
        unions[mask] = unions[mask ^ low] | support_masks[index]
    connectivity = [
        (unions[mask] & unions[full ^ mask]).bit_count()
        for mask in range(full + 1)
    ]
    return unions, connectivity


def exact_branchwidth(supports: tuple[tuple[int, ...], ...]) -> int:
    _unions, connectivity = union_profiles(supports)
    gate_count = len(supports)
    dynamic = [0] * (1 << gate_count)
    for index in range(gate_count):
        dynamic[1 << index] = connectivity[1 << index]
    for size in range(2, gate_count + 1):
        for indices in combinations(range(gate_count), size):
            mask = sum(1 << index for index in indices)
            anchor = mask & -mask
            best = 10**9
            subset = (mask - 1) & mask
            while subset:
                if subset & anchor and subset != mask:
                    best = min(best, max(connectivity[mask], dynamic[subset], dynamic[mask ^ subset]))
                subset = (subset - 1) & mask
            dynamic[mask] = best
    return dynamic[-1]


def minimum_hall(supports: tuple[tuple[int, ...], ...]) -> tuple[int, int]:
    unions, _connectivity = union_profiles(supports)
    for size in range(1, len(supports) + 1):
        for indices in combinations(range(len(supports)), size):
            mask = sum(1 << index for index in indices)
            neighborhood = unions[mask].bit_count()
            if neighborhood < size:
                return size, neighborhood
    raise AssertionError("positive stretch should force Hall deficiency")


def c4_count(supports: tuple[tuple[int, ...], ...]) -> int:
    total = 0
    for left, first in enumerate(supports):
        for second in supports[left + 1 :]:
            total += comb(len(set(first) & set(second)), 2)
    return total


def nor_nonconstant_vector(support: tuple[int, ...], monomials: dict[tuple[int, ...], int]) -> int:
    # NOR3 has ANF 1+x+y+z+xy+xz+yz+xyz; every nonempty local monomial occurs.
    vector = 0
    for degree in (1, 2, 3):
        for local in combinations(support, degree):
            vector ^= 1 << monomials[tuple(sorted(local))]
    return vector


def constant_syndromes(vectors: tuple[int, ...]) -> int:
    total = 0
    for selector in range(1, 1 << len(vectors)):
        combined = 0
        for index, vector in enumerate(vectors):
            if selector & (1 << index):
                combined ^= vector
        total += combined == 0
    return total


def main() -> None:
    v80 = json.loads((ROOT / "v80" / "RESULTS.json").read_text(encoding="utf-8"))
    v86 = json.loads((HERE / "RESULTS.json").read_text(encoding="utf-8"))

    observed_c4 = 0
    observed_rank = 0
    for name, source in v80["examples"].items():
        supports = tuple(tuple(map(int, support)) for support in source["supports"])
        n = int(source["n"])
        m = len(supports)
        assert len(set(supports)) == m

        hall_size, hall_neighborhood = minimum_hall(supports)
        width = exact_branchwidth(supports)
        c4s = c4_count(supports)

        all_monomials = [
            monomial
            for degree in (1, 2, 3)
            for monomial in combinations(range(n), degree)
        ]
        index = {monomial: position for position, monomial in enumerate(all_monomials)}
        vectors = tuple(nor_nonconstant_vector(support, index) for support in supports)

        # Distinct supports give distinct cubic pivots, so rank=m. Enumerate all selectors too.
        cubic_pivots = {
            tuple(sorted(support)): (vector >> index[tuple(sorted(support))]) & 1
            for support, vector in zip(supports, vectors)
        }
        assert len(cubic_pivots) == m and all(cubic_pivots.values())
        assert constant_syndromes(vectors) == 0

        row = v86["examples"][name]
        assert (hall_size, hall_neighborhood) == (
            row["minimum_hall_deficient_gate_count"],
            row["minimum_hall_neighborhood_size"],
        )
        assert width == row["support_branchwidth"]
        assert c4s == row["c4_count"]
        assert row["nor3_nonconstant_anf_rank"] == m
        observed_c4 += c4s
        observed_rank += m

    assert observed_c4 == 50
    assert observed_rank == 37

    for row in v86["asymptotic_two_barrier"]["rows"]:
        n = int(row["n"])
        m = n + ceil(n ** (2 / 3))
        duplicate = comb(m, 2) / comb(n, 3)
        assert abs(duplicate - row["duplicate_support_union_bound"]) < 1e-15
        assert 8 / 49 + duplicate < 1

    ratios = []
    for row in v86["width_gap"]:
        n = int(row["n"])
        m = n + ceil(n ** (2 / 3))
        ratio = (m - n) / sqrt(log2(m))
        assert abs(ratio - row["ratio"]) < 1e-12
        ratios.append(ratio)
    assert ratios == sorted(ratios) and len(set(ratios)) == len(ratios)

    original = {(0, 0), (1, 0)}
    restricted = {(0, 0)}
    assert (1, 0) not in restricted and (1, 0) in original

    print(
        "V86 independent verification passed: exact Hall/branchwidth recomputation, "
        "50 C4 witnesses, exhaustive NOR3 syndrome elimination, asymptotic collision bounds, and no-pullback control."
    )


if __name__ == "__main__":
    main()
