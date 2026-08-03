#!/usr/bin/env python3
"""V88: exact collision normal form for the repeated-table Eval_H map."""
from __future__ import annotations

from collections import Counter
from itertools import combinations, product
from typing import Iterable, Sequence

Support = tuple[int, ...]
TargetMatrix = tuple[tuple[int, ...], ...]


def validate_instance(
    supports: Sequence[Sequence[int]], targets: Sequence[Sequence[int]], n: int
) -> None:
    if n < 0:
        raise ValueError("n must be nonnegative")
    if not targets:
        raise ValueError("at least one target row is required")
    m = len(supports)
    if any(len(row) != m for row in targets):
        raise ValueError("every target row must have one bit per support")
    if any(bit not in (0, 1) for row in targets for bit in row):
        raise ValueError("targets must be Boolean")
    for support in supports:
        if not support:
            raise ValueError("supports must be nonempty")
        if len(set(support)) != len(support):
            raise ValueError("support variables must be distinct")
        if any(variable < 0 or variable >= n for variable in support):
            raise ValueError("support variable outside [0,n)")


def pattern_bit(pattern: int, row: int) -> int:
    """Read one normalized witness-row bit from a variable column pattern."""
    if row == 0:
        return 0
    return (pattern >> (row - 1)) & 1


def separated_on_support(
    patterns: Sequence[int], support: Sequence[int], row_a: int, row_b: int
) -> bool:
    return any(
        pattern_bit(patterns[variable], row_a)
        != pattern_bit(patterns[variable], row_b)
        for variable in support
    )


def patterns_cover_targets(
    supports: Sequence[Sequence[int]],
    targets: Sequence[Sequence[int]],
    patterns: Sequence[int],
    n: int,
) -> bool:
    validate_instance(supports, targets, n)
    if len(patterns) != n:
        raise ValueError("one normalized pattern is required per variable")
    k = len(targets)
    if any(pattern < 0 or pattern >= (1 << (k - 1)) for pattern in patterns):
        raise ValueError("pattern outside the normalized k-row alphabet")

    for output, support in enumerate(supports):
        for row_a in range(k):
            for row_b in range(row_a + 1, k):
                if targets[row_a][output] == targets[row_b][output]:
                    continue
                if not separated_on_support(patterns, support, row_a, row_b):
                    return False
    return True


def collision_normal_form_coverable(
    supports: Sequence[Sequence[int]], targets: Sequence[Sequence[int]], n: int
) -> tuple[bool, tuple[int, ...] | None]:
    """Decide the exact normal form by enumerating normalized variable patterns."""
    validate_instance(supports, targets, n)
    alphabet = range(1 << (len(targets) - 1))
    for patterns in product(alphabet, repeat=n):
        if patterns_cover_targets(supports, targets, patterns, n):
            return True, patterns
    return False, None


def direct_table_consistency_coverable(
    supports: Sequence[Sequence[int]], targets: Sequence[Sequence[int]], n: int
) -> tuple[bool, tuple[int, ...] | None]:
    """Direct tiny-instance audit using normalized witnesses and observed addresses.

    The first witness is normalized to zero. XOR-translating every witness by the
    original first witness preserves all equality relations among local addresses,
    which are the only relations relevant to extending the observed values to full
    local truth tables.
    """
    validate_instance(supports, targets, n)
    k = len(targets)
    for tail in product(range(1 << n), repeat=k - 1):
        witnesses = (0,) + tail
        consistent = True
        for output, support in enumerate(supports):
            observed: dict[tuple[int, ...], int] = {}
            for row, witness in enumerate(witnesses):
                address = tuple((witness >> variable) & 1 for variable in support)
                value = int(targets[row][output])
                previous = observed.get(address)
                if previous is not None and previous != value:
                    consistent = False
                    break
                observed[address] = value
            if not consistent:
                break
        if consistent:
            return True, witnesses
    return False, None


def pair_constructor(
    supports: Sequence[Sequence[int]], targets: Sequence[Sequence[int]], n: int
) -> tuple[int, ...]:
    """Construct normalized patterns covering every two-row target list."""
    validate_instance(supports, targets, n)
    if len(targets) != 2:
        raise ValueError("the pair constructor requires exactly two rows")
    active_variables: set[int] = set()
    for output, support in enumerate(supports):
        if targets[0][output] != targets[1][output]:
            active_variables.update(support)
    patterns = tuple(1 if variable in active_variables else 0 for variable in range(n))
    assert patterns_cover_targets(supports, targets, patterns, n)
    return patterns


def equal_pair_label(column: Sequence[int]) -> int | None:
    """For a nonconstant three-bit column, return its unique equal-row pair.

    Labels are 0=(rows 0,1), 1=(rows 0,2), and 2=(rows 1,2). Constant columns
    impose no collision constraint and return None.
    """
    if len(column) != 3:
        raise ValueError("three target bits are required")
    a, b, c = (int(bit) for bit in column)
    if a == b == c:
        return None
    if a == b:
        return 0
    if a == c:
        return 1
    return 2


