#!/usr/bin/env python3
"""V89/V90: exact local second-moment geometry of the seven-state basis CSP."""
from __future__ import annotations

import itertools
import json
import math
from collections import Counter
from fractions import Fraction

VECTORS = tuple(range(1, 8))
ORDERED_BASES = tuple(
    triple
    for triple in itertools.permutations(VECTORS, 3)
    if len(set(triple)) == 3
    and (triple[0] ^ triple[1] ^ triple[2]) != 0
)
BASE_SET = set(ORDERED_BASES)


def first_moment() -> dict:
    probability = Fraction(len(ORDERED_BASES), 7**3)
    upper_density = math.log(7) / math.log(1 / float(probability))
    return {
        "ordered_bases": len(ORDERED_BASES),
        "single_edge_basis_probability": (
            f"{probability.numerator}/{probability.denominator}"
        ),
        "exponential_base_at_density_one": round(
            7 * float(probability), 12
        ),
        "grows_exponentially_at_density_one": 7 * probability > 1,
        "first_moment_upper_density": round(upper_density, 12),
    }


def exact_local_hessian() -> dict:
    """Verify the energy Hessian is (1/6)I on the 36-dim tangent space."""
    size = 49
    uniform = Fraction(1, 7)
    q0 = Fraction(0)
    gradient = [Fraction(0) for _ in range(size)]
    hessian = [
        [Fraction(0) for _ in range(size)] for _ in range(size)
    ]

    zero_based = tuple(
        tuple(value - 1 for value in basis) for basis in ORDERED_BASES
    )
    for left in zero_based:
        for right in zero_based:
            indices = tuple(
                left[position] * 7 + right[position]
                for position in range(3)
            )
            q0 += uniform**3
            for position in range(3):
                gradient[indices[position]] += uniform**2
            for first, second in itertools.combinations(range(3), 2):
                remaining = 3 - first - second
                i, j = indices[first], indices[second]
                hessian[i][j] += uniform
                hessian[j][i] += uniform

    log_hessian = [
        [
            hessian[i][j] / q0
            - gradient[i] * gradient[j] / (q0 * q0)
            for j in range(size)
        ]
        for i in range(size)
    ]

    tangent = []
    for row in range(6):
        for column in range(6):
            vector = [Fraction(0) for _ in range(size)]
            vector[row * 7 + column] = 1
            vector[row * 7 + 6] = -1
            vector[6 * 7 + column] = -1
            vector[6 * 7 + 6] = 1
            tangent.append(vector)

    def bilinear(matrix, left, right):
        return sum(
            left[i] * matrix[i][j] * right[j]
            for i in range(size)
            for j in range(size)
            if left[i] and right[j]
        )

    def inner(left, right):
        return sum(a * b for a, b in zip(left, right))

    mismatches = 0
    for left in tangent:
        for right in tangent:
            if bilinear(log_hessian, left, right) != (
                Fraction(1, 6) * inner(left, right)
            ):
                mismatches += 1

    return {
        "overlap_tangent_dimension": len(tangent),
        "bilinear_pairs_checked": len(tangent) ** 2,
        "identity_mismatches": mismatches,
        "energy_log_hessian_eigenvalue": "1/6",
        "entropy_hessian_eigenvalue": "-1",
        "combined_hessian_eigenvalue": "-1+c/6",
        "uniform_overlap_locally_maximal_for_density_below": 6,
        "quadratic_coefficient": "-(6-c)/12 * ||D||_F^2",
        "strict_quadratic_coefficient_at_density_one": "-5/12",
        "uniform_overlap_polynomial_value": (
            f"{q0.numerator}/{q0.denominator}"
        ),
    }


def permutation_overlap_census() -> dict:
    distribution: Counter[int] = Counter()
    for permutation in itertools.permutations(VECTORS):
        image_count = 0
        for basis in ORDERED_BASES:
            image = tuple(permutation[value - 1] for value in basis)
            if image in BASE_SET:
                image_count += 1
        distribution[image_count] += 1
    return {
        "permutations_checked": math.factorial(7),
        "basis_image_count_distribution": [
            {"basis_images": count, "permutations": multiplicity}
            for count, multiplicity in sorted(distribution.items())
        ],
        "fano_automorphisms": distribution[len(ORDERED_BASES)],
    }


def diagonal_pair_counts() -> dict:
    counts = Counter(
        sum(left[index] == right[index] for index in range(3))
        for left in ORDERED_BASES
        for right in ORDERED_BASES
    )
    return {str(matches): counts[matches] for matches in range(4)}


def diagonal_critical_density(steps: int = 20000) -> dict:
    counts = {
        int(key): value for key, value in diagonal_pair_counts().items()
    }
    probability = Fraction(24, 49)
    best_density = math.inf
    best_parameter = None
    for index in range(1, steps):
        diagonal = (
            Fraction(1, 7)
            + Fraction(6, 7) * Fraction(index, steps)
        )
        off = (1 - diagonal) / 6
        polynomial = sum(
            counts[matches]
            * float(diagonal) ** matches
            * float(off) ** (3 - matches)
            for matches in range(4)
        )
        joint_probability = polynomial / 343.0
        energy = math.log(joint_probability / float(probability**2))
        if energy <= 0:
            continue
        entries = [float(diagonal)] * 7 + [float(off)] * 42
        entropy = -sum(
            value * math.log(value) for value in entries if value
        )
        threshold = (math.log(7) - entropy / 7) / energy
        if threshold < best_density:
            best_density = threshold
            best_parameter = float(diagonal)
    return {
        "steps": steps,
        "ordered_basis_pair_match_counts": diagonal_pair_counts(),
        "minimum_scanned_critical_density": round(best_density, 12),
        "diagonal_parameter_at_minimum": round(
            float(best_parameter), 12
        ),
        "proof_status": "numerical one-dimensional evidence only",
    }


def build_results() -> dict:
    return {
        "laboratory": "V89/V90",
        "module": "seven-state basis-CSP second-moment local geometry",
        "first_moment": first_moment(),
        "overlap_objective": {
            "normalization": "B is 7x7 doubly stochastic and A=B/7",
            "joint_probability": (
                "q(B)=7^-3 sum_{x,y ordered bases} "
                "B[x1,y1] B[x2,y2] B[x3,y3]"
            ),
            "relative_exponent": (
                "Psi_c(B)=H(B)/7-ln(7)+c ln(q(B)/(24/49)^2)"
            ),
            "uniform_value": 0,
        },
        "local_stability": exact_local_hessian(),
        "permutation_boundary": permutation_overlap_census(),
        "diagonal_family": diagonal_critical_density(),
        "scientific_status": {
            "basis7_overlap_objective_exact": True,
            "basis7_uniform_overlap_locally_stable_through_density_six": True,
            "basis7_global_overlap_inequality_proved": False,
            "v87_random_model_basis_colorable_whp": False,
            "support_only_universal_list_lower_bound_nine": False,
        },
        "interpretation": (
            "The seven-state basis CSP has a much larger exact local-stability "
            "margin than the strong-four specialization at density one. The "
            "remaining obstruction is global on the 7x7 Birkhoff polytope."
        ),
        "nonclaims": [
            "Local Hessian stability does not prove the global overlap inequality.",
            "The diagonal scan is not a proof over the continuous polytope.",
            "No asymptotic basis-colorability theorem is claimed.",
            "No nine-row constructor lower bound follows.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(build_results(), indent=2, sort_keys=True))
