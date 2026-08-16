from __future__ import annotations

import json
import random
from itertools import combinations, product

from hybrid_root_rank import Gate, avoid_with_certificate, in_range, strict_family


def gf2_rank(rows: list[int]) -> int:
    basis: dict[int, int] = {}
    for row in rows:
        x = row
        while x:
            pivot = x.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = x
                break
            x ^= basis[pivot]
    return len(basis)


def support_connected_and_min_degree(n: int, gates: list[Gate]) -> tuple[bool, int]:
    adj = [set() for _ in range(n)]
    degree = [0] * n
    for g in gates:
        for v in g.support:
            degree[v] += 1
        for u, v in combinations(g.support, 2):
            adj[u].add(v)
            adj[v].add(u)
    seen = {0}
    stack = [0]
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen) == n, min(degree)


def strict_checks() -> dict:
    brute = 0
    for k in (1, 2):
        n, gates, functional, affine = strict_family(k)
        y, meta = avoid_with_certificate(n, gates, functional, affine)
        assert meta["case"] == "hybrid_enumeration"
        assert meta["eta"] == 3
        assert meta["relaxed_assignments"] == 8
        assert meta["residual_outputs"] == 4
        assert not in_range(n, gates, y)
        brute += 1

    for k in range(1, 31):
        n, gates, functional, affine = strict_family(k)
        a = b = 4 * k
        assert n == 8 * k and len(gates) == n + 1
        assert len(functional) == a - 2
        assert len(affine) == b - 1
        rows = []
        for idx in affine:
            row = 0
            for v in gates[idx].support:
                row ^= 1 << v
            rows.append(row)
        assert gf2_rank(rows) == b - 1
        roots = n - len(functional)
        eta = roots - (b - 1)
        assert roots == b + 2 and eta == 3
        connected, min_degree = support_connected_and_min_degree(n, gates)
        assert connected and min_degree >= 2
        # Previous parameters on this family.
        assert 8 * k == n                  # V97 lambda, by no peel on connected essential support
        assert k + 3 == n - ((a - 2) + (3*k - 1))  # exact V101 mu
        assert 3 * k <= n                  # V102 beta lower bound from disjoint B gadgets
        assert 4 * k + 1 == n - (b - 1)   # exact V103 nu
    return {"bruteforce_k": [1, 2], "structural_k_through": 30, "eta": 3}


def randomized_residual_checks() -> int:
    rng = random.Random(104104)
    cases = 0
    # Mutate only the four unselected residual outputs. The hybrid certificate
    # and its eight-point relaxed domain remain valid independently of them.
    for k, trials in ((1, 420), (2, 40)):
        n, base, functional, affine = strict_family(k)
        selected = {i for i, _t, _h in functional} | set(affine)
        residual = [i for i in range(len(base)) if i not in selected]
        assert len(residual) == 4
        for _ in range(trials):
            gates = list(base)
            for idx in residual:
                support = tuple(rng.sample(range(n), 3))
                mask = rng.randrange(256)
                gates[idx] = Gate(support, mask)
            y, meta = avoid_with_certificate(n, gates, functional, affine)
            assert meta["eta"] == 3
            assert not in_range(n, gates, y), (k, y, meta)
            cases += 1
    return cases


def local_beta_lower_rule() -> bool:
    # EXACT-ONE 0x16: after fixing fewer than two coordinates, at least one
    # restriction is nonlinear; fixing any two leaves at most a unary function.
    def eval_mask(mask, bits):
        idx = sum(b << j for j, b in enumerate(bits))
        return (mask >> idx) & 1

    def affine(values, arity):
        c = values[0]
        coeff = [values[1 << j] ^ c for j in range(arity)]
        for idx, val in enumerate(values):
            want = c
            for j in range(arity):
                want ^= coeff[j] & ((idx >> j) & 1)
            if val != want:
                return False
        return True

    for fixed_count in (0, 1):
        for fixed_pos in combinations(range(3), fixed_count):
            free = [j for j in range(3) if j not in fixed_pos]
            strong = True
            for fb in product((0, 1), repeat=fixed_count):
                vals = []
                for xb in product((0, 1), repeat=len(free)):
                    local = [0, 0, 0]
                    for j, b in zip(fixed_pos, fb): local[j] = b
                    for j, b in zip(free, xb): local[j] = b
                    vals.append(eval_mask(0x16, local))
                strong &= affine(vals, len(free))
            assert not strong
    return True


def main() -> None:
    result = {
        "strict_family": strict_checks(),
        "random_residual_bruteforce_cases": randomized_residual_checks(),
        "exact_one_beta_local_lower_rule": local_beta_lower_rule(),
        "failures": 0,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
