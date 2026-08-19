from __future__ import annotations

import sys
from collections import deque
from dataclasses import dataclass
from itertools import combinations, product
from pathlib import Path

V109_DIR = Path(__file__).resolve().parents[1] / "v109"
sys.path.insert(0, str(V109_DIR))
from mux_gate_flow import FlowNetwork, MuxGate  # noqa: E402


@dataclass(frozen=True)
class DominatorDPCertificate:
    selector: int
    first_gate0: int
    first_branch0: int
    first_gate1: int
    first_branch1: int
    common_gates: tuple[int, ...]
    return_path0: tuple[tuple[int, int], ...]
    return_path1: tuple[tuple[int, int], ...]
    target: tuple[int, ...]

    @property
    def cycle0(self) -> tuple[tuple[int, int], ...]:
        return ((self.first_gate0, self.first_branch0),) + self.return_path0

    @property
    def cycle1(self) -> tuple[tuple[int, int], ...]:
        return ((self.first_gate1, self.first_branch1),) + self.return_path1

    @property
    def overlap(self) -> tuple[int, ...]:
        return tuple(sorted({gi for gi, _ in self.return_path0} & {gi for gi, _ in self.return_path1}))


def _valid_instance(n: int, gates: list[MuxGate]) -> bool:
    if n <= 0:
        return False
    return all(
        0 <= x < n
        for gate in gates
        for x in (gate.selector, gate.data0, gate.data1)
    )


def _allowed_return_gates(gates: list[MuxGate], root: int) -> tuple[int, ...]:
    return tuple(i for i, gate in enumerate(gates) if gate.selector != root)


def _reachable(
    n: int,
    gates: list[MuxGate],
    root: int,
    start: int,
    allowed: tuple[int, ...],
    banned_gate: int | None = None,
) -> bool:
    if start == root:
        return True
    adjacency = [[] for _ in range(n)]
    for gi in allowed:
        if gi == banned_gate:
            continue
        gate = gates[gi]
        adjacency[gate.selector].append(gate.data0)
        adjacency[gate.selector].append(gate.data1)
    seen = {start}
    stack = [start]
    while stack:
        u = stack.pop()
        for v in adjacency[u]:
            if v == root:
                return True
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return False


def common_gate_dominator_chain(
    n: int,
    gates: list[MuxGate],
    root: int,
    dest0: int,
    dest1: int,
) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]] | None:
    """Return source-to-sink common gate dominators, variable stages, allowed gates.

    The implementation intentionally uses repeated reachability rather than a
    sophisticated dominator algorithm.  This is slower but simple and still
    polynomial; the theorem ledger records the standard dominator-tree view.
    """
    if not _valid_instance(n, gates) or not (0 <= root < n):
        return None
    allowed = _allowed_return_gates(gates, root)
    if not _reachable(n, gates, root, dest0, allowed):
        return None
    if not _reachable(n, gates, root, dest1, allowed):
        return None

    common = tuple(
        gi
        for gi in allowed
        if not _reachable(n, gates, root, dest0, allowed, gi)
        and not _reachable(n, gates, root, dest1, allowed, gi)
    )
    if not common:
        return (), (0,) * n, allowed

    # Common dominators lie on one chain.  For a common gate h, every common
    # gate closer to the sink disconnects selector(h) from the sink.  The number
    # of such dominators therefore gives its source-to-sink position.
    dominated_by: dict[int, frozenset[int]] = {}
    for h in common:
        selector = gates[h].selector
        dominated_by[h] = frozenset(
            k
            for k in common
            if not _reachable(n, gates, root, selector, allowed, k)
        )

    ordered = tuple(sorted(common, key=lambda h: (-len(dominated_by[h]), h)))
    d = len(ordered)
    if tuple(len(dominated_by[h]) for h in ordered) != tuple(range(d, 0, -1)):
        return None
    for j, h in enumerate(ordered):
        if dominated_by[h] != frozenset(ordered[j:]):
            return None

    stage: list[int] = []
    for x in range(n):
        value = d
        for j, h in enumerate(ordered):
            if not _reachable(n, gates, root, x, allowed, h):
                value = j
                break
        stage.append(value)
    if any(stage[gates[h].selector] != j for j, h in enumerate(ordered)):
        return None
    return ordered, tuple(stage), allowed


