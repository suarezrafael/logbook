#!/usr/bin/env python3
"""V96 symbolic-size formulas and finite regression constructions.

The code audits two theorem families:

1. information-theoretic universal candidate lists for NC0_3-Avoid[N,N+1];
2. an explicit monotone-OR construction embedding logarithmically many arbitrary
   target words, giving a lower bound on every circuit-oblivious universal list.

None of these routines is a polynomial-time universal-list constructor for the
all-instance problem.  The upper bounds are existence/counting statements.
"""
from __future__ import annotations

import hashlib
import math
from typing import Iterable, Sequence


BitWord = tuple[int, ...]


def single_output_representation_bound(n: int, k: int = 3) -> int:
    """Overcount representations of one Boolean output depending on <=k inputs."""
    assert n >= k >= 0
    return sum(math.comb(n, j) * (1 << (1 << j)) for j in range(k + 1))


def circuit_oblivious_list_bound(n: int, k: int = 3) -> int:
    """Union-bound length for an N-only nonuniform universal candidate list."""
    q = single_output_representation_bound(n, k)
    return (n + 1) * math.ceil(math.log2(q)) + 1


def support_conditioned_list_bound(support_sizes: Iterable[int]) -> int:
    """Union-bound length once the ordered gate-support pattern is fixed."""
    sizes = tuple(support_sizes)
    assert all(0 <= size <= 3 for size in sizes)
    return 1 + sum(1 << size for size in sizes)


def or_block_embeddable_rows(n: int) -> int:
    """Rows embedded by the explicit three-block monotone-OR construction."""
    if n < 6:
        return 0
    return 3 * math.floor(math.log2(n / 3))


def deterministic_targets(n: int, count: int, case: int) -> list[BitWord]:
    """Stable regression targets; cryptographic hashing is only test-data plumbing."""
    m = n + 1
    result: list[BitWord] = []
    for row in range(count):
        bits = []
        for column in range(m):
            digest = hashlib.sha256(
                f"V96:{n}:{case}:{row}:{column}".encode("utf-8")
            ).digest()
            bits.append(digest[0] & 1)
        result.append(tuple(bits))
    return result


def block_or_embedding(n: int, targets: Sequence[BitWord]) -> dict:
    """Embed 3r arbitrary target words in one monotone 3-local OR circuit.

    Split the rows into three blocks of r.  For block b allocate one input
    x_(b,u) for every r-bit column pattern u.  Output coordinate i ORs the three
    inputs indexed by the three block-restrictions of target column i.
    A witness assignment for row (b,p) sets only block b, with x_(b,u)=u_p.
    """
    m = n + 1
    assert targets
    assert all(len(word) == m for word in targets)
    assert len(targets) % 3 == 0
    r = len(targets) // 3
    assert r >= 1
    assert 3 * (1 << r) <= n

    input_index: dict[tuple[int, int], int] = {}
    cursor = 0
    for block in range(3):
        for pattern in range(1 << r):
            input_index[(block, pattern)] = cursor
            cursor += 1

    supports: list[tuple[int, int, int]] = []
    for column in range(m):
        patterns: list[int] = []
        for block in range(3):
            pattern = 0
            for position in range(r):
                bit = targets[block * r + position][column]
                pattern |= bit << position
            patterns.append(pattern)
        supports.append(
            tuple(input_index[(block, patterns[block])] for block in range(3))
        )

    witnesses: list[BitWord] = []
    for block in range(3):
        for position in range(r):
            assignment = [0] * n
            for pattern in range(1 << r):
                assignment[input_index[(block, pattern)]] = (
                    pattern >> position
                ) & 1
            witnesses.append(tuple(assignment))

    for row, assignment in enumerate(witnesses):
        output = tuple(
            int(any(assignment[index] for index in support))
            for support in supports
        )
        assert output == targets[row]

    return {
        "r": r,
        "allocated_inputs": cursor,
        "supports": supports,
        "witness_inputs": witnesses,
    }


