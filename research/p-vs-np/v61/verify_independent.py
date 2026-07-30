#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def check_json_shapes() -> int:
    ledger = json.loads((ROOT / "LEDGER.json").read_text(encoding="utf-8"))
    results = json.loads((HERE / "RESULTS.json").read_text(encoding="utf-8"))
    assert set(("schema_version", "current_version", "program", "stable_results", "reproducibility_issues", "prior_art", "versions")).issubset(ledger)
    assert ledger["current_version"] == "V61"
    assert len(ledger["prior_art"]) >= 7
    assert results["prior_art"]["primary_sources_recorded"] >= 7
    assert results["program_decision"]["p_vs_np_route_active"] is False
    return 5


def check_no_false_repair() -> int:
    status = (ROOT / "v22" / "REPRODUCIBILITY_STATUS.md").read_text(encoding="utf-8")
    readme = (ROOT / "v22" / "README.md").read_text(encoding="utf-8")
    assert "Not reproducible" in status
    assert "cannot be recovered uniquely" in status
    assert "not repository-reproduced" in readme
    assert "no replacement dataset will be presented as the original artifact" in readme
    return 4


def check_claim_boundaries() -> int:
    audit = (HERE / "PRIOR_ART_AUDIT.md").read_text(encoding="utf-8")
    forbidden = [
        "we introduce irredundant 2-CNF",
        "the first monotone `NC0_3-Avoid` algorithm",
        "a new randomized algorithm for Avoid",
        "this advances P versus NP",
    ]
    for phrase in forbidden:
        assert phrase in audit
    assert "specific constrained construction novelty unresolved" in audit
    assert "exact prior art not located; novelty unconfirmed" in audit
    return 6


def check_runner_static() -> int:
    runner = (ROOT / "verify_all.sh").read_text(encoding="utf-8")
    rows = re.findall(r'"(V\d+\|[^"]+)"', runner)
    assert any(row.startswith("V22|") and "|skip|" in row for row in rows)
    assert any(row.startswith("V61|primary|") for row in rows)
    assert any(row.startswith("V61|independent|") for row in rows)
    assert "failures > 0" in runner
    return 4


def check_context() -> int:
    context = (HERE / "V62_CORE_CONTEXT.md").read_text(encoding="utf-8")
    for token in ("P versus NP", "Kuntewar", "não enviado", "n=9"):
        assert token in context
    return 4


def main() -> None:
    total = check_json_shapes() + check_no_false_repair() + check_claim_boundaries() + check_runner_static() + check_context()
    print(f"V61 independent verification passed: {total} independent checks; zero failures.")


if __name__ == "__main__":
    main()
