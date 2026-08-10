#!/usr/bin/env python3
from __future__ import annotations

"""Executable kernels for Laboratory V94.

The proof obligations live in THEOREMS.md.  This module provides deterministic
finite regression gates for two theorem-native objects:

1. an exact compiler from a pair of 3-CNF counting instances to one
   arbitrary-prefix child-count comparison instance over a fixed finite gate
   language of arity at most three; and
2. an exact Gaussian-elimination comparator for affine NC0_3 circuits.

The finite censuses are evidence against implementation mistakes, not proofs of
PP-completeness or of the affine theorem.
"""

from itertools import product
from typing import Iterable, Sequence

Literal = int                  # +/- (1-indexed original variable)
Clause = tuple[Literal, Literal, Literal]
Formula = tuple[Clause, ...]
AffineGate = tuple[int, int]   # (coefficient mask, constant bit)
Gate = tuple


def literal_value(assignment: int, literal: Literal) -> int:
    variable = abs(literal) - 1
    bit = (assignment >> variable) & 1
    return bit if literal > 0 else 1 - bit


def formula_count(n: int, formula: Sequence[Clause]) -> int:
    count = 0
    for assignment in range(1 << n):
        ok = True
        for clause in formula:
            if not any(literal_value(assignment, literal) for literal in clause):
                ok = False
                break
        count += int(ok)
    return count


def compile_pair(n: int, formula0: Sequence[Clause], formula1: Sequence[Clause]):
    """Compile a pair of 3-CNFs into the V94 comparison gadget.

    Variable layout:
      originals       0 .. n-1
      selector s      n
      one z per clause
      optional free dummies used only to make the final stretch exactly one

    Prefix gates, all fixed to output one:
      DEF(z,l2,l3)       : z == (l2 OR l3)
      COND(s,b,l1,z)     : tautological off branch b, and (l1 OR z) on branch b

    The next output is the selector.  Remaining outputs are harmless projections
    so the total number of outputs is exactly N+1.
    """
    selector = n
    tagged_clauses = [(0, clause) for clause in formula0] + [
        (1, clause) for clause in formula1
    ]
    clause_count = len(tagged_clauses)

    gates: list[Gate] = []
    for index, (branch, clause) in enumerate(tagged_clauses):
        z = n + 1 + index
        l1, l2, l3 = clause
        gates.append(("def", z, l2, l3))
        gates.append(("cond", selector, branch, l1, z))

    prefix_length = len(gates)
    base_variables = n + 1 + clause_count
    dummy_count = max(0, prefix_length - base_variables)
    input_count = base_variables + dummy_count

    gates.append(("proj", selector))
    while len(gates) < input_count + 1:
        gates.append(("proj", 0 if input_count else selector))

    assert len(gates) == input_count + 1
    prefix = (1,) * prefix_length
    return {
        "input_count": input_count,
        "output_count": len(gates),
        "prefix_length": prefix_length,
        "dummy_count": dummy_count,
        "selector": selector,
        "gates": tuple(gates),
        "prefix": prefix,
        "clause_count": clause_count,
    }


def eval_gate(gate: Gate, assignment: int) -> int:
    kind = gate[0]
    if kind == "proj":
        return (assignment >> gate[1]) & 1
    if kind == "def":
        _, z, l2, l3 = gate
        z_value = (assignment >> z) & 1
        rhs = literal_value(assignment, l2) | literal_value(assignment, l3)
        return int(z_value == rhs)
    if kind == "cond":
        _, selector, active_branch, l1, z = gate
        selector_value = (assignment >> selector) & 1
        if selector_value != active_branch:
            return 1
        return int(literal_value(assignment, l1) | ((assignment >> z) & 1))
    raise ValueError(f"unknown gate kind: {kind}")


def compiled_child_counts(compiled: dict) -> tuple[int, int]:
    prefix = compiled["prefix"]
    prefix_length = compiled["prefix_length"]
    gates = compiled["gates"]
    counts = [0, 0]
    for assignment in range(1 << compiled["input_count"]):
        prefix_ok = True
        for index, wanted in enumerate(prefix):
            if eval_gate(gates[index], assignment) != wanted:
                prefix_ok = False
                break
        if prefix_ok:
            child = eval_gate(gates[prefix_length], assignment)
            counts[child] += 1
    return counts[0], counts[1]


