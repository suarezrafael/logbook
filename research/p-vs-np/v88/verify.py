#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from collision_normal_form import build_results
from property_b_boundary import build_property_b_results
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


def verify_status(status: dict) -> None:
    candidate = status["candidate_version"]
    promoted = status["promoted_version"]
    highest = status["highest_directory"]

    if candidate == "V88":
        assert promoted == "V87"
        assert highest == "V88"
        assert status["promotion_state"] == "candidate"
        assert status["next_laboratory_version"] == "V88"
        return

    assert promoted == "V88"
    if candidate is None:
        assert highest == "V88"
        assert status["promotion_state"] == "promoted"
        assert status["next_laboratory_version"] == "V89"
        return

    assert candidate.startswith("V")
    assert int(candidate[1:]) >= 89
    assert highest == candidate
    assert status["promotion_state"] == "candidate"
    assert status["next_laboratory_version"] == candidate


def main() -> None:
    committed = json.loads(
        (ROOT / "RESULTS.json").read_text(encoding="utf-8")
    )
    generated = generated_results()
    assert generated == committed

    property_b_committed = json.loads(
        (ROOT / "PROPERTY_B_RESULTS.json").read_text(encoding="utf-8")
    )
    property_b_generated = build_property_b_results()
    assert property_b_generated == property_b_committed

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

    property_b = property_b_committed
    assert property_b["constructor_lower_bound"]["minimum_universal_rows"] == 4
    assert not property_b["constructor_lower_bound"][
        "support_only_universal_triple_exists"
    ]
    assert property_b["finite_audit"]["total_support_families_checked"] == 11
    assert property_b["finite_audit"]["v80_all_two_colorable"]
    assert property_b["finite_audit"]["v87_samples_all_two_colorable"]
    density = property_b["density_calibration"]
    assert density["coupling_density"] < density[
        "random_3_uniform_two_colorability_lower_density"
    ]

    status = json.loads(STATUS.read_text(encoding="utf-8"))
    verify_status(status)
    scientific = status["scientific_status"]
    assert scientific["eval_h_collision_normal_form"]
    assert scientific["eval_h_pairwise_obstruction_impossible"]
    assert scientific["eval_h_three_row_labeled_hypergraph_reduction"]
    assert scientific["eval_h_three_row_requires_fifteen_active_outputs"]
    assert scientific["eval_h_three_row_target_stretch_n5_n9_coverable"]
    assert scientific["v87_random_model_two_colorable_whp"]
    assert scientific["same_family_three_certificates_plus_property_b_exists"]
    assert scientific["constructor_model_lower_bound"]
    assert not scientific["support_only_universal_triple_exists"]
    assert not scientific["constructive_eval_h_list"]
    assert not scientific["p_vs_np_resolved"]

    print(
        "V88 verification passed: collision normal form, fourteen-output barrier, "
        "2,187 Fano labelings, 11 Property-B controls, and the universal "
        "three-row constructor lower bound."
    )


if __name__ == "__main__":
    main()
