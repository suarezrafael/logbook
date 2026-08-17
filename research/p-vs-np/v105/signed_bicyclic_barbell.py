from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from signed_majority_dumbbell import (
    Gate,
    PairEdge,
    _apply_walk,
    canonical_pair_edges,
)


@dataclass(frozen=True)
class Walk:
    vertices: tuple[int, ...]
    edge_ids: tuple[int, ...]

    @property
    def start(self) -> int:
        return self.vertices[0]

    @property
    def end(self) -> int:
        return self.vertices[-1]


@dataclass(frozen=True)
class BicyclicBarbell:
    component_vertices: tuple[int, ...]
    component_edge_ids: tuple[int, ...]
    left_cycle: Walk
    connector: Walk | None
    right_cycle: Walk
    kind: str


def _components(n: int, edges: list[PairEdge]):
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for ei, e in enumerate(edges):
        adjacency[e.u].append((e.v, ei))
        adjacency[e.v].append((e.u, ei))

    seen = set()
    for start in range(n):
        if start in seen or not adjacency[start]:
            continue
        vertices = set([start])
        edge_ids = set()
        queue = [start]
        seen.add(start)
        while queue:
            u = queue.pop()
            for v, ei in adjacency[u]:
                edge_ids.add(ei)
                if v not in seen:
                    seen.add(v)
                    vertices.add(v)
                    queue.append(v)
        yield vertices, edge_ids


def _simple_component(edges: list[PairEdge], edge_ids: set[int]) -> bool:
    pairs = set()
    for ei in edge_ids:
        e = edges[ei]
        key = (min(e.u, e.v), max(e.u, e.v))
        if key in pairs:
            return False
        pairs.add(key)
    return True


def _two_core(vertices: set[int], edge_ids: set[int], edges: list[PairEdge]):
    incident = {v: set() for v in vertices}
    for ei in edge_ids:
        e = edges[ei]
        incident[e.u].add(ei)
        incident[e.v].add(ei)

    active_v = set(vertices)
    active_e = set(edge_ids)
    queue = deque(v for v in active_v if len(incident[v]) < 2)
    while queue:
        v = queue.popleft()
        if v not in active_v or len(incident[v] & active_e) >= 2:
            continue
        active_v.remove(v)
        for ei in list(incident[v] & active_e):
            active_e.remove(ei)
            e = edges[ei]
            w = e.v if e.u == v else e.u
            if w in active_v and len(incident[w] & active_e) < 2:
                queue.append(w)
    return active_v, active_e


def _core_incidence(core_v: set[int], core_e: set[int], edges: list[PairEdge]):
    incident = {v: [] for v in core_v}
    for ei in core_e:
        e = edges[ei]
        incident[e.u].append(ei)
        incident[e.v].append(ei)
    return incident


def _other(edge: PairEdge, v: int) -> int:
    if edge.u == v:
        return edge.v
    if edge.v == v:
        return edge.u
    raise ValueError("vertex is not incident to edge")


def _trace_strand(
    start: int,
    first_edge: int,
    branches: set[int],
    incident: dict[int, list[int]],
    edges: list[PairEdge],
    used: set[int],
) -> Walk:
    vertices = [start]
    edge_ids = []
    current = start
    ei = first_edge
    while True:
        if ei in used:
            raise ValueError("core strand traversal reused an edge")
        used.add(ei)
        edge_ids.append(ei)
        nxt = _other(edges[ei], current)
        vertices.append(nxt)
        if nxt in branches:
            return Walk(tuple(vertices), tuple(edge_ids))
        candidates = [x for x in incident[nxt] if x != ei]
        if len(candidates) != 1:
            raise ValueError("non-branch core vertex is not degree two")
        current, ei = nxt, candidates[0]


def _strands(core_v: set[int], core_e: set[int], edges: list[PairEdge]):
    incident = _core_incidence(core_v, core_e, edges)
    degree = {v: len(incident[v]) for v in core_v}
    branches = {v for v, d in degree.items() if d != 2}
    if sorted(degree.values()).count(4) == 1 and all(d in (2, 4) for d in degree.values()):
        if len(branches) != 1:
            return None
    elif sorted(degree.values()).count(3) == 2 and all(d in (2, 3) for d in degree.values()):
        if len(branches) != 2:
            return None
    else:
        return None

    used = set()
    walks = []
    for branch in sorted(branches):
        for ei in incident[branch]:
            if ei in used:
                continue
            walks.append(_trace_strand(branch, ei, branches, incident, edges, used))
    if used != core_e:
        return None
    return branches, walks


