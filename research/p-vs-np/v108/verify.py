from __future__ import annotations

import json
import random
from itertools import combinations, product

from mux_scc_bridge import (
    MuxGate,
    avoid_mux_scc_bridge,
    find_scc_bridge_certificate,
    in_range,
    strict_two_cycle_family,
)


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

    size = 0
    for gi in indices:
        if augment(gi, set()):
            size += 1
    return size


def hall_minimality_checks():
    rows = []
    for k in range(3, 31):
        n, gates = strict_two_cycle_family(k)
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
            if all(local_backdoor_ok(g, chosen) for g in gates):
                return size
    raise AssertionError("all inputs form a backdoor")


def exact_beta_small():
    rows = {}
    for k in (3, 6):
        n, gates = strict_two_cycle_family(k)
        beta = exact_beta(n, gates)
        assert beta == 2 * n // 3
        rows[k] = {"n": n, "beta": beta}
    return rows


def strict_family_soundness():
    rows = []
    for k in range(3, 13):
        n, gates = strict_two_cycle_family(k)
        cert = find_scc_bridge_certificate(n, gates)
        assert cert is not None
        y, meta = avoid_mux_scc_bridge(n, gates)
        assert meta["deleted_outputs"] == 0
        if n <= 16:
            assert not in_range(n, gates, y), (k, y, meta)
        rows.append({
            "k": k,
            "n": n,
            "m": len(gates),
            "left_cycle": meta["left_cycle_outputs"],
            "right_cycle": meta["right_cycle_outputs"],
        })
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


def exhaustive_global_switching_k3():
    n, base = strict_two_cycle_family(3)
    cases = 0
    for switch in product((0, 1), repeat=n):
        # Output negations do not affect the branch digraph.  Vary them
        # deterministically so every input switching is tested with a signed target.
        flips = tuple((sum(switch) + i) & 1 for i in range(len(base)))
        gates = switched_family(base, switch, flips)
        cert = find_scc_bridge_certificate(n, gates)
        assert cert is not None, switch
        y, meta = avoid_mux_scc_bridge(n, gates)
        assert not in_range(n, gates, y), (switch, y, meta)
        cases += 1
    assert cases == 64
    return cases


def random_gate(rng: random.Random, n: int) -> MuxGate:
    selector, data0, data1 = rng.sample(range(n), 3)
    return MuxGate(
        selector,
        data0,
        data1,
        tuple(rng.randrange(2) for _ in range(3)),
        rng.randrange(2),
    )


def random_certificate_soundness():
    rng = random.Random(108108)
    checked = 0
    found = 0
    by_n = {}
    for n, trials in ((4, 220), (5, 200), (6, 160), (7, 100)):
        for _ in range(trials):
            m = n + 1 + rng.randrange(2)
            gates = [random_gate(rng, n) for _ in range(m)]
            cert = find_scc_bridge_certificate(n, gates)
            checked += 1
            if cert is None:
                continue
            y, meta = avoid_mux_scc_bridge(n, gates)
            assert not in_range(n, gates, y), (n, y, meta)
            found += 1
            by_n[n] = by_n.get(n, 0) + 1
    # This is a soundness test rather than a coverage theorem. Dense random
    # branch digraphs often collapse into one SCC, precisely the residual class
    # that V108 does not claim to solve. Still require a reproducibly non-vacuous
    # set of certificates across several sizes so detector disablement fails CI.
    assert found >= 20, (checked, found, by_n)
    assert len(by_n) >= 3, (checked, found, by_n)
    return {"checked": checked, "certificates": found, "by_n": by_n}


def main():
    result = {
        "strict_family": strict_family_soundness(),
        "hall_minimality": hall_minimality_checks(),
        "exact_beta_small": exact_beta_small(),
        "global_switching_k3": exhaustive_global_switching_k3(),
        "random_soundness": random_certificate_soundness(),
        "parameter": "kappa_SCC_deleted_outputs",
        "runtime_kappa_zero": "poly(N)",
        "runtime_fixed_k": "O(m^k poly(N))",
        "failures": 0,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
