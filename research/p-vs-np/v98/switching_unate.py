#!/usr/bin/env python3
from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from itertools import product


@dataclass(frozen=True)
class Gate:
    support: tuple[int, ...]
    mask: int


def eval_table(mask: int, bits: tuple[int, ...] | list[int]) -> int:
    idx = sum((int(bit) & 1) << i for i, bit in enumerate(bits))
    return (mask >> idx) & 1


def make_mask(arity: int, fn) -> int:
    mask = 0
    for bits in product((0, 1), repeat=arity):
        idx = sum(bits[i] << i for i in range(arity))
        mask |= (int(fn(bits)) & 1) << idx
    return mask


def essential_positions(mask: int, arity: int) -> tuple[int, ...]:
    answer: list[int] = []
    for j in range(arity):
        depends = False
        for bits in product((0, 1), repeat=arity):
            if bits[j]:
                continue
            low = list(bits)
            high = list(bits)
            high[j] = 1
            if eval_table(mask, low) != eval_table(mask, high):
                depends = True
                break
        if depends:
            answer.append(j)
    return tuple(answer)


def unate_direction(mask: int, arity: int, coordinate: int) -> int | None:
    """0 means nondecreasing, 1 means nonincreasing; None means non-unate/inessential."""
    positive = False
    negative = False
    for bits in product((0, 1), repeat=arity):
        if bits[coordinate]:
            continue
        low = list(bits)
        high = list(bits)
        high[coordinate] = 1
        delta = eval_table(mask, high) - eval_table(mask, low)
        positive |= delta > 0
        negative |= delta < 0
        if positive and negative:
            return None
    if not positive and not negative:
        return None
    return 0 if positive else 1


def is_monotone(mask: int, arity: int) -> bool:
    for j in range(arity):
        for bits in product((0, 1), repeat=arity):
            if bits[j]:
                continue
            low = list(bits)
            high = list(bits)
            high[j] = 1
            if eval_table(mask, low) > eval_table(mask, high):
                return False
    return True


def solve_balanced_unate(
    input_count: int, gates: list[Gate]
) -> tuple[list[int], list[int]] | None:
    """
    Solve d_(e,v)=r_v XOR q_e on the incidence graph.

    Essential support is required: this makes every unate direction unique.
    """
    adjacency: dict[tuple[str, int], list[tuple[tuple[str, int], int]]] = defaultdict(list)
    for edge, gate in enumerate(gates):
        arity = len(gate.support)
        if essential_positions(gate.mask, arity) != tuple(range(arity)):
            return None
        for local_index, vertex in enumerate(gate.support):
            direction = unate_direction(gate.mask, arity, local_index)
            if direction is None:
                return None
            x_node = ("x", vertex)
            g_node = ("g", edge)
            adjacency[x_node].append((g_node, direction))
            adjacency[g_node].append((x_node, direction))

    potential: dict[tuple[str, int], int] = {}
    nodes = [("x", i) for i in range(input_count)] + [
        ("g", e) for e in range(len(gates))
    ]
    for start in nodes:
        if start in potential:
            continue
        potential[start] = 0
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for neighbor, parity in adjacency[node]:
                value = potential[node] ^ parity
                if neighbor in potential:
                    if potential[neighbor] != value:
                        return None
                else:
                    potential[neighbor] = value
                    queue.append(neighbor)

    r = [potential[("x", i)] for i in range(input_count)]
    q = [potential[("g", e)] for e in range(len(gates))]
    return r, q


def transform_gate(gate: Gate, input_flips: list[int], output_flip: int) -> Gate:
    arity = len(gate.support)
    local_flips = [input_flips[v] for v in gate.support]
    mask = make_mask(
        arity,
        lambda z: eval_table(
            gate.mask, tuple(z[i] ^ local_flips[i] for i in range(arity))
        )
        ^ output_flip,
    )
    return Gate(gate.support, mask)