def _parity(walk: Walk, edges: list[PairEdge]) -> int:
    value = 0
    for ei in walk.edge_ids:
        value ^= edges[ei].delta
    return value


def find_bicyclic_odd_barbell(n: int, gates: list[Gate]):
    edges = canonical_pair_edges(gates)
    for vertices, edge_ids in _components(n, edges):
        # A connected bicyclic component has cycle rank two.
        if len(edge_ids) != len(vertices) + 1:
            continue
        if not _simple_component(edges, edge_ids):
            continue
        core_v, core_e = _two_core(vertices, edge_ids, edges)
        if len(core_e) != len(core_v) + 1:
            raise AssertionError("leaf pruning must preserve cycle rank")
        parsed = _strands(core_v, core_e, edges)
        if parsed is None:
            continue
        branches, walks = parsed

        if len(branches) == 1:
            # Figure-eight: two edge-disjoint cycles sharing one branch vertex.
            cycles = [walk for walk in walks if walk.start == walk.end]
            if len(cycles) != 2:
                continue
            if all(_parity(cycle, edges) == 1 for cycle in cycles):
                return edges, BicyclicBarbell(
                    tuple(sorted(vertices)), tuple(sorted(edge_ids)),
                    cycles[0], None, cycles[1], "figure_eight"
                )
            continue

        if len(branches) == 2:
            branch_list = sorted(branches)
            loops = [walk for walk in walks if walk.start == walk.end]
            links = [walk for walk in walks if walk.start != walk.end]
            if len(loops) == 2 and len(links) == 1:
                left = next((w for w in loops if w.start == branch_list[0]), None)
                right = next((w for w in loops if w.start == branch_list[1]), None)
                if left is None or right is None:
                    continue
                connector = links[0]
                if connector.start != branch_list[0]:
                    connector = Walk(tuple(reversed(connector.vertices)), tuple(reversed(connector.edge_ids)))
                if _parity(left, edges) == 1 and _parity(right, edges) == 1:
                    return edges, BicyclicBarbell(
                        tuple(sorted(vertices)), tuple(sorted(edge_ids)),
                        left, connector, right, "barbell"
                    )
            # Three branch-to-branch strands are the theta obstruction.  The
            # one-clause-per-output canonical-pair route does not certify it.
    return None


def avoid_by_bicyclic_odd_barbell(n: int, gates: list[Gate]):
    if len(gates) <= n:
        raise ValueError("range avoidance requires m>n")
    found = find_bicyclic_odd_barbell(n, gates)
    if found is None:
        raise ValueError("no simple bicyclic odd barbell component detected")
    edges, witness = found
    y = [0] * len(gates)

    left_end = _apply_walk(
        y, gates, edges,
        list(witness.left_cycle.vertices), list(witness.left_cycle.edge_ids), 0,
    )
    if left_end != 1:
        raise AssertionError("left signed cycle is not odd")

    if witness.connector is None:
        # Shared branch vertex: target the second odd cycle from the opposite
        # polarity, closing 0 -> 1 -> 0 in the implication SCC.
        right_start = 1
    else:
        right_start = _apply_walk(
            y, gates, edges,
            list(witness.connector.vertices), list(witness.connector.edge_ids), 1,
        )

    right_end = _apply_walk(
        y, gates, edges,
        list(witness.right_cycle.vertices), list(witness.right_cycle.edge_ids), right_start,
    )
    if right_end != (right_start ^ 1):
        raise AssertionError("right signed cycle is not odd")

    return tuple(y), {
        "case": "bicyclic_odd_barbell",
        "kind": witness.kind,
        "component_vertices": len(witness.component_vertices),
        "component_edges": len(witness.component_edge_ids),
        "left_cycle_length": len(witness.left_cycle.edge_ids),
        "connector_length": 0 if witness.connector is None else len(witness.connector.edge_ids),
        "right_cycle_length": len(witness.right_cycle.edge_ids),
    }
