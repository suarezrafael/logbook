#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from canonical_next_bit import build_results

ROOT = Path(__file__).resolve().parent
STATUS = ROOT.parent / "LAB_STATUS.json"


def version_number(name: str) -> int:
    assert name.startswith("V")
    return int(name[1:])


def verify_status(status: dict) -> None:
    promoted = status["promoted_version"]
    candidate = status.get("candidate_version")
    highest = status["highest_directory"]
    if candidate == "V95":
        assert promoted == "V94"
        assert highest == "V95"
        assert status["promotion_state"] == "candidate"
        assert status["next_laboratory_version"] == "V95"
    else:
        assert version_number(promoted) >= 95
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
    assert language["total_gate_types"] == 7
    assert language["maximum_locality"] == 3
    assert language["signed_or_balanced_definition_variants"] == 4
    assert language["and_balanced_definition_variants"] == 1

    representative = committed["representative_case"]
    assert representative["source_counts"] == [2, 3]
    assert representative["input_count"] == 7
    assert representative["output_count"] == 8
    assert representative["prefix_length"] == 4
    assert representative["canonical_output"] == [0, 0, 0, 0, 0, 1, 0, 0]
    assert representative["loader_child_counts"] == [
        [64, 64], [32, 32], [16, 16], [8, 8]
    ]
    assert representative["comparison_child_counts"] == [3, 5]
    assert representative["comparison_child_counts"] == representative["expected_comparison_child_counts"]
    assert representative["comparison_bit"] == representative["expected_comparison_bit"] == 0
    assert representative["final_fiber_size"] == 0
    assert not representative["canonical_output_in_range"]

    structural = committed["structural_size_audit"]
    assert structural["parameter_cases"] == 100
    assert structural["size_or_stretch_mismatches"] == 0
    assert structural["maximum_locality"] == 3

    audit = committed["exhaustive_one_clause_audit"]
    assert audit["signed_three_literal_clauses"] == 64
    assert audit["ordered_clause_pairs"] == 4096
    assert audit["equal_source_count_pairs"] == 1888
    assert audit["strict_source_count_pairs"] == 2208
    assert audit["canonical_zero_comparisons"] == 2992
    assert audit["canonical_one_comparisons"] == 1104
    assert audit["balanced_loader_decisions"] == 16384
    assert audit["loader_balance_failures"] == 0
    assert audit["loader_prefix_failures"] == 0
    assert audit["final_child_count_mismatches"] == 0
    assert audit["comparison_bit_mismatches"] == 0
    assert audit["canonical_outputs_in_range"] == 0
    assert audit["stretch_one_mismatches"] == 0

    theorem = committed["theorem_status"]
    assert theorem["balanced_definition_exact_tie_lemma"]
    assert theorem["balanced_loader_composable"]
    assert theorem["canonical_prefix_all_zero"]
    assert theorem["canonical_next_bit_PP_hard"]
    assert theorem["exact_canonical_word_PP_hard"]
    assert not theorem["arbitrary_avoidance_PP_hard"]
    assert not theorem["unrestricted_NC0_3_avoid_polynomial_time"]
    assert not theorem["hlz_runtime_improved"]
    assert not theorem["p_vs_np_resolved"]

    implication = json.loads((ROOT / "IMPLICATION.json").read_text(encoding="utf-8"))
    assert implication["laboratory"] == "V95"
    assert implication["classification"] == "barrier_and_closure"
    assert implication["material_advance_rule_met"]
    assert implication["stop_rule_fired"]
    assert [item["proved"] for item in implication["bridge_lemmas"][:6]] == [True] * 6
    assert [item["proved"] for item in implication["bridge_lemmas"][6:]] == [False, False]
    assert implication["next_front"] == "comparison_free_range_avoidance"
    assert not implication["p_vs_np_resolved"]

    if STATUS.exists():
        verify_status(json.loads(STATUS.read_text(encoding="utf-8")))

    print(
        "V95 verification passed: composable balanced canonical loader, "
        "4096 genuine-canonical comparison instances, 16384 exact tie steps, "
        "PP-hard next-bit contract, and comparison-free V96 handoff."
    )


if __name__ == "__main__":
    main()
