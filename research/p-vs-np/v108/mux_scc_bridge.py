from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from itertools import combinations, product


@dataclass(frozen=True)
class MuxGate:
    """Signed ternary multiplexer.

    value = out_flip XOR MUX(s XOR p_s, a XOR p_a, b XOR p_b),
    where MUX(z,A,B)=A for z=0 and B for z=1.
    """

    selector: int
    data0: int
    data1: int
    polarity: tuple[int, int, int] = (0, 0, 0)
    out_flip: int = 0

    def __post_init__(self):
        if len({self.selector, self.data0, self.data1}) != 3:
            raise ValueError("V108 requires essential MUX gates on three distinct inputs")
        if any(bit not in (0, 1) for bit in self.polarity) or self.out_flip not in (0, 1):
            raise ValueError("polarities must be Boolean")

    def value(self, x: tuple[int, ...]) -> int:
        ps, p0, p1 = self.polarity
        z = x[self.selector] ^ ps
        a = x[self.data0] ^ p0
        b = x[self.data1] ^ p1
        return (a if z == 0 else b) ^ self.out_flip

    def branch(self, branch: int) -> tuple[int, int, int, int]:
        """Return (selector, data, selector_source_phase, data_polarity)."""
        if branch not in (0, 1):
            raise ValueError(branch)
        ps, p0, p1 = self.polarity
        if branch == 0:
            return self.selector, self.data0, ps, p0
        return self.selector, self.data1, 1 ^ ps, p1

    def target_for_arrival(self, branch: int, data_good_phase: int) -> int:
        """Choose the output target whose branch implication arrives at `data_good_phase`."""
        _s, _d, _alpha, data_polarity = self.branch(branch)
        effective_target = data_good_phase ^ data_polarity
        return effective_target ^ self.out_flip


@dataclass(frozen=True)
class Arc:
    source: int
    dest: int
    gate_index: int
    branch: int
    source_phase: int


@dataclass(frozen=True)
class BridgeCertificate:
    bridge_gate: int
    ignored_gates: tuple[int, ...]
    left_cycle: tuple[int, ...]  # arc ids
    right_cycle: tuple[int, ...]
    bridge_branch: int


def branch_arcs(gates: list[MuxGate], bridge_gate: int, ignored: set[int]) -> list[Arc]:
    arcs: list[Arc] = []
    for i, gate in enumerate(gates):
        if i == bridge_gate or i in ignored:
            continue
        for branch in (0, 1):
            s, d, alpha, _pd = gate.branch(branch)
            arcs.append(Arc(s, d, i, branch, alpha))
    return arcs


def _scc(n: int, arcs: list[Arc]):
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    reverse: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for ai, arc in enumerate(arcs):
        adjacency[arc.source].append((arc.dest, ai))
        reverse[arc.dest].append((arc.source, ai))

    seen = [False] * n
    order: list[int] = []
    for start in range(n):
        if seen[start]:
            continue
        seen[start] = True
        stack = [(start, 0)]
        while stack:
            u, pos = stack[-1]
            if pos < len(adjacency[u]):
                v, _ai = adjacency[u][pos]
                stack[-1] = (u, pos + 1)
                if not seen[v]:
                    seen[v] = True
                    stack.append((v, 0))
            else:
                order.append(u)
                stack.pop()

    component = [-1] * n
    components: list[list[int]] = []
    for start in reversed(order):
        if component[start] != -1:
            continue
        cid = len(components)
        component[start] = cid
        vertices = []
        stack = [start]
        while stack:
            u = stack.pop()
            vertices.append(u)
            for v, _ai in reverse[u]:
                if component[v] == -1:
                    component[v] = cid
                    stack.append(v)
        components.append(vertices)
    return adjacency, component, components


def _cyclic_component(cid: int, components: list[list[int]]) -> bool:
    # Essential MUX branches never create self-loops, so SCC size > 1 is equivalent
    # to containing a directed cycle through every one of its vertices.
    return len(components[cid]) > 1


