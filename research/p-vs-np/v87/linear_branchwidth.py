#!/usr/bin/env python3
"""V87: linear branchwidth from a random-pair shadow."""
from __future__ import annotations

import itertools
import json
import math
import random
from pathlib import Path
from typing import Iterable, Sequence

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

Support = tuple[int, ...]


def support_masks(supports: Sequence[Support]) -> tuple[int, ...]:
    return tuple(sum(1 << variable for variable in support) for support in supports)


def subset_unions(supports: Sequence[Support]) -> list[int]:
    masks = support_masks(supports)
    unions = [0] * (1 << len(masks))
    for mask in range(1, 1 << len(masks)):
        bit = mask & -mask
        index = bit.bit_length() - 1
        unions[mask] = unions[mask ^ bit] | masks[index]
    return unions


def minimum_balanced_connectivity(supports: Sequence[Support]) -> dict[str, object]:
    gate_count = len(supports)
    full = (1 << gate_count) - 1
    lower = math.ceil(gate_count / 3)
    upper = (2 * gate_count) // 3
    unions = subset_unions(supports)
    best = 10**9
    minimizers = 0
    one_mask = 0
    checked = 0
    for mask in range(1, full):
        size = mask.bit_count()
        if lower <= size <= upper:
            checked += 1
            value = (unions[mask] & unions[full ^ mask]).bit_count()
            if value < best:
                best = value
                minimizers = 1
                one_mask = mask
            elif value == best:
                minimizers += 1
    return {
        "balanced_range": [lower, upper],
        "minimum_balanced_lambda": best,
        "minimizer_count": minimizers,
        "one_minimizer": [
            index for index in range(gate_count) if (one_mask >> index) & 1
        ],
        "balanced_subsets_checked": checked,
    }


def exact_support_branchwidth(supports: Sequence[Support]) -> int:
    unions = subset_unions(supports)
    gate_count = len(supports)
    full = (1 << gate_count) - 1
    connectivity = [
        (unions[mask] & unions[full ^ mask]).bit_count()
        for mask in range(1 << gate_count)
    ]
    dynamic = [0] * (1 << gate_count)
    for index in range(gate_count):
        dynamic[1 << index] = connectivity[1 << index]
    for size in range(2, gate_count + 1):
        for indices in itertools.combinations(range(gate_count), size):
            mask = sum(1 << index for index in indices)
            anchor = mask & -mask
            best = 10**9
            subset = (mask - 1) & mask
            while subset:
                if subset & anchor and subset != mask:
                    complement = mask ^ subset
                    best = min(
                        best,
                        max(
                            connectivity[mask],
                            dynamic[subset],
                            dynamic[complement],
                        ),
                    )
                subset = (subset - 1) & mask
            dynamic[mask] = best
    return dynamic[full]


def primal_edges(supports: Sequence[Support]) -> tuple[tuple[int, int], ...]:
    return tuple(
        sorted(
            {
                tuple(sorted(pair))
                for support in supports
                for pair in itertools.combinations(support, 2)
            }
        )
    )


def exact_treewidth(variable_count: int, edges: Iterable[tuple[int, int]]) -> int:
    adjacency = [0] * variable_count
    for left, right in edges:
        adjacency[left] |= 1 << right
        adjacency[right] |= 1 << left

    best = variable_count

    def search(active: int, current: list[int], width: int) -> None:
        nonlocal best
        if active == 0:
            best = min(best, width)
            return
        if width >= best:
            return

        vertices = [
            vertex for vertex in range(variable_count) if (active >> vertex) & 1
        ]
        vertices.sort(key=lambda vertex: (current[vertex] & active).bit_count())
        for vertex in vertices:
            neighborhood = current[vertex] & active & ~(1 << vertex)
            next_width = max(width, neighborhood.bit_count())
            if next_width >= best:
                continue
            updated = current.copy()
            remaining_neighbors = [
                other
                for other in range(variable_count)
                if (neighborhood >> other) & 1
            ]
            for other in remaining_neighbors:
                updated[other] |= neighborhood & ~(1 << other)
            search(active & ~(1 << vertex), updated, next_width)

    search((1 << variable_count) - 1, adjacency, 0)
    return best


