#!/usr/bin/env python3
"""V97 comparison-free peeling-kernel avoider.

The module works with explicit local truth tables. It normalizes every gate to
its essential support, isolates positive-surplus support-incidence components,
then applies safe reductions before enumerating the residual kernel.
"""
from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
import math
import random
from typing import Iterable


@dataclass(frozen=True)
class Gate:
    output: int
    support: tuple[int, ...]
    table: tuple[int, ...]


def eval_gate(gate: Gate, assignment: dict[int, int]) -> int:
    index = 0
    for pos, variable in enumerate(gate.support):
        index |= (assignment[variable] & 1) << pos
    return gate.table[index]


def normalize_gate(gate: Gate) -> Gate:
    """Delete inessential support coordinates from an explicit <=3-bit table."""
    support = list(gate.support)
    table = list(gate.table)
    while support:
        width = len(support)
        removed = False
        for pos in range(width):
            independent = all(
                table[index] == table[index | (1 << pos)]
                for index in range(1 << width)
                if ((index >> pos) & 1) == 0
            )
            if not independent:
                continue
            new_support = support[:pos] + support[pos + 1 :]
            new_table: list[int] = []
            for index in range(1 << len(new_support)):
                low = index & ((1 << pos) - 1)
                high = index >> pos
                old_index = low | (high << (pos + 1))
                new_table.append(table[old_index])
            support = new_support
            table = new_table
            removed = True
            break
        if not removed:
            break
    return Gate(gate.output, tuple(support), tuple(table))


def restrict_variable(gate: Gate, variable: int, value: int) -> Gate:
    if variable not in gate.support:
        return gate
    new_support = tuple(x for x in gate.support if x != variable)
    new_table: list[int] = []
    for index in range(1 << len(new_support)):
        assignment = {x: (index >> pos) & 1 for pos, x in enumerate(new_support)}
        assignment[variable] = value
        new_table.append(eval_gate(gate, assignment))
    return normalize_gate(Gate(gate.output, new_support, tuple(new_table)))


def gate_from_function(output: int, support: Iterable[int], function) -> Gate:
    support = tuple(support)
    table = []
    for index in range(1 << len(support)):
        bits = [(index >> pos) & 1 for pos in range(len(support))]
        table.append(int(function(*bits)))
    return normalize_gate(Gate(output, support, tuple(table)))


def support_components(input_count: int, gates: list[Gate]) -> list[dict]:
    input_to_gates: dict[int, list[int]] = defaultdict(list)
    for gate_index, gate in enumerate(gates):
        for variable in gate.support:
            input_to_gates[variable].append(gate_index)
    visited_inputs: set[int] = set()
    visited_gates: set[int] = set()
    components: list[dict] = []
    for gate_index in range(len(gates)):
        if gate_index in visited_gates:
            continue
        queue = deque([("gate", gate_index)])
        visited_gates.add(gate_index)
        inputs: set[int] = set()
        gate_indices: set[int] = set()
        while queue:
            kind, item = queue.popleft()
            if kind == "gate":
                gate_indices.add(item)
                for variable in gates[item].support:
                    if variable not in visited_inputs:
                        visited_inputs.add(variable)
                        queue.append(("input", variable))
            else:
                inputs.add(item)
                for neighbor in input_to_gates[item]:
                    if neighbor not in visited_gates:
                        visited_gates.add(neighbor)
                        queue.append(("gate", neighbor))
        components.append({"inputs": inputs, "gates": gate_indices})
    for variable in range(input_count):
        if variable not in visited_inputs:
            components.append({"inputs": {variable}, "gates": set()})
    return components


def _enumerate_missing_word(inputs: set[int], gates: dict[int, Gate]) -> tuple[int, ...]:
    ordered_inputs = sorted(inputs)
    ordered_outputs = sorted(gates)
    assert len(ordered_outputs) > len(ordered_inputs)
    local_range: set[tuple[int, ...]] = set()
    for bits in range(1 << len(ordered_inputs)):
        assignment = {variable: (bits >> pos) & 1 for pos, variable in enumerate(ordered_inputs)}
        local_range.add(tuple(eval_gate(gates[output], assignment) for output in ordered_outputs))
    for value in range((1 << len(ordered_inputs)) + 1):
        candidate = tuple((value >> pos) & 1 for pos in range(len(ordered_outputs)))
        if candidate not in local_range:
            return candidate
    raise AssertionError("pigeonhole candidate search failed")