def switch_to_monotone(
    input_count: int, gates: list[Gate]
) -> tuple[list[Gate], list[int], list[int]] | None:
    solution = solve_balanced_unate(input_count, gates)
    if solution is None:
        return None
    r, q = solution
    transformed = [
        transform_gate(gate, r, q[edge]) for edge, gate in enumerate(gates)
    ]
    if not all(is_monotone(gate.mask, len(gate.support)) for gate in transformed):
        raise AssertionError("balanced-unate solution failed to produce monotone gates")
    return transformed, r, q


def circuit_output(gates: list[Gate], assignment: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        eval_table(gate.mask, tuple(assignment[v] for v in gate.support))
        for gate in gates
    )


def output_range(input_count: int, gates: list[Gate]) -> set[tuple[int, ...]]:
    return {
        circuit_output(gates, assignment)
        for assignment in product((0, 1), repeat=input_count)
    }


def input_degrees(input_count: int, gates: list[Gate]) -> list[int]:
    degrees = [0] * input_count
    for gate in gates:
        for vertex in gate.support:
            degrees[vertex] += 1
    return degrees


MAJ3 = make_mask(3, lambda bits: int(sum(bits) >= 2))
PARITY3 = make_mask(3, lambda bits: bits[0] ^ bits[1] ^ bits[2])


def build_strict_balanced_unate_family(input_count: int) -> list[Gate]:
    """
    Exact-stretch irreducible family.

    Supports are cyclic triples plus one duplicate.  In transformed coordinates
    z_0=x_0 XOR 1 and z_i=x_i for i>0 every gate is MAJ3.
    """
    if input_count < 5:
        raise ValueError("input_count must be at least five")
    global_flips = [1] + [0] * (input_count - 1)
    supports = [
        (i, (i + 1) % input_count, (i + 2) % input_count)
        for i in range(input_count)
    ]
    supports.append(supports[0])

    gates: list[Gate] = []
    for support in supports:
        local = tuple(global_flips[v] for v in support)
        mask = make_mask(
            3,
            lambda x, local=local: int(
                sum(x[i] ^ local[i] for i in range(3)) >= 2
            ),
        )
        gates.append(Gate(support, mask))
    return gates


def build_parity_loose_x_host(
    ell: int,
) -> tuple[int, list[Gate], list[Gate], dict[int, int], int]:
    """
    Build an exact-stretch irreducible parity host containing a distinguished
    Berge-even-cycle plus chi intersection (a simple loose-X source).

    The distinguished X has 2*ell edges.  e_0 and e_3 receive the extra shared
    vertex w; every other cycle edge has a private third vertex.  Added parity
    edges raise every host input degree to at least two while preserving exact
    stretch.
    """
    if ell < 3:
        raise ValueError("ell must be at least three")
    length = 2 * ell
    w = length
    private: dict[int, int] = {}
    next_vertex = length + 1
    for i in range(length):
        if i not in (0, 3):
            private[i] = next_vertex
            next_vertex += 1

    x_gates: list[Gate] = []
    for i in range(length):
        if i in (0, 3):
            support = (i, (i + 1) % length, w)
        else:
            support = (i, (i + 1) % length, private[i])
        x_gates.append(Gate(support, PARITY3))

    input_count = next_vertex
    completion: list[Gate] = []
    for i in range(length):
        if i in (0, 3):
            continue
        completion.append(
            Gate((private[i], (i + 2) % length, (i + 4) % length), PARITY3)
        )
    completion.extend(
        [
            Gate((0, 2, w), PARITY3),
            Gate((1, 4, w), PARITY3),
        ]
    )

    host = x_gates + completion
    assert input_count == 2 * length - 1
    assert len(host) == input_count + 1
    assert min(input_degrees(input_count, host)) >= 2
    return input_count, x_gates, host, private, w


