#!/usr/bin/env python3
"""Independent V89 strong-four overlap audit."""
from __future__ import annotations

import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def rows(total: int, parts: int = 4):
    if parts == 1:
        yield (total,)
        return
    for head in range(total + 1):
        for tail in rows(total - head, parts - 1):
            yield (head,) + tail


def tables(margin: int):
    choices = tuple(rows(margin))
    chosen = []

    def visit(columns):
        depth = len(chosen)
        if depth == 4:
            if columns == (margin,) * 4:
                yield tuple(chosen)
            return
        for row in choices:
            next_columns = tuple(columns[j] + row[j] for j in range(4))
            if any(value > margin for value in next_columns):
                continue
            if depth == 3 and next_columns != (margin,) * 4:
                continue
            chosen.append(row)
            yield from visit(next_columns)
            chosen.pop()

    yield from visit((0, 0, 0, 0))


def direct_q(table, margin):
    denominator = 4 * margin
    answer = Fraction(0)
    for left in itertools.permutations(range(4), 3):
        for right in itertools.permutations(range(4), 3):
            term = Fraction(1)
            for i, j in zip(left, right):
                term *= Fraction(table[i][j], denominator)
            answer += term
    return answer


def closed_q(table, margin):
    cubic = sum(
        Fraction(value, margin) ** 3
        for row in table
        for value in row
    )
    return (2 + cubic) / 16


def exponent(table, margin, density):
    entropy = 0.0
    cubic = 0.0
    for row in table:
        for value in row:
            if value:
                b = value / margin
                entropy -= b * math.log(b)
                cubic += b**3
    return entropy / 4 - math.log(4) + density * math.log(
        4 * (2 + cubic) / 9
    )


def main():
    committed = json.loads(
        (ROOT / "STRONG4_RESULTS.json").read_text(encoding="utf-8")
    )

    identity_count = 0
    for margin in (1, 2):
        for table in tables(margin):
            assert direct_q(table, margin) == closed_q(table, margin)
            identity_count += 1
    assert identity_count == 306

    grid_count = 0
    for margin in (1, 2, 3, 4):
        best_one = -math.inf
        best_margin = -math.inf
        for table in tables(margin):
            best_one = max(best_one, exponent(table, margin, 1.0))
            best_margin = max(best_margin, exponent(table, margin, 1.05))
            grid_count += 1
        assert best_one <= 1e-12
        assert best_margin <= 1e-12
    assert grid_count == 12461

    local = committed["local_stability"]
    assert local["entropy_quadratic_coefficient"] == "-8/1"
    assert local["energy_log_quadratic_coefficient"] == "16/3"
    assert (
        local["uniform_overlap_locally_maximal_for_density_below"]
        == "3/2"
    )

    status = committed["scientific_status"]
    assert status["strong4_overlap_identity"]
    assert status["strong4_second_moment_reduced_to_birkhoff_inequality"]
    assert status[
        "strong4_uniform_overlap_locally_stable_through_density_three_halves"
    ]
    assert not status["strong4_birkhoff_global_inequality_proved"]
    assert not status["support_only_universal_list_lower_bound_nine"]

    print(
        "V89 independent strong-four audit passed: 306 exact overlap "
        "identities, 12,461 rational-grid overlaps, and exact local "
        "stability coefficients."
    )


if __name__ == "__main__":
    main()