def affine_value(gate: AffineGate, assignment: int) -> int:
    mask, constant = gate
    return constant ^ ((mask & assignment).bit_count() & 1)


def gf2_solution_count(n: int, equations: Iterable[tuple[int, int]]) -> int:
    """Count solutions of Ax=b over GF(2) with an incremental xor basis."""
    basis: dict[int, tuple[int, int]] = {}
    rank = 0
    for mask, rhs in equations:
        mask = int(mask)
        rhs = int(rhs) & 1
        while mask:
            pivot = mask.bit_length() - 1
            if pivot in basis:
                basis_mask, basis_rhs = basis[pivot]
                mask ^= basis_mask
                rhs ^= basis_rhs
            else:
                basis[pivot] = (mask, rhs)
                rank += 1
                break
        if mask == 0 and rhs:
            return 0
    return 1 << (n - rank)


def affine_child_counts(
    n: int, gates: Sequence[AffineGate], prefix: Sequence[int]
) -> tuple[int, int]:
    next_index = len(prefix)
    equations = [
        (gates[index][0], prefix[index] ^ gates[index][1])
        for index in range(next_index)
    ]
    mask, constant = gates[next_index]
    result = []
    for child in (0, 1):
        rhs = child ^ constant
        result.append(gf2_solution_count(n, equations + [(mask, rhs)]))
    return result[0], result[1]


def affine_canonical_output(n: int, gates: Sequence[AffineGate]) -> tuple[int, ...]:
    prefix: list[int] = []
    for _ in gates:
        count0, count1 = affine_child_counts(n, gates, prefix)
        prefix.append(0 if count0 <= count1 else 1)
    return tuple(prefix)


def affine_canonical_output_incremental(
    n: int, gates: Sequence[AffineGate]
) -> tuple[int, ...]:
    """Canonical V92 output using one maintained GF(2) row basis."""
    basis: dict[int, tuple[int, int]] = {}
    output: list[int] = []
    empty = False

    for mask, constant in gates:
        if empty:
            output.append(0)
            continue

        reduced_mask = mask
        rhs_for_output_zero = constant
        while reduced_mask:
            pivot = reduced_mask.bit_length() - 1
            if pivot not in basis:
                break
            basis_mask, basis_rhs = basis[pivot]
            reduced_mask ^= basis_mask
            rhs_for_output_zero ^= basis_rhs

        if reduced_mask:
            output.append(0)
            pivot = reduced_mask.bit_length() - 1
            basis[pivot] = (reduced_mask, rhs_for_output_zero)
        else:
            chosen = 1 if rhs_for_output_zero == 0 else 0
            output.append(chosen)
            empty = True

    return tuple(output)


def brute_affine_child_counts(
    n: int, gates: Sequence[AffineGate], prefix: Sequence[int]
) -> tuple[int, int]:
    next_index = len(prefix)
    counts = [0, 0]
    for assignment in range(1 << n):
        values = [affine_value(gate, assignment) for gate in gates]
        if tuple(values[:next_index]) == tuple(prefix):
            counts[values[next_index]] += 1
    return counts[0], counts[1]


def output_in_affine_range(
    n: int, gates: Sequence[AffineGate], output: Sequence[int]
) -> bool:
    target = tuple(output)
    for assignment in range(1 << n):
        if tuple(affine_value(gate, assignment) for gate in gates) == target:
            return True
    return False


def reduction_audit() -> dict:
    literals = (1, -1, 2, -2)
    clauses = tuple(product(literals, repeat=3))
    ordered_pairs = strict_pairs = equal_pairs = 0
    count_mismatches = stretch_mismatches = 0

    for clause0 in clauses:
        source0 = formula_count(2, (clause0,))
        for clause1 in clauses:
            source1 = formula_count(2, (clause1,))
            compiled = compile_pair(2, (clause0,), (clause1,))
            child0, child1 = compiled_child_counts(compiled)
            scale = 1 << compiled["dummy_count"]
            if (child0, child1) != (scale * source0, scale * source1):
                count_mismatches += 1
            if compiled["output_count"] != compiled["input_count"] + 1:
                stretch_mismatches += 1
            ordered_pairs += 1
            if source0 == source1:
                equal_pairs += 1
            else:
                strict_pairs += 1

    return {
        "variables": 2,
        "signed_literals": 4,
        "signed_three_literal_clauses": len(clauses),
        "ordered_single_clause_pairs": ordered_pairs,
        "strict_source_count_pairs": strict_pairs,
        "equal_source_count_pairs": equal_pairs,
        "count_mismatches": count_mismatches,
        "stretch_one_mismatches": stretch_mismatches,
    }


