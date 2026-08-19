from __future__ import annotations

import json
import random
import sys
from collections import defaultdict
from itertools import combinations, product
from pathlib import Path

from mux_dominator_dp import (
    DominatorDPCertificate,
    common_gate_dominator_chain,
    find_minimum_overlap_certificate,
    fixed_pair_minimum_overlap_certificate,
    in_range,
    strict_nonserial_optimum_family,
)

V111_DIR = Path(__file__).resolve().parents[1] / "v111"
V112_DIR = Path(__file__).resolve().parents[1] / "v112"
sys.path.insert(0, str(V111_DIR))
sys.path.insert(0, str(V112_DIR))
from mux_min_overlap import find_min_overlap_certificate as v111_certificate  # noqa: E402
from mux_phase_transfer import recognize_serial_chain as v112_recognize  # noqa: E402

V109_DIR = Path(__file__).resolve().parents[1] / "v109"
sys.path.insert(0, str(V109_DIR))
from mux_gate_flow import MuxGate  # noqa: E402


def target_word(gates, cycle0, cycle1):
    targets = [0] * len(gates)
    assigned = {}
    for cycle in (cycle0, cycle1):
        if not cycle:
            return None
        initial = gates[cycle[0][0]].branch(cycle[0][1])[2]
        for pos, (gi, branch) in enumerate(cycle):
            if pos + 1 < len(cycle):
                ngi, nb = cycle[pos + 1]
                desired = gates[ngi].branch(nb)[2]
            else:
                desired = 1 ^ initial
            t = gates[gi].target_for_arrival(branch, desired)
            if gi in assigned and assigned[gi] != t:
                return None
            assigned[gi] = t
            targets[gi] = t
    return tuple(targets)


def enumerate_gate_simple_paths(n, gates, root, start, limit=3000):
    allowed = [i for i, g in enumerate(gates) if g.selector != root]
    by_selector = defaultdict(list)
    for gi in allowed:
        by_selector[gates[gi].selector].append(gi)
    paths = []

    def dfs(var, path, used):
        if len(paths) >= limit:
            return
        if var == root:
            paths.append(tuple(path))
            return
        if len(path) >= len(allowed):
            return
        for gi in by_selector[var]:
            if gi in used:
                continue
            gate = gates[gi]
            for branch in (0, 1):
                dest = gate.branch(branch)[1]
                dfs(dest, path + [(gi, branch)], used | {gi})

    dfs(start, [], set())
    return list(dict.fromkeys(paths)), len(paths) >= limit


def brute_fixed_pair(n, gates, selector, g0, b0, g1, b1):
    d0 = gates[g0].branch(b0)[1]
    d1 = gates[g1].branch(b1)[1]
    paths0, capped0 = enumerate_gate_simple_paths(n, gates, selector, d0)
    paths1, capped1 = enumerate_gate_simple_paths(n, gates, selector, d1)
    if capped0 or capped1 or not paths0 or not paths1:
        return None
    best = len(gates) + 1
    compatible = False
    for p0 in paths0:
        used0 = {gi for gi, _ in p0}
        for p1 in paths1:
            overlap = len(used0 & {gi for gi, _ in p1})
            if overlap < best:
                best = overlap
                compatible = False
            if overlap == best:
                c0 = ((g0, b0),) + p0
                c1 = ((g1, b1),) + p1
                if target_word(gates, c0, c1) is not None:
                    compatible = True
    return best, compatible


def random_mux(n, m, rng):
    gates = []
    for _ in range(m):
        s, a, b = rng.sample(range(n), 3)
        polarity = tuple(rng.randrange(2) for _ in range(3))
        gates.append(MuxGate(s, a, b, polarity, rng.randrange(2)))
    return gates


def brute_crosscheck():
    rng = random.Random(113)
    compared = 0
    overlap_checks = 0
    compatible_checks = 0
    for n in range(3, 7):
        for _ in range(120):
            gates = random_mux(n, n + 1, rng)
            by_selector = defaultdict(list)
            for gi, gate in enumerate(gates):
                by_selector[gate.selector].append(gi)
            candidates = []
            for selector, ids in by_selector.items():
                for g0, g1 in combinations(ids, 2):
                    for b0, b1 in product((0, 1), repeat=2):
                        if gates[g0].branch(b0)[2] != gates[g1].branch(b1)[2]:
                            candidates.append((selector, g0, b0, g1, b1))
            rng.shuffle(candidates)
            for selector, g0, b0, g1, b1 in candidates[:4]:
                brute = brute_fixed_pair(n, gates, selector, g0, b0, g1, b1)
                if brute is None:
                    continue
                best, has_compatible = brute
                d0 = gates[g0].branch(b0)[1]
                d1 = gates[g1].branch(b1)[1]
                structure = common_gate_dominator_chain(n, gates, selector, d0, d1)
                assert structure is not None
                common, _stage, _allowed = structure
                assert best == len(common), (n, best, common)
                overlap_checks += 1
                cert = fixed_pair_minimum_overlap_certificate(
                    n, gates, selector, g0, b0, g1, b1
                )
                assert (cert is not None) == has_compatible, (
                    n,
                    selector,
                    g0,
                    b0,
                    g1,
                    b1,
                    best,
                    has_compatible,
                )
                if cert is not None:
                    assert len(cert.overlap) == best
                    assert cert.target is not None
                    compatible_checks += 1
                compared += 1
    assert compared >= 500
    return {
        "fixed_pairs": compared,
        "minimum_overlap_checks": overlap_checks,
        "compatible_optimum_checks": compatible_checks,
    }