def _flow_paths(
    n: int,
    gates: list[MuxGate],
    allowed_gates: set[int],
    starts: tuple[int, int],
    sink: int,
) -> tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]] | None:
    active = [i for i, start in enumerate(starts) if start != sink]
    decoded: dict[int, tuple[tuple[int, int], ...]] = {
        i: () for i, start in enumerate(starts) if start == sink
    }
    if not active:
        return decoded[0], decoded[1]

    ordered = tuple(sorted(allowed_gates))
    gate_pos = {gi: pos for pos, gi in enumerate(ordered)}
    source = n + 2 * len(ordered)
    net = FlowNetwork(source + 1)
    for gi in ordered:
        pos = gate_pos[gi]
        gin = n + 2 * pos
        gout = gin + 1
        gate = gates[gi]
        net.add_edge(gate.selector, gin, 2)
        net.add_edge(gin, gout, 1, ("gate", gi))
        net.add_edge(gout, gate.data0, 2, ("branch", gi, 0))
        net.add_edge(gout, gate.data1, 2, ("branch", gi, 1))
    for route in active:
        net.add_edge(source, starts[route], 1, ("source", route))

    if net.max_flow(source, sink, len(active)) != len(active):
        return None
    raw = net.positive_flow_paths(source, sink, len(active))
    for path in raw:
        tags = [meta for meta in path if meta and meta[0] == "source"]
        if len(tags) != 1:
            raise AssertionError("local flow path lost its source label")
        route = tags[0][1]
        decoded[route] = tuple(
            (meta[1], meta[2])
            for meta in path
            if meta and meta[0] == "branch"
        )
    if set(decoded) != {0, 1}:
        raise AssertionError("local two-flow did not decode both routes")
    return decoded[0], decoded[1]


def _target_word(
    gates: list[MuxGate],
    cycle0: tuple[tuple[int, int], ...],
    cycle1: tuple[tuple[int, int], ...],
) -> tuple[int, ...] | None:
    targets = [0] * len(gates)
    assigned: dict[int, int] = {}
    for cycle in (cycle0, cycle1):
        if not cycle:
            return None
        initial = gates[cycle[0][0]].branch(cycle[0][1])[2]
        for pos, (gi, branch) in enumerate(cycle):
            if pos + 1 < len(cycle):
                next_gi, next_branch = cycle[pos + 1]
                desired = gates[next_gi].branch(next_branch)[2]
            else:
                desired = 1 ^ initial
            target = gates[gi].target_for_arrival(branch, desired)
            if gi in assigned and assigned[gi] != target:
                return None
            assigned[gi] = target
            targets[gi] = target
    return tuple(targets)


def _segment_transition(
    n: int,
    gates: list[MuxGate],
    stage: tuple[int, ...],
    stage_index: int,
    allowed_stage: set[int],
    starts: tuple[int, int],
    sink: int,
    previous_gate: int,
    previous_branches: tuple[int, int],
    initial_alphas: tuple[int, int],
    next_gate: int | None = None,
    next_branches: tuple[int, int] | None = None,
) -> tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]] | None:
    options: list[list[tuple[int | None, int | None, int, tuple[tuple[int, int], ...], int]]] = []
    for route, start in enumerate(starts):
        if start == sink:
            if next_gate is not None:
                assert next_branches is not None
                desired = gates[next_gate].branch(next_branches[route])[2]
            else:
                desired = 1 ^ initial_alphas[route]
            options.append([(None, None, sink, (), desired)])
            continue
        if stage[start] != stage_index:
            return None
        current = []
        for gi in sorted(allowed_stage):
            gate = gates[gi]
            if gate.selector != start:
                continue
            for branch in (0, 1):
                _s, dest, alpha, _pd = gate.branch(branch)
                if dest != sink and stage[dest] != stage_index:
                    continue
                current.append((gi, branch, dest, ((gi, branch),), alpha))
        if not current:
            return None
        options.append(current)

    for first0 in options[0]:
        for first1 in options[1]:
            gi0, _b0, tail0, prefix0, desired0 = first0
            gi1, _b1, tail1, prefix1, desired1 = first1
            if gi0 is not None and gi0 == gi1:
                continue
            target0 = gates[previous_gate].target_for_arrival(previous_branches[0], desired0)
            target1 = gates[previous_gate].target_for_arrival(previous_branches[1], desired1)
            if target0 != target1:
                continue
            consumed = {gi for gi in (gi0, gi1) if gi is not None}
            tails = _flow_paths(
                n,
                gates,
                allowed_stage - consumed,
                (tail0, tail1),
                sink,
            )
            if tails is None:
                continue
            return prefix0 + tails[0], prefix1 + tails[1]
    return None


