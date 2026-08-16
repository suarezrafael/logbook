from __future__ import annotations

import json
import random
from itertools import product


def eval_mask(mask, bits):
    idx = sum(b << j for j, b in enumerate(bits))
    return (mask >> idx) & 1


def essential(mask):
    for j in range(3):
        if not any(
            ((mask >> i) & 1) != ((mask >> (i | (1 << j))) & 1)
            for i in range(8) if not ((i >> j) & 1)
        ):
            return False
    return True


def target(mask):
    return 1 if mask.bit_count() < 4 else 0


def rank_rows(rows, n):
    basis = {}
    for row in rows:
        x = row
        while x:
            pivot = x.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = x
                break
            x ^= basis[pivot]
    return len(basis)


def affine_hull_codim(mask, bit):
    points = [bits for bits in product((0, 1), repeat=3) if eval_mask(mask, bits) == bit]
    if not points:
        return 4
    equations = []
    for coeff in range(1, 8):
        vals = {
            sum(((coeff >> j) & 1) * p[j] for j in range(3)) & 1
            for p in points
        }
        if len(vals) == 1:
            equations.append(coeff)
    return rank_rows(equations, 3)


def census():
    ess = [m for m in range(256) if essential(m)]
    proper = [m for m in ess if affine_hull_codim(m, target(m)) > 0]
    full = [m for m in ess if affine_hull_codim(m, target(m)) == 0]
    assert len(ess) == 218 and len(proper) == 162 and len(full) == 56
    return len(ess), len(proper), len(full)


def inconsistent_canonical_witness():
    # Independent one-variable audit: identity and negation both have canonical
    # target zero. Their target fibers are x=0 and x=1, so canonical word 00 is
    # impossible. The actual image is exactly {01,10}.
    image = set()
    for x in (0, 1):
        identity = x
        negation = 1 ^ x
        image.add((identity, negation))
    assert image == {(0, 1), (1, 0)}
    assert (0, 0) not in image
    return {"canonical_witness": "00", "image_size": 2}


def strict_rows(k):
    rows = []

    def row(*variables):
        result = 0
        for v in variables:
            result ^= 1 << v
        return result

    for j in range(k):
        a, b, c, d = 4 * j, 4 * j + 1, 4 * j + 2, 4 * j + 3
        rows += [row(a, b, c), row(a, b, d), row(a, c, d)]
        if j:
            rows.append(row(4 * (j - 1) + 3, b, c))
    return rows


def strict_rank():
    for k in range(1, 41):
        rows = strict_rows(k)
        n = 4 * k
        assert len(rows) == n - 1
        assert rank_rows(rows, n) == n - 1
    return 40


def direct_strict_solutions():
    checks = 0
    for k in range(1, 5):
        n = 4 * k
        rows = strict_rows(k)
        solutions = []
        for x in range(1 << n):
            if all(((x & row).bit_count() & 1) == 1 for row in rows):
                solutions.append(x)
        assert len(solutions) == 2
        for x in solutions:
            for j in range(k):
                assert ((x >> (4 * j)) & 1) == 1
                b = (x >> (4 * j + 1)) & 1
                c = (x >> (4 * j + 2)) & 1
                d = (x >> (4 * j + 3)) & 1
                assert b == c == d
                if j < k - 1:
                    assert b == 1
        checks += 1
    return checks


def brute_rank_avoider_random():
    rng = random.Random(31337)
    cases = 0
    for n in range(3, 7):
        for _ in range(90):
            m = n + 1
            gates = []
            for _i in range(m):
                support = tuple(rng.sample(range(n), 3))
                mask = rng.randrange(256)
                gates.append((support, mask))

            blocks = []
            immediate = False
            for support, mask in gates:
                bit = target(mask)
                points = [p for p in product((0, 1), repeat=3) if eval_mask(mask, p) == bit]
                if not points:
                    immediate = True
                    break
                block = []
                for coeff in range(1, 8):
                    vals = {
                        sum(((coeff >> j) & 1) * p[j] for j in range(3)) & 1
                        for p in points
                    }
                    if len(vals) == 1:
                        rhs = next(iter(vals))
                        global_row = 0
                        for j, v in enumerate(support):
                            if (coeff >> j) & 1:
                                global_row ^= 1 << v
                        block.append((global_row, rhs))
                blocks.append(block)
            if immediate:
                cases += 1
                continue

            allowed = list(range(1 << n))
            selected = []
            for i, block in enumerate(blocks):
                restricted = [
                    x for x in allowed
                    if all(((x & row).bit_count() & 1) == rhs for row, rhs in block)
                ]
                if not restricted:
                    allowed = []
                    selected.append(i)
                    break
                if len(restricted) < len(allowed):
                    allowed = restricted
                    selected.append(i)
            if not allowed:
                cases += 1
                continue

            residual = [i for i in range(m) if i not in set(selected)]
            observed = set()
            for x in allowed:
                word = []
                for i in residual:
                    support, mask = gates[i]
                    bits = tuple((x >> v) & 1 for v in support)
                    word.append(eval_mask(mask, bits))
                observed.add(tuple(word))
            dimension = len(allowed).bit_length() - 1
            assert len(residual) > dimension
            assert len(observed) < (1 << len(residual))
            cases += 1
    return cases


def main():
    e, p, f = census()
    result = {
        "essential": e,
        "proper": p,
        "full": f,
        "inconsistent_canonical_witness": inconsistent_canonical_witness(),
        "strict_rank_k_through": strict_rank(),
        "strict_direct_solution_checks": direct_strict_solutions(),
        "independent_random_cases": brute_rank_avoider_random(),
        "failures": 0,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
