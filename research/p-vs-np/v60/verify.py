#!/usr/bin/env python3
"""Primary verifier for Laboratory V60.

Uses only the Python standard library. It checks the exact probability theorem,
repository orientation files, cumulative ledger invariants and preserved V59
finite-search status.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise AssertionError(f"Expected JSON object: {path}")
    return value


def verify_probability_bound() -> int:
    checks = 0
    for n in range(0, 31):
        for stretch in range(1, 9):
            m = n + stretch
            image_upper = 1 << n
            cube_size = 1 << m
            success = Fraction(cube_size - image_upper, cube_size)
            expected = 1 / success
            formula_success = 1 - Fraction(1, 1 << stretch)
            formula_expected = 1 / formula_success
            assert success == formula_success
            assert expected == formula_expected
            assert success >= Fraction(1, 2)
            assert expected <= 2
            if stretch == 1:
                assert expected == 2
            else:
                assert expected < 2
            checks += 1
    return checks


def verify_repository_state() -> int:
    required = [
        ROOT / "README.md",
        ROOT / "STATE.md",
        ROOT / "LEDGER.json",
        ROOT / "verify_all.sh",
        HERE / "README.md",
        HERE / "THEOREM.md",
        HERE / "PROOF.md",
        HERE / "SCIENTIFIC_STATUS.md",
        HERE / "MANUSCRIPT_PLAN.md",
        HERE / "RESULTS.json",
        HERE / "EXTERNAL_CONTACT_STATUS.md",
        HERE / "V61_CORE_CONTEXT.md",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    assert not missing, f"Missing required files: {missing}"

    state_lines = (ROOT / "STATE.md").read_text(encoding="utf-8").splitlines()
    assert len(state_lines) <= 200, f"STATE.md exceeds 200 lines: {len(state_lines)}"

    root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for token in ("STATE.md", "LEDGER.json", "verify_all.sh", "v60/"):
        assert token in root_readme
    assert "V22" in root_readme  # retained as historical entry, not active result
    assert "Current position" in root_readme

    state = (ROOT / "STATE.md").read_text(encoding="utf-8")
    for token in ("P-versus-NP route active:** no", "n=9", "not sent"):
        assert token in state

    return len(required) + 4


def verify_ledgers() -> int:
    ledger = load_json(ROOT / "LEDGER.json")
    results = load_json(HERE / "RESULTS.json")

    assert ledger["schema_version"] == 1
    assert ledger["current_version"] == "V60"
    assert ledger["program"]["p_vs_np_route_active"] is False
    assert ledger["program"]["p_vs_np_resolved"] is False
    assert ledger["current_decision"]["exact_n9_priority"] == "falsification_and_regression_only"
    assert ledger["finite_search"]["n9_complete"] is False
    assert ledger["external_contact"]["status"] == "not_sent"

    versions = ledger["versions"]
    names = [entry["version"] for entry in versions]
    assert len(names) == len(set(names)), "Duplicate version entries"
    assert names[-1] == "V60"
    assert {"V53", "V56", "V57", "V58", "V59", "V60"}.issubset(names)

    retractions = {entry["id"]: entry for entry in ledger["retractions"]}
    assert retractions["v53-girth-union-free"]["status"] == "retracted"
    assert retractions["v53-log-syndrome-degree"]["status"] == "retracted"

    stable_ids = {entry["id"] for entry in ledger["stable_results"]}
    assert "v60-randomized-easy-membership" in stable_ids
    assert "v59-flat-potentials" in stable_ids

    assert results["version"] == "V60"
    assert results["status"] == "passed"
    assert results["central_result"]["uniform_upper_bound_for_positive_stretch"] == 2
    assert results["central_result"]["deterministic_algorithm_implied"] is False
    assert results["program_decision"]["p_vs_np_route_active"] is False
    assert results["preserved_status"]["n9_complete"] is False
    assert results["preserved_status"]["external_contact_sent"] is False

    v59_path = ROOT / "v59" / "RESULTS.json"
    if v59_path.is_file():
        v59 = load_json(v59_path)
        assert v59["central_results"]["n9_exact_search_complete"] is False
        assert v59["central_results"]["direct_sum_flat_potential_barrier"] is True

    return 23


def main() -> None:
    probability_checks = verify_probability_bound()
    repository_checks = verify_repository_state()
    ledger_checks = verify_ledgers()
    total = probability_checks + repository_checks + ledger_checks
    print(
        "V60 primary verification passed: "
        f"{probability_checks} probability cases; "
        f"{repository_checks} repository checks; "
        f"{ledger_checks} ledger checks; total={total}; zero failures."
    )


if __name__ == "__main__":
    main()
