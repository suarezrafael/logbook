#!/usr/bin/env python3
from __future__ import annotations

import json
import math
from pathlib import Path

from peeling_kernel import build_results

ROOT = Path(__file__).resolve().parent
STATUS = ROOT.parent / "LAB_STATUS.json"


def version_number(name: str) -> int:
    assert name.startswith("V")
    return int(name[1:])


def verify_status(status: dict) -> None:
    assert status["next_front"] == "algorithmic_method_and_meta_complexity"
    promoted = status["promoted_version"]
    candidate = status.get("candidate_version")
    if candidate == "V97":
        assert promoted == "V96"
        assert status["highest_directory"] == "V97"
        assert status["promotion_state"] == "candidate"
        assert status["next_laboratory_version"] == "V97"
    else:
        assert version_number(promoted) >= 97
        if candidate is None:
            assert status["highest_directory"] == promoted
            assert status["promotion_state"] == "promoted"
            assert status["next_laboratory_version"] == f"V{version_number(promoted)+1}"


def main() -> None:
    committed = json.loads((ROOT / "RESULTS.json").read_text(encoding="utf-8"))
    rebuilt = build_results()
    assert rebuilt == committed

    theorem = committed["theorem_status"]
    for key in (
        "essential_support_normalization",
        "safe_leaf_input_output_pair_rule",
        "safe_unary_output_forcing_rule",
        "peeling_kernel_comparison_free_avoider",
        "lambda_never_exceeds_rho",
        "strict_extension_of_v96_parameter",
        "polynomial_when_lambda_logarithmic",
        "nonmonotone_ternary_strict_family",
    ):
        assert theorem[key]
    assert not theorem["unrestricted_NC0_3_avoid_polynomial_time"]
    assert not theorem["hlz_worst_case_runtime_improved"]
    assert not theorem["p_vs_np_resolved"]

    audit = committed["random_small_audit"]
    assert audit["total_cases"] == 240
    assert audit["absence_failures"] == 0
    assert audit["lambda_gt_rho_failures"] == 0
    assert audit["brute_force_input_evaluations"] == 76384

    unary = committed["unary_cascade_audit"]
    assert unary == {
        "total_cases": 32,
        "total_unary_forcing_steps": 128,
        "absence_failures": 0,
    }

    rows = committed["strict_extension_family"]["rows"]
    assert [row["input_count"] for row in rows] == [8, 16, 32, 64, 128]
    for row in rows:
        n = row["input_count"]
        assert row["output_count"] == n + 1
        assert row["rho"] == n
        assert row["lambda"] == math.ceil(math.log2(n))
        assert row["locality"] == 3
        assert row["gate_family"] == "ternary parity"
    assert committed["strict_extension_family"]["absence_failures"] == 0

    implication = json.loads((ROOT / "IMPLICATION.json").read_text(encoding="utf-8"))
    assert implication["laboratory"] == "V97"
    assert implication["classification"] == "frontier_progress"
    assert implication["material_advance_rule_met"]
    assert implication["stop_rule_fired"]
    assert [item["proved"] for item in implication["bridge_lemmas"][:7]] == [True] * 7
    assert [item["proved"] for item in implication["bridge_lemmas"][7:]] == [False, False]
    assert implication["next_front"] == "irreducible_nonmonotone_turan_certificates"
    assert not implication["p_vs_np_resolved"]

    literature = committed["literature_calibration"]
    assert literature["kuntewar_sarma_2025_monotone_nc03_m_gt_n_in_P"]
    assert not literature["strict_family_is_monotone"]
    assert not literature["strict_family_is_nc02"]
    assert literature["v84_small_hall_witness_FP_NP_preprocessor_preexists"]

    if STATUS.exists():
        verify_status(json.loads(STATUS.read_text(encoding="utf-8")))

    print(
        "V97 verification passed: safe leaf/unary peeling, O(2^lambda poly(N)) "
        "avoidance, lambda<=rho, strict nonmonotone rho=N/lambda=log N family, "
        "and conservative literature boundary."
    )


if __name__ == "__main__":
    main()
