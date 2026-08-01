#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

from or_path_family import or_path_instance, residual_width_tables
from two_fiber_model import (
    brute_preimage_counts,
    compiled_fiber_cells,
    make_gate,
    weighted_target_dp,
)
from v74_two_fiber_avoidance import generate_results

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def assert_value_error(callback) -> None:
    try:
        callback()
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def main() -> None:
    assert_value_error(lambda: make_gate([-1, 0], 0))
    negative_gate = {"support": [-1], "truth_mask": 0, "output_flip": 0}
    out_of_range_gate = {"support": [0, 2], "truth_mask": 0, "output_flip": 0}
    assert_value_error(lambda: weighted_target_dp(2, [negative_gate], [0]))
    assert_value_error(lambda: weighted_target_dp(2, [out_of_range_gate], [0]))
    assert_value_error(lambda: brute_preimage_counts(2, [out_of_range_gate]))

    gate_x = make_gate((0,), 0b10)
    gate_true = make_gate((0,), 0b11)
    gate_not_x = make_gate((0,), 0b10, output_flip=1)
    zero_fiber = compiled_fiber_cells(1, gate_x, 0)
    one_fiber = compiled_fiber_cells(1, gate_x, 1)
    tautology = compiled_fiber_cells(1, gate_x, None)
    assert zero_fiber != one_fiber
    assert tautology == (tuple(),)
    assert compiled_fiber_cells(1, gate_true, 1) != one_fiber
    assert compiled_fiber_cells(1, gate_not_x, 1) == zero_fiber

    path_n, path_gates, path_target = or_path_instance(5)
    cached_widths, cached_frontiers = residual_width_tables(
        path_n, path_gates, path_target
    )
    cached_widths[0] = -1
    cached_frontiers[0] = -1
    fresh_widths, fresh_frontiers = residual_width_tables(
        path_n, path_gates, path_target
    )
    assert fresh_widths[0] == 1
    assert fresh_frontiers[0] == 0

    results = generate_results()
    serialized = json.dumps(results, indent=2, sort_keys=True) + "\n"
    result_path = HERE / "RESULTS.json"
    assert json.loads(result_path.read_text(encoding="utf-8")) == results
    result_path.write_text(serialized, encoding="utf-8")

    required = [
        "README.md",
        "TWO_FIBER_AVOIDANCE.md",
        "EXHAUSTIVE_RESULTS.md",
        "V74_TWO_FIBER_AVOIDANCE_THEOREM.tex",
        "two_fiber_model.py",
        "or_path_family.py",
        "v74_two_fiber_avoidance.py",
        "verify.py",
        "verify_independent.py",
        "RESULTS.json",
        "V75_CORE_CONTEXT.md",
    ]
    assert all((HERE / name).is_file() for name in required)
    assert results["version"] == "V74"
    assert results["status"] == "passed" and results["failures"] == 0

    catalogue = results["affine_catalogue"]
    assert catalogue["affine_cells_by_arity"] == {"1": 3, "2": 11, "3": 51}
    assert catalogue["maximum_cells_per_ternary_fiber"] == 3
    assert catalogue["ternary_subset_partition_histogram"] == {
        "0": 1,
        "1": 51,
        "2": 196,
        "3": 8,
    }
    assert catalogue["worst_case_fiber_masks"] == [
        127,
        191,
        223,
        239,
        247,
        251,
        253,
        254,
    ]

    exhaustive = results["exhaustive_binary_circuits"]
    assert exhaustive["circuits"] == 4096
    assert exhaustive["target_checks"] == 32768
    assert exhaustive["avoidance_constructions"] == 4096
    assert exhaustive["prefix_partition_checks"] == 12288

    ternary = results["seeded_ternary_circuits"]
    assert ternary["circuits"] == 96
    assert ternary["target_checks"] == 1536
    assert ternary["avoidance_constructions"] == 96
    assert results["polarity"]["flipped_truth_table_point_checks"] == 2048

    path = results["or_path_family"]
    assert path["primal_treewidth"] == 1
    assert path["exact_formula"] == "G*_proj=1 for m=1 and G*_proj=3m-3 for m>=2"
    assert path["instances"][-1]["edge_count"] == 9
    assert path["instances"][-1]["Gstar"] == 24
    assert path["instances"][-1]["G_proj"] == 24

    scientific = results["scientific_status"]
    assert scientific["exact_both_fibers_encoded"] is True
    assert scientific["target_preimage_count_exact"] is True
    assert scientific["bounded_branchwidth_target_search_proved"] is True
    assert scientific["unrestricted_nc0_3_avoid_solved"] is False
    assert scientific["branch_decomposition_found_in_polynomial_time"] is False
    assert scientific["p_vs_np_resolved"] is False

    proof = (HERE / "TWO_FIBER_AVOIDANCE.md").read_text(encoding="utf-8")
    for token in (
        "Three-cell theorem",
        "mu_root(empty)",
        "N(p0)+N(p1)=N(p)",
        "O(m^2 A(b)^2 poly(n,m))",
        "C_B / G*_proj <= A(B)",
        "G*_proj = 3m-3",
        "does not imply a lower bound",
    ):
        assert token in proof, token

    finite = (HERE / "EXHAUSTIVE_RESULTS.md").read_text(encoding="utf-8")
    for token in ("4,096 circuits", "32,768", "1,536", "2,048", "3m-3"):
        assert token in finite, token

    tex = (HERE / "V74_TWO_FIBER_AVOIDANCE_THEOREM.tex").read_text(encoding="utf-8")
    for token in (
        "Three-cell ternary fiber theorem",
        "Exact target preimage count",
        "Prefix-count avoidance",
        "Exact OR-path residual cost",
    ):
        assert token in tex, token

    runner = (ROOT / "verify_all.sh").read_text(encoding="utf-8")
    assert "V74|primary|v74/verify.py|quick|" in runner
    assert "V74|independent|v74/verify_independent.py|quick|" in runner
    state = (ROOT / "STATE.md").read_text(encoding="utf-8")
    current = re.search(r"\*\*Current laboratory:\*\* V(\d+)(?: candidate)?", state)
    assert current and int(current.group(1)) >= 74
    assert "External contact:** sent" in state
    assert "P-versus-NP route active:** no" in state
    root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "[`v74/`](v74/)" in root_readme
    publication = (ROOT / "PUBLICATION_INDEX.md").read_text(encoding="utf-8")
    assert "V74_TWO_FIBER_AVOIDANCE_THEOREM.tex" in publication
    workflow = (
        ROOT.parent.parent / ".github" / "workflows" / "p-vs-np-verify.yml"
    ).read_text(encoding="utf-8")
    assert "V74_TWO_FIBER_AVOIDANCE_THEOREM.tex" in workflow

    ledger = json.loads((ROOT / "LEDGER.json").read_text(encoding="utf-8"))
    assert int(ledger["current_version"][1:]) >= 70
    assert ledger["program"]["p_vs_np_route_active"] is False
    assert ledger["program"]["p_vs_np_resolved"] is False

    corpus = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in HERE.iterdir()
        if path.suffix in {".md", ".json", ".tex"}
    )
    for forbidden in (
        "p versus np is solved",
        "we prove p != np",
        "unrestricted nc0_3-avoid is solved",
        "accepted by eccc",
        "peer reviewed theorem",
        "superpolynomial g*_proj lower bound proved",
    ):
        assert forbidden not in corpus

    print(
        "V74 primary verification passed: malformed-support rejection; immutable "
        "fiber-cache keys; exact two-fiber model; 256 ternary partitions; 4,096 "
        "exhaustive circuits and 32,768 targets; constructive bounded-width "
        "avoidance; OR-path G*=3m-3; semantic RESULTS.json lock; repository and "
        "LaTeX gates; zero failures."
    )


if __name__ == "__main__":
    main()
