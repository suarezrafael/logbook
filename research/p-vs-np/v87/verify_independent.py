#!/usr/bin/env python3
"""Independent V87 audit without importing the primary implementation."""
from __future__ import annotations

import itertools
import json
import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent

V80_SUPPORTS = {
    "seven_variables": (
        (0, 5, 6), (1, 3, 6), (0, 2, 4), (0, 4, 6),
        (2, 3, 5), (0, 3, 6), (0, 1, 2), (3, 4, 5),
        (2, 4, 5), (1, 5, 6), (2, 4, 6),
    ),
    "eight_variables": (
        (0, 1, 3), (0, 1, 4), (1, 2, 6), (2, 4, 7),
        (2, 3, 5), (0, 3, 7), (0, 3, 5), (1, 3, 6),
        (1, 2, 5), (0, 2, 4), (2, 6, 7), (0, 4, 7),
    ),
    "nine_variables": (
        (2, 3, 7), (2, 5, 7), (4, 5, 8), (0, 3, 6),
        (0, 5, 8), (3, 4, 7), (1, 2, 6), (1, 2, 4),
        (2, 6, 7), (5, 7, 8), (3, 4, 6), (1, 4, 8),
        (0, 1, 5), (0, 5, 6),
    ),
}


def unions_and_connectivity(supports):
    masks = [sum(1 << vertex for vertex in support) for support in supports]
    size = len(masks)
    full = (1 << size) - 1
    unions = [0] * (1 << size)
    for mask in range(1, 1 << size):
        bit = mask & -mask
        index = bit.bit_length() - 1
        unions[mask] = unions[mask ^ bit] | masks[index]
    connectivity = [
        (unions[mask] & unions[full ^ mask]).bit_count()
        for mask in range(1 << size)
    ]
    return unions, connectivity


def balanced_minimum(supports):
    _, connectivity = unions_and_connectivity(supports)
    size = len(supports)
    lower = math.ceil(size / 3)
    upper = (2 * size) // 3
    best = min(
        connectivity[mask]
        for mask in range(1, (1 << size) - 1)
        if lower <= mask.bit_count() <= upper
    )
    count = sum(
        connectivity[mask] == best
        for mask in range(1, (1 << size) - 1)
        if lower <= mask.bit_count() <= upper
    )
    checked = sum(
        lower <= mask.bit_count() <= upper
        for mask in range(1, (1 << size) - 1)
    )
    return best, count, checked


def branchwidth(supports):
    _, connectivity = unions_and_connectivity(supports)
    size = len(supports)
    dp = [0] * (1 << size)
    for index in range(size):
        dp[1 << index] = connectivity[1 << index]
    for cardinality in range(2, size + 1):
        for chosen in itertools.combinations(range(size), cardinality):
            mask = sum(1 << index for index in chosen)
            anchor = mask & -mask
            optimum = 10**9
            sub = (mask - 1) & mask
            while sub:
                if sub != mask and sub & anchor:
                    optimum = min(
                        optimum,
                        max(connectivity[mask], dp[sub], dp[mask ^ sub]),
                    )
                sub = (sub - 1) & mask
            dp[mask] = optimum
    return dp[-1]


def treewidth(vertex_count, supports):
    edges = {
        tuple(sorted(pair))
        for support in supports
        for pair in itertools.combinations(support, 2)
    }
    initial = [0] * vertex_count
    for left, right in edges:
        initial[left] |= 1 << right
        initial[right] |= 1 << left

    optimum = vertex_count

    def recurse(active, adjacency, width):
        nonlocal optimum
        if active == 0:
            optimum = min(optimum, width)
            return
        if width >= optimum:
            return
        vertices = [v for v in range(vertex_count) if active >> v & 1]
        vertices.sort(key=lambda v: (adjacency[v] & active).bit_count())
        for vertex in vertices:
            neighborhood = adjacency[vertex] & active & ~(1 << vertex)
            next_width = max(width, neighborhood.bit_count())
            if next_width >= optimum:
                continue
            updated = adjacency.copy()
            members = [v for v in range(vertex_count) if neighborhood >> v & 1]
            for member in members:
                updated[member] |= neighborhood & ~(1 << member)
            recurse(active & ~(1 << vertex), updated, next_width)

    recurse((1 << vertex_count) - 1, initial, 0)
    return optimum


def sample_supports(n, m, seed):
    rng = random.Random(seed)
    return tuple(rng.sample(tuple(itertools.combinations(range(n), 3)), m))


def main() -> None:
    committed = json.loads((HERE / "RESULTS.json").read_text(encoding="utf-8"))

    pair_counts = {
        pair: 0 for pair in itertools.combinations(range(6), 2)
    }
    for triple in itertools.combinations(range(6), 3):
        for pair in itertools.combinations(triple, 2):
            pair_counts[pair] += 1
    assert set(pair_counts.values()) == {4}
    assert committed["pair_shadow_uniformity"]["uniform"] is True

    transfer_checks = 0
    transfer_equalities = 0
    triples = tuple(itertools.combinations(range(5), 3))
    for gate_count in range(2, 7):
        for supports in itertools.combinations(triples, gate_count):
            bw = branchwidth(supports)
            tw = treewidth(5, supports)
            upper = max(3, math.ceil(3 * bw / 2))
            assert tw + 1 <= upper
            transfer_equalities += tw + 1 == upper
            transfer_checks += 1
    assert transfer_checks == committed["transfer_census"]["families_checked"] == 837
    assert transfer_equalities == committed["transfer_census"]["equality_cases"]

    for name, supports in V80_SUPPORTS.items():
        best, count, checked = balanced_minimum(supports)
        row = committed["v80_balanced_census"][name]
        assert (best, count, checked) == (
            row["minimum_balanced_lambda"],
            row["minimizer_count"],
            row["balanced_subsets_checked"],
        )

    total_balanced = 0
    for row in committed["random_balanced_census"]:
        supports = sample_supports(row["n"], row["m"], row["seed"])
        best, count, checked = balanced_minimum(supports)
        assert best == row["minimum_balanced_lambda"]
        assert count == row["minimizer_count"]
        assert checked == row["balanced_subsets_checked"]
        total_balanced += checked
    assert total_balanced == 17_601_500

    for row in committed["fixed_cut_expectations"]:
        n, m, selected = row["n"], row["m"], row["selected_gates"]
        avoid = (n - 3) / n
        expected = n * (
            1 - avoid**selected - avoid ** (m - selected) + avoid**m
        )
        assert abs(expected - row["expected_lambda"]) < 1e-12

    entropy = -(1 / 3) * math.log(1 / 3) - (2 / 3) * math.log(2 / 3)
    assert abs(
        entropy
        - committed["mcdiarmid_audit"]["balanced_subset_entropy_rate_per_gate"]
    ) < 1e-15
    assert entropy > 2 / 36

    status = committed["scientific_status"]
    assert status["same_family_defeats_hall_syndrome_and_width_certificates"]
    assert not status["explicit_deterministic_three_certificate_family"]
    assert not status["p_vs_np_resolved"]

    print(
        "V87 independent verification passed: uniform pair shadow, 837 transfer "
        "families, 17,601,500 exact balanced cuts, expectation correction, and "
        "the bounded-differences no-go."
    )


if __name__ == "__main__":
    main()