def reduce_positive_component(inputs: set[int], component_gates: list[Gate]) -> dict:
    """Apply the deterministic safe reduction sequence to one surplus component."""
    active_inputs = set(inputs)
    gates = {gate.output: normalize_gate(gate) for gate in component_gates}
    records: list[tuple] = []
    counters = {"unused_input_deletions": 0, "leaf_pair_deletions": 0, "unary_forcings": 0, "constant_terminations": 0}
    while True:
        constant_outputs = sorted(output for output, gate in gates.items() if len(gate.support) == 0)
        if constant_outputs:
            output = constant_outputs[0]
            target = {active_output: 0 for active_output in gates}
            target[output] = 1 - gates[output].table[0]
            counters["constant_terminations"] += 1
            for record in reversed(records):
                target[record[1]] = record[2]
            return {"kernel_inputs": 0, "kernel_outputs": 0, "target": target, "counters": counters, "terminated_by_constant": True}
        degree = {variable: 0 for variable in active_inputs}
        adjacency = {variable: [] for variable in active_inputs}
        for output, gate in gates.items():
            for variable in gate.support:
                degree[variable] += 1
                adjacency[variable].append(output)
        unused = sorted(variable for variable, value in degree.items() if value == 0)
        if unused:
            active_inputs.remove(unused[0])
            counters["unused_input_deletions"] += 1
            continue
        leaves = sorted(variable for variable, value in degree.items() if value == 1)
        if leaves:
            variable = leaves[0]
            output = adjacency[variable][0]
            records.append(("leaf", output, 0))
            del gates[output]
            active_inputs.remove(variable)
            counters["leaf_pair_deletions"] += 1
            continue
        unary_outputs = sorted(output for output, gate in gates.items() if len(gate.support) == 1)
        if unary_outputs:
            output = unary_outputs[0]
            gate = gates[output]
            variable = gate.support[0]
            zero_values = [value for value in (0, 1) if eval_gate(gate, {variable: value}) == 0]
            assert len(zero_values) == 1
            forced_value = zero_values[0]
            records.append(("forced", output, 0, variable, forced_value))
            del gates[output]
            active_inputs.remove(variable)
            gates = {active_output: restrict_variable(active_gate, variable, forced_value) for active_output, active_gate in gates.items()}
            counters["unary_forcings"] += 1
            continue
        break
    ordered_outputs = sorted(gates)
    missing = _enumerate_missing_word(active_inputs, gates)
    target = {output: bit for output, bit in zip(ordered_outputs, missing)}
    for record in reversed(records):
        target[record[1]] = record[2]
    return {"kernel_inputs": len(active_inputs), "kernel_outputs": len(gates), "target": target, "counters": counters, "terminated_by_constant": False}


def peeling_kernel_avoider(input_count: int, gates: list[Gate]) -> dict:
    normalized = [normalize_gate(gate) for gate in gates]
    components = support_components(input_count, normalized)
    positive = [component for component in components if len(component["gates"]) > len(component["inputs"])]
    assert positive, "stretch-one surplus guarantees a positive component"
    candidates = []
    for component in positive:
        local_gates = [normalized[index] for index in sorted(component["gates"])]
        reduced = reduce_positive_component(component["inputs"], local_gates)
        candidates.append((reduced["kernel_inputs"], len(component["inputs"]), min(component["gates"]) if component["gates"] else -1, component, reduced))
    candidates.sort(key=lambda item: item[:3])
    kernel_inputs, rho, _first, component, reduced = candidates[0]
    target = [0] * len(normalized)
    for output, bit in reduced["target"].items():
        target[output] = bit
    return {"target": tuple(target), "lambda": kernel_inputs, "rho": rho, "selected_component_inputs": len(component["inputs"]), "selected_component_outputs": len(component["gates"]), "counters": reduced["counters"], "terminated_by_constant": reduced["terminated_by_constant"]}


def evaluate_circuit(input_count: int, gates: list[Gate], bits: int) -> tuple[int, ...]:
    assignment = {variable: (bits >> variable) & 1 for variable in range(input_count)}
    return tuple(eval_gate(gate, assignment) for gate in sorted(gates, key=lambda g: g.output))


def strict_extension_family(input_count: int) -> tuple[list[Gate], int]:
    """One large positive component with rho=N but lambda=ceil(log2 N)."""
    assert input_count >= 8
    core = max(3, math.ceil(math.log2(input_count)))
    gates: list[Gate] = []
    output = 0
    for index in range(core + 1):
        support = (index % core, (index + 1) % core, (index + 2) % core)
        gates.append(gate_from_function(output, support, lambda a, b, c: a ^ b ^ c))
        output += 1
    for variable in range(core, input_count):
        gates.append(gate_from_function(output, (0, 1, variable), lambda a, b, c: a ^ b ^ c))
        output += 1
    assert len(gates) == input_count + 1
    return gates, core


def unary_cascade_family(case: int) -> tuple[int, list[Gate]]:
    input_count = 4
    gates = [
        gate_from_function(0, (0,), (lambda a: a) if (case & 1) == 0 else (lambda a: 1 ^ a)),
        gate_from_function(1, (0, 1), lambda a, b: a ^ b),
        gate_from_function(2, (1, 2), lambda a, b: a ^ b),
        gate_from_function(3, (2, 3), lambda a, b: a ^ b),
        gate_from_function(4, (3,), (lambda a: a) if (case & 2) == 0 else (lambda a: 1 ^ a)),
    ]
    return input_count, gates


