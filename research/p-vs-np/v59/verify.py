#!/usr/bin/env python3
from __future__ import annotations
import json, math, random, time
from pathlib import Path
import v59_core as core

ROOT = Path(__file__).resolve().parent

def main() -> None:
    started = time.perf_counter()
    assert len(core.ORBIT_07) == 48
    fiber_checks = 0
    for mask in core.ORBIT_07:
        for value in (0, 1):
            clauses = core.local_2cnf_for_fiber(mask, value)
            described = {
                point for point in range(8)
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

    direct = []
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
        direct.append(audit)

    rng = random.Random(59059)
    random_cases = []
    for _ in range(500):
        n = rng.randint(5, 10)
        stats = core.boundary_statistics(n, core.random_orbit_circuit(rng, n))
        assert stats["uniform_input_boundary_probability"] + 1e-12 >= stats["harper_sampling_lower_bound"]
        random_cases.append(stats)

    results = {
        "version": "V59",
        "status": "passed",
        "central_results": {
            "harper_internal_boundary_fraction": "binom(m,floor(m/2))/2^(m-1)=Theta(1/sqrt(m))",
            "input_sampling_success_lower_bound": "kappa_m * alpha",
            "direct_sum_flat_potential_barrier": True,
            "n9_exact_search_complete": False,
            "sms_blueprint_prepared": True,
        },
        "validation": {
            "orbit_size": len(core.ORBIT_07),
            "fiber_cnf_checks": fiber_checks,
            "harper_constant_checks": harper_checks,
            "direct_sum_cases": len(direct),
            "random_boundary_cases": len(random_cases),
            "random_min_input_boundary_probability": min(r["uniform_input_boundary_probability"] for r in random_cases),
            "random_min_uniform_image_boundary_fraction": min(r["uniform_image_boundary_fraction"] for r in random_cases),
            "random_min_ratio_to_harper_bound": min(r["ratio_to_lower_bound"] for r in random_cases),
            "failures": 0,
        },
        "direct_sum": direct,
        "scientific_status": {
            "peer_reviewed": False,
            "novelty_confirmed": False,
            "deterministic_0x07_avoid_solved": False,
            "p_vs_np_resolved": False,
        },
        "elapsed_seconds": round(time.perf_counter() - started, 6),
    }
    (ROOT / "RESULTS.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print("V59 primary verification passed:")
    print(f"  {fiber_checks} local 2-CNF fibers reconstructed;")
    print(f"  {harper_checks} Harper constants checked;")
    print(f"  {len(direct)} direct-sum flat-potential barriers;")
    print(f"  {len(random_cases)} random boundary-sampling inequalities; zero failures.")

if __name__ == "__main__":
    main()
