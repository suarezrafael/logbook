#!/usr/bin/env python3
"""Exact two-fiber affine model and weighted branch-decomposition counting.

Gate convention
---------------
A gate has a support of arity at most three, a truth-table bit mask, and an
explicit output flip. Local point bit j corresponds to support[j]. The
truth-table index is therefore the little-endian local point integer.

Every selected output fiber is partitioned into a minimum number of pairwise
disjoint affine cells. For arity at most three, at most three cells are ever
needed. The weighted branch DP stores, for each projected affine residual, the
number of internal assignments represented per boundary assignment.
"""
from __future__ import annotations

import functools
from collections import Counter
from pathlib import Path
import sys
from typing import Iterable, Sequence

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "v68"))

from affine_bitset import canonical_rref, extend_basis, project_basis, row

Gate = dict[str, object]
Basis = tuple[int, ...]
Tree = int | tuple["Tree", "Tree"]


def make_gate(
    support: Sequence[int], truth_mask: int, output_flip: int = 0
) -> Gate:
    support_tuple = tuple(int(variable) for variable in support)
    if not 1 <= len(support_tuple) <= 3:
        raise ValueError("gate arity must lie in 1..3")
    if any(variable < 0 for variable in support_tuple):
        raise ValueError("gate support variables must be nonnegative")
    if len(set(support_tuple)) != len(support_tuple):
        raise ValueError("gate support variables must be distinct")
    table_bits = 1 << len(support_tuple)
    if not 0 <= int(truth_mask) < (1 << table_bits):
        raise ValueError("truth mask does not fit the gate arity")
    return {
        "support": list(support_tuple),
        "truth_mask": int(truth_mask),
        "output_flip": int(output_flip) & 1,
    }


def validate_gate_support_range(n: int, gates: Sequence[Gate]) -> None:
    """Reject malformed supports before shifts or assignment enumeration."""
    if int(n) < 0:
        raise ValueError("the number of input variables must be nonnegative")
    for gate_index, gate in enumerate(gates):
        support = tuple(int(variable) for variable in gate["support"])
        if any(variable < 0 or variable >= int(n) for variable in support):
            raise ValueError(
                f"gate {gate_index} support variables must satisfy 0 <= variable < n"
            )


def effective_truth_mask(gate: Gate) -> int:
    arity = len(gate["support"])
    full = (1 << (1 << arity)) - 1
    base = int(gate["truth_mask"]) & full
    return base ^ (full if int(gate.get("output_flip", 0)) & 1 else 0)


def evaluate_gate(gate: Gate, assignment: int) -> int:
    local_point = 0
    for index, variable in enumerate(gate["support"]):
        local_point |= ((int(assignment) >> int(variable)) & 1) << index
    return (effective_truth_mask(gate) >> local_point) & 1


def evaluate_circuit(gates: Sequence[Gate], assignment: int) -> int:
    output = 0
    for index, gate in enumerate(gates):
        output |= evaluate_gate(gate, assignment) << index
    return output


def fiber_mask(gate: Gate, output_bit: int) -> int:
    arity = len(gate["support"])
    full = (1 << (1 << arity)) - 1
    positive = effective_truth_mask(gate)
    return positive if int(output_bit) & 1 else full ^ positive


def _is_linear_set(points: set[int]) -> bool:
    return 0 in points and all((left ^ right) in points for left in points for right in points)


def is_affine_mask(mask: int, arity: int) -> bool:
    if mask == 0:
        return False
    points = {point for point in range(1 << arity) if (mask >> point) & 1}
    base = min(points)
    return _is_linear_set({point ^ base for point in points})


@functools.lru_cache(None)
def affine_cell_masks(arity: int) -> tuple[int, ...]:
    if not 1 <= arity <= 3:
        raise ValueError("affine cell catalogue is restricted to arity 1..3")
    cells = [
        mask
        for mask in range(1, 1 << (1 << arity))
        if is_affine_mask(mask, arity)
    ]
    return tuple(sorted(cells, key=lambda mask: (-mask.bit_count(), mask)))


