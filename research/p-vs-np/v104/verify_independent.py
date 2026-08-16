from __future__ import annotations

import json
import random
from itertools import product


def value(gate, x_bits):
    mask, support = gate
    idx = sum((x_bits[v] & 1) << j for j, v in enumerate(support))
    return (mask >> idx) & 1


def target(gate):
    mask, support = gate
    arity = len(support)
    ones = (mask & ((1 << (1 << arity)) - 1)).bit_count()
    return 1 if ones < (1 << arity) - ones else 0


def fiber(gate, bit):
    mask, support = gate
    return [p for p in product((0, 1), repeat=len(support)) if ((mask >> sum(p[j] << j for j in range(len(p)))) & 1) == bit]


def local_hull_rows(gate, bit):
    mask, support = gate
    points = fiber(gate, bit)
    if not points:
        return None
    candidates = []
    for coeff in range(1, 1 << len(support)):
        vals = {sum(((coeff >> j) & 1) * p[j] for j in range(len(support))) & 1 for p in points}
        if len(vals) == 1:
            candidates.append((coeff, next(iter(vals))))
    basis = {}
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
        assert not (c == 0 and r)
    lifted = []
    for local, rhs in chosen:
        row = 0
        for j, v in enumerate(support):
            if (local >> j) & 1:
                row |= 1 << v
        lifted.append((row, rhs))
    return lifted


class System:
    def __init__(self, dimension):
        self.dimension = dimension
        self.rows = {}

    def copy(self):
        z = System(self.dimension)
        z.rows = dict(self.rows)
        return z

    @property
    def rank(self):
        return len(self.rows)

    def add(self, coeff, rhs):
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

    def add_many(self, rows):
        old = self.rank
        for row, rhs in rows:
            self.add(row, rhs)
        return self.rank - old

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


def functional_relation(gate, bit, head):
    _mask, support = gate
    if head not in support:
        return None
    hpos = support.index(head)
    tail_positions = [j for j in range(len(support)) if j != hpos]
    tails = tuple(support[j] for j in tail_positions)
    mapping = {}
    for p in fiber(gate, bit):
        key = tuple(p[j] for j in tail_positions)
        val = p[hpos]
        if key in mapping and mapping[key] != val:
            return None
        mapping[key] = val
    for key in product((0, 1), repeat=len(tails)):
        mapping.setdefault(tuple(key), 0)
    return tails, mapping


def acyclic(n, relations):
    out = [[] for _ in range(n)]
    indeg = [0] * n
    for head, (tails, _mapping) in relations.items():
        for tail in tails:
            out[tail].append(head)
            indeg[head] += 1
    q = [i for i, d in enumerate(indeg) if d == 0]
    order = []
    while q:
        u = q.pop()
        order.append(u)
        for v in out[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == n else None


def canonical_avoider(n, gates):
    m = len(gates)
    bits = [target(g) for g in gates]
    system = System(n)
    affine = []
    protected = set()

    for i, gate in enumerate(gates):
        rows = local_hull_rows(gate, bits[i])
        if rows is None:
            y = [0] * m
            y[i] = bits[i]
            return tuple(y), {"case": "empty", "eta": n}
        trial = system.copy()
        try:
            gain = trial.add_many(rows)
        except ValueError:
            y = [0] * m
            for j in affine:
                y[j] = bits[j]
            y[i] = bits[i]
            return tuple(y), {"case": "inconsistent", "eta": n - system.rank}
        if gain:
            system = trial
            affine.append(i)
            for row, _rhs in rows:
                protected.update(v for v in range(n) if (row >> v) & 1)

    relations = {}
    functional = []
    affine_set = set(affine)
    for i, gate in enumerate(gates):
        if i in affine_set:
            continue
        _mask, support = gate
        for head in sorted(support):
            if head in protected or head in relations:
                continue
            relation = functional_relation(gate, bits[i], head)
            if relation is None:
                continue
            trial = dict(relations)
            trial[head] = relation
            if acyclic(n, trial) is not None:
                relations = trial
                functional.append(i)
                break

    order = acyclic(n, relations)
    assert order is not None
    roots = [v for v in range(n) if v not in relations]
    rindex = {v: i for i, v in enumerate(roots)}
    root_system = System(len(roots))
    for row, rhs in system.rows.values():
        rr = 0
        for v in roots:
            if (row >> v) & 1:
                rr |= 1 << rindex[v]
        root_system.add(rr, rhs)
    assert root_system.rank == system.rank
    eta = len(roots) - root_system.rank

    selected = affine_set | set(functional)
    residual = [i for i in range(m) if i not in selected]
    assert len(residual) > eta
    observed = set()
    count = 0
    for root_bits in root_system.solutions():
        x = [None] * n
        for v, b in zip(roots, root_bits):
            x[v] = b
        for v in order:
            if v in relations:
                tails, mapping = relations[v]
                x[v] = mapping[tuple(int(x[t]) for t in tails)]
        full = tuple(int(v) for v in x)
        observed.add(tuple(value(gates[i], full) for i in residual))
        count += 1
    assert count == 1 << eta

    missing = next(word for word in product((0, 1), repeat=len(residual)) if word not in observed)
    y = [0] * m
    for i in affine:
        y[i] = bits[i]
    for i in functional:
        y[i] = bits[i]
    for i, b in zip(residual, missing):
        y[i] = b
    return tuple(y), {"case": "canonical", "rank": system.rank, "f": len(functional), "eta": eta}


def in_range(n, gates, y):
    for x in product((0, 1), repeat=n):
        if tuple(value(g, x) for g in gates) == y:
            return True
    return False


def family(k):
    a = b = 4 * k
    n = a + b
    gates = []
    for i in range(a):
        gates.append((0x1E, (i, (i + 1) % a, (i + 2) % a)))
    off = a
    for j in range(k):
        aa, bb, cc, dd = off + 4*j, off + 4*j + 1, off + 4*j + 2, off + 4*j + 3
        gates += [(0x16, (aa, bb, cc)), (0x16, (aa, bb, dd)), (0x16, (aa, cc, dd))]
        if j:
            gates.append((0x16, (off + 4*(j-1) + 3, bb, cc)))
    gates.append((0x17, (off, off + 1, off + 2)))
    gates.append((0x17, (0, off, off + 1)))
    assert len(gates) == n + 1
    return n, gates


def random_checks():
    rng = random.Random(94104)
    cases = 0
    for n in range(2, 7):
        arity = min(3, n)
        max_mask = 1 << (1 << arity)
        for _ in range(96):
            gates = [(rng.randrange(max_mask), tuple(rng.sample(range(n), arity))) for _j in range(n + 1)]
            y, meta = canonical_avoider(n, gates)
            assert not in_range(n, gates, y), (n, y, meta)
            cases += 1
    assert cases == 480
    return cases


def strict_checks():
    for k in range(1, 13):
        n, gates = family(k)
        y, meta = canonical_avoider(n, gates)
        assert meta["case"] == "canonical"
        assert meta["rank"] == 4 * k - 1
        assert meta["f"] == 4 * k - 2
        assert meta["eta"] == 3
        if k <= 2:
            assert not in_range(n, gates, y)
    return 12


def main():
    result = {
        "independent_canonical_random_cases": random_checks(),
        "independent_strict_eta_three_k_through": strict_checks(),
        "failures": 0,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
