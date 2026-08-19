from __future__ import annotations

import json
import sys
from itertools import combinations, product
from pathlib import Path

from mux_min_overlap import (
    MinOverlapCertificate,
    avoid_mux_min_overlap,
    find_min_overlap_certificate,
    in_range,
    strict_nested_chain_family,
)

V108_DIR = Path(__file__).resolve().parents[1] / "v108"
V109_DIR = Path(__file__).resolve().parents[1] / "v109"
V110_DIR = Path(__file__).resolve().parents[1] / "v110"
sys.path.insert(0, str(V108_DIR))
sys.path.insert(0, str(V109_DIR))
sys.path.insert(0, str(V110_DIR))
from mux_scc_bridge import find_scc_bridge_certificate as v108_certificate  # noqa: E402
from mux_gate_flow import GateBottleneck, MuxGate, find_double_cycle_or_bottleneck  # noqa: E402
from mux_shared_gate import NestedBottleneck, SharedGateCertificate, find_shared_gate_certificate  # noqa: E402


def maximum_support_matching(n, gates, indices):
    match = [-1] * n

    def augment(gi, seen):
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
    for depth in range(1, 21):
        n, gates, _shared = strict_nested_chain_family(2, depth)
        assert n == 5 * (depth + 1)
        assert len(gates) == n + 1
        for deleted in range(len(gates)):
            remaining = [i for i in range(len(gates)) if i != deleted]
            assert maximum_support_matching(n, gates, remaining) == n, (depth, deleted)
        rows.append((depth, n))
    return rows


def local_backdoor_ok(gate, chosen):
    return gate.selector in chosen or (gate.data0 in chosen and gate.data1 in chosen)


def exact_beta(n, gates):
    for size in range(n + 1):
        for subset in combinations(range(n), size):
            chosen = set(subset)
            if all(local_backdoor_ok(g, chosen) for g in gates):
                return size
    raise AssertionError("all variables must form a backdoor")


def beta_small_exact():
    rows = {}
    for depth in (1, 2):
        n, gates, _shared = strict_nested_chain_family(2, depth)
        beta = exact_beta(n, gates)
        expected = 3 * (depth + 1)
        assert beta == expected, (depth, beta, expected)
        rows[depth] = {"n": n, "beta": beta}
    return rows


def strict_family_soundness():
    rows = []
    for depth in range(1, 11):
        n, gates, intended_shared = strict_nested_chain_family(2, depth)
        found = find_min_overlap_certificate(n, gates)
        assert found is not None, depth
        cert, target = found
        assert isinstance(cert, MinOverlapCertificate)
        assert cert.overlap_cost == depth, (depth, cert.overlap_cost)
        assert set(cert.shared_gates) == set(intended_shared), (
            depth,
            cert.shared_gates,
            intended_shared,
        )
        target2, meta = avoid_mux_min_overlap(n, gates)
        assert target2 == target
        assert meta["overlap_cost"] == depth
        if depth <= 2:
            assert not in_range(n, gates, target), (depth, target, meta)

        old = find_double_cycle_or_bottleneck(n, gates)
        assert isinstance(old, GateBottleneck), (depth, old)
        v110 = find_shared_gate_certificate(n, gates)
        if depth == 1:
            assert isinstance(v110, SharedGateCertificate), (depth, v110)
        else:
            assert isinstance(v110, NestedBottleneck), (depth, v110)

        rows.append(
            {
                "depth": depth,
                "n": n,
                "m": len(gates),
                "overlap_cost": cert.overlap_cost,
                "shared_gates": len(cert.shared_gates),
                "v110_case": type(v110).__name__,
            }
        )
    return rows


def v108_first_depths_absent():
    rows = {}
    for depth in (1, 2):
        n, gates, _shared = strict_nested_chain_family(2, depth)
        checks = 0
        for mask in range(1 << len(gates)):
            ignored = {i for i in range(len(gates)) if (mask >> i) & 1}
            assert v108_certificate(n, gates, ignored) is None, (depth, ignored)
            checks += 1
        rows[depth] = checks
    return rows


def switched_family(gates, switch, flips):
    out = []
    for i, gate in enumerate(gates):
        ps, p0, p1 = gate.polarity
        out.append(
            MuxGate(
                gate.selector,
                gate.data0,
                gate.data1,
                (
                    ps ^ switch[gate.selector],
                    p0 ^ switch[gate.data0],
                    p1 ^ switch[gate.data1],
                ),
                gate.out_flip ^ flips[i],
            )
        )
    return out


def signed_switching_depth1():
    n, base, _shared = strict_nested_chain_family(2, 1)
    cases = 0
    for prefix in product((0, 1), repeat=4):
        switch = prefix + (0,) * (n - 4)
        flips = tuple((sum(prefix) + i) & 1 for i in range(len(base)))
        gates = switched_family(base, switch, flips)
        found = find_min_overlap_certificate(n, gates)
        assert found is not None, prefix
        cert, target = found
        assert cert.overlap_cost == 1
        assert not in_range(n, gates, target), (prefix, target)
        cases += 1
    assert cases == 16
    return cases


def main():
    result = {
        "strict_family": strict_family_soundness(),
        "hall_minimality": hall_minimality(),
        "beta_small_exact": beta_small_exact(),
        "v108_exhaustive_absence_first_depths": v108_first_depths_absent(),
        "signed_switching_depth1": signed_switching_depth1(),
        "certificate": "target_compatible_minimum_overlap_two_flow",
        "failures": 0,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
