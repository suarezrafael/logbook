#!/usr/bin/env python3
"""Standalone finite verifier for the V20 research note.

This script independently checks the 30-function taxonomy, coordinatewise
complement normalization, and representative certificates for threshold,
GF(2), and both GF(3) modes. The full 342-case suite is preserved in the
laboratory package; this repository verifier is intentionally compact.
"""

from __future__ import annotations

import itertools
import json


def complement(bits):
    return tuple(1 - bit for bit in bits)


def nondecreasing(bits):
    return all(bits[i] <= bits[i + 1] for i in range(len(bits) - 1))


def parity_truth(arity):
    return tuple(weight & 1 for weight in range(arity + 1))


def exact_mod3(residue):
    return tuple(int(weight % 3 == residue) for weight in range(4))


def classify(truth):
    truth = tuple(truth)
    inverse = complement(truth)
    if len(set(truth)) == 1:
        return "CONSTANT", 0, truth
    if nondecreasing(truth):
        return "THRESHOLD", 0, truth
    if nondecreasing(inverse):
        return "THRESHOLD", 1, inverse
    odd = parity_truth(len(truth) - 1)
    if truth == odd:
        return "PARITY", 0, truth
    if inverse == odd:
        return "PARITY", 1, inverse
    if len(truth) == 4:
        for residue in range(3):
            exact = exact_mod3(residue)
            if truth == exact:
                return "MOD3_INDICATOR", 0, truth
            if inverse == exact:
                return "MOD3_INDICATOR", 1, inverse
    raise AssertionError(f"unclassified: {truth}")


def gate_value(variables, truth, assignment):
    weight = sum((assignment >> variable) & 1 for variable in variables)
    return truth[weight]


def image(inputs, gates):
    return {
        tuple(gate_value(variables, truth, assignment) for variables, truth in gates)
        for assignment in range(1 << inputs)
    }


def taxonomy_check():
    counts = {}
    for arity in range(4):
        for mask in range(1 << (arity + 1)):
            truth = tuple((mask >> weight) & 1 for weight in range(arity + 1))
            family, _, _ = classify(truth)
            counts[family] = counts.get(family, 0) + 1
    expected = {
        "CONSTANT": 8,
        "THRESHOLD": 12,
        "PARITY": 4,
        "MOD3_INDICATOR": 6,
    }
    assert counts == expected, (counts, expected)
    return counts


def certificate_examples():
    # Threshold: duplicate coordinates cannot disagree.
    majority = (0, 0, 1, 1)
    threshold_gates = [((0, 1, 2), majority), ((0, 1, 2), majority)]
    assert (0, 1) not in image(3, threshold_gates)

    # GF(2): rows 110, 011, 101 sum to zero, so output parity is even.
    xor2 = (0, 1, 0)
    parity_gates = [
        ((0, 1), xor2),
        ((1, 2), xor2),
        ((0, 2), xor2),
    ]
    assert (0, 0, 1) not in image(3, parity_gates)

    # GF(3), one-violation mode: identical equations have identical indicators.
    residue0 = exact_mod3(0)
    one_violation = [((0, 1, 2), residue0), ((0, 1, 2), residue0)]
    assert (1, 0) not in image(3, one_violation)

    # GF(3), inconsistent all-ones mode: the same row cannot equal two residues.
    residue1 = exact_mod3(1)
    inconsistent = [((0, 1, 2), residue0), ((0, 1, 2), residue1)]
    assert (1, 1) not in image(3, inconsistent)

    # Coordinatewise complement normalization preserves avoidance.
    complemented = [
        (variables, complement(truth))
        for variables, truth in inconsistent
    ]
    assert (0, 0) not in image(3, complemented)

    return {
        "threshold_duplicate": True,
        "parity_left_null": True,
        "mod3_one_violation": True,
        "mod3_inconsistent_all_ones": True,
        "coordinatewise_complement": True,
    }


def main():
    result = {
        "taxonomy": taxonomy_check(),
        "representative_certificates": certificate_examples(),
        "status": "verified",
        "scientific_caution": (
            "Finite verification is not peer review and does not establish "
            "priority or resolve P versus NP."
        ),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
