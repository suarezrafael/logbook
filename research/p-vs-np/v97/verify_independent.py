#!/usr/bin/env python3
"""Independent V97 audit; does not import peeling_kernel.py."""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATUS = ROOT.parent / "LAB_STATUS.json"


def bit(table: int, index: int) -> int:
    return (table >> index) & 1


def missing_from_two_rows(rows: set[tuple[int, int]]) -> tuple[int, int]:
    for value in range(4):
        word = (value & 1, (value >> 1) & 1)
        if word not in rows:
            return word
    raise AssertionError("two-row image unexpectedly fills four words")


def exhaustive_leaf_rule() -> int:
    checked = 0
    # x occurs only in g0(x,y); g1,g2 depend only on y.
    for g0 in range(16):
        depends_on_x = any(bit(g0, y << 1) != bit(g0, 1 | (y << 1)) for y in (0, 1))
        if not depends_on_x:
            continue
        for g1 in range(4):
            for g2 in range(4):
                reduced = {(bit(g1, y), bit(g2, y)) for y in (0, 1)}
                t1, t2 = missing_from_two_rows(reduced)
                target = (0, t1, t2)
                image = {
                    (bit(g0, x | (y << 1)), bit(g1, y), bit(g2, y))
                    for x in (0, 1) for y in (0, 1)
                }
                assert target not in image
                checked += 1
    return checked


def exhaustive_unary_rule() -> int:
    checked = 0
    # Unary identity/negation output forces x after target 0.
    for negate in (0, 1):
        forced_x = negate
        for g1 in range(16):
            for g2 in range(16):
                reduced = {
                    (bit(g1, forced_x | (y << 1)), bit(g2, forced_x | (y << 1)))
                    for y in (0, 1)
                }
                t1, t2 = missing_from_two_rows(reduced)
                target = (0, t1, t2)
                image = set()
                for x in (0, 1):
                    for y in (0, 1):
                        unary = x ^ negate
                        image.add((unary, bit(g1, x | (y << 1)), bit(g2, x | (y << 1))))
                assert target not in image
                checked += 1
    return checked


def strict_family_output(n: int, assignment: int) -> tuple[int, ...]:
    h = max(3, math.ceil(math.log2(n)))
    def x(index: int) -> int:
        return (assignment >> index) & 1
    outputs = []
    for i in range(h + 1):
        outputs.append(x(i % h) ^ x((i + 1) % h) ^ x((i + 2) % h))
    for z in range(h, n):
        outputs.append(x(0) ^ x(1) ^ x(z))
    assert len(outputs) == n + 1
    return tuple(outputs)


def strict_family_missing_target(n: int) -> tuple[int, ...]:
    h = max(3, math.ceil(math.log2(n)))
    core_range = {
        strict_family_output(n, assignment)[: h + 1]
        for assignment in range(1 << h)
    }
    missing_core = None
    for value in range((1 << h) + 1):
        word = tuple((value >> pos) & 1 for pos in range(h + 1))
        if word not in core_range:
            missing_core = word
            break
    assert missing_core is not None
    return missing_core + (0,) * (n - h)


def verify_strict_family() -> tuple[int, int]:
    brute_cases = 0
    failures = 0
    for n in (8, 16):
        target = strict_family_missing_target(n)
        image = {strict_family_output(n, assignment) for assignment in range(1 << n)}
        failures += int(target in image)
        brute_cases += 1
    return brute_cases, failures


def verify_status() -> None:
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    assert status["next_front"] == "algorithmic_method_and_meta_complexity"
    candidate = status.get("candidate_version")
    if candidate == "V97":
        assert status["promoted_version"] == "V96"
        assert status["highest_directory"] == "V97"
        assert status["promotion_state"] == "candidate"
    else:
        assert int(status["promoted_version"][1:]) >= 97
        if candidate is None:
            assert status["highest_directory"] == status["promoted_version"]
            assert status["promotion_state"] == "promoted"


def main() -> None:
    committed = json.loads((ROOT / "RESULTS.json").read_text(encoding="utf-8"))

    leaf_cases = exhaustive_leaf_rule()
    unary_cases = exhaustive_unary_rule()
    brute_cases, strict_failures = verify_strict_family()
    assert leaf_cases == 192
    assert unary_cases == 512
    assert brute_cases == 2
    assert strict_failures == 0

    rows = committed["strict_extension_family"]["rows"]
    for row in rows:
        n = row["input_count"]
        h = max(3, math.ceil(math.log2(n)))
        assert row["rho"] == n
        assert row["lambda"] == h
        assert row["leaf_pair_deletions"] == n - h
        assert row["output_count"] == n + 1

    theorem = committed["theorem_status"]
    assert theorem["peeling_kernel_comparison_free_avoider"]
    assert theorem["lambda_never_exceeds_rho"]
    assert theorem["strict_extension_of_v96_parameter"]
    assert theorem["nonmonotone_ternary_strict_family"]
    assert not theorem["unrestricted_NC0_3_avoid_polynomial_time"]
    assert not theorem["hlz_worst_case_runtime_improved"]
    assert not theorem["p_vs_np_resolved"]

    implication = json.loads((ROOT / "IMPLICATION.json").read_text(encoding="utf-8"))
    assert implication["classification"] == "frontier_progress"
    assert implication["next_front"] == "irreducible_nonmonotone_turan_certificates"
    assert implication["material_advance_rule_met"]
    assert implication["stop_rule_fired"]

    if STATUS.exists():
        verify_status()

    print(
        "V97 independent verification passed: 192 exhaustive leaf-rule tables, "
        "512 exhaustive unary-forcing tables, strict parity family controls, "
        "and conservative status/implication checks."
    )


if __name__ == "__main__":
    main()