def _distinct_targets(length: int, count: int, case: int) -> list[BitWord]:
    assert count <= 1 << length
    result: list[BitWord] = []
    nonce = 0
    while len(result) < count:
        digest = hashlib.sha256(
            f"V96-fixed:{length}:{case}:{nonce}".encode("utf-8")
        ).digest()
        word = tuple((digest[index // 8] >> (index % 8)) & 1 for index in range(length))
        if word not in result:
            result.append(word)
        nonce += 1
    return result


def fixed_triple_embed(targets: Sequence[BitWord]) -> list[list[int]]:
    """Embed <=8 distinct targets when every output uses one common input triple."""
    distinct = list(dict.fromkeys(targets))
    assert distinct
    assert len(distinct) <= 8
    m = len(distinct[0])
    assert all(len(word) == m for word in distinct)

    tables = [[0] * 8 for _ in range(m)]
    for assignment, word in enumerate(distinct):
        for column, bit in enumerate(word):
            tables[column][assignment] = bit

    for assignment, word in enumerate(distinct):
        assert tuple(table[assignment] for table in tables) == word
    return tables


def representative_bounds() -> list[dict]:
    rows = []
    for n in (6, 12, 24, 48, 96):
        q = single_output_representation_bound(n)
        embedded = or_block_embeddable_rows(n)
        rows.append(
            {
                "input_count": n,
                "output_count": n + 1,
                "single_output_representation_bound": q,
                "ceil_log2_single_output_bound": math.ceil(math.log2(q)),
                "circuit_oblivious_nonuniform_upper": circuit_oblivious_list_bound(n),
                "all_ternary_support_conditioned_upper": 8 * (n + 1) + 1,
                "or_block_lower_embeddable_targets": embedded,
                "or_block_universal_lower_bound": embedded + 1,
            }
        )
    return rows


def build_results() -> dict:
    embedding_cases = 0
    embedded_rows = 0
    embedding_failures = 0
    input_budget_failures = 0
    for n in (6, 12, 24, 48, 96):
        count = or_block_embeddable_rows(n)
        for case in range(16):
            targets = deterministic_targets(n, count, case)
            try:
                model = block_or_embedding(n, targets)
                embedded_rows += count
                if model["allocated_inputs"] > n:
                    input_budget_failures += 1
            except AssertionError:
                embedding_failures += 1
            embedding_cases += 1

    fixed_triple_cases = 0
    fixed_triple_embedding_failures = 0
    for case in range(32):
        targets = _distinct_targets(length=9, count=8, case=case)
        try:
            fixed_triple_embed(targets)
        except AssertionError:
            fixed_triple_embedding_failures += 1
        fixed_triple_cases += 1

    return {
        "laboratory": "V96",
        "theorem_status": {
            "support_conditioned_linear_nonuniform_hitlist": True,
            "circuit_oblivious_nlogn_nonuniform_hitlist": True,
            "circuit_oblivious_hitlist_logarithmic_lower_bound": True,
            "fixed_triple_support_hitlist_number_nine": True,
            "uniform_hitlist_to_FP_NP_avoid_transfer": True,
            "constructive_polynomial_hitlist": False,
            "unrestricted_NC0_3_avoid_polynomial_time": False,
            "hlz_runtime_improved": False,
            "p_vs_np_resolved": False,
        },
        "symbolic_formulas": {
            "support_conditioned_upper": "1 + sum_i 2^{|S_i|} <= 8(N+1)+1",
            "circuit_oblivious_upper": "(N+1)*ceil(log2(sum_{j=0}^3 binom(N,j) 2^{2^j}))+1 = O(N log N)",
            "monotone_or_embeddable_targets": "3*floor(log2(N/3))",
            "circuit_oblivious_universal_lower": "3*floor(log2(N/3))+1",
            "fixed_common_triple_exact_number": 9,
        },
        "representative_bounds": representative_bounds(),
        "embedding_audit": {
            "input_sizes": [6, 12, 24, 48, 96],
            "cases_per_size": 16,
            "total_cases": embedding_cases,
            "total_embedded_target_rows": embedded_rows,
            "embedding_failures": embedding_failures,
            "input_budget_failures": input_budget_failures,
        },
        "fixed_triple_control": {
            "common_support_size": 3,
            "maximum_range_size": 8,
            "exact_universal_list_number": 9,
            "eight_target_embedding_cases": fixed_triple_cases,
            "embedding_failures": fixed_triple_embedding_failures,
        },
        "literature_calibration": {
            "hlz_k3_stretch_one_runtime": "O(N*2^(N/2))",
            "glw_2022_explicit_hitset_k3_stretch_threshold": "M >= 8192*N^2 + N",
            "glw_threshold_reaches_stretch_one": False,
            "ggnss_2023_FP_NP_transfer_stretch": "M=N+N^(2/3)",
            "uniform_minimal_stretch_solver_would_reach_transfer_by_truncation": True,
        },
    }


if __name__ == "__main__":
    import json

    print(json.dumps(build_results(), indent=2, sort_keys=True))
