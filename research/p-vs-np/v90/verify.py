#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from local_global_entropy import build_results

ROOT = Path(__file__).resolve().parent
STATUS = ROOT.parent / "LAB_STATUS.json"
POLICY = ROOT.parent / "IMPLICATION_POLICY.md"


def version_number(name: str) -> int:
    assert name.startswith("V")
    return int(name[1:])


def verify_status(status: dict) -> None:
    promoted = status["promoted_version"]
    candidate = status["candidate_version"]
    highest = status["highest_directory"]

    if candidate == "V90":
        assert promoted == "V89"
        assert highest == "V90"
        assert status["promotion_state"] == "candidate"
        assert status["next_laboratory_version"] == "V90"
    else:
        assert version_number(promoted) >= 90
        if candidate is None:
            assert highest == promoted
            assert status["promotion_state"] == "promoted"
            assert status["next_laboratory_version"] == (
                f"V{version_number(promoted) + 1}"
            )
        else:
            assert version_number(candidate) == version_number(promoted) + 1
            assert highest == candidate
            assert status["promotion_state"] == "candidate"
            assert status["next_laboratory_version"] == candidate

    assert status["research_budget"]["eval_h_constructor_front_deadline"] == "V90"
    assert status["research_budget"]["close_front_if_no_material_advance"] is True
    assert status["research_budget"]["eval_h_constructor_front_closed"] is True
    assert status["next_front"] == "algorithmic_method_and_meta_complexity"


def main() -> None:
    committed = json.loads((ROOT / "RESULTS.json").read_text(encoding="utf-8"))
    generated = build_results()
    assert generated == committed

    hoeffding = committed["hoeffding_decomposition"]
    assert hoeffding["ordered_bases"] == 168
    assert hoeffding["basis_probability"] == "24/49"
    assert hoeffding["degree_two_norm_squared"] == "288/2401"
    assert hoeffding["degree_three_norm_squared"] == "312/2401"

    exact = committed["exact_quadratic_identity"]
    assert exact["tangent_dimension"] == 36
    assert exact["bilinear_pairs_checked"] == 1296
    assert exact["mismatches"] == 0
    assert exact["relative_quadratic_coefficient"] == "1/12"

    local = committed["local_certificate"]
    assert local["certified_density"] == "21/20"
    assert local["frobenius_radius"] == "1/5"
    assert local["entropy_lower_coefficient"] == "5/24"
    assert local["energy_upper_coefficient"] == "23/120"
    assert local["strict_margin_coefficient"] == "17/2400"

    gap = committed["remaining_gap"]
    assert not gap["global_entropy_contraction_proved"]
    assert not gap["random_model_basis_colorable_whp"]
    assert not gap["nine_row_constructor_lower_bound"]
    assert not gap["v90_stop_condition_met"]

    implication = json.loads(
        (ROOT / "IMPLICATION.json").read_text(encoding="utf-8")
    )
    assert implication["laboratory"] == "V90"
    assert implication["classification"] == "barrier_and_closure"
    assert not implication["recognized_frontier_implication"]
    assert not implication["material_advance_rule_met"]
    assert implication["stop_rule_fired"]
    assert implication["next_front"].startswith("V91 Williams-style")

    policy = POLICY.read_text(encoding="utf-8")
    assert "Direct implication" in policy
    assert "Natural-proofs checkpoint" in policy
    assert "Algorithmic-method checkpoint" in policy
    assert "barrier_and_closure" in policy

    barrier = (ROOT / "NATURAL_PROOFS_BARRIER.md").read_text(
        encoding="utf-8"
    )
    assert "not automatically a natural proof" in barrier
    assert "certificate-discovery program" in barrier

    context = (ROOT / "V91_CORE_CONTEXT.md").read_text(encoding="utf-8")
    assert "SAT/#SAT transfer" in context
    assert "Missing-String/Range-Avoidance transfer" in context
    assert "2^{O(k^2)}" in context

    status = json.loads(STATUS.read_text(encoding="utf-8"))
    verify_status(status)
    scientific = status["scientific_status"]
    assert scientific["basis7_finite_local_entropy_certificate"]
    assert not scientific["basis7_global_overlap_inequality_proved"]
    assert not scientific["support_only_universal_list_lower_bound_nine"]
    assert scientific["eval_h_constructor_front_closed_after_v90"]
    assert scientific["implication_ratio_policy_active"]
    assert not scientific["p_vs_np_resolved"]

    print(
        "V90 verification passed: exact Hoeffding decomposition, 1,296 "
        "tangent identities, the radius-1/5 entropy certificate at c=21/20, "
        "the implication-ratio policy, and formal Eval_H closure."
    )


if __name__ == "__main__":
    main()
