from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Iterable


@dataclass(frozen=True)
class Gate:
    support: tuple[int, ...]
    mask: int

    def local_value(self, bits: tuple[int, ...]) -> int:
        idx = sum((b & 1) << j for j, b in enumerate(bits))
        return (self.mask >> idx) & 1

    def value(self, x: tuple[int, ...]) -> int:
        return self.local_value(tuple(x[v] for v in self.support))


def canonical_target(g: Gate) -> int:
    arity = len(g.support)
    ones = (g.mask & ((1 << (1 << arity)) - 1)).bit_count()
    zeros = (1 << arity) - ones
    return 1 if ones < zeros else 0


def fiber(g: Gate, target: int) -> list[tuple[int, ...]]:
    return [bits for bits in product((0, 1), repeat=len(g.support)) if g.local_value(bits) == target]


def functional_total_map(g: Gate, target: int, head: int):
    if head not in g.support:
        return None
    hpos = g.support.index(head)
    tail_positions = [j for j in range(len(g.support)) if j != hpos]
    tails = tuple(g.support[j] for j in tail_positions)
    mapping: dict[tuple[int, ...], int] = {}
    for p in fiber(g, target):
        key = tuple(p[j] for j in tail_positions)
        val = p[hpos]
        if key in mapping and mapping[key] != val:
            return None
        mapping[key] = val
    for key in product((0, 1), repeat=len(tails)):
        mapping.setdefault(tuple(key), 0)
    return tails, mapping


def local_affine_hull_equations(g: Gate, target: int) -> list[tuple[int, int]] | None:
    points = fiber(g, target)
    if not points:
        return None
    candidates = []
    for coeff in range(1, 1 << len(g.support)):
        vals = {
            sum(((coeff >> j) & 1) * p[j] for j in range(len(g.support))) & 1
            for p in points
        }
        if len(vals) == 1:
            candidates.append((coeff, next(iter(vals))))
    basis: dict[int, tuple[int, int]] = {}
    chosen = []
    for coeff, rhs in candidates:
        c, r = coeff, rhs
        while c:
            pivot = c.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = (c, r)
                chosen.append((coeff, rhs))
                break
            bc, br = basis[pivot]
            c ^= bc
            r ^= br
        if c == 0 and r:
            raise AssertionError("equations valid on one nonempty fiber cannot conflict")
    return chosen


class LinearSystem:
    def __init__(self, dimension: int):
        self.dimension = dimension
        self.rows: dict[int, tuple[int, int]] = {}

    @property
    def rank(self) -> int:
        return len(self.rows)

    def copy(self):
        other = LinearSystem(self.dimension)
        other.rows = dict(self.rows)
        return other

    def add(self, coeff: int, rhs: int) -> bool:
        c, r = coeff, rhs & 1
        while c:
            pivot = c.bit_length() - 1
            if pivot not in self.rows:
                self.rows[pivot] = (c, r)
                return True
            bc, br = self.rows[pivot]
            c ^= bc
            r ^= br
        if r:
            raise ValueError("inconsistent")
        return False

    def add_many(self, rows: Iterable[tuple[int, int]]) -> int:
        before = self.rank
        for c, r in rows:
            self.add(c, r)
        return self.rank - before

    def solutions(self):
        pivots = set(self.rows)
        free = [i for i in range(self.dimension) if i not in pivots]
        for free_bits in product((0, 1), repeat=len(free)):
            x = [0] * self.dimension
            for i, b in zip(free, free_bits):
                x[i] = b
            for pivot in sorted(self.rows):
                coeff, rhs = self.rows[pivot]
                val = rhs
                rest = coeff & ~(1 << pivot)
                while rest:
                    bit = rest & -rest
                    j = bit.bit_length() - 1
                    val ^= x[j]
                    rest ^= bit
                x[pivot] = val
            yield tuple(x)


