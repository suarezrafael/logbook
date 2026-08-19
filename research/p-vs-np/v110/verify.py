from __future__ import annotations

import json
import sys
from itertools import combinations, product
from pathlib import Path

from mux_shared_gate import (
    SharedGateCertificate,
    avoid_mux_shared_gate,
    find_shared_gate_certificate,
    in_range,
    strict_shared_bottleneck_family,
)

V109_DIR = Path(__file__).resolve().parents[1] / "v109"
V108_DIR = Path(__file__).resolve().parents[1] / "v108"
sys.path.insert(0, str(V109_DIR))
sys.path.insert(0, str(V108_DIR))
from mux_gate_flow import GateBottleneck, MuxGate, find_double_cycle_or_bottleneck  # noqa: E402
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


def hall_minimality() -> list[tuple[int, int, int]]:
    rows = []
    for k in range(2, 21):
        n, gates, _h = strict_shared_bottleneck_family(k)
        assert len(gates) == n + 1
        for deleted in range(len(gates)):
            remaining = [i for i in range(len(gates)) if i != deleted]
            assert maximum_support_matching(n, gates, remaining) == n, (k, deleted)
        rows.append((k, n, len(gates)))
    return rows


def local_backdoor_ok(gate: MuxGate, chosen: set[int]) -> bool:
    return gate.selector in chosen or (gate.data0 in chosen and gate.data1 in chosen)


def exact_beta(n: int, gates: list[MuxGate]) -> int:
    for size in range(n + 1):
        for subset in combinations(range(n), size):
            chosen = set(subset)
            if all(local_backdoor_ok(g, chosen) for g in gates):
                return size
    raise AssertionError("all variables form a backdoor")


def beta_small() -> dict[int, dict[str, int]]:
    rows = {}
    for k in (2, 3):
        n, gates, _h = strict_shared_bottleneck_family(k)
        beta = exact_beta(n, gates)
        expected = 2 + 4 * ((k + 1) // 2)
        assert beta == expected, (k, beta, expected)
        rows[k] = {"n": n, "beta": beta}
    return rows


def strict_family_soundness() -> list[dict[str, object]]:
    rows = []
    for k in range(2, 11):
        n, gates, intended_h = strict_shared_bottleneck_family(k)
        old = find_double_cycle_or_bottleneck(n, gates)
        assert isinstance(old, GateBottleneck), (k, old)
        cert = find_shared_gate_certificate(n, gates)
        assert isinstance(cert, SharedGateCertificate), (k, cert)
        assert cert.shared_gate == intended_h, (k, cert.shared_gate, intended_h)
        assert cert.shared_target in (0, 1)
        overlap = {gi for gi, _ in cert.cycle0} & {gi for gi, _ in cert.cycle1}
        assert overlap == {intended_h}, (k, overlap, intended_h)
        y, meta = avoid_mux_shared_gate(n, gates)
        if n <= 14:
            assert not in_range(n, gates, y), (k, y, meta)
        rows.append({"k": k, "n": n, "m": len(gates), **meta})
    return rows


def v108_separation() -> dict[int, int]:
    rows = {}
    for k in (2, 3):
        n, gates, _h = strict_shared_bottleneck_family(k)
        checks = 0
        for mask in range(1 << len(gates)):
            ignored = {i for i in range(len(gates)) if (mask >> i) & 1}
            assert v108_certificate(n, gates, ignored) is None, (k, ignored)
            checks += 1
        rows[k] = checks
    return rows


def switched_family(
    gates: list[MuxGate],
    switch: tuple[int, ...],
    flips: tuple[int, ...],
) -> list[MuxGate]:
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


def signed_switching_k2() -> int:
    n, base, intended_h = strict_shared_bottleneck_family(2)
    cases = 0
    # Exhaust a six-dimensional switching slice; every witness is checked
    # against the complete original image of the signed circuit.
    for prefix in product((0, 1), repeat=6):
        switch = prefix + (0,) * (n - 6)
        flips = tuple((sum(prefix) + i) & 1 for i in range(len(base)))
        gates = switched_family(base, switch, flips)
        old = find_double_cycle_or_bottleneck(n, gates)
        assert isinstance(old, GateBottleneck), (switch, old)
        cert = find_shared_gate_certificate(n, gates)
        assert isinstance(cert, SharedGateCertificate), (switch, cert)
        assert cert.shared_gate == intended_h
        y, meta = avoid_mux_shared_gate(n, gates)
        assert not in_range(n, gates, y), (switch, y, meta)
        cases += 1
    assert cases == 64
    return cases


def main() -> None:
    result = {
        "strict_family": strict_family_soundness(),
        "hall_minimality": hall_minimality(),
        "beta_small_exact": beta_small(),
        "v108_no_certificate_all_ignored_subsets": v108_separation(),
        "signed_switching_k2": signed_switching_k2(),
        "certificate": "phase_compatible_single_shared_gate_double_cycle",
        "failures": 0,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