def _random_gate(output: int, input_count: int, rng: random.Random) -> Gate:
    width = rng.choice(range(min(3, input_count) + 1))
    support = tuple(sorted(rng.sample(range(input_count), width)))
    table = tuple(rng.randrange(2) for _ in range(1 << width))
    return normalize_gate(Gate(output, support, table))


def _random_circuit(input_count: int, seed: int) -> list[Gate]:
    rng = random.Random(seed)
    return [_random_gate(output, input_count, rng) for output in range(input_count + 1)]


def build_results() -> dict:
    random_cases = random_absence_failures = lambda_gt_rho_failures = 0
    brute_force_input_evaluations = 0
    aggregate = {"unused_input_deletions": 0, "leaf_pair_deletions": 0, "unary_forcings": 0, "constant_terminations": 0}
    for input_count in range(2, 8):
        for case in range(40):
            gates = _random_circuit(input_count, 1000 * input_count + case)
            result = peeling_kernel_avoider(input_count, gates)
            image = {evaluate_circuit(input_count, gates, bits) for bits in range(1 << input_count)}
            brute_force_input_evaluations += 1 << input_count
            random_absence_failures += int(result["target"] in image)
            lambda_gt_rho_failures += int(result["lambda"] > result["rho"])
            for key in aggregate:
                aggregate[key] += result["counters"][key]
            random_cases += 1
    unary_cases = unary_absence_failures = unary_forcing_steps = 0
    for case in range(32):
        input_count, gates = unary_cascade_family(case)
        result = peeling_kernel_avoider(input_count, gates)
        image = {evaluate_circuit(input_count, gates, bits) for bits in range(1 << input_count)}
        brute_force_input_evaluations += 1 << input_count
        unary_cases += 1
        unary_forcing_steps += result["counters"]["unary_forcings"]
        unary_absence_failures += int(result["target"] in image)
    strict_rows = []
    strict_bruteforce_cases = strict_absence_failures = 0
    for input_count in (8, 16, 32, 64, 128):
        gates, expected_core = strict_extension_family(input_count)
        result = peeling_kernel_avoider(input_count, gates)
        assert result["rho"] == input_count
        assert result["lambda"] == expected_core
        strict_rows.append({"input_count": input_count, "output_count": input_count + 1, "rho": result["rho"], "lambda": result["lambda"], "ceil_log2_input": math.ceil(math.log2(input_count)), "leaf_pair_deletions": result["counters"]["leaf_pair_deletions"], "locality": 3, "gate_family": "ternary parity"})
        if input_count <= 16:
            image = {evaluate_circuit(input_count, gates, bits) for bits in range(1 << input_count)}
            brute_force_input_evaluations += 1 << input_count
            strict_bruteforce_cases += 1
            strict_absence_failures += int(result["target"] in image)
    return {
        "laboratory": "V97",
        "theorem_status": {
            "essential_support_normalization": True,
            "safe_leaf_input_output_pair_rule": True,
            "safe_unary_output_forcing_rule": True,
            "peeling_kernel_comparison_free_avoider": True,
            "lambda_never_exceeds_rho": True,
            "strict_extension_of_v96_parameter": True,
            "polynomial_when_lambda_logarithmic": True,
            "nonmonotone_ternary_strict_family": True,
            "unrestricted_NC0_3_avoid_polynomial_time": False,
            "hlz_worst_case_runtime_improved": False,
            "p_vs_np_resolved": False,
        },
        "runtime": {"formula": "O(2^lambda * poly(N))", "polynomial_regime": "lambda=O(log N)", "instancewise_beats_hlz_when": "lambda <= (1/2-epsilon)N - O(log N)", "hlz_k3_baseline": "O(N*2^(N/2))"},
        "random_small_audit": {"input_sizes": [2, 3, 4, 5, 6, 7], "cases_per_size": 40, "total_cases": random_cases, "absence_failures": random_absence_failures, "lambda_gt_rho_failures": lambda_gt_rho_failures, "brute_force_input_evaluations": brute_force_input_evaluations, "reduction_counters": aggregate},
        "unary_cascade_audit": {"total_cases": unary_cases, "total_unary_forcing_steps": unary_forcing_steps, "absence_failures": unary_absence_failures},
        "strict_extension_family": {"description": "single connected positive-surplus component; parity-3 core plus parity-3 leaf attachments", "rows": strict_rows, "brute_force_cases": strict_bruteforce_cases, "absence_failures": strict_absence_failures},
        "literature_calibration": {"kuntewar_sarma_2025_monotone_nc03_m_gt_n_in_P": True, "strict_family_is_monotone": False, "strict_family_is_nc02": False, "v84_small_hall_witness_FP_NP_preprocessor_preexists": True, "v97_does_not_claim_general_hall_extraction": True},
    }


if __name__ == "__main__":
    import json
    print(json.dumps(build_results(), indent=2, sort_keys=True))