def fixed_pair_minimum_overlap_certificate(
    n: int,
    gates: list[MuxGate],
    selector: int,
    first_gate0: int,
    first_branch0: int,
    first_gate1: int,
    first_branch1: int,
) -> DominatorDPCertificate | None:
    if not _valid_instance(n, gates):
        return None
    if first_gate0 == first_gate1:
        return None
    g0 = gates[first_gate0]
    g1 = gates[first_gate1]
    s0, dest0, alpha0, _ = g0.branch(first_branch0)
    s1, dest1, alpha1, _ = g1.branch(first_branch1)
    if s0 != selector or s1 != selector or alpha0 == alpha1:
        return None

    structure = common_gate_dominator_chain(n, gates, selector, dest0, dest1)
    if structure is None:
        return None
    common, stage, allowed = structure
    d = len(common)
    noncommon = set(allowed) - set(common)
    stage_gates = [
        {gi for gi in noncommon if stage[gates[gi].selector] == j}
        for j in range(d + 1)
    ]
    initial_alphas = (alpha0, alpha1)

    if d == 0:
        returns = _flow_paths(n, gates, stage_gates[0], (dest0, dest1), selector)
        if returns is None:
            return None
        cycle0 = ((first_gate0, first_branch0),) + returns[0]
        cycle1 = ((first_gate1, first_branch1),) + returns[1]
        target = _target_word(gates, cycle0, cycle1)
        if target is None:
            raise AssertionError("gate-disjoint opposite-phase cycles must be target-compatible")
        return DominatorDPCertificate(
            selector,
            first_gate0,
            first_branch0,
            first_gate1,
            first_branch1,
            (),
            returns[0],
            returns[1],
            target,
        )

    first_common = common[0]
    initial_returns = _flow_paths(
        n,
        gates,
        stage_gates[0],
        (dest0, dest1),
        gates[first_common].selector,
    )
    if initial_returns is None:
        return None

    # State = branch choice of route 0 and route 1 at the current common gate.
    # Witness paths already include the current common-gate branch.
    dp: dict[tuple[int, int], tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]]] = {}
    for state in product((0, 1), repeat=2):
        dp[state] = (
            initial_returns[0] + ((first_common, state[0]),),
            initial_returns[1] + ((first_common, state[1]),),
        )

    for j in range(d - 1):
        previous = common[j]
        nxt = common[j + 1]
        sink = gates[nxt].selector
        new_dp = {}
        for state, prefixes in sorted(dp.items()):
            starts = (
                gates[previous].branch(state[0])[1],
                gates[previous].branch(state[1])[1],
            )
            for next_state in product((0, 1), repeat=2):
                segment = _segment_transition(
                    n,
                    gates,
                    stage,
                    j + 1,
                    stage_gates[j + 1],
                    starts,
                    sink,
                    previous,
                    state,
                    initial_alphas,
                    nxt,
                    next_state,
                )
                if segment is None or next_state in new_dp:
                    continue
                new_dp[next_state] = (
                    prefixes[0] + segment[0] + ((nxt, next_state[0]),),
                    prefixes[1] + segment[1] + ((nxt, next_state[1]),),
                )
        dp = new_dp
        if not dp:
            return None

    last = common[-1]
    for state, prefixes in sorted(dp.items()):
        starts = (
            gates[last].branch(state[0])[1],
            gates[last].branch(state[1])[1],
        )
        segment = _segment_transition(
            n,
            gates,
            stage,
            d,
            stage_gates[d],
            starts,
            selector,
            last,
            state,
            initial_alphas,
        )
        if segment is None:
            continue
        return0 = prefixes[0] + segment[0]
        return1 = prefixes[1] + segment[1]
        cycle0 = ((first_gate0, first_branch0),) + return0
        cycle1 = ((first_gate1, first_branch1),) + return1
        target = _target_word(gates, cycle0, cycle1)
        if target is None:
            raise AssertionError("DP accepted incompatible common-gate targets")
        overlap = tuple(sorted({gi for gi, _ in return0} & {gi for gi, _ in return1}))
        if overlap != tuple(sorted(common)):
            raise AssertionError(("minimum-overlap DP used unexpected shared gates", overlap, common))
        return DominatorDPCertificate(
            selector,
            first_gate0,
            first_branch0,
            first_gate1,
            first_branch1,
            common,
            return0,
            return1,
            target,
        )
    return None


