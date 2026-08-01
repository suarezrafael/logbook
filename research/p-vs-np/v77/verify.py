#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from hashlib import sha256
from pathlib import Path

from topology_tree_certificate import (
    adjacency_from_edges,
    balanced_gate_tree,
    build_topology_certificate,
    prune_to_gate_tree,
    rooted_binary_source_tree,
)
from v77_topology_tree_transfer import generate_results

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def assert_value_error(callback) -> None:
    try:
        callback()
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def main() -> None:
    assert_value_error(lambda: adjacency_from_edges([]))
    assert_value_error(lambda: adjacency_from_edges([(0, 0)]))
    assert_value_error(lambda: balanced_gate_tree([]))
    assert_value_error(lambda: rooted_binary_source_tree((0, 0)))

    tiny = rooted_binary_source_tree(((0, 1), (2, 3)))
    certificate = build_topology_certificate(tiny)
    internal_vertex = next(
        vertex for vertex, neighbors in tiny.items() if len(neighbors) > 1
    )
    assert_value_error(
        lambda: prune_to_gate_tree(certificate, {internal_vertex: 0})
    )
    assert_value_error(lambda: prune_to_gate_tree(certificate, {999999: 0}))
    pruned = prune_to_gate_tree(certificate, {index: index for index in range(4)})
    assert max(record["external_degree"] for record in pruned["records"]) <= 2

    result_path = HERE / "RESULTS.json"
    static_path = HERE / "STATIC_TOPOLOGY_CERTIFICATE.json"
    if not result_path.is_file() or not static_path.is_file():
        raise AssertionError("committed V77 deterministic artifacts are missing")
    committed = json.loads(result_path.read_text(encoding="utf-8"))
    committed_static = json.loads(static_path.read_text(encoding="utf-8"))
    generated, generated_static = generate_results()
    normalized = json.loads(json.dumps(generated, sort_keys=True))
    normalized_static = json.loads(json.dumps(generated_static, sort_keys=True))
    if committed != normalized:
        raise AssertionError("committed V77 RESULTS.json differs from generation")
    if committed_static != normalized_static:
        raise AssertionError("committed V77 static certificate differs from generation")
    static_bytes = (json.dumps(committed_static, indent=2, sort_keys=True) + "\n").encode()
    assert sha256(static_bytes).hexdigest() == committed["static_certificate"]["sha256"]

    required = [
        "README.md",
        "TOPOLOGY_TREE_TRANSFER.md",
        "FPT_SUPPORT_WIDTH_COMPOSITION.md",
        "EXHAUSTIVE_RESULTS.md",
        "V77_TOPOLOGY_TREE_TRANSFER_THEOREM.tex",
        "V77_FPT_SUPPORT_WIDTH_THEOREM.tex",
        "V78_CORE_CONTEXT.md",
        "topology_tree_certificate.py",
        "support_connectivity_oracle.py",
        "v77_topology_tree_transfer.py",
        "verify.py",
        "verify_independent.py",
        "verify_composition.py",
        "verify_composition_independent.py",
        "RESULTS.json",
        "COMPOSITION_RESULTS.json",
        "STATIC_TOPOLOGY_CERTIFICATE.json",
    ]
    assert all((HERE / name).is_file() for name in required)
    assert committed["version"] == "V77"
    assert committed["status"] == "passed" and committed["failures"] == 0

    theorem = committed["transfer_theorem"]
    assert theorem["output_width"] == "at most 2b"
    assert theorem["output_height"] == "O(log m)"
    assert theorem["output_external_path_length"] == "O(m log m)"
    assert "A(2b)^2" in theorem["v75_consequence"]
    assert "Frederickson" in theorem["prior_art"]

    topology = committed["topology_certificate_audit"]
    assert topology["ordered_source_shapes"] == 2055
    assert topology["source_vertices"] == 31042
    assert topology["topology_clusters"] == 73239
    assert topology["retained_label_clusters"] == 33097
    assert topology["maximum_topology_height"] == 6
    assert topology["maximum_retained_gate_height"] == 4
    assert topology["retained_degree_three_clusters"] == 0
    assert topology["retained_cluster_boundary_edge_histogram"] == {
        "0": 2055,
        "1": 27861,
        "2": 3181,
    }

    seeded = committed["seeded_transfer_audit"]
    assert seeded["seed"] == 770077
    assert seeded["systems"] == 256
    assert seeded["retained_records_checked"] == 5132
    assert seeded["maximum_cover_edges"] == 2

    tight = committed["two_edge_tightness_witness"]
    assert tight["source_width_b"] == 3
    assert tight["cluster_width"] == 6
    assert tight["ratio"] == [6, 3]
    assert len(tight["boundary_edges"]) == 2

    iso = committed["five_variable_isomorphism_audit"]
    assert iso["variables"] == 5
    assert iso["support_universe_size"] == 25
    assert iso["maximum_gate_count"] == 6
    assert iso["raw_families"] == 245505
    assert iso["isomorphism_orbits"] == 2802
    assert iso["perfect_height_width_inflations"] == 0
    assert [iso["by_gate_count"][str(index)]["isomorphism_orbits"] for index in range(1, 7)] == [3, 12, 50, 193, 648, 1896]

    regression = committed["v76_witness_regression"]
    assert regression["families"] == 6
    assert regression["all_minimum_width"] == 2
    assert regression["all_perfect_height_width"] == 3

    status = committed["scientific_status"]
    assert status["topology_tree_log_height_is_prior_art"] is True
    assert status["retained_cluster_two_edge_lemma_proved"] is True
    assert status["supplied_decomposition_width_2b_log_height_transfer_proved"] is True
    assert status["v76_width_4b_transfer_still_correct_but_dominated"] is True
    assert status["factor_two_known_optimal_for_all_hierarchies"] is False
    assert status["width_preserving_O_log_m_refuted"] is False
    assert status["unrestricted_nc0_3_avoid_solved"] is False
    assert status["p_vs_np_resolved"] is False

    proof = (HERE / "TOPOLOGY_TREE_TRANSFER.md").read_text(encoding="utf-8")
    for token in (
        "Leaf-label pruning lemma",
        "retained two-edge lemma",
        "at most two original edges",
        "width(T') <= 2b",
        "O(m log m A(2b)^2 poly(n,m))",
        "Frederickson",
        "can be tight for a particular valid cluster",
    ):
        assert token in proof, token

    finite = (HERE / "EXHAUSTIVE_RESULTS.md").read_text(encoding="utf-8")
    for token in ("2,055", "73,239", "33,097", "5,132", "245,505", "2,802"):
        assert token in finite, token

    tex = (HERE / "V77_TOPOLOGY_TREE_TRANSFER_THEOREM.tex").read_text(encoding="utf-8")
    for token in (
        "Retained two-edge lemma",
        "Two-edge support-boundary cover",
        "Restricted topology-tree transfer",
        "2b",
    ):
        assert token in tex, token

    runner = (ROOT / "verify_all.sh").read_text(encoding="utf-8")
    assert "V77|primary|v77/verify.py|quick|" in runner
    assert "V77|independent|v77/verify_independent.py|quick|" in runner
    workflow = (ROOT.parent.parent / ".github" / "workflows" / "p-vs-np-verify.yml").read_text(encoding="utf-8")
    assert "V77_TOPOLOGY_TREE_TRANSFER_THEOREM.tex" in workflow
    assert "V77_FPT_SUPPORT_WIDTH_THEOREM.tex" in workflow

    state = (ROOT / "STATE.md").read_text(encoding="utf-8")
    current = re.search(r"\*\*Current laboratory:\*\* V(\d+)(?: candidate)?", state)
    assert current and int(current.group(1)) >= 77
    assert "**Direct P-versus-NP route active:** no" in state
    assert "**P versus NP resolved:** no" in state
    root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "[`v77/`](v77/)" in root_readme
    publication = (ROOT / "PUBLICATION_INDEX.md").read_text(encoding="utf-8")
    assert "V77_TOPOLOGY_TREE_TRANSFER_THEOREM.tex" in publication
    assert "V77_FPT_SUPPORT_WIDTH_THEOREM.tex" in publication

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
        "we prove factor two is globally optimal",
        "width-preserving logarithmic balancing is impossible",
        "peer reviewed theorem",
    ):
        assert forbidden not in corpus

    print(
        "V77 primary verification passed: prior-art topology hierarchy; proved retained two-edge cover and 2b transfer; "
        "validated leaf-only labels; 2,055 source shapes; 2,802 five-variable support orbits; zero failures."
    )


if __name__ == "__main__":
    main()
