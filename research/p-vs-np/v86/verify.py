#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from certificate_intersection import build_results

HERE = Path(__file__).resolve().parent


def main() -> None:
    committed = json.loads((HERE / "RESULTS.json").read_text(encoding="utf-8"))
    recomputed = build_results()
    assert recomputed == committed

    examples = committed["examples"]
    assert [examples[name]["c4_count"] for name in sorted(examples)] == [17, 18, 15]
    assert [examples[name]["incidence_girth"] for name in sorted(examples)] == [4, 4, 4]
    assert [examples[name]["nor3_nonconstant_anf_rank"] for name in sorted(examples)] == [12, 14, 11]
    assert all(row["nonzero_constant_syndromes_under_nor3"] == 0 for row in examples.values())
    assert [examples[name]["minimum_hall_deficient_gate_count"] for name in sorted(examples)] == [8, 9, 7]
    assert [examples[name]["minimum_hall_neighborhood_size"] for name in sorted(examples)] == [7, 8, 6]
    assert [examples[name]["support_branchwidth"] for name in sorted(examples)] == [5, 6, 5]
    assert all(row["all_three_certificate_families_fail_simultaneously"] is False for row in examples.values())

    totals = committed["totals"]
    assert totals == {
        "examples": 3,
        "c4_witnesses": 50,
        "nor3_nonconstant_anf_rank": 37,
        "nonzero_constant_syndromes_under_nor3": 0,
    }

    rows = committed["asymptotic_two_barrier"]["rows"]
    assert all(row["combined_with_v80_hall_bad_event_bound"] < 1 for row in rows)
    assert all(
        rows[index + 1]["duplicate_support_union_bound"] < rows[index]["duplicate_support_union_bound"]
        for index in range(len(rows) - 1)
    )

    gap = committed["width_gap"]
    assert all(gap[index + 1]["ratio"] > gap[index]["ratio"] for index in range(len(gap) - 1))
    assert committed["restriction_no_pullback"]["avoids_restricted_map"] is True
    assert committed["restriction_no_pullback"]["avoids_original_map"] is False

    print(
        "V86 primary verification passed: 3 V80 families, 50 C4 witnesses, "
        "37 independent NOR3 ANF vectors, zero constant syndromes, and the width-gap/no-pullback audits."
    )


if __name__ == "__main__":
    main()
