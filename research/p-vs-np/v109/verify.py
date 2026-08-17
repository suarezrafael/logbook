from __future__ import annotations

import json
import random
import sys
from itertools import combinations, product
from pathlib import Path

from mux_gate_flow import (
    DoubleCycleCertificate,
    GateBottleneck,
    MuxGate,
    avoid_mux_double_cycle,
    branch_graph_strongly_connected,
    find_double_cycle_or_bottleneck,
    in_range,
    strict_single_scc_family,
)

V108_DIR = Path(__file__).resolve().parents[1] / "v108"
sys.path.insert(0, str(V108_DIR))
from mux_scc_bridge import find_scc_bridge_certificate as v108_certificate  # noqa: E402


def maximum_support_matching(n: int, gates: list[MuxGate], indices: list[int]) -> int:
    match = [-1] * n

    def augment(gi: int, seen: set[int]) -> bool:
        gate = gates[gi]
        for v in (gate.selector, gate.data0, gate.data1):
            if v in seen:
                continue
            seen.add(v)
            if match[v] == -1 or augment(match[v], seen):
                match[v] = gi
                return True
        return False

    return sum(augment(gi, set()) for gi in indices)


def hall_minimality():
    rows = []
    for k in range(2, 31):
        n, gates = strict_single_scc_family(k)
        assert len(gates) == n + 1
        for deleted in range(len(gates)):
            remaining = [i for i in range(len(gates)) if i != deleted]
            assert maximum_support_matching(n, gates, remaining) == n, (k, deleted)
        rows.append((k, n, len(gates)))
    return rows


def local_backdoor_ok(gate: MuxGate, chosen: set[int]) -> bool:
    return gate.selector in chosen or (
        gate.data0 in chosen and gate.data1 in chosen
    )


def exact_beta(n: int, gates: list[MuxGate]) -> int:
    for size in range(n + 1):
        for subset in combinations(range(n), size):
            chosen = set(subset)
            if all(local_backdoor_ok(gate, chosen) for gate in gates):
                return size
    raise AssertionError("all variables form a backdoor")


