#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def version_number(value: str) -> int:
    assert value.startswith("V") and value[1:].isdigit()
    return int(value[1:])


def unions(supports: list[list[int]]) -> list[int]:
    encoded = [sum(1 << variable for variable in support) for support in supports]
    result = [0] * (1 << len(encoded))
    for mask in range(1, 1 << len(encoded)):
        bit = mask & -mask
        result[mask] = result[mask ^ bit] | encoded[bit.bit_length() - 1]
    return result


def matching_rank(supports: list[list[int]], mask: int) -> int:
    variable_count = 1 + max(
        (variable for support in supports for variable in support),
        default=-1,
    )
    matched = [-1] * variable_count

    def search(gate: int, seen: set[int]) -> bool:
        for variable in supports[gate]:
            if variable in seen:
                continue
            seen.add(variable)
            if matched[variable] == -1 or search(matched[variable], seen):
                matched[variable] = gate
                return True
        return False

    answer = 0
    for gate in range(len(supports)):
        if (mask >> gate) & 1 and search(gate, set()):
            answer += 1
    return answer


def circuits(supports: list[list[int]]) -> list[int]:
    result: list[int] = []
    for mask in range(1, 1 << len(supports)):
        if matching_rank(supports, mask) == mask.bit_count():
            continue
        if all(
            matching_rank(supports, mask ^ (1 << gate))
            == mask.bit_count() - 1
            for gate in range(len(supports))
            if (mask >> gate) & 1
        ):
            result.append(mask)
    return result


def independently_audit(
    supports: list[list[int]], committed: dict[str, object]
) -> int:
    neighborhood = unions(supports)
    dependent = [
        mask
        for mask in range(1, 1 << len(supports))
        if neighborhood[mask].bit_count() < mask.bit_count()
    ]
    hstar = min(neighborhood[mask].bit_count() for mask in dependent)
    hstar_minimizers = [
        mask for mask in dependent if neighborhood[mask].bit_count() == hstar
    ]
    minimal = [
        mask
        for mask in hstar_minimizers
        if not any(
            other != mask and (other & mask) == other
            for other in hstar_minimizers
        )
    ]
    circuit_masks = circuits(supports)
    girth = min(mask.bit_count() for mask in circuit_masks)

    assert hstar == girth - 1
    assert hstar == committed["minimum_hall_neighborhood"]
    assert girth == committed["transversal_girth"]
    assert len(hstar_minimizers) == committed["hstar_minimizer_count"]
    assert len(minimal) == committed[
        "inclusion_minimal_hstar_minimizer_count"
    ]
    assert all(
        mask.bit_count() - neighborhood[mask].bit_count() == 1
        for mask in minimal
    )
    assert len(circuit_masks) == committed["total_circuit_count"]
    assert matching_rank(supports, (1 << len(supports)) - 1) == committed[
        "transversal_rank"
    ]
    return 1 << len(supports)


def main() -> None:
    data = json.loads((HERE / "RESULTS.json").read_text(encoding="utf-8"))
    v80 = json.loads((ROOT / "v80" / "RESULTS.json").read_text(encoding="utf-8"))
    total = 0
    for name, row in data["v80_rank_three_census"].items():
        total += independently_audit(v80["examples"][name]["supports"], row)

    controls = {
        "theta_three_parallel_edges": [[0, 1], [0, 1], [0, 1]],
        "tight_handcuff_two_loops": [[0], [0]],
        "loose_handcuff_two_loops_bridge": [[0], [0, 1], [1]],
    }
    for name, supports in controls.items():
        independently_audit(supports, data["degree_two_controls"][name])

    assert total == 22528
    map_ = data["literature_map"]
    assert map_["general_transversal_girth"]["status"] == "NP-hard"
    assert map_["parameterized_girth"]["useful_for_target_regime"] is False
    assert map_["left_degree_three"][
        "polynomial_time_known_from_located_sources"
    ] is False
    assert map_["left_degree_three"][
        "np_hardness_known_from_located_sources"
    ] is False

    status = json.loads((ROOT / "LAB_STATUS.json").read_text(encoding="utf-8"))
    promoted = status["promoted_version"]
    candidate = status.get("candidate_version")
    assert version_number(promoted) >= 82
    if candidate is None:
        assert status["highest_directory"] == promoted
        assert status["promotion_state"] == "promoted"
    else:
        assert version_number(candidate) == version_number(promoted) + 1
        assert status["highest_directory"] == candidate
        assert status["promotion_state"] == "candidate"
    assert status["scientific_status"]["p_vs_np_resolved"] is False
    assert status["scientific_status"][
        "degree_three_transversal_girth_polynomial_time"
    ] is None
    assert status["scientific_status"][
        "degree_three_transversal_girth_np_hard"
    ] is None

    print(
        f"V82 independent verification passed: {total} rank-three subset "
        "states plus degree-two bicircular controls independently checked; "
        "the degree-three complexity boundary remains open."
    )


if __name__ == "__main__":
    main()
