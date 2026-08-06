#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from canonical_halving import build_results

ROOT = Path(__file__).resolve().parent
STATUS = ROOT.parent / "LAB_STATUS.json"


def version_number(name: str) -> int:
    assert name.startswith("V")
    return int(name[1:])


def verify_status(status: dict) -> None:
    promoted = status["promoted_version"]
    candidate = status["candidate_version"]
    highest = status["highest_directory"]
    if candidate == "V92":
        assert promoted == "V91"
        assert highest == "V92"
        assert status["promotion_state"] == "candidate"
        assert status["next_laboratory_version"] == "V92"
    else:
        assert version_number(promoted) >= 92
        if candidate is None:
            assert highest == promoted
            assert status["promotion_state"] == "promoted"
            assert status["next_laboratory_version"] == f"V{version_number(promoted)+1}"
        else:
            assert version_number(candidate) == version_number(promoted) + 1
            assert highest == candidate


def main() -> None:
    committed = json.loads((ROOT / "RESULTS.json").read_text(encoding="utf-8"))
    assert build_results() == committed

    binary = committed["exhaustive_binary"]
    assert binary["circuits"] == 4096
    assert binary["prefix_count_checks"] == 61440
    assert binary["avoided_outputs"] == 4096
    assert binary["claim_6_8_checks"] == 8448
    assert binary["claim_6_8_mismatches"] == 0
    assert binary["same_as_v75_capacity_policy"] == 2560
    assert binary["different_from_v75_capacity_policy"] == 1536
    assert binary["halving_step_histogram"] == {"1": 512, "2": 2816, "3": 768}

    seeded = committed["seeded_ternary"]
    assert seeded["circuits"] == 512
    assert seeded["prefix_count_checks"] == 2107
    assert seeded["claim_6_8_checks"] == 1595
    assert seeded["claim_6_8_mismatches"] == 0
    assert seeded["maximum_halving_steps"] <= 5

    theorem = committed["theorem_status"]
    assert theorem["component_factorization_exact"]
    assert theorem["canonical_halving_returns_nonimage"]
    assert theorem["all_instance_semantic_completion"]
    assert theorem["v75_exact_prefix_counts_can_implement_policy"]
    assert theorem["hlz_greedy_can_implement_policy"]
    assert not theorem["polynomial_all_instance_runtime"]
    assert not theorem["published_lower_bound_transfer_triggered"]
    assert not theorem["p_vs_np_resolved"]

    implication = json.loads((ROOT / "IMPLICATION.json").read_text(encoding="utf-8"))
    assert implication["laboratory"] == "V92"
    assert implication["classification"] == "infrastructure"
    assert implication["material_advance_rule_met"]
    assert not implication["stop_rule_fired"]
    assert [item["proved"] for item in implication["bridge_lemmas"][:4]] == [True] * 4
    assert [item["proved"] for item in implication["bridge_lemmas"][4:]] == [False] * 3

    v75_source = (ROOT.parent / "v75" / "symbolic_prefix_circuit.py").read_text(encoding="utf-8")
    assert "def prefix_count(" in v75_source
    assert "def find_avoided_output_incremental(" in v75_source
    assert "completion_capacity" in v75_source
    assert "chosen_bit = 0 if count_zero < completion_capacity else 1" in v75_source

    theorem_doc = (ROOT / "CANONICAL_COMPLETION_THEOREM.md").read_text(encoding="utf-8")
    assert "N(p0)+N(p1)=N(p)" in theorem_doc
    assert "n+1" in theorem_doc
    assert "single-valued" in theorem_doc

    calibration = (ROOT / "HLYZ_RUNTIME_CALIBRATION.md").read_text(encoding="utf-8")
    assert "Claim 6.8" in calibration
    assert "Theorem 6.11" in calibration
    assert "O(n * 2^((k-2)n/(k-1)))" in calibration

    status = json.loads(STATUS.read_text(encoding="utf-8"))
    verify_status(status)
    scientific = status["scientific_status"]
    assert scientific["canonical_halving_policy_defined"]
    assert scientific["canonical_halving_component_factorization_exact"]
    assert scientific["canonical_halving_all_instance_semantic_completion"]
    assert scientific["canonical_halving_v75_prefix_count_adapter_proved"]
    assert scientific["canonical_halving_hlz_policy_alignment_proved"]
    assert scientific["v75_capacity_policy_differs_from_canonical_halving"]
    assert not scientific["all_instance_nc0_k_avoid_polynomial_time"]
    assert scientific["hlz_greedy_worst_case_exponential_audited"]
    assert not scientific["v92_published_lower_bound_transfer_triggered"]
    assert not scientific["p_vs_np_resolved"]

    print(
        "V92 verification passed: canonical halving, 4,096 exhaustive binary circuits, "
        "512 ternary controls, exact component factorization, 10,043 Claim 6.8 checks, "
        "and the all-instance semantic/runtime separation."
    )


if __name__ == "__main__":
    main()
