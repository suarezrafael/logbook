#!/usr/bin/env python3
"""V89: exact second-moment reduction for strong four-coloring."""
from __future__ import annotations

import itertools
import json
import math
from fractions import Fraction
from typing import Iterator, Sequence

Matrix = tuple[tuple[int, int, int, int], ...]


def compositions(total: int, parts: int = 4) -> Iterator[tuple[int, ...]]:
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total - first, parts - 1):
            yield (first,) + tail


def balanced_integer_overlaps(row_sum: int) -> Iterator[Matrix]:
    """All 4x4 nonnegative integer matrices with every margin=row_sum."""
    rows = tuple(compositions(row_sum))
    matrix: list[tuple[int, int, int, int]] = []

    def search(column_sums: tuple[int, int, int, int]) -> Iterator[Matrix]:
        depth = len(matrix)
        if depth == 4:
            if column_sums == (row_sum,) * 4:
                yield tuple(matrix)
            return
        for row in rows:
            updated = tuple(column_sums[j] + row[j] for j in range(4))
            if any(value > row_sum for value in updated):
                continue
            if depth == 3 and updated != (row_sum,) * 4:
                continue
            matrix.append(row)
            yield from search(updated)
            matrix.pop()

    yield from search((0, 0, 0, 0))


def joint_rainbow_probability(overlap: Matrix, row_sum: int) -> Fraction:
    """Probability that an ordered triple is rainbow in both colorings.

    overlap/row_sum is a 4x4 doubly stochastic matrix B. The probability
    matrix for the pair of colors is A=B/4=overlap/(4*row_sum).
    """
    denominator = 4 * row_sum
    total = Fraction(0)
    for first_rows in itertools.permutations(range(4), 3):
        for second_rows in itertools.permutations(range(4), 3):
            product = Fraction(1)
            for left, right in zip(first_rows, second_rows):
                product *= Fraction(overlap[left][right], denominator)
            total += product
    return total


def cubic_formula(overlap: Matrix, row_sum: int) -> Fraction:
    """Closed form q(A)=1/8+4 sum A_ij^3=(2+sum B_ij^3)/16."""
    cubic = sum(
        Fraction(value, row_sum) ** 3
        for row in overlap
        for value in row
    )
    return (Fraction(2) + cubic) / 16


def entropy_of_b(overlap: Matrix, row_sum: int) -> float:
    entropy = 0.0
    for row in overlap:
        for value in row:
            if value:
                probability = value / row_sum
                entropy -= probability * math.log(probability)
    return entropy


def cubic_mass_of_b(overlap: Matrix, row_sum: int) -> Fraction:
    return sum(
        Fraction(value, row_sum) ** 3
        for row in overlap
        for value in row
    )


def relative_second_moment_exponent(
    overlap: Matrix, row_sum: int, density: float
) -> float:
    """Exponent relative to the independent/uniform overlap.

    Phi_c(B)=H(B)/4-ln4+c ln(4(2+sum B^3)/9).
    Uniform B has value zero.
    """
    entropy = entropy_of_b(overlap, row_sum)
    cubic = float(cubic_mass_of_b(overlap, row_sum))
    return (
        entropy / 4
        - math.log(4)
        + density * math.log(4 * (2 + cubic) / 9)
    )


def exact_overlap_identity_census(max_row_sum: int = 3) -> dict:
    by_margin = []
    checked = 0
    for row_sum in range(1, max_row_sum + 1):
        count = 0
        mismatches = 0
        for overlap in balanced_integer_overlaps(row_sum):
            count += 1
            checked += 1
            if joint_rainbow_probability(overlap, row_sum) != cubic_formula(
                overlap, row_sum
            ):
                mismatches += 1
        by_margin.append(
            {
                "row_sum": row_sum,
                "overlap_matrices": count,
                "identity_mismatches": mismatches,
            }
        )
    return {
        "margins": by_margin,
        "overlap_matrices_checked": checked,
        "identity_mismatches": sum(
            row["identity_mismatches"] for row in by_margin
        ),
    }


def rational_grid_census(
    max_row_sum: int = 5,
    densities: Sequence[float] = (1.0, 1.01, 1.02, 1.05),
) -> dict:
    rows = []
    total = 0
    for row_sum in range(1, max_row_sum + 1):
        maxima = {density: -math.inf for density in densities}
        maximizers = {density: 0 for density in densities}
        count = 0
        for overlap in balanced_integer_overlaps(row_sum):
            count += 1
            total += 1
            for density in densities:
                value = relative_second_moment_exponent(
                    overlap, row_sum, density
                )
                if value > maxima[density] + 1e-13:
                    maxima[density] = value
                    maximizers[density] = 1
                elif abs(value - maxima[density]) <= 1e-13:
                    maximizers[density] += 1
        rows.append(
            {
                "row_sum": row_sum,
                "overlap_matrices": count,
                "density_maxima": [
                    {
                        "density": density,
                        "maximum_relative_exponent": round(
                            maxima[density], 15
                        ),
                        "maximizers": maximizers[density],
                        "nonpositive": maxima[density] <= 1e-12,
                    }
                    for density in densities
                ],
            }
        )
    return {
        "rows": rows,
        "overlap_matrices_checked": total,
        "all_grid_maxima_nonpositive": all(
            item["nonpositive"]
            for row in rows
            for item in row["density_maxima"]
        ),
        "warning": (
            "Finite rational grids are evidence only; they do not certify the "
            "continuous Birkhoff-polytope inequality."
        ),
    }


