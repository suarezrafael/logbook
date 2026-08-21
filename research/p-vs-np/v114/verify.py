from __future__ import annotations

import random

import mux_waypoint_barrier as barrier

TERMINALS = (0, 1, 2, 3)


def simple_paths(n: int, edges: list[tuple[int, int]], source: int, sink: int):
    adjacency = [[] for _ in range(n)]
    for u, v in sorted(set(edges)):
        if u != v:
            adjacency[u].append(v)
    out = []

    def dfs(u: int, seen: set[int], path: list[int]) -> None:
        if u == sink:
            out.append(tuple(path))
            return
        for v in adjacency[u]:
            if v in seen:
                continue
            seen.add(v)
            path.append(v)
            dfs(v, seen, path)
            path.pop()
            seen.remove(v)

    dfs(source, {source}, [source])
    return out


def ddp_witness(n: int, edges: list[tuple[int, int]]):
    s1, t1, s2, t2 = TERMINALS
    for p1 in simple_paths(n, edges, s1, t1):
        s_p1 = set(p1)
        for p2 in simple_paths(n, edges, s2, t2):
            if not (s_p1 & set(p2)):
                return p1, p2
    return None


def enumerate_returns(instance: barrier.BarrierInstance, start: int, cap: int = 20000):
    by_selector: dict[int, list[int]] = {}
    for gi, gate in enumerate(instance.gates):
        if gate.selector == instance.root:
            continue
        by_selector.setdefault(gate.selector, []).append(gi)
    found = []

    def dfs(current: int, used: set[int], path: list[tuple[int, int]]) -> None:
        if len(found) >= cap:
            raise AssertionError("small-instance route census exceeded cap")
        if current == instance.root:
            found.append(tuple(path))
            return
        for gi in by_selector.get(current, ()):
            if gi in used:
                continue
            used.add(gi)
            for branch in (0, 1):
                path.append((gi, branch))
                dfs(instance.gates[gi].branch(branch)[1], used, path)
                path.pop()
            used.remove(gi)

    dfs(start, set(), [])
    return found


def exact_one_opposite_pair_exists(instance: barrier.BarrierInstance) -> bool:
    p0 = enumerate_returns(instance, instance.route0_start)
    p1 = enumerate_returns(instance, instance.route1_start)
    for r0 in p0:
        used0 = {gi for gi, _ in r0}
        for r1 in p1:
            overlap = used0 & {gi for gi, _ in r1}
            if len(overlap) != 1:
                continue
            h = next(iter(overlap))
            b0 = next(b for gi, b in r0 if gi == h)
            b1 = next(b for gi, b in r1 if gi == h)
            if b0 == b1:
                continue
            target = barrier._target_word(
                instance.gates,
                ((instance.first_gate0, 0),) + r0,
                ((instance.first_gate1, 0),) + r1,
            )
            if target is not None:
                return True
    return False


def check_structure(instance: barrier.BarrierInstance) -> None:
    assert len(instance.gates) == instance.n + 1
    for gate in instance.gates:
        assert len({gate.selector, gate.data0, gate.data1}) == 3
        assert 0 <= gate.selector < instance.n
        assert 0 <= gate.data0 < instance.n
        assert 0 <= gate.data1 < instance.n
    bypass = barrier.bypass_optimum_certificate(instance)
    assert not bypass.overlap
    assert barrier._check_return_path(instance, instance.route0_start, bypass.return_path0)
    assert barrier._check_return_path(instance, instance.route1_start, bypass.return_path1)
    alpha0 = instance.gates[instance.first_gate0].branch(0)[2]
    alpha1 = instance.gates[instance.first_gate1].branch(0)[2]
    assert alpha0 != alpha1


def main() -> None:
    yes_edges = [(0, 1), (2, 3)]
    yes = barrier.build_exact_stretch_barrier_instance(4, yes_edges, TERMINALS)
    check_structure(yes)
    witness = ddp_witness(4, yes_edges)
    assert witness is not None
    cert = barrier.certificate_from_ddp_paths(yes, witness[0], witness[1], TERMINALS)
    assert barrier.validate_certificate(yes, cert)
    assert cert.overlap == (yes.shared_gate,)
    assert not barrier.in_range(yes, cert.target)

    no_edges = [(0, 2), (2, 1), (2, 3)]
    no = barrier.build_exact_stretch_barrier_instance(4, no_edges, TERMINALS)
    check_structure(no)
    assert ddp_witness(4, no_edges) is None
    assert not exact_one_opposite_pair_exists(no)

    arcs = [(u, v) for u in range(4) for v in range(4) if u != v]
    rng = random.Random(114114)
    checked = 0
    yes_count = 0
    no_count = 0
    for _ in range(96):
        edges = [edge for edge in arcs if rng.random() < 0.32]
        witness = ddp_witness(4, edges)
        instance = barrier.build_exact_stretch_barrier_instance(4, edges, TERMINALS)
        check_structure(instance)
        got = exact_one_opposite_pair_exists(instance)
        assert got == (witness is not None), (edges, witness, got)
        if witness is not None:
            cert = barrier.certificate_from_ddp_paths(instance, witness[0], witness[1], TERMINALS)
            assert barrier.validate_certificate(instance, cert)
            yes_count += 1
        else:
            no_count += 1
        checked += 1

    # Stretch padding is audited on sparse and dense five-vertex controls.
    five_arcs = [(u, v) for u in range(5) for v in range(5) if u != v]
    for step in (1, 3, 5, 7):
        edges = [edge for i, edge in enumerate(five_arcs) if i % step == 0]
        instance = barrier.build_exact_stretch_barrier_instance(5, edges, TERMINALS)
        check_structure(instance)

    print(
        "V114 primary verification passed: "
        f"{checked} seeded four-vertex reductions ({yes_count} yes/{no_count} no), "
        "exact m=n+1 padding, explicit zero-overlap bypass, and one full-range missing target."
    )


if __name__ == "__main__":
    main()
