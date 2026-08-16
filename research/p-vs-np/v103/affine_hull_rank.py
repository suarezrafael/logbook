from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Iterable


@dataclass(frozen=True)
class Gate:
    support: tuple[int, ...]
    mask: int

    @property
    def arity(self) -> int:
        return len(self.support)

    def value_local(self, bits: tuple[int, ...]) -> int:
        idx = sum((b & 1) << j for j, b in enumerate(bits))
        return (self.mask >> idx) & 1

    def value(self, assignment: tuple[int, ...]) -> int:
        return self.value_local(tuple(assignment[v] for v in self.support))


def canonical_target(g: Gate) -> int:
    ones = (g.mask & ((1 << (1 << g.arity)) - 1)).bit_count()
    zeros = (1 << g.arity) - ones
    return 1 if ones < zeros else 0


def fiber(g: Gate, target: int) -> list[tuple[int, ...]]:
    return [bits for bits in product((0, 1), repeat=g.arity) if g.value_local(bits) == target]


def local_affine_hull_equations(g: Gate, target: int) -> list[tuple[int, int]] | None:
    """Independent equations for aff(fiber); None denotes an empty fiber."""
    points = fiber(g, target)
    if not points:
        return None
    candidates: list[tuple[int, int]] = []
    for coeff in range(1, 1 << g.arity):
        values = {
            sum(((coeff >> j) & 1) * p[j] for j in range(g.arity)) & 1
            for p in points
        }
        if len(values) == 1:
            candidates.append((coeff, next(iter(values))))
    basis: dict[int, tuple[int, int]] = {}
    chosen: list[tuple[int, int]] = []
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
            raise AssertionError("valid equations on a nonempty fiber cannot conflict")
    return chosen


def lift_equations(g: Gate, local_eqs: Iterable[tuple[int, int]]) -> list[tuple[int, int]]:
    out = []
    for local_mask, rhs in local_eqs:
        global_mask = 0
        for j, v in enumerate(g.support):
            if (local_mask >> j) & 1:
                global_mask |= 1 << v
        out.append((global_mask, rhs))
    return out


class LinearSystem:
    def __init__(self, n: int):
        self.n = n
        self.rows: dict[int, tuple[int, int]] = {}

    @property
    def rank(self) -> int:
        return len(self.rows)

    def copy(self) -> "LinearSystem":
        other = LinearSystem(self.n)
        other.rows = dict(self.rows)
        return other

    def add(self, coeff: int, rhs: int) -> bool:
        c, r = coeff, rhs & 1
        while c:
            pivot = c.bit_length() - 1
            if pivot not in self.rows:
                for q, (ec, er) in list(self.rows.items()):
                    if (ec >> pivot) & 1:
                        self.rows[q] = (ec ^ c, er ^ r)
                self.rows[pivot] = (c, r)
                return True
            bc, br = self.rows[pivot]
            c ^= bc
            r ^= br
        if r:
            raise ValueError("inconsistent affine system")
        return False

    def add_many(self, equations: Iterable[tuple[int, int]]) -> int:
        before = self.rank
        for coeff, rhs in equations:
            self.add(coeff, rhs)
        return self.rank - before

    def solutions(self) -> Iterable[tuple[int, ...]]:
        pivots = set(self.rows)
        free = [v for v in range(self.n) if v not in pivots]
        for free_bits in product((0, 1), repeat=len(free)):
            x = [0] * self.n
            for v, b in zip(free, free_bits):
                x[v] = b
            for pivot in sorted(self.rows):
                coeff, rhs = self.rows[pivot]
                value = rhs
                rest = coeff & ~(1 << pivot)
                while rest:
                    lsb = rest & -rest
                    j = lsb.bit_length() - 1
                    value ^= x[j]
                    rest ^= lsb
                x[pivot] = value
            for coeff, rhs in self.rows.values():
                assert (sum(x[j] for j in range(self.n) if (coeff >> j) & 1) & 1) == rhs
            yield tuple(x)


def first_missing_from_observed(observed: set[tuple[int, ...]], length: int) -> tuple[int, ...]:
    q = len(observed)
    for z in range(q + 1):
        bits = tuple((z >> j) & 1 for j in range(length))
        if bits not in observed:
            return bits
    raise AssertionError("q+1 candidates cannot all lie in a q-element observed set")


