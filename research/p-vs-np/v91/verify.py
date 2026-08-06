#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from reproduction import build_results

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

    if candidate == "V91":
        assert promoted == "V90"
        assert highest == "V91"
        assert status["promotion_state"] == "candidate"
        assert status["next_laboratory_version"] == "V91"
    else:
        assert version_number(promoted) >= 91
        if candidate is None:
            assert highest == promoted
            assert status["promotion_state"] == "promoted"
            assert status["next_laboratory_version"] == f"V{version_number(promoted) + 1}"
        else:
            assert version_number(candidate) == version_number(promoted) + 1
            assert highest == candidate
            assert status["promotion_state"] == "candidate"
            assert status["next_laboratory_version"] == candidate

    assert status["research_budget"]["eval_h_constructor_front_closed"] is True
    assert status["next_front"] == "algorithmic_method_and_meta_complexity"


def main() -> None:
    reproduction = json.loads(
        (ROOT / "REPRODUCTION_RESULTS.json").read_text(encoding="utf-8")
    )
    assert build_results() == reproduction
    assert reproduction["korten_ggm"]["exhaustive_n1"]["maps_checked"] == 16
    assert reproduction["korten_ggm"]["deterministic_sample_n2"]["maps_checked"] == 64
    assert reproduction["missing_string"]["proper_subsets_checked"] == 65808
    assert "not the full CHR/Li" in reproduction["reproduction_scope"]

    results = json.loads((ROOT / "RESULTS.json").read_text(encoding="utf-8"))
    assert results["laboratory"] == "V91"
    assert results["classification"] == "reproduction_calibration_and_barrier"
    assert results["reproduction"] == reproduction

    li = results["theorem_calibration"]["Li_2023"]
    assert li["range_avoidance_lengths"] == "all"
    assert "depth-3" in li["missing_string_consequence"]
    assert "already closed" in li["status_for_v91"]

    vw = results["theorem_calibration"]["Vyas_Williams_TR24_113"]
    assert "July 2024" in vw["source_gate"]
    assert vw["theorem_1_10"].startswith("false")

    verdict = results["engine_verdict"]
    assert not verdict["all_instance_coverage"]
    assert not verdict["single_valued_search_guarantee"]
    assert verdict["polynomial_time_regime"] == "support branchwidth O(sqrt(log m)) only"
    assert not verdict["published_transfer_triggered"]

    implication = json.loads(
        (ROOT / "IMPLICATION.json").read_text(encoding="utf-8")
    )
    assert implication["laboratory"] == "V91"
    assert implication["classification"] == "barrier_and_closure"
    assert not implication["recognized_frontier_implication"]
    assert not implication["material_advance_rule_met"]
    assert implication["stop_rule_fired"]
    assert implication["bridge_lemmas"][0]["proved"]
    assert all(
        not item["proved"] for item in implication["bridge_lemmas"][1:]
    )

    calibration = (ROOT / "THEOREM_CALIBRATION.md").read_text(encoding="utf-8")
    assert "Theorem 1.10" in calibration
    assert "forbidden as a premise" in calibration
    assert "depth-3 AC0" in calibration
    assert "all-instance coverage" in calibration

    barrier = (ROOT / "BARRIER_AUDIT.md").read_text(encoding="utf-8")
    assert "algebrization" in barrier.lower()
    assert "nonalgebrizing" in barrier.lower()
    assert "No implication may cite" in barrier

    engine = (ROOT / "ENGINE_COMPATIBILITY.md").read_text(encoding="utf-8")
    assert "C_low" in engine
    assert "high-width branch" in engine
    assert "cannot be instantiated" in engine

    next_context = (ROOT / "V92_CORE_CONTEXT.md").read_text(encoding="utf-8")
    assert "all-instance completion gate" in next_context
    assert "high width" in next_context
    assert "theorem-native canonical output" in next_context

    policy = POLICY.read_text(encoding="utf-8")
    assert "Algorithmic-method checkpoint" in policy
    assert "barrier_and_closure" in policy

    status = json.loads(STATUS.read_text(encoding="utf-8"))
    verify_status(status)
    scientific = status["scientific_status"]
    assert scientific["chr_li_range_avoidance_chain_calibrated"]
    assert scientific["korten_ggm_decoding_kernel_reproduced_finitely"]
    assert not scientific["full_chr_li_single_valued_algorithm_reproduced"]
    assert scientific["missing_string_depth3_transfer_target_closed_by_li"]
    assert scientific["vyas_williams_tr24_113_erratum_enforced"]
    assert not scientific["vyas_williams_conference_theorem_1_10_usable"]
    assert scientific["missing_string_algebrization_barrier_audited"]
    assert not scientific["inherited_width_engine_triggers_published_transfer"]
    assert not scientific["v91_new_circuit_lower_bound"]
    assert not scientific["p_vs_np_resolved"]

    print(
        "V91 verification passed: 80 finite Korten/GGM maps, 65,808 "
        "Missing-String instances, post-Li theorem calibration, the TR24-113 "
        "erratum gate, the algebrization audit, and the width-engine no-go."
    )


if __name__ == "__main__":
    main()
