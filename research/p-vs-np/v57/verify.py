#!/usr/bin/env python3
"""Primary exhaustive verifier for Laboratory V57."""
from __future__ import annotations

import itertools
import json
import math
import time
from collections import Counter
from pathlib import Path

import v57_core as core

ROOT = Path(__file__).resolve().parent


def bits(value: int, n: int) -> tuple[int, ...]:
    return tuple((value >> i) & 1 for i in range(n))


def check_boundary_theorem(max_m: int = 4) -> int:
    checks = 0
    for m in range(1, max_m + 1):
        cube = [tuple((x >> i) & 1 for i in range(m)) for x in range(1 << m)]
        for subset_mask in range(1, (1 << (1 << m)) - 1):
            image = {cube[i] for i in range(1 << m) if (subset_mask >> i) & 1}
            point, coordinate = core.boundary_edge(image)
            neighbor = list(point)
            neighbor[coordinate] ^= 1
            assert tuple(neighbor) not in image
            context = point[:coordinate] + point[coordinate + 1:]
            matching = [p for p in image if p[:coordinate] + p[coordinate + 1:] == context]
            assert matching and all(p[coordinate] == point[coordinate] for p in matching)
            checks += 1
    return checks


def explicit_g4_certificate() -> dict:
    orbit = set(core.ORBIT_07)
    assert len(orbit) == 48
    assert all(mask in orbit for mask, _support in core.G4_MASK_SUPPORT)
    assert [f"0x{mask:02x}" for mask, _support in core.G4_MASK_SUPPORT] == [
        "0x51", "0x45", "0x51", "0x45", "0x15"
    ]

    sets = core.gadget_sets(4, core.G4_MASK_SUPPORT)
    common = core.intersection(sets, range(16))
    assert common == {0}
    assert core.redundant_blocks(sets, range(16)) == []
    witnesses = core.irredundancy_witnesses(sets, range(16))
    assert witnesses == list(core.G4_WITNESSES)
    for index, witness in enumerate(witnesses):
        assert witness not in sets[index]
        assert all(witness in sets[j] for j in range(5) if j != index)

    clauses = [clause for block in core.G4_CLAUSE_BLOCKS for clause in block]
    components = core.implication_graph_sccs(4, clauses)
    normalized_components = sorted(
        [sorted([(v, int(sign)) for v, sign in comp]) for comp in components],
        key=lambda comp: (len(comp), comp),
    )
    assert len(components) == 4

    image = core.circuit_image(4, core.G4_MASK_SUPPORT)
    assert len(image) < 32
    assert core.boundary_edge(image) is not None
    forcing_patterns = core.full_context_forcing_patterns(image)
    assert forcing_patterns

    return {
        "n": 4,
        "m": 5,
        "masks": [f"0x{mask:02x}" for mask, _support in core.G4_MASK_SUPPORT],
        "supports": [list(support) for _mask, support in core.G4_MASK_SUPPORT],
        "common_active_assignments": [list(bits(x, 4)) for x in sorted(common)],
        "irredundancy_witnesses": [list(bits(x, 4)) for x in witnesses],
        "implication_graph_scc_count": len(components),
        "implication_graph_sccs": normalized_components,
        "all_variables_forced_by_full_formula": True,
        "redundant_blocks": [],
        "range_size": len(image),
        "full_context_forcing_patterns": len(forcing_patterns),
    }


def exhaustive_n3() -> dict:
    orbit = core.ORBIT_07
    assert len(orbit) == 48
    counts = Counter()
    checked = 0
    for masks in itertools.combinations_with_replacement(orbit, 4):
        sets = [core.small_fiber(mask) for mask in masks]
        common = core.intersection(sets, range(8))
        if not common:
            counts["inconsistent"] += 1
        else:
            redundant = core.redundant_blocks(sets, range(8))
            if redundant:
                counts["consistent_with_redundant_block"] += 1
            else:
                counts["consistent_irredundant"] += 1
        checked += 1
    assert checked == math.comb(48 + 4 - 1, 4) == 249900
    assert counts == Counter({
        "inconsistent": 206280,
        "consistent_with_redundant_block": 43620,
        "consistent_irredundant": 0,
    })
    return {"multisets_checked": checked, **dict(counts)}


