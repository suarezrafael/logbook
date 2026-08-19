from __future__ import annotations

import sys
from collections import deque
from dataclasses import dataclass
from itertools import combinations, product
from pathlib import Path

V109_DIR = Path(__file__).resolve().parents[1] / "v109"
sys.path.insert(0, str(V109_DIR))
from mux_gate_flow import MuxGate  # noqa: E402


@dataclass(frozen=True)
class MinOverlapCertificate:
    selector: int
    first_gate0: int
    first_branch0: int
    first_gate1: int
    first_branch1: int
    return_path0: tuple[tuple[int, int], ...]
    return_path1: tuple[tuple[int, int], ...]
    shared_gates: tuple[int, ...]
    overlap_cost: int

    @property
    def cycle0(self) -> tuple[tuple[int, int], ...]:
        return ((self.first_gate0, self.first_branch0),) + self.return_path0

    @property
    def cycle1(self) -> tuple[tuple[int, int], ...]:
        return ((self.first_gate1, self.first_branch1),) + self.return_path1


class MinCostFlowNetwork:
    """Tiny integral min-cost-flow engine specialized to exactly two units."""

    def __init__(self, size: int):
        self.adj: list[list[list[object]]] = [[] for _ in range(size)]
        self.forward: list[tuple[int, int, int, int, object | None]] = []

    def add_edge(self, u: int, v: int, cap: int, cost: int, meta=None) -> None:
        ui = len(self.adj[u])
        vi = len(self.adj[v])
        self.adj[u].append([v, cap, vi, cost, cap, meta])
        self.adj[v].append([u, 0, ui, -cost, 0, None])
        self.forward.append((u, ui, cap, cost, meta))

    def min_cost_flow(self, source: int, sink: int) -> tuple[int, int]:
        amount = 2
        value = 0
        total_cost = 0
        size = len(self.adj)
        inf = 10**18
        while value < amount:
            # Residual reverse arcs can have cost -1 after the first unit.  Use
            # deterministic Bellman-Ford passes, not queue-based SPFA, so the
            # implementation has an explicit worst-case polynomial bound.
            dist = [inf] * size
            parent: list[tuple[int, int] | None] = [None] * size
            dist[source] = 0
            for _ in range(size - 1):
                changed = False
                for u in range(size):
                    if dist[u] == inf:
                        continue
                    for ei, edge in enumerate(self.adj[u]):
                        v, cap, _rev, cost, _orig, _meta = edge
                        if cap <= 0 or dist[v] <= dist[u] + cost:
                            continue
                        dist[v] = dist[u] + cost
                        parent[v] = (u, ei)
                        changed = True
                if not changed:
                    break
            if parent[sink] is None:
                break
            cur = sink
            while cur != source:
                u, ei = parent[cur]
                edge = self.adj[u][ei]
                v, cap, rev, cost, _orig, _meta = edge
                edge[1] = cap - 1
                self.adj[v][rev][1] += 1
                total_cost += cost
                cur = u
            value += 1
        return value, total_cost

    def positive_flow_paths(self, source: int, sink: int, count: int = 2):
        remaining: dict[tuple[int, int], int] = {}
        metadata: dict[tuple[int, int], object | None] = {}
        for u, ei, original, _cost, meta in self.forward:
            flow = original - self.adj[u][ei][1]
            if flow > 0:
                key = (u, ei)
                remaining[key] = flow
                metadata[key] = meta

        paths = []
        for _ in range(count):
            parent: dict[int, tuple[int, int] | None] = {source: None}
            queue = deque([source])
            while queue and sink not in parent:
                u = queue.popleft()
                for ei, edge in enumerate(self.adj[u]):
                    key = (u, ei)
                    if remaining.get(key, 0) <= 0:
                        continue
                    v = edge[0]
                    if v in parent:
                        continue
                    parent[v] = key
                    queue.append(v)
                    if v == sink:
                        break
            if sink not in parent:
                raise AssertionError("integral min-cost flow did not decompose into two paths")
            keys = []
            cur = sink
            while cur != source:
                key = parent[cur]
                assert key is not None
                keys.append(key)
                cur = key[0]
            keys.reverse()
            for key in keys:
                remaining[key] -= 1
            paths.append([metadata.get(key) for key in keys])
        return paths


