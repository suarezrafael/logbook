#!/usr/bin/env python3
"""Canonical all-instance halving adapter for local Range Avoidance.

The algorithm fixes output bits in index order.  At every step it chooses the
smaller exact preimage child, breaking ties toward zero.  Once the preimage
count reaches zero, the remaining output bits are set to zero.

This file also implements the connected-component preimage representation used
in Huang--Li--Zhong's local greedy analysis.  It is a finite executable model,
not an implementation of their asymptotically optimized meet-in-the-middle
algorithm.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
import json
import random
from pathlib import Path
from typing import Iterable, Sequence

ROOT = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Gate:
    support: tuple[int, ...]
    table: int

    def evaluate(self, assignment: int) -> int:
        index = 0
        for local_index, variable in enumerate(self.support):
            index |= ((assignment >> variable) & 1) << local_index
        return (self.table >> index) & 1


@dataclass(frozen=True)
class Circuit:
    n: int
    gates: tuple[Gate, ...]
    locality: int

    @property
    def m(self) -> int:
        return len(self.gates)

    def validate(self) -> None:
        assert self.m >= self.n + 1
        assert self.locality >= 1
        for gate in self.gates:
            assert 1 <= len(gate.support) <= self.locality
            assert len(set(gate.support)) == len(gate.support)
            assert all(0 <= variable < self.n for variable in gate.support)
            assert 0 <= gate.table < (1 << (1 << len(gate.support)))

    def output_bits(self, assignment: int) -> tuple[int, ...]:
        return tuple(gate.evaluate(assignment) for gate in self.gates)


def brute_prefix_count(circuit: Circuit, prefix: Sequence[int]) -> int:
    return sum(
        circuit.output_bits(assignment)[: len(prefix)] == tuple(prefix)
        for assignment in range(1 << circuit.n)
    )


def fixed_gate_components(circuit: Circuit, length: int) -> list[tuple[int, ...]]:
    remaining = set(range(length))
    components: list[tuple[int, ...]] = []
    while remaining:
        seed = min(remaining)
        remaining.remove(seed)
        component = {seed}
        variables = set(circuit.gates[seed].support)
        changed = True
        while changed:
            changed = False
            for gate_index in sorted(tuple(remaining)):
                support = set(circuit.gates[gate_index].support)
                if variables & support:
                    remaining.remove(gate_index)
                    component.add(gate_index)
                    variables |= support
                    changed = True
        components.append(tuple(sorted(component)))
    return components


def component_valid_assignments(
    circuit: Circuit, prefix: Sequence[int], component: Sequence[int]
) -> tuple[int, tuple[int, ...]]:
    variables = tuple(
        sorted({variable for index in component for variable in circuit.gates[index].support})
    )
    valid = 0
    for local_assignment in range(1 << len(variables)):
        global_assignment = 0
        for local_index, variable in enumerate(variables):
            global_assignment |= ((local_assignment >> local_index) & 1) << variable
        if all(
            circuit.gates[gate_index].evaluate(global_assignment) == prefix[gate_index]
            for gate_index in component
        ):
            valid += 1
    return valid, variables


def component_prefix_data(circuit: Circuit, prefix: Sequence[int]) -> dict[str, object]:
    if not prefix:
        return {
            "components": [],
            "component_sizes": [],
            "used_variables": 0,
            "preimage_count": 1 << circuit.n,
            "traversed_weight": None,
        }
    components = fixed_gate_components(circuit, len(prefix))
    sizes: list[int] = []
    used: set[int] = set()
    for component in components:
        size, variables = component_valid_assignments(circuit, prefix, component)
        sizes.append(size)
        used.update(variables)
    product_size = 1
    for size in sizes:
        product_size *= size
    preimage_count = (1 << (circuit.n - len(used))) * product_size
    traversed_weight = (1 << (circuit.locality - len(components))) * product_size
    return {
        "components": [list(component) for component in components],
        "component_sizes": sizes,
        "used_variables": len(used),
        "preimage_count": preimage_count,
        "traversed_weight": traversed_weight,
    }


def component_prefix_count(circuit: Circuit, prefix: Sequence[int]) -> int:
    return int(component_prefix_data(circuit, prefix)["preimage_count"])


def canonical_halving(circuit: Circuit, counter=component_prefix_count) -> dict[str, object]:
    circuit.validate()
    prefix: list[int] = []
    current = 1 << circuit.n
    trace: list[dict[str, int]] = []
    for index in range(circuit.m):
        if current == 0:
            prefix.extend([0] * (circuit.m - index))
            break
        count_zero = int(counter(circuit, prefix + [0]))
        count_one = int(counter(circuit, prefix + [1]))
        assert count_zero + count_one == current
        chosen = 0 if count_zero <= count_one else 1
        chosen_count = count_zero if chosen == 0 else count_one
        assert 2 * chosen_count <= current
        prefix.append(chosen)
        trace.append(
            {
                "index": index,
                "parent_count": current,
                "count_zero": count_zero,
                "count_one": count_one,
                "chosen_bit": chosen,
                "chosen_count": chosen_count,
            }
        )
        current = chosen_count
    assert len(prefix) == circuit.m
    assert current == 0
    assert len(trace) <= circuit.n + 1
    return {
        "target_bits": prefix,
        "target_integer": sum(bit << index for index, bit in enumerate(prefix)),
        "preimage_count": current,
        "halving_steps": len(trace),
        "trace": trace,
    }


def completion_capacity_policy(circuit: Circuit) -> tuple[int, ...]:
    """The V75 deficit/capacity policy, included only for semantic comparison."""
    prefix: list[int] = []
    parent_count = 1 << circuit.n
    for index in range(circuit.m):
        count_zero = component_prefix_count(circuit, prefix + [0])
        count_one = parent_count - count_zero
        capacity = 1 << (circuit.m - index - 1)
        chosen = 0 if count_zero < capacity else 1
        prefix.append(chosen)
        parent_count = count_zero if chosen == 0 else count_one
    assert component_prefix_count(circuit, prefix) == 0
    return tuple(prefix)


def exhaustive_binary_results() -> dict[str, object]:
    circuits = 0
    prefix_checks = 0
    avoided = 0
    claim_checks = 0
    claim_mismatches = 0
    same_policy = 0
    different_policy = 0
    step_histogram: dict[int, int] = {}
    max_weight = 0
    support = (0, 1)
    for tables in product(range(16), repeat=3):
        circuit = Circuit(2, tuple(Gate(support, table) for table in tables), 2)
        result = canonical_halving(circuit)
        assert brute_prefix_count(circuit, result["target_bits"]) == 0
        avoided += 1
        for length in range(circuit.m + 1):
            for bits in product((0, 1), repeat=length):
                assert component_prefix_count(circuit, bits) == brute_prefix_count(circuit, bits)
                prefix_checks += 1
        for length in range(1, len(result["trace"]) + 1):
            data = component_prefix_data(circuit, result["target_bits"][:length])
            weight = int(data["traversed_weight"])
            bound = 1 << ((circuit.locality - 2) * length + circuit.locality)
            claim_checks += 1
            if weight > bound:
                claim_mismatches += 1
            max_weight = max(max_weight, weight)
        old = completion_capacity_policy(circuit)
        new = tuple(result["target_bits"])
        if old == new:
            same_policy += 1
        else:
            different_policy += 1
        steps = int(result["halving_steps"])
        step_histogram[steps] = step_histogram.get(steps, 0) + 1
        circuits += 1
    assert circuits == 4096
    assert claim_mismatches == 0
    return {
        "circuits": circuits,
        "prefix_count_checks": prefix_checks,
        "avoided_outputs": avoided,
        "claim_6_8_checks": claim_checks,
        "claim_6_8_mismatches": claim_mismatches,
        "maximum_traversed_weight": max_weight,
        "same_as_v75_capacity_policy": same_policy,
        "different_from_v75_capacity_policy": different_policy,
        "halving_step_histogram": {str(key): step_histogram[key] for key in sorted(step_histogram)},
    }


def random_circuit(rng: random.Random, n: int, m: int, locality: int) -> Circuit:
    gates: list[Gate] = []
    for _ in range(m):
        support = tuple(sorted(rng.sample(range(n), locality)))
        table = rng.randrange(1 << (1 << locality))
        gates.append(Gate(support, table))
    return Circuit(n, tuple(gates), locality)


def seeded_ternary_results(seed: int = 920092, samples: int = 512) -> dict[str, object]:
    rng = random.Random(seed)
    prefix_checks = 0
    claim_checks = 0
    claim_mismatches = 0
    avoided = 0
    max_weight = 0
    max_steps = 0
    for _ in range(samples):
        circuit = random_circuit(rng, n=4, m=5, locality=3)
        result = canonical_halving(circuit)
        assert brute_prefix_count(circuit, result["target_bits"]) == 0
        avoided += 1
        max_steps = max(max_steps, int(result["halving_steps"]))
        for length in range(len(result["trace"]) + 1):
            prefix = result["target_bits"][:length]
            assert component_prefix_count(circuit, prefix) == brute_prefix_count(circuit, prefix)
            prefix_checks += 1
            if length:
                data = component_prefix_data(circuit, prefix)
                weight = int(data["traversed_weight"])
                bound = 1 << ((circuit.locality - 2) * length + circuit.locality)
                claim_checks += 1
                if weight > bound:
                    claim_mismatches += 1
                max_weight = max(max_weight, weight)
    assert claim_mismatches == 0
    return {
        "seed": seed,
        "circuits": samples,
        "prefix_count_checks": prefix_checks,
        "avoided_outputs": avoided,
        "claim_6_8_checks": claim_checks,
        "claim_6_8_mismatches": claim_mismatches,
        "maximum_traversed_weight": max_weight,
        "maximum_halving_steps": max_steps,
    }


def build_results() -> dict[str, object]:
    exhaustive = exhaustive_binary_results()
    seeded = seeded_ternary_results()
    return {
        "laboratory": "V92",
        "module": "canonical all-instance halving adapter",
        "canonical_policy": {
            "output_order": "0,1,...,m-1",
            "choice": "smaller exact preimage child",
            "tie_break": 0,
            "suffix_after_empty": 0,
            "maximum_nonempty_steps": "n+1",
        },
        "exhaustive_binary": exhaustive,
        "seeded_ternary": seeded,
        "theorem_status": {
            "component_factorization_exact": True,
            "canonical_halving_returns_nonimage": True,
            "all_instance_semantic_completion": True,
            "v75_exact_prefix_counts_can_implement_policy": True,
            "hlz_greedy_can_implement_policy": True,
            "polynomial_all_instance_runtime": False,
            "published_lower_bound_transfer_triggered": False,
            "p_vs_np_resolved": False,
        },
    }


def main() -> None:
    results = build_results()
    (ROOT / "RESULTS.json").write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        "V92 canonical-halving audit passed: "
        f"binary circuits={results['exhaustive_binary']['circuits']}; "
        f"ternary samples={results['seeded_ternary']['circuits']}; "
        f"policy differences={results['exhaustive_binary']['different_from_v75_capacity_policy']}."
    )


if __name__ == "__main__":
    main()
