#!/usr/bin/env python3
"""Primary verifier for Laboratory V60, made future-version safe in V61/V62."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def verify_probability_bound() -> int:
    checks = 0
    for n in range(0, 31):
        for stretch in range(1, 9):
            m = n + stretch
            success = Fraction((1 << m) - (1 << n), 1 << m)
            expected = 1 / success
            assert success == 1 - Fraction(1, 1 << stretch)
            assert expected == 1 / (1 - Fraction(1, 1 << stretch))
            assert success >= Fraction(1, 2)
            assert expected <= 2
            assert (expected == 2) == (stretch == 1)
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
    assert not missing, missing

    state = (ROOT / "STATE.md").read_text(encoding="utf-8")
    assert state.startswith("# Cumulative scientific state\n")
    assert len(state.encode("utf-8")) <= 100_000

    root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for token in ("STATE.md", "LEDGER.json", "verify_all.sh"):
        assert token in root_readme
    for token in ("P-versus-NP route active:** no", "n=9"):
        assert token in state
    historical_contact = (HERE / "EXTERNAL_CONTACT_STATUS.md").read_text(encoding="utf-8")
    assert "Status:** not sent" in historical_contact
    return len(required) + 4


def verify_ledgers() -> int:
    ledger = load_json(ROOT / "LEDGER.json")
    results = load_json(HERE / "RESULTS.json")
    assert ledger["schema_version"] >= 1
    assert ledger["program"]["p_vs_np_route_active"] is False
    assert ledger["program"]["p_vs_np_resolved"] is False
    assert ledger["current_decision"]["exact_n9_priority"] == "falsification_and_regression_only"
    assert ledger["finite_search"]["n9_complete"] is False
    assert isinstance(ledger["external_contact"]["status"], str)
    names = [entry["version"] for entry in ledger["versions"]]
    assert len(names) == len(set(names))
    assert "V60" in names
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
    return 22


def main() -> None:
    probability = verify_probability_bound()
    repository = verify_repository_state()
    ledger = verify_ledgers()
    print(
        "V60 primary verification passed: "
        f"{probability} probability cases; {repository} repository checks; "
        f"{ledger} ledger checks; total={probability + repository + ledger}; zero failures."
    )


if __name__ == "__main__":
    main()
