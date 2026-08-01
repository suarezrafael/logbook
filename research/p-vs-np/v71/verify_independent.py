#!/usr/bin/env python3
"""Independent bit-mask checks for the V71 width inequalities."""
from __future__ import annotations
import itertools
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent


def boundary(edges, mask):
    left = right = 0
    for i, edge in enumerate(edges):
        bits = sum(1 << v for v in edge)
        if mask >> i & 1:
            left |= bits
        else:
            right |= bits
    return (left & right).bit_count()


def q_of_order(edges, order):
    mask = 0
    answer = 0
    for i in order:
        mask |= 1 << i
        answer = max(answer, boundary(edges, mask))
    return answer


def q_star(edges):
    return min(q_of_order(edges, order) for order in itertools.permutations(range(len(edges))))


def primal(edges, n):
    adj = [0] * n
    for edge in edges:
        for u, v in itertools.combinations(edge, 2):
            adj[u] |= 1 << v
            adj[v] |= 1 << u
    return adj


def pathwidth(edges, n):
    adj = primal(edges, n)
    best = n
    for order in itertools.permutations(range(n)):
        prefix = 0
        width = 0
        for v in order:
            prefix |= 1 << v
            outside = ((1 << n) - 1) ^ prefix
            width = max(width, sum(1 for u in range(n) if prefix >> u & 1 and adj[u] & outside))
        best = min(best, width)
    return best


def main():
    results = json.loads((HERE / "RESULTS.json").read_text())
    assert results["version"] == "V71" and results["failures"] == 0
    rng = random.Random(171071)
    supports = [edge for size in (1, 2, 3) for edge in itertools.combinations(range(4), size)]
    checked = 0
    for _ in range(240):
        edges = tuple(rng.sample(supports, rng.randint(1, 6)))
        q = q_star(edges)
        p = pathwidth(edges, 4)
        rank = max(map(len, edges))
        assert q <= p + 1
        assert p <= q + rank - 1
        checked += 1
    assert "linear branch-width" in (HERE / "README.md").read_text()
    assert "TO_BE_REVIEWED" in (HERE / "ECCC_METADATA.yaml").read_text()
    print(f"V71 independent verification passed: {checked} bit-mask instances; additive width inequalities and nonpublication metadata; zero failures.")


if __name__ == "__main__":
    main()