@functools.lru_cache(None)
def minimum_affine_partition(mask: int, arity: int) -> tuple[int, ...]:
    """Return a deterministic minimum disjoint affine partition of a local set."""
    if mask == 0:
        return tuple()
    lowest_point = (mask & -mask).bit_length() - 1
    best: tuple[tuple[object, ...], tuple[int, ...]] | None = None
    for cell in affine_cell_masks(arity):
        if not ((cell >> lowest_point) & 1) or cell & ~mask:
            continue
        remainder = minimum_affine_partition(mask ^ cell, arity)
        candidate = (cell,) + remainder
        key: tuple[object, ...] = (
            len(candidate),
            tuple(-item.bit_count() for item in candidate),
            candidate,
        )
        if best is None or key < best[0]:
            best = (key, candidate)
    if best is None:
        raise AssertionError("singletons should make every local set partitionable")
    return best[1]


def cell_equations(n: int, support: Sequence[int], cell_mask: int) -> Basis:
    support_tuple = tuple(int(variable) for variable in support)
    arity = len(support_tuple)
    points = [point for point in range(1 << arity) if (cell_mask >> point) & 1]
    if not points:
        raise ValueError("an affine cell must be nonempty")
    equations: list[int] = []
    for coefficients in range(1, 1 << arity):
        values = {(coefficients & point).bit_count() & 1 for point in points}
        if len(values) != 1:
            continue
        variables = tuple(
            support_tuple[index]
            for index in range(arity)
            if (coefficients >> index) & 1
        )
        equations.append(row(n, variables, next(iter(values))))
    basis = canonical_rref(tuple(equations), n)
    if basis is None:
        raise AssertionError("catalogued affine cells must be consistent")
    return basis


def compiled_fiber_cells(
    n: int, gate: Gate, output_bit: int | None
) -> tuple[Basis, ...]:
    """Compile a selected fiber, or the tautology when output_bit is None."""
    if output_bit is None:
        return (tuple(),)
    support = tuple(int(variable) for variable in gate["support"])
    mask = fiber_mask(gate, int(output_bit))
    return tuple(
        cell_equations(n, support, cell_mask)
        for cell_mask in minimum_affine_partition(mask, len(support))
    )


def balanced_branch_tree(order: Iterable[int]) -> Tree:
    leaves = list(int(index) for index in order)
    if not leaves:
        raise ValueError("a branch tree needs at least one gate")
    if len(leaves) == 1:
        return leaves[0]
    middle = len(leaves) // 2
    return balanced_branch_tree(leaves[:middle]), balanced_branch_tree(leaves[middle:])


def tree_subset(node: Tree) -> set[int]:
    if isinstance(node, int):
        return {node}
    return tree_subset(node[0]) | tree_subset(node[1])


def boundary_variables(gates: Sequence[Gate], subset: Iterable[int]) -> tuple[int, ...]:
    chosen = set(int(index) for index in subset)
    left = {
        int(variable)
        for index, gate in enumerate(gates)
        if index in chosen
        for variable in gate["support"]
    }
    right = {
        int(variable)
        for index, gate in enumerate(gates)
        if index not in chosen
        for variable in gate["support"]
    }
    return tuple(sorted(left & right))


