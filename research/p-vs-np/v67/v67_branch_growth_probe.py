#!/usr/bin/env python3
from __future__ import annotations

import json
import random
from collections import Counter
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEED = 42
SAMPLES = 4000
N_MIN = 4
N_MAX = 12

# Positive fiber of the ternary representative 0x07:
# {000,001,010}.  Each tuple is a disjoint two-affine-cell partition.
LOCAL_PARTITIONS = (
    (frozenset({0}), frozenset({1, 2})),
    (frozenset({0, 1}), frozenset({2})),
    (frozenset({0, 2}), frozenset({1})),
)


def affine_set(points: frozenset[int]) -> bool:
    if not points:
        return False
    base = next(iter(points))
    linear = {x ^ base for x in points}
    return 0 in linear and all((u ^ v) in linear for u in linear for v in linear)


def lift_cell(cell: frozenset[int], support: tuple[int, int, int], n: int) -> frozenset[int]:
    a, b, c = support
    return frozenset(
        x
        for x in range(1 << n)
        if (((x >> a) & 1) | (((x >> b) & 1) << 1) | (((x >> c) & 1) << 2)) in cell
    )


def build_system(n: int, specs: list[dict] | tuple[dict, ...]):
    answer = []
    for item in specs:
        support = tuple(item["support"])
        partition = int(item["partition"])
        left, right = LOCAL_PARTITIONS[partition]
        answer.append((lift_cell(left, support, n), lift_cell(right, support, n)))
    return tuple(answer)


def consistent_signatures(system, n: int) -> frozenset[int]:
    signatures = set()
    for point in range(1 << n):
        signature = 0
        for gate, (left, right) in enumerate(system):
            if point in left:
                continue
            if point in right:
                signature |= 1 << gate
                continue
            break
        else:
            signatures.add(signature)
    return frozenset(signatures)


def optimal_pruned_tree(system, n: int) -> tuple[int, int, int, int]:
    @lru_cache(None)
    def solve(feasible: tuple[int, ...], remaining: tuple[int, ...]):
        current = frozenset(feasible)
        if not current or not remaining:
            return 1, 0, 0, None
        best = None
        for gate in remaining:
            tail = tuple(x for x in remaining if x != gate)
            left = solve(tuple(sorted(current & system[gate][0])), tail)
            right = solve(tuple(sorted(current & system[gate][1])), tail)
            candidate = (
                left[0] + right[0],
                1 + left[1] + right[1],
                1 + max(left[2], right[2]),
                gate,
            )
            if best is None or candidate[:3] < best[:3]:
                best = candidate
        return best

    reached = set()

    def walk(feasible: tuple[int, ...], remaining: tuple[int, ...]):
        state = (feasible, remaining)
        if state in reached:
            return
        reached.add(state)
        current = frozenset(feasible)
        if not current or not remaining:
            return
        gate = solve(feasible, remaining)[3]
        tail = tuple(x for x in remaining if x != gate)
        walk(tuple(sorted(current & system[gate][0])), tail)
        walk(tuple(sorted(current & system[gate][1])), tail)

    remaining = tuple(range(len(system)))
    root = solve(tuple(range(1 << n)), remaining)
    walk(tuple(range(1 << n)), remaining)
    return root[0], root[1], root[2], len(reached)


def greedy_pruned_tree(system, n: int) -> tuple[int, int, int]:
    @lru_cache(None)
    def solve(feasible: tuple[int, ...], remaining: tuple[int, ...]):
        current = frozenset(feasible)
        if not current or not remaining:
            return 1, 0, 0
        candidates = []
        for gate in remaining:
            left = tuple(sorted(current & system[gate][0]))
            right = tuple(sorted(current & system[gate][1]))
            score = (
                int(bool(left)) + int(bool(right)),
                max(len(left), len(right)),
                abs(len(left) - len(right)),
                gate,
            )
            candidates.append((score, gate, left, right))
        _, gate, left, right = min(candidates)
        tail = tuple(x for x in remaining if x != gate)
        a = solve(left, tail)
        b = solve(right, tail)
        return a[0] + b[0], 1 + a[1] + b[1], 1 + max(a[2], b[2])

    return solve(tuple(range(1 << n)), tuple(range(len(system))))


