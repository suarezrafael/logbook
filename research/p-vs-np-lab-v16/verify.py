from __future__ import annotations

import collections
import itertools
import json
from pathlib import Path

Gate = tuple[int, int, int]
Hypergraph = tuple[Gate, ...]
Bits = tuple[int, ...]


def vertices(gates: Hypergraph) -> tuple[int, ...]:
    return tuple(sorted({v for gate in gates for v in gate}))


def generate(max_edges: int = 5) -> dict[int, set[Hypergraph]]:
    levels: dict[int, set[Hypergraph]] = {1: {((0, 1, 2),)}}
    for edge_count in range(2, max_edges + 1):
        next_level: set[Hypergraph] = set()
        for gates in levels[edge_count - 1]:
            used = vertices(gates)
            next_vertex = max(used) + 1
            for shared_count in (1, 2, 3):
                for shared in itertools.combinations(used, shared_count):
                    fresh = tuple(range(next_vertex, next_vertex + 3 - shared_count))
                    gate = tuple(sorted(shared + fresh))
                    if gate in gates:
                        continue
                    if any(len(set(gate) & set(previous)) > 1 for previous in gates):
                        continue
                    next_level.add(tuple(sorted(gates + (gate,))))
        levels[edge_count] = next_level
    return levels


def clauses(gate: Gate, bit: int) -> tuple[tuple[int, int], ...]:
    literals = tuple(v + 1 for v in gate)
    if bit:
        return tuple(itertools.combinations(literals, 2))
    return tuple((-a, -b) for a, b in itertools.combinations(literals, 2))


def sat_two_cnf(variable_count: int, formula: list[tuple[int, int]]) -> bool:
    graph = [[] for _ in range(2 * variable_count)]

    def node(literal: int) -> int:
        variable = abs(literal) - 1
        return 2 * variable + int(literal > 0)

    for first, second in formula:
        graph[node(-first)].append(node(second))
        graph[node(-second)].append(node(first))

    index = 0
    stack: list[int] = []
    on_stack = [False] * len(graph)
    indices = [-1] * len(graph)
    low = [0] * len(graph)
    component = [-1] * len(graph)
    component_id = 0

    def visit(vertex: int) -> None:
        nonlocal index, component_id
        indices[vertex] = low[vertex] = index
        index += 1
        stack.append(vertex)
        on_stack[vertex] = True
        for neighbor in graph[vertex]:
            if indices[neighbor] == -1:
                visit(neighbor)
                low[vertex] = min(low[vertex], low[neighbor])
            elif on_stack[neighbor]:
                low[vertex] = min(low[vertex], indices[neighbor])
        if low[vertex] != indices[vertex]:
            return
        while True:
            member = stack.pop()
            on_stack[member] = False
            component[member] = component_id
            if member == vertex:
                break
        component_id += 1

    for vertex in range(len(graph)):
        if indices[vertex] == -1:
            visit(vertex)

    return all(component[2 * v] != component[2 * v + 1] for v in range(variable_count))


def satisfiable(gates: Hypergraph, bits: Bits) -> bool:
    used = vertices(gates)
    mapping = {original: reduced for reduced, original in enumerate(used)}
    formula: list[tuple[int, int]] = []
    for gate, bit in zip(gates, bits):
        formula.extend(clauses(tuple(mapping[v] for v in gate), bit))
    return sat_two_cnf(len(used), formula)


def majority(values: tuple[int, int, int]) -> int:
    return int(sum(values) >= 2)


def brute_force_satisfiable(gates: Hypergraph, bits: Bits) -> bool:
    used = vertices(gates)
    mapping = {original: reduced for reduced, original in enumerate(used)}
    for assignment in range(1 << len(used)):
        values = tuple((assignment >> i) & 1 for i in range(len(used)))
        if all(majority(tuple(values[mapping[v]] for v in gate)) == bit for gate, bit in zip(gates, bits)):
            return True
    return False


def signatures(gates: Hypergraph) -> tuple[tuple[int, ...], ...]:
    return tuple(sorted(tuple(i for i, gate in enumerate(gates) if vertex in gate) for vertex in vertices(gates)))


