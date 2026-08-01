#!/usr/bin/env python3
"""Monotone arithmetic circuits for exact paired-variable output counting.

The module compiles the weighted affine residual dynamic program of V74 into a
shared arithmetic DAG.  The DAG represents the generating polynomial

    P_C(u,v) = sum_x product_i z_{i,C_i(x)},

without expanding its 2^m possible monomials.  It supports fresh evaluation,
exact prefix counts, dependency-cone measurements, and incremental prefix
search for an avoided output.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
import sys
from typing import Iterable, Mapping, Sequence

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "v68"))
sys.path.insert(0, str(ROOT / "v74"))

from affine_bitset import extend_basis, project_basis
from two_fiber_model import (
    Basis,
    Gate,
    Tree,
    balanced_branch_tree,
    boundary_variables,
    compiled_fiber_cells,
    tree_subset,
    validate_gate_support_range,
)


@dataclass(frozen=True)
class ArithmeticNode:
    kind: str
    payload: object


class MonotoneArithmeticCircuit:
    """A topologically ordered DAG over nonnegative integers."""

    def __init__(self) -> None:
        self.nodes: list[ArithmeticNode] = []
        self.parents: list[set[int]] = []
        self._constants: dict[int, int] = {}
        self._variables: dict[tuple[int, int], int] = {}

    def _append(self, kind: str, payload: object, children: Sequence[int] = ()) -> int:
        node_id = len(self.nodes)
        self.nodes.append(ArithmeticNode(kind, payload))
        self.parents.append(set())
        for child in children:
            if not 0 <= int(child) < node_id:
                raise ValueError("arithmetic children must precede their parent")
            self.parents[int(child)].add(node_id)
        return node_id

    def constant(self, value: int) -> int:
        value = int(value)
        if value < 0:
            raise ValueError("the circuit is monotone and rejects negative constants")
        if value not in self._constants:
            self._constants[value] = self._append("const", value)
        return self._constants[value]

    def variable(self, output_index: int, output_bit: int) -> int:
        key = (int(output_index), int(output_bit) & 1)
        if key not in self._variables:
            self._variables[key] = self._append("var", key)
        return self._variables[key]

    def add(self, left: int, right: int) -> int:
        zero = self.constant(0)
        if left == zero:
            return int(right)
        if right == zero:
            return int(left)
        return self._append("add", (int(left), int(right)), (left, right))

    def multiply(self, left: int, right: int) -> int:
        zero = self.constant(0)
        one = self.constant(1)
        if left == zero or right == zero:
            return zero
        if left == one:
            return int(right)
        if right == one:
            return int(left)
        return self._append("mul", (int(left), int(right)), (left, right))

    def scale(self, node: int, factor: int) -> int:
        factor = int(factor)
        if factor < 0:
            raise ValueError("the circuit is monotone and rejects negative factors")
        return self.multiply(self.constant(factor), int(node))

    @property
    def variable_nodes(self) -> Mapping[tuple[int, int], int]:
        return dict(self._variables)

    @property
    def operation_count(self) -> int:
        return sum(node.kind in {"add", "mul"} for node in self.nodes)

    def evaluate(
        self, root: int, variable_values: Mapping[tuple[int, int], int] | None = None
    ) -> int:
        supplied = {} if variable_values is None else {
            (int(index), int(bit) & 1): int(value)
            for (index, bit), value in variable_values.items()
        }
        values: list[int] = []
        for node in self.nodes:
            if node.kind == "const":
                value = int(node.payload)
            elif node.kind == "var":
                value = supplied.get(node.payload, 1)
            elif node.kind == "add":
                left, right = node.payload
                value = values[int(left)] + values[int(right)]
            elif node.kind == "mul":
                left, right = node.payload
                value = values[int(left)] * values[int(right)]
            else:
                raise AssertionError(f"unknown arithmetic node kind {node.kind}")
            values.append(value)
        return values[int(root)]

    def dependency_cone(self, variable_keys: Iterable[tuple[int, int]]) -> set[int]:
        frontier = [self._variables[key] for key in variable_keys]
        seen: set[int] = set(frontier)
        operations: set[int] = set()
        while frontier:
            child = frontier.pop()
            for parent in self.parents[child]:
                if parent in seen:
                    continue
                seen.add(parent)
                frontier.append(parent)
                if self.nodes[parent].kind in {"add", "mul"}:
                    operations.add(parent)
        return operations


class IncrementalEvaluator:
    """Maintain all DAG values and reevaluate only changed dependency cones."""

    def __init__(self, circuit: MonotoneArithmeticCircuit, root: int) -> None:
        self.circuit = circuit
        self.root = int(root)
        self.values: list[int] = []
        self.variable_values: dict[tuple[int, int], int] = {}
        for node in circuit.nodes:
            if node.kind == "const":
                value = int(node.payload)
            elif node.kind == "var":
                self.variable_values[node.payload] = 1
                value = 1
            elif node.kind == "add":
                left, right = node.payload
                value = self.values[int(left)] + self.values[int(right)]
            elif node.kind == "mul":
                left, right = node.payload
                value = self.values[int(left)] * self.values[int(right)]
            else:
                raise AssertionError(f"unknown arithmetic node kind {node.kind}")
            self.values.append(value)

    @property
    def root_value(self) -> int:
        return self.values[self.root]

    def update(self, changes: Mapping[tuple[int, int], int]) -> tuple[int, int]:
        changed_nodes: list[int] = []
        for raw_key, raw_value in changes.items():
            key = (int(raw_key[0]), int(raw_key[1]) & 1)
            if key not in self.circuit.variable_nodes:
                raise KeyError(f"unknown paired variable {key}")
            value = int(raw_value)
            if value < 0:
                raise ValueError("monotone evaluation rejects negative variable values")
            node_id = self.circuit.variable_nodes[key]
            if self.values[node_id] == value:
                continue
            self.values[node_id] = value
            self.variable_values[key] = value
            changed_nodes.append(node_id)

        affected: set[int] = set()
        frontier = list(changed_nodes)
        while frontier:
            child = frontier.pop()
            for parent in self.circuit.parents[child]:
                if parent not in affected:
                    affected.add(parent)
                    frontier.append(parent)

        reevaluated = 0
        for node_id in sorted(affected):
            node = self.circuit.nodes[node_id]
            if node.kind == "add":
                left, right = node.payload
                self.values[node_id] = self.values[int(left)] + self.values[int(right)]
                reevaluated += 1
            elif node.kind == "mul":
                left, right = node.payload
                self.values[node_id] = self.values[int(left)] * self.values[int(right)]
                reevaluated += 1
        return self.root_value, reevaluated

    def fresh_root_value(self) -> int:
        return self.circuit.evaluate(self.root, self.variable_values)


def tree_leaves(tree: Tree) -> tuple[int, ...]:
    if isinstance(tree, int):
        return (int(tree),)
    return tree_leaves(tree[0]) + tree_leaves(tree[1])


def caterpillar_branch_tree(order: Iterable[int]) -> Tree:
    leaves = list(int(index) for index in order)
    if not leaves:
        raise ValueError("a branch tree needs at least one gate")
    tree: Tree = leaves[0]
    for leaf in leaves[1:]:
        tree = (tree, leaf)
    return tree


def leaf_depths(tree: Tree) -> dict[int, int]:
    depths: dict[int, int] = {}

    def visit(node: Tree, depth: int) -> None:
        if isinstance(node, int):
            if node in depths:
                raise ValueError("branch tree leaves must be unique")
            depths[int(node)] = int(depth)
            return
        visit(node[0], depth + 1)
        visit(node[1], depth + 1)

    visit(tree, 0)
    return depths


def _add_term(
    circuit: MonotoneArithmeticCircuit,
    expressions: dict[Basis, int],
    residual: Basis,
    term: int,
) -> None:
    zero = circuit.constant(0)
    expressions[residual] = circuit.add(expressions.get(residual, zero), term)


def build_symbolic_prefix_circuit(
    n: int,
    gates: Sequence[Gate],
    tree: Tree | None = None,
) -> dict[str, object]:
    gate_tuple = tuple(gates)
    validate_gate_support_range(n, gate_tuple)
    if not gate_tuple:
        raise ValueError("at least one output gate is required")
    if tree is None:
        tree = balanced_branch_tree(range(len(gate_tuple)))
    leaves = tree_leaves(tree)
    if sorted(leaves) != list(range(len(gate_tuple))):
        raise ValueError("branch tree leaves must be each gate index exactly once")
    if tree_subset(tree) != set(range(len(gate_tuple))):
        raise ValueError("branch tree leaf set is invalid")

    circuit = MonotoneArithmeticCircuit()
    zero = circuit.constant(0)
    circuit.constant(1)
    for index in range(len(gate_tuple)):
        circuit.variable(index, 0)
        circuit.variable(index, 1)

    all_variables = {
        int(variable) for gate in gate_tuple for variable in gate["support"]
    }
    records: list[dict[str, object]] = []

    def visit(node: Tree, address: str = "R") -> dict[Basis, int]:
        subset = tree_subset(node)
        boundary = boundary_variables(gate_tuple, subset)
        operations_before = circuit.operation_count
        if isinstance(node, int):
            expressions: dict[Basis, int] = {}
            support = tuple(int(variable) for variable in gate_tuple[node]["support"])
            local_terms = 0
            for bit in (0, 1):
                variable = circuit.variable(node, bit)
                for cell in compiled_fiber_cells(n, gate_tuple[node], bit):
                    projected = project_basis(cell, n, boundary)
                    if projected is None:
                        continue
                    source_dimension = len(support) - len(cell)
                    projected_dimension = len(boundary) - len(projected)
                    delta = source_dimension - projected_dimension
                    if delta < 0:
                        raise AssertionError("projection cannot increase affine codimension")
                    term = circuit.scale(variable, 1 << delta)
                    _add_term(circuit, expressions, projected, term)
                    local_terms += 1
            pair_transitions = 0
        else:
            left_expressions = visit(node[0], address + "0")
            right_expressions = visit(node[1], address + "1")
            expressions = {}
            pair_transitions = 0
            local_terms = 0
            left_boundary = boundary_variables(gate_tuple, tree_subset(node[0]))
            right_boundary = boundary_variables(gate_tuple, tree_subset(node[1]))
            union_boundary = tuple(sorted(set(left_boundary) | set(right_boundary)))
            for left_basis, left_expression in left_expressions.items():
                for right_basis, right_expression in right_expressions.items():
                    pair_transitions += 1
                    combined = extend_basis(left_basis, right_basis, n)
                    if combined is None:
                        continue
                    projected = project_basis(combined, n, boundary)
                    if projected is None:
                        continue
                    combined_dimension = len(union_boundary) - len(combined)
                    projected_dimension = len(boundary) - len(projected)
                    delta = combined_dimension - projected_dimension
                    if delta < 0:
                        raise AssertionError("projection fiber dimension must be nonnegative")
                    term = circuit.multiply(left_expression, right_expression)
                    term = circuit.scale(term, 1 << delta)
                    _add_term(circuit, expressions, projected, term)
                    local_terms += 1

        records.append(
            {
                "address": address,
                "subset_size": len(subset),
                "boundary_size": len(boundary),
                "state_count": len(expressions),
                "pair_transitions": pair_transitions,
                "accepted_terms": local_terms,
                "operations_created": circuit.operation_count - operations_before,
            }
        )
        return expressions

    root_expressions = visit(tree)
    root_expression = root_expressions.get(tuple(), zero)
    root = circuit.scale(root_expression, 1 << (int(n) - len(all_variables)))
    depths = leaf_depths(tree)
    cones = {
        index: len(circuit.dependency_cone(((index, 0), (index, 1))))
        for index in range(len(gate_tuple))
    }
    return {
        "n": int(n),
        "m": len(gate_tuple),
        "tree": tree,
        "root": root,
        "circuit": circuit,
        "records": records,
        "boundary_width": max(record["boundary_size"] for record in records),
        "arithmetic_operations": circuit.operation_count,
        "total_nodes": len(circuit.nodes),
        "leaf_depths": depths,
        "external_path_length": sum(depths.values()),
        "dependency_cone_operations": cones,
        "dependency_cone_sum": sum(cones.values()),
    }


def paired_assignment_for_prefix(prefix: Sequence[int]) -> dict[tuple[int, int], int]:
    assignment: dict[tuple[int, int], int] = {}
    for index, raw_bit in enumerate(prefix):
        bit = int(raw_bit) & 1
        assignment[(index, bit)] = 1
        assignment[(index, 1 - bit)] = 0
    return assignment


def prefix_count(model: Mapping[str, object], prefix: Sequence[int]) -> int:
    if len(prefix) > int(model["m"]):
        raise ValueError("prefix cannot be longer than the output word")
    circuit = model["circuit"]
    assert isinstance(circuit, MonotoneArithmeticCircuit)
    return circuit.evaluate(int(model["root"]), paired_assignment_for_prefix(prefix))


def coefficient(model: Mapping[str, object], output_bits: Sequence[int]) -> int:
    if len(output_bits) != int(model["m"]):
        raise ValueError("a coefficient query needs one bit per output")
    return prefix_count(model, output_bits)


def find_avoided_output_incremental(model: Mapping[str, object]) -> dict[str, object]:
    n = int(model["n"])
    m = int(model["m"])
    if m <= n:
        raise ValueError("positive stretch m>n is required")
    circuit = model["circuit"]
    assert isinstance(circuit, MonotoneArithmeticCircuit)
    evaluator = IncrementalEvaluator(circuit, int(model["root"]))
    if evaluator.root_value != 1 << n:
        raise AssertionError("all paired variables set to one must count every input")

    prefix: list[int] = []
    parent_count = 1 << n
    trace: list[dict[str, int]] = []
    dynamic_reevaluations = 0
    for index in range(m):
        count_zero, touched_zero = evaluator.update({(index, 1): 0})
        dynamic_reevaluations += touched_zero
        if count_zero != evaluator.fresh_root_value():
            raise AssertionError("incremental zero-child value differs from fresh evaluation")
        count_one = parent_count - count_zero
        completion_capacity = 1 << (m - index - 1)
        chosen_bit = 0 if count_zero < completion_capacity else 1
        touched_select = 0
        if chosen_bit == 0:
            chosen_count = count_zero
        else:
            chosen_count, touched_select = evaluator.update(
                {(index, 1): 1, (index, 0): 0}
            )
            dynamic_reevaluations += touched_select
            if chosen_count != count_one:
                raise AssertionError("paired fibers must partition the parent prefix")
            if chosen_count != evaluator.fresh_root_value():
                raise AssertionError("incremental selected value differs from fresh evaluation")
        trace.append(
            {
                "index": index,
                "count_zero": count_zero,
                "count_one": count_one,
                "completion_capacity": completion_capacity,
                "chosen_bit": chosen_bit,
                "chosen_count": chosen_count,
                "reevaluated_zero": touched_zero,
                "reevaluated_select": touched_select,
            }
        )
        prefix.append(chosen_bit)
        parent_count = chosen_count

    if parent_count != 0:
        raise AssertionError("the final selected output must have zero preimages")
    target_integer = sum(bit << index for index, bit in enumerate(prefix))
    return {
        "target_bits": prefix,
        "target_integer": target_integer,
        "preimage_count": 0,
        "trace": trace,
        "initial_operations": int(model["arithmetic_operations"]),
        "dynamic_reevaluations": dynamic_reevaluations,
        "total_arithmetic_reevaluations": int(model["arithmetic_operations"])
        + dynamic_reevaluations,
    }
