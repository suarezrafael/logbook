#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from unate_frontier import build_results

ROOT = Path(__file__).resolve().parent


def main() -> None:
    committed = json.loads((ROOT / "RESULTS.json").read_text(encoding="utf-8"))
    rebuilt = build_results()
    assert rebuilt == committed

    theorem = committed["theorem_status"]
    for key in (
        "essential_unate_partition_three_npn_orbits",
        "singleton_core_positive_surplus_avoidance_in_P",
        "singleton_core_conflict_constructor",
        "singleton_core_conflict_free_switches_to_monotone_AND",
        "strict_unbalanced_singleton_lambda_n_family",
        "signed_majority_simple_x_cycle_rank_two",
        "signed_majority_balanced_class_exactly_two_missing",
        "signed_majority_three_nonzero_classes_surjective",
        "signed_majority_simple_x_local_certificate_closed_on_unbalanced_classes",
    ):
        assert theorem[key]
    assert not theorem["middle_unate_orbit_solved"]
    assert not theorem["all_unate_nc03_avoid_polynomial_time"]
    assert not theorem["unrestricted_nc03_avoid_polynomial_time"]
    assert not theorem["hlz_worst_case_runtime_improved"]
    assert not theorem["p_vs_np_resolved"]

    partition = committed["ternary_unate_partition"]
    assert partition["all_masks"] == 256
    assert partition["essential_ternary"] == 218
    assert partition["essential_unate"] == 72
    assert sorted(row["size"] for row in partition["npn_orbits"]) == [8, 16, 48]
    assert {row["canonical_mask"] for row in partition["npn_orbits"]} == {"0x01", "0x07", "0x17"}

    strict = committed["singleton_strict_family"]["rows"]
    assert [row["n"] for row in strict] == list(range(5, 11))
    for row in strict:
        assert row["m"] == row["n"] + 1
        assert row["min_input_degree"] >= 3
        assert row["switching_balanced"] is False
        assert row["missing_word_absent"]

    signed = committed["signed_majority_x"]
    assert signed["abstract_bad_boundary_types"] == {
        "00": [["P01", "P10", 1, 0], ["P10", "P01", 0, 1]],
        "01": [],
        "10": [],
        "11": [],
    }
    for row in signed["length_audit"]:
        assert row["length"] % 2 == 0 and row["length"] >= 6
        assert row["missing_by_class"] == {"00": 2, "01": 0, "10": 0, "11": 0}
    assert signed["brute_length_6"] == [
        {"class": "00", "range_size": 62, "missing": 2},
        {"class": "01", "range_size": 64, "missing": 0},
        {"class": "10", "range_size": 64, "missing": 0},
        {"class": "11", "range_size": 64, "missing": 0},
    ]
    assert signed["length_6_cohomology_class_counts"] == {
        "00": 65536,
        "01": 65536,
        "10": 65536,
        "11": 65536,
    }

    implication = json.loads((ROOT / "IMPLICATION.json").read_text(encoding="utf-8"))
    assert implication["laboratory"] == "V99"
    assert implication["classification"] == "frontier_progress"
    assert implication["material_advance_rule_met"]
    assert [item["proved"] for item in implication["bridge_lemmas"][:10]] == [True] * 10
    assert [item["proved"] for item in implication["bridge_lemmas"][10:]] == [False] * 3
    assert implication["next_front"] == "middle_unate_bijunctive_transfer"
    assert not implication["p_vs_np_resolved"]
    assert not implication["novelty_confirmed"]
    assert not implication["peer_reviewed"]

    print(
        "V99 verification passed: singleton-core polynomial extension, strict "
        "unbalanced lambda=N family, and exact signed-MAJ simple-X dichotomy."
    )


if __name__ == "__main__":
    main()