def parity_loose_x_witness(ell: int, target: tuple[int, ...]) -> tuple[int, ...]:
    """
    Realize every target on the distinguished parity-labeled loose X.

    Set w=0, v_0=target_0, v_3=target_3, all other cycle vertices zero.
    Each non-special edge has a private variable that fixes its remaining parity.
    """
    length = 2 * ell
    if len(target) != length:
        raise ValueError("target length mismatch")
    input_count, _x_gates, _host, private, w = build_parity_loose_x_host(ell)
    assignment = [0] * input_count
    assignment[0] = target[0]
    assignment[3] = target[3]
    assignment[w] = 0
    for i in range(length):
        if i in (0, 3):
            continue
        assignment[private[i]] = (
            target[i] ^ assignment[i] ^ assignment[(i + 1) % length]
        )
    return tuple(assignment)


def build_results() -> dict:
    essential_ternary = 0
    essential_unate = 0
    for mask in range(256):
        if essential_positions(mask, 3) != (0, 1, 2):
            continue
        essential_ternary += 1
        if all(unate_direction(mask, 3, j) is not None for j in range(3)):
            essential_unate += 1

    strict_rows = []
    for input_count in range(5, 11):
        gates = build_strict_balanced_unate_family(input_count)
        switched = switch_to_monotone(input_count, gates)
        assert switched is not None
        transformed, _r, q = switched
        original_range = output_range(input_count, gates)
        transformed_range = output_range(input_count, transformed)
        mapped_range = {
            tuple(word[e] ^ q[e] for e in range(len(gates)))
            for word in original_range
        }
        assert mapped_range == transformed_range
        strict_rows.append(
            {
                "n": input_count,
                "m": len(gates),
                "min_input_degree": min(input_degrees(input_count, gates)),
                "balanced": True,
                "raw_nonmonotone": any(
                    not is_monotone(gate.mask, 3) for gate in gates
                ),
                "all_essential_ternary": all(
                    essential_positions(gate.mask, 3) == (0, 1, 2)
                    for gate in gates
                ),
                "range_size": len(original_range),
            }
        )

    x_rows = []
    for ell in range(3, 7):
        length = 2 * ell
        input_count, x_gates, host, _private, _w = build_parity_loose_x_host(ell)
        verified = 0
        for target in product((0, 1), repeat=length):
            witness = parity_loose_x_witness(ell, target)
            if circuit_output(x_gates, witness) != target:
                raise AssertionError("parity loose-X witness failed")
            verified += 1
        host_range_size = len(output_range(input_count, host)) if ell == 3 else None
        x_rows.append(
            {
                "ell": ell,
                "x_edges": length,
                "host_inputs": input_count,
                "host_outputs": len(host),
                "min_host_input_degree": min(input_degrees(input_count, host)),
                "all_x_targets_verified": verified,
                "host_range_size_if_bruteforced": host_range_size,
            }
        )

    return {
        "laboratory": "V98",
        "result_type": (
            "switching-balanced unate extension plus loose-X support-only obstruction"
        ),
        "theorem_status": {
            "balanced_unate_recognizable_linear_incidence_time": True,
            "balanced_unate_switches_to_monotone": True,
            "balanced_unate_positive_surplus_component_avoidance_in_P_via_kuntewar_sarma": True,
            "strict_nonmonotone_irreducible_large_kernel_family": True,
            "loose_x_support_alone_insufficient_for_arbitrary_ternary_labels": True,
            "parity_labeled_loose_x_surjective": True,
            "unrestricted_NC0_3_avoid_polynomial_time": False,
            "hlz_worst_case_runtime_improved": False,
            "p_vs_np_resolved": False,
        },
        "ternary_truth_table_audit": {
            "all_masks": 256,
            "essential_ternary_masks": essential_ternary,
            "essential_ternary_unate_masks": essential_unate,
        },
        "strict_family_audit": {"rows": strict_rows},
        "loose_x_parity_audit": {"rows": x_rows},
        "literature_calibration": {
            "kuntewar_sarma_2025_monotone_nc03_m_gt_n_in_P": True,
            "v98_reduction_uses_published_monotone_algorithm_as_black_box": True,
            "novelty_confirmed": False,
        },
    }


if __name__ == "__main__":
    import json

    print(json.dumps(build_results(), indent=2, sort_keys=True))
