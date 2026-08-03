#!/usr/bin/env python3
from __future__ import annotations

from itertools import combinations
from math import ceil, comb, log2, sqrt
from pathlib import Path
import sys
from typing import Sequence

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "v80"))

from hall_branchwidth import EXAMPLES, exact_support_branchwidth, minimum_hall_witness

Support = tuple[int, ...]
NOR3_MASK = 1


def anf_coefficients(truth_mask: int, arity: int) -> tuple[int, ...]:
    values = [(int(truth_mask) >> x) & 1 for x in range(1 << arity)]
    for variable in range(arity):
        for x in range(1 << arity):
            if x & (1 << variable):
                values[x] ^= values[x ^ (1 << variable)]
    return tuple(values)


def c4_witnesses(supports: Sequence[Support]) -> tuple[tuple[int, int, tuple[int, int]], ...]:
    witnesses: list[tuple[int, int, tuple[int, int]]] = []
    for left, first in enumerate(supports):
        for right in range(left + 1, len(supports)):
            intersection = tuple(sorted(set(first) & set(supports[right])))
            for pair in combinations(intersection, 2):
                witnesses.append((left, right, tuple(pair)))
    return tuple(witnesses)


def incidence_girth(supports: Sequence[Support]) -> int | None:
    gate_count = len(supports)
    variables = sorted({variable for support in supports for variable in support})
    offset = gate_count
    adjacency: dict[int, set[int]] = {
        node: set() for node in range(gate_count + len(variables))
    }
    variable_index = {variable: offset + index for index, variable in enumerate(variables)}
    for gate, support in enumerate(supports):
        for variable in support:
            node = variable_index[variable]
            adjacency[gate].add(node)
            adjacency[node].add(gate)

    best: int | None = None
    for start in adjacency:
        distance = {start: 0}
        parent = {start: -1}
        queue = [start]
        for node in queue:
            for neighbor in adjacency[node]:
                if neighbor not in distance:
                    distance[neighbor] = distance[node] + 1
                    parent[neighbor] = node
                    queue.append(neighbor)
                elif parent[node] != neighbor:
                    length = distance[node] + distance[neighbor] + 1
                    best = length if best is None else min(best, length)
    return best


def monomial_index(variable_count: int) -> dict[tuple[int, ...], int]:
    monomials = [
        monomial
        for degree in (1, 2, 3)
        for monomial in combinations(range(variable_count), degree)
    ]
    return {monomial: index for index, monomial in enumerate(monomials)}


def global_nonconstant_anf_vector(
    support: Support, truth_mask: int, index: dict[tuple[int, ...], int]
) -> int:
    coefficients = anf_coefficients(truth_mask, len(support))
    vector = 0
    for local_subset in range(1, 1 << len(support)):
        if not coefficients[local_subset]:
            continue
        monomial = tuple(
            sorted(
                support[position]
                for position in range(len(support))
                if local_subset & (1 << position)
            )
        )
        vector ^= 1 << index[monomial]
    return vector


def gf2_rank(vectors: Sequence[int]) -> int:
    basis: dict[int, int] = {}
    for vector in vectors:
        reduced = int(vector)
        while reduced:
            pivot = reduced.bit_length() - 1
            if pivot in basis:
                reduced ^= basis[pivot]
            else:
                basis[pivot] = reduced
                break
    return len(basis)


def nonzero_constant_syndromes(vectors: Sequence[int]) -> int:
    count = 0
    for selector in range(1, 1 << len(vectors)):
        combined = 0
        for index, vector in enumerate(vectors):
            if selector & (1 << index):
                combined ^= vector
        if combined == 0:
            count += 1
    return count


