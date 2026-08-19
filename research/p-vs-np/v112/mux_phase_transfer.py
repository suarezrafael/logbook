from __future__ import annotations

import sys
from dataclasses import dataclass
from itertools import product
from pathlib import Path

V109_DIR = Path(__file__).resolve().parents[1] / "v109"
V111_DIR = Path(__file__).resolve().parents[1] / "v111"
sys.path.insert(0, str(V109_DIR))
sys.path.insert(0, str(V111_DIR))
from mux_gate_flow import MuxGate  # noqa: E402
from mux_min_overlap import strict_nested_chain_family  # noqa: E402


@dataclass(frozen=True)
class SerialLayer:
    left: tuple[int, int]
    right: tuple[int, int]
    exit_var: int


@dataclass(frozen=True)
class SerialChain:
    root: int
    central_gates: tuple[int, int]
    layers: tuple[SerialLayer, ...]
    shared_gates: tuple[int, ...]


@dataclass(frozen=True)
class PhaseTransferCertificate:
    chain: SerialChain
    cycle0: tuple[tuple[int, int], ...]
    cycle1: tuple[tuple[int, int], ...]
    target: tuple[int, ...]

    @property
    def shared_gates(self) -> tuple[int, ...]:
        return tuple(sorted({gi for gi, _ in self.cycle0} & {gi for gi, _ in self.cycle1}))


def _data_set(gate: MuxGate) -> set[int]:
    return {gate.data0, gate.data1}


def _selector_map(n: int, gates: list[MuxGate]) -> list[list[int]]:
    by_selector = [[] for _ in range(n)]
    for gi, gate in enumerate(gates):
        if not (0 <= gate.selector < n):
            raise ValueError("selector outside input range")
        by_selector[gate.selector].append(gi)
    return by_selector


def _first_layer(
    root: int,
    central: tuple[int, int],
    by_selector: list[list[int]],
    gates: list[MuxGate],
) -> SerialLayer | None:
    vars4 = {
        gates[central[0]].data0,
        gates[central[0]].data1,
        gates[central[1]].data0,
        gates[central[1]].data1,
    }
    if len(vars4) != 4 or root in vars4:
        return None
    if any(len(by_selector[x]) != 1 for x in vars4):
        return None
    data_sets = [_data_set(gates[by_selector[x][0]]) for x in vars4]
    common = set.intersection(*data_sets)
    if len(common) != 1:
        return None
    exit_var = next(iter(common))
    if exit_var in vars4:
        return None

    partner: dict[int, int] = {}
    for x in vars4:
        rest = _data_set(gates[by_selector[x][0]]) - {exit_var}
        if len(rest) != 1:
            return None
        y = next(iter(rest))
        if y not in vars4 or y == x:
            return None
        partner[x] = y
    if any(partner.get(partner[x]) != x for x in vars4):
        return None

    pairs = sorted({tuple(sorted((x, partner[x]))) for x in vars4})
    if len(pairs) != 2 or set(pairs[0]) & set(pairs[1]):
        return None
    return SerialLayer(pairs[0], pairs[1], exit_var)


def _next_layer(
    hub: int,
    shared_gate: int,
    by_selector: list[list[int]],
    gates: list[MuxGate],
) -> SerialLayer | None:
    gate = gates[shared_gate]
    if gate.selector != hub:
        return None
    p, q = gate.data0, gate.data1
    if p == q or p == hub or q == hub:
        return None
    if len(by_selector[p]) != 1 or len(by_selector[q]) != 1:
        return None
    dp = _data_set(gates[by_selector[p][0]])
    dq = _data_set(gates[by_selector[q][0]])
    common = dp & dq
    if len(common) != 1:
        return None
    exit_var = next(iter(common))
    pp_set = dp - {exit_var}
    qq_set = dq - {exit_var}
    if len(pp_set) != 1 or len(qq_set) != 1:
        return None
    pp = next(iter(pp_set))
    qq = next(iter(qq_set))
    if len({p, pp, q, qq}) != 4:
        return None
    if len(by_selector[pp]) != 1 or len(by_selector[qq]) != 1:
        return None
    if _data_set(gates[by_selector[pp][0]]) != {p, exit_var}:
        return None
    if _data_set(gates[by_selector[qq][0]]) != {q, exit_var}:
        return None
    return SerialLayer((p, pp), (q, qq), exit_var)