def _build_min_overlap_network(
    n: int,
    gates: list[MuxGate],
    selector: int,
    dest0: int,
    dest1: int,
) -> tuple[MinCostFlowNetwork, int, int]:
    allowed = [i for i, gate in enumerate(gates) if gate.selector != selector]
    gate_pos = {gi: pos for pos, gi in enumerate(allowed)}
    source = n + 2 * len(allowed)
    net = MinCostFlowNetwork(source + 1)
    for gi in allowed:
        pos = gate_pos[gi]
        gin = n + 2 * pos
        gout = gin + 1
        gate = gates[gi]
        net.add_edge(gate.selector, gin, 2, 0)
        # The first unit through an output is free; a second unit costs one.
        # Hence total flow cost counts output gates shared by both paths.
        net.add_edge(gin, gout, 1, 0, ("gate", gi, 0))
        net.add_edge(gin, gout, 1, 1, ("gate", gi, 1))
        net.add_edge(gout, gate.data0, 2, 0, ("branch", gi, 0))
        net.add_edge(gout, gate.data1, 2, 0, ("branch", gi, 1))
    net.add_edge(source, dest0, 1, 0, ("source", 0))
    net.add_edge(source, dest1, 1, 0, ("source", 1))
    return net, source, selector


def _decode_paths(
    net: MinCostFlowNetwork,
    source: int,
    sink: int,
) -> tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]]:
    decoded: dict[int, tuple[tuple[int, int], ...]] = {}
    for path in net.positive_flow_paths(source, sink, 2):
        tags = [meta for meta in path if meta and meta[0] == "source"]
        if len(tags) != 1:
            raise AssertionError("each V111 path must retain exactly one source label")
        sid = tags[0][1]
        decoded[sid] = tuple(
            (meta[1], meta[2]) for meta in path if meta and meta[0] == "branch"
        )
    if set(decoded) != {0, 1}:
        raise AssertionError("V111 flow did not use both prescribed first destinations")
    return decoded[0], decoded[1]


def _required_target_at_position(
    gates: list[MuxGate],
    cycle: tuple[tuple[int, int], ...],
    pos: int,
) -> int:
    first_alpha = gates[cycle[0][0]].branch(cycle[0][1])[2]
    gi, branch = cycle[pos]
    if pos + 1 < len(cycle):
        next_gi, next_branch = cycle[pos + 1]
        desired = gates[next_gi].branch(next_branch)[2]
    else:
        desired = 1 ^ first_alpha
    return gates[gi].target_for_arrival(branch, desired)


def _compatible_target_word(
    gates: list[MuxGate],
    cycle0: tuple[tuple[int, int], ...],
    cycle1: tuple[tuple[int, int], ...],
) -> tuple[tuple[int, ...], dict[int, int]] | None:
    targets = [0] * len(gates)
    assigned: dict[int, int] = {}
    for cycle in (cycle0, cycle1):
        for pos, (gi, _branch) in enumerate(cycle):
            target = _required_target_at_position(gates, cycle, pos)
            if gi in assigned and assigned[gi] != target:
                return None
            assigned[gi] = target
            targets[gi] = target
    return tuple(targets), assigned


def _candidate_for_pair(
    n: int,
    gates: list[MuxGate],
    selector: int,
    g0: int,
    b0: int,
    g1: int,
    b1: int,
) -> tuple[MinOverlapCertificate, tuple[int, ...]] | None:
    _s0, d0, a0, _ = gates[g0].branch(b0)
    _s1, d1, a1, _ = gates[g1].branch(b1)
    if a0 == a1:
        return None
    net, source, sink = _build_min_overlap_network(n, gates, selector, d0, d1)
    value, cost = net.min_cost_flow(source, sink)
    if value != 2:
        return None
    p0, p1 = _decode_paths(net, source, sink)
    c0 = ((g0, b0),) + p0
    c1 = ((g1, b1),) + p1
    overlap = tuple(sorted({gi for gi, _ in c0} & {gi for gi, _ in c1}))
    if cost != len(overlap):
        raise AssertionError(("min-cost overlap accounting mismatch", cost, overlap))
    compatible = _compatible_target_word(gates, c0, c1)
    if compatible is None:
        return None
    target, _assigned = compatible
    cert = MinOverlapCertificate(
        selector,
        g0,
        b0,
        g1,
        b1,
        p0,
        p1,
        overlap,
        cost,
    )
    return cert, target


