#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def check_v22() -> int:
    verify_path = ROOT / "v22" / "verify.py"
    tree = ast.parse(verify_path.read_text(encoding="utf-8"))
    positional = []
    string_literals = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "add_argument":
            if node.args and isinstance(node.args[0], ast.Constant):
                positional.append(node.args[0].value)
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            string_literals.append(node.value)
    assert "results" in positional
    assert "full_certificate_cases.json" in string_literals
    assert not (ROOT / "v22" / "full_certificate_cases.json").exists()
    aggregate = load(ROOT / "v22" / "RESULTS.json")
    assert aggregate["verification"]["complete_certificates"] == 125
    assert "cases" not in aggregate
    return 5


def check_runner() -> int:
    text = (ROOT / "verify_all.sh").read_text(encoding="utf-8")
    assert "V22|primary|v22/verify.py|skip|" in text
    assert "full_certificate_cases.json" in text
    assert 'if [[ "$tier" == "skip" ]]' in text
    assert "V61|primary|v61/verify.py|quick|" in text
    assert "V61|independent|v61/verify_independent.py|quick|" in text
    return 5


def check_ledger_and_state() -> int:
    ledger = load(ROOT / "LEDGER.json")
    results = load(HERE / "RESULTS.json")
    assert ledger["schema_version"] == 2
    assert ledger["current_version"] == "V61"
    assert ledger["program"]["p_vs_np_route_active"] is False
    issue = {x["id"]: x for x in ledger["reproducibility_issues"]}["v22-missing-certificate-dataset"]
    assert issue["reconstructible_from_results_json"] is False
    assert issue["runner_policy"] == "SKIP_with_reason"
    v22 = [x for x in ledger["versions"] if x["version"] == "V22"][0]
    assert "missing_original_certificate_artifact" in v22["status"]
    assert ledger["current_decision"]["v25_role"] == "supplementary_only"
    assert ledger["external_contact"]["status"] == "not_sent"
    assert results["version"] == "V61" and results["status"] == "passed"
    assert results["v22_repair"]["runner_status"] == "SKIP"
    assert results["manuscript"]["v25_in_main_narrative"] is False
    state = (ROOT / "STATE.md").read_text(encoding="utf-8")
    assert "P-versus-NP route active:** no" in state
    assert "V22 reproducibility correction" in state
    return 13


def check_prior_art_and_manuscript() -> int:
    audit = (HERE / "PRIOR_ART_AUDIT.md").read_text(encoding="utf-8")
    plan = (ROOT / "v60" / "MANUSCRIPT_PLAN.md").read_text(encoding="utf-8")
    abstract = (HERE / "MANUSCRIPT_ABSTRACT.md").read_text(encoding="utf-8")
    for token in (
        "ECCC TR22-048",
        "10.4230/LIPIcs.APPROX/RANDOM.2022.20",
        "ECCC TR23-021",
        "arXiv:2503.17114",
        "arXiv:cs/0506074",
        "arXiv:2309.01750",
    ):
        assert token in audit
    assert "positive/negative pair" in plan
    assert "Supplementary material" in plan
    assert "Four-input 222-class classification as supplementary context" not in plan
    assert "affine" in abstract.lower() and "bijunctive" in abstract.lower()
    assert "novelty" in abstract.lower()
    return 8


def main() -> None:
    total = check_v22() + check_runner() + check_ledger_and_state() + check_prior_art_and_manuscript()
    print(f"V61 primary verification passed: {total} audit checks; zero failures.")


if __name__ == "__main__":
    main()