def avoid_by_affine_hulls(n: int, gates: list[Gate]) -> tuple[tuple[int, ...], dict]:
    m = len(gates)
    if m <= n:
        raise ValueError("range avoidance requires m>n")

    system = LinearSystem(n)
    selected: list[int] = []
    targets = [canonical_target(g) for g in gates]

    for i, (g, target) in enumerate(zip(gates, targets)):
        local = local_affine_hull_equations(g, target)
        if local is None:
            y = [0] * m
            y[i] = target
            return tuple(y), {
                "case": "empty_fiber",
                "rank": system.rank,
                "nu": n - system.rank,
                "selected": selected,
            }
        equations = lift_equations(g, local)
        trial = system.copy()
        try:
            gain = trial.add_many(equations)
        except ValueError:
            # The retained canonical hulls together with gate i are already
            # inconsistent. Returning the complete canonical target vector is
            # the simplest auditable witness: any preimage would satisfy every
            # one of those inconsistent relaxed constraints.
            return tuple(targets), {
                "case": "inconsistent_hulls",
                "rank": system.rank,
                "nu": n - system.rank,
                "selected": selected,
                "conflict_gate": i,
            }
        if gain > 0:
            system = trial
            selected.append(i)

    rank = system.rank
    nu = n - rank
    selected_set = set(selected)
    residual_indices = [i for i in range(m) if i not in selected_set]
    assert len(selected) <= rank
    assert len(residual_indices) > nu

    observed: set[tuple[int, ...]] = set()
    solution_count = 0
    for x in system.solutions():
        solution_count += 1
        observed.add(tuple(gates[i].value(x) for i in residual_indices))
    assert solution_count == 1 << nu

    missing = first_missing_from_observed(observed, len(residual_indices))
    y = [0] * m
    for i in selected:
        y[i] = targets[i]
    for i, b in zip(residual_indices, missing):
        y[i] = b
    return tuple(y), {
        "case": "rank_enumeration",
        "rank": rank,
        "nu": nu,
        "selected": selected,
        "residual": residual_indices,
        "relaxed_solutions": solution_count,
        "observed_residual": len(observed),
    }


def in_range(n: int, gates: list[Gate], y: tuple[int, ...]) -> bool:
    for x in product((0, 1), repeat=n):
        if tuple(g.value(x) for g in gates) == y:
            return True
    return False


def essential(mask: int, arity: int = 3) -> bool:
    for j in range(arity):
        depends = False
        for idx in range(1 << arity):
            if ((idx >> j) & 1) == 0:
                if ((mask >> idx) & 1) != ((mask >> (idx | (1 << j))) & 1):
                    depends = True
                    break
        if not depends:
            return False
    return True


def canonical_hull_proper(mask: int) -> bool:
    g = Gate(tuple(range(3)), mask)
    eqs = local_affine_hull_equations(g, canonical_target(g))
    return eqs is None or len(eqs) > 0


def strict_family(k: int) -> tuple[int, list[Gate]]:
    if k < 1:
        raise ValueError(k)
    n = 4 * k
    gates: list[Gate] = []
    for j in range(k):
        a, b, c, d = 4 * j, 4 * j + 1, 4 * j + 2, 4 * j + 3
        gates.extend([
            Gate((a, b, c), 0x16),
            Gate((a, b, d), 0x16),
            Gate((a, c, d), 0x16),
        ])
        if j >= 1:
            gates.append(Gate((4 * (j - 1) + 3, b, c), 0x16))
    gates.append(Gate((0, 1, 2), 0x17))
    a, b, c = 4 * (k - 1), 4 * (k - 1) + 1, 4 * (k - 1) + 2
    gates.append(Gate((a, b, c), 0x17))
    assert len(gates) == n + 1
    return n, gates


def hull_rank_for_targets(n: int, gates: list[Gate]) -> tuple[int, bool]:
    system = LinearSystem(n)
    try:
        for g in gates:
            target = canonical_target(g)
            local = local_affine_hull_equations(g, target)
            if local is None:
                return system.rank, False
            system.add_many(lift_equations(g, local))
    except ValueError:
        return system.rank, False
    return system.rank, True
