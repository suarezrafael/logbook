from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from itertools import product


@dataclass(frozen=True)
class Gate:
    support: tuple[int, int, int]
    mask: int

    def value(self, x: tuple[int, ...]) -> int:
        idx = sum((x[v] & 1) << j for j, v in enumerate(self.support))
        return (self.mask >> idx) & 1


def majority(bits: tuple[int, int, int]) -> int:
    return 1 if sum(bits) >= 2 else 0


def mask_from_polarity(polarity: tuple[int, int, int]) -> int:
    mask = 0
    for bits in product((0, 1), repeat=3):
        value = majority(tuple(bits[j] ^ polarity[j] for j in range(3)))
        idx = sum(bits[j] << j for j in range(3))
        mask |= value << idx
    return mask


SIGNED_MAJORITY_POLARITIES = {
    mask_from_polarity(tuple((p >> j) & 1 for j in range(3))):
    tuple((p >> j) & 1 for j in range(3))
    for p in range(8)
}


def majority_polarity(g: Gate) -> tuple[int, int, int] | None:
    return SIGNED_MAJORITY_POLARITIES.get(g.mask)


@dataclass(frozen=True)
class PairEdge:
    gate_index: int
    u: int
    v: int
    delta: int


@dataclass(frozen=True)
class Triangle:
    vertices: tuple[int, int, int]
    edge_ids: tuple[int, int, int]


def canonical_pair_edges(gates: list[Gate]) -> list[PairEdge]:
    edges = []
    for i, g in enumerate(gates):
        p = majority_polarity(g)
        if p is None:
            raise ValueError("V105 dumbbell detector requires signed-majority gates")
        u, v = g.support[0], g.support[1]
        if u == v:
            raise ValueError("essential signed-majority support must use distinct variables")
        # If the selected target is chosen so that x_u=a is the bad endpoint
        # value, the induced pair clause implies x_v=a XOR delta.
        delta = 1 ^ p[0] ^ p[1]
        edges.append(PairEdge(i, u, v, delta))
    return edges


def _odd_triangles(n: int, edges: list[PairEdge]) -> list[Triangle]:
    by_pair: dict[tuple[int, int], list[int]] = {}
    for ei, e in enumerate(edges):
        key = (min(e.u, e.v), max(e.u, e.v))
        by_pair.setdefault(key, []).append(ei)

    triangles: list[Triangle] = []
    for a in range(n):
        for b in range(a + 1, n):
            ab = by_pair.get((a, b), ())
            if not ab:
                continue
            for c in range(b + 1, n):
                bc = by_pair.get((b, c), ())
                ca = by_pair.get((a, c), ())
                if not bc or not ca:
                    continue
                for eab in ab:
                    for ebc in bc:
                        for eca in ca:
                            if len({eab, ebc, eca}) < 3:
                                continue
                            parity = edges[eab].delta ^ edges[ebc].delta ^ edges[eca].delta
                            if parity == 1:
                                triangles.append(Triangle((a, b, c), (eab, ebc, eca)))
    return triangles


def _path_between_triangles(
    n: int,
    edges: list[PairEdge],
    left: Triangle,
    right: Triangle,
):
    left_vertices = set(left.vertices)
    right_vertices = set(right.vertices)
    blocked_edges = set(left.edge_ids) | set(right.edge_ids)

    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for ei, e in enumerate(edges):
        if ei in blocked_edges:
            continue
        adjacency[e.u].append((e.v, ei))
        adjacency[e.v].append((e.u, ei))

    for start in left.vertices:
        for end in right.vertices:
            banned = (left_vertices | right_vertices) - {start, end}
            queue = deque([start])
            parent: dict[int, tuple[int, int] | None] = {start: None}
            while queue:
                u = queue.popleft()
                if u == end:
                    vertices = [end]
                    edge_ids = []
                    cur = end
                    while parent[cur] is not None:
                        prev, edge_id = parent[cur]
                        vertices.append(prev)
                        edge_ids.append(edge_id)
                        cur = prev
                    vertices.reverse()
                    edge_ids.reverse()
                    return start, end, vertices, edge_ids
                for v, edge_id in adjacency[u]:
                    if v in banned or v in parent:
                        continue
                    parent[v] = (u, edge_id)
                    queue.append(v)
    return None


def find_odd_triangle_dumbbell(n: int, gates: list[Gate]):
    edges = canonical_pair_edges(gates)
    triangles = _odd_triangles(n, edges)
    for i, left in enumerate(triangles):
        lv = set(left.vertices)
        for right in triangles[i + 1 :]:
            if lv & set(right.vertices):
                continue
            witness = _path_between_triangles(n, edges, left, right)
            if witness is not None:
                return edges, left, right, witness
    return None


