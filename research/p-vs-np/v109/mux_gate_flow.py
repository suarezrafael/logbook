from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from itertools import combinations, product


@dataclass(frozen=True)
class MuxGate:
    """Signed essential ternary multiplexer.

    value = out_flip XOR MUX(s XOR p_s, a XOR p_a, b XOR p_b),
    with MUX(z,A,B)=A for z=0 and B for z=1.
    """

    selector: int
    data0: int
    data1: int
    polarity: tuple[int, int, int] = (0, 0, 0)
    out_flip: int = 0

    def __post_init__(self):
        if len({self.selector, self.data0, self.data1}) != 3:
            raise ValueError("V109 requires three distinct inputs per MUX")
        if any(bit not in (0, 1) for bit in self.polarity) or self.out_flip not in (0, 1):
            raise ValueError("polarity bits must be Boolean")

    def value(self, x: tuple[int, ...]) -> int:
        ps, p0, p1 = self.polarity
        z = x[self.selector] ^ ps
        a = x[self.data0] ^ p0
        b = x[self.data1] ^ p1
        return (a if z == 0 else b) ^ self.out_flip

    def branch(self, branch: int) -> tuple[int, int, int, int]:
        if branch not in (0, 1):
            raise ValueError(branch)
        ps, p0, p1 = self.polarity
        if branch == 0:
            return self.selector, self.data0, ps, p0
        return self.selector, self.data1, 1 ^ ps, p1

    def target_for_arrival(self, branch: int, data_good_phase: int) -> int:
        _s, _d, _alpha, data_polarity = self.branch(branch)
        return (data_good_phase ^ data_polarity) ^ self.out_flip


@dataclass(frozen=True)
class DoubleCycleCertificate:
    selector: int
    first_gate0: int
    first_branch0: int
    first_gate1: int
    first_branch1: int
    return_path0: tuple[tuple[int, int], ...]
    return_path1: tuple[tuple[int, int], ...]

    @property
    def cycle0(self) -> tuple[tuple[int, int], ...]:
        return ((self.first_gate0, self.first_branch0),) + self.return_path0

    @property
    def cycle1(self) -> tuple[tuple[int, int], ...]:
        return ((self.first_gate1, self.first_branch1),) + self.return_path1


@dataclass(frozen=True)
class GateBottleneck:
    selector: int
    first_gate0: int
    first_branch0: int
    first_gate1: int
    first_branch1: int
    bottleneck_gate: int


class FlowNetwork:
    def __init__(self, size: int):
        self.adj: list[list[list[object]]] = [[] for _ in range(size)]
        self.forward: list[tuple[int, int, int, object | None]] = []

    def add_edge(self, u: int, v: int, cap: int, meta=None):
        ui = len(self.adj[u])
        vi = len(self.adj[v])
        self.adj[u].append([v, cap, vi, cap, meta])
        self.adj[v].append([u, 0, ui, 0, None])
        self.forward.append((u, ui, cap, meta))

    def max_flow(self, source: int, sink: int, limit: int = 2) -> int:
        value = 0
        while value < limit:
            parent: list[tuple[int, int] | None] = [None] * len(self.adj)
            parent[source] = (-1, -1)
            queue = deque([source])
            while queue and parent[sink] is None:
                u = queue.popleft()
                for ei, edge in enumerate(self.adj[u]):
                    v, cap, _rev, _orig, _meta = edge
                    if cap and parent[v] is None:
                        parent[v] = (u, ei)
                        queue.append(v)
                        if v == sink:
                            break
            if parent[sink] is None:
                break
            cur = sink
            while cur != source:
                u, ei = parent[cur]
                edge = self.adj[u][ei]
                v, cap, rev, _orig, _meta = edge
                edge[1] = cap - 1
                self.adj[v][rev][1] += 1
                cur = u
            value += 1
        return value

    def residual_reachable(self, source: int) -> set[int]:
        seen = {source}
        stack = [source]
        while stack:
            u = stack.pop()
            for v, cap, _rev, _orig, _meta in self.adj[u]:
                if cap and v not in seen:
                    seen.add(v)
                    stack.append(v)
        return seen

    def positive_flow_paths(self, source: int, sink: int, count: int):
        # Remaining positive forward flow; capacities are tiny and we only need
        # two source-to-sink paths.  Flow cycles, if any, are ignored.
        remaining = {}
        metadata = {}
        for u, ei, original, meta in self.forward:
            edge = self.adj[u][ei]
            flow = original - edge[1]
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
                raise AssertionError("integral flow did not decompose into source-sink paths")
            keys = []
            cur = sink
            while cur != source:
                key = parent[cur]
                assert key is not None
                keys.append(key)
                u, ei = key
                cur = u
            keys.reverse()
            for key in keys:
                remaining[key] -= 1
            paths.append([metadata.get(key) for key in keys])
        return paths


