from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import floor, log2
from typing import Iterable, Sequence


def truth_bit(mask: int, x: int) -> int:
    return (mask >> x) & 1


def pm_value(mask: int, x: int) -> int:
    return 1 if truth_bit(mask, x) == 0 else -1


def walsh_spectrum(mask: int, arity: int = 3) -> dict[int, float]:
    size = 1 << arity
    result: dict[int, float] = {}
    for subset in range(size):
        total = 0
        for x in range(size):
            character = -1 if ((x & subset).bit_count() & 1) else 1
            total += pm_value(mask, x) * character
        result[subset] = total / size
    return result


def is_affine(mask: int, arity: int = 3) -> bool:
    return any(abs(value) == 1 for value in walsh_spectrum(mask, arity).values())


def is_balanced(mask: int, arity: int = 3) -> bool:
    return mask.bit_count() == (1 << (arity - 1))


def essential_variables(mask: int, arity: int = 3) -> tuple[bool, ...]:
    essential = []
    for bit in range(arity):
        changes = False
        for x in range(1 << arity):
            y = x ^ (1 << bit)
            if truth_bit(mask, x) != truth_bit(mask, y):
                changes = True
                break
        essential.append(changes)
    return tuple(essential)


def classify_predicates() -> dict:
    affine: list[int] = []
    nonaffine_unbalanced: list[int] = []
    balanced_nonaffine: list[int] = []
    low_degree_profiles: dict[str, int] = {}
    witnesses: list[dict] = []

    for mask in range(256):
        spectrum = walsh_spectrum(mask)
        if is_affine(mask):
            affine.append(mask)
            continue
        if not is_balanced(mask):
            nonaffine_unbalanced.append(mask)
            continue

        balanced_nonaffine.append(mask)
        low = {
            subset: coefficient
            for subset, coefficient in spectrum.items()
            if 1 <= subset.bit_count() <= 2 and coefficient != 0
        }
        best_subset, best_coefficient = max(
            low.items(), key=lambda item: (abs(item[1]), -item[0])
        )
        profile = (
            len(low),
            abs(spectrum[7]),
            tuple(sorted(abs(value) for value in low.values())),
        )
        key = repr(profile)
        low_degree_profiles[key] = low_degree_profiles.get(key, 0) + 1
        witnesses.append(
            {
                "mask": f"0x{mask:02x}",
                "best_subset": best_subset,
                "best_subset_size": best_subset.bit_count(),
                "fourier_correlation": abs(best_coefficient),
                "agreement_probability": (1 + abs(best_coefficient)) / 2,
                "nonzero_low_degree_coefficients": len(low),
                "cubic_coefficient_abs": abs(spectrum[7]),
            }
        )

    return {
        "total": 256,
        "affine_count": len(affine),
        "nonaffine_unbalanced_count": len(nonaffine_unbalanced),
        "balanced_nonaffine_count": len(balanced_nonaffine),
        "balanced_nonaffine_min_best_low_degree_correlation": min(
            item["fourier_correlation"] for item in witnesses
        ),
        "balanced_nonaffine_max_best_low_degree_correlation": max(
            item["fourier_correlation"] for item in witnesses
        ),
        "balanced_nonaffine_min_best_agreement": min(
            item["agreement_probability"] for item in witnesses
        ),
        "low_degree_profiles": low_degree_profiles,
        "witnesses": witnesses,
    }


def majority_mask(arity: int = 3) -> int:
    mask = 0
    for x in range(1 << arity):
        if x.bit_count() >= (arity + 1) // 2:
            mask |= 1 << x
    return mask


def nae_mask(arity: int = 3) -> int:
    mask = 0
    for x in range(1 << arity):
        if x not in (0, (1 << arity) - 1):
            mask |= 1 << x
    return mask


def essential_antipodal_gate(value_at_zero: int, value_at_one: int) -> int:
    """Return a 3-input truth table with prescribed 000/111 values and all variables essential."""
    if value_at_zero not in (0, 1) or value_at_one not in (0, 1):
        raise ValueError("endpoint values must be bits")
    base = nae_mask() if value_at_zero == value_at_one else majority_mask()
    if value_at_zero == 1:
        base ^= 0xFF
    assert truth_bit(base, 0) == value_at_zero
    assert truth_bit(base, 7) == value_at_one
    assert all(essential_variables(base))
    return base


def pair_embedding_truth_tables(y0: Sequence[int], y1: Sequence[int]) -> list[int]:
    if len(y0) != len(y1):
        raise ValueError("targets must have equal length")
    return [essential_antipodal_gate(a, b) for a, b in zip(y0, y1)]


