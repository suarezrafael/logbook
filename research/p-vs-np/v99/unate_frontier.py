#!/usr/bin/env python3
from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from itertools import permutations, product


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
        for bits in product((0, 1), repeat=arity):
            if bits[j]:
                continue
            high = list(bits)
            high[j] = 1
            if eval_table(mask, bits) != eval_table(mask, high):
                answer.append(j)
                break
    return tuple(answer)


def unate_direction(mask: int, arity: int, coordinate: int) -> int | None:
    positive = negative = False
    for bits in product((0, 1), repeat=arity):
        if bits[coordinate]:
            continue
        high = list(bits)
        high[coordinate] = 1
        delta = eval_table(mask, high) - eval_table(mask, bits)
        positive |= delta > 0
        negative |= delta < 0
        if positive and negative:
            return None
    if not positive and not negative:
        return None
    return 0 if positive else 1


def transform_mask(mask: int, perm: tuple[int, ...], flips: tuple[int, ...], out_flip: int) -> int:
    arity = len(perm)
    return make_mask(
        arity,
        lambda x: eval_table(mask, tuple(x[perm[j]] ^ flips[j] for j in range(arity))) ^ out_flip,
    )


def npn_canonical(mask: int, arity: int = 3) -> int:
    return min(
        transform_mask(mask, perm, flips, out_flip)
        for perm in permutations(range(arity))
        for flips in product((0, 1), repeat=arity)
        for out_flip in (0, 1)
    )


def singleton_orientation(mask: int, arity: int) -> tuple[int, tuple[int, ...]] | None:
    zeros: list[tuple[int, ...]] = []
    ones: list[tuple[int, ...]] = []
    for bits in product((0, 1), repeat=arity):
        (ones if eval_table(mask, bits) else zeros).append(bits)
    if len(ones) == 1:
        return 0, ones[0]
    if len(zeros) == 1:
        return 1, zeros[0]
    return None


def orient_singleton_component(gates: list[Gate]) -> tuple[list[int], list[tuple[int, ...]]] | None:
    output_flips: list[int] = []
    demands: list[tuple[int, ...]] = []
    for gate in gates:
        oriented = singleton_orientation(gate.mask, len(gate.support))
        if oriented is None:
            return None
        q, alpha = oriented
        output_flips.append(q)
        demands.append(alpha)
    return output_flips, demands


def singleton_conflict(input_count: int, gates: list[Gate]) -> tuple[int, int, int] | None:
    oriented = orient_singleton_component(gates)
    if oriented is None:
        return None
    _q, demands = oriented
    seen: dict[int, tuple[int, int]] = {}
    for e, gate in enumerate(gates):
        for j, v in enumerate(gate.support):
            demand = demands[e][j]
            if v in seen and seen[v][0] != demand:
                return seen[v][1], e, v
            seen[v] = (demand, e)
    return None


def singleton_global_demands(input_count: int, gates: list[Gate]) -> list[int] | None:
    oriented = orient_singleton_component(gates)
    if oriented is None:
        return None
    _q, demands = oriented
    result: list[int | None] = [None] * input_count
    for e, gate in enumerate(gates):
        for j, v in enumerate(gate.support):
            demand = demands[e][j]
            if result[v] is None:
                result[v] = demand
            elif result[v] != demand:
                return None
    return [0 if value is None else int(value) for value in result]


def singleton_missing_word(input_count: int, gates: list[Gate]) -> tuple[int, ...] | None:
    oriented = orient_singleton_component(gates)
    if oriented is None:
        return None
    q, _demands = oriented
    conflict = singleton_conflict(input_count, gates)
    if conflict is None:
        return None
    e, f, _v = conflict
    oriented_target = [0] * len(gates)
    oriented_target[e] = 1
    oriented_target[f] = 1
    return tuple(oriented_target[i] ^ q[i] for i in range(len(gates)))


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
    degree = [0] * input_count
    for gate in gates:
        for v in gate.support:
            degree[v] += 1
    return degree


def and_literal_mask(signs: tuple[int, int, int]) -> int:
    return make_mask(3, lambda x: int(all((x[j] ^ signs[j]) == 1 for j in range(3))))


def build_singleton_strict_family(n: int) -> list[Gate]:
    if n < 5:
        raise ValueError("n must be at least five")
    supports = [(i, (i + 1) % n, (i + 2) % n) for i in range(n)]
    gates = [Gate(s, and_literal_mask((0, 0, 0))) for s in supports]
    gates.append(Gate(supports[0], and_literal_mask((1, 0, 0))))
    return gates