def _build_return_network(
    n: int,
    gates: list[MuxGate],
    selector: int,
    dest0: int,
    dest1: int,
):
    allowed = [i for i, gate in enumerate(gates) if gate.selector != selector]
    gate_pos = {gi: pos for pos, gi in enumerate(allowed)}
    base = n
    source = n + 2 * len(allowed)
    size = source + 1
    net = FlowNetwork(size)
    INF = 2

    for gi in allowed:
        pos = gate_pos[gi]
        gin = base + 2 * pos
        gout = gin + 1
        gate = gates[gi]
        net.add_edge(gate.selector, gin, INF)
        net.add_edge(gin, gout, 1, ("gate", gi))
        net.add_edge(gout, gate.data0, INF, ("branch", gi, 0))
        net.add_edge(gout, gate.data1, INF, ("branch", gi, 1))

    net.add_edge(source, dest0, 1, ("source", 0))
    net.add_edge(source, dest1, 1, ("source", 1))
    return net, source, selector, allowed, gate_pos


def _single_reachable(n: int, gates: list[MuxGate], selector: int, start: int) -> bool:
    adjacency = [[] for _ in range(n)]
    for gate in gates:
        if gate.selector == selector:
            continue
        adjacency[gate.selector].append(gate.data0)
        adjacency[gate.selector].append(gate.data1)
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


def _decode_flow_paths(
    raw_paths,
    first_gate0: int,
    first_gate1: int,
):
    decoded = {}
    for path in raw_paths:
        source_tags = [meta for meta in path if meta and meta[0] == "source"]
        if len(source_tags) != 1:
            raise AssertionError("flow path must use exactly one source tag")
        source_id = source_tags[0][1]
        branches = [
            (meta[1], meta[2])
            for meta in path
            if meta and meta[0] == "branch"
        ]
        decoded[source_id] = tuple(branches)
    if set(decoded) != {0, 1}:
        raise AssertionError("flow did not use both prescribed first arcs")
    return decoded[0], decoded[1]


def _flow_or_bottleneck_for_pair(
    n: int,
    gates: list[MuxGate],
    selector: int,
    g0: int,
    b0: int,
    g1: int,
    b1: int,
):
    s0, d0, a0, _ = gates[g0].branch(b0)
    s1, d1, a1, _ = gates[g1].branch(b1)
    if s0 != selector or s1 != selector or a0 == a1:
        raise ValueError("first arcs must share a selector and have opposite source phases")
    if not _single_reachable(n, gates, selector, d0):
        return None
    if not _single_reachable(n, gates, selector, d1):
        return None

    net, source, sink, allowed, gate_pos = _build_return_network(
        n, gates, selector, d0, d1
    )
    value = net.max_flow(source, sink, 2)
    if value == 2:
        paths = net.positive_flow_paths(source, sink, 2)
        p0, p1 = _decode_flow_paths(paths, g0, g1)
        return DoubleCycleCertificate(
            selector, g0, b0, g1, b1, p0, p1
        )
    if value != 1:
        return None

    reachable = net.residual_reachable(source)
    cut_gates = []
    base = n
    for gi in allowed:
        pos = gate_pos[gi]
        gin = base + 2 * pos
        gout = gin + 1
        if gin in reachable and gout not in reachable:
            cut_gates.append(gi)
    if len(cut_gates) != 1:
        raise AssertionError(("unit gate cut expected", selector, g0, g1, cut_gates))
    return GateBottleneck(selector, g0, b0, g1, b1, cut_gates[0])


