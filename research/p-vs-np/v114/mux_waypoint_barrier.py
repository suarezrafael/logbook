from __future__ import annotations

import sys
from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import Iterable

V109_DIR = Path(__file__).resolve().parents[1] / "v109"
sys.path.insert(0, str(V109_DIR))
from mux_gate_flow import MuxGate  # noqa: E402


@dataclass(frozen=True)
class BarrierInstance:
    n: int
    gates: tuple[MuxGate, ...]
    root: int
    first_gate0: int
    first_gate1: int
    shared_gate: int
    graph_entry_gate: int
    route0_start: int
    s1_var: int
    route1_start: int
    vertex_gate: tuple[int, ...]
    arc_gate_items: tuple[tuple[int, int, int], ...]
    waypoint_vertex: int
    bypass_return0: tuple[tuple[int, int], ...]
    scaffold_return1: tuple[tuple[int, int], ...]

    def arc_gate_map(self) -> dict[tuple[int, int], int]:
        return {(u, v): gi for u, v, gi in self.arc_gate_items}


@dataclass(frozen=True)
class ReturnCertificate:
    return_path0: tuple[tuple[int, int], ...]
    return_path1: tuple[tuple[int, int], ...]
    target: tuple[int, ...]

    @property
    def overlap(self) -> tuple[int, ...]:
        a = {gi for gi, _ in self.return_path0}
        b = {gi for gi, _ in self.return_path1}
        return tuple(sorted(a & b))


def _dedup_edges(vertex_count: int, edges: Iterable[tuple[int, int]]) -> tuple[tuple[int, int], ...]:
    cleaned = sorted({(int(u), int(v)) for u, v in edges})
    if any(not (0 <= u < vertex_count and 0 <= v < vertex_count) for u, v in cleaned):
        raise ValueError("edge endpoint outside graph")
    return tuple(cleaned)


