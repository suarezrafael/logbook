#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import random
from pathlib import Path

import v59_core as core

ROOT = Path(__file__).resolve().parent


def main() -> None:
    assert len(core.ORBIT_07) == 48
    fiber_checks = 0
    for mask in core.ORBIT_07:
        for value in (0, 1):
            clauses = core.local_2cnf_for_fiber(mask, value)
            described = {
                point
                for point in range(8)
                if all(core.eval_clause(clause, point) for clause in clauses)
            }
            assert described == set(core.fiber(mask, value))
            fiber_checks += 1

    harper_checks = 0
    for m in range(2, 33):
        kappa = core.harper_vertex_expansion_constant(m)
        assert 0 < kappa <= 1
        assert kappa * math.sqrt(m) > 1.25
        harper_checks += 1

    direct_sum = []
    for k in range(4):
        audit = core.direct_sum_potential_audit(k)
        assert audit["boundary_size"] == audit["image_size"] - 1
        assert audit["interior_preimages"] == 1
        assert all(value == 1 for value in audit["neighbor_preimages"])
        assert audit["interior_exact_forced"] == audit["n"]
        assert set(audit["neighbor_exact_forced"]) == {audit["n"]}
        assert audit["interior_unit_forced"] == 0
        assert set(audit["neighbor_unit_forced"]) == {0}
        assert not audit["strict_exact_forced_improvement_exists"]
        assert not audit["strict_unit_improvement_exists"]
        assert not audit["strict_smaller_fiber_exists"]
        direct_sum.append(audit)

    rng = random.Random(59059)
    random_cases = []
    for _ in range(500):
        n = rng.randint(5, 10)
        statistics = core.boundary_statistics(n, core.random_orbit_circuit(rng, n))
        assert (
            statistics["uniform_input_boundary_probability"] + 1e-12
            >= statistics["harper_sampling_lower_bound"]
        )
        random_cases.append(statistics)

    computed_central = {
        "harper_internal_boundary_fraction": "binom(m,floor(m/2))/2^(m-1)=Theta(1/sqrt(m))",
        "input_sampling_success_lower_bound": "kappa_m * alpha",
        "direct_sum_flat_potential_barrier": True,
        "n9_exact_search_complete": False,
        "sms_blueprint_prepared": True,
    }
    computed_validation = {
        "orbit_size": len(core.ORBIT_07),
        "fiber_cnf_checks": fiber_checks,
        "harper_constant_checks": harper_checks,
        "direct_sum_cases": len(direct_sum),
        "random_boundary_cases": len(random_cases),
        "random_min_input_boundary_probability": min(
            item["uniform_input_boundary_probability"] for item in random_cases
        ),
        "random_min_uniform_image_boundary_fraction": min(
            item["uniform_image_boundary_fraction"] for item in random_cases
        ),
        "random_min_ratio_to_harper_bound": min(
            item["ratio_to_lower_bound"] for item in random_cases
        ),
        "failures": 0,
    }

    committed = json.loads((ROOT / "RESULTS.json").read_text(encoding="utf-8"))
    assert committed["version"] == "V59"
    assert committed["status"] == "passed"
    assert committed["central_results"] == computed_central
    assert committed["validation"] == computed_validation
    assert committed["direct_sum"] == direct_sum
    assert committed["scientific_status"] == {
        "peer_reviewed": False,
        "novelty_confirmed": False,
        "deterministic_0x07_avoid_solved": False,
        "p_vs_np_resolved": False,
    }

    print("V59 primary verification passed:")
    print(f"  {fiber_checks} local 2-CNF fibers reconstructed;")
    print(f"  {harper_checks} Harper constants checked;")
    print(f"  {len(direct_sum)} direct-sum flat-potential barriers;")
    print(f"  {len(random_cases)} random boundary-sampling inequalities;")
    print("  committed evidence matches without timing or snapshot rewrites; zero failures.")


if __name__ == "__main__":
    main()
