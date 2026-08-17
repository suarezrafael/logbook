from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from itertools import combinations, product


@dataclass(frozen=True)
class Gate:
    support: tuple[int, int, int]
    polarity: tuple[int, int, int]

    def __post_init__(self):
        if len(set(self.support)) != 3:
            raise ValueError("signed-majority support must contain three distinct variables")
        if any(bit not in (0, 1) for bit in self.polarity):
            raise ValueError("polarity bits must be Boolean")

    def value(self, x: tuple[int, ...]) -> int:
        bits = [x[v] ^ p for v, p in zip(self.support, self.polarity)]
        return 1 if sum(bits) >= 2 else 0


@dataclass(frozen=True)
class PairEdge:
    gate_index: int
    u: int
    v: int
    delta: int


@dataclass(frozen=True)
class Walk:
    vertices: tuple[int, ...]
    edge_ids: tuple[int, ...]


PAIR_POSITIONS = ((0, 1), (0, 2), (1, 2))


def edge_for_choice(gate_index: int, gate: Gate, choice: int) -> PairEdge:
    i, j = PAIR_POSITIONS[choice]
    return PairEdge(
        gate_index,
        gate.support[i],
        gate.support[j],
        1 ^ gate.polarity[i] ^ gate.polarity[j],
    )


def selected_edges(gates: list[Gate], choices: tuple[int, ...]) -> list[PairEdge]:
    if len(choices) != len(gates):
        raise ValueError("one pair choice is required for every gate")
    return [edge_for_choice(i, gate, choice) for i, (gate, choice) in enumerate(zip(gates, choices))]


def _components(n: int, edges: list[PairEdge]):
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for ei, e in enumerate(edges):
        adjacency[e.u].append((e.v, ei))
        adjacency[e.v].append((e.u, ei))
    seen = set()
    for start in range(n):
        if start in seen or not adjacency[start]:
            continue
        vertices = {start}
        edge_ids = set()
        stack = [start]
        seen.add(start)
        while stack:
            u = stack.pop()
            for v, ei in adjacency[u]:
                edge_ids.add(ei)
                if v not in seen:
                    seen.add(v)
                    vertices.add(v)
                    stack.append(v)
        yield vertices, edge_ids


def _simple(edges: list[PairEdge], edge_ids: set[int]) -> bool:
    pairs = set()
    for ei in edge_ids:
        e = edges[ei]
        pair = (min(e.u, e.v), max(e.u, e.v))
        if pair in pairs:
            return False
        pairs.add(pair)
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


def _other(edge: PairEdge, v: int) -> int:
    if edge.u == v:
        return edge.v
    if edge.v == v:
        return edge.u
    raise ValueError("vertex is not incident to edge")


def _trace(start, first, branches, incident, edges, used) -> Walk:
    vertices = [start]
    edge_ids = []
    current, ei = start, first
    while True:
        if ei in used:
            raise ValueError("edge repeated while tracing bicyclic core")
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


def _parse_core(core_v: set[int], core_e: set[int], edges: list[PairEdge]):
    incident = {v: [] for v in core_v}
    for ei in core_e:
        e = edges[ei]
        incident[e.u].append(ei)
        incident[e.v].append(ei)
    degree = {v: len(incident[v]) for v in core_v}
    branches = {v for v, d in degree.items() if d != 2}
    if len(branches) == 1 and all(d in (2, 4) for d in degree.values()):
        if degree[next(iter(branches))] != 4:
            return None
    elif len(branches) == 2 and all(d in (2, 3) for d in degree.values()):
        if any(degree[v] != 3 for v in branches):
            return None
    else:
        return None
    used = set()
    walks = []
    for branch in sorted(branches):
        for ei in incident[branch]:
            if ei not in used:
                walks.append(_trace(branch, ei, branches, incident, edges, used))
    if used != core_e:
        return None
    return branches, walks


def _parity(walk: Walk, edges: list[PairEdge]) -> int:
    ans = 0
    for ei in walk.edge_ids:
        ans ^= edges[ei].delta
    return ans


def find_odd_barbell(n: int, edges: list[PairEdge]):
    for vertices, edge_ids in _components(n, edges):
        if len(edge_ids) != len(vertices) + 1 or not _simple(edges, edge_ids):
            continue
        core_v, core_e = _two_core(vertices, edge_ids, edges)
        parsed = _parse_core(core_v, core_e, edges)
        if parsed is None:
            continue
        branches, walks = parsed
        if len(branches) == 1:
            cycles = [w for w in walks if w.vertices[0] == w.vertices[-1]]
            if len(cycles) == 2 and all(_parity(w, edges) == 1 for w in cycles):
                return cycles[0], None, cycles[1], "figure_eight"
        else:
            b0, b1 = sorted(branches)
            loops = [w for w in walks if w.vertices[0] == w.vertices[-1]]
            links = [w for w in walks if w.vertices[0] != w.vertices[-1]]
            if len(loops) == 2 and len(links) == 1:
                left = next((w for w in loops if w.vertices[0] == b0), None)
                right = next((w for w in loops if w.vertices[0] == b1), None)
                if left is None or right is None:
                    continue
                link = links[0]
                if link.vertices[0] != b0:
                    link = Walk(tuple(reversed(link.vertices)), tuple(reversed(link.edge_ids)))
                if _parity(left, edges) == _parity(right, edges) == 1:
                    return left, link, right, "barbell"
    return None


