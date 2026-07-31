from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path
from typing import Any, Sequence

Monomial = tuple[int, ...]
Polynomial = dict[Monomial, int]


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def next_prime(value: int) -> int:
    candidate = value + 1
    while not is_prime(candidate):
        candidate += 1
    return candidate


def support(truth: Sequence[int]) -> tuple[int, ...]:
    return tuple(index for index, bit in enumerate(truth) if bit)


def normalized_support(truth: Sequence[int]) -> tuple[tuple[int, ...], int] | None:
    accepted = support(truth)
    universe = tuple(range(len(truth)))
    if not accepted or len(accepted) == len(universe):
        return None
    rejected = tuple(weight for weight in universe if weight not in accepted)
    if len(accepted) <= len(rejected):
        return accepted, 0
    return rejected, 1


def normalize_poly(polynomial: Polynomial, prime: int) -> Polynomial:
    return {
        monomial: coefficient % prime
        for monomial, coefficient in polynomial.items()
        if coefficient % prime
    }


def multiply_factor(
    polynomial: Polynomial,
    variables: Sequence[int],
    residue: int,
    prime: int,
) -> Polynomial:
    result: Polynomial = {}
    for monomial, coefficient in polynomial.items():
        result[monomial] = (
            result.get(monomial, 0) - residue * coefficient
        ) % prime
        present = set(monomial)
        for variable in variables:
            target = tuple(sorted(present | {variable}))
            result[target] = (result.get(target, 0) + coefficient) % prime
    return normalize_poly(result, prime)


def gate_polynomial(
    gate: dict[str, Any], prime: int
) -> tuple[Polynomial, int, tuple[int, ...]]:
    normalized = normalized_support(gate["truth_by_weight"])
    if normalized is None:
        raise ValueError("constant gate in dependency certificate")
    accepted, flip = normalized
    polynomial: Polynomial = {(): 1}
    for residue in accepted:
        polynomial = multiply_factor(
            polynomial, gate["variables"], residue, prime
        )
    return polynomial, flip, accepted


def add_scaled(
    accumulator: Polynomial,
    polynomial: Polynomial,
    scale: int,
    prime: int,
) -> None:
    for monomial, coefficient in polynomial.items():
        accumulator[monomial] = (
            accumulator.get(monomial, 0) + scale * coefficient
        ) % prime


def evaluate_gate(gate: dict[str, Any], assignment: int) -> int:
    weight = sum(
        (assignment >> variable) & 1 for variable in gate["variables"]
    )
    return gate["truth_by_weight"][weight]


def evaluate_circuit(
    circuit: dict[str, Any], assignment: int
) -> tuple[int, ...]:
    return tuple(evaluate_gate(gate, assignment) for gate in circuit["gates"])


