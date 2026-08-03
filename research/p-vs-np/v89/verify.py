#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from oa8_addressing import build_results
from strong4_second_moment import build_strong4_results

ROOT = Path(__file__).resolve().parent
STATUS = ROOT.parent / "LAB_STATUS.json"


def verify_status(status: dict) -> None:
    assert status["highest_directory"] == "V89"
    assert status["promoted_version"] == "V88"
    assert status["candidate_version"] == "V89"
    assert status["promotion_state"] == "candidate"
    assert status["next_laboratory_version"] == "V89"
    budget = status["research_budget"]
    assert budget["eval_h_constructor_front_deadline"] == "V90"
    assert budget["close_front_if_no_material_advance"] is True


def verify_addressing() -> None:
    committed = json.loads(
        (ROOT / "RESULTS.json").read_text(encoding="utf-8")
    )
    generated = build_results()
    assert generated == committed

    assert committed["oa_8_4_2_3"]["every_three_rows_injective"]
    table = {
        row["colors"]: row["maximum_target_rows"]
        for row in committed["uniform_color_code_table"]
    }
    assert table == {
        3: 8,
        4: 8,
        5: 4,
        6: 4,
        7: 2,
        8: 2,
        9: 2,
        10: 2,
    }

    audit = committed["finite_audit"]
    assert audit["families_checked"] == 11
    assert audit["all_basis_colorable"]
    assert audit["all_eight_row_injective"]
    assert not audit["all_primal_four_colorable"]
    assert audit["primal_chromatic_numbers"] == [
        6, 5, 5, 5, 6, 5, 5, 5, 5, 5, 6
    ]

    scientific = committed["scientific_status"]
    assert scientific["eval_h_eight_row_basis_addressing_theorem"]
    assert scientific[
        "target_independent_ternary_addressing_ceiling_eight"
    ]
    assert scientific["v80_and_v87_samples_basis_colorable"]
    assert not scientific["v87_random_model_basis_colorable_whp"]
    assert not scientific["support_only_universal_list_lower_bound_nine"]
    assert not scientific["p_vs_np_resolved"]


def verify_strong_four_reduction() -> None:
    committed = json.loads(
        (ROOT / "STRONG4_RESULTS.json").read_text(encoding="utf-8")
    )
    generated = build_strong4_results()
    assert generated == committed

    first = committed["first_moment"]
    assert first["single_edge_rainbow_probability"] == "3/8"
    assert first["exponential_base_at_density_one"] == 1.5
    assert first["grows_exponentially_at_density_one"]

    exact = committed["overlap_identity"]["exact_census"]
    assert exact["overlap_matrices_checked"] == 2314
    assert exact["identity_mismatches"] == 0

    local = committed["local_stability"]
    assert local["combined_coefficient"] == "-8 + (16/3)c"
    assert (
        local["uniform_overlap_locally_maximal_for_density_below"]
        == "3/2"
    )
    assert local["strict_local_margin_at_density_one"] == "8/3"

    grid = committed["finite_rational_grid"]
    assert grid["overlap_matrices_checked"] == 52637
    assert grid["all_grid_maxima_nonpositive"]

    scientific = committed["scientific_status"]
    assert scientific["strong4_overlap_identity"]
    assert scientific[
        "strong4_second_moment_reduced_to_birkhoff_inequality"
    ]
    assert scientific[
        "strong4_uniform_overlap_locally_stable_through_density_three_halves"
    ]
    assert not scientific["strong4_birkhoff_global_inequality_proved"]
    assert not scientific["support_only_universal_list_lower_bound_nine"]


def main() -> None:
    verify_addressing()
    verify_strong_four_reduction()

    status = json.loads(STATUS.read_text(encoding="utf-8"))
    verify_status(status)
    scientific = status["scientific_status"]
    assert scientific["strong4_overlap_identity"]
    assert scientific[
        "strong4_second_moment_reduced_to_birkhoff_inequality"
    ]
    assert scientific[
        "strong4_uniform_overlap_locally_stable_through_density_three_halves"
    ]
    assert not scientific["strong4_birkhoff_global_inequality_proved"]
    assert not scientific["support_only_universal_list_lower_bound_nine"]

    print(
        "V89 verification passed: eight-row OA/basis addressing, 11 finite "
        "controls, 2,314 exact strong-four overlap identities, 52,637 "
        "rational overlaps, and the exact local-stability reduction."
    )


if __name__ == "__main__":
    main()
