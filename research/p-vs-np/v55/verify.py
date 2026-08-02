#!/usr/bin/env python3
from __future__ import annotations

import itertools
import json
import random
from pathlib import Path

import v55_core as c

ROOT = Path(__file__).resolve().parent
SEED = 550055


def gate(rng, n, orbit):
    return {"mask": rng.choice(orbit), "support": tuple(rng.sample(range(n), 3))}


def main():
    rng = random.Random(SEED)
    classes = c.classify_npn_classes()
    assert len(classes) == 14 and sum(row["orbit_size"] for row in classes) == 256
    assert [row["canonical_int"] for row in classes] == [
        0x00,
        0x01,
        0x03,
        0x06,
        0x07,
        0x0F,
        0x16,
        0x17,
        0x18,
        0x19,
        0x1B,
        0x1E,
        0x3C,
        0x69,
    ]
    affine = [
        row["canonical_int"]
        for row in classes
        if row["has_affine_orientation"] and row["essential_arity"] == 3
    ]
    nonaffine = [
        row["canonical_int"]
        for row in classes
        if not row["has_affine_orientation"] and row["essential_arity"] == 3
    ]
    affine_orientable_classes = sum(row["has_affine_orientation"] for row in classes)
    assert affine == [0x01, 0x06, 0x18, 0x69]
    assert nonaffine == list(c.NONAFFINE_ESSENTIAL_CANONICALS)
    assert affine_orientable_classes == 8

    orbit18 = c.npn_orbit(0x18)
    assert len(orbit18) == 8
    for mask in orbit18:
        info = c.oriented_affine_fiber(mask)
        assert info and len(info["points"]) == 2
        assert info["points"][0] ^ info["points"][1] == 7
        for support in itertools.combinations(range(5), 3):
            block = c.gate_affine_block(mask, support, 5)
            assert all(c.antipodal_row_invariant(row, 5) for row in block["rows"])

    histogram = {}
    exhaustive = 0
    for masks in itertools.product(orbit18, repeat=4):
        gates = [{"mask": mask, "support": (0, 1, 2)} for mask in masks]
        cert = c.affine_block_certificate(3, gates, 3)
        assert cert["global_row_rank"] <= 3
        assert c.verify_affine_certificate(3, gates, cert, True)
        degree = cert["separator_degree_bound"]
        histogram[degree] = histogram.get(degree, 0) + 1
        exhaustive += 1

    random_antipodal = 0
    for n in range(4, 13):
        for _ in range(40):
            gates = [gate(rng, n, orbit18) for _ in range(n + 1)]
            cert = c.affine_block_certificate(n, gates, n)
            assert cert["global_row_rank"] <= n
            assert c.verify_affine_certificate(n, gates, cert, True)
            random_antipodal += 1

    affine_masks = tuple(
        sorted({mask for canonical in c.AFFINE_CANONICALS for mask in c.npn_orbit(canonical)})
    )
    mixed = 0
    for n in range(3, 11):
        for _ in range(35):
            gates = [gate(rng, n, affine_masks) for _ in range(n + 2)]
            cert = c.affine_block_certificate(n, gates, n + 1)
            assert cert["global_row_rank"] <= n + 1
            assert c.verify_affine_certificate(n, gates, cert, True)
            mixed += 1

    orbit06 = c.npn_orbit(0x06)
    distance_two = 0
    for n in range(3, 11):
        for _ in range(20):
            gates = [gate(rng, n, orbit06) for _ in range(n + 2)]
            cert = c.affine_block_certificate(n, gates, n + 1)
            assert c.verify_affine_certificate(n, gates, cert, True)
            distance_two += 1

    orbit69 = c.npn_orbit(0x69)
    parity = 0
    for n in range(3, 13):
        for _ in range(25):
            gates = [gate(rng, n, orbit69) for _ in range(n + 1)]
            cert = c.parity3_certificate(n, gates)
            assert c.target_is_absent(n, gates, cert["target"])
            parity += 1

    abstract = 0
    for dimension in range(1, 12):
        for _ in range(50):
            blocks = [
                {
                    "rows": tuple(
                        c.xor_basis(
                            rng.randrange(1 << dimension)
                            for _ in range(rng.randrange(1, 4))
                        )
                    )
                }
                for _ in range(dimension + 1)
            ]
            assert c.redundant_block(blocks) is not None
            abstract += 1

    computed = {
        "version": "V55",
        "status": "passed",
        "seed": SEED,
        "theorems": {
            "general_affine_fiber_threshold": "m>n+1",
            "antipodal_pair_threshold": "m>n",
            "antipodal_canonical_mask": "0x18",
            "antipodal_orbit_size": 8,
            "parity3_threshold": "m>n",
            "remaining_nonaffine_essential_classes": [
                f"0x{x:02x}" for x in c.NONAFFINE_ESSENTIAL_CANONICALS
            ],
        },
        "classification": {
            "boolean_functions": 256,
            "npn_classes": 14,
            "affine_orientable_classes": affine_orientable_classes,
            "essential_affine_classes": [f"0x{x:02x}" for x in affine],
            "essential_nonaffine_classes": [f"0x{x:02x}" for x in nonaffine],
        },
        "validation": {
            "exhaustive_antipodal_n3_m4": exhaustive,
            "random_antipodal_stretch_one": random_antipodal,
            "random_mixed_affine_n_plus_2": mixed,
            "distance_two_pair_n_plus_2": distance_two,
            "parity3_stretch_one": parity,
            "abstract_block_subspace_cases": abstract,
            "failures": 0,
        },
        "constructed_separator_degree_histogram_n3": {
            str(key): value for key, value in sorted(histogram.items())
        },
        "scientific_status": {
            "peer_reviewed": False,
            "novelty_confirmed": False,
            "general_nc0_3_avoid_solved": False,
            "p_vs_np_resolved": False,
        },
    }

    committed = json.loads((ROOT / "RESULTS.json").read_text(encoding="utf-8"))
    for key in ("version", "status", "seed", "theorems", "classification"):
        assert committed[key] == computed[key], key
    for key, value in computed["validation"].items():
        assert committed["validation"][key] == value, key
    assert committed["validation"]["saved_certificates"] == 19
    assert committed["constructed_separator_degree_histogram_n3"] == computed[
        "constructed_separator_degree_histogram_n3"
    ]
    assert committed["scientific_status"] == computed["scientific_status"]

    print("V55 primary verification passed:")
    print("  14/14 ternary NPN classes classified;")
    print(f"  {exhaustive} exhaustive antipodal-pair stretch-one circuits;")
    print(f"  {random_antipodal} random antipodal-pair stretch-one circuits;")
    print(f"  {mixed} mixed affine-fiber n+2 circuits;")
    print(f"  {distance_two} distance-two-pair n+2 circuits;")
    print(f"  {parity} parity3 stretch-one circuits;")
    print(f"  {abstract} abstract block-subspace regressions; zero failures;")
    print("  committed RESULTS.json matches recomputed invariant fields without rewriting.")


if __name__ == "__main__":
    main()