def find_double_cycle_or_bottleneck(n: int, gates: list[MuxGate]):
    by_selector: dict[int, list[int]] = {}
    for i, gate in enumerate(gates):
        by_selector.setdefault(gate.selector, []).append(i)

    first_bottleneck = None
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
                    result = _flow_or_bottleneck_for_pair(
                        n, gates, selector, g0, b0, g1, b1
                    )
                    if isinstance(result, DoubleCycleCertificate):
                        return result
                    if isinstance(result, GateBottleneck) and first_bottleneck is None:
                        first_bottleneck = result
    return first_bottleneck


def _assign_cycle_targets(
    gates: list[MuxGate],
    cycle: tuple[tuple[int, int], ...],
    targets: list[int],
    used: set[int],
):
    alphas = [gates[gi].branch(branch)[2] for gi, branch in cycle]
    for pos, (gi, branch) in enumerate(cycle):
        if gi in used:
            raise AssertionError("double-cycle certificate reused an output gate")
        beta = alphas[pos + 1] if pos + 1 < len(cycle) else 1 ^ alphas[0]
        targets[gi] = gates[gi].target_for_arrival(branch, beta)
        used.add(gi)
    return alphas[0]


def construct_missing_from_double_cycle(
    n: int,
    gates: list[MuxGate],
    cert: DoubleCycleCertificate,
):
    targets = [0] * len(gates)
    used: set[int] = set()
    alpha0 = _assign_cycle_targets(gates, cert.cycle0, targets, used)
    alpha1 = _assign_cycle_targets(gates, cert.cycle1, targets, used)
    if alpha0 == alpha1:
        raise AssertionError("the two cycles must start at opposite selector phases")

    # Cycle j contains selector implication alpha_j -> 1-alpha_j.  Therefore
    # every satisfying assignment would need x_selector=1-alpha_j.  Opposite
    # alpha values force both Boolean values on the same selector.
    return tuple(targets), {
        "case": "mux_gate_disjoint_opposite_cycles",
        "selector": cert.selector,
        "cycle0_outputs": len(cert.cycle0),
        "cycle1_outputs": len(cert.cycle1),
        "used_outputs": len(used),
    }


def avoid_mux_double_cycle(n: int, gates: list[MuxGate]):
    result = find_double_cycle_or_bottleneck(n, gates)
    if not isinstance(result, DoubleCycleCertificate):
        raise ValueError("no V109 gate-disjoint opposite-phase double-cycle certificate")
    return construct_missing_from_double_cycle(n, gates, result)


def branch_graph_strongly_connected(n: int, gates: list[MuxGate]) -> bool:
    adjacency = [[] for _ in range(n)]
    reverse = [[] for _ in range(n)]
    for gate in gates:
        for d in (gate.data0, gate.data1):
            adjacency[gate.selector].append(d)
            reverse[d].append(gate.selector)

    def reach(graph):
        seen = {0}
        stack = [0]
        while stack:
            u = stack.pop()
            for v in graph[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        return len(seen) == n

    return n > 0 and reach(adjacency) and reach(reverse)


def strict_single_scc_family(k: int):
    """Hall-minimal exact-stretch family outside the entire V108 certificate hierarchy."""
    if k < 2:
        raise ValueError("each return lobe needs at least two internal variables")
    v = 0
    left = list(range(1, k + 1))
    right = list(range(k + 1, 2 * k + 1))
    gates: list[MuxGate] = [
        MuxGate(v, left[0], right[0]),
        MuxGate(v, left[0], right[0]),
    ]
    for lobe in (left, right):
        for i, selector in enumerate(lobe):
            if i + 1 < len(lobe):
                gates.append(MuxGate(selector, lobe[i + 1], v))
            else:
                gates.append(MuxGate(selector, v, lobe[0]))
    n = 2 * k + 1
    if len(gates) != n + 1:
        raise AssertionError("V109 strict family must have exact positive stretch")
    return n, gates


def in_range(n: int, gates: list[MuxGate], y: tuple[int, ...]) -> bool:
    return any(
        tuple(g.value(x) for g in gates) == y
        for x in product((0, 1), repeat=n)
    )