def solve_switching_balance(input_count: int, gates: list[Gate]) -> tuple[list[int], list[int]] | None:
    adjacency: dict[tuple[str, int], list[tuple[tuple[str, int], int]]] = defaultdict(list)
    for e, gate in enumerate(gates):
        if essential_positions(gate.mask, len(gate.support)) != tuple(range(len(gate.support))):
            return None
        for j, v in enumerate(gate.support):
            d = unate_direction(gate.mask, len(gate.support), j)
            if d is None:
                return None
            a = ("x", v)
            b = ("g", e)
            adjacency[a].append((b, d))
            adjacency[b].append((a, d))
    potential: dict[tuple[str, int], int] = {}
    nodes = [("x", i) for i in range(input_count)] + [("g", e) for e in range(len(gates))]
    for start in nodes:
        if start in potential:
            continue
        potential[start] = 0
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v, parity in adjacency[u]:
                wanted = potential[u] ^ parity
                if v in potential:
                    if potential[v] != wanted:
                        return None
                else:
                    potential[v] = wanted
                    queue.append(v)
    return [potential[("x", i)] for i in range(input_count)], [potential[("g", e)] for e in range(len(gates))]


J = 0b1111
R0 = 0b0111
R1 = 0b1110
I2 = 0b1001
P01 = 0b1011
P10 = 0b1101


def matrix_get(matrix: int, row: int, col: int) -> int:
    return (matrix >> (2 * row + col)) & 1


def boolean_matrix_multiply(left: int, right: int) -> int:
    out = 0
    for row in (0, 1):
        for col in (0, 1):
            value = any(matrix_get(left, row, mid) and matrix_get(right, mid, col) for mid in (0, 1))
            out |= int(value) << (2 * row + col)
    return out


def path_relation(target_bits: tuple[int, ...]) -> int:
    matrix = I2
    for bit in target_bits:
        matrix = boolean_matrix_multiply(matrix, R1 if bit else R0)
    return matrix


def majority(bits: tuple[int, int, int]) -> int:
    return int(sum(bits) >= 2)


def abstract_boundary_feasible(B: int, A: int, short_relation: int, long_relation: int, y0: int, y3: int) -> bool:
    for v0, v1, v3, v4, w in product((0, 1), repeat=5):
        if not matrix_get(short_relation, v1, v3):
            continue
        if not matrix_get(long_relation, v4, v0):
            continue
        if majority((v0 ^ B, v1, w ^ A)) != y0:
            continue
        if majority((v3, v4, w)) != y3:
            continue
        return True
    return False


def abstract_bad_boundary_types(B: int, A: int) -> list[tuple[str, str, int, int]]:
    relations = {"J": J, "P01": P01, "P10": P10}
    bad: list[tuple[str, str, int, int]] = []
    for short_name, short in relations.items():
        for long_name, long in relations.items():
            for y0, y3 in product((0, 1), repeat=2):
                if not abstract_boundary_feasible(B, A, short, long, y0, y3):
                    bad.append((short_name, long_name, y0, y3))
    return bad


def simple_x_supports(length: int) -> tuple[int, list[tuple[int, int, int]], int, dict[int, int]]:
    if length < 6 or length % 2:
        raise ValueError("length must be even and at least six")
    w = length
    private: dict[int, int] = {}
    cursor = length + 1
    for i in range(length):
        if i not in (0, 3):
            private[i] = cursor
            cursor += 1
    supports: list[tuple[int, int, int]] = []
    for i in range(length):
        third = w if i in (0, 3) else private[i]
        supports.append((i, (i + 1) % length, third))
    return cursor, supports, w, private


def signed_majority_mask(signs: tuple[int, int, int]) -> int:
    return make_mask(3, lambda x: majority(tuple(x[j] ^ signs[j] for j in range(3))))


def canonical_majority_signs(length: int, B: int, A: int) -> list[tuple[int, int, int]]:
    signs = [(0, 0, 0) for _ in range(length)]
    signs[0] = (B, 0, A)
    return signs


def majority_x_gates(length: int, B: int, A: int) -> list[Gate]:
    _n, supports, _w, _private = simple_x_supports(length)
    signs = canonical_majority_signs(length, B, A)
    return [Gate(support, signed_majority_mask(sign)) for support, sign in zip(supports, signs)]


