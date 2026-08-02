#!/usr/bin/env python3
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def masks(supports: list[list[int]]) -> tuple[int, ...]:
    return tuple(sum(1 << variable for variable in support) for support in supports)


def independent_profiles(supports: list[list[int]]) -> tuple[list[int], list[int]]:
    encoded = masks(supports)
    count = len(encoded)
    full = (1 << count) - 1
    unions = [0] * (1 << count)
    for mask in range(1, 1 << count):
        low = mask & -mask
        index = low.bit_length() - 1
        unions[mask] = unions[mask - low] | encoded[index]
    cuts = [
        (unions[mask] & unions[full ^ mask]).bit_count()
        for mask in range(1 << count)
    ]
    return unions, cuts


def independent_branchwidth(supports: list[list[int]]) -> int:
    _unions, cuts = independent_profiles(supports)
    full = (1 << len(supports)) - 1

    @lru_cache(maxsize=None)
    def solve(mask: int) -> int:
        if mask & (mask - 1) == 0:
            return cuts[mask]
        anchor = mask & -mask
        answer = 10**9
        subset = (mask - 1) & mask
        while subset:
            if subset & anchor and subset != mask:
                answer = min(answer, max(cuts[mask], solve(subset), solve(mask ^ subset)))
            subset = (subset - 1) & mask
        return answer

    return solve(full)


def main() -> None:
    data = json.loads((HERE / "RESULTS.json").read_text(encoding="utf-8"))
    total_subsets = 0
    for example in data["examples"].values():
        supports = example["supports"]
        gate_count = int(example["m"])
        variable_count = int(example["n"])
        full = (1 << gate_count) - 1
        unions, cuts = independent_profiles(supports)

        active = unions[full].bit_count()
        assert active == variable_count
        minimum = min(
            mask.bit_count()
            for mask in range(1, 1 << gate_count)
            if unions[mask].bit_count() < mask.bit_count()
        )
        assert minimum == example["minimum_hall_deficient_gate_count"]
        assert independent_branchwidth(supports) == example["support_branchwidth"]

        for mask in range(1, full):
            complement = full ^ mask
            assert cuts[mask] == (
                unions[mask].bit_count() + unions[complement].bit_count() - active
            )
            if (
                unions[mask].bit_count() >= mask.bit_count()
                and unions[complement].bit_count() >= complement.bit_count()
            ):
                assert cuts[mask] >= gate_count - active
        total_subsets += full - 1

    barrier = data["probabilistic_barrier"]
    assert barrier["bad_event_geometric_base"] == [1, 8]
    assert barrier["bad_event_sum_upper_bound"] == [8, 49]

    status = json.loads((ROOT / "LAB_STATUS.json").read_text(encoding="utf-8"))
    assert status["promoted_version"] == "V80"
    candidate = status.get("candidate_version")
    if candidate is None:
        assert status["highest_directory"] == "V80"
        assert status["promotion_state"] == "promoted"
    else:
        assert candidate == "V81"
        assert status["highest_directory"] == "V81"
        assert status["promotion_state"] == "candidate"
    assert status["next_laboratory_version"] == "V81"
    assert status["scientific_status"]["p_vs_np_resolved"] is False
    assert status["scientific_status"]["p_vs_np_route_active"] is False

    audit = (HERE / "HIGH_WIDTH_DICHOTOMY_AUDIT.md").read_text(encoding="utf-8")
    assert "randomized expected-polynomial" in audit
    assert "does not close the deterministic" in audit
    assert "The third outcome is not failure" in audit
    assert "does not assert high branchwidth for every such family" in audit

    print(
        f"V80 independent verification passed: {total_subsets} nontrivial subset cuts "
        "checked, exact branchwidth recomputed independently, deterministic versus "
        "randomized oracle boundaries preserved, and V80 remains promoted."
    )


if __name__ == "__main__":
    main()