def recognize_serial_chain(n: int, gates: list[MuxGate]) -> SerialChain | None:
    """Recognize the exact k=2 serial two-lobe support template in O(N)."""
    if n <= 0 or len(gates) != n + 1:
        return None
    try:
        by_selector = _selector_map(n, gates)
    except ValueError:
        return None
    roots = [v for v, ids in enumerate(by_selector) if len(ids) == 2]
    if len(roots) != 1:
        return None
    root = roots[0]
    if any(len(ids) != 1 for v, ids in enumerate(by_selector) if v != root):
        return None
    central = tuple(sorted(by_selector[root]))
    first = _first_layer(root, central, by_selector, gates)
    if first is None:
        return None

    layers = [first]
    shared: list[int] = []
    used_vars = {root, *first.left, *first.right}
    used_gates = {central[0], central[1]}
    used_gates.update(by_selector[x][0] for x in first.left + first.right)
    exit_var = first.exit_var

    while exit_var != root:
        if exit_var in used_vars:
            return None
        used_vars.add(exit_var)
        if not (0 <= exit_var < n) or len(by_selector[exit_var]) != 1:
            return None
        h = by_selector[exit_var][0]
        if h in used_gates:
            return None
        nxt = _next_layer(exit_var, h, by_selector, gates)
        if nxt is None:
            return None
        layer_vars = set(nxt.left + nxt.right)
        if layer_vars & used_vars:
            return None
        used_vars.update(layer_vars)
        shared.append(h)
        used_gates.add(h)
        for x in nxt.left + nxt.right:
            used_gates.add(by_selector[x][0])
        layers.append(nxt)
        exit_var = nxt.exit_var

    if used_vars != set(range(n)):
        return None
    if used_gates != set(range(len(gates))):
        return None
    if len(shared) + 1 != len(layers):
        return None
    return SerialChain(root, central, tuple(layers), tuple(shared))


def _lobe_index(layer: SerialLayer, var: int) -> int | None:
    if var in layer.left:
        return 0
    if var in layer.right:
        return 1
    return None


def _lobe_paths(
    gates: list[MuxGate],
    by_selector: list[list[int]],
    pair: tuple[int, int],
    start: int,
    exit_var: int,
) -> tuple[tuple[tuple[int, int], ...], ...]:
    allowed = set(pair)
    if start not in allowed:
        return ()
    out: list[tuple[tuple[int, int], ...]] = []
    stack = [(start, tuple(), frozenset())]
    while stack:
        cur, path, used = stack.pop()
        if cur == exit_var:
            out.append(path)
            continue
        if cur not in allowed or len(by_selector[cur]) != 1:
            continue
        gi = by_selector[cur][0]
        if gi in used:
            continue
        gate = gates[gi]
        # Reverse push order so branch 0 is considered first after sorting.
        for branch in (1, 0):
            _s, dest, _alpha, _pd = gate.branch(branch)
            if dest == exit_var or dest in allowed:
                stack.append((dest, path + ((gi, branch),), used | {gi}))
    return tuple(sorted(set(out)))


def _required_target_at_position(
    gates: list[MuxGate],
    cycle: tuple[tuple[int, int], ...],
    pos: int,
) -> int:
    first_alpha = gates[cycle[0][0]].branch(cycle[0][1])[2]
    gi, branch = cycle[pos]
    if pos + 1 < len(cycle):
        next_gi, next_branch = cycle[pos + 1]
        desired = gates[next_gi].branch(next_branch)[2]
    else:
        desired = 1 ^ first_alpha
    return gates[gi].target_for_arrival(branch, desired)


def _target_word(
    gates: list[MuxGate],
    cycle0: tuple[tuple[int, int], ...],
    cycle1: tuple[tuple[int, int], ...],
) -> tuple[int, ...] | None:
    targets = [0] * len(gates)
    assigned: dict[int, int] = {}
    for cycle in (cycle0, cycle1):
        for pos, (gi, _branch) in enumerate(cycle):
            target = _required_target_at_position(gates, cycle, pos)
            if gi in assigned and assigned[gi] != target:
                return None
            assigned[gi] = target
            targets[gi] = target
    return tuple(targets)


