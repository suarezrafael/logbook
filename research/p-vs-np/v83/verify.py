#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from selector_series import build_results

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def version_number(value: str) -> int:
    assert value.startswith("V") and value[1:].isdigit()
    return int(value[1:])


def main() -> None:
    committed = json.loads((HERE / "RESULTS.json").read_text(encoding="utf-8"))
    assert build_results() == committed

    readme = (HERE / "README.md").read_text(encoding="utf-8")
    proof = (HERE / "DEGREE_THREE_TRANSVERSAL_GIRTH_HARDNESS.md").read_text(
        encoding="utf-8"
    )
    theorem = (
        HERE / "V83_DEGREE_THREE_TRANSVERSAL_GIRTH_THEOREM.tex"
    ).read_text(encoding="utf-8")
    core = (HERE / "V84_CORE_CONTEXT.md").read_text(encoding="utf-8")

    for phrase in (
        "NP-complete",
        "path-selector series expansion",
        "exact circuit correspondence",
        "left degree <= 2",
        "left degree <= 3",
        "novelty and peer-review status remain unconfirmed",
    ):
        assert phrase.lower() in readme.lower()
    for phrase in (
        "Complete-chain equivalence",
        "threshold circuits are cliques",
        "no circuit below q",
        "maximum left degree three",
    ):
        assert phrase.lower() in proof.lower()
    assert "Exact circuit correspondence" in theorem
    assert "Degree-three transversal girth" in theorem
    assert "Priority one: exact FP^NP extraction" in core

    result_theorem = committed["theorem"]
    assert result_theorem["circuit_correspondence"] == "exact"
    assert result_theorem["maximum_expanded_left_degree"] == 3
    assert result_theorem["uniform_degree_girth_scaling"] is True

    census = committed["exhaustive_census"]
    assert census["source_presentations_checked"] == 768
    assert census["source_subset_states_checked"] == 7424
    assert census["expanded_subset_states_checked"] == 31184
    assert sum(row["graphs_checked"] for row in committed["colbourn_k4_graph_census"]) == 1088
    assert committed["direct_transformed_witnesses"] == [
        {
            "expanded_circuits": 1,
            "expanded_elements": 18,
            "expanded_girth": 18,
            "name": "K4",
            "source_elements": 6,
        },
        {
            "expanded_circuits": 0,
            "expanded_elements": 15,
            "expanded_girth": None,
            "name": "K4_minus_edge",
            "source_elements": 5,
        },
    ]
    assert committed["source_arithmetic_audit"]["identity_valid"] is False
    assert committed["source_arithmetic_audit"]["threshold_reproved_from_hall"] is True
    assert committed["complexity_conclusion"]["status"] == "NP-complete"
    assert committed["complexity_conclusion"]["novelty_confirmed"] is False
    assert committed["complexity_conclusion"]["p_vs_np_resolved"] is False

    status = json.loads((ROOT / "LAB_STATUS.json").read_text(encoding="utf-8"))
    promoted = status["promoted_version"]
    candidate = status.get("candidate_version")
    assert version_number(promoted) >= 82
    if candidate is None:
        assert status["highest_directory"] == promoted
        assert status["promotion_state"] == "promoted"
        assert status["next_laboratory_version"] == f"V{version_number(promoted) + 1}"
        reached = version_number(promoted)
    else:
        assert version_number(candidate) == version_number(promoted) + 1
        assert status["highest_directory"] == candidate
        assert status["promotion_state"] == "candidate"
        assert status["next_laboratory_version"] == candidate
        reached = version_number(candidate)
    assert reached >= 83
    assert status["infrastructure_frozen"] is True
    assert status["scientific_status"][
        "minimum_neighborhood_hall_polynomial_time"
    ] is None
    assert status["scientific_status"][
        "minimum_neighborhood_hall_np_hard"
    ] is True
    assert status["scientific_status"][
        "degree_three_transversal_girth_polynomial_time"
    ] is None
    assert status["scientific_status"][
        "degree_three_transversal_girth_np_hard"
    ] is True
    assert status["scientific_status"]["p_vs_np_resolved"] is False
    assert status["scientific_status"]["p_vs_np_route_active"] is False

    runner = (ROOT / "verify_all.sh").read_text(encoding="utf-8")
    assert "V83|primary|v83/verify.py|quick|" in runner
    assert "V83|independent|v83/verify_independent.py|quick|" in runner
    assert "V83" in runner.split("FOCUSED_VERSIONS=(", 1)[1].split(")", 1)[0]
    manifest = (ROOT / "LATEX_MODULES.tsv").read_text(encoding="utf-8")
    assert "v83\tv83/V83_DEGREE_THREE_TRANSVERSAL_GIRTH_THEOREM.tex" in manifest

    print(
        "V83 primary verification passed: exact path-selector circuit "
        "correspondence and degree-three transversal-girth NP-completeness "
        "remain preserved."
    )


if __name__ == "__main__":
    main()
