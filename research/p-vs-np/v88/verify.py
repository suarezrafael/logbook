#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from collision_normal_form import build_results

ROOT = Path(__file__).resolve().parent
STATUS = ROOT.parent / "LAB_STATUS.json"


def main() -> None:
    committed = json.loads((ROOT / "RESULTS.json").read_text(encoding="utf-8"))
    generated = build_results()
    assert generated == committed

    audit = committed["finite_audit"]
    assert audit["simple_ternary_support_families"] == 15
    assert audit["target_instances"] == 7264
    assert audit["equivalence_mismatches"] == 0
    assert audit["three_row_coloring_mismatches"] == 0
    assert audit["pair_constructor_failures"] == 0
    assert audit["uncovered_targets"] == 0

    status = json.loads(STATUS.read_text(encoding="utf-8"))
    assert status["promoted_version"] == "V87"
    assert status["candidate_version"] == "V88"
    assert status["highest_directory"] == "V88"
    assert status["promotion_state"] == "candidate"
    scientific = status["scientific_status"]
    assert scientific["eval_h_collision_normal_form"]
    assert scientific["eval_h_pairwise_obstruction_impossible"]
    assert scientific["eval_h_three_row_labeled_hypergraph_reduction"]
    assert not scientific["constructive_eval_h_list"]
    assert not scientific["p_vs_np_resolved"]

    print(
        "V88 verification passed: 7,264 exact target instances, collision/direct "
        "equivalence, universal pair constructor, and three-row coloring reduction."
    )


if __name__ == "__main__":
    main()
