from __future__ import annotations

from itertools import product

from oracle_extraction import (
    CountingD3GirthOracle,
    LocalGate,
    brute_circuits,
    brute_girth,
    extract_girth_circuit_and_hall_witness,
    is_hall_expanding_through,
    local_enumeration_and_lift,
    normalize_presentation,
    output_is_avoided,
    private_path_circuit,
    query_bound,
)


def all_presentations(left_count: int, right_count: int):
    choices = tuple(
        tuple(right for right in range(right_count) if mask & (1 << right))
        for mask in range(1 << right_count)
    )
    for rows in product(choices, repeat=left_count):
        yield normalize_presentation(rows)


def canonical_reference(
    shortest_circuits: tuple[tuple[int, ...], ...], order: tuple[int, ...]
) -> tuple[int, ...]:
    candidates = [set(circuit) for circuit in shortest_circuits]
    for element in order:
        excluding = [candidate for candidate in candidates if element not in candidate]
        if excluding:
            candidates = excluding
    assert len(candidates) == 1
    return tuple(sorted(candidates[0]))


def truth_tables(arity: int):
    for mask in range(1 << (1 << arity)):
        yield tuple((mask >> index) & 1 for index in range(1 << arity))


def local_family_audit(supports: tuple[tuple[int, ...], ...]) -> dict:
    presentation = normalize_presentation(supports)
    oracle = CountingD3GirthOracle(presentation)
    extraction = extract_girth_circuit_and_hall_witness(
        presentation, oracle, dependence_guaranteed=True
    )
    assert extraction.circuit is not None
    input_count = max((max(row, default=-1) for row in presentation), default=-1) + 1
    tables = [tuple(truth_tables(len(row))) for row in presentation]
    circuits_checked = avoided_checked = max_local_image = 0
    for gate_tables in product(*tables):
        gates = tuple(
            LocalGate(row, table) for row, table in zip(presentation, gate_tables)
        )
        witness = local_enumeration_and_lift(gates, extraction.circuit)
        assert output_is_avoided(gates, witness.global_output, input_count)
        max_local_image = max(max_local_image, witness.local_assignments_enumerated)
        circuits_checked += 1
        avoided_checked += 1
    return {
        "supports": [list(row) for row in presentation],
        "truth_table_combinations": circuits_checked,
        "avoided_outputs_verified": avoided_checked,
        "girth": extraction.girth,
        "canonical_circuit": list(extraction.circuit),
        "neighborhood_size": len(extraction.neighborhood or ()),
        "local_assignments_enumerated": max_local_image,
    }


def build_results() -> dict:
    boxes = []
    total_presentations = 0
    dependent_presentations = 0
    free_presentations = 0
    subset_states = 0
    oracle_queries = 0
    maximum_query_slack = 0
    canonical_checks = 0
    hall_checks = 0

    for left_count, right_count in ((3, 2), (4, 2), (3, 3)):
        box_count = box_dependent = 0
        for supports in all_presentations(left_count, right_count):
            circuits = brute_circuits(supports)
            girth = min((len(circuit) for circuit in circuits), default=None)
            oracle = CountingD3GirthOracle(supports)
            extraction = extract_girth_circuit_and_hall_witness(supports, oracle)
            assert extraction.girth == girth
            assert extraction.query_count == oracle.queries
            bound = query_bound(left_count, dependence_guaranteed=False)
            assert extraction.query_count <= bound
            maximum_query_slack = max(maximum_query_slack, bound - extraction.query_count)
            oracle_queries += extraction.query_count
            if girth is None:
                assert extraction.circuit is None
                assert extraction.neighborhood is None
                free_presentations += 1
            else:
                shortest = tuple(circuit for circuit in circuits if len(circuit) == girth)
                expected = canonical_reference(shortest, tuple(range(left_count)))
                assert extraction.circuit == expected
                assert extraction.neighborhood == tuple(
                    sorted({right for left in expected for right in supports[left]})
                )
                assert len(extraction.neighborhood) == girth - 1
                assert is_hall_expanding_through(
                    supports, tuple(range(left_count)), girth - 1
                )
                dependent_presentations += 1
                box_dependent += 1
                canonical_checks += 1
                hall_checks += 1
            box_count += 1
            total_presentations += 1
            subset_states += (1 << left_count) - 1
        boxes.append(
            {
                "left": left_count,
                "right": right_count,
                "presentations": box_count,
                "dependent_presentations": box_dependent,
            }
        )

    local_rows = [
        local_family_audit(((0,), (0,))),
        local_family_audit(((0,), (1,), (0, 1))),
    ]

    path_rows = []
    for length in (4, 6, 8, 10):
        supports = private_path_circuit(length)
        assert brute_girth(supports) == length
        oracle = CountingD3GirthOracle(supports)
        extraction = extract_girth_circuit_and_hall_witness(
            supports, oracle, dependence_guaranteed=True
        )
        assert extraction.girth == length
        assert extraction.circuit == tuple(range(length))
        assert len(extraction.neighborhood or ()) == length - 1
        for threshold in range(1, length):
            assert is_hall_expanding_through(
                supports, tuple(range(length)), threshold
            )
        path_rows.append(
            {
                "length": length,
                "girth": extraction.girth,
                "neighborhood_size": len(extraction.neighborhood or ()),
                "oracle_queries": extraction.query_count,
                "query_bound": query_bound(length, dependence_guaranteed=True),
                "hall_expanding_through": length - 1,
            }
        )

    return {
        "theorem": {
            "name": "FP^NP girth extraction and logarithmic-circuit avoidance",
            "exact_girth_queries": "ceil(log2(m)) when dependence is guaranteed; one extra existence query otherwise",
            "canonical_circuit_queries": "at most m deletion queries",
            "degree_three_promise_preserved": True,
            "short_circuit_local_range_bound": "2^(g-1) out of 2^g projections",
            "hard_branch": "girth > L implies Hall noncontraction for every output set of size at most L",
            "reduction_type": "deterministic FP^NP preprocessing dichotomy / promise reduction, not a many-one solver",
        },
        "exhaustive_extraction_census": {
            "boxes": boxes,
            "presentations_checked": total_presentations,
            "dependent_presentations": dependent_presentations,
            "free_presentations": free_presentations,
            "subset_states_checked": subset_states,
            "oracle_queries_simulated": oracle_queries,
            "canonical_circuits_checked": canonical_checks,
            "hall_witnesses_checked": hall_checks,
            "maximum_query_bound_slack": maximum_query_slack,
        },
        "local_avoidance_census": {
            "families": local_rows,
            "truth_table_combinations": sum(
                row["truth_table_combinations"] for row in local_rows
            ),
            "avoided_outputs_verified": sum(
                row["avoided_outputs_verified"] for row in local_rows
            ),
        },
        "long_circuit_controls": path_rows,
        "complexity_boundary": {
            "small_girth": "if g <= c log2(n+m) for fixed c, local enumeration and lift is polynomial",
            "large_girth": "all output subsets of size at most c log2(n+m) satisfy |N(S)| >= |S|",
            "unrestricted_NC0_3_avoid_solved": False,
            "deterministic_FP_NP_target_solved": False,
            "p_vs_np_resolved": False,
            "novelty_confirmed": False,
        },
    }


if __name__ == "__main__":
    import json

    print(json.dumps(build_results(), indent=2, sort_keys=True))