def transfer_census() -> dict[str, object]:
    triples = tuple(itertools.combinations(range(5), 3))
    checked = 0
    violations = 0
    maximum_treewidth = 0
    maximum_branchwidth = 0
    equality_cases = 0
    by_gate_count: dict[str, int] = {}
    for gate_count in range(2, 7):
        count = 0
        for supports in itertools.combinations(triples, gate_count):
            branchwidth = exact_support_branchwidth(supports)
            treewidth = exact_treewidth(5, primal_edges(supports))
            upper = max(3, math.ceil(3 * branchwidth / 2))
            if treewidth + 1 > upper:
                violations += 1
            if treewidth + 1 == upper:
                equality_cases += 1
            maximum_treewidth = max(maximum_treewidth, treewidth)
            maximum_branchwidth = max(maximum_branchwidth, branchwidth)
            checked += 1
            count += 1
        by_gate_count[str(gate_count)] = count
    return {
        "families_checked": checked,
        "by_gate_count": by_gate_count,
        "violations": violations,
        "equality_cases": equality_cases,
        "maximum_treewidth": maximum_treewidth,
        "maximum_branchwidth": maximum_branchwidth,
        "verified_inequality": "tw(primal)+1 <= max(3, ceil(3*bw/2))",
    }


def pair_shadow_uniformity(variable_count: int = 6) -> dict[str, object]:
    counts = {
        pair: 0 for pair in itertools.combinations(range(variable_count), 2)
    }
    for triple in itertools.combinations(range(variable_count), 3):
        for pair in itertools.combinations(triple, 2):
            counts[pair] += 1
    values = sorted(set(counts.values()))
    return {
        "n": variable_count,
        "triples": math.comb(variable_count, 3),
        "pairs": math.comb(variable_count, 2),
        "occurrences_per_pair": values,
        "expected_occurrences_per_pair": variable_count - 2,
        "uniform": values == [variable_count - 2],
    }


def sample_simple_supports(
    variable_count: int, gate_count: int, seed: int
) -> tuple[Support, ...]:
    rng = random.Random(seed)
    universe = tuple(itertools.combinations(range(variable_count), 3))
    return tuple(rng.sample(universe, gate_count))


def random_balanced_census() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for variable_count in (10, 12, 14, 16):
        gate_count = variable_count + math.ceil(variable_count ** (2 / 3))
        for offset in range(2):
            seed = 87000 + 100 * variable_count + offset
            supports = sample_simple_supports(variable_count, gate_count, seed)
            audit = minimum_balanced_connectivity(supports)
            rows.append(
                {
                    "n": variable_count,
                    "m": gate_count,
                    "seed": seed,
                    "minimum_balanced_lambda": audit[
                        "minimum_balanced_lambda"
                    ],
                    "minimum_balanced_lambda_over_n": (
                        audit["minimum_balanced_lambda"] / variable_count
                    ),
                    "minimizer_count": audit["minimizer_count"],
                    "balanced_subsets_checked": audit[
                        "balanced_subsets_checked"
                    ],
                }
            )
    return rows


def v80_balanced_census() -> dict[str, object]:
    source = json.loads(
        (ROOT / "v80" / "RESULTS.json").read_text(encoding="utf-8")
    )
    rows: dict[str, object] = {}
    for name, record in source["examples"].items():
        supports = tuple(
            tuple(map(int, support)) for support in record["supports"]
        )
        rows[name] = {
            "n": int(record["n"]),
            "m": int(record["m"]),
            **minimum_balanced_connectivity(supports),
        }
    return rows


def fixed_cut_expectation(
    variable_count: int, gate_count: int, selected_gate_count: int
) -> float:
    avoid_one_variable = (variable_count - 3) / variable_count
    return variable_count * (
        1
        - avoid_one_variable**selected_gate_count
        - avoid_one_variable ** (gate_count - selected_gate_count)
        + avoid_one_variable**gate_count
    )


