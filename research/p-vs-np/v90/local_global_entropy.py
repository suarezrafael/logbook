#!/usr/bin/env python3
"""V90: exact Hoeffding geometry and a finite local entropy certificate."""
from __future__ import annotations

import itertools
import json
from fractions import Fraction

VECTORS = tuple(range(1, 8))
TRIPLES = tuple(itertools.product(VECTORS, repeat=3))
ORDERED_BASES = tuple(
    triple
    for triple in TRIPLES
    if len(set(triple)) == 3 and (triple[0] ^ triple[1] ^ triple[2]) != 0
)
P = Fraction(24, 49)
P2 = P * P


def is_basis(triple: tuple[int, int, int]) -> bool:
    return len(set(triple)) == 3 and (triple[0] ^ triple[1] ^ triple[2]) != 0


def pair_component(left: int, right: int) -> Fraction:
    satisfying = sum(is_basis((left, right, third)) for third in VECTORS)
    return Fraction(satisfying, 7) - P


def hoeffding_data() -> dict:
    pair_values = {
        "diagonal": pair_component(1, 1),
        "off_diagonal": pair_component(1, 2),
    }
    pair_norm = sum(
        pair_component(left, right) ** 2
        for left in VECTORS
        for right in VECTORS
    ) / 49
    degree_two_norm = 3 * pair_norm

    variance = P * (1 - P)
    degree_three_norm = variance - degree_two_norm
    return {
        "ordered_bases": len(ORDERED_BASES),
        "basis_probability": P,
        "variance": variance,
        "pair_component_values": pair_values,
        "one_pair_component_norm_squared": pair_norm,
        "degree_two_norm_squared": degree_two_norm,
        "degree_three_norm_squared": degree_three_norm,
    }


def exact_quadratic_checks() -> dict:
    """Check the degree-two bilinear form on a 36-dimensional tangent basis."""
    tangent = []
    for row in range(6):
        for column in range(6):
            matrix = [[Fraction(0) for _ in VECTORS] for _ in VECTORS]
            matrix[row][column] = 1
            matrix[row][6] = -1
            matrix[6][column] = -1
            matrix[6][6] = 1
            tangent.append(matrix)

    h = [
        [pair_component(i + 1, j + 1) for j in range(7)]
        for i in range(7)
    ]

    def inner(left, right):
        return sum(
            left[i][j] * right[i][j]
            for i in range(7)
            for j in range(7)
        )

    def one_pair_bilinear(left, right):
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

    mismatches = 0
    target = Fraction(16, 2401)
    for left in tangent:
        for right in tangent:
            if one_pair_bilinear(left, right) != target * inner(left, right):
                mismatches += 1

    return {
        "tangent_dimension": len(tangent),
        "bilinear_pairs_checked": len(tangent) ** 2,
        "mismatches": mismatches,
        "one_pair_quadratic_coefficient": target,
        "three_pair_quadratic_coefficient": 3 * target,
        "relative_quadratic_coefficient": (3 * target) / P2,
    }


def local_certificate() -> dict:
    radius = Fraction(1, 5)
    density = Fraction(21, 20)

    entropy_coefficient = Fraction(1, 1) / (2 * (1 + 7 * radius))
    energy_coefficient = Fraction(1, 12) + Fraction(13, 24) * radius
    margin = entropy_coefficient - density * energy_coefficient

    assert entropy_coefficient == Fraction(5, 24)
    assert energy_coefficient == Fraction(23, 120)
    assert margin == Fraction(17, 2400)
    assert margin > 0

    return {
        "certified_density": density,
        "frobenius_radius": radius,
        "entropy_lower_coefficient": entropy_coefficient,
        "energy_upper_coefficient": energy_coefficient,
        "strict_margin_coefficient": margin,
        "conclusion": (
            "D(B)-(21/20)L(B) >= (17/2400)||B-U||_F^2 "
            "for ||B-U||_F <= 1/5"
        ),
    }


def invariant_family() -> dict:
    return {
        "matrix": "diagonal alpha; off-diagonal (1-alpha)/6",
        "entropy_defect": (
            "D(alpha)=alpha ln(7 alpha)+(1-alpha) "
            "ln(7(1-alpha)/6)"
        ),
        "joint_probability": (
            "q(alpha)=(91 alpha^3+33 alpha^2-15 alpha+107)/441"
        ),
        "symmetry_reduction_proved": False,
    }


def build_results() -> dict:
    data = hoeffding_data()
    checks = exact_quadratic_checks()
    cert = local_certificate()
    return {
        "laboratory": "V90",
        "module": "seven-state local-global entropy contraction",
        "hoeffding_decomposition": {
            key: (
                f"{value.numerator}/{value.denominator}"
                if isinstance(value, Fraction)
                else {
                    subkey: f"{subvalue.numerator}/{subvalue.denominator}"
                    for subkey, subvalue in value.items()
                }
                if isinstance(value, dict)
                else value
            )
            for key, value in data.items()
        },
        "exact_quadratic_identity": {
            key: f"{value.numerator}/{value.denominator}"
            if isinstance(value, Fraction)
            else value
            for key, value in checks.items()
        },
        "global_spectral_envelope": {
            "centered_matrix": "C=B-U",
            "operator_norm": "sigma=||C||_(2->2) <= 1",
            "exact_decomposition": (
                "q(B)=(24/49)^2+(48/2401)||C||_F^2+T_3(C)"
            ),
            "cubic_bound": (
                "|T_3(C)| <= (312/2401) sigma^3"
            ),
            "relative_energy_bound": (
                "q(B)/(24/49)^2 <= 1+||C||_F^2/12+13 sigma^3/24"
            ),
        },
        "local_certificate": {
            key: f"{value.numerator}/{value.denominator}"
            if isinstance(value, Fraction)
            else value
            for key, value in cert.items()
        },
        "invariant_family": invariant_family(),
        "literature_boundary": {
            "strong_four_case_imported": False,
            "reason": (
                "Located strong-colorability lower theorems require the number "
                "of colors to be sufficiently large; no checked theorem statement "
                "covers k=3, r=4, c=1."
            ),
        },
        "remaining_gap": {
            "region": "||B-U||_F > 1/5 in the 7x7 Birkhoff polytope",
            "global_entropy_contraction_proved": False,
            "random_model_basis_colorable_whp": False,
            "nine_row_constructor_lower_bound": False,
            "v90_stop_condition_met": False,
        },
        "nonclaims": [
            "The local ball is not a global second-moment theorem.",
            "The GL(3,2)-invariant family is not known to contain every maximizer.",
            "The literature audit does not prove strong four-colorability at density one.",
            "P versus NP remains unresolved.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(build_results(), indent=2, sort_keys=True))
