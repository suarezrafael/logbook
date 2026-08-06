#!/usr/bin/env python3
from __future__ import annotations

import json
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def gate(table: int, bit: int) -> int:
    return (table >> bit) & 1


def output(tables: tuple[int, int], x: int) -> tuple[int, int]:
    return gate(tables[0], x), gate(tables[1], x)


def count(tables: tuple[int, int], prefix: tuple[int, ...]) -> int:
    return sum(output(tables, x)[: len(prefix)] == prefix for x in (0, 1))


def independent_unary_audit() -> int:
    checked = 0
    for tables in product(range(4), repeat=2):
        prefix: tuple[int, ...] = ()
        current = 2
        for _ in range(2):
            if current == 0:
                prefix += (0,) * (2 - len(prefix))
                break
            zero = count(tables, prefix + (0,))
            one = count(tables, prefix + (1,))
            assert zero + one == current
            bit = 0 if zero <= one else 1
            prefix += (bit,)
            current = zero if bit == 0 else one
        assert len(prefix) == 2
        assert count(tables, prefix) == 0
        checked += 1
    return checked


def main() -> None:
    assert independent_unary_audit() == 16

    results = json.loads((ROOT / "RESULTS.json").read_text(encoding="utf-8"))
    binary = results["exhaustive_binary"]
    assert binary["same_as_v75_capacity_policy"] + binary["different_from_v75_capacity_policy"] == 4096
    assert sum(binary["halving_step_histogram"].values()) == 4096
    assert binary["claim_6_8_mismatches"] == 0
    assert results["seeded_ternary"]["claim_6_8_mismatches"] == 0

    implication = json.loads((ROOT / "IMPLICATION.json").read_text(encoding="utf-8"))
    assert implication["current_gap"].startswith("The first missing bridge is runtime")
    assert "2^Omega(n)" in implication["current_gap"]

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "total semantic completion" in readme
    assert "not a total polynomial-time completion" in readme
    assert "does not give a polynomial-time all-instance algorithm" in readme

    next_context = (ROOT / "V93_CORE_CONTEXT.md").read_text(encoding="utf-8")
    assert "high-width child-count compression gate" in next_context
    assert "No experiment is authorized" in next_context
    assert "Chen–Hu–Ren" in next_context

    status = json.loads((ROOT.parent / "LAB_STATUS.json").read_text(encoding="utf-8"))
    assert status["promoted_version"] in {"V91", "V92"} or int(status["promoted_version"][1:]) > 92
    if status["candidate_version"] == "V92":
        assert status["highest_directory"] == "V92"
        assert status["promotion_state"] == "candidate"
    assert not status["scientific_status"]["v92_published_lower_bound_transfer_triggered"]
    assert not status["scientific_status"]["p_vs_np_resolved"]

    print(
        "V92 independent verification passed: exhaustive unary halving, closed-form "
        "ledger checks, explicit runtime gap, and conservative nonclaims."
    )


if __name__ == "__main__":
    main()