def weighted_target_dp(
    n: int,
    gates: Sequence[Gate],
    target: Sequence[int | None],
    tree: Tree | None = None,
) -> dict[str, object]:
    """Count exact preimages of a full target or an output prefix.

    A residual weight is the number of assignments to variables internal to a
    node per satisfying assignment of its boundary residual. Equal projected
    residuals add their weights. Affine projection fibers have uniform size,
    which makes the recurrence exact.
    """
    gate_tuple = tuple(gates)
    validate_gate_support_range(n, gate_tuple)
    target_tuple = tuple(target)
    if len(target_tuple) != len(gate_tuple):
        raise ValueError("target length must equal the number of gates")
    if tree is None:
        tree = balanced_branch_tree(range(len(gate_tuple)))
    if tree_subset(tree) != set(range(len(gate_tuple))):
        raise ValueError("branch tree leaves must be exactly the gate indices")

    all_variables = {
        int(variable) for gate in gate_tuple for variable in gate["support"]
    }
    records: list[dict[str, object]] = []

    def visit(node: Tree, address: str = "R") -> Counter[Basis]:
        subset = tree_subset(node)
        boundary = boundary_variables(gate_tuple, subset)
        if isinstance(node, int):
            counts: Counter[Basis] = Counter()
            support = tuple(int(variable) for variable in gate_tuple[node]["support"])
            for cell in compiled_fiber_cells(n, gate_tuple[node], target_tuple[node]):
                projected = project_basis(cell, n, boundary)
                if projected is None:
                    continue
                source_dimension = len(support) - len(cell)
                projected_dimension = len(boundary) - len(projected)
                delta = source_dimension - projected_dimension
                if delta < 0:
                    raise AssertionError("projection cannot increase affine codimension")
                counts[projected] += 1 << delta
            pair_transitions = 0
        else:
            left_counts = visit(node[0], address + "0")
            right_counts = visit(node[1], address + "1")
            counts = Counter()
            pair_transitions = 0
            left_boundary = boundary_variables(gate_tuple, tree_subset(node[0]))
            right_boundary = boundary_variables(gate_tuple, tree_subset(node[1]))
            union_boundary = tuple(sorted(set(left_boundary) | set(right_boundary)))
            for left_basis, left_weight in left_counts.items():
                for right_basis, right_weight in right_counts.items():
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
                    counts[projected] += (
                        left_weight * right_weight * (1 << delta)
                    )
        records.append(
            {
                "address": address,
                "subset_size": len(subset),
                "boundary_size": len(boundary),
                "state_count": len(counts),
                "weight_sum": sum(counts.values()),
                "pair_transitions": pair_transitions,
            }
        )
        return counts

    root_counts = visit(tree)
    used_variable_count = root_counts.get(tuple(), 0)
    preimage_count = used_variable_count * (1 << (n - len(all_variables)))
    return {
        "preimage_count": preimage_count,
        "root_residuals": len(root_counts),
        "records": records,
    }


def prefix_count(
    n: int, gates: Sequence[Gate], prefix: Sequence[int], tree: Tree | None = None
) -> int:
    target: list[int | None] = list(int(bit) & 1 for bit in prefix)
    target.extend([None] * (len(gates) - len(target)))
    return int(weighted_target_dp(n, gates, target, tree)["preimage_count"])


def find_avoided_output(
    n: int, gates: Sequence[Gate], tree: Tree | None = None
) -> dict[str, object]:
    """Construct an absent output by prefix counting and the pigeonhole rule."""
    m = len(gates)
    if m <= n:
        raise ValueError("positive stretch m>n is required")
    prefix: list[int] = []
    parent_count = 1 << n
    trace: list[dict[str, int]] = []
    for index in range(m):
        count_zero = prefix_count(n, gates, prefix + [0], tree)
        count_one = prefix_count(n, gates, prefix + [1], tree)
        if count_zero + count_one != parent_count:
            raise AssertionError("the two exact gate fibers must partition the parent prefix")
        completion_capacity = 1 << (m - index - 1)
        chosen_bit = 0 if count_zero < completion_capacity else 1
        chosen_count = count_zero if chosen_bit == 0 else count_one
        trace.append(
            {
                "index": index,
                "count_zero": count_zero,
                "count_one": count_one,
                "completion_capacity": completion_capacity,
                "chosen_bit": chosen_bit,
                "chosen_count": chosen_count,
            }
        )
        prefix.append(chosen_bit)
        parent_count = chosen_count
    if parent_count != 0:
        raise AssertionError("the final chosen output must have zero preimages")
    target_integer = sum(bit << index for index, bit in enumerate(prefix))
    return {
        "target_bits": prefix,
        "target_integer": target_integer,
        "preimage_count": 0,
        "trace": trace,
    }


def brute_preimage_counts(n: int, gates: Sequence[Gate]) -> Counter[int]:
    gate_tuple = tuple(gates)
    validate_gate_support_range(n, gate_tuple)
    return Counter(evaluate_circuit(gate_tuple, assignment) for assignment in range(1 << n))
