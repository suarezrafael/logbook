#!/usr/bin/env python3
"""Bitset affine-state engine for V68.

Rows are Python integers. Coefficient bits occupy positions 0..n-1 and the
right-hand side is bit n. The insertion routine is persistent: extending a
canonical basis only reduces the new rows and updates affected pivots, rather
than refactoring the full path from raw equations.
"""
from __future__ import annotations
from functools import lru_cache

INCONSISTENT = None


def row(n: int, variables: tuple[int, ...] | list[int], rhs: int) -> int:
    value = (int(rhs) & 1) << n
    for variable in variables:
        value ^= 1 << int(variable)
    return value


def pivot_of(value: int, n: int) -> int | None:
    coefficients = value & ((1 << n) - 1)
    if not coefficients:
        return None
    return (coefficients & -coefficients).bit_length() - 1


def insert_row(basis: tuple[int, ...], value: int, n: int) -> tuple[int, ...] | None:
    """Insert one equation into a canonical reduced bitset basis."""
    current = list(basis)
    by_pivot = {pivot_of(existing, n): existing for existing in current}
    for pivot in sorted(p for p in by_pivot if p is not None):
        if (value >> pivot) & 1:
            value ^= by_pivot[pivot]
    coefficients = value & ((1 << n) - 1)
    if not coefficients:
        return None if ((value >> n) & 1) else basis
    pivot = pivot_of(value, n)
    assert pivot is not None
    updated = []
    for existing in current:
        if (existing >> pivot) & 1:
            existing ^= value
        updated.append(existing)
    updated.append(value)
    updated.sort(key=lambda item: pivot_of(item, n))
    return tuple(updated)


def extend_basis(
    basis: tuple[int, ...], equations: tuple[int, ...] | list[int], n: int
) -> tuple[int, ...] | None:
    current: tuple[int, ...] | None = basis
    for equation in equations:
        if current is None:
            return None
        current = insert_row(current, equation, n)
    return current


def canonical_rref(
    equations: tuple[int, ...] | list[int], n: int, column_order: tuple[int, ...] | None = None
) -> tuple[int, ...] | None:
    """Canonical RREF with an optional pivot priority used for projection."""
    rows = [int(value) for value in equations if value]
    if column_order is None:
        column_order = tuple(range(n))
    lead = 0
    for column in column_order:
        chosen = next(
            (index for index in range(lead, len(rows)) if (rows[index] >> column) & 1),
            None,
        )
        if chosen is None:
            continue
        rows[lead], rows[chosen] = rows[chosen], rows[lead]
        pivot_row = rows[lead]
        for index in range(len(rows)):
            if index != lead and ((rows[index] >> column) & 1):
                rows[index] ^= pivot_row
        lead += 1
    coefficient_mask = (1 << n) - 1
    for value in rows:
        if not (value & coefficient_mask) and ((value >> n) & 1):
            return None
    rows = [value for value in rows if value & coefficient_mask]
    rows.sort(key=lambda item: pivot_of(item, n))
    return tuple(rows)


def project_basis(
    basis: tuple[int, ...], n: int, active_variables: tuple[int, ...] | list[int] | set[int]
) -> tuple[int, ...] | None:
    """Existentially project an affine system onto active variables.

    Eliminated variables receive pivot priority. Rows whose pivots remain in
    eliminated variables can always be solved for those variables and are then
    discarded; the surviving rows are the exact affine constraints on the
    active coordinates.
    """
    active = tuple(sorted(set(int(variable) for variable in active_variables)))
    active_set = set(active)
    eliminated = tuple(variable for variable in range(n) if variable not in active_set)
    reduced = canonical_rref(basis, n, eliminated + active)
    if reduced is None:
        return None
    eliminated_mask = sum(1 << variable for variable in eliminated)
    surviving = tuple(value for value in reduced if not (value & eliminated_mask))
    return canonical_rref(surviving, n, active)


def satisfies(basis: tuple[int, ...], assignment: int, n: int) -> bool:
    coefficient_mask = (1 << n) - 1
    return all(
        ((value & coefficient_mask & assignment).bit_count() & 1) == ((value >> n) & 1)
        for value in basis
    )


def build_projected_ordered_dag(gates: tuple[dict, ...], n: int) -> dict:
    """Build an ordered residual-state DAG with dead-variable projection.

    The state key is `(gate_index, canonical_projected_basis)`. This is a
    repository-local projected DAG model, not an asserted OBDD/FBDD or proof
    system equivalence.
    """
    suffix_active: list[tuple[int, ...]] = []
    for index in range(len(gates) + 1):
        variables = sorted(
            {
                variable
                for gate in gates[index:]
                for variable in gate["support"]
            }
        )
        suffix_active.append(tuple(variables))

    states: set[tuple[int, tuple[int, ...]]] = set()
    edges: dict[tuple[int, tuple[int, ...]], tuple[object, object]] = {}
    DEAD = ("dead",)
    ACCEPT = ("accept",)

    @lru_cache(None)
    def visit(index: int, basis: tuple[int, ...] | None):
        if basis is None:
            return DEAD
        if index == len(gates):
            return ACCEPT
        key = (index, basis)
        states.add(key)
        children = []
        for cell in gates[index]["cells"]:
            child = extend_basis(basis, cell, n)
            if child is not None:
                child = project_basis(child, n, suffix_active[index + 1])
            children.append(visit(index + 1, child))
        edges[key] = tuple(children)
        return key

    root = visit(0, tuple())
    return {
        "root": root,
        "nonterminal_states": len(states),
        "total_nodes_with_terminals": len(states) + 2,
        "states": states,
        "edges": edges,
    }
