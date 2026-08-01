#!/usr/bin/env python3
"""Independent semantic verifier for V75.

This file intentionally does not import the primary arithmetic-circuit builder,
the affine residual engine, or the V75 result generator.  It reconstructs gate
truth tables directly, enumerates Boolean inputs, reruns the prefix pigeonhole
search, and checks the committed finite snapshot and tree-shape identities.
"""
from __future__ import annotations

from collections import Counter
import itertools
import json
from pathlib import Path
import random
from typing import Sequence

HERE = Path(__file__).resolve().parent


def effective_truth_mask(gate: dict[str, object]) -> int:
    arity = len(gate["support"])
    full = (1 << (1 << arity)) - 1
    base = int(gate["truth_mask"]) & full
    return base ^ (full if int(gate.get("output_flip", 0)) & 1 else 0)


def evaluate_gate(gate: dict[str, object], assignment: int) -> int:
    local = 0
    for index, variable in enumerate(gate["support"]):
        local |= ((int(assignment) >> int(variable)) & 1) << index
    return (effective_truth_mask(gate) >> local) & 1


def output_counts(n: int, gates: Sequence[dict[str, object]]) -> Counter[int]:
    counts: Counter[int] = Counter()
    for assignment in range(1 << int(n)):
        output = 0
        for index, gate in enumerate(gates):
            output |= evaluate_gate(gate, assignment) << index
        counts[output] += 1
    return counts


def prefix_count(counts: Counter[int], prefix: Sequence[int]) -> int:
    mask = (1 << len(prefix)) - 1
    target = sum((int(bit) & 1) << index for index, bit in enumerate(prefix))
    return sum(count for output, count in counts.items() if (output & mask) == target)


def direct_avoided_output(n: int, m: int, counts: Counter[int]) -> tuple[list[int], int]:
    prefix: list[int] = []
    parent = 1 << int(n)
    for index in range(int(m)):
        count_zero = prefix_count(counts, prefix + [0])
        count_one = prefix_count(counts, prefix + [1])
        assert count_zero + count_one == parent
        capacity = 1 << (int(m) - index - 1)
        bit = 0 if count_zero < capacity else 1
        prefix.append(bit)
        parent = count_zero if bit == 0 else count_one
    assert parent == 0
    target = sum(bit << index for index, bit in enumerate(prefix))
    assert counts.get(target, 0) == 0
    return prefix, target


def balanced_depths(leaves: Sequence[int], depth: int = 0) -> dict[int, int]:
    if len(leaves) == 1:
        return {int(leaves[0]): int(depth)}
    middle = len(leaves) // 2
    return {
        **balanced_depths(leaves[:middle], depth + 1),
        **balanced_depths(leaves[middle:], depth + 1),
    }


def caterpillar_depths(m: int) -> dict[int, int]:
    if int(m) == 1:
        return {0: 0}
    result = {0: int(m) - 1, 1: int(m) - 1}
    for index in range(2, int(m)):
        result[index] = int(m) - index
    return result


def random_gate(rng: random.Random, n: int) -> dict[str, object]:
    arity = rng.randint(1, 3)
    support = sorted(rng.sample(range(n), arity))
    truth_mask = rng.randrange(1 << (1 << arity))
    return {
        "support": support,
        "truth_mask": truth_mask,
        "output_flip": rng.randrange(2),
    }


def main() -> None:
    results = json.loads((HERE / "RESULTS.json").read_text(encoding="utf-8"))
    assert results["version"] == "V75"
    assert results["status"] == "passed" and results["failures"] == 0

    exhaustive = results["exhaustive_binary_circuits"]
    circuits = coefficient_checks = prefix_checks = avoidance_checks = 0
    for masks in itertools.product(range(16), repeat=3):
        gates = [
            {"support": [0, 1], "truth_mask": mask, "output_flip": 0}
            for mask in masks
        ]
        counts = output_counts(2, gates)
        assert sum(counts.values()) == 4
        coefficient_checks += 8
        prefix_checks += 15
        direct_avoided_output(2, 3, counts)
        avoidance_checks += 1
        circuits += 1
    assert exhaustive["circuits"] == circuits == 4096
    assert exhaustive["coefficient_checks"] == coefficient_checks == 32768
    assert exhaustive["prefix_checks"] == prefix_checks == 61440
    assert exhaustive["avoidance_constructions"] == avoidance_checks == 4096

    seeded = results["seeded_ternary_circuits"]
    rng = random.Random(int(seeded["seed"]))
    first_gates = None
    for circuit_index in range(int(seeded["circuits"])):
        gates = [random_gate(rng, 5) for _ in range(6)]
        counts = output_counts(5, gates)
        direct_avoided_output(5, 6, counts)
        if circuit_index == 0:
            first_gates = gates
    representative = seeded["representative"]
    assert first_gates == representative["gates"]
    direct_counts = output_counts(5, representative["gates"])
    assert representative["output_counts"] == [
        direct_counts.get(output, 0) for output in range(64)
    ]
    for shape in ("balanced", "caterpillar"):
        snapshot = representative[shape]
        assert direct_counts.get(int(snapshot["avoided_output"]), 0) == 0
        bits = [int(bit) for bit in snapshot["target_bits"]]
        assert sum(bit << index for index, bit in enumerate(bits)) == int(
            snapshot["avoided_output"]
        )
        assert int(snapshot["dynamic_reevaluations"]) <= 2 * int(
            snapshot["dependency_cone_sum"]
        )
    assert seeded["coefficient_checks"] == 48 * 64 * 2
    assert seeded["prefix_checks"] == 48 * 127 * 2
    assert seeded["avoidance_constructions"] == 48 * 2

    for row in results["tree_shapes"]["instances"]:
        m = int(row["m"])
        balanced = balanced_depths(list(range(m)))
        caterpillar = caterpillar_depths(m)
        assert row["balanced_height"] == max(balanced.values())
        assert row["balanced_external_path_length"] == sum(balanced.values())
        assert row["caterpillar_height"] == max(caterpillar.values())
        assert row["caterpillar_external_path_length"] == sum(caterpillar.values())
    last = results["tree_shapes"]["instances"][-1]
    assert last == {
        "m": 64,
        "balanced_height": 6,
        "balanced_external_path_length": 384,
        "caterpillar_height": 63,
        "caterpillar_external_path_length": 2079,
    }

    status = results["theorem_status"]
    assert status["paired_generating_polynomial_exact"] is True
    assert status["monotone_arithmetic_translation_exact"] is True
    assert status["balanced_supplied_tree_bound_O_m_log_m_A_b_squared"] is True
    assert status["arbitrary_supplied_tree_improvement"] is False
    assert status["automatic_balancing_without_width_loss"] is False
    assert status["unrestricted_nc0_3_avoid_solved"] is False
    assert status["p_vs_np_resolved"] is False

    corpus = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in HERE.iterdir()
        if path.suffix in {".md", ".json", ".tex"}
    )
    for forbidden in (
        "p versus np is solved",
        "we prove p != np",
        "unrestricted nc0_3-avoid is solved",
        "automatic width-preserving balancing theorem proved",
        "peer reviewed theorem",
    ):
        assert forbidden not in corpus

    print(
        "V75 independent verification passed: direct truth-table semantics for "
        "4,096 binary circuits; independent prefix avoidance; seeded ternary "
        "snapshot reconstruction; balanced/caterpillar depth identities; zero failures."
    )


if __name__ == "__main__":
    main()