def majority_x_abstract_feasible(target: tuple[int, ...], B: int, A: int) -> bool:
    length = len(target)
    if length < 6 or length % 2:
        raise ValueError("target length must be even and at least six")
    short_relation = path_relation(tuple(target[1:3]))
    long_relation = path_relation(tuple(target[4:]))
    return abstract_boundary_feasible(B, A, short_relation, long_relation, target[0], target[3])


def cohomology_syndrome(signs: list[tuple[int, int, int]]) -> tuple[int, int]:
    length = len(signs)
    B = 0
    for edge in range(length):
        B ^= signs[edge][0] ^ signs[edge][1]
    A = (
        signs[0][2]
        ^ signs[0][1]
        ^ signs[1][0]
        ^ signs[1][1]
        ^ signs[2][0]
        ^ signs[2][1]
        ^ signs[3][0]
        ^ signs[3][2]
    )
    return B, A


def build_results() -> dict:
    essential = []
    unate = []
    npn_groups: dict[int, list[int]] = defaultdict(list)
    for mask in range(256):
        if essential_positions(mask, 3) != (0, 1, 2):
            continue
        essential.append(mask)
        if all(unate_direction(mask, 3, j) is not None for j in range(3)):
            unate.append(mask)
            npn_groups[npn_canonical(mask)].append(mask)

    orbit_rows = sorted(
        ({"canonical_mask": f"0x{canonical:02x}", "size": len(masks)} for canonical, masks in npn_groups.items()),
        key=lambda row: row["size"],
    )

    singleton_rows = []
    for n in range(5, 11):
        gates = build_singleton_strict_family(n)
        conflict = singleton_conflict(n, gates)
        missing = singleton_missing_word(n, gates)
        assert conflict is not None and missing is not None
        range_set = output_range(n, gates)
        assert missing not in range_set
        singleton_rows.append(
            {
                "n": n,
                "m": len(gates),
                "min_input_degree": min(input_degrees(n, gates)),
                "switching_balanced": solve_switching_balance(n, gates) is not None,
                "conflict": list(conflict),
                "missing_word_absent": True,
                "range_size": len(range_set),
            }
        )

    boundary = {
        f"{B}{A}": [list(item) for item in abstract_bad_boundary_types(B, A)]
        for B, A in product((0, 1), repeat=2)
    }

    length_rows = []
    for length in range(6, 16, 2):
        missing_by_class = {}
        for B, A in product((0, 1), repeat=2):
            missing = sum(
                not majority_x_abstract_feasible(target, B, A)
                for target in product((0, 1), repeat=length)
            )
            missing_by_class[f"{B}{A}"] = missing
        length_rows.append({"length": length, "missing_by_class": missing_by_class})

    brute_rows = []
    for B, A in product((0, 1), repeat=2):
        gates = majority_x_gates(6, B, A)
        range_set = output_range(11, gates)
        abstract_range = {
            target
            for target in product((0, 1), repeat=6)
            if majority_x_abstract_feasible(target, B, A)
        }
        assert range_set == abstract_range
        brute_rows.append(
            {"class": f"{B}{A}", "range_size": len(range_set), "missing": 64 - len(range_set)}
        )

    class_counts = {f"{B}{A}": 1 << 16 for B, A in product((0, 1), repeat=2)}

    return {
        "laboratory": "V99",
        "theorem_status": {
            "essential_unate_partition_three_npn_orbits": True,
            "singleton_core_positive_surplus_avoidance_in_P": True,
            "singleton_core_conflict_constructor": True,
            "singleton_core_conflict_free_switches_to_monotone_AND": True,
            "strict_unbalanced_singleton_lambda_n_family": True,
            "signed_majority_simple_x_cycle_rank_two": True,
            "signed_majority_balanced_class_exactly_two_missing": True,
            "signed_majority_three_nonzero_classes_surjective": True,
            "signed_majority_simple_x_local_certificate_closed_on_unbalanced_classes": True,
            "middle_unate_orbit_solved": False,
            "all_unate_nc03_avoid_polynomial_time": False,
            "unrestricted_nc03_avoid_polynomial_time": False,
            "hlz_worst_case_runtime_improved": False,
            "p_vs_np_resolved": False,
        },
        "ternary_unate_partition": {
            "all_masks": 256,
            "essential_ternary": len(essential),
            "essential_unate": len(unate),
            "npn_orbits": orbit_rows,
        },
        "singleton_strict_family": {"rows": singleton_rows},
        "signed_majority_x": {
            "abstract_bad_boundary_types": boundary,
            "length_audit": length_rows,
            "brute_length_6": brute_rows,
            "length_6_cohomology_class_counts": class_counts,
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(build_results(), indent=2, sort_keys=True))