def verify_case(case: dict[str, Any]) -> dict[str, bool]:
    circuit = case["circuit"]
    result = case["result"]
    certificate = result["certificate"]
    if result["status"] != "SOLVED" or certificate is None:
        return {
            "certificate_present": False,
            "dependency_identity": False,
            "output_pattern": False,
            "zero_set_semantics": False,
            "range_missing": False,
        }

    maximum_fanin = max(len(gate["variables"]) for gate in circuit["gates"])
    prime = next_prime(maximum_fanin)
    degree = (maximum_fanin + 1) // 2
    ambient = sum(
        math.comb(circuit["inputs"], index) for index in range(degree + 1)
    )
    coefficients = certificate["dependency_coefficients"]
    if (
        certificate["prime"] != prime
        or certificate["degree_bound"] != degree
        or certificate["ambient_dimension"] != ambient
        or len(coefficients) != len(circuit["gates"])
    ):
        return {
            "certificate_present": True,
            "dependency_identity": False,
            "output_pattern": False,
            "zero_set_semantics": False,
            "range_missing": False,
        }

    polynomials = []
    flips = []
    normalized_sets = []
    for gate in circuit["gates"]:
        polynomial, flip, accepted = gate_polynomial(gate, prime)
        polynomials.append(polynomial)
        flips.append(flip)
        normalized_sets.append(accepted)

    combined: Polynomial = {}
    for coefficient, polynomial in zip(coefficients, polynomials):
        add_scaled(combined, polynomial, coefficient, prime)
    dependency_identity = not normalize_poly(combined, prime)

    dependency_support = tuple(
        index
        for index, coefficient in enumerate(coefficients)
        if coefficient % prime
    )
    distinguished = certificate["distinguished_gate"]
    expected_normalized = [0] * len(circuit["gates"])
    for index in dependency_support:
        expected_normalized[index] = 1
    if distinguished in dependency_support:
        expected_normalized[distinguished] = 0
    expected_original = tuple(
        bit ^ flip for bit, flip in zip(expected_normalized, flips)
    )
    output_pattern = (
        tuple(certificate["dependency_support"]) == dependency_support
        and distinguished in dependency_support
        and tuple(certificate["normalized_output"]) == tuple(expected_normalized)
        and tuple(certificate["output_flips"]) == tuple(flips)
        and tuple(certificate["original_output"]) == expected_original
    )

    zero_set_semantics = True
    for gate, polynomial, accepted in zip(
        circuit["gates"], polynomials, normalized_sets
    ):
        for weight in range(len(gate["variables"]) + 1):
            assignment = 0
            for variable in gate["variables"][:weight]:
                assignment |= 1 << variable
            polynomial_value = 0
            for monomial, coefficient in polynomial.items():
                term = coefficient
                for variable in monomial:
                    term *= (assignment >> variable) & 1
                polynomial_value += term
            if (polynomial_value % prime == 0) != (weight in accepted):
                zero_set_semantics = False
                break
        if not zero_set_semantics:
            break

    target = tuple(certificate["original_output"])
    range_missing = all(
        evaluate_circuit(circuit, assignment) != target
        for assignment in range(1 << circuit["inputs"])
    )
    return {
        "certificate_present": True,
        "dependency_identity": dependency_identity,
        "output_pattern": output_pattern,
        "zero_set_semantics": zero_set_semantics,
        "range_missing": range_missing,
    }


def taxonomy_check(maximum_fanin: int = 8) -> dict[str, Any]:
    failures = []
    checked = 0
    for arity in range(maximum_fanin + 1):
        degree = (arity + 1) // 2
        for mask in range(1 << (arity + 1)):
            checked += 1
            truth = tuple(
                (mask >> weight) & 1 for weight in range(arity + 1)
            )
            accepted = support(truth)
            normalized_size = min(
                len(accepted), arity + 1 - len(accepted)
            )
            if normalized_size > degree:
                failures.append(
                    {
                        "arity": arity,
                        "truth": truth,
                        "normalized_size": normalized_size,
                        "degree": degree,
                    }
                )
    return {"checked": checked, "failures": failures}


def verify(results: Path) -> dict[str, Any]:
    cases = json.loads(
        (results / "full_certificate_cases.json").read_text(encoding="utf-8")
    )
    case_results = [verify_case(case) for case in cases]
    failures = [
        index
        for index, result in enumerate(case_results)
        if not all(result.values())
    ]
    taxonomy = taxonomy_check()
    kinds: dict[str, int] = {}
    for case in cases:
        kinds[case["kind"]] = kinds.get(case["kind"], 0) + 1
    observed = {
        "cases": len(cases),
        "cases_by_kind": kinds,
        "case_failures": failures,
        "taxonomy_checked": taxonomy["checked"],
        "taxonomy_failures": taxonomy["failures"],
        "all_dependency_identities": all(
            result["dependency_identity"] for result in case_results
        ),
        "all_zero_set_semantics": all(
            result["zero_set_semantics"] for result in case_results
        ),
        "all_missing_outputs": all(
            result["range_missing"] for result in case_results
        ),
    }
    observed["matches_claims"] = (
        len(cases) == 125
        and not failures
        and taxonomy["checked"] == 1022
        and not taxonomy["failures"]
    )
    return observed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("results", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify(args.results)
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    print(payload)
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    if not result["matches_claims"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
