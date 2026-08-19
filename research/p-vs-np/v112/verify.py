from __future__ import annotations

import json
import random
import sys
from itertools import combinations, product
from pathlib import Path

from mux_phase_transfer import (
    PhaseTransferCertificate,
    avoid_mux_phase_transfer,
    find_phase_transfer_certificate,
    in_range,
    recognize_serial_chain,
    strict_phase_transfer_family,
)

V109_DIR = Path(__file__).resolve().parents[1] / "v109"
V110_DIR = Path(__file__).resolve().parents[1] / "v110"
V111_DIR = Path(__file__).resolve().parents[1] / "v111"
sys.path.insert(0, str(V109_DIR))
sys.path.insert(0, str(V110_DIR))
sys.path.insert(0, str(V111_DIR))
from mux_gate_flow import MuxGate  # noqa: E402
from mux_shared_gate import NestedBottleneck, find_shared_gate_certificate  # noqa: E402
from mux_min_overlap import find_min_overlap_certificate  # noqa: E402


def required_targets(gates, cycle):
    initial = gates[cycle[0][0]].branch(cycle[0][1])[2]
    out = {}
    for pos, (gi, branch) in enumerate(cycle):
        if pos + 1 < len(cycle):
            ng, nb = cycle[pos + 1]
            desired = gates[ng].branch(nb)[2]
        else:
            desired = 1 ^ initial
        target = gates[gi].target_for_arrival(branch, desired)
        if gi in out and out[gi] != target:
            return None
        out[gi] = target
    return out


def compatible(gates, c0, c1):
    t0 = required_targets(gates, c0)
    t1 = required_targets(gates, c1)
    if t0 is None or t1 is None:
        return False
    return all(t0[g] == t1[g] for g in set(t0) & set(t1))


def validate_cycle(gates, root, cycle):
    assert cycle
    for pos, (gi, branch) in enumerate(cycle):
        _s, dest, _alpha, _pd = gates[gi].branch(branch)
        if pos + 1 < len(cycle):
            next_gi, _next_branch = cycle[pos + 1]
            assert dest == gates[next_gi].selector, (pos, gi, dest, next_gi)
        else:
            assert dest == root, (pos, gi, dest, root)


def explicit_good_cycles(depth):
    c0 = [(0, 0), (2, 1)]
    c1 = [(1, 1), (5, 1), (4, 1)]
    for j in range(depth):
        h = 6 + 5 * j
        c0.extend(((h, 1), (h + 3, 1)))
        c1.extend(((h, 0), (h + 1, 0), (h + 2, 0)))
    return tuple(c0), tuple(c1)


def explicit_bad_cycles(depth):
    c0 = [(0, 0), (2, 1)]
    c1 = [(1, 1), (5, 0)]
    for j in range(depth):
        h = 6 + 5 * j
        c0.extend(((h, 0), (h + 1, 1)))
        c1.extend(((h, 1), (h + 3, 1)))
    return tuple(c0), tuple(c1)


def periodic_family_checks():
    rows = []
    for depth in range(1, 51):
        n, gates, shared = strict_phase_transfer_family(depth)
        chain = recognize_serial_chain(n, gates)
        assert chain is not None, depth
        assert len(chain.shared_gates) == depth
        cert = find_phase_transfer_certificate(n, gates)
        assert isinstance(cert, PhaseTransferCertificate), depth
        assert len(cert.shared_gates) == depth
        validate_cycle(gates, chain.root, cert.cycle0)
        validate_cycle(gates, chain.root, cert.cycle1)
        assert compatible(gates, cert.cycle0, cert.cycle1)
        y, meta = avoid_mux_phase_transfer(n, gates)
        assert y == cert.target
        assert meta["shared_hubs"] == depth
        if depth <= 2:
            assert not in_range(n, gates, y), (depth, y)

        good0, good1 = explicit_good_cycles(depth)
        bad0, bad1 = explicit_bad_cycles(depth)
        validate_cycle(gates, 0, good0)
        validate_cycle(gates, 0, good1)
        validate_cycle(gates, 0, bad0)
        validate_cycle(gates, 0, bad1)
        assert compatible(gates, good0, good1), depth
        assert not compatible(gates, bad0, bad1), depth
        assert len({gi for gi, _ in good0} & {gi for gi, _ in good1}) == depth
        assert len({gi for gi, _ in bad0} & {gi for gi, _ in bad1}) == depth

        # Current V111 deterministic minimum-cost decomposition is deliberately
        # a bad optimum on this periodic signing.  V112 searches the phase
        # transfer relation instead of treating that one optimum as canonical.
        assert find_min_overlap_certificate(n, gates) is None, depth
        if depth >= 2:
            assert isinstance(find_shared_gate_certificate(n, gates), NestedBottleneck)

        rows.append({"depth": depth, "n": n, "m": len(gates), "overlap": depth})
    return rows


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
    for depth in range(1, 31):
        n, gates, _shared = strict_phase_transfer_family(depth)
        for deleted in range(len(gates)):
            remaining = [i for i in range(len(gates)) if i != deleted]
            assert maximum_support_matching(n, gates, remaining) == n, (depth, deleted)
    return 30


def local_backdoor_ok(gate, chosen):
    return gate.selector in chosen or (gate.data0 in chosen and gate.data1 in chosen)


def exact_beta(n, gates):
    for size in range(n + 1):
        for subset in combinations(range(n), size):
            chosen = set(subset)
            if all(local_backdoor_ok(g, chosen) for g in gates):
                return size
    raise AssertionError("all variables form a backdoor")


def beta_small():
    rows = {}
    for depth in (1, 2):
        n, gates, _shared = strict_phase_transfer_family(depth)
        beta = exact_beta(n, gates)
        expected = 3 * (depth + 1)
        assert beta == expected, (depth, beta, expected)
        rows[depth] = {"n": n, "beta": beta}
    return rows


def renamed_and_reordered_controls():
    rng = random.Random(112)
    cases = 0
    n, base, _shared = strict_phase_transfer_family(1)
    for _ in range(24):
        perm = list(range(n))
        rng.shuffle(perm)
        gates = [
            MuxGate(
                perm[g.selector],
                perm[g.data0],
                perm[g.data1],
                g.polarity,
                g.out_flip,
            )
            for g in base
        ]
        rng.shuffle(gates)
        chain = recognize_serial_chain(n, gates)
        assert chain is not None
        found = find_phase_transfer_certificate(n, gates)
        assert found is not None
        assert not in_range(n, gates, found.target)
        cases += 1
    return cases


def random_signed_template_soundness():
    rng = random.Random(1112)
    checked = 0
    found_count = 0
    for _ in range(80):
        n, base, _shared = strict_phase_transfer_family(1)
        gates = [
            MuxGate(
                g.selector,
                g.data0,
                g.data1,
                tuple(rng.randrange(2) for _ in range(3)),
                rng.randrange(2),
            )
            for g in base
        ]
        cert = find_phase_transfer_certificate(n, gates)
        if cert is not None:
            assert not in_range(n, gates, cert.target)
            found_count += 1
        checked += 1
    assert found_count > 0
    return {"checked": checked, "certificates": found_count}


def main():
    result = {
        "periodic_family": periodic_family_checks(),
        "hall_minimal_depth_through": hall_minimality(),
        "beta_small_exact": beta_small(),
        "renamed_reordered_controls": renamed_and_reordered_controls(),
        "random_signed_template": random_signed_template_soundness(),
        "certificate": "serial_two_lobe_phase_transfer",
        "failures": 0,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
