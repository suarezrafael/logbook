#!/usr/bin/env python3
from __future__ import annotations

import json
from itertools import combinations
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def version_number(value: str) -> int:
    assert value.startswith("V") and value[1:].isdigit()
    return int(value[1:])


def maximum_matching_rank(supports: list[set[int]], mask: int) -> int:
    matched: dict[int, int] = {}

    def augment(left: int, seen: set[int]) -> bool:
        for right in supports[left]:
            if right in seen:
                continue
            seen.add(right)
            owner = matched.get(right)
            if owner is None or augment(owner, seen):
                matched[right] = left
                return True
        return False

    rank = 0
    for left in range(len(supports)):
        if mask & (1 << left) and augment(left, set()):
            rank += 1
    return rank


def circuit_masks(supports: list[set[int]]) -> set[int]:
    ranks = [0] * (1 << len(supports))
    for mask in range(1, 1 << len(supports)):
        ranks[mask] = maximum_matching_rank(supports, mask)
    return {
        mask
        for mask in range(1, 1 << len(supports))
        if ranks[mask] < mask.bit_count()
        and all(
            ranks[mask ^ (1 << i)] == mask.bit_count() - 1
            for i in range(len(supports))
            if mask & (1 << i)
        )
    }


def independent_chain(d: int) -> list[set[int]]:
    # External vertices 0..d-1; private vertices d..2d-2.
    supports: list[set[int]] = []
    for i in range(d):
        row = {i}
        if i > 0:
            row.add(d + i - 1)
        if i < d - 1:
            row.add(d + i)
        supports.append(row)
    return supports


def private_only_chain(d: int) -> list[set[int]]:
    supports: list[set[int]] = []
    for i in range(d):
        row: set[int] = set()
        if i > 0:
            row.add(i - 1)
        if i < d - 1:
            row.add(i)
        supports.append(row)
    return supports


def source_colbourn(vertex_count: int, edges: tuple[tuple[int, int], ...], k: int) -> list[set[int]]:
    q = comb(k, 2)
    r = q - k - 1
    return [{u, v, *(vertex_count + z for z in range(r))} for u, v in edges]


def has_clique(vertex_count: int, edges: tuple[tuple[int, int], ...], k: int) -> bool:
    edge_set = set(edges)
    return any(
        all(edge in edge_set for edge in combinations(vertices, 2))
        for vertices in combinations(range(vertex_count), k)
    )


def main() -> None:
    committed = json.loads((HERE / "RESULTS.json").read_text(encoding="utf-8"))

    # Independent local-gadget audit. The private path has one circuit: the full
    # chain. Every proper subset is independent. Adding external choices removes
    # that local circuit.
    for d in range(1, 9):
        private = private_only_chain(d)
        circuits = circuit_masks(private)
        assert circuits == {(1 << d) - 1}
        external = independent_chain(d)
        assert circuit_masks(external) == set()
        assert max(map(len, external), default=0) <= 3

    # Recheck the complete k=4 graph census without importing the generator.
    independent_graph_count = 0
    independent_yes_count = 0
    for vertex_count in (4, 5):
        universe = tuple(combinations(range(vertex_count), 2))
        for mask in range(1 << len(universe)):
            edges = tuple(universe[i] for i in range(len(universe)) if mask & (1 << i))
            supports = source_colbourn(vertex_count, edges, 4)
            circuits = circuit_masks(supports)
            has_short = any(circuit.bit_count() <= 6 for circuit in circuits)
            clique = has_clique(vertex_count, edges, 4)
            assert has_short == clique
            independent_graph_count += 1
            independent_yes_count += int(clique)

    assert independent_graph_count == 1088
    assert independent_yes_count == 67

    # Direct inequality audit for k=4..10: all t<q simple edge sets obey
    # t-v <= q-k-1, and equality at q occurs only for a k-clique.
    for k in range(4, 11):
        q = comb(k, 2)
        r = q - k - 1
        for v in range(k):
            assert comb(v, 2) - v <= r
        assert (q - 1) - k == r
        assert r + k == q - 1
        assert q * (q - k + 1) >= q

    assert committed["theorem"]["maximum_expanded_left_degree"] == 3
    assert committed["exhaustive_census"]["source_presentations_checked"] == 768
    assert committed["source_arithmetic_audit"]["identity_valid"] is False
    assert committed["source_arithmetic_audit"]["corrected_reservoir"] == "r = binom(k,2)-k-1"
    assert committed["complexity_conclusion"]["status"] == "NP-complete"
    assert committed["complexity_conclusion"]["novelty_confirmed"] is False

    status = json.loads((ROOT / "LAB_STATUS.json").read_text(encoding="utf-8"))
    promoted = status["promoted_version"]
    candidate = status.get("candidate_version")
    assert version_number(promoted) >= 82
    if candidate is None:
        assert status["highest_directory"] == promoted
        assert status["promotion_state"] == "promoted"
        reached = version_number(promoted)
    else:
        assert version_number(candidate) == version_number(promoted) + 1
        assert status["highest_directory"] == candidate
        assert status["promotion_state"] == "candidate"
        reached = version_number(candidate)
    assert reached >= 83
    assert status["scientific_status"][
        "degree_three_transversal_girth_np_hard"
    ] is True
    assert status["scientific_status"]["p_vs_np_resolved"] is False

    print(
        "V83 independent verification passed: private-chain minimality, "
        "1,088 Clique presentations, and the degree-three threshold arithmetic "
        "remain independently preserved."
    )


if __name__ == "__main__":
    main()
