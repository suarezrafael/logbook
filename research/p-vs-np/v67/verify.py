#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from v67_branch_growth_probe import main as run_probe

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def verify_repository_surface() -> int:
    required = [
        "README.md",
        "DIRECT_SUM_PROPOSITION.md",
        "BRANCHING_SANDWICH.md",
        "OVERLAP_GROWTH_REPORT.md",
        "WITNESSES.json",
        "RESULTS.json",
        "V68_CORE_CONTEXT.md",
        "verify_independent.py",
    ]
    assert all((HERE / name).is_file() for name in required)

    results = json.loads((HERE / "RESULTS.json").read_text())
    witnesses = json.loads((HERE / "WITNESSES.json").read_text())
    ledger = json.loads((ROOT / "LEDGER.json").read_text())

    assert results["version"] == "V67" and results["failures"] == 0
    assert results["direct_sum_finite_validation"]["direct_sum_c"] == 6
    assert results["regular_overlap_chains"]["maximum_c"] <= 2
    assert results["random_overlap_probe"]["seed"] == 42
    assert results["random_overlap_probe"]["samples"] == 4000
    assert results["random_overlap_probe"]["first_c16_n10"]["c"] == 16
    assert results["random_overlap_probe"]["global_best"]["c"] == 36
    assert witnesses["c16"]["signatures"] == results["random_overlap_probe"]["first_c16_n10"]["signatures"]
    assert witnesses["c36"]["signatures"] == results["random_overlap_probe"]["global_best"]["signatures"]

    assert ledger["schema_version"] >= 8
    assert int(ledger["current_version"][1:]) >= 67
    assert ledger["program"]["p_vs_np_route_active"] is False
    assert ledger["program"]["p_vs_np_resolved"] is False
    assert any(item["version"] == "V67" for item in ledger["versions"])
    assert ledger["affine_cell_branching"]["v67_seed"] == 42
    assert ledger["affine_cell_branching"]["v67_samples"] == 4000
    assert ledger["affine_cell_branching"]["v67_max_c"] == 36

    runner = (ROOT / "verify_all.sh").read_text()
    assert "V67|primary|v67/verify.py|quick|" in runner
    assert "V67|independent|v67/verify_independent.py|quick|" in runner

    state = (ROOT / "STATE.md").read_text()
    assert int(__import__("re").search(r"\*\*Current laboratory:\*\* V(\d+)", state).group(1)) >= 67
    assert "Direct P-versus-NP route active:** no" in state
    assert "c=36" in state

    root_readme = (ROOT / "README.md").read_text()
    assert "[`v67/`](v67/)" in root_readme
    assert "direct sums of V57" in root_readme

    direct = (HERE / "DIRECT_SUM_PROPOSITION.md").read_text()
    assert "c(A \\oplus B)=c(A)c(B)" in direct
    assert "specific to direct sums of components with `c=1`" in direct
    sandwich = (HERE / "BRANCHING_SANDWICH.md").read_text()
    assert "c <= L_aff <= L_greedy" in sandwich
    assert "not claimed to be minimum DAG sizes" in sandwich

    corpus = "\n".join(
        path.read_text().lower()
        for path in HERE.iterdir()
        if path.suffix in {".md", ".json"}
    )
    forbidden = (
        "p versus np is solved",
        "we prove p != np",
        "c_max(n) is exponential",
        "polynomial branching is proved",
        "unrestricted nc0_3-avoid is solved",
    )
    assert all(phrase not in corpus for phrase in forbidden)
    return 31


def main() -> None:
    run_probe()
    checks = verify_repository_surface()
    print(
        "V67 primary verification passed: direct-sum proposition surface; "
        "18 regular chains; 4,000 seeded overlap systems; "
        f"{checks} repository checks; zero failures."
    )


if __name__ == "__main__":
    main()
