#!/usr/bin/env python3
"""Exact projected-residual optimum for the OR=1 path family."""
from __future__ import annotations

from pathlib import Path
import sys
from typing import Sequence

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "v68"))

from affine_bitset import extend_basis, project_basis
from two_fiber_model import Gate, boundary_variables, compiled_fiber_cells, make_gate

OR_MASK = 0b1110


def or_path_instance(edge_count: int) -> tuple[int, list[Gate], list[int]]:
    if edge_count < 1:
        raise ValueError("edge_count must be positive")
    gates = [make_gate((index, index + 1), OR_MASK) for index in range(edge_count)]
    return edge_count + 1, gates, [1] * edge_count


def residual_width_tables(
    n: int, gates: Sequence[Gate], target: Sequence[int]
) -> tuple[list[int], list[int]]:
    m = len(gates)
    compiled = [compiled_fiber_cells(n, gates[index], target[index]) for index in range(m)]
    basis_sets: list[set[tuple[int, ...]] | None] = [None] * (1 << m)
    basis_sets[0] = {tuple()}
    for mask in range(1, 1 << m):
        bit = mask & -mask
        gate_index = bit.bit_length() - 1
        previous = mask ^ bit
        next_states: set[tuple[int, ...]] = set()
        assert basis_sets[previous] is not None
        for basis in basis_sets[previous]:
            for cell in compiled[gate_index]:
                child = extend_basis(basis, cell, n)
                if child is not None:
                    next_states.add(child)
        basis_sets[mask] = next_states

    widths: list[int] = []
    frontiers: list[int] = []
    for mask, states in enumerate(basis_sets):
        assert states is not None
        processed = {index for index in range(m) if (mask >> index) & 1}
        active = tuple(
            sorted(
                {
                    int(variable)
                    for index, gate in enumerate(gates)
                    if index not in processed
                    for variable in gate["support"]
                }
            )
        )
        residuals = {project_basis(basis, n, active) for basis in states}
        residuals.discard(None)
        widths.append(len(residuals))
        frontiers.append(len(boundary_variables(gates, processed)))
    return widths, frontiers


def exact_gproj(n: int, gates: Sequence[Gate], target: Sequence[int]) -> dict[str, object]:
    widths, frontiers = residual_width_tables(n, gates, target)
    m = len(gates)
    infinity = 10**30
    costs = [infinity] * (1 << m)
    previous: list[tuple[int, int] | None] = [None] * (1 << m)
    costs[0] = 0
    for mask in range((1 << m) - 1):
        candidate = costs[mask] + widths[mask]
        for gate_index in range(m):
            if (mask >> gate_index) & 1:
                continue
            next_mask = mask | (1 << gate_index)
            if candidate < costs[next_mask]:
                costs[next_mask] = candidate
                previous[next_mask] = (mask, gate_index)
    order: list[int] = []
    mask = (1 << m) - 1
    while mask:
        record = previous[mask]
        if record is None:
            raise AssertionError("every finite instance must have an order")
        mask, gate_index = record
        order.append(gate_index)
    order.reverse()
    return {
        "Gstar": costs[-1],
        "order": order,
        "widths": widths,
        "frontiers": frontiers,
    }


def endpoint_order_profile(edge_count: int) -> dict[str, object]:
    n, gates, target = or_path_instance(edge_count)
    widths, _ = residual_width_tables(n, gates, target)
    mask = 0
    profile: list[int] = []
    for gate_index in range(edge_count):
        profile.append(widths[mask])
        mask |= 1 << gate_index
    expected = [1] if edge_count == 1 else [1, 2] + [3] * (edge_count - 2)
    if profile != expected:
        raise AssertionError((edge_count, profile, expected))
    return {
        "edge_count": edge_count,
        "vertex_count": edge_count + 1,
        "primal_treewidth": 1,
        "profile": profile,
        "G_proj": sum(profile),
        "formula": 1 if edge_count == 1 else 3 * edge_count - 3,
    }


def verify_all_order_lower_bound(edge_count: int) -> dict[str, int]:
    """Check the subset inequalities used by the all-orders proof."""
    n, gates, target = or_path_instance(edge_count)
    widths, _ = residual_width_tables(n, gates, target)
    singleton_minimum = (
        min(widths[1 << index] for index in range(edge_count))
        if edge_count >= 2
        else 1
    )
    larger_minimum = (
        min(
            widths[mask]
            for mask in range(1, (1 << edge_count) - 1)
            if mask.bit_count() >= 2
        )
        if edge_count >= 3
        else 0
    )
    expected_singleton = 2 if edge_count >= 2 else 1
    if singleton_minimum != expected_singleton:
        raise AssertionError(singleton_minimum)
    if edge_count >= 3 and larger_minimum < 3:
        raise AssertionError(larger_minimum)
    exact = exact_gproj(n, gates, target)
    formula = 1 if edge_count == 1 else 3 * edge_count - 3
    if exact["Gstar"] != formula:
        raise AssertionError((edge_count, exact["Gstar"], formula))
    return {
        "edge_count": edge_count,
        "singleton_minimum": singleton_minimum,
        "larger_proper_subset_minimum": larger_minimum,
        "Gstar": int(exact["Gstar"]),
    }
