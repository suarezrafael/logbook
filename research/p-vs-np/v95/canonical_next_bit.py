#!/usr/bin/env python3
from __future__ import annotations

"""Executable kernels for Laboratory V95.

The symbolic proof lives in THEOREMS.md.  This module validates two objects:

1. the composable balanced-definition loader whose canonical bits are exact
   ties resolved to zero; and
2. the compiler mapping a pair of 3-CNF counts to a genuinely canonical next
   bit of an NC0_3 stretch-one circuit.

Finite enumeration is a regression gate, not a proof of PP-hardness.
"""

from itertools import product
from typing import Sequence

Literal = int
Clause = tuple[Literal, Literal, Literal]
Formula = tuple[Clause, ...]
Signal = tuple[int, bool]  # (input coordinate, negated)
Gate = tuple


def signal_value(assignment: int, signal: Signal) -> int:
    index, negated = signal
    return ((assignment >> index) & 1) ^ int(negated)


def literal_signal(literal: Literal) -> Signal:
    return abs(literal) - 1, literal < 0


def formula_count(n: int, formula: Sequence[Clause]) -> int:
    total = 0
    for assignment in range(1 << n):
        ok = True
        for clause in formula:
            if not any(signal_value(assignment, literal_signal(lit)) for lit in clause):
                ok = False
                break
        total += int(ok)
    return total


def compile_pair(n: int, formula0: Sequence[Clause], formula1: Sequence[Clause]) -> dict:
    if not formula0 or not formula1:
        raise ValueError("V95 compiler expects two nonempty 3-CNFs")

    selector = n
    next_variable = n + 1
    definitions: list[Gate] = []

    def add_or(left: Signal, right: Signal) -> Signal:
        nonlocal next_variable
        z = next_variable
        next_variable += 1
        definitions.append(("or_def", z, left, right))
        return z, False

    def add_and(left: Signal, right: Signal) -> Signal:
        nonlocal next_variable
        z = next_variable
        next_variable += 1
        definitions.append(("and_def", z, left, right))
        return z, False

    def compile_formula(formula: Sequence[Clause]) -> Signal:
        clause_values: list[Signal] = []
        for clause in formula:
            if len(clause) != 3:
                raise ValueError("all clauses must have width exactly three")
            l1, l2, l3 = (literal_signal(literal) for literal in clause)
            partial = add_or(l1, l2)
            value = add_or(partial, l3)
            clause_values.append(value)

        current = clause_values[0]
        for value in clause_values[1:]:
            current = add_and(current, value)
        return current

    truth0 = compile_formula(formula0)
    truth1 = compile_formula(formula1)
    prefix_length = len(definitions)
    input_count = next_variable

    gates: list[Gate] = list(definitions)
    gates.append(("selector_compare", selector, truth0[0], truth1[0]))

    # q+1 useful outputs plus exactly n+1 harmless projections = N+1 outputs.
    while len(gates) < input_count + 1:
        gates.append(("proj", selector))

    assert len(gates) == input_count + 1
    return {
        "input_count": input_count,
        "output_count": len(gates),
        "prefix_length": prefix_length,
        "selector": selector,
        "truth0": truth0[0],
        "truth1": truth1[0],
        "gates": tuple(gates),
    }


def eval_gate(gate: Gate, assignment: int) -> int:
    kind = gate[0]
    if kind == "or_def":
        _, z, left, right = gate
        correct = signal_value(assignment, left) | signal_value(assignment, right)
        return ((assignment >> z) & 1) ^ correct
    if kind == "and_def":
        _, z, left, right = gate
        correct = signal_value(assignment, left) & signal_value(assignment, right)
        return ((assignment >> z) & 1) ^ correct
    if kind == "selector_compare":
        _, selector, truth0, truth1 = gate
        s = (assignment >> selector) & 1
        t0 = (assignment >> truth0) & 1
        t1 = (assignment >> truth1) & 1
        return (1 - t0) if s == 0 else t1
    if kind == "proj":
        return (assignment >> gate[1]) & 1
    raise ValueError(f"unknown gate kind: {kind}")


def canonical_trace(compiled: dict) -> tuple[tuple[int, ...], tuple[tuple[int, int], ...], int]:
    alive = list(range(1 << compiled["input_count"]))
    output: list[int] = []
    child_counts: list[tuple[int, int]] = []

    for gate in compiled["gates"]:
        counts = [0, 0]
        for assignment in alive:
            counts[eval_gate(gate, assignment)] += 1
        bit = 0 if counts[0] <= counts[1] else 1
        output.append(bit)
        child_counts.append((counts[0], counts[1]))
        alive = [
            assignment
            for assignment in alive
            if eval_gate(gate, assignment) == bit
        ]

    return tuple(output), tuple(child_counts), len(alive)


def circuit_output(compiled: dict, assignment: int) -> tuple[int, ...]:
    return tuple(eval_gate(gate, assignment) for gate in compiled["gates"])


def output_in_range(compiled: dict, output: Sequence[int]) -> bool:
    target = tuple(output)
    return any(
        circuit_output(compiled, assignment) == target
        for assignment in range(1 << compiled["input_count"])
    )