def exhaustive_normalized_n4() -> dict:
    blocks = core.normalized_blocks_containing_zero(4)
    assert len(blocks) == 36
    histogram = Counter()
    irredundant_examples = []
    checked = 0
    for family in itertools.combinations(blocks, 5):
        descriptions = [description for description, _block in family]
        sets = [block for _description, block in family]
        redundant = core.redundant_blocks(sets, range(16))
        histogram[len(redundant)] += 1
        if not redundant:
            witnesses = core.irredundancy_witnesses(sets, range(16))
            assert witnesses is not None
            if len(irredundant_examples) < 12:
                irredundant_examples.append({
                    "descriptions": [list(item) for item in descriptions],
                    "witnesses": [list(bits(x, 4)) for x in witnesses],
                })
        checked += 1
    assert checked == math.comb(36, 5) == 376992
    assert histogram == Counter({0: 12, 1: 228, 2: 8088, 3: 87804, 4: 194712, 5: 86148})
    assert len(irredundant_examples) == 12
    return {
        "normalized_blocks": len(blocks),
        "families_checked": checked,
        "redundant_block_count_histogram": {str(k): v for k, v in sorted(histogram.items())},
        "consistent_irredundant_families": histogram[0],
        "examples": irredundant_examples,
    }


def asymptotic_family_checks() -> dict:
    structural = []
    brute_force = []
    for k in range(0, 21):
        n, gates = core.stretch_one_family(k)
        assert len(gates) == n + 1
        assert all(mask in core.ORBIT_07 for mask, _support in gates)
        structural.append({"k": k, "n": n, "m": len(gates)})

    for k in range(0, 4):
        n, gates = core.stretch_one_family(k)
        sets = core.gadget_sets(n, gates)
        common = core.intersection(sets, range(1 << n))
        witnesses = core.irredundancy_witnesses(sets, range(1 << n))
        assert common == {0}
        assert witnesses is not None and len(witnesses) == len(gates)
        assert core.redundant_blocks(sets, range(1 << n)) == []
        brute_force.append({"k": k, "n": n, "m": len(gates), "assignments": 1 << n})
    return {"structural_instances": structural, "brute_force_instances": brute_force}


def main() -> None:
    started = time.perf_counter()
    boundary_checks = check_boundary_theorem(4)
    gadget = explicit_g4_certificate()
    n3 = exhaustive_n3()
    n4 = exhaustive_normalized_n4()
    family = asymptotic_family_checks()

    results = {
        "version": "V57",
        "status": "passed",
        "central_results": {
            "universal_boundary_forcing": True,
            "direct_bijunctive_block_redundancy_false": True,
            "minimal_distinct_support_counterexample": {"n": 4, "m": 5, "orbit": "0x07"},
            "infinite_stretch_one_irredundant_family": "n=4+3k, m=5+3k=n+1",
            "scc_count_rank_surrogate_refuted_by_gadget": True,
        },
        "validation": {
            "proper_cube_subsets_checked": boundary_checks,
            "n3_orbit_multisets": n3,
            "n4_normalized_families": n4,
            "asymptotic_family": family,
            "explicit_gadget": gadget,
            "failures": 0,
        },
        "scientific_status": {
            "peer_reviewed": False,
            "novelty_confirmed": False,
            "prior_art_for_2cnf_redundancy_exists": True,
            "general_nc0_3_avoid_solved": False,
            "p_vs_np_resolved": False,
        },
        "elapsed_seconds": round(time.perf_counter() - started, 6),
    }
    certificates = {
        "explicit_g4": gadget,
        "n3_minimality": n3,
        "n4_exhaustive_histogram": n4["redundant_block_count_histogram"],
        "asymptotic_formula": family["structural_instances"],
    }
    (ROOT / "RESULTS.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    (ROOT / "CERTIFICATES.json").write_text(json.dumps(certificates, indent=2), encoding="utf-8")

    print("V57 primary verification passed:")
    print(f"  {boundary_checks} nonempty proper cube subsets checked for boundary forcing;")
    print("  explicit n=4,m=5 0x07 gadget: consistent, unique common assignment, 0 redundant blocks;")
    print("  249900 n=3,m=4 orbit multisets exhausted; no consistent irredundant family;")
    print("  376992 normalized n=4,m=5 block families exhausted; exactly 12 irredundant;")
    print("  stretch-one direct-product family checked structurally through k=20 and exhaustively through k=3;")
    print("  implication graph has 4 SCCs while all 5 blocks remain essential; zero failures.")


if __name__ == "__main__":
    main()