def canonical(gates: Hypergraph, bits: Bits, complement: bool) -> tuple:
    edge_count = len(gates)
    base_signatures = signatures(gates)
    best = None
    for permutation in itertools.permutations(range(edge_count)):
        transformed_signatures = tuple(sorted(tuple(sorted(permutation[i] for i in signature)) for signature in base_signatures))
        transformed_bits = [0] * edge_count
        for old, new in enumerate(permutation):
            transformed_bits[new] = bits[old]
        candidate = (tuple(transformed_bits), transformed_signatures)
        if complement:
            candidate = min(candidate, (tuple(1 - bit for bit in transformed_bits), transformed_signatures))
        best = candidate if best is None or candidate < best else best
    assert best is not None
    return best


def satisfying_assignments(gates: Hypergraph, bits: Bits):
    used = vertices(gates)
    mapping = {original: reduced for reduced, original in enumerate(used)}
    answers = []
    for assignment in range(1 << len(used)):
        values = tuple((assignment >> i) & 1 for i in range(len(used)))
        if all(majority(tuple(values[mapping[v]] for v in gate)) == bit for gate, bit in zip(gates, bits)):
            answers.append(values)
    return tuple(answers), mapping


def cap_count(gates: Hypergraph, bits: Bits) -> int:
    count = 0
    for removed in range(5):
        remaining_gates = gates[:removed] + gates[removed + 1 :]
        remaining_bits = bits[:removed] + bits[removed + 1 :]
        answers, mapping = satisfying_assignments(remaining_gates, remaining_bits)
        if len(answers) != 2:
            continue
        live = [vertex for vertex, index in mapping.items() if {answer[index] for answer in answers} == {0, 1}]
        if not live:
            continue
        cap = gates[removed]
        fresh = [vertex for vertex in cap if vertex not in mapping]
        values = set()
        for answer in answers:
            base = {vertex: answer[index] for vertex, index in mapping.items()}
            for fresh_assignment in range(1 << len(fresh)):
                extended = dict(base)
                for position, vertex in enumerate(fresh):
                    extended[vertex] = (fresh_assignment >> position) & 1
                values.add(majority(tuple(extended[v] for v in cap)))
        if len(values) == 1 and next(iter(values)) != bits[removed]:
            count += 1
    return count


def main() -> None:
    levels = generate(5)
    counts: list[int] = []
    witnesses: list[tuple[Hypergraph, Bits]] = []

    for edge_count in range(1, 6):
        unsat = 0
        for gates in levels[edge_count]:
            for bits in itertools.product((0, 1), repeat=edge_count):
                bits = tuple(bits)
                if not satisfiable(gates, bits):
                    unsat += 1
                    witnesses.append((gates, bits))
        counts.append(unsat)

    colored_classes = {canonical(gates, bits, False) for gates, bits in witnesses}
    complement_classes = {canonical(gates, bits, True) for gates, bits in witnesses}
    brute_force_errors = sum(brute_force_satisfiable(gates, bits) for gates, bits in witnesses)
    deletion_errors = 0
    cap_histogram = collections.Counter()

    for gates, bits in witnesses:
        cap_histogram[cap_count(gates, bits)] += 1
        for removed in range(5):
            if not brute_force_satisfiable(gates[:removed] + gates[removed + 1 :], bits[:removed] + bits[removed + 1 :]):
                deletion_errors += 1

    result = {
        "generated_hypergraphs": {str(i): len(levels[i]) for i in range(1, 6)},
        "unsatisfiable_by_edge_count": counts,
        "witnesses": len(witnesses),
        "labeled_hypergraphs": len({gates for gates, _ in witnesses}),
        "colored_classes": len(colored_classes),
        "complement_classes": len(complement_classes),
        "brute_force_witness_errors": brute_force_errors,
        "deletion_minimality_errors": deletion_errors,
        "cap_decomposition_histogram": dict(cap_histogram),
    }
    expected = {
        "generated_hypergraphs": {"1": 1, "2": 3, "3": 27, "4": 471, "5": 13059},
        "unsatisfiable_by_edge_count": [0, 0, 0, 0, 792],
        "witnesses": 792,
        "labeled_hypergraphs": 396,
        "colored_classes": 6,
        "complement_classes": 3,
        "brute_force_witness_errors": 0,
        "deletion_minimality_errors": 0,
        "cap_decomposition_histogram": {3: 792},
    }
    result["matches_expected"] = result == expected
    print(json.dumps(result, indent=2))
    if not result["matches_expected"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
