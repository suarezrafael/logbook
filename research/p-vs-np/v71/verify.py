#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from v71_width_correspondence import generate_results

HERE = Path(__file__).resolve().parent


def main():
    results = generate_results()
    (HERE / "RESULTS.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
    required = [
        "README.md", "WIDTH_CORRESPONDENCE.md", "THEOREM_STATUS.md",
        "V71_WIDTH_CORRESPONDENCE_THEOREM.tex", "MANUSCRIPT.tex",
        "REFERENCES.bib", "ECCC_METADATA.yaml", "RELEASE_PLAN.md",
        "V72_CORE_CONTEXT.md", "v71_width_correspondence.py",
        "verify.py", "verify_independent.py", "RESULTS.json",
    ]
    assert all((HERE / name).is_file() for name in required)
    assert results["status"] == "passed" and results["failures"] == 0
    assert results["exhaustive_hypergraphs_n4_m_le_5"] == 3472
    assert results["seeded_hypergraphs_n5"] == 160
    status = results["scientific_status"]
    assert status["standard_width_correspondence_proved"] is True
    assert status["constructible_pathwidth_order_proved"] is True
    assert status["bounded_treewidth_implies_bounded_linear_width"] is False
    assert status["general_polynomial_good_order_proved"] is False
    assert status["p_vs_np_resolved"] is False
    theorem = (HERE / "WIDTH_CORRESPONDENCE.md").read_text()
    for token in (
        "linear branch-width", "pw(P(H)) <= q*+r-1",
        "q* <= pw(P(H))+1", "G_proj(pi) <= m A(p+1)",
        "Treewidth alone does not bound `q*`",
    ):
        assert token in theorem
    tex = (HERE / "V71_WIDTH_CORRESPONDENCE_THEOREM.tex").read_text()
    for token in ("Exact width vocabulary", "Pathwidth sandwich", "m A(p+1)"):
        assert token in tex
    manuscript = (HERE / "MANUSCRIPT.tex").read_text().lower()
    for token in ("scientific status", "retracted", "open problems", "p versus np is unresolved"):
        assert token in manuscript
    metadata = (HERE / "ECCC_METADATA.yaml").read_text().lower()
    assert "draft_not_submitted" in metadata and "peer_reviewed: false" in metadata
    corpus = "\n".join(path.read_text().lower() for path in HERE.iterdir() if path.suffix in {".md", ".json", ".tex", ".yaml"})
    for forbidden in (
        "p versus np is solved", "we prove p != np", "accepted by eccc",
        "peer reviewed theorem", "novelty confirmed: true", "status: submitted",
    ):
        assert forbidden not in corpus
    print("V71 primary verification passed: width correspondence, pathwidth sandwich, 3,632 finite instances, manuscript and release gates; zero failures.")


if __name__ == "__main__":
    main()