def affine_audit() -> dict:
    functions = tuple((mask, constant) for mask in range(8) for constant in (0, 1))
    circuit_count = child_decisions = 0
    child_count_mismatches = range_failures = incremental_output_mismatches = 0

    for gates in product(functions, repeat=4):
        prefix: list[int] = []
        for _ in gates:
            exact = affine_child_counts(3, gates, prefix)
            brute = brute_affine_child_counts(3, gates, prefix)
            if exact != brute:
                child_count_mismatches += 1
            prefix.append(0 if exact[0] <= exact[1] else 1)
            child_decisions += 1
        incremental = affine_canonical_output_incremental(3, gates)
        if incremental != tuple(prefix):
            incremental_output_mismatches += 1
        if output_in_affine_range(3, gates, prefix):
            range_failures += 1
        circuit_count += 1

    return {
        "variables": 3,
        "outputs": 4,
        "affine_functions": len(functions),
        "affine_circuits": circuit_count,
        "child_decisions": child_decisions,
        "child_count_mismatches": child_count_mismatches,
        "incremental_output_mismatches": incremental_output_mismatches,
        "canonical_outputs_in_range": range_failures,
    }


def representative_compiler_case() -> dict:
    formula0: Formula = ((1, 1, 1),)
    formula1: Formula = ((1, 2, 3),)
    compiled = compile_pair(3, formula0, formula1)
    source = (formula_count(3, formula0), formula_count(3, formula1))
    children = compiled_child_counts(compiled)
    return {
        "source_counts": list(source),
        "compiled_child_counts": list(children),
        "dummy_count": compiled["dummy_count"],
        "input_count": compiled["input_count"],
        "output_count": compiled["output_count"],
        "prefix_length": compiled["prefix_length"],
        "comparison_preserved": source[0] <= source[1] and children[0] <= children[1],
    }


def canonical_separation_control() -> dict:
    satisfying = 0
    for z, a, b in product((0, 1), repeat=3):
        satisfying += int(z == (a | b))
    falsifying = 8 - satisfying
    return {
        "def_truth_table_ones": satisfying,
        "def_truth_table_zeros": falsifying,
        "v92_first_bit_on_def_first_order": 0 if falsifying <= satisfying else 1,
        "hardness_prefix_first_bit": 1,
        "reduction_prefix_is_canonical_in_this_order": False,
    }


def build_results() -> dict:
    return {
        "laboratory": "V94",
        "fixed_gate_language": {
            "maximum_arity": 3,
            "definition_variants": 4,
            "conditional_clause_variants": 4,
            "projection_variants": 1,
            "total_gate_types": 9,
        },
        "representative_compiler_case": representative_compiler_case(),
        "arbitrary_prefix_reduction_audit": reduction_audit(),
        "canonical_separation_control": canonical_separation_control(),
        "affine_comparator_audit": affine_audit(),
        "theorem_status": {
            "arbitrary_prefix_comparison_in_PP": True,
            "arbitrary_prefix_comparison_PP_hard_via_exact_scaled_reduction": True,
            "arbitrary_prefix_comparison_PP_complete": True,
            "stretch_one_preserved": True,
            "fixed_arity_at_most_three_language": True,
            "affine_all_prefix_comparison_in_P": True,
            "affine_canonical_avoider_in_P": True,
            "canonical_prefix_PP_hardness_proved": False,
            "unrestricted_NC0_3_avoid_polynomial_time": False,
            "hlz_runtime_improved": False,
            "p_vs_np_resolved": False,
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(build_results(), indent=2, sort_keys=True))
