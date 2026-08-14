#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from switching_unate import build_results

ROOT = Path(__file__).resolve().parent


def main() -> None:
    committed = json.loads((ROOT / "RESULTS.json").read_text(encoding="utf-8"))
    rebuilt = build_results()
    assert rebuilt == committed

    theorem = committed["theorem_status"]
    for key in (
        "balanced_unate_recognizable_linear_incidence_time",
        "balanced_unate_switches_to_monotone",
        "balanced_unate_positive_surplus_component_avoidance_in_P_via_kuntewar_sarma",
        "strict_nonmonotone_irreducible_large_kernel_family",
        "loose_x_support_alone_insufficient_for_arbitrary_ternary_labels",
        "parity_labeled_loose_x_surjective",
    ):
        assert theorem[key]
    assert not theorem["unrestricted_NC0_3_avoid_polynomial_time"]
    assert not theorem["hlz_worst_case_runtime_improved"]
    assert not theorem["p_vs_np_resolved"]

    census = committed["ternary_truth_table_audit"]
    assert census == {
        "all_masks": 256,
        "essential_ternary_masks": 218,
        "essential_ternary_unate_masks": 72,
    }

    strict = committed["strict_family_audit"]["rows"]
    assert [row["n"] for row in strict] == list(range(5, 11))
    for row in strict:
        assert row["m"] == row["n"] + 1
        assert row["min_input_degree"] >= 3
        assert row["balanced"]
        assert row["raw_nonmonotone"]
        assert row["all_essential_ternary"]

    xrows = committed["loose_x_parity_audit"]["rows"]
    assert [row["x_edges"] for row in xrows] == [6, 8, 10, 12]
    for row in xrows:
        assert row["host_outputs"] == row["host_inputs"] + 1
        assert row["min_host_input_degree"] >= 2
        assert row["all_x_targets_verified"] == 2 ** row["x_edges"]
    assert xrows[0]["host_range_size_if_bruteforced"] == 1024

    implication = json.loads((ROOT / "IMPLICATION.json").read_text(encoding="utf-8"))
    assert implication["laboratory"] == "V98"
    assert implication["classification"] == "frontier_progress"
    assert implication["material_advance_rule_met"]
    assert [item["proved"] for item in implication["bridge_lemmas"][:8]] == [True] * 8
    assert [item["proved"] for item in implication["bridge_lemmas"][8:]] == [False] * 3
    assert implication["next_front"] == "label_cohomology_and_nonunate_transfer"
    assert not implication["p_vs_np_resolved"]
    assert not implication["novelty_confirmed"]
    assert not implication["peer_reviewed"]

    print(
        "V98 verification passed: balanced-unate switching to monotone, strict "
        "irreducible nonmonotone family, and parity loose-X support obstruction."
    )


if __name__ == "__main__":
    main()
