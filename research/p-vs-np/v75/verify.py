#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

from symbolic_prefix_circuit import (
    MonotoneArithmeticCircuit,
    build_symbolic_prefix_circuit,
    caterpillar_branch_tree,
)
from v75_symbolic_prefix import generate_results

import sys
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "v74"))
from two_fiber_model import make_gate


def assert_value_error(callback) -> None:
    try:
        callback()
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def main() -> None:
    assert_value_error(lambda: build_symbolic_prefix_circuit(2, []))
    gate = make_gate([0, 1], 6)
    assert_value_error(lambda: build_symbolic_prefix_circuit(2, [gate, gate], (0, 0)))
    assert_value_error(lambda: caterpillar_branch_tree([]))
    arithmetic = MonotoneArithmeticCircuit()
    assert_value_error(lambda: arithmetic.constant(-1))
    assert_value_error(lambda: arithmetic.scale(arithmetic.constant(1), -1))

    committed = json.loads((HERE / "RESULTS.json").read_text(encoding="utf-8"))
    generated = generate_results()
    assert generated == committed, "RESULTS.json drifted from deterministic generation"
    results = committed

    required = [
        "README.md",
        "SYMBOLIC_PREFIX_CIRCUIT.md",
        "EXHAUSTIVE_RESULTS.md",
        "V75_SYMBOLIC_PREFIX_THEOREM.tex",
        "V76_CORE_CONTEXT.md",
        "symbolic_prefix_circuit.py",
        "v75_symbolic_prefix.py",
        "verify.py",
        "verify_independent.py",
        "RESULTS.json",
    ]
    assert all((HERE / name).is_file() for name in required)
    assert results["version"] == "V75"
    assert results["status"] == "passed" and results["failures"] == 0

    exhaustive = results["exhaustive_binary_circuits"]
    assert exhaustive["circuits"] == 4096
    assert exhaustive["coefficient_checks"] == 32768
    assert exhaustive["prefix_checks"] == 61440
    assert exhaustive["avoidance_constructions"] == 4096
    assert exhaustive["arithmetic_operations_max"] == 11
    assert exhaustive["dynamic_reevaluations_max"] == 40

    seeded = results["seeded_ternary_circuits"]
    assert seeded["seed"] == 750075
    assert seeded["circuits"] == 48
    assert seeded["coefficient_checks"] == 6144
    assert seeded["prefix_checks"] == 12192
    assert seeded["avoidance_constructions"] == 96
    representative = seeded["representative"]
    assert representative["balanced"]["arithmetic_operations"] == 67
    assert representative["balanced"]["dynamic_reevaluations"] == 187
    assert representative["caterpillar"]["arithmetic_operations"] == 68
    assert representative["caterpillar"]["dynamic_reevaluations"] == 221

    last_shape = results["tree_shapes"]["instances"][-1]
    assert last_shape["m"] == 64
    assert last_shape["balanced_external_path_length"] == 384
    assert last_shape["caterpillar_external_path_length"] == 2079

    status = results["theorem_status"]
    assert status["paired_generating_polynomial_exact"] is True
    assert status["monotone_arithmetic_translation_exact"] is True
    assert status["arithmetic_size_O_m_A_b_squared"] is True
    assert status["incremental_bound_depth_sensitive"] is True
    assert status["balanced_supplied_tree_bound_O_m_log_m_A_b_squared"] is True
    assert status["arbitrary_supplied_tree_improvement"] is False
    assert status["automatic_balancing_without_width_loss"] is False
    assert status["unrestricted_nc0_3_avoid_solved"] is False
    assert status["p_vs_np_resolved"] is False

    proof = (HERE / "SYMBOLIC_PREFIX_CIRCUIT.md").read_text(encoding="utf-8")
    for token in (
        "Paired generating polynomial theorem",
        "S = O(m A(b)^2)",
        "O(S + sum_i D_T(i))",
        "O(m log(m) A(b)^2 poly(n,m))",
        "caterpillar",
        "Korhonen and Oum",
        "does not remove the depth obstruction",
    ):
        assert token in proof, token

    finite = (HERE / "EXHAUSTIVE_RESULTS.md").read_text(encoding="utf-8")
    for token in ("4,096", "32,768", "61,440", "12,192", "2,079"):
        assert token in finite, token

    tex = (HERE / "V75_SYMBOLIC_PREFIX_THEOREM.tex").read_text(encoding="utf-8")
    for token in (
        "Exact paired generating polynomial",
        "Monotone residual circuit",
        "Depth-sensitive incremental evaluation",
        "Balanced supplied decomposition corollary",
    ):
        assert token in tex, token

    runner = (ROOT / "verify_all.sh").read_text(encoding="utf-8")
    assert "V75|primary|v75/verify.py|quick|" in runner
    assert "V75|independent|v75/verify_independent.py|quick|" in runner
    workflow = (
        ROOT.parent.parent / ".github" / "workflows" / "p-vs-np-verify.yml"
    ).read_text(encoding="utf-8")
    assert "V75_SYMBOLIC_PREFIX_THEOREM.tex" in workflow

    state = (ROOT / "STATE.md").read_text(encoding="utf-8")
    current = re.search(r"\*\*Current laboratory:\*\* V(\d+)(?: candidate)?", state)
    assert current and int(current.group(1)) >= 75
    assert "Direct P-versus-NP route active:** no" in state
    assert "P versus NP resolved:** no" in state
    root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "[`v75/`](v75/)" in root_readme
    publication = (ROOT / "PUBLICATION_INDEX.md").read_text(encoding="utf-8")
    assert "V75_SYMBOLIC_PREFIX_THEOREM.tex" in publication

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
        "automatic width-preserving balancing theorem proved",
        "peer reviewed theorem",
    ):
        assert forbidden not in corpus

    print(
        "V75 primary verification passed: exact symbolic coefficients and prefixes; "
        "4,096 exhaustive circuits; 48 seeded ternary circuits on balanced and "
        "caterpillar trees; incremental/fresh agreement; repository and LaTeX gates; zero failures."
    )


if __name__ == "__main__":
    main()
