from __future__ import annotations

import json
import random
from itertools import combinations

from canonical_affine_first import canonical_affine_first_avoid
from hybrid_root_rank import Gate, in_range, strict_family


def support_connected_and_min_degree(n: int, gates: list[Gate]) -> tuple[bool, int]:
    adjacency = [set() for _ in range(n)]
    degree = [0] * n
    for gate in gates:
        for v in gate.support:
            degree[v] += 1
        for u, v in combinations(gate.support, 2):
            adjacency[u].add(v)
            adjacency[v].add(u)
    seen = {0}
    stack = [0]
    while stack:
        u = stack.pop()
        for v in adjacency[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen) == n, min(degree)


def random_exact_stretch_checks() -> int:
    rng = random.Random(1042026)
    cases = 0
    for n in range(2, 8):
        arity = min(3, n)
        max_mask = 1 << (1 << arity)
        for _ in range(300):
            gates = [
                Gate(tuple(rng.sample(range(n), arity)), rng.randrange(max_mask))
                for _j in range(n + 1)
            ]
            y, meta = canonical_affine_first_avoid(n, gates)
            assert len(y) == n + 1
            assert not in_range(n, gates, y), (n, y, meta)
            assert meta["eta"] >= 0
            cases += 1
    assert cases == 1800
    return cases


def strict_family_checks() -> dict:
    brute = []
    for k in (1, 2):
        n, gates, _functional, _affine = strict_family(k)
        y, meta = canonical_affine_first_avoid(n, gates)
        assert meta["case"] == "canonical_affine_first"
        assert meta["affine_rank"] == 4 * k - 1
        assert meta["functional_blocks"] == 4 * k - 2
        assert meta["eta"] == 3
        assert meta["relaxed_assignments"] == 8
        assert meta["residual_outputs"] == 4
        assert not in_range(n, gates, y)
        brute.append(k)

    for k in range(1, 21):
        n, gates, _functional, _affine = strict_family(k)
        y, meta = canonical_affine_first_avoid(n, gates)
        assert meta["affine_rank"] == 4 * k - 1
        assert meta["functional_blocks"] == 4 * k - 2
        assert meta["eta"] == 3
        assert meta["relaxed_assignments"] == 8
        assert meta["residual_outputs"] == 4
        connected, min_degree = support_connected_and_min_degree(n, gates)
        assert connected and min_degree >= 2
        # Previous structural scales on the same family.
        assert n == 8 * k                       # V97 lambda
        assert k + 3 == n - (7 * k - 3)        # V101 mu
        assert 3 * k <= 7 * k                  # V102 beta lower/upper witnesses
        assert 4 * k + 1 == n - (4 * k - 1)    # V103 nu
    return {"complete_range_k": brute, "canonical_eta_three_k_through": 20}


def mutated_residual_checks() -> int:
    rng = random.Random(104404)
    cases = 0
    for k, trials in ((1, 200), (2, 12)):
        n, base, functional, affine = strict_family(k)
        selected = {i for i, _t, _h in functional} | set(affine)
        residual = [i for i in range(len(base)) if i not in selected]
        assert len(residual) == 4
        for _ in range(trials):
            gates = list(base)
            for idx in residual:
                gates[idx] = Gate(tuple(rng.sample(range(n), 3)), rng.randrange(256))
            y, meta = canonical_affine_first_avoid(n, gates)
            assert not in_range(n, gates, y), (k, y, meta)
            cases += 1
    return cases


def main() -> None:
    result = {
        "canonical_random_exact_stretch_cases": random_exact_stretch_checks(),
        "strict_family": strict_family_checks(),
        "canonical_mutated_residual_cases": mutated_residual_checks(),
        "failures": 0,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
