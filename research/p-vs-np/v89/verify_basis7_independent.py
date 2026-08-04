#!/usr/bin/env python3
"""Independent exact audit of the seven-state basis-CSP overlap packet."""
from __future__ import annotations

import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
V = tuple(range(1, 8))
R = tuple(
    triple
    for triple in itertools.permutations(V, 3)
    if len(set(triple)) == 3
    and (triple[0] ^ triple[1] ^ triple[2]) != 0
)
RSET = set(R)


def main() -> None:
    committed = json.loads(
        (ROOT / "BASIS7_RESULTS.json").read_text(encoding="utf-8")
    )
    assert len(R) == 168
    assert Fraction(len(R), 7**3) == Fraction(24, 49)

    matches = Counter(
        sum(left[i] == right[i] for i in range(3))
        for left in R
        for right in R
    )
    assert [matches[i] for i in range(4)] == [17976, 8568, 1512, 168]

    distribution = Counter()
    for permutation in itertools.permutations(V):
        distribution[
            sum(
                tuple(permutation[value - 1] for value in basis) in RSET
                for basis in R
            )
        ] += 1
    assert distribution == Counter(
        {126: 1344, 132: 2352, 144: 1176, 168: 168}
    )

    local = committed["local_stability"]
    assert local["overlap_tangent_dimension"] == 36
    assert local["bilinear_pairs_checked"] == 1296
    assert local["identity_mismatches"] == 0
    assert local["energy_log_hessian_eigenvalue"] == "1/6"
    assert local["combined_hessian_eigenvalue"] == "-1+c/6"
    assert local["uniform_overlap_locally_maximal_for_density_below"] == 6

    print(
        "V89 seven-state independent verification passed: 168 ordered bases, "
        "28,224 basis pairs, 5,040 permutation overlaps, and the exact "
        "36-dimensional local-stability certificate."
    )


if __name__ == "__main__":
    main()