def explicit_good_cycles(depth):
    c0 = [(0, 0), (2, 1)]
    c1 = [(1, 0), (3, 0), (4, 0)]
    for j in range(depth):
        h = 8 + 7 * j
        c0.extend(((h, 0), (h + 1, 0), (h + 2, 0), (h + 3, 0)))
        c1.extend(((h, 1), (h + 4, 1)))
    return tuple(c0), tuple(c1)


def explicit_bad_cycles(depth):
    c0 = [(0, 0), (2, 1)]
    c1 = [(1, 0), (3, 0), (4, 0)]
    for j in range(depth):
        h = 8 + 7 * j
        c0.extend(((h, 0), (h + 1, 0), (h + 2, 0), (h + 3, 0)))
        c1.extend(((h, 1), (h + 4, 0), (h + 5, 0), (h + 6, 0)))
    return tuple(c0), tuple(c1)


def validate_cycle(gates, root, cycle):
    for pos, (gi, branch) in enumerate(cycle):
        dest = gates[gi].branch(branch)[1]
        if pos + 1 < len(cycle):
            assert dest == gates[cycle[pos + 1][0]].selector, (pos, gi, dest)
        else:
            assert dest == root, (pos, gi, dest, root)


def strict_family_checks():
    rows = []
    for depth in range(1, 31):
        n, gates, shared = strict_nonserial_optimum_family(depth)
        assert n == 7 * (depth + 1)
        assert len(gates) == n + 1
        assert v112_recognize(n, gates) is None

        cert = fixed_pair_minimum_overlap_certificate(n, gates, 0, 0, 0, 1, 0)
        assert isinstance(cert, DominatorDPCertificate), depth
        assert cert.common_gates == shared, (depth, cert.common_gates, shared)
        assert len(cert.overlap) == depth
        if depth == 1:
            assert not in_range(n, gates, cert.target), cert.target

        good0, good1 = explicit_good_cycles(depth)
        bad0, bad1 = explicit_bad_cycles(depth)
        validate_cycle(gates, 0, good0)
        validate_cycle(gates, 0, good1)
        validate_cycle(gates, 0, bad0)
        validate_cycle(gates, 0, bad1)
        assert target_word(gates, good0, good1) is not None
        assert target_word(gates, bad0, bad1) is None
        assert len({gi for gi, _ in good0} & {gi for gi, _ in good1}) == depth
        assert len({gi for gi, _ in bad0} & {gi for gi, _ in bad1}) == depth

        # Finite implementation audit only: the current V111 deterministic
        # optimum decomposition is incompatible on this periodic signing.
        if depth <= 20:
            assert v111_certificate(n, gates) is None, depth

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
    for depth in range(1, 21):
        n, gates, _shared = strict_nonserial_optimum_family(depth)
        for deleted in range(len(gates)):
            remaining = [i for i in range(len(gates)) if i != deleted]
            assert maximum_support_matching(n, gates, remaining) == n, (depth, deleted)
    return 20


def local_backdoor_ok(gate, chosen):
    return gate.selector in chosen or (gate.data0 in chosen and gate.data1 in chosen)


def exact_beta_small():
    n, gates, _shared = strict_nonserial_optimum_family(1)
    expected = 10
    for size in range(expected):
        for subset in combinations(range(n), size):
            chosen = set(subset)
            assert not all(local_backdoor_ok(g, chosen) for g in gates)
    found = False
    for subset in combinations(range(n), expected):
        chosen = set(subset)
        if all(local_backdoor_ok(g, chosen) for g in gates):
            found = True
            break
    assert found
    assert expected * 7 == 5 * n
    return {"n": n, "beta": expected}


def malformed_controls():
    n, gates, _shared = strict_nonserial_optimum_family(1)
    bad = list(gates)
    g = bad[0]
    bad[0] = MuxGate(n, g.data0, g.data1, g.polarity, g.out_flip)
    assert find_minimum_overlap_certificate(n, bad) is None
    return 1


def main():
    result = {
        "brute_crosscheck": brute_crosscheck(),
        "strict_nonserial_family": strict_family_checks(),
        "hall_minimal_depth_through": hall_minimality(),
        "beta_small_exact": exact_beta_small(),
        "malformed_controls": malformed_controls(),
        "certificate": "common_gate_dominator_minimum_overlap_dp",
        "failures": 0,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
