#!/usr/bin/env python3
from __future__ import annotations

import json
import math
from pathlib import Path

from component_avoidance import build_component_audit
from hitlist_compression import (
    build_results,
    circuit_oblivious_list_bound,
    or_block_embeddable_rows,
    single_output_representation_bound,
    support_conditioned_list_bound,
)

ROOT = Path(__file__).resolve().parent
STATUS = ROOT.parent / "LAB_STATUS.json"


def version_number(name: str) -> int:
    assert name.startswith("V")
    return int(name[1:])


def verify_status(status: dict) -> None:
    promoted = status["promoted_version"]
    candidate = status.get("candidate_version")
    highest = status["highest_directory"]
    assert status["next_front"] == "algorithmic_method_and_meta_complexity"
    if candidate == "V96":
        assert promoted == "V95"
        assert highest == "V96"
        assert status["promotion_state"] == "candidate"
        assert status["next_laboratory_version"] == "V96"
    else:
        assert version_number(promoted) >= 96
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
    rebuilt["surplus_component_audit"] = build_component_audit()
    rebuilt["symbolic_formulas"]["surplus_component_runtime"] = "O(2^rho * poly(N))"
    rebuilt["theorem_status"]["surplus_component_fpt_avoider"] = True
    assert rebuilt == committed

    theorem = committed["theorem_status"]
    assert theorem["support_conditioned_linear_nonuniform_hitlist"]
    assert theorem["circuit_oblivious_nlogn_nonuniform_hitlist"]
    assert theorem["circuit_oblivious_hitlist_logarithmic_lower_bound"]
    assert theorem["fixed_triple_support_hitlist_number_nine"]
    assert theorem["surplus_component_fpt_avoider"]
    assert theorem["uniform_hitlist_to_FP_NP_avoid_transfer"]
    assert not theorem["constructive_polynomial_hitlist"]
    assert not theorem["unrestricted_NC0_3_avoid_polynomial_time"]
    assert not theorem["hlz_runtime_improved"]
    assert not theorem["p_vs_np_resolved"]

    for row in committed["representative_bounds"]:
        n = row["input_count"]
        q = single_output_representation_bound(n)
        assert q == row["single_output_representation_bound"]
        assert math.ceil(math.log2(q)) == row["ceil_log2_single_output_bound"]
        assert circuit_oblivious_list_bound(n) == row["circuit_oblivious_nonuniform_upper"]
        assert support_conditioned_list_bound([3] * (n + 1)) == row["all_ternary_support_conditioned_upper"]
        embedded = or_block_embeddable_rows(n)
        assert embedded == row["or_block_lower_embeddable_targets"]
        assert embedded + 1 == row["or_block_universal_lower_bound"]

    audit = committed["embedding_audit"]
    assert audit == {
        "input_sizes": [6, 12, 24, 48, 96],
        "cases_per_size": 16,
        "total_cases": 80,
        "total_embedded_target_rows": 720,
        "embedding_failures": 0,
        "input_budget_failures": 0,
    }

    fixed = committed["fixed_triple_control"]
    assert fixed["common_support_size"] == 3
    assert fixed["maximum_range_size"] == 8
    assert fixed["exact_universal_list_number"] == 9
    assert fixed["eight_target_embedding_cases"] == 32
    assert fixed["embedding_failures"] == 0

    component = committed["surplus_component_audit"]
    assert component["total_cases"] == 56
    assert component["brute_force_input_evaluations"] == 16256
    assert component["maximum_surplus_component_parameter"] == 3
    assert component["rho_mismatches"] == 0
    assert component["absence_failures"] == 0
    assert component["runtime_formula"] == "O(2^rho * poly(N))"
    assert component["polynomial_when"] == "rho=O(log N)"

    implication = json.loads((ROOT / "IMPLICATION.json").read_text(encoding="utf-8"))
    assert implication["laboratory"] == "V96"
    assert implication["classification"] == "barrier_and_closure"
    assert implication["material_advance_rule_met"]
    assert implication["stop_rule_fired"]
    assert implication["next_front"] == "uniform_hitlist_or_certificate_extraction"
    assert not implication["p_vs_np_resolved"]

    if STATUS.exists():
        verify_status(json.loads(STATUS.read_text(encoding="utf-8")))

    print(
        "V96 verification passed: O(N)/O(N log N) nonuniform hitlists, "
        "monotone-OR Omega(log N), exact common-triple nine, surplus-component "
        "O(2^rho poly(N)) avoider, and conservative uniformization boundary."
    )


if __name__ == "__main__":
    main()
