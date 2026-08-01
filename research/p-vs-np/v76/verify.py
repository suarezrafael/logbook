#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

from decomposition_pareto import (
    balanced_branch_tree,
    exact_pareto_frontier,
    normalize_supports,
    tree_metrics,
)
from cluster_cut_cover import audit_all_two_boundary_clusters
from v76_top_tree_transfer import WITNESS, generate_results

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def assert_value_error(callback) -> None:
    try:
        callback()
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def main() -> None:
    assert_value_error(lambda: normalize_supports([]))
    assert_value_error(lambda: normalize_supports([(0, 1, 2, 3)]))
    assert_value_error(lambda: normalize_supports([(-1,)]))
    assert_value_error(lambda: balanced_branch_tree([]))
    assert_value_error(lambda: tree_metrics(((0,), (1,)), (0, 0)))

    direct_audit = audit_all_two_boundary_clusters(
        WITNESS, balanced_branch_tree(range(7))
    )
    assert direct_audit["maximum_cover_edges"] == 4
    assert direct_audit["labelled_cluster_states"] > 0

    result_path = HERE / "RESULTS.json"
    if not result_path.is_file():
        raise AssertionError("committed V76 RESULTS.json is missing")
    committed = json.loads(result_path.read_text(encoding="utf-8"))
    generated = generate_results()
    if committed != generated:
        raise AssertionError("committed V76 RESULTS.json differs from generation")
    results = committed

    required = [
        "README.md",
        "TOP_TREE_TRANSFER.md",
        "EXHAUSTIVE_RESULTS.md",
        "V76_TOP_TREE_TRANSFER_THEOREM.tex",
        "V77_CORE_CONTEXT.md",
        "decomposition_pareto.py",
        "cluster_cut_cover.py",
        "v76_top_tree_transfer.py",
        "verify.py",
        "verify_independent.py",
        "RESULTS.json",
    ]
    assert all((HERE / name).is_file() for name in required)
    assert results["version"] == "V76"
    assert results["status"] == "passed" and results["failures"] == 0

    prior = results["top_tree_prior_art"]
    assert "Alstrup" in prior["source"]
    assert prior["height"] == "O(log m) for the O(m)-size labelled branch tree"
    assert "not a new top-tree library" in prior["implementation_status"]

    theorem = results["transfer_theorem"]
    assert theorem["output_width"] == "at most 4b"
    assert theorem["output_height"] == "O(log m)"
    assert theorem["output_external_path_length"] == "O(m log m)"
    assert "four" in theorem["cover_lemma"]
    assert "A(4b)^2" in theorem["v75_consequence"]

    validation = results["exact_dp_validation"]
    assert validation["instances"] == 1470
    assert validation["rooted_tree_evaluations"] == 16212

    exhaustive = results["exhaustive_n4_simple_rank3"]
    assert exhaustive["support_universe_size"] == 14
    assert exhaustive["instances"] == 9907
    assert exhaustive["inflated_instances"] == 6
    assert exhaustive["maximum_additive_inflation"] == 1
    assert exhaustive["by_gate_count"]["7"]["instances"] == 3432
    assert exhaustive["by_gate_count"]["7"]["perfect_height_width_inflations"] == 6

    witness = results["canonical_perfect_height_tradeoff"]
    assert witness["supports"] == [list(support) for support in WITNESS]
    assert witness["rank"] == 2 and witness["gate_count"] == 7
    assert witness["rooted_binary_trees"] == 10395
    frontier = [tuple(item) for item in witness["exact"]["frontier"]]
    assert frontier == [(2, 4, 21), (3, 3, 20)]

    cover = results["top_cluster_cover_validation"]
    assert cover["seed"] == 760076
    assert cover["exact_optimal_source_instances_n4_m_le_4"] == 1470
    assert cover["sampled_witness_source_trees"] == 128
    assert cover["seeded_random_instances"] == 64
    assert cover["connected_vertex_clusters"] == 47565
    assert cover["labelled_cluster_states"] == 101213
    assert cover["maximum_cover_edges"] == 4
    assert cover["all_states_covered"] is True

    paths = results["or_path_regression"]
    assert len(paths) == 8
    assert paths[-1]["edge_count"] == 8
    assert paths[-1]["exact"]["minimum_width"] == 2
    assert paths[-1]["exact"]["minimum_width_at_log_height"] == 2

    private = results["private_vertex_tree_regression"]
    assert [item["gate_count"] for item in private] == [2, 6, 14]
    assert [item["exact"]["minimum_width"] for item in private] == [1, 2, 2]
    assert [item["exact"]["minimum_width_at_log_height"] for item in private] == [1, 2, 3]

    status = results["scientific_status"]
    assert status["top_tree_log_height_is_prior_art"] is True
    assert status["four_cut_cover_lemma_proved"] is True
    assert status["supplied_decomposition_width_4b_log_height_transfer_proved"] is True
    assert status["v75_arbitrary_tree_depth_obstruction_removed_at_4b"] is True
    assert status["width_2b_centroid_transfer_claimed"] is False
    assert status["width_preserving_O_log_m_refuted"] is False
    assert status["factor_four_known_optimal"] is False
    assert status["unrestricted_nc0_3_avoid_solved"] is False
    assert status["p_vs_np_resolved"] is False

    proof = (HERE / "TOP_TREE_TRANSFER.md").read_text(encoding="utf-8")
    for token in (
        "Top-tree transfer theorem",
        "at most four original branch edges",
        "width(T') <= 4b",
        "O(m log m A(4b)^2 poly(n,m))",
        "does not refute width-preserving O(log m)",
        "Alstrup, Holm, de Lichtenberg, and Thorup",
        "Korhonen and Oum",
        "discarded centroid argument",
    ):
        assert token in proof, token

    finite = (HERE / "EXHAUSTIVE_RESULTS.md").read_text(encoding="utf-8")
    for token in (
        "9,907",
        "3,432",
        "six",
        "10,395",
        "(2,4,21)",
        "(3,3,20)",
        "101,213",
    ):
        assert token in finite, token

    tex = (HERE / "V76_TOP_TREE_TRANSFER_THEOREM.tex").read_text(encoding="utf-8")
    for token in (
        "Top-tree support-boundary transfer",
        "Four-cut cover lemma",
        "Perfect-height tradeoff witness",
        "4b",
    ):
        assert token in tex, token

    runner = (ROOT / "verify_all.sh").read_text(encoding="utf-8")
    assert "V76|primary|v76/verify.py|quick|" in runner
    assert "V76|independent|v76/verify_independent.py|quick|" in runner
    workflow = (
        ROOT.parent.parent / ".github" / "workflows" / "p-vs-np-verify.yml"
    ).read_text(encoding="utf-8")
    assert "V76_TOP_TREE_TRANSFER_THEOREM.tex" in workflow

    state = (ROOT / "STATE.md").read_text(encoding="utf-8")
    current = re.search(r"\*\*Current laboratory:\*\* V(\d+)(?: candidate)?", state)
    assert current and int(current.group(1)) >= 76
    assert "**Direct P-versus-NP route active:** no" in state
    assert "**P versus NP resolved:** no" in state
    root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "[`v76/`](v76/)" in root_readme
    publication = (ROOT / "PUBLICATION_INDEX.md").read_text(encoding="utf-8")
    assert "V76_TOP_TREE_TRANSFER_THEOREM.tex" in publication

    ledger = json.loads((ROOT / "LEDGER.json").read_text(encoding="utf-8"))
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
        "factor four is optimal",
        "width-preserving logarithmic balancing is impossible",
        "width 2b centroid theorem",
        "peer reviewed theorem",
    ):
        assert forbidden not in corpus

    direct = exact_pareto_frontier(WITNESS)
    assert direct["minimum_width"] == 2
    assert direct["minimum_width_at_log_height"] == 3

    print(
        "V76 primary verification passed: prior-art top-tree height; proved "
        "four-cut support-boundary cover and 4b transfer; 1,470 DP/brute "
        "instances; 9,907 exhaustive families; exact witness and regressions; "
        "zero failures."
    )


if __name__ == "__main__":
    main()