def _target_for_source(gate: Gate, source: int, value: int) -> int:
    pos = gate.support.index(source)
    return 1 ^ gate.polarity[pos] ^ value


def _apply_walk(y, gates, edges, walk: Walk, start_value: int) -> int:
    value = start_value
    for j, ei in enumerate(walk.edge_ids):
        edge = edges[ei]
        source = walk.vertices[j]
        y[edge.gate_index] = _target_for_source(gates[edge.gate_index], source, value)
        value ^= edge.delta
    return value


def target_from_barbell(gates: list[Gate], edges: list[PairEdge], witness):
    left, connector, right, kind = witness
    y = [0] * len(gates)
    left_end = _apply_walk(y, gates, edges, left, 0)
    if left_end != 1:
        raise AssertionError("left cycle must be odd")
    if connector is None:
        right_start = 1
    else:
        right_start = _apply_walk(y, gates, edges, connector, 1)
    right_end = _apply_walk(y, gates, edges, right, right_start)
    if right_end != (right_start ^ 1):
        raise AssertionError("right cycle must be odd")
    return tuple(y), kind


def avoid_with_choices(n: int, gates: list[Gate], choices: tuple[int, ...]):
    edges = selected_edges(gates, choices)
    witness = find_odd_barbell(n, edges)
    if witness is None:
        raise ValueError("selected pairs contain no detected odd barbell")
    y, kind = target_from_barbell(gates, edges, witness)
    return y, {"kind": kind, "choices": choices}


def repair_choices(m: int, changed: tuple[tuple[int, int], ...]) -> tuple[int, ...]:
    choices = [0] * m
    for gate_index, choice in changed:
        if choice not in (1, 2):
            raise ValueError("repair choices must use one of the two noncanonical pairs")
        choices[gate_index] = choice
    return tuple(choices)


def avoid_with_pair_repair(n: int, gates: list[Gate], budget: int):
    """Enumerate at most `budget` noncanonical pair choices.

    Runtime is O((2m)^budget poly(N)) for fixed budget, before the final constant-
    locality implication construction.
    """
    m = len(gates)
    if m <= n:
        raise ValueError("range avoidance requires m>n")
    for used in range(budget + 1):
        for gate_indices in combinations(range(m), used):
            for alternatives in product((1, 2), repeat=used):
                changed = tuple(zip(gate_indices, alternatives))
                choices = repair_choices(m, changed)
                edges = selected_edges(gates, choices)
                witness = find_odd_barbell(n, edges)
                if witness is not None:
                    y, kind = target_from_barbell(gates, edges, witness)
                    return y, {
                        "case": "pair_repair",
                        "repair_distance": used,
                        "kind": kind,
                        "changed": changed,
                    }
    raise ValueError("no odd barbell found within the requested repair budget")


def in_range(n: int, gates: list[Gate], y: tuple[int, ...]) -> bool:
    return any(tuple(g.value(x) for g in gates) == y for x in product((0, 1), repeat=n))


def strict_one_repair_family(subdivision_pairs: int):
    """Infinite family with canonical theta core and one-switch figure-eight.

    `subdivision_pairs` must be nonnegative.  Two vertices are added per unit,
    so the left figure-eight cycle stays odd when every selected transport is 1.
    """
    q = subdivision_pairs
    if q < 0:
        raise ValueError(q)
    extra = 2 * q
    # Base vertices 0..4.  Subdivide common edge 0-2 by `extra` new vertices.
    path_internal = list(range(5, 5 + extra))
    n = 5 + extra
    gates: list[Gate] = []

    # Common figure-eight/canonical-theta edges except 0-2.
    gates.append(Gate((0, 1, 2), (0, 0, 0)))          # 0-1
    gates.append(Gate((0, 3, 4), (0, 0, 0)))          # 0-3
    gates.append(Gate((0, 4, 2), (0, 0, 0)))          # 0-4 (leaf in canonical core)
    gates.append(Gate((1, 2, 3), (0, 0, 0)))          # 1-2

    # The only repaired gate: canonical 1-3, alternate pair (positions 1,2)=3-4.
    # p_1=p_2=0 makes the repaired edge transport odd; p_0=1 also destroys a
    # global switching-to-monotone assignment when combined with the positive gates.
    repair_gate_index = len(gates)
    gates.append(Gate((1, 3, 4), (1, 0, 0)))

    path = [0] + path_internal + [2]
    for i, (u, v) in enumerate(zip(path, path[1:])):
        # Variable 1 is distinct from every path endpoint.
        gates.append(Gate((u, v, 1), (0, 0, 0)))

    assert len(gates) == n + 1
    return n, gates, repair_gate_index
