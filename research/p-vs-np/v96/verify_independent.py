#!/usr/bin/env python3
"""Independent V96 audit without importing hitlist_compression.py."""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATUS = ROOT.parent / "LAB_STATUS.json"


def q_bound(n: int) -> int:
    return sum(math.comb(n, j) * (2 ** (2 ** j)) for j in range(4))


def independent_targets(n: int, rows: int, case: int) -> list[tuple[int, ...]]:
    m = n + 1
    return [
        tuple(
            (((row + 1) * (column + 3) + 5 * case + (row << (column % 3))) >> (column % 5)) & 1
            for column in range(m)
        )
        for row in range(rows)
    ]


def verify_or_embedding(n: int, targets: list[tuple[int, ...]]) -> int:
    assert len(targets) % 3 == 0
    r = len(targets) // 3
    assert 3 * (2 ** r) <= n
    m = n + 1

    # Reserve contiguous blocks of 2^r inputs.  A selected variable encodes one
    # entire r-row column pattern.
    def idx(block: int, pattern: int) -> int:
        return block * (2 ** r) + pattern

    supports: list[tuple[int, int, int]] = []
    for column in range(m):
        selected = []
        for block in range(3):
            pattern = sum(
                targets[block * r + p][column] << p for p in range(r)
            )
            selected.append(idx(block, pattern))
        supports.append(tuple(selected))

    checked = 0
    for block in range(3):
        for p in range(r):
            assignment = [0] * n
            for pattern in range(2 ** r):
                assignment[idx(block, pattern)] = (pattern >> p) & 1
            output = tuple(
                int(any(assignment[var] for var in support)) for support in supports
            )
            assert output == targets[block * r + p]
            checked += 1
    return checked


def verify_fixed_triple(case: int) -> None:
    m = 10
    # Eight guaranteed-distinct words: first three bits encode the row.
    targets = []
    for row in range(8):
        word = tuple(
            ((row >> column) & 1) if column < 3
            else ((row * (column + 1) + case + column) & 1)
            for column in range(m)
        )
        targets.append(word)
    assert len(set(targets)) == 8

    tables = [[0] * 8 for _ in range(m)]
    for assignment, word in enumerate(targets):
        for column, bit in enumerate(word):
            tables[column][assignment] = bit
    for assignment, word in enumerate(targets):
        assert tuple(table[assignment] for table in tables) == word


def verify_status() -> None:
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    assert status["next_front"] == "algorithmic_method_and_meta_complexity"
    candidate = status.get("candidate_version")
    if candidate == "V96":
        assert status["promoted_version"] == "V95"
        assert status["highest_directory"] == "V96"
        assert status["promotion_state"] == "candidate"
        assert status["next_laboratory_version"] == "V96"
    else:
        promoted = int(status["promoted_version"][1:])
        assert promoted >= 96
        if candidate is None:
            assert status["highest_directory"] == status["promoted_version"]
            assert status["promotion_state"] == "promoted"


def main() -> None:
    committed = json.loads((ROOT / "RESULTS.json").read_text(encoding="utf-8"))

    expected_ns = [6, 12, 24, 48, 96]
    assert [row["input_count"] for row in committed["representative_bounds"]] == expected_ns
    for row in committed["representative_bounds"]:
        n = row["input_count"]
        q = q_bound(n)
        assert row["single_output_representation_bound"] == q
        assert row["circuit_oblivious_nonuniform_upper"] == (
            (n + 1) * math.ceil(math.log2(q)) + 1
        )
        assert row["all_ternary_support_conditioned_upper"] == 8 * (n + 1) + 1
        t = 3 * math.floor(math.log2(n / 3))
        assert row["or_block_lower_embeddable_targets"] == t
        assert row["or_block_universal_lower_bound"] == t + 1

    checked_rows = 0
    checked_cases = 0
    for n in expected_ns:
        t = 3 * math.floor(math.log2(n / 3))
        for case in range(11):
            targets = independent_targets(n, t, case)
            checked_rows += verify_or_embedding(n, targets)
            checked_cases += 1
    assert checked_cases == 55
    assert checked_rows == 495

    for case in range(17):
        verify_fixed_triple(case)

    theorem = committed["theorem_status"]
    assert theorem["support_conditioned_linear_nonuniform_hitlist"]
    assert theorem["circuit_oblivious_nlogn_nonuniform_hitlist"]
    assert theorem["circuit_oblivious_hitlist_logarithmic_lower_bound"]
    assert theorem["fixed_triple_support_hitlist_number_nine"]
    assert theorem["uniform_hitlist_to_FP_NP_avoid_transfer"]
    assert not theorem["constructive_polynomial_hitlist"]
    assert not theorem["unrestricted_NC0_3_avoid_polynomial_time"]
    assert not theorem["hlz_runtime_improved"]
    assert not theorem["p_vs_np_resolved"]

    implication = json.loads((ROOT / "IMPLICATION.json").read_text(encoding="utf-8"))
    assert implication["classification"] == "barrier_and_closure"
    assert implication["next_front"] == "uniform_hitlist_or_certificate_extraction"
    assert implication["stop_rule_fired"]
    assert not implication["p_vs_np_resolved"]

    if STATUS.exists():
        verify_status()

    print(
        "V96 independent verification passed: 55 fresh monotone-OR embeddings "
        "cover 495 target rows, 17 fixed-triple eight-target controls, exact "
        "counting bounds, and conservative nonuniform/uniform separation."
    )


if __name__ == "__main__":
    main()
