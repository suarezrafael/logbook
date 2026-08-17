from __future__ import annotations

import sys
from dataclasses import dataclass
from itertools import combinations, product
from pathlib import Path

V109_DIR = Path(__file__).resolve().parents[1] / "v109"
sys.path.insert(0, str(V109_DIR))
from mux_gate_flow import FlowNetwork, GateBottleneck, MuxGate, _flow_or_bottleneck_for_pair  # noqa: E402


@dataclass(frozen=True)
class SharedGateCertificate:
    selector: int
    first_gate0: int
    first_branch0: int
    first_gate1: int
    first_branch1: int
    shared_gate: int
    return_path0: tuple[tuple[int, int], ...]
    return_path1: tuple[tuple[int, int], ...]
    shared_target: int

    @property
    def cycle0(self):
        return ((self.first_gate0, self.first_branch0),) + self.return_path0

    @property
    def cycle1(self):
        return ((self.first_gate1, self.first_branch1),) + self.return_path1


@dataclass(frozen=True)
class NestedBottleneck:
    selector: int
    first_gate0: int
    first_branch0: int
    first_gate1: int
    first_branch1: int
    first_bottleneck: int


def _build_upgraded_network(n, gates, selector, dest0, dest1, shared_gate):
    allowed = [i for i, gate in enumerate(gates) if gate.selector != selector]
    gate_pos = {gi: pos for pos, gi in enumerate(allowed)}
    source = n + 2 * len(allowed)
    net = FlowNetwork(source + 1)
    for gi in allowed:
        pos = gate_pos[gi]
        gin = n + 2 * pos
        gout = gin + 1
        gate = gates[gi]
        net.add_edge(gate.selector, gin, 2)
        net.add_edge(gin, gout, 2 if gi == shared_gate else 1, ("gate", gi))
        net.add_edge(gout, gate.data0, 2, ("branch", gi, 0))
        net.add_edge(gout, gate.data1, 2, ("branch", gi, 1))
    net.add_edge(source, dest0, 1, ("source", 0))
    net.add_edge(source, dest1, 1, ("source", 1))
    return net, source, selector


def _decode_two_paths(net, source, sink):
    raw = net.positive_flow_paths(source, sink, 2)
    decoded = {}
    for path in raw:
        tags = [meta for meta in path if meta and meta[0] == "source"]
        if len(tags) != 1:
            raise AssertionError("each upgraded-flow path must retain one source tag")
        decoded[tags[0][1]] = tuple(
            (meta[1], meta[2]) for meta in path if meta and meta[0] == "branch"
        )
    if set(decoded) != {0, 1}:
        raise AssertionError("upgraded flow failed to use both prescribed sources")
    return decoded[0], decoded[1]


def _required_target_at_position(gates, cycle, pos):
    first_alpha = gates[cycle[0][0]].branch(cycle[0][1])[2]
    gi, branch = cycle[pos]
    if pos + 1 < len(cycle):
        next_gi, next_branch = cycle[pos + 1]
        desired = gates[next_gi].branch(next_branch)[2]
    else:
        desired = 1 ^ first_alpha
    return gates[gi].target_for_arrival(branch, desired)


def _shared_target(gates, cycle0, cycle1, shared_gate):
    positions = []
    for cycle in (cycle0, cycle1):
        loc = [i for i, (gi, _branch) in enumerate(cycle) if gi == shared_gate]
        if len(loc) != 1:
            return None
        positions.append(loc[0])
    y0 = _required_target_at_position(gates, cycle0, positions[0])
    y1 = _required_target_at_position(gates, cycle1, positions[1])
    return y0 if y0 == y1 else None


def _upgrade_bottleneck_pair(n, gates, bottleneck):
    selector = bottleneck.selector
    g0, b0 = bottleneck.first_gate0, bottleneck.first_branch0
    g1, b1 = bottleneck.first_gate1, bottleneck.first_branch1
    _s0, d0, a0, _ = gates[g0].branch(b0)
    _s1, d1, a1, _ = gates[g1].branch(b1)
    if a0 == a1:
        raise AssertionError("V110 starts from opposite selector phases")
    h = bottleneck.bottleneck_gate
    net, source, sink = _build_upgraded_network(n, gates, selector, d0, d1, h)
    if net.max_flow(source, sink, 2) != 2:
        return NestedBottleneck(selector, g0, b0, g1, b1, h)
    p0, p1 = _decode_two_paths(net, source, sink)
    c0 = ((g0, b0),) + p0
    c1 = ((g1, b1),) + p1
    overlap = {gi for gi, _ in c0} & {gi for gi, _ in c1}
    if overlap != {h}:
        raise AssertionError(("upgraded routes must share exactly h", overlap, h))
    y = _shared_target(gates, c0, c1, h)
    if y is None:
        return None
    return SharedGateCertificate(selector, g0, b0, g1, b1, h, p0, p1, y)


