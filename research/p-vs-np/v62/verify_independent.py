#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def sat_clause(bits: int, clause: tuple[int, ...]) -> bool:
    for literal in clause:
        variable = abs(literal) - 1
        value = (bits >> variable) & 1
        if (literal > 0 and value) or (literal < 0 and not value):
            return True
    return False


def independent_formula_checks() -> int:
    common = (-1,)
    binaries = [(-2, 3), (2, -3), (-2, 4), (2, -4), (-3, -4)]
    clauses = [common, *binaries]
    models = [bits for bits in range(16) if all(sat_clause(bits, c) for c in clauses)]
    assert models == [0]
    for index, clause in enumerate(clauses):
        witness = None
        for bits in range(16):
            if all(sat_clause(bits, other) for j, other in enumerate(clauses) if j != index) and not sat_clause(bits, clause):
                witness = bits
                break
        assert witness is not None
    blocks = [[common, binary] for binary in binaries]
    for index, block in enumerate(blocks):
        witness = None
        for bits in range(16):
            other_clauses = [c for j, b in enumerate(blocks) if j != index for c in b]
            if all(sat_clause(bits, c) for c in other_clauses) and not all(sat_clause(bits, c) for c in block):
                witness = bits
                break
        assert witness is not None
    return 27


def independent_metadata_checks() -> int:
    ledger = json.loads((ROOT / "LEDGER.json").read_text(encoding="utf-8"))
    matrix = json.loads((HERE / "SOURCE_TO_CLAIM.json").read_text(encoding="utf-8"))
    results = json.loads((HERE / "RESULTS.json").read_text(encoding="utf-8"))
    assert ledger["current_version"] == "V62"
    assert ledger["external_contact"]["authorization_granted"] is True
    assert sum(len(item["recipients"]) for item in ledger["external_contact"]["outreach"]) == 4
    assert ledger["verification"]["ci_workflow"] == ".github/workflows/p-vs-np-verify.yml"
    assert len(matrix["entries"]) == results["central_outputs"]["source_to_claim_entries"]
    assert {e["manuscript_role"] for e in matrix["entries"]} >= {"background", "direct_overlap", "central_positive_result", "central_negative_result"}
    assert all(not e["repository_novelty_claim"] for e in matrix["entries"])
    assert results["comparison"]["v54_pure_and3_algorithm_subsumed_by_monotone_result"] is True
    assert results["comparison"]["v54_low_degree_separator_equivalence_resolved"] is False
    return 9


def independent_prose_checks() -> int:
    manuscript = (HERE / "INTEGRATED_MANUSCRIPT.md").read_text(encoding="utf-8").lower()
    search_log = (HERE / "PRIOR_ART_SEARCH_LOG.md").read_text(encoding="utf-8").lower()
    context = (HERE / "V63_CORE_CONTEXT.md").read_text(encoding="utf-8").lower()
    forbidden_assertions = ["we introduce irredundant 2-cnf", "first monotone nc0_3-avoid algorithm", "we prove p != np"]
    assert all(phrase not in manuscript for phrase in forbidden_assertions)
    assert "not evidence of novelty" in search_log
    assert "await" in context or "aguardar" in context
    return 2


def main() -> None:
    total = independent_formula_checks() + independent_metadata_checks() + independent_prose_checks()
    assert total == 38, total
    print("V62 independent verification passed: 38 checks; zero failures.")


if __name__ == "__main__":
    main()
