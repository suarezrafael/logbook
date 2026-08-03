#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from oa8_addressing import build_results

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


def main() -> None:
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

    verify_status(json.loads(STATUS.read_text(encoding="utf-8")))

    print(
        "V89 verification passed: OA(8,4,2,3), exact code table, "
        "11 primal chromatic audits, 11 basis colorings, and the "
        "eight-row target-independent boundary."
    )


if __name__ == "__main__":
    main()
