#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import re
from pathlib import Path

from v72_branch_residual import generate_results

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main():
    results = generate_results()
    (HERE / "RESULTS.json").write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n"
    )
    required = [
        "README.md",
        "COMPLEXITY_AND_BRANCH_DP.md",
        "PATHWIDTH_BENCHMARK.md",
        "PRIOR_ART.md",
        "V72_BRANCH_RESIDUAL_THEOREM.tex",
        "v72_branch_residual.py",
        "verify.py",
        "verify_independent.py",
        "RESULTS.json",
        "V73_CORE_CONTEXT.md",
    ]
    assert all((HERE / name).is_file() for name in required)
    assert results["version"] == "V72"
    assert results["status"] == "passed" and results["failures"] == 0
    assert results["exact_dp_exhaustive_rank3_n4_m_le_4"] == 1470
    assert results["branch_validation"]["systems"] == 96
    assert results["branch_validation"]["nodes"] == 852

    expected = {
        "v69-natural-n6": (4, 4, 21, 15),
        "v69-natural-n8": (4, 5, 28, 15),
        "v69-natural-n10": (4, 5, 35, 17),
        "v69-natural-n12": (4, 5, 57, 29),
        "v70-exact-record-n8": (4, 5, 40, 29),
        "v70-exact-record-n10": (4, 5, 50, 30),
    }
    benchmarks = {item["label"]: item for item in results["pathwidth_benchmarks"]}
    assert set(benchmarks) == set(expected)
    for label, values in expected.items():
        item = benchmarks[label]
        actual = (
            item["primal_pathwidth"],
            item["path_frontier_width"],
            item["path_G_proj"],
            item["exact_Gstar"],
        )
        assert actual == values, (label, actual, values)
    assert results["benchmark_summary"]["cases"] == 6
    assert results["benchmark_summary"]["path_orders_within_factor_2_1_on_preserved_cases"] is True
    assert math.isclose(
        results["benchmark_summary"]["maximum_ratio_to_Gstar"],
        35 / 17,
        rel_tol=0,
        abs_tol=1e-12,
    )
    assert results["benchmark_summary"]["linear_width_objective_equals_Gproj_objective"] is False

    padded = results["padded_binary_tree_family"]
    assert [item["linear_branch_width"] for item in padded] == [1, 1, 2]
    assert all(item["primal_treewidth_upper_bound"] == 2 for item in padded)

    scientific = results["scientific_status"]
    assert scientific["rank3_width_decision_np_complete"] is True
    assert scientific["exact_width_dp_verified"] is True
    assert scientific["branch_residual_dp_proved"] is True
    assert scientific["bounded_treewidth_forces_bounded_linear_width"] is False
    assert scientific["bounded_treewidth_forces_small_Gstar"] is False
    assert scientific["general_polynomial_good_order_proved"] is False
    assert scientific["p_vs_np_resolved"] is False

    proof = (HERE / "COMPLEXITY_AND_BRANCH_DP.md").read_text()
    for token in (
        "NP-complete",
        "{u,v,z_uv}",
        "D[S] = min",
        "A(b)^2",
        "treewidth at most two",
        "does not prove that the affine projected-DAG optimum",
    ):
        assert token in proof
    benchmark = (HERE / "PATHWIDTH_BENCHMARK.md").read_text()
    for token in ("2.059", "G_proj = 61", "G_proj = 50", "G*_proj = 30"):
        assert token in benchmark
    prior = (HERE / "PRIOR_ART.md").read_text()
    for token in (
        "10.1016/S0166-218X(00)00175-X",
        "2010.02388",
        "10.1016/0020-0190(92)90234-M",
    ):
        assert token in prior
    tex = (HERE / "V72_BRANCH_RESIDUAL_THEOREM.tex").read_text()
    for token in (
        "Three-uniform NP-completeness",
        "Exact width dynamic program",
        "Exact branch residual DP",
        "A(b)^2",
    ):
        assert token in tex

    runner = (ROOT / "verify_all.sh").read_text()
    assert "V72|primary|v72/verify.py|quick|" in runner
    assert "V72|independent|v72/verify_independent.py|quick|" in runner
    state = (ROOT / "STATE.md").read_text()
    current = re.search(r"\*\*Current laboratory:\*\* V(\d+)(?: candidate)?", state)
    assert current and int(current.group(1)) >= 72
    root_readme = (ROOT / "README.md").read_text()
    assert "[`v72/`](v72/)" in root_readme
    publication = (ROOT / "PUBLICATION_INDEX.md").read_text()
    assert "V72_BRANCH_RESIDUAL_THEOREM.tex" in publication
    workflow = (ROOT.parent.parent / ".github" / "workflows" / "p-vs-np-verify.yml").read_text()
    assert "V72_BRANCH_RESIDUAL_THEOREM.tex" in workflow

    ledger = json.loads((ROOT / "LEDGER.json").read_text())
    assert int(ledger["current_version"][1:]) >= 70
    assert ledger["program"]["p_vs_np_route_active"] is False
    assert ledger["program"]["p_vs_np_resolved"] is False

    corpus = "\n".join(
        path.read_text().lower()
        for path in HERE.iterdir()
        if path.suffix in {".md", ".json", ".tex"}
    )
    for forbidden in (
        "p versus np is solved",
        "we prove p != np",
        "accepted by eccc",
        "peer reviewed theorem",
        "all orders force superpolynomial",
        "unrestricted nc0_3-avoid is solved",
    ):
        assert forbidden not in corpus

    print(
        "V72 primary verification passed: rank-three NP-completeness; "
        "1,470 exact width cases; 852 branch nodes; six preserved-record "
        "pathwidth benchmarks; repository and LaTeX gates; zero failures."
    )


if __name__ == "__main__":
    main()
