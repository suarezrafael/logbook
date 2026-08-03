#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from linear_branchwidth import build_results

HERE = Path(__file__).resolve().parent


def main() -> None:
    committed = json.loads((HERE / "RESULTS.json").read_text(encoding="utf-8"))
    recomputed = build_results()
    assert recomputed == committed

    transfer = committed["transfer_census"]
    assert transfer["families_checked"] == 837
    assert transfer["violations"] == 0
    assert transfer["by_gate_count"] == {
        "2": 45,
        "3": 120,
        "4": 210,
        "5": 252,
        "6": 210,
    }

    pair_shadow = committed["pair_shadow_uniformity"]
    assert pair_shadow["uniform"] is True
    assert pair_shadow["occurrences_per_pair"] == [4]

    v80 = committed["v80_balanced_census"]
    assert [v80[name]["minimum_balanced_lambda"] for name in sorted(v80)] == [4, 5, 5]

    random_rows = committed["random_balanced_census"]
    assert len(random_rows) == 8
    assert sum(row["balanced_subsets_checked"] for row in random_rows) == 17_601_500
    assert min(row["minimum_balanced_lambda_over_n"] for row in random_rows) == 0.3125

    mcdiarmid = committed["mcdiarmid_audit"]
    assert mcdiarmid["entropy_exceeds_best_tail_rate"] is True
    assert mcdiarmid["balanced_subset_entropy_rate_per_gate"] > 0.63
    assert mcdiarmid["optimistic_maximum_mcdiarmid_tail_rate_per_n"] < 0.056
    assert abs(
        mcdiarmid["asymptotic_expected_fixed_cut_lambda_over_n"]
        - mcdiarmid["incorrect_subtract_n_approximation"]
        - mcdiarmid["missing_unused_vertex_term"]
    ) < 1e-12

    status = committed["scientific_status"]
    assert status["same_family_defeats_hall_syndrome_and_width_certificates"] is True
    assert status["explicit_deterministic_three_certificate_family"] is False
    assert status["unrestricted_NC0_3_avoid_solved"] is False
    assert status["p_vs_np_resolved"] is False

    print(
        "V87 primary verification passed: 837 transfer cases, exact pair-shadow "
        "uniformity, 17,601,500 balanced-cut checks, the McDiarmid no-go, and "
        "the linear-branchwidth three-certificate theorem."
    )


if __name__ == "__main__":
    main()
