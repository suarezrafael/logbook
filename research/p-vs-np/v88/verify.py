#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from collision_normal_form import build_results
from three_row_barrier import build_three_row_results

ROOT = Path(__file__).resolve().parent
STATUS = ROOT.parent / "LAB_STATUS.json"


def generated_results() -> dict:
    generated = build_results()
    barrier = build_three_row_results()
    generated["three_row_barrier"] = barrier
    generated["scientific_status"][
        "eval_h_three_row_requires_fifteen_active_outputs"
    ] = True
    generated["scientific_status"][
        "eval_h_three_row_target_stretch_n5_n9_coverable"
    ] = True
    generated["theorems"]["three_row_fourteen_output_barrier"] = barrier[
        "theorem"
    ]
    return generated


def main() -> None:
    committed = json.loads((ROOT / "RESULTS.json").read_text(encoding="utf-8"))
    generated = generated_results()
    assert generated == committed

    audit = committed["finite_audit"]
    assert audit["simple_ternary_support_families"] == 15
    assert audit["target_instances"] == 7264
    assert audit["equivalence_mismatches"] == 0
    assert audit["three_row_coloring_mismatches"] == 0
    assert audit["pair_constructor_failures"] == 0
    assert audit["uncovered_targets"] == 0

    barrier = committed["three_row_barrier"]
    assert barrier["minimum_active_outputs_for_three_row_obstruction"] == 15
    assert barrier["pair_formula_census"]["formula_mismatches"] == 0
    assert (
        barrier["pair_formula_census"][
            "labeled_distinct_support_pairs_checked"
        ]
        == 1710
    )
    assert barrier["fano_labeling_census"]["labelings"] == 2187
    assert barrier["fano_labeling_census"]["uncoverable_labelings"] == 0
    for certificate in barrier["moment_certificates"]:
        assert (
            certificate["pair_intersection_lower_bound"]
            > certificate["pair_intersection_upper_bound_if_cover"]
        )

    status = json.loads(STATUS.read_text(encoding="utf-8"))
    assert status["promoted_version"] == "V87"
    assert status["candidate_version"] == "V88"
    assert status["highest_directory"] == "V88"
    assert status["promotion_state"] == "candidate"
    scientific = status["scientific_status"]
    assert scientific["eval_h_collision_normal_form"]
    assert scientific["eval_h_pairwise_obstruction_impossible"]
    assert scientific["eval_h_three_row_labeled_hypergraph_reduction"]
    assert scientific["eval_h_three_row_requires_fifteen_active_outputs"]
    assert scientific["eval_h_three_row_target_stretch_n5_n9_coverable"]
    assert not scientific["constructive_eval_h_list"]
    assert not scientific["p_vs_np_resolved"]

    print(
        "V88 verification passed: 7,264 exact target instances, 1,710 pair "
        "intersection checks, all 2,187 Fano labelings, and the fourteen-output "
        "three-row contradiction."
    )


if __name__ == "__main__":
    main()
