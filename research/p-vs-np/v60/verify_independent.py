#!/usr/bin/env python3
"""Independent verifier for Laboratory V60.

This implementation does not import verify.py. It reconstructs the counting
argument through direct enumeration for small dimensions, validates the JSON
ledger shape and checks that the prose contains the promoted/nonpromoted
boundaries.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def outside_fraction_for_injective_prefix(n: int, m: int) -> tuple[int, int]:
    assert m > n
    image = {bits + (0,) * (m - n) for bits in itertools.product((0, 1), repeat=n)}
    cube = set(itertools.product((0, 1), repeat=m))
    return len(cube - image), len(cube)


def independent_counting_checks() -> int:
    checks = 0
    for n in range(0, 8):
        for stretch in range(1, 5):
            m = n + stretch
            outside, total = outside_fraction_for_injective_prefix(n, m)
            expected_outside = (1 << m) - (1 << n)
            assert outside == expected_outside
            assert total == 1 << m
            assert 2 * outside >= total
            if stretch == 1:
                assert 2 * outside == total
            else:
                assert 2 * outside > total
            checks += 1
    return checks


def independent_ledger_checks() -> int:
    ledger = json.loads((ROOT / "LEDGER.json").read_text(encoding="utf-8"))
    results = json.loads((HERE / "RESULTS.json").read_text(encoding="utf-8"))

    required_top = {
        "schema_version",
        "updated",
        "current_version",
        "program",
        "current_decision",
        "stable_results",
        "retractions",
        "open_questions",
        "versions",
        "finite_search",
        "external_contact",
        "verification",
    }
    assert required_top.issubset(ledger)
    assert isinstance(ledger["stable_results"], list) and ledger["stable_results"]
    assert isinstance(ledger["versions"], list) and ledger["versions"]

    for entry in ledger["versions"]:
        assert set(entry) == {"version", "path", "contribution", "status"}
        assert entry["version"].startswith("V")

    assert all(item["status"] == "retracted" for item in ledger["retractions"])
    assert results["scientific_status"]["p_vs_np_resolved"] is False
    assert results["scientific_status"]["unrestricted_lower_bound_proved"] is False
    assert results["repository_repairs"]["main_merged"] is False
    return 10 + len(ledger["versions"])


def independent_prose_checks() -> int:
    theorem = (HERE / "THEOREM.md").read_text(encoding="utf-8")
    proof = (HERE / "PROOF.md").read_text(encoding="utf-8")
    status = (HERE / "SCIENTIFIC_STATUS.md").read_text(encoding="utf-8")
    manuscript = (HERE / "MANUSCRIPT_PLAN.md").read_text(encoding="utf-8")
    external = (HERE / "EXTERNAL_CONTACT_STATUS.md").read_text(encoding="utf-8")

    required_fragments = [
        (theorem, "1 - 2^(n-m)"),
        (theorem, "expected number of tests is at most two"),
        (proof, "geometric random variable"),
        (proof, "does not construct a deterministic walk"),
        (status, "Not promoted"),
        (status, "n=9"),
        (manuscript, "Material to omit"),
        (manuscript, "Related work"),
        (external, "not sent"),
    ]
    for text, fragment in required_fragments:
        assert fragment in text, fragment
    return len(required_fragments)


def main() -> None:
    counting = independent_counting_checks()
    ledger = independent_ledger_checks()
    prose = independent_prose_checks()
    print(
        "V60 independent verification passed: "
        f"{counting} exhaustive small-cube counts; "
        f"{ledger} ledger/schema checks; {prose} prose-boundary checks; zero failures."
    )


if __name__ == "__main__":
    main()