def colors_to_patterns(colors: Sequence[int]) -> tuple[int, ...]:
    """Map active three-row colors to normalized patterns 01,10,11."""
    mapping = (0b10, 0b01, 0b11)
    if any(color not in (0, 1, 2) for color in colors):
        raise ValueError("three-row colors must lie in {0,1,2}")
    return tuple(mapping[color] for color in colors)


def three_row_coloring_coverable(
    supports: Sequence[Sequence[int]], targets: Sequence[Sequence[int]], n: int
) -> tuple[bool, tuple[int, ...] | None]:
    """Exact three-row reduction to a labeled three-color hypergraph problem."""
    validate_instance(supports, targets, n)
    if len(targets) != 3:
        raise ValueError("the coloring reduction requires exactly three rows")
    labels = [
        equal_pair_label(tuple(targets[row][output] for row in range(3)))
        for output in range(len(supports))
    ]
    for colors in product(range(3), repeat=n):
        valid = True
        for support, label in zip(supports, labels):
            if label is None:
                continue
            first = colors[support[0]]
            if all(colors[variable] == first for variable in support) and first != label:
                valid = False
                break
        if valid:
            patterns = colors_to_patterns(colors)
            assert patterns_cover_targets(supports, targets, patterns, n)
            return True, colors
    return False, None


def all_simple_ternary_families(n: int) -> Iterable[tuple[Support, ...]]:
    triples = tuple(combinations(range(n), 3))
    for mask in range(1, 1 << len(triples)):
        yield tuple(triples[index] for index in range(len(triples)) if mask & (1 << index))


def targets_from_bits(k: int, m: int, bits: int) -> TargetMatrix:
    return tuple(
        tuple((bits >> (row * m + output)) & 1 for output in range(m))
        for row in range(k)
    )


def build_results() -> dict:
    n = 4
    aggregate: Counter[tuple[int, int, bool]] = Counter()
    equivalence_mismatches = 0
    coloring_mismatches = 0
    pair_constructor_failures = 0
    target_instances = 0

    for supports in all_simple_ternary_families(n):
        m = len(supports)
        for k in (1, 2, 3):
            for bits in range(1 << (k * m)):
                targets = targets_from_bits(k, m, bits)
                normal, _ = collision_normal_form_coverable(supports, targets, n)
                direct, _ = direct_table_consistency_coverable(supports, targets, n)
                equivalence_mismatches += normal != direct
                if k == 2:
                    patterns = pair_constructor(supports, targets, n)
                    pair_constructor_failures += not patterns_cover_targets(
                        supports, targets, patterns, n
                    )
                if k == 3:
                    colored, _ = three_row_coloring_coverable(supports, targets, n)
                    coloring_mismatches += normal != colored
                aggregate[(k, m, normal)] += 1
                target_instances += 1

    breakdown: list[dict] = []
    for (k, m, coverable), count in sorted(aggregate.items()):
        breakdown.append(
            {
                "rows": k,
                "supports": m,
                "coverable": coverable,
                "instances": count,
            }
        )

    uncovered = sum(
        count for (k, _m, coverable), count in aggregate.items() if not coverable
    )
    return {
        "laboratory": "V88",
        "scope": "collision normal form for repeated-table Eval_H",
        "theorems": {
            "collision_normal_form": (
                "A target list is coverable iff normalized variable-row patterns "
                "separate every differing target pair on its output support."
            ),
            "pair_constructor": (
                "Every two-row target list is coverable by activating the union "
                "of supports on which the two targets differ."
            ),
            "three_row_reduction": (
                "Three-row coverability is exactly a labeled three-color "
                "hypergraph problem; a nonconstant target column labels its "
                "unique equal row pair."
            ),
        },
        "finite_audit": {
            "variables": n,
            "simple_ternary_support_families": (1 << 4) - 1,
            "target_instances": target_instances,
            "rows_checked": [1, 2, 3],
            "equivalence_mismatches": equivalence_mismatches,
            "three_row_coloring_mismatches": coloring_mismatches,
            "pair_constructor_failures": pair_constructor_failures,
            "uncovered_targets": uncovered,
            "breakdown": breakdown,
        },
        "parameterization": {
            "normalized_alphabet_size": "2^(k-1)",
            "local_separation_constraints_upper_bound": "m*binom(k,2)",
            "three_row_active_colors": 3,
        },
        "scientific_status": {
            "constructive_eval_h_list": False,
            "constructor_model_lower_bound": False,
            "explicit_deterministic_three_certificate_family": False,
            "eval_h_collision_normal_form": True,
            "eval_h_pairwise_obstruction_impossible": True,
            "eval_h_three_row_labeled_hypergraph_reduction": True,
            "p_vs_np_resolved": False,
            "peer_reviewed": False,
            "novelty_confirmed": False,
        },
    }


if __name__ == "__main__":
    import json

    print(json.dumps(build_results(), indent=2, sort_keys=True))