def _topological_order(n: int, relations: dict[int, tuple[tuple[int, ...], dict]]) -> list[int]:
    out = [[] for _ in range(n)]
    indeg = [0] * n
    for head, (tails, _mapping) in relations.items():
        for tail in tails:
            out[tail].append(head)
            indeg[head] += 1
    queue = [i for i in range(n) if indeg[i] == 0]
    order = []
    while queue:
        u = queue.pop()
        order.append(u)
        for v in out[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    if len(order) != n:
        raise ValueError("functional certificate is cyclic")
    return order


def avoid_with_certificate(
    n: int,
    gates: list[Gate],
    functional_certificate: list[tuple[int, int, int]],
    affine_candidates: list[int],
):
    m = len(gates)
    if m <= n:
        raise ValueError("requires m>n")

    relations: dict[int, tuple[tuple[int, ...], dict]] = {}
    functional_indices = set()
    functional_targets: dict[int, int] = {}
    for idx, target, head in functional_certificate:
        if idx in functional_indices or idx in affine_candidates:
            raise ValueError("selected output blocks must be disjoint")
        relation = functional_total_map(gates[idx], target, head)
        if relation is None or head in relations:
            raise ValueError("invalid functional anchor certificate")
        relations[head] = relation
        functional_indices.add(idx)
        functional_targets[idx] = target

    topo = _topological_order(n, relations)
    roots = [v for v in range(n) if v not in relations]
    root_index = {v: i for i, v in enumerate(roots)}
    system = LinearSystem(len(roots))
    affine_selected: list[int] = []
    affine_targets: dict[int, int] = {}

    for idx in affine_candidates:
        if idx in functional_indices:
            raise ValueError("selected output blocks must be disjoint")
        g = gates[idx]
        target = canonical_target(g)
        local = local_affine_hull_equations(g, target)
        if local is None:
            y = [0] * m
            for i, b in functional_targets.items():
                y[i] = b
            y[idx] = target
            return tuple(y), {"case": "empty_affine_fiber", "eta": len(roots), "roots": roots}
        lifted = []
        for local_mask, rhs in local:
            coeff = 0
            for j, v in enumerate(g.support):
                if (local_mask >> j) & 1:
                    if v not in root_index:
                        raise ValueError("affine hull equation is not root-supported")
                    coeff |= 1 << root_index[v]
            lifted.append((coeff, rhs))
        trial = system.copy()
        try:
            gain = trial.add_many(lifted)
        except ValueError:
            y = [0] * m
            for i, b in functional_targets.items():
                y[i] = b
            for i in affine_selected:
                y[i] = affine_targets[i]
            y[idx] = target
            return tuple(y), {"case": "inconsistent_root_hulls", "eta": len(roots) - system.rank, "roots": roots}
        if gain > 0:
            system = trial
            affine_selected.append(idx)
            affine_targets[idx] = target

    eta = len(roots) - system.rank
    selected = functional_indices | set(affine_selected)
    residual = [i for i in range(m) if i not in selected]
    if len(residual) <= eta:
        raise AssertionError("m>n and block-count<=codimension must leave more than eta outputs")

    observed = set()
    relaxed_count = 0
    for root_bits in system.solutions():
        x: list[int | None] = [None] * n
        for v, b in zip(roots, root_bits):
            x[v] = b
        for v in topo:
            if v not in relations:
                continue
            tails, mapping = relations[v]
            key = tuple(int(x[t]) for t in tails)
            x[v] = mapping[key]
        if any(v is None for v in x):
            raise AssertionError("DAG extension incomplete")
        full = tuple(int(v) for v in x)
        relaxed_count += 1
        observed.add(tuple(gates[i].value(full) for i in residual))
    if relaxed_count != 1 << eta:
        raise AssertionError((relaxed_count, eta))

    missing = None
    for z in range(len(observed) + 1):
        word = tuple((z >> j) & 1 for j in range(len(residual)))
        if word not in observed:
            missing = word
            break
    if missing is None:
        raise AssertionError("pigeonhole candidate search failed")

    y = [0] * m
    for i, b in functional_targets.items():
        y[i] = b
    for i, b in affine_targets.items():
        y[i] = b
    for i, b in zip(residual, missing):
        y[i] = b
    return tuple(y), {
        "case": "hybrid_enumeration",
        "functional_blocks": len(functional_indices),
        "affine_blocks": len(affine_selected),
        "roots": roots,
        "root_rank": system.rank,
        "eta": eta,
        "relaxed_assignments": relaxed_count,
        "residual_outputs": len(residual),
        "observed_residual": len(observed),
    }


def in_range(n: int, gates: list[Gate], y: tuple[int, ...]) -> bool:
    return any(tuple(g.value(x) for g in gates) == y for x in product((0, 1), repeat=n))


def strict_family(k: int):
    if k < 1:
        raise ValueError(k)
    a = 4 * k
    b = 4 * k
    n = a + b
    gates: list[Gate] = []
    for i in range(a):
        gates.append(Gate((i, (i + 1) % a, (i + 2) % a), 0x1E))
    off = a
    for j in range(k):
        aa, bb, cc, dd = off + 4*j, off + 4*j + 1, off + 4*j + 2, off + 4*j + 3
        gates.extend([
            Gate((aa, bb, cc), 0x16),
            Gate((aa, bb, dd), 0x16),
            Gate((aa, cc, dd), 0x16),
        ])
        if j:
            gates.append(Gate((off + 4*(j-1) + 3, bb, cc), 0x16))
    gates.append(Gate((off, off + 1, off + 2), 0x17))
    gates.append(Gate((0, off, off + 1), 0x17))
    assert len(gates) == n + 1
    functional = [(i, 0, i + 2) for i in range(a - 2)]
    affine = list(range(a, a + b - 1))
    return n, gates, functional, affine
