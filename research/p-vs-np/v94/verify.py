#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from child_count_comparison import build_results

ROOT = Path(__file__).resolve().parent
STATUS = ROOT.parent / "LAB_STATUS.json"


def version_number(name: str) -> int:
    assert name.startswith("V")
    return int(name[1:])


def verify_status(status: dict) -> None:
    promoted = status["promoted_version"]
    candidate = status.get("candidate_version")
    highest = status["highest_directory"]
    if candidate == "V94":
        assert promoted == "V93"
        assert highest == "V94"
        assert status["promotion_state"] == "candidate"
        assert status["next_laboratory_version"] == "V94"
    else:
        assert version_number(promoted) >= 94
        if candidate is None:
            assert highest == promoted
            assert status["promotion_state"] == "promoted"
            assert status["next_laboratory_version"] == f"V{version_number(promoted)+1}"
        else:
            assert version_number(candidate) == version_number(promoted) + 1
            assert highest == candidate


def main() -> None:
    committed = json.loads((ROOT / "RESULTS.json").read_text(encoding="utf-8"))
    rebuilt = build_results()
    assert rebuilt == committed

    language = committed["fixed_gate_language"]
    assert language == {
        "maximum_arity": 3,
        "definition_variants": 4,
        "conditional_clause_variants": 4,
        "projection_variants": 1,
        "total_gate_types": 9,
    }

    reduction = committed["arbitrary_prefix_reduction_audit"]
    assert reduction["signed_three_literal_clauses"] == 64
    assert reduction["ordered_single_clause_pairs"] == 4096
    assert reduction["strict_source_count_pairs"] == 2208
    assert reduction["equal_source_count_pairs"] == 1888
    assert reduction["count_mismatches"] == 0
    assert reduction["stretch_one_mismatches"] == 0

    separation = committed["canonical_separation_control"]
    assert separation["def_truth_table_ones"] == 4
    assert separation["def_truth_table_zeros"] == 4
    assert separation["v92_first_bit_on_def_first_order"] == 0
    assert separation["hardness_prefix_first_bit"] == 1
    assert not separation["reduction_prefix_is_canonical_in_this_order"]

    affine = committed["affine_comparator_audit"]
    assert affine["affine_functions"] == 16
    assert affine["affine_circuits"] == 65536
    assert affine["child_decisions"] == 262144
    assert affine["child_count_mismatches"] == 0
    assert affine["incremental_output_mismatches"] == 0
    assert affine["canonical_outputs_in_range"] == 0

    theorem = committed["theorem_status"]
    assert theorem["arbitrary_prefix_comparison_in_PP"]
    assert theorem["arbitrary_prefix_comparison_PP_hard_via_exact_scaled_reduction"]
    assert theorem["arbitrary_prefix_comparison_PP_complete"]
    assert theorem["stretch_one_preserved"]
    assert theorem["affine_all_prefix_comparison_in_P"]
    assert theorem["affine_canonical_avoider_in_P"]
    assert not theorem["canonical_prefix_PP_hardness_proved"]
    assert not theorem["unrestricted_NC0_3_avoid_polynomial_time"]
    assert not theorem["hlz_runtime_improved"]
    assert not theorem["p_vs_np_resolved"]

    implication = json.loads((ROOT / "IMPLICATION.json").read_text(encoding="utf-8"))
    assert implication["laboratory"] == "V94"
    assert implication["classification"] == "barrier"
    assert implication["material_advance_rule_met"]
    assert implication["stop_rule_fired"]
    assert [item["proved"] for item in implication["bridge_lemmas"][:6]] == [True] * 6
    assert [item["proved"] for item in implication["bridge_lemmas"][6:]] == [False, False]
    assert not implication["p_vs_np_resolved"]

    if STATUS.exists():
        verify_status(json.loads(STATUS.read_text(encoding="utf-8")))

    print(
        "V94 verification passed: exact stretch-one arbitrary-prefix compiler, "
        "4096 pair audit, PP-comparison theorem contract, canonical-prefix "
        "separation, and 65536-circuit affine comparator audit."
    )


if __name__ == "__main__":
    main()