def beta_checks():
    rows = {}
    for k in (2, 3, 4):
        n, gates = strict_single_scc_family(k)
        beta = exact_beta(n, gates)
        expected = 1 + 2 * ((k + 1) // 2)
        assert beta == expected, (k, beta, expected)
        rows[k] = {"n": n, "beta": beta}
    return rows


def strict_family_soundness():
    rows = []
    for k in range(2, 13):
        n, gates = strict_single_scc_family(k)
        assert branch_graph_strongly_connected(n, gates)
        result = find_double_cycle_or_bottleneck(n, gates)
        assert isinstance(result, DoubleCycleCertificate), (k, result)
        c0 = {gi for gi, _branch in result.cycle0}
        c1 = {gi for gi, _branch in result.cycle1}
        assert not (c0 & c1)
        alpha0 = gates[result.cycle0[0][0]].branch(result.cycle0[0][1])[2]
        alpha1 = gates[result.cycle1[0][0]].branch(result.cycle1[0][1])[2]
        assert alpha0 != alpha1
        y, meta = avoid_mux_double_cycle(n, gates)
        if n <= 15:
            assert not in_range(n, gates, y), (k, y, meta)
        rows.append({"k": k, "n": n, "m": len(gates), **meta})
    return rows


def v108_hierarchy_separation():
    # Exhaust every ignored-output set for the first three nontrivial members.
    # The theorem ledger gives the arbitrary-k structural proof.
    rows = {}
    for k in (2, 3, 4):
        n, gates = strict_single_scc_family(k)
        checked = 0
        for size in range(len(gates) + 1):
            for ignored_tuple in combinations(range(len(gates)), size):
                ignored = set(ignored_tuple)
                cert = v108_certificate(n, gates, ignored)
                assert cert is None, (k, ignored_tuple, cert)
                checked += 1
        assert checked == 1 << len(gates)
        rows[k] = checked
    return rows


def switched_family(gates: list[MuxGate], switch: tuple[int, ...], flips: tuple[int, ...]):
    out = []
    for i, gate in enumerate(gates):
        ps, p0, p1 = gate.polarity
        out.append(MuxGate(
            gate.selector,
            gate.data0,
            gate.data1,
            (
                ps ^ switch[gate.selector],
                p0 ^ switch[gate.data0],
                p1 ^ switch[gate.data1],
            ),
            gate.out_flip ^ flips[i],
        ))
    return out


def exhaustive_switching_k2():
    n, base = strict_single_scc_family(2)
    cases = 0
    for switch in product((0, 1), repeat=n):
        flips = tuple((sum(switch) + i) & 1 for i in range(len(base)))
        gates = switched_family(base, switch, flips)
        result = find_double_cycle_or_bottleneck(n, gates)
        assert isinstance(result, DoubleCycleCertificate), (switch, result)
        y, meta = avoid_mux_double_cycle(n, gates)
        assert not in_range(n, gates, y), (switch, y, meta)
        cases += 1
    assert cases == 32
    return cases


def path_exists_without_gate(
    n: int,
    gates: list[MuxGate],
    selector: int,
    start: int,
    removed_gate: int,
) -> bool:
    adjacency = [[] for _ in range(n)]
    for i, gate in enumerate(gates):
        if i == removed_gate or gate.selector == selector:
            continue
        adjacency[gate.selector].extend((gate.data0, gate.data1))
    seen = {start}
    stack = [start]
    while stack:
        u = stack.pop()
        if u == selector:
            return True
        for v in adjacency[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return False


def deterministic_bottleneck_control():
    # One repeated selector 0; both return cones can reach 0 only through gate 4.
    gates = [
        MuxGate(0, 1, 2),
        MuxGate(0, 1, 2),
        MuxGate(1, 3, 2),
        MuxGate(2, 3, 1),
        MuxGate(3, 0, 1),
    ]
    n = 4
    assert branch_graph_strongly_connected(n, gates)
    result = find_double_cycle_or_bottleneck(n, gates)
    assert isinstance(result, GateBottleneck), result
    assert result.bottleneck_gate == 4, result
    d0 = gates[result.first_gate0].branch(result.first_branch0)[1]
    d1 = gates[result.first_gate1].branch(result.first_branch1)[1]
    assert not path_exists_without_gate(n, gates, result.selector, d0, result.bottleneck_gate)
    assert not path_exists_without_gate(n, gates, result.selector, d1, result.bottleneck_gate)
    return {
        "selector": result.selector,
        "bottleneck_gate": result.bottleneck_gate,
        "first_gates": [result.first_gate0, result.first_gate1],
    }


def random_gate(rng: random.Random, n: int, selector: int) -> MuxGate:
    data = rng.sample([v for v in range(n) if v != selector], 2)
    return MuxGate(
        selector,
        data[0],
        data[1],
        tuple(rng.randrange(2) for _ in range(3)),
        rng.randrange(2),
    )


def random_strong_dichotomy():
    rng = random.Random(109109)
    strong = 0
    doubles = 0
    bottlenecks = 0
    sound = 0
    attempts = 0
    by_n = {}
    for n, target in ((4, 80), (5, 80), (6, 70), (7, 50)):
        accepted = 0
        while accepted < target and attempts < 20000:
            attempts += 1
            repeated = rng.randrange(n)
            gates = [random_gate(rng, n, s) for s in range(n)]
            gates.append(random_gate(rng, n, repeated))
            if not branch_graph_strongly_connected(n, gates):
                continue
            accepted += 1
            strong += 1
            result = find_double_cycle_or_bottleneck(n, gates)
            assert result is not None, (n, repeated)
            if isinstance(result, DoubleCycleCertificate):
                doubles += 1
                y, meta = avoid_mux_double_cycle(n, gates)
                assert not in_range(n, gates, y), (n, y, meta)
                sound += 1
            else:
                assert isinstance(result, GateBottleneck)
                bottlenecks += 1
                d0 = gates[result.first_gate0].branch(result.first_branch0)[1]
                d1 = gates[result.first_gate1].branch(result.first_branch1)[1]
                assert not path_exists_without_gate(
                    n, gates, result.selector, d0, result.bottleneck_gate
                )
                assert not path_exists_without_gate(
                    n, gates, result.selector, d1, result.bottleneck_gate
                )
            by_n[n] = by_n.get(n, 0) + 1
    assert strong == 280, (strong, attempts, by_n)
    assert doubles + bottlenecks == strong
    assert doubles >= 40, (doubles, bottlenecks)
    return {
        "strong_cases": strong,
        "double_cycle": doubles,
        "gate_bottleneck": bottlenecks,
        "double_cycle_soundness": sound,
        "by_n": by_n,
    }


def main():
    result = {
        "strict_family": strict_family_soundness(),
        "hall_minimality": hall_minimality(),
        "beta_small_exact": beta_checks(),
        "v108_no_certificate_all_ignored_subsets": v108_hierarchy_separation(),
        "signed_switchings_k2": exhaustive_switching_k2(),
        "deterministic_bottleneck": deterministic_bottleneck_control(),
        "random_strong_dichotomy": random_strong_dichotomy(),
        "failures": 0,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
