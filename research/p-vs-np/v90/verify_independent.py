#!/usr/bin/env python3
"""Independent V90 audit without importing the result generator."""
from __future__ import annotations

import itertools
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
V = tuple(range(1, 8))
U = Fraction(1, 7)


def rank_three(columns: tuple[int, int, int]) -> bool:
    span = {0}
    for column in columns:
        span |= {value ^ column for value in tuple(span)}
    return len(span) == 8


def bases() -> tuple[tuple[int, int, int], ...]:
    return tuple(
        triple for triple in itertools.product(V, repeat=3) if rank_three(triple)
    )


def q_value(matrix, ordered_bases) -> Fraction:
    total = Fraction(0)
    for left in ordered_bases:
        for right in ordered_bases:
            total += (
                matrix[left[0] - 1][right[0] - 1]
                * matrix[left[1] - 1][right[1] - 1]
                * matrix[left[2] - 1][right[2] - 1]
            )
    return total / 343


def tangent_basis():
    result = []
    for row in range(6):
        for column in range(6):
            matrix = [[Fraction(0) for _ in V] for _ in V]
            matrix[row][column] = 1
            matrix[row][6] = -1
            matrix[6][column] = -1
            matrix[6][6] = 1
            result.append(matrix)
    return result


def inner(left, right):
    return sum(
        left[i][j] * right[i][j] for i in range(7) for j in range(7)
    )


def pair_component(left, right, ordered_bases, probability):
    count = sum(
        1
        for basis in ordered_bases
        if basis[0] == left and basis[1] == right
    )
    return Fraction(count, 7) - probability


def independent_quadratic_audit(ordered_bases, probability):
    h = [
        [
            pair_component(i + 1, j + 1, ordered_bases, probability)
            for j in range(7)
        ]
        for i in range(7)
    ]
    tangent = tangent_basis()

    def bilinear(left, right):
        total = Fraction(0)
        for x1 in range(7):
            for x2 in range(7):
                for y1 in range(7):
                    if not left[x1][y1]:
                        continue
                    for y2 in range(7):
                        if right[x2][y2]:
                            total += (
                                left[x1][y1]
                                * right[x2][y2]
                                * h[x1][x2]
                                * h[y1][y2]
                            )
        return total / 49

    target = Fraction(16, 2401)
    mismatches = 0
    for left in tangent:
        for right in tangent:
            if bilinear(left, right) != target * inner(left, right):
                mismatches += 1
    return mismatches


def diagonal_family_audit(ordered_bases):
    checked = 0
    for numerator in range(1, 20):
        alpha = Fraction(numerator, 20)
        beta = (1 - alpha) / 6
        matrix = [
            [alpha if i == j else beta for j in range(7)]
            for i in range(7)
        ]
        direct = q_value(matrix, ordered_bases)
        formula = (
            91 * alpha**3
            + 33 * alpha**2
            - 15 * alpha
            + 107
        ) / 441
        assert direct == formula
        checked += 1
    return checked


def main() -> None:
    ordered_bases = bases()
    assert len(ordered_bases) == 168
    probability = Fraction(len(ordered_bases), 7**3)
    assert probability == Fraction(24, 49)

    diagonal = pair_component(1, 1, ordered_bases, probability)
    off = pair_component(1, 2, ordered_bases, probability)
    assert diagonal == Fraction(-24, 49)
    assert off == Fraction(4, 49)

    one_pair_norm = sum(
        pair_component(i, j, ordered_bases, probability) ** 2
        for i in V
        for j in V
    ) / 49
    assert one_pair_norm == Fraction(96, 2401)
    variance = probability * (1 - probability)
    assert variance == Fraction(600, 2401)
    assert 3 * one_pair_norm == Fraction(288, 2401)
    assert variance - 3 * one_pair_norm == Fraction(312, 2401)

    assert independent_quadratic_audit(ordered_bases, probability) == 0
    assert diagonal_family_audit(ordered_bases) == 19

    radius = Fraction(1, 5)
    density = Fraction(21, 20)
    entropy = 1 / (2 * (1 + 7 * radius))
    energy = Fraction(1, 12) + Fraction(13, 24) * radius
    margin = entropy - density * energy
    assert entropy == Fraction(5, 24)
    assert energy == Fraction(23, 120)
    assert margin == Fraction(17, 2400) > 0

    committed = json.loads((ROOT / "RESULTS.json").read_text(encoding="utf-8"))
    assert committed["local_certificate"]["strict_margin_coefficient"] == "17/2400"
    assert not committed["remaining_gap"]["global_entropy_contraction_proved"]

    implication = json.loads(
        (ROOT / "IMPLICATION.json").read_text(encoding="utf-8")
    )
    assert implication["stop_rule_fired"]
    assert implication["classification"] == "barrier_and_closure"
    assert not implication["recognized_frontier_implication"]

    status = json.loads(
        (ROOT.parent / "LAB_STATUS.json").read_text(encoding="utf-8")
    )
    assert status["candidate_version"] == "V90"
    assert status["scientific_status"]["eval_h_constructor_front_closed_after_v90"]

    print(
        "V90 independent verification passed: 168 bases, exact Hoeffding norms, "
        "1,296 independent tangent checks, 19 invariant-family identities, "
        "the radius-1/5 margin, and the fired Eval_H stop rule."
    )


if __name__ == "__main__":
    main()