def find_shared_gate_certificate(n: int, gates: list[MuxGate]):
    by_selector = {}
    for i, gate in enumerate(gates):
        by_selector.setdefault(gate.selector, []).append(i)
    first_nested = None
    for selector, indices in sorted(by_selector.items()):
        if len(indices) < 2:
            continue
        for g0, g1 in combinations(indices, 2):
            for b0 in (0, 1):
                a0 = gates[g0].branch(b0)[2]
                for b1 in (0, 1):
                    a1 = gates[g1].branch(b1)[2]
                    if a0 == a1:
                        continue
                    old = _flow_or_bottleneck_for_pair(n, gates, selector, g0, b0, g1, b1)
                    if not isinstance(old, GateBottleneck):
                        continue
                    upgraded = _upgrade_bottleneck_pair(n, gates, old)
                    if isinstance(upgraded, SharedGateCertificate):
                        return upgraded
                    if isinstance(upgraded, NestedBottleneck) and first_nested is None:
                        first_nested = upgraded
    return first_nested


def construct_missing_from_shared_gate(n, gates, cert):
    targets = [0] * len(gates)
    assigned = {}
    for cycle in (cert.cycle0, cert.cycle1):
        first_alpha = gates[cycle[0][0]].branch(cycle[0][1])[2]
        for pos, (gi, branch) in enumerate(cycle):
            if pos + 1 < len(cycle):
                ngi, nbranch = cycle[pos + 1]
                desired = gates[ngi].branch(nbranch)[2]
            else:
                desired = 1 ^ first_alpha
            target = gates[gi].target_for_arrival(branch, desired)
            if gi in assigned and assigned[gi] != target:
                raise AssertionError(("shared target incompatibility", gi, assigned[gi], target))
            assigned[gi] = target
            targets[gi] = target
    if assigned.get(cert.shared_gate) != cert.shared_target:
        raise AssertionError("stored shared target disagrees with lifted cycles")
    return tuple(targets), {
        "case": "mux_single_shared_gate_compatible_cycles",
        "selector": cert.selector,
        "shared_gate": cert.shared_gate,
        "shared_target": cert.shared_target,
        "cycle0_outputs": len(cert.cycle0),
        "cycle1_outputs": len(cert.cycle1),
        "used_outputs": len(assigned),
    }


def avoid_mux_shared_gate(n, gates):
    cert = find_shared_gate_certificate(n, gates)
    if not isinstance(cert, SharedGateCertificate):
        raise ValueError("no V110 phase-compatible single-shared-gate certificate")
    return construct_missing_from_shared_gate(n, gates, cert)


def strict_shared_bottleneck_family(k: int):
    if k < 2:
        raise ValueError("V110 strict family needs k>=2")
    v = 0
    left = list(range(1, k + 1))
    right = list(range(k + 1, 2 * k + 1))
    w = 2 * k + 1
    post_left = list(range(2 * k + 2, 3 * k + 2))
    post_right = list(range(3 * k + 2, 4 * k + 2))
    gates = [MuxGate(v, left[0], right[0]), MuxGate(v, left[1], right[1])]
    for lobe in (left, right):
        for i, selector in enumerate(lobe):
            gates.append(MuxGate(selector, lobe[i + 1] if i + 1 < k else w, w if i + 1 < k else lobe[0]))
    shared_gate = len(gates)
    gates.append(MuxGate(w, post_left[0], post_right[0]))
    for lobe in (post_left, post_right):
        for i, selector in enumerate(lobe):
            gates.append(MuxGate(selector, lobe[i + 1] if i + 1 < k else v, v if i + 1 < k else lobe[0]))
    n = 4 * k + 2
    if len(gates) != n + 1:
        raise AssertionError("V110 strict family must have m=n+1")
    return n, gates, shared_gate


def in_range(n, gates, y):
    return any(tuple(g.value(x) for g in gates) == y for x in product((0, 1), repeat=n))