def _path_within_component(
    start: int,
    target: int,
    cid: int,
    adjacency,
    component,
):
    queue = deque([start])
    parent: dict[int, tuple[int, int] | None] = {start: None}
    while queue:
        u = queue.popleft()
        if u == target:
            vertices = [u]
            edge_ids = []
            while parent[u] is not None:
                prev, arc_id = parent[u]
                vertices.append(prev)
                edge_ids.append(arc_id)
                u = prev
            vertices.reverse()
            edge_ids.reverse()
            return vertices, edge_ids
        for v, arc_id in adjacency[u]:
            if component[v] != cid or v in parent:
                continue
            parent[v] = (u, arc_id)
            queue.append(v)
    return None


def _cycle_from_first_arc(first_arc_id: int, arcs, adjacency, component):
    first = arcs[first_arc_id]
    cid = component[first.source]
    if component[first.dest] != cid:
        return None
    back = _path_within_component(first.dest, first.source, cid, adjacency, component)
    if back is None:
        return None
    _vertices, back_arcs = back
    cycle = [first_arc_id] + back_arcs
    # Simple vertex path + the first arc means no output gate can occur twice:
    # every branch arc of a gate has the same selector/source variable.
    if len({arcs[ai].gate_index for ai in cycle}) != len(cycle):
        raise AssertionError("simple directed cycle unexpectedly reused a MUX output")
    for a, b in zip(cycle, cycle[1:] + cycle[:1]):
        if arcs[a].dest != arcs[b].source:
            raise AssertionError("cycle reconstruction is not contiguous")
    return tuple(cycle)


def find_scc_bridge_certificate(
    n: int,
    gates: list[MuxGate],
    ignored: set[int] | None = None,
) -> BridgeCertificate | None:
    ignored = set() if ignored is None else set(ignored)
    for bridge_index, bridge in enumerate(gates):
        if bridge_index in ignored:
            continue
        arcs = branch_arcs(gates, bridge_index, ignored)
        adjacency, component, components = _scc(n, arcs)
        left_cid = component[bridge.selector]
        if not _cyclic_component(left_cid, components):
            continue

        # The outgoing cycle edge fixes the literal excluded by the left cycle.
        # The forced selector value is its complement, which uniquely chooses
        # one of the two bridge branches because their source phases are opposite.
        for left_dest, left_arc_id in adjacency[bridge.selector]:
            if component[left_dest] != left_cid:
                continue
            left_cycle = _cycle_from_first_arc(
                left_arc_id, arcs, adjacency, component
            )
            if left_cycle is None:
                continue
            left_alpha = arcs[left_arc_id].source_phase
            forced_selector = 1 ^ left_alpha
            ps = bridge.polarity[0]
            bridge_branch = forced_selector ^ ps
            _s, right_terminal, bridge_alpha, _pd = bridge.branch(bridge_branch)
            if bridge_alpha != forced_selector:
                raise AssertionError("bridge branch phase mismatch")

            right_cid = component[right_terminal]
            if right_cid == left_cid or not _cyclic_component(right_cid, components):
                continue

            for right_dest, right_arc_id in adjacency[right_terminal]:
                if component[right_dest] != right_cid:
                    continue
                right_cycle = _cycle_from_first_arc(
                    right_arc_id, arcs, adjacency, component
                )
                if right_cycle is None:
                    continue
                left_gates = {arcs[ai].gate_index for ai in left_cycle}
                right_gates = {arcs[ai].gate_index for ai in right_cycle}
                if left_gates & right_gates:
                    raise AssertionError("cycles in distinct SCCs reused an output gate")
                return BridgeCertificate(
                    bridge_gate=bridge_index,
                    ignored_gates=tuple(sorted(ignored)),
                    left_cycle=left_cycle,
                    right_cycle=right_cycle,
                    bridge_branch=bridge_branch,
                )
    return None


def find_with_deletion_budget(
    n: int,
    gates: list[MuxGate],
    max_deleted: int,
) -> BridgeCertificate | None:
    """XP hierarchy for distance to the SCC-separated certificate.

    Ignored output gates are harmless: once a subfamily target is impossible,
    their output coordinates can be filled arbitrarily.
    """
    if max_deleted < 0:
        raise ValueError(max_deleted)
    indices = range(len(gates))
    for size in range(max_deleted + 1):
        for deleted in combinations(indices, size):
            cert = find_scc_bridge_certificate(n, gates, set(deleted))
            if cert is not None:
                return cert
    return None


