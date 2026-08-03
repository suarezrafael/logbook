#!/usr/bin/env python3
"""Source-level V75 specialization for exact Hamming-ball pair counts."""
from __future__ import annotations

from math import comb
from pathlib import Path
import sys
from typing import Mapping, Sequence

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def hamming_ball_volume(m: int, radius: int) -> int:
    if radius < 0:
        return 0
    return sum(comb(m, j) for j in range(min(m, radius) + 1))


def _zero(radius: int) -> tuple[int, ...]:
    return (0,) * (radius + 1)


def _constant(value: int, radius: int) -> tuple[int, ...]:
    return (int(value),) + (0,) * radius


def _add(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    return tuple(int(a) + int(b) for a, b in zip(left, right))


def _multiply(left: Sequence[int], right: Sequence[int], radius: int) -> tuple[int, ...]:
    result = [0] * (radius + 1)
    for i, a in enumerate(left):
        if not a:
            continue
        for j, b in enumerate(right[: radius - i + 1]):
            if b:
                result[i + j] += int(a) * int(b)
    return tuple(result)


def distance_variable_values(
    m: int, prefix: Sequence[int], radius: int
) -> dict[tuple[int, int], tuple[int, ...]]:
    if radius < 0:
        raise ValueError("radius must be nonnegative")
    if len(prefix) > m:
        raise ValueError("prefix cannot exceed output length")
    one = _constant(1, radius)
    t = (0, 1) + (0,) * (radius - 1) if radius >= 1 else _zero(radius)
    one_plus_t = _add(one, t)
    values: dict[tuple[int, int], tuple[int, ...]] = {}
    for index in range(m):
        if index < len(prefix):
            requested = int(prefix[index]) & 1
            values[(index, requested)] = one
            values[(index, 1 - requested)] = t
        else:
            values[(index, 0)] = one_plus_t
            values[(index, 1)] = one_plus_t
    return values


def distance_polynomial(
    model: Mapping[str, object], prefix: Sequence[int], radius: int
) -> tuple[int, ...]:
    """Return exact pair counts by Hamming distance, truncated at ``radius``.

    The V75 arithmetic DAG represents

        sum_x product_i z_{i,C_i(x)}.

    Pinned coordinates assign weight 1 to agreement and t to disagreement.
    Unpinned coordinates assign 1+t to both paired variables, thereby summing
    over both possible target bits. Evaluation over Z[t]/(t^(r+1)) gives the
    exact number of pairs (x,z) at every distance at most r.
    """
    m = int(model["m"])
    if len(prefix) > m:
        raise ValueError("prefix cannot exceed output length")
    circuit = model["circuit"]
    root = int(model["root"])
    supplied = distance_variable_values(m, prefix, radius)
    values: list[tuple[int, ...]] = []
    for node in circuit.nodes:
        if node.kind == "const":
            value = _constant(int(node.payload), radius)
        elif node.kind == "var":
            value = supplied[node.payload]
        elif node.kind == "add":
            left, right = node.payload
            value = _add(values[int(left)], values[int(right)])
        elif node.kind == "mul":
            left, right = node.payload
            value = _multiply(values[int(left)], values[int(right)], radius)
        else:
            raise AssertionError(f"unknown V75 arithmetic node kind {node.kind}")
        values.append(value)
    return values[root]


def distance_pair_count(
    model: Mapping[str, object], prefix: Sequence[int], radius: int
) -> int:
    return sum(distance_polynomial(model, prefix, radius))


def build_v75_model(n: int, gates: Sequence[object], tree: object | None = None) -> Mapping[str, object]:
    v75 = str(ROOT / "v75")
    v74 = str(ROOT / "v74")
    if v75 not in sys.path:
        sys.path.insert(0, v75)
    if v74 not in sys.path:
        sys.path.insert(0, v74)
    from symbolic_prefix_circuit import build_symbolic_prefix_circuit

    return build_symbolic_prefix_circuit(n, gates, tree)


def remote_point_from_v75_model(model: Mapping[str, object], radius: int) -> dict[str, object]:
    n = int(model["n"])
    m = int(model["m"])
    root_count = distance_pair_count(model, (), radius)
    expected_root = (1 << n) * hamming_ball_volume(m, radius)
    if root_count != expected_root:
        raise AssertionError((root_count, expected_root))
    if root_count >= (1 << m):
        raise ValueError("strict Hamming-volume condition is required")

    prefix: tuple[int, ...] = ()
    parent_count = root_count
    trace: list[dict[str, int]] = []
    for length in range(m):
        counts = tuple(
            distance_pair_count(model, prefix + (bit,), radius) for bit in (0, 1)
        )
        if sum(counts) != parent_count:
            raise AssertionError((prefix, parent_count, counts))
        capacity = 1 << (m - length - 1)
        choices = [bit for bit in (0, 1) if counts[bit] < capacity]
        if not choices:
            raise AssertionError((prefix, counts, capacity))
        chosen = min(choices, key=lambda bit: (counts[bit], bit))
        trace.append(
            {
                "length": length + 1,
                "count_zero": counts[0],
                "count_one": counts[1],
                "capacity": capacity,
                "chosen": chosen,
            }
        )
        prefix += (chosen,)
        parent_count = counts[chosen]

    if parent_count != 0:
        raise AssertionError("the terminal target must have zero nearby preimages")
    target = sum(bit << i for i, bit in enumerate(prefix))
    return {
        "target_integer": target,
        "target_bits": list(prefix),
        "radius": radius,
        "root_pair_count": root_count,
        "terminal_pair_count": parent_count,
        "trace": trace,
        "arithmetic_operations": int(model["arithmetic_operations"]),
        "boundary_width": int(model["boundary_width"]),
    }
