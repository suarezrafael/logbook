#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from build_results import build_results

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def version_number(value: str) -> int:
    assert value.startswith("V") and value[1:].isdigit()
    return int(value[1:])


def main() -> None:
    committed = json.loads((HERE / "RESULTS.json").read_text(encoding="utf-8"))
    assert build_results() == committed

    readme = (HERE / "README.md").read_text(encoding="utf-8")
    proof = (HERE / "GIRTH_EXTRACTION_AND_HALL_PROMISE_REDUCTION.md").read_text(
        encoding="utf-8"
    )
    theorem = (HERE / "V84_FP_NP_EXTRACTION_THEOREM.tex").read_text(
        encoding="utf-8"
    )
    core = (HERE / "V85_CORE_CONTEXT.md").read_text(encoding="utf-8")

    for phrase in (
        "canonical deletion theorem",
        "short-circuit avoidance",
        "hall-expander promise reduction",
        "not a many-one reduction",
        "does not solve unrestricted",
    ):
        assert phrase.lower() in readme.lower()
    for phrase in (
        "Exact girth",
        "Canonical shortest circuit by deletion",
        "Exact Hall witness",
        "Local enumeration and lift",
        "Parameterized dichotomy",
    ):
        assert phrase.lower() in proof.lower()
    assert "Exact extraction" in theorem
    assert "Local avoidance or Hall expansion" in theorem
    assert "logarithmic Hall-expander branch" in core

    census = committed["exhaustive_extraction_census"]
    assert census["presentations_checked"] == 832
    assert census["subset_states_checked"] == 7872
    assert census["oracle_queries_simulated"] == 3961
    assert census["canonical_circuits_checked"] == 585
    assert census["hall_witnesses_checked"] == 585
    local = committed["local_avoidance_census"]
    assert local["truth_table_combinations"] == 272
    assert local["avoided_outputs_verified"] == 272
    assert [row["girth"] for row in committed["long_circuit_controls"]] == [
        4,
        6,
        8,
        10,
    ]

    theorem_data = committed["theorem"]
    assert theorem_data["degree_three_promise_preserved"] is True
    assert "ceil(log2(m))" in theorem_data["exact_girth_queries"]
    assert theorem_data["canonical_circuit_queries"] == "at most m deletion queries"
    assert "not a many-one solver" in theorem_data["reduction_type"]

    status = json.loads((ROOT / "LAB_STATUS.json").read_text(encoding="utf-8"))
    promoted = status["promoted_version"]
    candidate = status.get("candidate_version")
    reached = version_number(promoted) >= 84 or (
        candidate is not None and version_number(candidate) >= 84
    )
    assert reached
    if candidate is None:
        assert status["highest_directory"] == promoted
        assert status["promotion_state"] == "promoted"
    else:
        assert version_number(candidate) == version_number(promoted) + 1
        assert status["highest_directory"] == candidate
        assert status["promotion_state"] == "candidate"
    scientific = status["scientific_status"]
    assert scientific["exact_degree_three_girth_in_FP_NP"] is True
    assert scientific["canonical_shortest_circuit_in_FP_NP"] is True
    assert scientific["logarithmic_girth_NC0_3_avoid_in_FP_NP"] is True
    assert scientific["logarithmic_hall_expander_promise_reduction"] is True
    assert scientific["unrestricted_NC0_3_avoid_solved"] is False
    assert scientific["deterministic_FP_NP_target_solved"] is False
    assert scientific["p_vs_np_resolved"] is False

    runner = (ROOT / "verify_all.sh").read_text(encoding="utf-8")
    assert "V84|primary|v84/verify.py|quick|" in runner
    assert "V84|independent|v84/verify_independent.py|quick|" in runner
    assert "V84" in runner.split("FOCUSED_VERSIONS=(", 1)[1].split(")", 1)[0]
    manifest = (ROOT / "LATEX_MODULES.tsv").read_text(encoding="utf-8")
    assert "v84\tv84/V84_FP_NP_EXTRACTION_THEOREM.tex" in manifest

    print(
        "V84 primary verification passed: exact FP^NP girth/circuit/Hall "
        "extraction, local avoidance, and the Hall-expander promise dichotomy "
        "match the committed evidence."
    )


if __name__ == "__main__":
    main()