def find_min_overlap_certificate(
    n: int,
    gates: list[MuxGate],
) -> tuple[MinOverlapCertificate, tuple[int, ...]] | None:
    by_selector: dict[int, list[int]] = {}
    for i, gate in enumerate(gates):
        by_selector.setdefault(gate.selector, []).append(i)

    best: tuple[MinOverlapCertificate, tuple[int, ...]] | None = None
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
                    candidate = _candidate_for_pair(n, gates, selector, g0, b0, g1, b1)
                    if candidate is None:
                        continue
                    if best is None:
                        best = candidate
                        continue
                    cert, _target = candidate
                    best_cert, _best_target = best
                    key = (cert.overlap_cost, cert.selector, cert.first_gate0, cert.first_branch0, cert.first_gate1, cert.first_branch1)
                    best_key = (
                        best_cert.overlap_cost,
                        best_cert.selector,
                        best_cert.first_gate0,
                        best_cert.first_branch0,
                        best_cert.first_gate1,
                        best_cert.first_branch1,
                    )
                    if key < best_key:
                        best = candidate
    return best


def avoid_mux_min_overlap(
    n: int,
    gates: list[MuxGate],
) -> tuple[tuple[int, ...], dict[str, object]]:
    found = find_min_overlap_certificate(n, gates)
    if found is None:
        raise ValueError("no V111 target-compatible minimum-overlap two-flow certificate")
    cert, target = found
    return target, {
        "case": "mux_target_compatible_minimum_overlap_two_flow",
        "selector": cert.selector,
        "overlap_cost": cert.overlap_cost,
        "shared_gates": list(cert.shared_gates),
        "cycle0_outputs": len(cert.cycle0),
        "cycle1_outputs": len(cert.cycle1),
    }


def strict_nested_chain_family(
    k: int,
    depth: int,
) -> tuple[int, list[MuxGate], tuple[int, ...]]:
    """Exact-stretch family with `depth` unavoidable shared MUX bottlenecks."""
    if k < 2:
        raise ValueError("V111 strict family needs k>=2")
    if depth < 1:
        raise ValueError("V111 strict family needs depth>=1")

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
    n = next_var

    first_left, first_right = layers[0]
    gates: list[MuxGate] = [
        MuxGate(0, first_left[0], first_right[0]),
        MuxGate(0, first_left[1], first_right[1]),
    ]

    def add_lobes(pair: tuple[list[int], list[int]], exit_hub: int) -> None:
        for lobe in pair:
            for i, selector in enumerate(lobe):
                gates.append(MuxGate(
                    selector,
                    lobe[i + 1] if i + 1 < k else exit_hub,
                    exit_hub if i + 1 < k else lobe[0],
                ))

    add_lobes(layers[0], hubs[1])
    shared: list[int] = []
    for j in range(1, depth + 1):
        left, right = layers[j]
        shared.append(len(gates))
        gates.append(MuxGate(hubs[j], left[0], right[0]))
        exit_hub = hubs[j + 1] if j < depth else 0
        add_lobes(layers[j], exit_hub)

    if len(gates) != n + 1:
        raise AssertionError(("V111 strict family must have m=n+1", n, len(gates)))
    return n, gates, tuple(shared)


def in_range(n: int, gates: list[MuxGate], y: tuple[int, ...]) -> bool:
    return any(tuple(g.value(x) for g in gates) == y for x in product((0, 1), repeat=n))
