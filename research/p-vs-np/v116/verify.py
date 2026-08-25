from __future__ import annotations

import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
V109_DIR = ROOT / "v109"
V113_DIR = ROOT / "v113"
V115_DIR = ROOT / "v115"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(V109_DIR))
sys.path.insert(0, str(V113_DIR))
sys.path.insert(0, str(V115_DIR))

from mux_gate_flow import MuxGate  # noqa: E402
from mux_dominator_dp import fixed_pair_minimum_overlap_certificate, in_range  # noqa: E402
from mux_dag_budget_one import fixed_pair_dag_budget_one_certificate  # noqa: E402
from mux_one_feedback_gate import (  # noqa: E402
    fixed_pair_one_feedback_budget_one_certificate,
    strict_tau_one_delta_one_family,
)


def target_word(gates, cycle0, cycle1):
    target = [0] * len(gates)
    assigned = {}
    for cycle in (cycle0, cycle1):
        initial = gates[cycle[0][0]].branch(cycle[0][1])[2]
        for pos, (gi, branch) in enumerate(cycle):
            if pos + 1 < len(cycle):
                ngi, nb = cycle[pos + 1]
                desired = gates[ngi].branch(nb)[2]
            else:
                desired = 1 ^ initial
            bit = gates[gi].target_for_arrival(branch, desired)
            if gi in assigned and assigned[gi] != bit:
                return None
            assigned[gi] = bit
            target[gi] = bit
    return tuple(target)


def enumerate_returns(n, gates, root, start, cap=4000):
    by_selector = {}
    for gi, gate in enumerate(gates):
        if gate.selector != root:
            by_selector.setdefault(gate.selector, []).append(gi)
    found = []

    def dfs(vertex, used, path):
        if len(found) >= cap:
            return
        if vertex == root:
            found.append(tuple(path))
            return
        for gi in by_selector.get(vertex, ()):
            if gi in used:
                continue
            gate = gates[gi]
            for branch, dest in enumerate((gate.data0, gate.data1)):
                dfs(dest, used | {gi}, path + [(gi, branch)])

    dfs(start, set(), [])
    if len(found) >= cap:
        raise AssertionError("route census cap reached")
    return found


def brute_fixed_pair(n, gates, root, first0, first1):
    dest0 = gates[first0].branch(0)[1]
    dest1 = gates[first1].branch(0)[1]
    returns0 = enumerate_returns(n, gates, root, dest0)
    returns1 = enumerate_returns(n, gates, root, dest1)
    min_overlap = None
    min_compatible = None
    for route0 in returns0:
        used0 = {gi for gi, _ in route0}
        for route1 in returns1:
            overlap = len(used0 & {gi for gi, _ in route1})
            if min_overlap is None or overlap < min_overlap:
                min_overlap = overlap
            target = target_word(
                gates,
                ((first0, 0),) + route0,
                ((first1, 0),) + route1,
            )
            if target is not None and (
                min_compatible is None or overlap < min_compatible
            ):
                min_compatible = overlap
    return min_overlap, min_compatible


def random_tau_one_instance(seed):
    rng = random.Random(seed)
    n = 7
    root = 0
    gates = [
        MuxGate(root, 1, 6, (0, 0, 0), rng.randrange(2)),
        MuxGate(root, 2, 6, (1, 0, 0), rng.randrange(2)),
    ]
    for selector in range(1, 6):
        gates.append(
            MuxGate(
                selector,
                selector + 1,
                root,
                tuple(rng.randrange(2) for _ in range(3)),
                rng.randrange(2),
            )
        )
    for _ in range(2):
        selector = rng.randint(1, 4)
        d0, d1 = rng.sample(list(range(selector + 1, 7)), 2)
        gates.append(
            MuxGate(
                selector,
                d0,
                d1,
                tuple(rng.randrange(2) for _ in range(3)),
                rng.randrange(2),
            )
        )
    if seed % 2 == 0:
        selector = rng.randint(3, 5)
        lower = rng.randint(1, selector - 1)
        gates.append(
            MuxGate(
                selector,
                lower,
                root,
                tuple(rng.randrange(2) for _ in range(3)),
                rng.randrange(2),
            )
        )
    return n, gates


def check_seeded_crosscheck():
    checked = 0
    for seed in range(300):
        n, gates = random_tau_one_instance(seed)
        brute_min, brute_compatible = brute_fixed_pair(n, gates, 0, 0, 1)
        try:
            cert = fixed_pair_one_feedback_budget_one_certificate(
                n, gates, 0, 0, 0, 1, 0
            )
        except ValueError:
            continue
        expected = (
            brute_min is not None
            and brute_compatible is not None
            and brute_compatible <= brute_min + 1
        )
        assert (cert is not None) == expected, (
            seed,
            brute_min,
            brute_compatible,
            cert,
        )
        if cert is not None:
            assert target_word(gates, cert.cycle0, cert.cycle1) == cert.target
            assert len(cert.overlap) <= len(cert.common_gates) + 1
        checked += 1
    assert checked >= 250
    return checked


def check_strict_family():
    for depth in range(41):
        n, gates, ids = strict_tau_one_delta_one_family(depth)
        first0, first1, common_gate, feedback_extra, cycle_gate = ids
        assert len(gates) == n + 1
        root = gates[first0].selector
        cert = fixed_pair_one_feedback_budget_one_certificate(
            n, gates, root, first0, 0, first1, 0
        )
        assert cert is not None
        assert cert.delta == 1
        assert cert.extra_gate == feedback_extra
        assert common_gate in cert.common_gates
        assert feedback_extra in cert.overlap
        assert cycle_gate not in cert.overlap
        assert cert.feedback_gates[-1] == feedback_extra
        assert target_word(gates, cert.cycle0, cert.cycle1) == cert.target

        assert (
            fixed_pair_minimum_overlap_certificate(
                n, gates, root, first0, 0, first1, 0
            )
            is None
        )
        try:
            fixed_pair_dag_budget_one_certificate(
                n, gates, root, first0, 0, first1, 0
            )
        except ValueError:
            pass
        else:
            raise AssertionError("V115 accepted a cyclic V116 strict family")

    n, gates, ids = strict_tau_one_delta_one_family(0)
    first0, first1, _common, _extra, _cycle = ids
    brute_min, brute_compatible = brute_fixed_pair(
        n, gates, gates[first0].selector, first0, first1
    )
    assert brute_min == 1
    assert brute_compatible == 2
    cert = fixed_pair_one_feedback_budget_one_certificate(
        n, gates, gates[first0].selector, first0, 0, first1, 0
    )
    assert cert is not None
    assert not in_range(n, gates, cert.target)


def main():
    checked = check_seeded_crosscheck()
    check_strict_family()
    print(
        "V116 primary verifier passed: "
        f"{checked} seeded tau<=1 fixed pairs cross-checked; "
        "strict cyclic Delta=1 family verified through depth 40."
    )


if __name__ == "__main__":
    main()
