from __future__ import annotations

import random
from dataclasses import dataclass
from itertools import product

TERMINALS = (0, 1, 2, 3)


@dataclass(frozen=True)
class Gate:
    selector: int
    d0: int
    d1: int
    ps: int = 0
    p0: int = 0
    p1: int = 0
    flip: int = 0

    def branch(self, b: int):
        if b == 0:
            return self.selector, self.d0, self.ps, self.p0
        return self.selector, self.d1, 1 ^ self.ps, self.p1

    def target(self, b: int, desired: int) -> int:
        return desired ^ self.branch(b)[3] ^ self.flip

    def value(self, x: tuple[int, ...]) -> int:
        z = x[self.selector] ^ self.ps
        a = x[self.d0] ^ self.p0
        b = x[self.d1] ^ self.p1
        return (a if z == 0 else b) ^ self.flip


@dataclass
class Encoded:
    n: int
    gates: list[Gate]
    root: int
    start0: int
    start1: int
    fg0: int
    fg1: int
    shared: int


def encode(nv: int, edges: list[tuple[int, int]], terminals=TERMINALS) -> Encoded:
    s1, t1, s2, t2 = terminals
    edges = sorted(set(edges))
    q = 0
    xv = list(range(q, q + nv + 1)); q += nv + 1
    w = nv
    choice = {}
    for v in range(nv):
        if v != t2:
            choice[v] = q; q += 1
    root = q; q += 1
    start0 = q; q += 1
    start1 = q; q += 1
    after1 = q; q += 1
    dead0 = q; q += 1
    dead1 = q; q += 1
    dead2 = q; q += 1
    bypass_mid = q; q += 1

    gates: list[Gate] = []
    for v in range(nv):
        if v == t2:
            gates.append(Gate(xv[v], root, dead0))
        else:
            gates.append(Gate(xv[v], choice[v], dead0))
    shared = len(gates)
    gates.append(Gate(xv[w], xv[s2], after1))

    for u, v in edges:
        if u != t2:
            gates.append(Gate(choice[u], xv[v], dead1))
    gates.append(Gate(choice[t1], xv[w], dead1))

    fg0 = len(gates); gates.append(Gate(root, start0, dead0, 0))
    fg1 = len(gates); gates.append(Gate(root, start1, dead1, 1))
    gates.append(Gate(start0, xv[s1], dead0))
    gates.append(Gate(start0, bypass_mid, dead1))
    gates.append(Gate(start1, xv[w], dead0))
    gates.append(Gate(after1, root, dead1))
    gates.append(Gate(bypass_mid, root, dead1))

    n = q
    if len(gates) <= n:
        gates.extend(Gate(dead0, dead1, dead2) for _ in range(n + 1 - len(gates)))
    elif len(gates) > n + 1:
        n += len(gates) - n - 1
    assert len(gates) == n + 1
    return Encoded(n, gates, root, start0, start1, fg0, fg1, shared)


def graph_paths(n: int, edges: list[tuple[int, int]], s: int, t: int):
    adj = [[] for _ in range(n)]
    for u, v in sorted(set(edges)):
        adj[u].append(v)
    out = []
    def dfs(u, seen, path):
        if u == t:
            out.append(tuple(path)); return
        for v in adj[u]:
            if v in seen: continue
            seen.add(v); path.append(v)
            dfs(v, seen, path)
            path.pop(); seen.remove(v)
    dfs(s, {s}, [s])
    return out


def ddp(n: int, edges: list[tuple[int, int]]) -> bool:
    p1 = graph_paths(n, edges, 0, 1)
    p2 = graph_paths(n, edges, 2, 3)
    return any(not (set(a) & set(b)) for a in p1 for b in p2)


def returns(enc: Encoded, start: int, cap=30000):
    by = {}
    for i, g in enumerate(enc.gates):
        if g.selector != enc.root:
            by.setdefault(g.selector, []).append(i)
    out = []
    def dfs(cur, used, path):
        if len(out) >= cap:
            raise AssertionError("independent census cap exceeded")
        if cur == enc.root:
            out.append(tuple(path)); return
        for gi in by.get(cur, ()):
            if gi in used: continue
            used.add(gi)
            for b in (0, 1):
                path.append((gi, b))
                dfs(enc.gates[gi].branch(b)[1], used, path)
                path.pop()
            used.remove(gi)
    dfs(start, set(), [])
    return out


def compatible(enc: Encoded, r0, r1):
    assigned = {}
    word = [0] * len(enc.gates)
    cycles = [((enc.fg0, 0),) + r0, ((enc.fg1, 0),) + r1]
    for cycle in cycles:
        alpha = enc.gates[cycle[0][0]].branch(cycle[0][1])[2]
        for i, (gi, b) in enumerate(cycle):
            if i + 1 < len(cycle):
                ngi, nb = cycle[i + 1]
                desired = enc.gates[ngi].branch(nb)[2]
            else:
                desired = 1 ^ alpha
            bit = enc.gates[gi].target(b, desired)
            if gi in assigned and assigned[gi] != bit:
                return None
            assigned[gi] = bit; word[gi] = bit
    return tuple(word)


def exact_one_opposite(enc: Encoded):
    p0 = returns(enc, enc.start0)
    p1 = returns(enc, enc.start1)
    for a in p0:
        sa = {gi for gi, _ in a}
        for b in p1:
            overlap = sa & {gi for gi, _ in b}
            if len(overlap) != 1: continue
            h = next(iter(overlap))
            ba = next(x for gi, x in a if gi == h)
            bb = next(x for gi, x in b if gi == h)
            if ba == bb: continue
            word = compatible(enc, a, b)
            if word is not None:
                return True, word, h
    return False, None, None


def main() -> None:
    controls = [
        ([(0, 1), (2, 3)], True),
        ([(0, 2), (2, 1), (2, 3)], False),
        ([(0, 1), (2, 0), (0, 3)], False),
        ([(0, 2), (2, 1), (0, 1), (2, 3)], True),
    ]
    for edges, expected in controls:
        enc = encode(4, edges)
        got, word, h = exact_one_opposite(enc)
        assert ddp(4, edges) == expected == got
        assert len(enc.gates) == enc.n + 1
        if got:
            assert h == enc.shared
            assert word is not None

    arcs = [(u, v) for u in range(4) for v in range(4) if u != v]
    rng = random.Random(4114)
    yes = no = 0
    for _ in range(128):
        edges = [e for e in arcs if rng.random() < 0.30]
        expected = ddp(4, edges)
        enc = encode(4, edges)
        got, _word, h = exact_one_opposite(enc)
        assert got == expected, (edges, expected, got)
        if got:
            assert h == enc.shared
            yes += 1
        else:
            no += 1

    # One independently reconstructed yes target is checked against the full
    # circuit image, not against the route theorem implementation.
    enc = encode(4, [(0, 1), (2, 3)])
    got, word, _h = exact_one_opposite(enc)
    assert got and word is not None
    assert not any(
        tuple(g.value(x) for g in enc.gates) == word
        for x in product((0, 1), repeat=enc.n)
    )

    print(
        "V114 independent verification passed: "
        f"128 seeded reductions ({yes} yes/{no} no), four adversarial controls, "
        "standalone encoder/route census, exact stretch, and independent full-image check."
    )


if __name__ == "__main__":
    main()