def fixed_cut_expectation_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for variable_count in (64, 256, 1024, 4096):
        gate_count = variable_count + math.ceil(variable_count ** (2 / 3))
        selected = math.ceil(gate_count / 3)
        expectation = fixed_cut_expectation(
            variable_count, gate_count, selected
        )
        rows.append(
            {
                "n": variable_count,
                "m": gate_count,
                "selected_gates": selected,
                "expected_lambda": expectation,
                "expected_lambda_over_n": expectation / variable_count,
            }
        )
    return rows


def binary_entropy(value: float) -> float:
    if value in (0.0, 1.0):
        return 0.0
    return -value * math.log(value) - (1 - value) * math.log(1 - value)


def mcdiarmid_audit() -> dict[str, object]:
    alpha = 1 / 3
    entropy_rate = binary_entropy(alpha)
    support_replacement_lipschitz = 6
    optimistic_best_tail_rate = 2 / (
        support_replacement_lipschitz**2
    )
    asymptotic_expected_fixed_cut = (
        1 - math.exp(-1) - math.exp(-2) + math.exp(-3)
    )
    subtract_full_cube_approximation = (
        (1 - math.exp(-1)) + (1 - math.exp(-2)) - 1
    )
    return {
        "balanced_fraction": alpha,
        "balanced_subset_entropy_rate_per_gate": entropy_rate,
        "support_replacement_lipschitz": support_replacement_lipschitz,
        "optimistic_maximum_mcdiarmid_tail_rate_per_n": (
            optimistic_best_tail_rate
        ),
        "entropy_exceeds_best_tail_rate": (
            entropy_rate > optimistic_best_tail_rate
        ),
        "asymptotic_expected_fixed_cut_lambda_over_n": (
            asymptotic_expected_fixed_cut
        ),
        "incorrect_subtract_n_approximation": (
            subtract_full_cube_approximation
        ),
        "missing_unused_vertex_term": math.exp(-3),
        "conclusion": (
            "Direct bounded-differences plus a union bound over all "
            "balanced gate subsets cannot prove uniform linear connectivity."
        ),
    }


def build_results() -> dict[str, object]:
    return {
        "laboratory": "V87",
        "scope": (
            "linear support branchwidth via a random-pair shadow and "
            "completion of the three-certificate obstruction"
        ),
        "theorems": {
            "rank_three_transfer": (
                "For every rank-at-most-three hypergraph H, "
                "tw(primal(H))+1 <= max(3, ceil(3*bw(H)/2))."
            ),
            "pair_shadow": (
                "A uniformly selected pair inside a uniformly random "
                "3-subset is a uniform random graph edge."
            ),
            "linear_branchwidth": (
                "At m=n+ceil(n^(2/3)), the V86 random simple support "
                "model has support branchwidth Omega(n) with high probability."
            ),
            "three_certificate_obstruction": (
                "For all sufficiently large n, one simple 3-uniform "
                "support family simultaneously has linear-scale local Hall "
                "expansion, no constant NOR3 syndrome, and linear branchwidth."
            ),
            "mcdiarmid_no_go": (
                "The direct McDiarmid union bound over all balanced cuts "
                "does not close; a random-graph shadow is used instead."
            ),
        },
        "pair_shadow_uniformity": pair_shadow_uniformity(),
        "transfer_census": transfer_census(),
        "v80_balanced_census": v80_balanced_census(),
        "random_balanced_census": random_balanced_census(),
        "fixed_cut_expectations": fixed_cut_expectation_rows(),
        "mcdiarmid_audit": mcdiarmid_audit(),
        "scientific_status": {
            "same_family_defeats_hall_syndrome_and_width_certificates": True,
            "support_branchwidth_linear_for_v86_random_model": True,
            "explicit_deterministic_three_certificate_family": False,
            "constructive_eval_h_list": False,
            "unrestricted_NC0_3_avoid_solved": False,
            "rigid_matrix_constructed": False,
            "p_vs_np_resolved": False,
            "novelty_confirmed": False,
            "peer_reviewed": False,
        },
    }


if __name__ == "__main__":
    print(json.dumps(build_results(), indent=2, sort_keys=True))