def _assign_cycle_targets(
    gates: list[MuxGate],
    arcs: list[Arc],
    cycle: tuple[int, ...],
    targets: list[int],
    used: set[int],
) -> int:
    alphas = [arcs[ai].source_phase for ai in cycle]
    for pos, arc_id in enumerate(cycle):
        arc = arcs[arc_id]
        if arc.gate_index in used:
            raise AssertionError("certificate reused an output gate")
        beta = alphas[pos + 1] if pos + 1 < len(cycle) else 1 ^ alphas[0]
        targets[arc.gate_index] = gates[arc.gate_index].target_for_arrival(
            arc.branch, beta
        )
        used.add(arc.gate_index)
    # The cycle contains the implication x=alpha -> x=1-alpha, hence any
    # satisfying assignment is forced to x=1-alpha.
    return alphas[0]


def construct_missing_from_certificate(
    n: int,
    gates: list[MuxGate],
    cert: BridgeCertificate,
):
    ignored = set(cert.ignored_gates)
    arcs = branch_arcs(gates, cert.bridge_gate, ignored)
    targets = [0] * len(gates)
    used: set[int] = set()

    left_alpha = _assign_cycle_targets(
        gates, arcs, cert.left_cycle, targets, used
    )
    right_alpha = _assign_cycle_targets(
        gates, arcs, cert.right_cycle, targets, used
    )

    bridge = gates[cert.bridge_gate]
    forced_selector = 1 ^ left_alpha
    _s, _d, bridge_alpha, _pd = bridge.branch(cert.bridge_branch)
    if bridge_alpha != forced_selector:
        raise AssertionError("left unit does not trigger the bridge clause")
    # Force the right terminal to the literal that the right cycle excludes.
    targets[cert.bridge_gate] = bridge.target_for_arrival(
        cert.bridge_branch, right_alpha
    )
    used.add(cert.bridge_gate)

    return tuple(targets), {
        "case": "mux_scc_cycle_bridge",
        "deleted_outputs": len(ignored),
        "left_cycle_outputs": len(cert.left_cycle),
        "right_cycle_outputs": len(cert.right_cycle),
        "bridge_gate": cert.bridge_gate,
        "bridge_branch": cert.bridge_branch,
        "used_outputs": len(used),
    }


def avoid_mux_scc_bridge(
    n: int,
    gates: list[MuxGate],
    max_deleted: int = 0,
):
    cert = find_with_deletion_budget(n, gates, max_deleted)
    if cert is None:
        raise ValueError("no V108 SCC-separated two-cycle certificate within deletion budget")
    return construct_missing_from_certificate(n, gates, cert)


def in_range(n: int, gates: list[MuxGate], y: tuple[int, ...]) -> bool:
    return any(
        tuple(g.value(x) for g in gates) == y
        for x in product((0, 1), repeat=n)
    )


def strict_two_cycle_family(k: int):
    """Exact-stretch Hall circuit with beta=2n/3 for k divisible by three."""
    if k < 3:
        raise ValueError("cycle length must be at least three")
    left = list(range(k))
    right = list(range(k, 2 * k))
    gates: list[MuxGate] = []
    for cycle in (left, right):
        for i, selector in enumerate(cycle):
            gates.append(
                MuxGate(
                    selector,
                    cycle[(i + 1) % k],
                    cycle[(i + 2) % k],
                )
            )
    # Left branch-0 cycle forces x_left[0]=1.  With p_s=0 this activates
    # bridge branch 1, which points to right[0].  The right branch-0 cycle can
    # be targeted to force right[0]=1 while the bridge forces it to 0.
    gates.append(MuxGate(left[0], left[2], right[0]))
    n = 2 * k
    if len(gates) != n + 1:
        raise AssertionError("strict family must have exact positive stretch")
    return n, gates