def diagonal_family_matrix(parameter: float) -> tuple[tuple[float, ...], ...]:
    off_diagonal = (1.0 - parameter) / 3.0
    return tuple(
        tuple(
            parameter if row == column else off_diagonal
            for column in range(4)
        )
        for row in range(4)
    )


def diagonal_family_critical_density(steps: int = 10000) -> dict:
    """Deterministic one-dimensional scan of the symmetric overlap family."""
    best_density = math.inf
    best_parameter = None
    for index in range(1, steps):
        parameter = 0.25 + 0.75 * index / steps
        matrix = diagonal_family_matrix(parameter)
        entries = tuple(value for row in matrix for value in row)
        entropy = -sum(value * math.log(value) for value in entries if value)
        cubic = sum(value**3 for value in entries)
        energy_log = math.log(4 * (2 + cubic) / 9)
        if energy_log <= 0:
            continue
        threshold = (math.log(4) - entropy / 4) / energy_log
        if threshold < best_density:
            best_density = threshold
            best_parameter = parameter
    return {
        "steps": steps,
        "minimum_scanned_critical_density": round(best_density, 12),
        "parameter_at_minimum": round(float(best_parameter), 12),
        "interpretation": (
            "Within the diagonal/off-diagonal family, the uniform overlap "
            "remains maximal below the reported scanned density."
        ),
        "proof_status": "numerical one-dimensional evidence",
    }


def local_stability() -> dict:
    """Exact quadratic coefficient around the uniform overlap."""
    return {
        "entropy_quadratic_coefficient": Fraction(-8),
        "energy_log_quadratic_coefficient": Fraction(16, 3),
        "combined_coefficient": "-8 + (16/3)c",
        "uniform_overlap_locally_maximal_for_density_below": Fraction(3, 2),
        "target_density_limit": 1,
        "strict_local_margin_at_density_one": Fraction(8, 3),
    }


def first_moment() -> dict:
    rainbow_probability = Fraction(3, 8)
    base_at_one = 4 * float(rainbow_probability)
    first_moment_upper_density = math.log(4) / math.log(Fraction(8, 3))
    return {
        "balanced_color_classes": 4,
        "single_edge_rainbow_probability": "3/8",
        "exponential_base_at_density_one": round(base_at_one, 12),
        "grows_exponentially_at_density_one": base_at_one > 1,
        "first_moment_upper_density": round(first_moment_upper_density, 12),
    }


def build_strong4_results() -> dict:
    identity = exact_overlap_identity_census()
    grid = rational_grid_census()
    local = local_stability()
    return {
        "laboratory": "V89",
        "module": "strong-four-color second-moment reduction",
        "first_moment": first_moment(),
        "overlap_identity": {
            "formula": "q(A)=1/8+4*sum(A_ij^3)",
            "normalized_formula": "q(B)=(2+sum(B_ij^3))/16",
            "birkhoff_constraints": (
                "B is a nonnegative 4x4 matrix with all row and column sums one"
            ),
            "exact_census": identity,
        },
        "second_moment_objective": {
            "relative_exponent": (
                "Phi_c(B)=H(B)/4-ln(4)+c*ln(4*(2+sum(B_ij^3))/9)"
            ),
            "uniform_value": 0,
            "bridge_sufficient_condition": (
                "For one fixed c0>1, prove Phi_c0(B)<=0 for every 4x4 "
                "doubly stochastic B, with equality only at the uniform matrix."
            ),
            "density_one_equivalent_inequality": (
                "ln(2+sum(B_ij^3))-(1/4)sum(B_ij ln B_ij)<=ln(9)"
            ),
        },
        "local_stability": {
            key: (
                f"{value.numerator}/{value.denominator}"
                if isinstance(value, Fraction)
                else value
            )
            for key, value in local.items()
        },
        "finite_rational_grid": grid,
        "diagonal_family": diagonal_family_critical_density(),
        "scientific_status": {
            "strong4_overlap_identity": True,
            "strong4_second_moment_reduced_to_birkhoff_inequality": True,
            "strong4_uniform_overlap_locally_stable_through_density_three_halves": True,
            "strong4_birkhoff_global_inequality_proved": False,
            "v87_random_model_primal_four_colorable_whp": False,
            "support_only_universal_list_lower_bound_nine": False,
        },
        "nonclaims": [
            "The finite grid is not a proof over the continuous polytope.",
            "Local stability does not imply global maximality.",
            "No strong-four-colorability threshold at r=4 is claimed from the cited large-r literature.",
            "The nine-row constructor lower bound remains open.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(build_strong4_results(), indent=2, sort_keys=True))
