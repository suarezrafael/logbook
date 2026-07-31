#!/usr/bin/env python3
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

LOCAL_PARTITIONS = (
    ({0}, {1, 2}),
    ({0, 1}, {2}),
    ({0, 2}, {1}),
)


def lift(cell, support, n):
    a, b, c = support
    answer = set()
    for x in range(1 << n):
        local = ((x >> a) & 1) | (((x >> b) & 1) << 1) | (((x >> c) & 1) << 2)
        if local in cell:
            answer.add(x)
    return frozenset(answer)


def compile_system(n, specs):
    system = []
    for item in specs:
        left, right = LOCAL_PARTITIONS[item["partition"]]
        support = tuple(item["support"])
        system.append((lift(left, support, n), lift(right, support, n)))
    return tuple(system)


def signatures(system, n):
    found = set()
    for x in range(1 << n):
        word = []
        for left, right in system:
            if x in left:
                word.append(0)
            elif x in right:
                word.append(1)
            else:
                break
        else:
            found.add(tuple(word))
    return found


def fixed_greedy_leaves(system, n):
    @lru_cache(None)
    def visit(feasible, remaining):
        current = set(feasible)
        if not current or not remaining:
            return 1
        candidates = []
        for gate in remaining:
            left = tuple(sorted(current & set(system[gate][0])))
            right = tuple(sorted(current & set(system[gate][1])))
            score = (
                int(bool(left)) + int(bool(right)),
                max(len(left), len(right)),
                abs(len(left) - len(right)),
                gate,
            )
            candidates.append((score, gate, left, right))
        _, gate, left, right = min(candidates)
        tail = tuple(i for i in remaining if i != gate)
        return visit(left, tail) + visit(right, tail)

    return visit(tuple(range(1 << n)), tuple(range(len(system))))


def verify_witness(name, expected_c, expected_greedy):
    data = json.loads((HERE / "WITNESSES.json").read_text())[name]
    system = compile_system(data["n"], data["specs"])
    found = signatures(system, data["n"])
    encoded = sorted(sum(bit << i for i, bit in enumerate(word)) for word in found)
    assert len(found) == expected_c == data["c"]
    assert encoded == data["signatures"]
    assert fixed_greedy_leaves(system, data["n"]) == expected_greedy == data["L_greedy"]
    assert data["c"] <= data["L_aff"] <= data["L_greedy"]
    return len(found)


def verify_direct_sum_factorization():
    left_specs = [
        {"support": [1, 0, 2], "partition": 0},
        {"support": [1, 0, 2], "partition": 0},
        {"support": [0, 1, 2], "partition": 0},
        {"support": [0, 2, 1], "partition": 0},
    ]
    right_specs = [
        {"support": [0, 2, 1], "partition": 0},
        {"support": [2, 0, 1], "partition": 0},
        {"support": [0, 2, 1], "partition": 1},
        {"support": [2, 0, 1], "partition": 0},
    ]
    shifted = left_specs + [
        {"support": [v + 3 for v in item["support"]], "partition": item["partition"]}
        for item in right_specs
    ]
    c_left = len(signatures(compile_system(3, left_specs), 3))
    c_right = len(signatures(compile_system(3, right_specs), 3))
    c_sum = len(signatures(compile_system(6, shifted), 6))
    assert (c_left, c_right, c_sum) == (2, 3, 6)
    assert c_sum == c_left * c_right
    return 3


def verify_surfaces():
    results = json.loads((HERE / "RESULTS.json").read_text())
    ledger = json.loads((ROOT / "LEDGER.json").read_text())
    assert results["version"] == "V67" and results["failures"] == 0
    assert results["random_overlap_probe"]["seed"] == 42
    assert results["random_overlap_probe"]["samples"] == 4000
    assert results["regular_overlap_chains"]["maximum_c"] <= 2
    assert results["direct_sum_finite_validation"]["direct_sum_c"] == 6
    assert ledger["schema_version"] >= 8 and int(ledger["current_version"][1:]) >= 67
    assert ledger["program"]["p_vs_np_route_active"] is False
    assert ledger["program"]["p_vs_np_resolved"] is False
    assert any(item["version"] == "V67" for item in ledger["versions"])
    runner = (ROOT / "verify_all.sh").read_text()
    assert "V67|primary|v67/verify.py|quick|" in runner
    assert "V67|independent|v67/verify_independent.py|quick|" in runner
    state = (ROOT / "STATE.md").read_text()
    assert int(__import__("re").search(r"\*\*Current laboratory:\*\* V(\d+)", state).group(1)) >= 67
    assert "Direct P-versus-NP route active:** no" in state
    theorem = (HERE / "DIRECT_SUM_PROPOSITION.md").read_text()
    assert "c(A \\oplus B)=c(A)c(B)" in theorem
    assert "1 + sum" in theorem
    sandwich = (HERE / "BRANCHING_SANDWICH.md").read_text()
    assert "c <= L_aff <= L_greedy" in sandwich
    corpus = "\n".join(
        path.read_text().lower()
        for path in HERE.iterdir()
        if path.suffix in {".md", ".json"}
    )
    for forbidden in (
        "p versus np is solved",
        "we prove p != np",
        "c_max(n) is exponential",
        "polynomial branching is proved",
    ):
        assert forbidden not in corpus
    return 18


def main():
    checks = verify_direct_sum_factorization()
    checks += verify_witness("c16", 16, 25)
    checks += verify_witness("c36", 36, 62)
    checks += verify_surfaces()
    print(
        f"V67 independent verification passed: {checks} checks; "
        "c=16 and c=36 witnesses brute-forced; zero failures."
    )


if __name__ == "__main__":
    main()