def audit_example(name: str, specification: dict[str, object]) -> dict[str, object]:
    variable_count = int(specification["n"])
    supports = tuple(tuple(map(int, support)) for support in specification["supports"])
    gate_count = len(supports)
    assert len(set(supports)) == gate_count
    assert all(len(support) == 3 for support in supports)

    index = monomial_index(variable_count)
    nor_vectors = tuple(
        global_nonconstant_anf_vector(support, NOR3_MASK, index)
        for support in supports
    )
    minimum_size, _witness, neighborhood_size = minimum_hall_witness(supports)
    c4s = c4_witnesses(supports)
    rank = gf2_rank(nor_vectors)
    syndrome_count = nonzero_constant_syndromes(nor_vectors)

    assert rank == gate_count
    assert syndrome_count == 0
    assert incidence_girth(supports) == 4
    return {
        "name": name,
        "n": variable_count,
        "m": gate_count,
        "stretch": gate_count - variable_count,
        "c4_count": len(c4s),
        "incidence_girth": 4,
        "minimum_hall_deficient_gate_count": minimum_size,
        "minimum_hall_neighborhood_size": neighborhood_size,
        "support_branchwidth": exact_support_branchwidth(supports),
        "nor3_nonconstant_anf_rank": rank,
        "nonzero_constant_syndromes_under_nor3": syndrome_count,
        "small_hall_enumeration_still_applies": True,
        "bounded_width_enumeration_still_applies": True,
        "all_three_certificate_families_fail_simultaneously": False,
    }


def asymptotic_two_barrier_theorem() -> dict[str, object]:
    rows = []
    for n in (64, 512, 4096, 32768):
        m = n + ceil(n ** (2 / 3))
        collision_bound = comb(m, 2) / comb(n, 3)
        rows.append(
            {
                "n": n,
                "m": m,
                "duplicate_support_union_bound": collision_bound,
                "combined_with_v80_hall_bad_event_bound": (8 / 49) + collision_bound,
            }
        )
    return {
        "model": "independent uniformly random 3-subsets",
        "hall_bad_event_bound": "at most 8/49 for the V80 local-expansion range",
        "duplicate_support_bound": "binom(m,2)/binom(n,3)=O(1/n)",
        "conclusion": (
            "For all sufficiently large n, there exists a simple 3-uniform support "
            "family at target stretch with no Hall-deficient set of size at most "
            "n/(16e^2); assigning NOR3 to every gate gives no nonzero constant syndrome."
        ),
        "high_branchwidth_proved": False,
        "rows": rows,
    }


def restriction_no_pullback() -> dict[str, object]:
    unrestricted_range = {(0, 0), (1, 0)}
    restricted_range = {(0, 0)}
    target = (1, 0)
    assert target not in restricted_range
    assert target in unrestricted_range
    return {
        "map": "C(x)=(x,0)",
        "restriction": "x=0",
        "target": list(target),
        "avoids_restricted_map": True,
        "avoids_original_map": False,
    }


def width_gap_rows() -> list[dict[str, object]]:
    rows = []
    for n in (64, 512, 4096, 32768):
        m = n + ceil(n ** (2 / 3))
        stretch = m - n
        sqrt_log = sqrt(log2(m))
        rows.append(
            {
                "n": n,
                "m": m,
                "hard_branch_width_lower_bound": stretch,
                "v85_polynomial_width_scale": sqrt_log,
                "ratio": stretch / sqrt_log,
            }
        )
    return rows


def build_results() -> dict[str, object]:
    examples = {
        name: audit_example(name, specification)
        for name, specification in EXAMPLES.items()
    }
    return {
        "version": "V86",
        "status": "candidate",
        "scope": "intersection audit for Hall, syndrome, and width certificates",
        "examples": examples,
        "totals": {
            "examples": len(examples),
            "c4_witnesses": sum(row["c4_count"] for row in examples.values()),
            "nor3_nonconstant_anf_rank": sum(
                row["nor3_nonconstant_anf_rank"] for row in examples.values()
            ),
            "nonzero_constant_syndromes_under_nor3": 0,
        },
        "theorems": {
            "c4_is_necessary_not_sufficient_for_nonlinear_syndrome": True,
            "simple_3_uniform_nor3_has_no_constant_syndrome": True,
            "asymptotic_local_hall_plus_no_syndrome_family_exists": True,
            "asymptotic_high_branchwidth_for_that_family": False,
            "single_family_defeating_all_three_certificates_found": False,
            "restriction_of_inputs_has_no_avoidance_pullback": True,
            "sqrt_log_width_optimization_reaches_v84_hard_branch": False,
        },
        "asymptotic_two_barrier": asymptotic_two_barrier_theorem(),
        "width_gap": width_gap_rows(),
        "restriction_no_pullback": restriction_no_pullback(),
        "nonclaims": {
            "unrestricted_NC0_3_avoid_solved": False,
            "rigid_matrix_constructed": False,
            "new_unrestricted_circuit_lower_bound": False,
            "p_vs_np_resolved": False,
            "peer_reviewed": False,
            "novelty_confirmed": False,
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(build_results(), indent=2, sort_keys=True))