def representative_case() -> dict:
    formula0: Formula = ((1, 1, 1),)
    formula1: Formula = ((1, 2, 2),)
    compiled = compile_pair(2, formula0, formula1)
    source0 = formula_count(2, formula0)
    source1 = formula_count(2, formula1)
    output, child_counts, final_fiber = canonical_trace(compiled)
    q = compiled["prefix_length"]
    return {
        "source_counts": [source0, source1],
        "input_count": compiled["input_count"],
        "output_count": compiled["output_count"],
        "prefix_length": q,
        "canonical_output": list(output),
        "loader_child_counts": [list(pair) for pair in child_counts[:q]],
        "comparison_child_counts": list(child_counts[q]),
        "expected_comparison_child_counts": [
            source0 + 4 - source1,
            4 - source0 + source1,
        ],
        "comparison_bit": output[q],
        "expected_comparison_bit": 0 if source0 <= source1 else 1,
        "final_fiber_size": final_fiber,
        "canonical_output_in_range": output_in_range(compiled, output),
    }


def structural_size_audit() -> dict:
    cases = 0
    mismatches = 0
    max_locality = 0
    sample_clause: Clause = (1, -2, 3)

    for n in range(3, 7):
        for r0 in range(1, 6):
            for r1 in range(1, 6):
                formula0 = (sample_clause,) * r0
                formula1 = (sample_clause,) * r1
                compiled = compile_pair(n, formula0, formula1)
                expected_q = 3 * (r0 + r1) - 2
                expected_n = n + 1 + expected_q
                if compiled["prefix_length"] != expected_q:
                    mismatches += 1
                if compiled["input_count"] != expected_n:
                    mismatches += 1
                if compiled["output_count"] != expected_n + 1:
                    mismatches += 1
                for gate in compiled["gates"]:
                    if gate[0] in {"or_def", "and_def", "selector_compare"}:
                        max_locality = max(max_locality, 3)
                    elif gate[0] == "proj":
                        max_locality = max(max_locality, 1)
                    else:
                        mismatches += 1
                cases += 1

    return {
        "parameter_cases": cases,
        "size_or_stretch_mismatches": mismatches,
        "maximum_locality": max_locality,
    }


def exhaustive_one_clause_audit() -> dict:
    literals = (1, -1, 2, -2)
    clauses = tuple(product(literals, repeat=3))

    pairs = equal_pairs = strict_pairs = 0
    canonical_zero_comparisons = canonical_one_comparisons = 0
    balanced_loader_decisions = 0
    loader_balance_failures = 0
    loader_prefix_failures = 0
    final_count_mismatches = 0
    comparison_bit_mismatches = 0
    canonical_outputs_in_range = 0
    stretch_mismatches = 0

    for clause0 in clauses:
        source0 = formula_count(2, (clause0,))
        for clause1 in clauses:
            source1 = formula_count(2, (clause1,))
            compiled = compile_pair(2, (clause0,), (clause1,))
            output, child_counts, final_fiber = canonical_trace(compiled)
            q = compiled["prefix_length"]

            if compiled["output_count"] != compiled["input_count"] + 1:
                stretch_mismatches += 1

            loader_pairs = child_counts[:q]
            balanced_loader_decisions += sum(left == right for left, right in loader_pairs)
            loader_balance_failures += sum(left != right for left, right in loader_pairs)
            if output[:q] != (0,) * q:
                loader_prefix_failures += 1

            expected_children = (
                source0 + 4 - source1,
                4 - source0 + source1,
            )
            if child_counts[q] != expected_children:
                final_count_mismatches += 1

            expected_bit = 0 if source0 <= source1 else 1
            if output[q] != expected_bit:
                comparison_bit_mismatches += 1

            canonical_zero_comparisons += int(expected_bit == 0)
            canonical_one_comparisons += int(expected_bit == 1)
            equal_pairs += int(source0 == source1)
            strict_pairs += int(source0 != source1)

            if final_fiber != 0 or output_in_range(compiled, output):
                canonical_outputs_in_range += 1
            pairs += 1

    return {
        "source_variables": 2,
        "signed_literals": 4,
        "signed_three_literal_clauses": len(clauses),
        "ordered_clause_pairs": pairs,
        "equal_source_count_pairs": equal_pairs,
        "strict_source_count_pairs": strict_pairs,
        "canonical_zero_comparisons": canonical_zero_comparisons,
        "canonical_one_comparisons": canonical_one_comparisons,
        "balanced_loader_decisions": balanced_loader_decisions,
        "loader_balance_failures": loader_balance_failures,
        "loader_prefix_failures": loader_prefix_failures,
        "final_child_count_mismatches": final_count_mismatches,
        "comparison_bit_mismatches": comparison_bit_mismatches,
        "canonical_outputs_in_range": canonical_outputs_in_range,
        "stretch_one_mismatches": stretch_mismatches,
    }


def build_results() -> dict:
    return {
        "laboratory": "V95",
        "fixed_gate_language": {
            "signed_or_balanced_definition_variants": 4,
            "and_balanced_definition_variants": 1,
            "selector_comparison_variants": 1,
            "projection_variants": 1,
            "total_gate_types": 7,
            "maximum_locality": 3,
        },
        "representative_case": representative_case(),
        "structural_size_audit": structural_size_audit(),
        "exhaustive_one_clause_audit": exhaustive_one_clause_audit(),
        "theorem_status": {
            "balanced_definition_exact_tie_lemma": True,
            "balanced_loader_composable": True,
            "canonical_prefix_all_zero": True,
            "canonical_next_bit_PP_hard": True,
            "exact_canonical_word_PP_hard": True,
            "arbitrary_avoidance_PP_hard": False,
            "unrestricted_NC0_3_avoid_polynomial_time": False,
            "hlz_runtime_improved": False,
            "p_vs_np_resolved": False,
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(build_results(), indent=2, sort_keys=True))
