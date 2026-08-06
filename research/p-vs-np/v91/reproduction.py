#!/usr/bin/env python3
"""Finite executable audit of the Korten/GGM decoding kernel used by CHR/Li.

This is deliberately not an implementation of the full single-valued FS2P
algorithm.  It exhaustively checks the deterministic decoding invariant on
small expanding maps and separately checks the Missing-String search model.
"""
from __future__ import annotations

import json
from itertools import combinations, product
from pathlib import Path
from typing import Iterable, Sequence

ROOT = Path(__file__).resolve().parent


def split_word(word: int, n: int) -> tuple[int, int]:
    mask = (1 << n) - 1
    return word >> n, word & mask


def join_word(left: int, right: int, n: int) -> int:
    return (left << n) | right


def ggm_leaves(mapping: Sequence[int], root: int, n: int, height: int) -> tuple[int, ...]:
    level = (root,)
    for _ in range(height):
        children: list[int] = []
        for value in level:
            children.extend(split_word(mapping[value], n))
        level = tuple(children)
    return level


def lex_first_preimage(mapping: Sequence[int], target: int) -> int | None:
    for x, value in enumerate(mapping):
        if value == target:
            return x
    return None


def decode_korten(mapping: Sequence[int], leaves: Sequence[int], n: int) -> int:
    """Return a value outside Im(mapping), using bottom-up lex-first decoding."""
    level = tuple(leaves)
    assert level and (len(level) & (len(level) - 1)) == 0
    while len(level) > 1:
        parents: list[int] = []
        for index in range(0, len(level), 2):
            target = join_word(level[index], level[index + 1], n)
            preimage = lex_first_preimage(mapping, target)
            if preimage is None:
                return target
            parents.append(preimage)
        level = tuple(parents)
    raise AssertionError("a purported non-image leaf vector decoded to a root")


def encode_leaves(leaves: Sequence[int], n: int) -> int:
    value = 0
    for leaf in leaves:
        value = (value << n) | leaf
    return value


def decode_leaves(value: int, n: int, count: int) -> tuple[int, ...]:
    mask = (1 << n) - 1
    leaves = [0] * count
    for index in range(count - 1, -1, -1):
        leaves[index] = value & mask
        value >>= n
    return tuple(leaves)


def lex_first_missing_ggm(mapping: Sequence[int], n: int, height: int) -> tuple[int, ...]:
    leaf_count = 1 << height
    image = {
        encode_leaves(ggm_leaves(mapping, root, n, height), n)
        for root in range(1 << n)
    }
    for encoded in range(1 << (n * leaf_count)):
        if encoded not in image:
            return decode_leaves(encoded, n, leaf_count)
    raise AssertionError("expanding GGM map unexpectedly surjective")


def all_maps_n1() -> Iterable[tuple[int, ...]]:
    return product(range(4), repeat=2)


def sampled_maps_n2() -> Iterable[tuple[int, ...]]:
    # Deterministic sample with collisions, permutations, and mixed images.
    for seed in range(64):
        state = (seed + 1) * 0x9E3779B1
        values: list[int] = []
        for x in range(4):
            state = (1664525 * (state ^ (x * 0x45D9F3B)) + 1013904223) & 0xFFFFFFFF
            values.append((state >> 12) & 0xF)
        yield tuple(values)


def audit_korten_family(maps: Iterable[Sequence[int]], n: int, height: int) -> dict[str, int]:
    checked = 0
    for mapping in maps:
        assert len(mapping) == 1 << n
        assert all(0 <= value < (1 << (2 * n)) for value in mapping)
        leaves = lex_first_missing_ggm(mapping, n, height)
        image = {ggm_leaves(mapping, root, n, height) for root in range(1 << n)}
        assert tuple(leaves) not in image
        missing = decode_korten(mapping, leaves, n)
        assert missing not in set(mapping)
        checked += 1
    return {"maps_checked": checked, "height": height, "n": n}


def lex_first_missing_string(strings: Sequence[int], n: int) -> int:
    present = set(strings)
    for candidate in range(1 << n):
        if candidate not in present:
            return candidate
    raise ValueError("Missing-String requires fewer than 2^n distinct strings")


def audit_missing_string(max_n: int = 4) -> dict[str, int]:
    instances = 0
    for n in range(1, max_n + 1):
        universe = range(1 << n)
        # Every proper subset is a canonical set-valued instance.
        for size in range(1 << n):
            for subset in combinations(universe, size):
                answer = lex_first_missing_string(subset, n)
                assert answer not in subset
                assert all(value in subset for value in range(answer))
                instances += 1
    return {"max_n": max_n, "proper_subsets_checked": instances}


def build_results() -> dict[str, object]:
    n1 = audit_korten_family(all_maps_n1(), n=1, height=2)
    n2 = audit_korten_family(sampled_maps_n2(), n=2, height=2)
    missing = audit_missing_string(max_n=4)
    return {
        "laboratory": "V91",
        "reproduction_scope": "finite Korten/GGM decoding kernel, not the full CHR/Li FS2P algorithm",
        "korten_ggm": {"exhaustive_n1": n1, "deterministic_sample_n2": n2},
        "missing_string": missing,
        "checks": {
            "lexicographic_preimages": True,
            "nonimage_leaf_vector": True,
            "decoded_output_outside_original_range": True,
            "canonical_missing_string_output": True,
        },
    }


def main() -> None:
    results = build_results()
    output = ROOT / "REPRODUCTION_RESULTS.json"
    output.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        "V91 reproduction passed: "
        f"Korten maps={results['korten_ggm']['exhaustive_n1']['maps_checked'] + results['korten_ggm']['deterministic_sample_n2']['maps_checked']}; "
        f"Missing-String subsets={results['missing_string']['proper_subsets_checked']}."
    )


if __name__ == "__main__":
    main()
