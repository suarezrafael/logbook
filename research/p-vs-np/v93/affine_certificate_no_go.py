#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter


def truth_bit(tt: int, x: int) -> int:
    return (tt >> x) & 1


def truth_table_from_projection(n: int, index: int) -> int:
    tt = 0
    for x in range(1 << n):
        tt |= ((x >> index) & 1) << x
    return tt


def truth_table_from_callable(n: int, fn) -> int:
    tt = 0
    for x in range(1 << n):
        bits = tuple((x >> i) & 1 for i in range(n))
        tt |= (fn(bits) & 1) << x
    return tt


def anf_coefficients(tt: int, n: int) -> list[int]:
    coeff = [truth_bit(tt, x) for x in range(1 << n)]
    for i in range(n):
        for mask in range(1 << n):
            if mask & (1 << i):
                coeff[mask] ^= coeff[mask ^ (1 << i)]
    return coeff


def is_affine(tt: int, n: int) -> bool:
    coeff = anf_coefficients(tt, n)
    return all(coeff[mask] == 0 for mask in range(1 << n) if mask.bit_count() >= 2)


def support(tt: int, n: int) -> tuple[int, ...]:
    out = []
    for i in range(n):
        depends = False
        for x in range(1 << n):
            if x & (1 << i):
                continue
            if truth_bit(tt, x) != truth_bit(tt, x | (1 << i)):
                depends = True
                break
        if depends:
            out.append(i)
    return tuple(out)


def syndrome_relation(outputs: tuple[int, ...], n: int) -> tuple[tuple[int, int], ...]:
    """All (lambda,c) such that XOR_i lambda_i C_i(x) == c for every x."""
    m = len(outputs)
    relation = []
    for lam in range(1 << m):
        first = None
        constant = True
        for x in range(1 << n):
            value = 0
            for i, tt in enumerate(outputs):
                if (lam >> i) & 1:
                    value ^= truth_bit(tt, x)
            if first is None:
                first = value
            elif value != first:
                constant = False
                break
        if constant:
            relation.append((lam, int(first or 0)))
    return tuple(relation)


def affine_syndrome_certificate(outputs: tuple[int, ...], n: int):
    return (
        tuple(support(tt, n) for tt in outputs),
        syndrome_relation(outputs, n),
    )


def evaluate(outputs: tuple[int, ...], n: int, x: int) -> int:
    y = 0
    for i, tt in enumerate(outputs):
        y |= truth_bit(tt, x) << i
    return y


def image(outputs: tuple[int, ...], n: int) -> frozenset[int]:
    return frozenset(evaluate(outputs, n, x) for x in range(1 << n))


def first_child_counts(outputs: tuple[int, ...], n: int) -> tuple[int, int]:
    tt = outputs[0]
    ones = sum(truth_bit(tt, x) for x in range(1 << n))
    return (1 << n) - ones, ones


def canonical_first_bit(outputs: tuple[int, ...], n: int) -> int:
    n0, n1 = first_child_counts(outputs, n)
    return 0 if n0 <= n1 else 1


def forced_next_bit_from_syndrome(
    outputs: tuple[int, ...], n: int, prefix: tuple[int, ...], next_index: int
) -> int | None:
    """Return the value forced for output[next_index] by a syndrome using only prefix+next."""
    assert len(prefix) == next_index
    for lam, const in syndrome_relation(outputs, n):
        if not ((lam >> next_index) & 1):
            continue
        if any((lam >> i) & 1 for i in range(next_index + 1, len(outputs))):
            continue
        forced = const
        for i, bit in enumerate(prefix):
            if (lam >> i) & 1:
                forced ^= bit
        return forced
    return None


def exact_prefix_count(outputs: tuple[int, ...], n: int, prefix: tuple[int, ...]) -> int:
    total = 0
    for x in range(1 << n):
        ok = True
        for i, bit in enumerate(prefix):
            if truth_bit(outputs[i], x) != bit:
                ok = False
                break
        total += int(ok)
    return total