def find_phase_transfer_certificate(
    n: int,
    gates: list[MuxGate],
) -> PhaseTransferCertificate | None:
    chain = recognize_serial_chain(n, gates)
    if chain is None:
        return None
    by_selector = _selector_map(n, gates)
    c0, c1 = chain.central_gates
    first = chain.layers[0]

    for b0, b1 in product((0, 1), repeat=2):
        _s0, d0, a0, _p0 = gates[c0].branch(b0)
        _s1, d1, a1, _p1 = gates[c1].branch(b1)
        if a0 == a1:
            continue
        li0 = _lobe_index(first, d0)
        li1 = _lobe_index(first, d1)
        if li0 is None or li1 is None or li0 == li1:
            continue
        pair0 = first.left if li0 == 0 else first.right
        pair1 = first.left if li1 == 0 else first.right
        paths0 = _lobe_paths(gates, by_selector, pair0, d0, first.exit_var)
        paths1 = _lobe_paths(gates, by_selector, pair1, d1, first.exit_var)
        for p0 in paths0:
            for p1 in paths1:
                cycle0 = [(c0, b0), *p0]
                cycle1 = [(c1, b1), *p1]
                failed = False

                for j, h in enumerate(chain.shared_gates):
                    layer = chain.layers[j + 1]
                    chosen = None
                    for hb0, hb1 in product((0, 1), repeat=2):
                        _hs0, hd0, _ha0, _hp0 = gates[h].branch(hb0)
                        _hs1, hd1, _ha1, _hp1 = gates[h].branch(hb1)
                        lj0 = _lobe_index(layer, hd0)
                        lj1 = _lobe_index(layer, hd1)
                        if lj0 is None or lj1 is None or lj0 == lj1:
                            continue
                        lpair0 = layer.left if lj0 == 0 else layer.right
                        lpair1 = layer.left if lj1 == 0 else layer.right
                        q0s = _lobe_paths(gates, by_selector, lpair0, hd0, layer.exit_var)
                        q1s = _lobe_paths(gates, by_selector, lpair1, hd1, layer.exit_var)
                        for q0 in q0s:
                            for q1 in q1s:
                                if not q0 or not q1:
                                    continue
                                next_a0 = gates[q0[0][0]].branch(q0[0][1])[2]
                                next_a1 = gates[q1[0][0]].branch(q1[0][1])[2]
                                t0 = gates[h].target_for_arrival(hb0, next_a0)
                                t1 = gates[h].target_for_arrival(hb1, next_a1)
                                if t0 == t1:
                                    chosen = (hb0, hb1, q0, q1)
                                    break
                            if chosen is not None:
                                break
                        if chosen is not None:
                            break
                    if chosen is None:
                        failed = True
                        break
                    hb0, hb1, q0, q1 = chosen
                    cycle0.append((h, hb0))
                    cycle0.extend(q0)
                    cycle1.append((h, hb1))
                    cycle1.extend(q1)

                if failed:
                    continue
                c0t = tuple(cycle0)
                c1t = tuple(cycle1)
                target = _target_word(gates, c0t, c1t)
                if target is None:
                    continue
                return PhaseTransferCertificate(chain, c0t, c1t, target)
    return None


def avoid_mux_phase_transfer(
    n: int,
    gates: list[MuxGate],
) -> tuple[tuple[int, ...], dict[str, object]]:
    cert = find_phase_transfer_certificate(n, gates)
    if cert is None:
        raise ValueError("no V112 serial phase-transfer certificate")
    return cert.target, {
        "case": "mux_serial_two_lobe_phase_transfer",
        "layers": len(cert.chain.layers),
        "shared_hubs": len(cert.chain.shared_gates),
        "shared_gates_used": len(cert.shared_gates),
        "cycle0_outputs": len(cert.cycle0),
        "cycle1_outputs": len(cert.cycle1),
    }


CENTRAL_PATTERN = (
    ((0, 1, 1), 0),
    ((0, 1, 1), 1),
)
FIRST_LOBE_PATTERN = (
    ((0, 0, 1), 1),
    ((0, 0, 1), 0),
    ((1, 0, 1), 1),
    ((1, 1, 1), 1),
)
REPEATED_BLOCK_PATTERN = (
    ((0, 1, 1), 0),
    ((1, 0, 1), 1),
    ((0, 0, 0), 0),
    ((0, 1, 1), 0),
    ((1, 1, 1), 1),
)


def strict_phase_transfer_family(depth: int) -> tuple[int, list[MuxGate], tuple[int, ...]]:
    """Periodic signing with compatible and incompatible optimum overlap flows."""
    n, base, shared = strict_nested_chain_family(2, depth)
    gates: list[MuxGate] = []
    for i, gate in enumerate(base):
        if i < 2:
            polarity, out_flip = CENTRAL_PATTERN[i]
        elif i < 6:
            polarity, out_flip = FIRST_LOBE_PATTERN[i - 2]
        else:
            polarity, out_flip = REPEATED_BLOCK_PATTERN[(i - 6) % 5]
        gates.append(
            MuxGate(
                gate.selector,
                gate.data0,
                gate.data1,
                polarity,
                out_flip,
            )
        )
    return n, gates, shared


def in_range(n: int, gates: list[MuxGate], y: tuple[int, ...]) -> bool:
    return any(
        tuple(g.value(x) for g in gates) == y
        for x in product((0, 1), repeat=n)
    )
