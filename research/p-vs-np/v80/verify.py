#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from hall_branchwidth import build_results

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main() -> None:
    committed = json.loads((HERE / "RESULTS.json").read_text(encoding="utf-8"))
    assert build_results() == committed

    audit = (HERE / "HIGH_WIDTH_DICHOTOMY_AUDIT.md").read_text(encoding="utf-8")
    readme = (HERE / "README.md").read_text(encoding="utf-8")
    core = (HERE / "V81_CORE_CONTEXT.md").read_text(encoding="utf-8")
    theorem = (HERE / "V80_HALL_BRANCHWIDTH_DICHOTOMY_THEOREM.tex").read_text(encoding="utf-8")
    for phrase in (
        "Hall argument by itself does not close",
        "Candidate-list target",
        "balanced Hall expansion forces width",
        "n/(16e^2)",
        "ECCC TR23-021",
        "Bounded-arithmetic second front",
    ):
        assert phrase in audit
    assert "does not resolve P versus NP" in readme
    assert "deterministic candidate lists" in core
    assert "Balanced Hall expansion forces support width" in theorem
    assert "Local Hall-expansion barrier" in theorem

    status = json.loads((ROOT / "LAB_STATUS.json").read_text(encoding="utf-8"))
    assert status["promoted_version"] == "V79"
    assert status["candidate_version"] == "V80"
    assert status["highest_directory"] == "V80"
    assert status["promotion_state"] == "candidate"
    assert status["infrastructure_frozen"] is True
    assert status["next_laboratory_version"] == "V80"
    assert status["next_laboratory_focus"] == "high-width deterministic candidate-list dichotomy"
    assert status["scientific_status"]["p_vs_np_route_active"] is False

    runner = (ROOT / "verify_all.sh").read_text(encoding="utf-8")
    assert "V80|primary|v80/verify.py|quick|" in runner
    assert "V80|independent|v80/verify_independent.py|quick|" in runner
    assert "V80" in runner.split("FOCUSED_VERSIONS=(", 1)[1].split(")", 1)[0]
    manifest = (ROOT / "LATEX_MODULES.tsv").read_text(encoding="utf-8")
    assert "v80\tv80/V80_HALL_BRANCHWIDTH_DICHOTOMY_THEOREM.tex" in manifest

    nine = committed["examples"]["nine_variables"]
    assert nine["support_branchwidth"] == 6
    assert nine["minimum_hall_deficient_gate_count"] == 9
    assert nine["minimum_hall_neighborhood_size"] == 8
    assert committed["algorithmic_boundary"]["counting_alone_implies_deterministic_FP_NP"] is False
    assert committed["probabilistic_barrier"]["bad_event_sum_upper_bound"] == [8, 49]

    print(
        "V80 primary verification passed: Hall counting is separated from deterministic "
        "FP^NP construction; the cut identity, local-expansion barrier, and exact finite "
        "branchwidth audits all match committed evidence."
    )


if __name__ == "__main__":
    main()