@dataclass(frozen=True)
class SupportListBound:
    n: int
    m: int
    description_bits: int
    minimum_counting_list_size: int
    additive_stretch: int


def counting_list_bound(
    n: int,
    support_sizes: Sequence[int],
    allowed_function_counts: Sequence[int] | None = None,
) -> SupportListBound:
    m = len(support_sizes)
    if m <= n:
        raise ValueError("range avoidance requires m > n")
    if allowed_function_counts is None:
        allowed_function_counts = [1 << (1 << size) for size in support_sizes]
    if len(allowed_function_counts) != m:
        raise ValueError("one function-family size per output is required")
    if any(count <= 0 or count & (count - 1) for count in allowed_function_counts):
        raise ValueError("this exact bit-count implementation expects powers of two")
    q = sum(int(log2(count)) for count in allowed_function_counts)
    gap = m - n
    k = floor(q / gap) + 1
    return SupportListBound(
        n=n,
        m=m,
        description_bits=q,
        minimum_counting_list_size=k,
        additive_stretch=k * gap - q,
    )


def evaluate_local_circuit(
    supports: Sequence[Sequence[int]],
    truth_tables: Sequence[int],
    witness: int,
) -> tuple[int, ...]:
    """Evaluate a local Boolean circuit encoded by ordered support lists and truth masks."""
    if len(supports) != len(truth_tables):
        raise ValueError("one truth table per support is required")
    output: list[int] = []
    for support, mask in zip(supports, truth_tables):
        if len(set(support)) != len(support):
            raise ValueError("support variables must be distinct")
        if mask < 0 or mask >= (1 << (1 << len(support))):
            raise ValueError("truth-table mask does not match support arity")
        address = 0
        for position, variable in enumerate(support):
            address |= ((witness >> variable) & 1) << position
        output.append(truth_bit(mask, address))
    return tuple(output)


def eval_h(
    supports: Sequence[Sequence[int]],
    truth_tables: Sequence[int],
    witnesses: Sequence[int],
) -> tuple[int, ...]:
    """Structured evaluation map used in the support-only list reduction.

    The returned tuple concatenates C(x^1),...,C(x^k). A missing output is
    precisely a target list that cannot be covered simultaneously.
    """
    flattened: list[int] = []
    for witness in witnesses:
        flattened.extend(evaluate_local_circuit(supports, truth_tables, witness))
    return tuple(flattened)


def eval_h_dimensions(
    n: int,
    support_sizes: Sequence[int],
    k: int,
) -> dict[str, int]:
    """Return the unrestricted-table input/output lengths of Eval_H."""
    if k <= 0:
        raise ValueError("k must be positive")
    q = sum(1 << size for size in support_sizes)
    m = len(support_sizes)
    return {
        "truth_table_bits": q,
        "input_bits": q + n * k,
        "output_bits": m * k,
        "additive_stretch": k * (m - n) - q,
        "adaptive_query_depth": max(support_sizes, default=0) + 1,
        "nonadaptive_junta_bound": max(((1 << size) + size for size in support_sizes), default=0),
    }


def list_is_coverable(
    supports: Sequence[Sequence[int]],
    targets: Sequence[Sequence[int]],
    n: int,
) -> bool:
    """Exact small-instance test.

    A target list is simultaneously coverable iff there are input witnesses whose
    equal local projections never receive conflicting target bits.
    """
    if not targets:
        return True
    m = len(supports)
    if any(len(row) != m for row in targets):
        raise ValueError("each target must have one bit per output")
    assignments = range(1 << n)
    remaining = len(targets) - 1
    for tail in product(assignments, repeat=remaining):
        witnesses = (0,) + tail
        valid = True
        for output, support in enumerate(supports):
            seen: dict[tuple[int, ...], int] = {}
            for row, witness in zip(targets, witnesses):
                projection = tuple((witness >> variable) & 1 for variable in support)
                value = int(row[output])
                previous = seen.get(projection)
                if previous is not None and previous != value:
                    valid = False
                    break
                seen[projection] = value
            if not valid:
                break
        if valid:
            return True
    return False


def verify_pair_embedding_exhaustively() -> dict:
    masks = {}
    for a, b in product((0, 1), repeat=2):
        mask = essential_antipodal_gate(a, b)
        masks[f"{a}{b}"] = f"0x{mask:02x}"
    return {
        "endpoint_cases": 4,
        "all_endpoint_cases_constructed": len(masks) == 4,
        "masks": masks,
    }