def build_results() -> dict:
    n = 3
    projections = tuple(truth_table_from_projection(n, i) for i in range(n))
    universe = frozenset(range(1 << 4))

    nonaffine = 0
    nonaffine_balanced = 0
    nonaffine_unbalanced = 0
    same_certificate_functions = 0
    complementary_image_functions = 0
    opposite_decision_functions = 0
    support_mismatches = 0
    syndrome_mismatches = 0
    range_partition_mismatches = 0
    decision_mismatches = 0
    decision_hist = Counter()

    representative = None

    for f in range(1 << (1 << n)):
        fbar = f ^ ((1 << (1 << n)) - 1)
        c = (f,) + projections
        cbar = (fbar,) + projections

        cert = affine_syndrome_certificate(c, n)
        certbar = affine_syndrome_certificate(cbar, n)
        if cert[0] != certbar[0]:
            support_mismatches += 1

        im = image(c, n)
        imbar = image(cbar, n)
        if im.isdisjoint(imbar) and (im | imbar) == universe:
            complementary_image_functions += 1
        else:
            range_partition_mismatches += 1

        if not is_affine(f, n):
            nonaffine += 1
            wt = sum(truth_bit(f, x) for x in range(1 << n))
            if wt == 4:
                nonaffine_balanced += 1
            else:
                nonaffine_unbalanced += 1

            if cert == certbar:
                same_certificate_functions += 1
            else:
                syndrome_mismatches += 1

            b = canonical_first_bit(c, n)
            bbar = canonical_first_bit(cbar, n)
            decision_hist[(wt, b, bbar)] += 1

            if wt != 4:
                if b != bbar:
                    opposite_decision_functions += 1
                else:
                    decision_mismatches += 1

            if f == truth_table_from_callable(3, lambda bits: bits[0] & bits[1] & bits[2]):
                representative = {
                    "f_truth_table_hex": hex(f),
                    "complement_truth_table_hex": hex(fbar),
                    "supports": [list(s) for s in cert[0]],
                    "syndrome_relation": [list(item) for item in cert[1]],
                    "child_counts_f": list(first_child_counts(c, n)),
                    "child_counts_not_f": list(first_child_counts(cbar, n)),
                    "canonical_bit_f": b,
                    "canonical_bit_not_f": bbar,
                    "image_size_f": len(im),
                    "image_size_not_f": len(imbar),
                    "image_union_size": len(im | imbar),
                    "image_intersection_size": len(im & imbar),
                }

    x0, x1, _ = projections
    xor01 = x0 ^ x1
    zero_detect_c = (x0, x1, xor01)
    prefix = (0, 1)
    forced = forced_next_bit_from_syndrome(zero_detect_c, 3, prefix, 2)
    child_zero = exact_prefix_count(zero_detect_c, 3, prefix + (0,))
    child_one = exact_prefix_count(zero_detect_c, 3, prefix + (1,))

    return {
        "target_row": {
            "class": "high-support-branchwidth NC0_3",
            "stretch": "m=n+1",
            "required_complexity": "strict improvement over O(n*2^(n/2)) for k=3, or a polynomial-time certificate branch",
            "named_baseline": "Huang-Li-Zhong ITCS 2026 Theorem 1.14",
        },
        "certificate_row": {
            "model": "AS(C)=(essential supports, full constant-output-parity syndrome relation Sigma(C))",
            "constructible_from_input": True,
            "verifiable": True,
            "determines_canonical_decision": False,
        },
        "mandatory_affine_comparison_census": {
            "ternary_functions": 256,
            "affine_functions": 16,
            "nonaffine_functions": nonaffine,
            "nonaffine_balanced_functions": nonaffine_balanced,
            "nonaffine_unbalanced_functions": nonaffine_unbalanced,
            "same_certificate_nonaffine_functions": same_certificate_functions,
            "complementary_image_functions": complementary_image_functions,
            "opposite_canonical_decision_functions": opposite_decision_functions,
            "opposite_canonical_decision_pairs": opposite_decision_functions // 2,
            "nonaffine_no_common_avoider_pairs": nonaffine // 2,
            "support_mismatches": support_mismatches,
            "syndrome_mismatches_on_nonaffine": syndrome_mismatches,
            "range_partition_mismatches": range_partition_mismatches,
            "decision_mismatches_on_unbalanced_nonaffine": decision_mismatches,
        },
        "representative_and_vs_nand": representative,
        "track_a_zero_detection": {
            "circuit": "(x0,x1,x0 xor x1)",
            "prefix": list(prefix),
            "forced_next_bit": forced,
            "count_child_0": child_zero,
            "count_child_1": child_one,
            "certificate_can_certify_empty_child_here": forced is not None and min(child_zero, child_one) == 0,
        },
        "theorem_status": {
            "global_affine_syndrome_comparison_oracle_closed": True,
            "certificate_only_single_valued_avoider_closed": True,
            "high_width_lift_symbolic": True,
            "zero_detection_subroutine_survives": True,
            "all_instance_polynomial_time": False,
            "new_circuit_lower_bound": False,
            "p_vs_np_resolved": False,
            "novelty_confirmed": False,
            "peer_reviewed": False,
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(build_results(), indent=2, sort_keys=True))