def build_exact_stretch_barrier_instance(
    vertex_count: int,
    edges: Iterable[tuple[int, int]],
    terminals: tuple[int, int, int, int],
) -> BarrierInstance:
    """Reduce a 2-DDP instance to exact-one compatible MUX return selection.

    Terminals are (s1,t1,s2,t2).  The generated circuit has m=n+1.  The
    distinguished first pair has an explicit gate-disjoint compatible optimum,
    while deciding whether it also has a target-compatible return pair sharing
    exactly one return gate is equivalent to the original directed two-disjoint-
    paths instance.
    """
    if vertex_count < 4:
        raise ValueError("four distinct terminals are required")
    s1, t1, s2, t2 = terminals
    if len({s1, t1, s2, t2}) != 4 or any(not (0 <= t < vertex_count) for t in terminals):
        raise ValueError("terminals must be four distinct graph vertices")
    original_edges = _dedup_edges(vertex_count, edges)

    next_var = 0
    x_var = list(range(next_var, next_var + vertex_count + 1))
    next_var += vertex_count + 1
    waypoint = vertex_count

    choice_var: dict[int, int] = {}
    for v in range(vertex_count):
        if v == t2:
            continue
        choice_var[v] = next_var
        next_var += 1

    root = next_var; next_var += 1
    route0_start = next_var; next_var += 1
    route1_start = next_var; next_var += 1
    route1_after = next_var; next_var += 1
    dead0 = next_var; next_var += 1
    dead1 = next_var; next_var += 1
    dead2 = next_var; next_var += 1
    bypass_mid = next_var; next_var += 1

    gates: list[MuxGate] = []
    vertex_gate = [-1] * (vertex_count + 1)

    # Every original logical vertex is paid for by one mandatory gate.  This
    # makes gate-simple return routes correspond to vertex-simple graph paths.
    for v in range(vertex_count):
        gi = len(gates)
        vertex_gate[v] = gi
        if v == t2:
            gates.append(MuxGate(x_var[v], root, dead0))
        else:
            gates.append(MuxGate(x_var[v], choice_var[v], dead0))

    # Shared waypoint gate. Opposite branches lead to the graph suffix and the
    # private scaffold. Both next gates have source phase zero, so the two uses
    # demand the same target bit at this shared MUX.
    shared_gate = len(gates)
    vertex_gate[waypoint] = shared_gate
    gates.append(MuxGate(x_var[waypoint], x_var[s2], route1_after))

    arc_map: dict[tuple[int, int], int] = {}
    for u, v in original_edges:
        if u == t2:
            continue
        gi = len(gates)
        gates.append(MuxGate(choice_var[u], x_var[v], dead1))
        arc_map[(u, v)] = gi

    # Unique connector t1 -> waypoint.  There are no other graph arcs into the
    # fresh waypoint, and the waypoint branch 0 is the unique continuation to s2.
    connector = (t1, waypoint)
    connector_gate = len(gates)
    gates.append(MuxGate(choice_var[t1], x_var[waypoint], dead1))
    arc_map[connector] = connector_gate

    # Root first pair: prescribed branch 0 has opposite selector source phases.
    first_gate0 = len(gates)
    gates.append(MuxGate(root, route0_start, dead0, (0, 0, 0), 0))
    first_gate1 = len(gates)
    gates.append(MuxGate(root, route1_start, dead1, (1, 0, 0), 0))

    graph_entry = len(gates)
    gates.append(MuxGate(route0_start, x_var[s1], dead0))
    bypass0 = len(gates)
    gates.append(MuxGate(route0_start, bypass_mid, dead1))

    scaffold_pre = len(gates)
    gates.append(MuxGate(route1_start, x_var[waypoint], dead0))
    scaffold_post = len(gates)
    gates.append(MuxGate(route1_after, root, dead1))

    # Explicit private bypass proves the unconstrained minimum overlap is zero;
    # hence the hard one-shared gate is genuinely non-dominator "extra" overlap.
    bypass1 = len(gates)
    gates.append(MuxGate(bypass_mid, root, dead1))

    n = next_var
    # Force exact positive stretch without adding any route back from a trap.
    if len(gates) <= n:
        for _ in range(n + 1 - len(gates)):
            gates.append(MuxGate(dead0, dead1, dead2))
    elif len(gates) > n + 1:
        n += len(gates) - n - 1  # isolated unused variables
    if len(gates) != n + 1:
        raise AssertionError(("exact stretch padding failed", n, len(gates)))

    return BarrierInstance(
        n=n,
        gates=tuple(gates),
        root=root,
        first_gate0=first_gate0,
        first_gate1=first_gate1,
        shared_gate=shared_gate,
        graph_entry_gate=graph_entry,
        route0_start=route0_start,
        s1_var=x_var[s1],
        route1_start=route1_start,
        vertex_gate=tuple(vertex_gate),
        arc_gate_items=tuple((u, v, gi) for (u, v), gi in sorted(arc_map.items())),
        waypoint_vertex=waypoint,
        bypass_return0=((bypass0, 0), (bypass1, 0)),
        scaffold_return1=((scaffold_pre, 0), (shared_gate, 1), (scaffold_post, 0)),
    )


def _target_word(
    gates: tuple[MuxGate, ...],
    cycle0: tuple[tuple[int, int], ...],
    cycle1: tuple[tuple[int, int], ...],
) -> tuple[int, ...] | None:
    target = [0] * len(gates)
    assigned: dict[int, int] = {}
    for cycle in (cycle0, cycle1):
        if not cycle:
            return None
        initial_alpha = gates[cycle[0][0]].branch(cycle[0][1])[2]
        for pos, (gi, branch) in enumerate(cycle):
            if pos + 1 < len(cycle):
                ngi, nb = cycle[pos + 1]
                desired = gates[ngi].branch(nb)[2]
            else:
                desired = 1 ^ initial_alpha
            bit = gates[gi].target_for_arrival(branch, desired)
            if gi in assigned and assigned[gi] != bit:
                return None
            assigned[gi] = bit
            target[gi] = bit
    return tuple(target)