def find_minimum_overlap_certificate(
    n: int,
    gates: list[MuxGate],
) -> DominatorDPCertificate | None:
    if not _valid_instance(n, gates):
        return None
    by_selector: dict[int, list[int]] = {}
    for gi, gate in enumerate(gates):
        by_selector.setdefault(gate.selector, []).append(gi)
    for selector, ids in sorted(by_selector.items()):
        if len(ids) < 2:
            continue
        for g0, g1 in combinations(ids, 2):
            for b0, b1 in product((0, 1), repeat=2):
                if gates[g0].branch(b0)[2] == gates[g1].branch(b1)[2]:
                    continue
                cert = fixed_pair_minimum_overlap_certificate(
                    n, gates, selector, g0, b0, g1, b1
                )
                if cert is not None:
                    return cert
    return None


def avoid_mux_dominator_dp(
    n: int,
    gates: list[MuxGate],
) -> tuple[tuple[int, ...], dict[str, object]]:
    cert = find_minimum_overlap_certificate(n, gates)
    if cert is None:
        raise ValueError("no V113 target-compatible minimum-overlap certificate")
    return cert.target, {
        "case": "mux_common_dominator_optimum_flow_dp",
        "selector": cert.selector,
        "common_dominators": len(cert.common_gates),
        "minimum_overlap": len(cert.common_gates),
        "cycle0_outputs": len(cert.cycle0),
        "cycle1_outputs": len(cert.cycle1),
    }


K3_CENTRAL_PATTERN = (
    ((1, 1, 1), 0),
    ((0, 1, 1), 0),
)
K3_FIRST_PATTERN = (
    ((0, 1, 0), 0),
    ((1, 0, 1), 0),
    ((1, 0, 1), 0),
    ((1, 1, 0), 0),
    ((1, 0, 1), 1),
    ((1, 0, 0), 0),
)
K3_BLOCK_PATTERN = (
    ((0, 0, 1), 0),
    ((1, 1, 1), 1),
    ((1, 1, 1), 0),
    ((1, 0, 1), 0),
    ((1, 1, 1), 1),
    ((1, 1, 1), 1),
    ((1, 1, 0), 1),
)


def _unsigned_nested_chain_k3(depth: int) -> tuple[int, list[MuxGate], tuple[int, ...]]:
    if depth < 1:
        raise ValueError("V113 strict family needs positive depth")
    k = 3
    next_var = 1
    layers: list[tuple[list[int], list[int]]] = []
    hubs = [0]
    for j in range(depth + 1):
        left = list(range(next_var, next_var + k))
        next_var += k
        right = list(range(next_var, next_var + k))
        next_var += k
        layers.append((left, right))
        if j < depth:
            hubs.append(next_var)
            next_var += 1
    gates = [
        MuxGate(0, layers[0][0][0], layers[0][1][0]),
        MuxGate(0, layers[0][0][1], layers[0][1][1]),
    ]

    def add_lobes(pair: tuple[list[int], list[int]], exit_hub: int) -> None:
        for lobe in pair:
            for i, selector in enumerate(lobe):
                gates.append(
                    MuxGate(
                        selector,
                        lobe[i + 1] if i + 1 < k else exit_hub,
                        exit_hub if i + 1 < k else lobe[0],
                    )
                )

    add_lobes(layers[0], hubs[1])
    shared = []
    for j in range(1, depth + 1):
        left, right = layers[j]
        shared.append(len(gates))
        gates.append(MuxGate(hubs[j], left[0], right[0]))
        exit_hub = hubs[j + 1] if j < depth else 0
        add_lobes(layers[j], exit_hub)
    n = next_var
    if n != 7 * (depth + 1) or len(gates) != n + 1:
        raise AssertionError("V113 k=3 family size mismatch")
    return n, gates, tuple(shared)


def strict_nonserial_optimum_family(
    depth: int,
) -> tuple[int, list[MuxGate], tuple[int, ...]]:
    """Periodic k=3 family with mixed compatible/incompatible optimum flows."""
    n, base, shared = _unsigned_nested_chain_k3(depth)
    gates = []
    for i, gate in enumerate(base):
        if i < 2:
            polarity, out_flip = K3_CENTRAL_PATTERN[i]
        elif i < 8:
            polarity, out_flip = K3_FIRST_PATTERN[i - 2]
        else:
            polarity, out_flip = K3_BLOCK_PATTERN[(i - 8) % 7]
        gates.append(
            MuxGate(
                gate.selector,
                gate.data0,
                gate.data1,
                polarity,
                out_flip,
            )
        )
    return n, gates, shared


def in_range(n: int, gates: list[MuxGate], y: tuple[int, ...]) -> bool:
    return any(
        tuple(g.value(x) for g in gates) == y
        for x in product((0, 1), repeat=n)
    )