def _edge_orientation(edge: PairEdge, source: int) -> tuple[int, int]:
    if source == edge.u:
        return edge.u, edge.v
    if source == edge.v:
        return edge.v, edge.u
    raise ValueError("source is not incident to edge")


def _target_for_source(g: Gate, source: int, source_value: int) -> int:
    p = majority_polarity(g)
    if p is None:
        raise ValueError("not a signed-majority gate")
    pos = g.support.index(source)
    # source_value = 1-target XOR p_source
    return 1 ^ p[pos] ^ source_value


def _transport(edge: PairEdge, value: int) -> int:
    return value ^ edge.delta


def _triangle_walk(triangle: Triangle, start: int, edges: list[PairEdge]):
    a, b, c = triangle.vertices
    others = [v for v in (a, b, c) if v != start]
    order = [start, others[0], others[1], start]
    edge_lookup = {}
    for ei in triangle.edge_ids:
        e = edges[ei]
        edge_lookup[frozenset((e.u, e.v))] = ei
    walk_edges = [edge_lookup[frozenset((order[j], order[j + 1]))] for j in range(3)]
    return order, walk_edges


def _apply_walk(
    y: list[int],
    gates: list[Gate],
    edges: list[PairEdge],
    vertices: list[int],
    edge_ids: list[int],
    start_value: int,
) -> int:
    value = start_value
    for j, ei in enumerate(edge_ids):
        source = vertices[j]
        edge = edges[ei]
        _edge_orientation(edge, source)
        gate_index = edge.gate_index
        y[gate_index] = _target_for_source(gates[gate_index], source, value)
        value = _transport(edge, value)
    return value


def avoid_by_odd_triangle_dumbbell(n: int, gates: list[Gate]):
    if len(gates) <= n:
        raise ValueError("range avoidance requires m>n")
    witness = find_odd_triangle_dumbbell(n, gates)
    if witness is None:
        raise ValueError("canonical pair graph has no detected odd-triangle dumbbell")

    edges, left, right, path_info = witness
    start, end, path_vertices, path_edges = path_info
    y = [0] * len(gates)

    # Left odd triangle: a -> not a.
    left_vertices, left_edges = _triangle_walk(left, start, edges)
    left_end = _apply_walk(y, gates, edges, left_vertices, left_edges, 0)
    assert left_end == 1

    # Connecting path: not a -> b. Its contraposition also gives not b -> a.
    b = _apply_walk(y, gates, edges, path_vertices, path_edges, 1)

    # Right odd triangle: b -> not b.
    right_vertices, right_edges = _triangle_walk(right, end, edges)
    right_end = _apply_walk(y, gates, edges, right_vertices, right_edges, b)
    assert right_end == (b ^ 1)

    return tuple(y), {
        "case": "odd_triangle_dumbbell",
        "left_triangle": left.vertices,
        "right_triangle": right.vertices,
        "path_vertices": tuple(path_vertices),
        "used_outputs": len(left_edges) + len(path_edges) + len(right_edges),
    }


def in_range(n: int, gates: list[Gate], y: tuple[int, ...]) -> bool:
    return any(tuple(g.value(x) for g in gates) == y for x in product((0, 1), repeat=n))


def strict_family(internal_path_vertices: int):
    r = internal_path_vertices
    if r < 2:
        raise ValueError("strict family uses at least two internal path vertices")

    a0, a1, a2 = 0, 1, 2
    path_internal = list(range(3, 3 + r))
    b0, b1, b2 = 3 + r, 4 + r, 5 + r
    n = r + 6
    gates: list[Gate] = []

    # Canonical pair graph left triangle. One third-literal polarity conflict
    # makes the full incidence component switching-unbalanced while leaving all
    # selected pair signs unchanged.
    gates.append(Gate((a0, a1, a2), mask_from_polarity((0, 0, 1))))
    gates.append(Gate((a1, a2, a0), mask_from_polarity((0, 0, 0))))
    gates.append(Gate((a2, a0, a1), mask_from_polarity((0, 0, 0))))

    path = [a0] + path_internal + [b0]
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        third = path[i + 2] if i + 2 < len(path) else b1
        gates.append(Gate((u, v, third), mask_from_polarity((0, 0, 0))))

    gates.append(Gate((b0, b1, b2), mask_from_polarity((0, 0, 0))))
    gates.append(Gate((b1, b2, b0), mask_from_polarity((0, 0, 0))))
    gates.append(Gate((b2, b0, b1), mask_from_polarity((0, 0, 0))))

    assert len(gates) == n + 1
    return n, gates