def _check_return_path(
    instance: BarrierInstance,
    start: int,
    path: tuple[tuple[int, int], ...],
) -> bool:
    current = start
    used: set[int] = set()
    for gi, branch in path:
        if not (0 <= gi < len(instance.gates)) or branch not in (0, 1) or gi in used:
            return False
        gate = instance.gates[gi]
        if gate.selector != current or gate.selector == instance.root:
            return False
        current = gate.branch(branch)[1]
        used.add(gi)
    return current == instance.root


def certificate_from_ddp_paths(
    instance: BarrierInstance,
    path1: tuple[int, ...],
    path2: tuple[int, ...],
    terminals: tuple[int, int, int, int],
) -> ReturnCertificate:
    s1, t1, s2, t2 = terminals
    if not path1 or path1[0] != s1 or path1[-1] != t1:
        raise ValueError("path1 has wrong terminals")
    if not path2 or path2[0] != s2 or path2[-1] != t2:
        raise ValueError("path2 has wrong terminals")
    if len(set(path1)) != len(path1) or len(set(path2)) != len(path2) or set(path1) & set(path2):
        raise ValueError("DDP witness paths must be vertex-simple and disjoint")

    arc_map = instance.arc_gate_map()
    r0: list[tuple[int, int]] = [(instance.graph_entry_gate, 0)]
    for u, v in zip(path1, path1[1:]):
        r0.append((instance.vertex_gate[u], 0))
        r0.append((arc_map[(u, v)], 0))
    r0.append((instance.vertex_gate[t1], 0))
    r0.append((arc_map[(t1, instance.waypoint_vertex)], 0))
    r0.append((instance.shared_gate, 0))
    for u, v in zip(path2, path2[1:]):
        r0.append((instance.vertex_gate[u], 0))
        r0.append((arc_map[(u, v)], 0))
    r0.append((instance.vertex_gate[t2], 0))

    return0 = tuple(r0)
    return1 = instance.scaffold_return1
    cycle0 = ((instance.first_gate0, 0),) + return0
    cycle1 = ((instance.first_gate1, 0),) + return1
    target = _target_word(instance.gates, cycle0, cycle1)
    if target is None:
        raise AssertionError("reduction witness lost shared-waypoint target compatibility")
    cert = ReturnCertificate(return0, return1, target)
    if cert.overlap != (instance.shared_gate,):
        raise AssertionError(("reduction witness must share exactly the waypoint", cert.overlap))
    return cert


def validate_certificate(instance: BarrierInstance, cert: ReturnCertificate) -> bool:
    if len(cert.overlap) != 1:
        return False
    shared = cert.overlap[0]
    b0 = [b for gi, b in cert.return_path0 if gi == shared]
    b1 = [b for gi, b in cert.return_path1 if gi == shared]
    if len(b0) != 1 or len(b1) != 1 or b0[0] == b1[0]:
        return False
    if not _check_return_path(instance, instance.route0_start, cert.return_path0):
        return False
    if not _check_return_path(instance, instance.route1_start, cert.return_path1):
        return False
    cycle0 = ((instance.first_gate0, 0),) + cert.return_path0
    cycle1 = ((instance.first_gate1, 0),) + cert.return_path1
    target = _target_word(instance.gates, cycle0, cycle1)
    return target is not None and target == cert.target


def bypass_optimum_certificate(instance: BarrierInstance) -> ReturnCertificate:
    cycle0 = ((instance.first_gate0, 0),) + instance.bypass_return0
    cycle1 = ((instance.first_gate1, 0),) + instance.scaffold_return1
    target = _target_word(instance.gates, cycle0, cycle1)
    if target is None:
        raise AssertionError("private bypass and scaffold are gate-disjoint")
    cert = ReturnCertificate(instance.bypass_return0, instance.scaffold_return1, target)
    if cert.overlap:
        raise AssertionError("private bypass must witness minimum overlap zero")
    return cert


def in_range(instance: BarrierInstance, target: tuple[int, ...]) -> bool:
    return any(
        tuple(g.value(x) for g in instance.gates) == target
        for x in product((0, 1), repeat=instance.n)
    )
