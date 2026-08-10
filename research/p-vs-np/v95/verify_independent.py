#!/usr/bin/env python3
from __future__ import annotations

"""Independent semantic verifier for V95.

This file imports neither canonical_next_bit.py nor its helpers. It reconstructs
the exhaustive one-clause compiler directly.
"""

import json
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def bit(x: int, index: int) -> int:
    return (x >> index) & 1


def literal_value(x: int, literal: int) -> int:
    value = bit(x, abs(literal) - 1)
    return value if literal > 0 else 1 - value


def source_count(clause: tuple[int, int, int]) -> int:
    return sum(
        int(any(literal_value(x, literal) for literal in clause))
        for x in range(4)
    )


def eval_or_error(x: int, z: int, left, right) -> int:
    def value(signal):
        kind, payload = signal
        if kind == "lit":
            return literal_value(x, payload)
        return bit(x, payload)

    return bit(x, z) ^ (value(left) | value(right))


def gates_for_pair(c0, c1):
    return (
        ("or", 3, ("lit", c0[0]), ("lit", c0[1])),
        ("or", 4, ("var", 3), ("lit", c0[2])),
        ("or", 5, ("lit", c1[0]), ("lit", c1[1])),
        ("or", 6, ("var", 5), ("lit", c1[2])),
        ("h", 2, 4, 6),
        ("proj", 2),
        ("proj", 2),
        ("proj", 2),
    )


def eval_gate(gate, x: int) -> int:
    if gate[0] == "or":
        return eval_or_error(x, gate[1], gate[2], gate[3])
    if gate[0] == "h":
        _, selector, truth0, truth1 = gate
        return (1 - bit(x, truth0)) if bit(x, selector) == 0 else bit(x, truth1)
    return bit(x, gate[1])


def canonical_trace(gates):
    alive = list(range(128))
    output = []
    counts = []
    for gate in gates:
        child = [0, 0]
        for x in alive:
            child[eval_gate(gate, x)] += 1
        chosen = 0 if child[0] <= child[1] else 1
        output.append(chosen)
        counts.append(tuple(child))
        alive = [x for x in alive if eval_gate(gate, x) == chosen]
    return tuple(output), tuple(counts), len(alive)


def output_in_range(gates, target) -> bool:
    target = tuple(target)
    return any(
        tuple(eval_gate(gate, x) for gate in gates) == target
        for x in range(128)
    )


def main() -> None:
    committed = json.loads((ROOT / "RESULTS.json").read_text(encoding="utf-8"))
    clauses = tuple(product((1, -1, 2, -2), repeat=3))

    pairs = equal_pairs = strict_pairs = 0
    zero_bits = one_bits = balanced = 0
    loader_failures = count_failures = bit_failures = range_failures = 0

    for c0 in clauses:
        a = source_count(c0)
        for c1 in clauses:
            b = source_count(c1)
            gates = gates_for_pair(c0, c1)
            output, counts, final_fiber = canonical_trace(gates)

            loader_failures += int(output[:4] != (0, 0, 0, 0))
            balanced += sum(left == right for left, right in counts[:4])
            loader_failures += sum(left != right for left, right in counts[:4])

            expected_counts = (a + 4 - b, 4 - a + b)
            count_failures += int(counts[4] != expected_counts)
            expected_bit = 0 if a <= b else 1
            bit_failures += int(output[4] != expected_bit)

            zero_bits += int(expected_bit == 0)
            one_bits += int(expected_bit == 1)
            equal_pairs += int(a == b)
            strict_pairs += int(a != b)
            range_failures += int(final_fiber != 0 or output_in_range(gates, output))
            pairs += 1

    audit = committed["exhaustive_one_clause_audit"]
    assert pairs == audit["ordered_clause_pairs"] == 4096
    assert equal_pairs == audit["equal_source_count_pairs"] == 1888
    assert strict_pairs == audit["strict_source_count_pairs"] == 2208
    assert zero_bits == audit["canonical_zero_comparisons"] == 2992
    assert one_bits == audit["canonical_one_comparisons"] == 1104
    assert balanced == audit["balanced_loader_decisions"] == 16384
    assert loader_failures == 0
    assert audit["loader_balance_failures"] == 0
    assert audit["loader_prefix_failures"] == 0
    assert count_failures == audit["final_child_count_mismatches"] == 0
    assert bit_failures == audit["comparison_bit_mismatches"] == 0
    assert range_failures == audit["canonical_outputs_in_range"] == 0

    theorem = committed["theorem_status"]
    assert theorem["balanced_loader_composable"]
    assert theorem["canonical_next_bit_PP_hard"]
    assert theorem["exact_canonical_word_PP_hard"]
    assert not theorem["arbitrary_avoidance_PP_hard"]
    assert not theorem["p_vs_np_resolved"]

    print(
        "V95 independent verification passed: 4096 independently reconstructed "
        "canonical compiler pairs, 16384 exact tie loader steps, and zero "
        "comparison/range mismatches."
    )


if __name__ == "__main__":
    main()