def regular_chain(n: int, pattern: str) -> list[dict]:
    specs = []
    for i in range(n):
        partition = 0 if pattern == "constant" else i % 3
        specs.append({"support": [i, (i + 1) % n, (i + 2) % n], "partition": partition})
    if pattern == "constant":
        specs.append({"support": [0, 1, 2], "partition": 1})
    elif pattern == "rotating":
        specs.append({"support": [0, 2, 4 % n], "partition": 2})
    else:
        raise ValueError(pattern)
    return specs


def direct_sum_specs(n_left: int, left: list[dict], right: list[dict]) -> list[dict]:
    shifted = [
        {
            "support": [int(v) + n_left for v in item["support"]],
            "partition": int(item["partition"]),
        }
        for item in right
    ]
    return [dict(item) for item in left] + shifted


def verify_direct_sum_examples():
    left = [
        {"support": [1, 0, 2], "partition": 0},
        {"support": [1, 0, 2], "partition": 0},
        {"support": [0, 1, 2], "partition": 0},
        {"support": [0, 2, 1], "partition": 0},
    ]
    right = [
        {"support": [0, 2, 1], "partition": 0},
        {"support": [2, 0, 1], "partition": 0},
        {"support": [0, 2, 1], "partition": 1},
        {"support": [2, 0, 1], "partition": 0},
    ]
    left_system = build_system(3, left)
    right_system = build_system(3, right)
    combined = direct_sum_specs(3, left, right)
    combined_system = build_system(6, combined)
    c_left = len(consistent_signatures(left_system, 3))
    c_right = len(consistent_signatures(right_system, 3))
    c_combined = len(consistent_signatures(combined_system, 6))
    l_left = optimal_pruned_tree(left_system, 3)[0]
    l_right = optimal_pruned_tree(right_system, 3)[0]
    l_combined = optimal_pruned_tree(combined_system, 6)[0]
    upper = l_left + c_left * (l_right - 1)
    assert (c_left, c_right, c_combined) == (2, 3, 6)
    assert c_combined == c_left * c_right
    assert l_combined <= upper
    return {
        "left_c": c_left,
        "right_c": c_right,
        "direct_sum_c": c_combined,
        "left_L_aff": l_left,
        "right_L_aff": l_right,
        "direct_sum_L_aff": l_combined,
        "composition_upper_bound": upper,
    }


def verify_regular_chains():
    rows = []
    maximum = 0
    for pattern in ("constant", "rotating"):
        for n in range(4, 13):
            system = build_system(n, regular_chain(n, pattern))
            count = len(consistent_signatures(system, n))
            maximum = max(maximum, count)
            rows.append({"pattern": pattern, "n": n, "m": n + 1, "c": count})
    assert maximum <= 2
    return {"cases": rows, "maximum_c": maximum}


