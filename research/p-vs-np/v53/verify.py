#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import v53_core as core

ROOT = Path(__file__).resolve().parent


def main() -> None:
    computed = []
    union_checks = rank_checks = exact_checks = 0

    # Preserved finite V53 examples.
    for name, case in core.FINITE_EXAMPLES.items():
        n, edges, t = case["n"], case["edges"], case["t"]
        m = len(edges)
        assert m == n + 1
        assert all(len(edge) == 3 and len(set(edge)) == 3 for edge in edges)
        ok, unions, collision = core.union_free_certificate(edges, t)
        assert ok and collision is None
        expected = sum(__import__("math").comb(m, j) for j in range(t + 1))
        assert len(unions) == expected
        union_checks += len(unions)
        image = core.circuit_image(n, edges)
        degree = core.exact_syndrome_degree_gf2(image, m, t + 2)
        assert degree == t + 1
        exact_checks += 1
        monomials = core.monomials(m, t)
        matrix = core.evaluation_matrix(image, m, t)
        ranks = {}
        for prime in (2, 3, 5):
            rank = core.rank_mod(matrix, prime)
            assert rank == len(monomials)
            ranks[str(prime)] = rank
            rank_checks += 1
        flipped = core.circuit_image(n, edges, case["output_flip_mask"])
        assert core.exact_syndrome_degree_gf2(flipped, m, t + 2) == degree
        computed.append(
            {
                "name": name,
                "n": n,
                "m": m,
                "t_union_free": t,
                "subset_unions_checked": len(unions),
                "range_size": len(image),
                "minimum_syndrome_degree_gf2": degree,
                "degree_t_evaluation_rank": ranks,
                "degree_t_monomials": len(monomials),
                "output_flip_control_degree": degree,
                "edges": edges,
            }
        )

    # Mandatory regression for the theorem retracted by V54.
    nested_cover = [
        [0, 1, 2],
        [0, 3, 4],
        [1, 5, 6],
        [2, 7, 8],
    ]
    ok4, _, collision4 = core.union_free_certificate(nested_cover, 4)
    assert not ok4 and collision4 is not None
    left, right, _ = collision4
    assert set(left) == {1, 2, 3}
    assert set(right) == {0, 1, 2, 3}

    committed_results = json.loads((ROOT / "RESULTS.json").read_text(encoding="utf-8"))
    committed_examples = json.loads(
        (ROOT / "FINITE_EXAMPLES.json").read_text(encoding="utf-8")
    )
    assert committed_results["status"] == "passed_with_retraction_regression"
    assert committed_results["scientific_status"] == {
        "union_free_substitution_lemma_preserved": True,
        "incidence_girth_implication_retracted": True,
        "omega_log_family_retracted": True,
        "use_v54_as_current_record": True,
    }
    assert committed_results["retraction_regression"]["four_union_free"] is False
    assert committed_results["retraction_regression"]["failure_mode"] == (
        "nested cover collision"
    )
    assert committed_results["summary"] == {
        "examples": len(computed),
        "union_values_checked": union_checks,
        "field_rank_checks": rank_checks,
        "exact_degree_checks": exact_checks,
        "retraction_regressions": 1,
        "failures": 0,
    }

    assert len(committed_examples) == len(computed)
    assert committed_results["finite_examples"] == committed_examples
    for actual, expected_example in zip(computed, committed_examples, strict=True):
        for key, value in actual.items():
            assert expected_example[key] == value, (key, expected_example[key], value)

    print("V53 corrected verification passed:")
    print(f"  {len(computed)}/{len(computed)} finite NC0_3 stretch-one examples preserved;")
    print(f"  {union_checks} distinct subset unions checked;")
    print(f"  {rank_checks} full-rank evaluations over GF(2), GF(3), GF(5);")
    print("  exact syndrome degrees 3 and 4 preserved;")
    print("  immutable retraction status preserved without rewriting snapshots.")


if __name__ == "__main__":
    main()
