"""V102 strong-affine-backdoor range avoidance core.

A gate is (support, mask), where support is a tuple of distinct global variable
indices and mask stores the gate truth table in little-endian lexicographic
order. Supports have arity at most three.
"""
from itertools import combinations, product


def gate_value(mask, bits):
    idx = 0
    for j, b in enumerate(bits):
        idx |= (int(b) & 1) << j
    return (mask >> idx) & 1


def restricted_affine_local(mask, arity, fixed):
    """Return (constant, coeffs_by_local_pos) or None for one restriction."""
    free = [i for i in range(arity) if i not in fixed]

    def ev(assign):
        bits = [0] * arity
        for i, v in fixed.items():
            bits[i] = v
        for i, v in assign.items():
            bits[i] = v
        return gate_value(mask, bits)

    c = ev({})
    coeff = {i: ev({i: 1}) ^ c for i in free}
    for vals in product((0, 1), repeat=len(free)):
        assign = dict(zip(free, vals))
        pred = c
        for i, v in assign.items():
            pred ^= coeff[i] & v
        if pred != ev(assign):
            return None
    return c, coeff


def strong_affine_local(mask, arity, conditioned_positions):
    positions = tuple(sorted(conditioned_positions))
    for vals in product((0, 1), repeat=len(positions)):
        if restricted_affine_local(mask, arity, dict(zip(positions, vals))) is None:
            return False
    return True


def local_minimal_good_supersets(mask, arity, current):
    """Inclusion-minimal local supersets of current that are strong-affine."""
    current = frozenset(current)
    remaining = [i for i in range(arity) if i not in current]
    good = []
    for r in range(len(remaining) + 1):
        for extra in combinations(remaining, r):
            cand = current | frozenset(extra)
            if strong_affine_local(mask, arity, cand):
                if not any(prev <= cand for prev in good):
                    good.append(cand)
    minimal = []
    for cand in good:
        if not any(other < cand for other in good):
            minimal.append(cand)
    return minimal


def is_backdoor(circuit, backdoor):
    B = set(backdoor)
    for support, mask in circuit:
        local = {i for i, v in enumerate(support) if v in B}
        if not strong_affine_local(mask, len(support), local):
            return False
    return True


def find_backdoor_at_most(circuit, k):
    """Bounded-search detection; branching factor <= 3 for arity <= 3."""
    def rec(B):
        if len(B) > k:
            return None
        for support, mask in circuit:
            local = {i for i, v in enumerate(support) if v in B}
            if strong_affine_local(mask, len(support), local):
                continue
            supersets = local_minimal_good_supersets(mask, len(support), local)
            extensions = []
            for S in supersets:
                ext = frozenset(support[i] for i in S if support[i] not in B)
                if ext and len(B | set(ext)) <= k:
                    extensions.append(ext)
            # Every valid global backdoor extending B must realize one of these
            # local strong-affine supersets.
            for ext in extensions:
                ans = rec(B | set(ext))
                if ans is not None:
                    return ans
            return None
        return frozenset(B)

    return rec(set())


def minimum_backdoor(circuit, n):
    for k in range(n + 1):
        ans = find_backdoor_at_most(circuit, k)
        if ans is not None:
            return ans
    raise AssertionError("conditioning all inputs must be a backdoor")


def _restricted_affine_global(support, mask, Bset, sigma):
    arity = len(support)
    fixed_local = {i: sigma[v] for i, v in enumerate(support) if v in Bset}
    rep = restricted_affine_local(mask, arity, fixed_local)
    if rep is None:
        return None
    c, local_coeff = rep
    return c, {support[i]: a for i, a in local_coeff.items()}


def _gf2_solution_count(num_vars, equations):
    """Count solutions to rows (bitmask, rhs) over GF(2)."""
    rows = [mask | ((rhs & 1) << num_vars) for mask, rhs in equations]
    rank = 0
    for col in range(num_vars):
        pivot = next((r for r in range(rank, len(rows)) if (rows[r] >> col) & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for r in range(len(rows)):
            if r != rank and ((rows[r] >> col) & 1):
                rows[r] ^= rows[rank]
        rank += 1
    varmask = (1 << num_vars) - 1
    for row in rows:
        if (row & varmask) == 0 and ((row >> num_vars) & 1):
            return 0
    return 1 << (num_vars - rank)


def prefix_preimage_count(circuit, n, backdoor, prefix):
    B = tuple(sorted(backdoor))
    Bset = set(B)
    free = [v for v in range(n) if v not in Bset]
    free_index = {v: i for i, v in enumerate(free)}
    total = 0

    for values in product((0, 1), repeat=len(B)):
        sigma = dict(zip(B, values))
        equations = []
        for (support, mask), target in zip(circuit, prefix):
            rep = _restricted_affine_global(support, mask, Bset, sigma)
            if rep is None:
                raise ValueError("supplied set is not a strong affine backdoor")
            c, coeff = rep
            row = 0
            for v, a in coeff.items():
                if a:
                    row |= 1 << free_index[v]
            equations.append((row, target ^ c))
        total += _gf2_solution_count(len(free), equations)
    return total


def avoid_with_backdoor(circuit, n, backdoor):
    if not is_backdoor(circuit, backdoor):
        raise ValueError("supplied set is not a strong affine backdoor")
    prefix = []
    for _ in range(len(circuit)):
        count0 = prefix_preimage_count(circuit, n, backdoor, prefix + [0])
        count1 = prefix_preimage_count(circuit, n, backdoor, prefix + [1])
        prefix.append(0 if count0 <= count1 else 1)
    return tuple(prefix)
