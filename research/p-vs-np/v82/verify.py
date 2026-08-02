#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from transversal_girth import build_results

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main() -> None:
    committed = json.loads((HERE / "RESULTS.json").read_text(encoding="utf-8"))
    assert build_results() == committed

    audit = (HERE / "TRANSVERSAL_GIRTH_COMPLEXITY_AUDIT.md").read_text(
        encoding="utf-8"
    )
    readme = (HERE / "README.md").read_text(encoding="utf-8")
    core = (HERE / "V83_CORE_CONTEXT.md").read_text(encoding="utf-8")
    theorem = (
        HERE / "V82_TRANSVERSAL_GIRTH_EQUIVALENCE_THEOREM.tex"
    ).read_text(encoding="utf-8")

    for phrase in (
        "h*(G) = girth(T(G)) - 1",
        "deficiency exactly one",
        "Colbourn and Elmallah",
        "Degree at most two",
        "degree three",
        "three focused mathematical iterations",
    ):
        assert phrase.lower() in audit.lower()
    assert "does not settle transversal girth for left degree three" in readme
    assert "Three-iteration stopping rule" in core
    assert "Hall--girth equivalence" in theorem
    assert "Deficiency-one separation" in theorem

    status = json.loads((ROOT / "LAB_STATUS.json").read_text(encoding="utf-8"))
    assert status["promoted_version"] == "V81"
    assert status["candidate_version"] == "V82"
    assert status["highest_directory"] == "V82"
    assert status["promotion_state"] == "candidate"
    assert status["infrastructure_frozen"] is True
    assert status["next_laboratory_version"] == "V82"
    assert status["scientific_status"][
        "degree_three_transversal_girth_polynomial_time"
    ] is None
    assert status["scientific_status"][
        "degree_three_transversal_girth_np_hard"
    ] is None
    assert status["scientific_status"]["p_vs_np_route_active"] is False

    runner = (ROOT / "verify_all.sh").read_text(encoding="utf-8")
    assert "V82|primary|v82/verify.py|quick|" in runner
    assert "V82|independent|v82/verify_independent.py|quick|" in runner
    assert "V82" in runner.split("FOCUSED_VERSIONS=(", 1)[1].split(")", 1)[0]
    manifest = (ROOT / "LATEX_MODULES.tsv").read_text(encoding="utf-8")
    assert (
        "v82\tv82/V82_TRANSVERSAL_GIRTH_EQUIVALENCE_THEOREM.tex"
        in manifest
    )

    census = committed["v80_rank_three_census"]
    assert sum(row["subset_states_checked"] for row in census.values()) == 22528
    assert [census[name]["transversal_girth"] for name in (
        "seven_variables", "eight_variables", "nine_variables"
    )] == [7, 8, 9]
    for row in census.values():
        assert row["hstar_equals_girth_minus_one"] is True
        assert (
            row[
                "all_inclusion_minimal_hstar_minimizers_have_deficiency_one"
            ]
            is True
        )
        assert row["transversal_rank"] == row["n"]

    controls = committed["degree_two_controls"]
    assert {row["bicircular_topology"] for row in controls.values()} == {
        "theta",
        "tight_handcuff",
        "loose_handcuff",
    }
    assert all(row["hstar_equals_girth_minus_one"] for row in controls.values())
    assert committed["literature_map"]["left_degree_three"][
        "status"
    ] == "open within the V82 audit"

    print(
        "V82 primary verification passed: Hall-neighborhood minima equal "
        "transversal girth minus one, minimal minimizers have deficiency one, "
        "and the degree-two/general-hardness boundary matches committed evidence."
    )


if __name__ == "__main__":
    main()
