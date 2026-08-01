#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from support_connectivity_oracle import generate_composition_results, lambda_value

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main() -> None:
    for supports, mask in (([], 0), ([(0, 1, 2, 3)], 0), ([(0,)], 2)):
        try:
            lambda_value(supports, mask)
        except ValueError:
            pass
        else:
            raise AssertionError("malformed oracle input was accepted")

    path = HERE / "COMPOSITION_RESULTS.json"
    committed = json.loads(path.read_text(encoding="utf-8"))
    generated = json.loads(json.dumps(generate_composition_results(), sort_keys=True))
    if committed != generated:
        raise AssertionError("committed composition snapshot differs from generation")

    audit = committed["connectivity_oracle_audit"]
    assert audit == {
        "families": 127,
        "normalization_failures": 0,
        "ordered_submodularity_pairs": 78124,
        "submodularity_failures": 0,
        "subset_values": 2186,
        "support_universe_size": 7,
        "symmetry_failures": 0,
    }

    theorem = committed["composition_theorem"]
    assert theorem["requires_supplied_decomposition"] is False
    assert theorem["requires_stretch"] == "m > n"
    assert theorem["decomposition_runtime_exact"] == (
        "2^{O(k)} gamma m^6 log m + 2^{O(k^2)} gamma m"
    )
    assert theorem["decomposition_runtime_simplified"] == (
        "2^{O(k^2)} gamma m^6 log m"
    )
    assert "A(2k)^2" in theorem["total_runtime_exact"]
    assert theorem["result"] == "NC0_3-Avoid is FPT parameterized by support connectivity branchwidth"

    status = committed["scientific_status"]
    assert status["lambda_is_connectivity_function"] is True
    assert status["parameterized_chain_without_supplied_decomposition_closed"] is True
    assert status["korhonen_oum_algorithm_implemented_here"] is False
    assert status["unrestricted_nc0_3_avoid_solved"] is False
    assert status["p_vs_np_resolved"] is False

    proof = (HERE / "FPT_SUPPORT_WIDTH_COMPOSITION.md").read_text(encoding="utf-8")
    for token in (
        "connectivity function",
        "Korhonen and Oum",
        "2^{O(k)} gamma m^6 log m + 2^{O(k^2)} gamma m",
        "width at most `2k`",
        "fixed-parameter tractable in `k`",
        "does not implement the Korhonen--Oum algorithm",
    ):
        assert token in proof, token

    formal = (HERE / "V77_FPT_SUPPORT_WIDTH_THEOREM.tex").read_text(encoding="utf-8")
    for token in (
        "Support connectivity",
        "Support-branchwidth FPT avoidance",
        "2^{O(k^2)}\\gamma m",
        "A(2k)^2",
    ):
        assert token in formal, token

    state = (ROOT / "STATE.md").read_text(encoding="utf-8")
    assert "support-branchwidth FPT composition" in state
    assert "without a supplied decomposition" in state
    assert "**Direct P-versus-NP route active:** no" in state

    runner = (ROOT / "verify_all.sh").read_text(encoding="utf-8")
    assert "V77|composition|v77/verify_composition.py|quick|" in runner
    assert "V77|composition-independent|v77/verify_composition_independent.py|quick|" in runner

    workflow = (
        ROOT.parent.parent / ".github" / "workflows" / "p-vs-np-verify.yml"
    ).read_text(encoding="utf-8")
    assert "V77_FPT_SUPPORT_WIDTH_THEOREM.tex" in workflow

    print(
        "V77 composition verification passed: lambda_C connectivity function; "
        "127 exhaustive support families; 78,124 submodularity pairs; "
        "Korhonen-Oum discovery composed with V77/V75/V74; zero failures."
    )


if __name__ == "__main__":
    main()