def random_probe():
    rng = random.Random(SEED)
    by_n: dict[int, dict] = {}
    first_c16_n10 = None
    global_best = {"c": -1}
    distribution = Counter()

    for iteration in range(SAMPLES):
        n = rng.randint(N_MIN, N_MAX)
        specs = [
            {
                "support": list(rng.sample(range(n), 3)),
                "partition": rng.randrange(3),
            }
            for _ in range(n + 1)
        ]
        system = build_system(n, specs)
        signatures = consistent_signatures(system, n)
        count = len(signatures)
        distribution[count] += 1

        previous = by_n.get(n)
        if previous is None or count > previous["c"]:
            by_n[n] = {"c": count, "iteration": iteration}

        if n == 10 and count == 16 and first_c16_n10 is None:
            first_c16_n10 = {
                "iteration": iteration,
                "n": n,
                "m": n + 1,
                "c": count,
                "specs": specs,
                "signatures": sorted(signatures),
            }

        if count > global_best["c"]:
            global_best = {
                "iteration": iteration,
                "n": n,
                "m": n + 1,
                "c": count,
                "specs": specs,
                "signatures": sorted(signatures),
            }

    assert first_c16_n10 is not None
    assert first_c16_n10["iteration"] == 344
    assert global_best["iteration"] == 2360
    assert (global_best["n"], global_best["c"]) == (11, 36)
    assert {n: row["c"] for n, row in sorted(by_n.items())} == {
        4: 4, 5: 6, 6: 8, 7: 10, 8: 16, 9: 18, 10: 26, 11: 36, 12: 30
    }

    for witness in (first_c16_n10, global_best):
        system = build_system(witness["n"], witness["specs"])
        optimal = optimal_pruned_tree(system, witness["n"])
        greedy = greedy_pruned_tree(system, witness["n"])
        assert witness["c"] <= optimal[0] <= greedy[0]
        witness["L_aff"] = optimal[0]
        witness["D_aff"] = optimal[2]
        witness["G_aff"] = optimal[3]
        witness["L_greedy"] = greedy[0]
        witness["D_greedy"] = greedy[2]

    assert (
        first_c16_n10["L_aff"],
        first_c16_n10["G_aff"],
        first_c16_n10["L_greedy"],
    ) == (25, 47, 25)
    assert (
        global_best["L_aff"],
        global_best["G_aff"],
        global_best["L_greedy"],
    ) == (61, 108, 62)

    return {
        "seed": SEED,
        "samples": SAMPLES,
        "n_range": [N_MIN, N_MAX],
        "generator": "n uniform in [4,12]; m=n+1; ordered three-variable supports sampled without replacement; one of the three positive-fiber 0x07 affine partitions selected uniformly",
        "distribution": {str(k): v for k, v in sorted(distribution.items())},
        "maximum_by_n": {str(n): row for n, row in sorted(by_n.items())},
        "first_c16_n10": first_c16_n10,
        "global_best": global_best,
    }


def main():
    assert all(affine_set(cell) for part in LOCAL_PARTITIONS for cell in part)
    assert all(left.isdisjoint(right) and left | right == frozenset({0, 1, 2})
               for left, right in LOCAL_PARTITIONS)

    direct_sum = verify_direct_sum_examples()
    chains = verify_regular_chains()
    probe = random_probe()

    results = {
        "version": "V67",
        "status": "passed",
        "direct_sum_finite_validation": direct_sum,
        "regular_overlap_chains": chains,
        "random_overlap_probe": probe,
        "branching_sandwich": {
            "statement": "c <= L_aff <= L_greedy",
            "c16": {
                "c": probe["first_c16_n10"]["c"],
                "L_aff": probe["first_c16_n10"]["L_aff"],
                "L_greedy": probe["first_c16_n10"]["L_greedy"],
            },
            "c36": {
                "c": probe["global_best"]["c"],
                "L_aff": probe["global_best"]["L_aff"],
                "L_greedy": probe["global_best"]["L_greedy"],
            },
        },
        "scientific_status": {
            "direct_sum_proposition_proved": True,
            "explicit_exponential_family_found": False,
            "polynomial_branching_bound_proved": False,
            "unrestricted_nc0_3_avoid_solved": False,
            "circuit_lower_bound_proved": False,
            "p_vs_np_route_active": False,
            "p_vs_np_resolved": False,
            "peer_reviewed": False,
            "novelty_confirmed": False,
        },
        "failures": 0,
    }
    (HERE / "RESULTS.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
    witness_payload = {
        "version": "V67",
        "local_partitions": [
            {"left": sorted(left), "right": sorted(right)}
            for left, right in LOCAL_PARTITIONS
        ],
        "c16": probe["first_c16_n10"],
        "c36": probe["global_best"],
    }
    (HERE / "WITNESSES.json").write_text(
        json.dumps(witness_payload, indent=2, sort_keys=True) + "\n"
    )
    print(
        "V67 branch-growth probe passed: direct-sum multiplicativity; "
        "18 regular chains; 4,000 seeded overlap systems; "
        "c=16 witness at n=10 and c=36 witness at n=11; zero failures."
    )


if __name__ == "__main__":
    main()
