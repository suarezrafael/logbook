#!/usr/bin/env python3
"""Explicit stretch-one spine family for Laboratory V68.

Local truth-table convention
----------------------------
For local coordinates `(a,b,c)`, the truth-table index is `4a+2b+c`.
Thus mask `0x07` has positive fiber `{000,001,010}` and pins `a=0`.

Construction
------------
Variables are one shared spine `s` and `k` fresh pairs `(u_t,v_t)`, so
`n=2k+1`. Each motif contributes two gates on `(s,u_t,v_t)` and
`(s,v_t,u_t)`, both using the partition

    {000}  dot-union  {001,010}.

The two cells are affine. The first gives branch bit 0 and the second branch
bit 1. Two anchors on motif 0 use the orbit-equivalent masks `0x0b` and
`0x0d`, partitioned as singleton `000` plus the complementary affine line.
Their intersection with the motif fiber leaves only `000`. Hence motif 0 is
frozen, while every motif t>=1 contributes exactly two independent complete
branch choices. Therefore

    c(S_k) = 2^(k-1) = 2^((n-3)/2).

The output count is `m=2k+2=n+1`.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

from affine_bitset import build_projected_ordered_dag, row, satisfies

HERE = Path(__file__).resolve().parent
MOTIF_MASK = 0x07
ANCHOR_MASKS = (0x0B, 0x0D)


def transform_mask(mask: int, permutation, negations, output_flip: int) -> int:
    result = 0
    for target in range(8):
        bits = (
            (target >> 2) & 1,
            (target >> 1) & 1,
            target & 1,
        )
        source_bits = tuple(bits[permutation[i]] ^ negations[i] for i in range(3))
        source = (source_bits[0] << 2) | (source_bits[1] << 1) | source_bits[2]
        result |= ((((mask >> source) & 1) ^ output_flip) << target)
    return result


def npn_orbit(mask: int) -> frozenset[int]:
    return frozenset(
        transform_mask(mask, permutation, negations, output_flip)
        for permutation in itertools.permutations(range(3))
        for negations in itertools.product((0, 1), repeat=3)
        for output_flip in (0, 1)
    )


def make_gate(name: str, mask: int, support: tuple[int, int, int], cells):
    return {
        "name": name,
        "mask": mask,
        "support": support,
        "cells": tuple(tuple(cell) for cell in cells),
    }


def motif_gates(n: int, t: int):
    s = 0
    u = 1 + 2 * t
    v = 2 + 2 * t
    zero = (
        row(n, (s,), 0),
        row(n, (u,), 0),
        row(n, (v,), 0),
    )
    one_hot = (
        row(n, (s,), 0),
        row(n, (u, v), 1),
    )
    cells = (zero, one_hot)
    return (
        make_gate(f"M{t}a", MOTIF_MASK, (s, u, v), cells),
        make_gate(f"M{t}b", MOTIF_MASK, (s, v, u), cells),
    )


def anchor_gates(n: int):
    s, u, v = 0, 1, 2
    singleton = (
        row(n, (s,), 0),
        row(n, (u,), 0),
        row(n, (v,), 0),
    )
    mask_0b_line = (row(n, (s,), 0), row(n, (v,), 1))
    mask_0d_line = (row(n, (s,), 0), row(n, (u,), 1))
    return (
        make_gate("A0b", 0x0B, (s, u, v), (singleton, mask_0b_line)),
        make_gate("A0d", 0x0D, (s, u, v), (singleton, mask_0d_line)),
    )


def spine_family(k: int) -> dict:
    if k < 1:
        raise ValueError("k must be positive")
    n = 2 * k + 1
    gates = list(motif_gates(n, 0))
    gates.extend(anchor_gates(n))
    for t in range(1, k):
        gates.extend(motif_gates(n, t))
    assert len(gates) == 2 * k + 2 == n + 1
    return {
        "k": k,
        "n": n,
        "m": len(gates),
        "variables": {
            "spine": 0,
            "pairs": [[1 + 2 * t, 2 + 2 * t] for t in range(k)],
        },
        "gates": tuple(gates),
    }


def cell_membership(gate: dict, branch: int, assignment: int, n: int) -> bool:
    return satisfies(gate["cells"][branch], assignment, n)


def brute_force_signatures(k: int) -> frozenset[int]:
    family = spine_family(k)
    n = family["n"]
    signatures = set()
    for assignment in range(1 << n):
        signature = 0
        for index, gate in enumerate(family["gates"]):
            if cell_membership(gate, 0, assignment, n):
                continue
            if cell_membership(gate, 1, assignment, n):
                signature |= 1 << index
                continue
            break
        else:
            signatures.add(signature)
    return frozenset(signatures)


def formula_count(k: int) -> int:
    return 1 << (k - 1)


def projected_dag_metrics(k: int) -> dict:
    family = spine_family(k)
    dag = build_projected_ordered_dag(family["gates"], family["n"])
    return {
        "nonterminal_states": dag["nonterminal_states"],
        "total_nodes_with_terminals": dag["total_nodes_with_terminals"],
        "expected_nonterminal_states": 3 * k + 4,
    }


def analyze_v67_c36() -> dict:
    specs = [
        {"partition": 2, "support": [2, 7, 4]},
        {"partition": 2, "support": [8, 4, 7]},
        {"partition": 0, "support": [10, 2, 7]},
        {"partition": 1, "support": [5, 9, 4]},
        {"partition": 0, "support": [6, 1, 7]},
        {"partition": 0, "support": [5, 3, 6]},
        {"partition": 1, "support": [6, 8, 4]},
        {"partition": 2, "support": [7, 0, 6]},
        {"partition": 2, "support": [7, 4, 0]},
        {"partition": 0, "support": [1, 2, 6]},
        {"partition": 2, "support": [2, 8, 7]},
        {"partition": 0, "support": [0, 10, 7]},
    ]
    signatures = [
        0, 8, 32, 40, 66, 74, 98, 106, 528, 536, 560, 568, 594, 602,
        626, 634, 1541, 1549, 1573, 1581, 2052, 2060, 2084, 2092,
        2118, 2126, 2150, 2158, 2580, 2588, 2612, 2620, 2646, 2654,
        2678, 2686,
    ]
    position_counts = [Counter() for _ in range(3)]
    for specification in specs:
        for position, variable in enumerate(specification["support"]):
            position_counts[position][variable] += 1
    frozen = [
        bit
        for bit in range(12)
        if len({(signature >> bit) & 1 for signature in signatures}) == 1
    ]
    independent = []
    for bit in range(12):
        fibers = {}
        for signature in signatures:
            branch = (signature >> bit) & 1
            deleted = (signature & ((1 << bit) - 1)) | ((signature >> (bit + 1)) << bit)
            fibers.setdefault(deleted, set()).add(branch)
        if len(fibers) == 18 and all(values == {0, 1} for values in fibers.values()):
            independent.append(bit)
    never_pinned = sorted(set(range(11)) - set(position_counts[0]))
    assert frozen == [7, 8]
    assert independent == [3, 5]
    assert never_pinned == [3, 4, 9]
    return {
        "signature_count": len(signatures),
        "frozen_gate_indices": frozen,
        "independent_factor_gate_indices": independent,
        "factorization": "2 x 18",
        "variables_never_in_pinned_position": never_pinned,
        "position_counts": [
            {str(variable): count for variable, count in sorted(counter.items())}
            for counter in position_counts
        ],
        "partition_distribution": {
            str(key): value
            for key, value in sorted(Counter(item["partition"] for item in specs).items())
        },
    }


def generate_results() -> dict:
    orbit = npn_orbit(MOTIF_MASK)
    assert len(orbit) == 48
    assert all(mask in orbit for mask in ANCHOR_MASKS)
    exact = []
    for k in range(1, 6):
        signatures = brute_force_signatures(k)
        expected = formula_count(k)
        assert len(signatures) == expected
        metrics = projected_dag_metrics(k)
        assert metrics["nonterminal_states"] == metrics["expected_nonterminal_states"]
        exact.append(
            {
                "k": k,
                "n": 2 * k + 1,
                "m": 2 * k + 2,
                "c": len(signatures),
                "tree_leaf_lower_bound": len(signatures),
                "G_proj_nonterminal": metrics["nonterminal_states"],
                "G_proj_total_with_terminals": metrics["total_nodes_with_terminals"],
            }
        )
    symbolic = []
    for k in range(1, 65):
        metrics = projected_dag_metrics(k)
        assert metrics["nonterminal_states"] == 3 * k + 4
        symbolic.append(
            {
                "k": k,
                "n": 2 * k + 1,
                "m": 2 * k + 2,
                "c_formula": formula_count(k),
                "G_proj_nonterminal": metrics["nonterminal_states"],
            }
        )
    return {
        "version": "V68",
        "status": "passed",
        "construction": {
            "n": "2k+1",
            "m": "2k+2=n+1",
            "consistent_complete_branches": "2^(k-1)=2^((n-3)/2)",
            "gate_masks": ["0x07", "0x0b", "0x0d"],
            "all_masks_in_npn_orbit_0x07": True,
        },
        "theorem": {
            "tree_lower_bound": "L_aff >= c = 2^(k-1)",
            "projected_ordered_dag_upper_bound": "G_proj <= 3k+4 nonterminal states",
            "separation": "exponential complete-branch tree lower bound versus linear explicit projected residual DAG",
        },
        "exact_bruteforce": exact,
        "symbolic_and_dag_checks": {
            "k_range": [1, 64],
            "cases": symbolic,
        },
        "c36_structure": analyze_v67_c36(),
        "scientific_status": {
            "explicit_exponential_tree_family_proved": True,
            "projected_dag_linear_for_spine_family": True,
            "general_polynomial_projected_dag_proved": False,
            "standard_obdd_fbdd_simulation_proved": False,
            "unrestricted_nc0_3_avoid_solved": False,
            "circuit_lower_bound_proved": False,
            "p_vs_np_route_active": False,
            "p_vs_np_resolved": False,
            "peer_reviewed": False,
            "novelty_confirmed": False,
        },
        "failures": 0,
    }


def main():
    results = generate_results()
    (HERE / "RESULTS.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
    print(
        "V68 spine verification passed: exact k=1..5; symbolic and projected-DAG "
        "checks k=1..64; c=2^(k-1); G_proj=3k+4; zero failures."
    )


if __name__ == "__main__":
    main()
