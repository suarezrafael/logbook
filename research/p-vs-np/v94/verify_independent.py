#!/usr/bin/env python3
from __future__ import annotations

"""Independent semantic verifier for V94.

This file intentionally imports neither child_count_comparison.py nor its helper
functions. It reconstructs the two finite theorem controls directly.
"""

import json
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def lit_value(x: int, lit: int) -> int:
    bit = (x >> (abs(lit) - 1)) & 1
    return bit if lit > 0 else 1 - bit


def source_count(n: int, clause: tuple[int, int, int]) -> int:
    return sum(any(lit_value(x, lit) for lit in clause) for x in range(1 << n))


def compile_one_clause_pair(c0, c1):
    s = 2
    z0, z1 = 3, 4
    gates = [
        ("def", z0, c0[1], c0[2]),
        ("cond", s, 0, c0[0], z0),
        ("def", z1, c1[1], c1[2]),
        ("cond", s, 1, c1[0], z1),
        ("proj", s),
        ("proj", 0),
    ]
    assert len(gates) == 6 == 5 + 1
    return gates


def eval_gate(gate, x: int) -> int:
    if gate[0] == "proj":
        return (x >> gate[1]) & 1
    if gate[0] == "def":
        _, z, a, b = gate
        return int(((x >> z) & 1) == (lit_value(x, a) | lit_value(x, b)))
    _, s, active, a, z = gate
    if ((x >> s) & 1) != active:
        return 1
    return int(lit_value(x, a) | ((x >> z) & 1))


def child_counts(gates) -> tuple[int, int]:
    counts = [0, 0]
    for x in range(1 << 5):
        if all(eval_gate(gates[i], x) == 1 for i in range(4)):
            counts[eval_gate(gates[4], x)] += 1
    return counts[0], counts[1]


def independent_reduction_audit() -> tuple[int, int, int, int]:
    clauses = tuple(product((1, -1, 2, -2), repeat=3))
    pairs = mismatches = strict_pairs = equal_pairs = 0
    for c0 in clauses:
        a = source_count(2, c0)
        for c1 in clauses:
            b = source_count(2, c1)
            if child_counts(compile_one_clause_pair(c0, c1)) != (a, b):
                mismatches += 1
            pairs += 1
            strict_pairs += int(a != b)
            equal_pairs += int(a == b)
    return pairs, mismatches, strict_pairs, equal_pairs


def affine_eval(mask: int, constant: int, x: int) -> int:
    return constant ^ ((mask & x).bit_count() & 1)


def rank_or_inconsistent(equations) -> tuple[int, bool]:
    basis = {}
    rank = 0
    for mask, rhs in equations:
        while mask:
            pivot = mask.bit_length() - 1
            if pivot in basis:
                bm, br = basis[pivot]
                mask ^= bm
                rhs ^= br
            else:
                basis[pivot] = (mask, rhs)
                rank += 1
                break
        if mask == 0 and rhs:
            return rank, True
    return rank, False


def linear_count(equations) -> int:
    rank, bad = rank_or_inconsistent(equations)
    return 0 if bad else 1 << (3 - rank)


def independent_affine_audit() -> tuple[int, int, int]:
    functions = tuple((mask, c) for mask in range(8) for c in (0, 1))
    circuits = mismatches = in_range = 0
    for gates in product(functions, repeat=4):
        prefix = []
        for j, (mask, constant) in enumerate(gates):
            prior = [(gates[i][0], prefix[i] ^ gates[i][1]) for i in range(j)]
            exact = (
                linear_count(prior + [(mask, constant)]),
                linear_count(prior + [(mask, 1 ^ constant)]),
            )
            brute = [0, 0]
            for x in range(8):
                values = [affine_eval(m, c, x) for m, c in gates]
                if values[:j] == prefix:
                    brute[values[j]] += 1
            mismatches += int(exact != tuple(brute))
            prefix.append(0 if exact[0] <= exact[1] else 1)
        target = tuple(prefix)
        in_range += int(
            any(tuple(affine_eval(m, c, x) for m, c in gates) == target for x in range(8))
        )
        circuits += 1
    return circuits, mismatches, in_range


def main() -> None:
    committed = json.loads((ROOT / "RESULTS.json").read_text(encoding="utf-8"))

    pairs, mismatches, strict_pairs, equal_pairs = independent_reduction_audit()
    r = committed["arbitrary_prefix_reduction_audit"]
    assert pairs == r["ordered_single_clause_pairs"] == 4096
    assert mismatches == r["count_mismatches"] == 0
    assert strict_pairs == r["strict_source_count_pairs"] == 2208
    assert equal_pairs == r["equal_source_count_pairs"] == 1888

    ones = sum(int(z == (a | b)) for z, a, b in product((0, 1), repeat=3))
    assert ones == 4
    assert committed["canonical_separation_control"]["def_truth_table_ones"] == ones
    assert committed["canonical_separation_control"]["hardness_prefix_first_bit"] == 1
    assert committed["canonical_separation_control"]["v92_first_bit_on_def_first_order"] == 0

    circuits, affine_mismatches, in_range = independent_affine_audit()
    a = committed["affine_comparator_audit"]
    assert circuits == a["affine_circuits"] == 65536
    assert affine_mismatches == a["child_count_mismatches"] == 0
    assert in_range == a["canonical_outputs_in_range"] == 0

    theorem = committed["theorem_status"]
    assert theorem["arbitrary_prefix_comparison_PP_complete"]
    assert not theorem["canonical_prefix_PP_hardness_proved"]
    assert theorem["affine_canonical_avoider_in_P"]
    assert not theorem["p_vs_np_resolved"]

    print(
        "V94 independent verification passed: 4096 source/compiler pairs and "
        "65536 affine circuits reconstructed without importing the primary kernel."
    )


if __name__ == "__main__":
    main()
