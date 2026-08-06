#!/usr/bin/env python3
from __future__ import annotations

import json
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def split2(value: int, n: int) -> tuple[int, int]:
    mask = (1 << n) - 1
    return value >> n, value & mask


def iterate(mapping: tuple[int, ...], root: int, n: int) -> tuple[int, ...]:
    first = split2(mapping[root], n)
    return split2(mapping[first[0]], n) + split2(mapping[first[1]], n)


def first_absent(values: set[int], universe_size: int) -> int:
    for candidate in range(universe_size):
        if candidate not in values:
            return candidate
    raise AssertionError("expected a missing value")


def independent_n1_audit() -> int:
    checked = 0
    for mapping in product(range(4), repeat=2):
        leaf_image = {iterate(mapping, root, 1) for root in range(2)}
        all_leaf_vectors = tuple(product(range(2), repeat=4))
        leaves = next(vector for vector in all_leaf_vectors if vector not in leaf_image)

        level = leaves
        missing = None
        while len(level) > 1 and missing is None:
            parents: list[int] = []
            for index in range(0, len(level), 2):
                target = (level[index] << 1) | level[index + 1]
                preimages = [x for x, value in enumerate(mapping) if value == target]
                if not preimages:
                    missing = target
                    break
                parents.append(min(preimages))
            level = tuple(parents)
        assert missing is not None
        assert missing not in set(mapping)
        checked += 1
    return checked


def expected_missing_string_count(max_n: int) -> int:
    # Number of proper subsets of an n-bit universe, summed over n.
    return sum((1 << (1 << n)) - 1 for n in range(1, max_n + 1))


def main() -> None:
    reproduction = json.loads(
        (ROOT / "REPRODUCTION_RESULTS.json").read_text(encoding="utf-8")
    )
    assert independent_n1_audit() == 16
    assert reproduction["missing_string"]["proper_subsets_checked"] == expected_missing_string_count(4)

    status = json.loads((ROOT.parent / "LAB_STATUS.json").read_text(encoding="utf-8"))
    assert status["promoted_version"] in {"V90", "V91"} or int(status["promoted_version"][1:]) > 91
    if status["candidate_version"] == "V91":
        assert status["highest_directory"] == "V91"
        assert status["promotion_state"] == "candidate"
    assert not status["scientific_status"]["williams_transfer_instantiated"]
    assert not status["scientific_status"]["p_vs_np_resolved"]

    implication = json.loads((ROOT / "IMPLICATION.json").read_text(encoding="utf-8"))
    names = {item["name"]: item["proved"] for item in implication["bridge_lemmas"]}
    assert names["finite Korten/GGM decoding invariant"]
    assert not names["all-instance coverage for a standard circuit class"]
    assert not names["nonalgebrizing ingredient outside the Chen-Hu-Ren barrier scope"]

    results = json.loads((ROOT / "RESULTS.json").read_text(encoding="utf-8"))
    nonclaims = " ".join(results["nonclaims"])
    assert "No new circuit lower bound" in nonclaims
    assert "P versus NP remains unresolved" in nonclaims

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "65,808" in readme
    assert "full CHR/Li algorithm" in readme
    assert "closed **for the inherited width-promised engine**" in readme

    print(
        "V91 independent verification passed: exhaustive n=1 decoding, "
        "closed-form Missing-String count, conservative status, and explicit nonclaims."
    )


if __name__ == "__main__":
    main()
