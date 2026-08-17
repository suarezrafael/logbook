from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from itertools import combinations, product


PAIR_POSITIONS = ((0, 1), (0, 2), (1, 2))


@dataclass(frozen=True)
class Gate:
    support: tuple[int, int, int]
    polarity: tuple[int, int, int]

    def __post_init__(self):
        if len(set(self.support)) != 3:
            raise ValueError("V107 requires essential signed-majority gates on three distinct inputs")
        if any(p not in (0, 1) for p in self.polarity):
            raise ValueError("polarity bits must be Boolean")

    def value(self, x: tuple[int, ...]) -> int:
        return int(sum(x[v] ^ p for v, p in zip(self.support, self.polarity)) >= 2)


@dataclass(frozen=True)
class Candidate:
    gate_index: int
    choice: int
    u: int
    v: int
    delta: int


@dataclass(frozen=True)
class VirtualPath:
    vertices: tuple[int, ...]
    edge_ids: tuple[int, ...]
    parity: int


class ParityDSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n
        self.xor_parent = [0] * n
        self.has_cycle = [False] * n

    def find(self, x: int) -> tuple[int, int]:
        if self.parent[x] == x:
            return x, 0
        root, up = self.find(self.parent[x])
        self.xor_parent[x] ^= up
        self.parent[x] = root
        return self.parent[x], self.xor_parent[x]

    def add_edge(self, u: int, v: int, delta: int) -> bool:
        ru, xu = self.find(u)
        rv, xv = self.find(v)
        if ru == rv:
            cycle_parity = xu ^ xv ^ delta
            if self.has_cycle[ru] or cycle_parity == 0:
                return False
            self.has_cycle[ru] = True
            return True
        if self.has_cycle[ru] and self.has_cycle[rv]:
            return False
        if self.size[ru] < self.size[rv]:
            ru, rv = rv, ru
            xu, xv = xv, xu
        self.parent[rv] = ru
        # Need xor(u->root) XOR xor(v->root) = delta after the merge.
        self.xor_parent[rv] = xu ^ xv ^ delta
        self.size[ru] += self.size[rv]
        self.has_cycle[ru] = self.has_cycle[ru] or self.has_cycle[rv]
        return True


def candidate_for(gate_index: int, gate: Gate, choice: int) -> Candidate:
    i, j = PAIR_POSITIONS[choice]
    return Candidate(
        gate_index,
        choice,
        gate.support[i],
        gate.support[j],
        1 ^ gate.polarity[i] ^ gate.polarity[j],
    )


def frame_independent(n: int, elements: list[Candidate]) -> bool:
    dsu = ParityDSU(n)
    return all(dsu.add_edge(e.u, e.v, e.delta) for e in elements)


def partition_independent(elements: list[Candidate]) -> bool:
    return len({e.gate_index for e in elements}) == len(elements)


def matroid_intersection_transversal(n: int, gates: list[Gate], gate_indices: list[int]) -> list[Candidate]:
    """Unweighted matroid intersection: partition matroid ∩ signed-frame matroid."""
    ground = [candidate_for(i, gates[i], c) for i in gate_indices for c in range(3)]
    current: set[int] = set()

    def elems(ids: set[int]) -> list[Candidate]:
        return [ground[i] for i in sorted(ids)]

    def m1(ids: set[int]) -> bool:
        return partition_independent(elems(ids))

    def m2(ids: set[int]) -> bool:
        return frame_independent(n, elems(ids))

    while len(current) < len(gate_indices):
        outside = [i for i in range(len(ground)) if i not in current]
        sources = [x for x in outside if m1(current | {x})]
        sinks = {x for x in outside if m2(current | {x})}
        queue = deque(sources)
        parent: dict[int, int | None] = {x: None for x in sources}
        endpoint = next((x for x in sources if x in sinks), None)

        while queue and endpoint is None:
            z = queue.popleft()
            if z in current:
                # M1 exchange arc: inside -> outside.
                for x in outside:
                    if x in parent:
                        continue
                    trial = (current - {z}) | {x}
                    if m1(trial):
                        parent[x] = z
                        if x in sinks:
                            endpoint = x
                            break
                        queue.append(x)
            else:
                # M2 exchange arc: outside -> inside.
                for y in sorted(current):
                    if y in parent:
                        continue
                    trial = (current - {y}) | {z}
                    if m2(trial):
                        parent[y] = z
                        queue.append(y)

        if endpoint is None:
            break

        path = []
        cur: int | None = endpoint
        while cur is not None:
            path.append(cur)
            cur = parent[cur]
        for element_id in path:
            if element_id in current:
                current.remove(element_id)
            else:
                current.add(element_id)
        assert m1(current) and m2(current)

    result = elems(current)
    if len(result) != len(gate_indices):
        raise ValueError("no full frame-independent candidate-pair transversal")
    return result


def support_of(gates: list[Gate], indices: list[int] | set[int]) -> set[int]:
    out: set[int] = set()
    for i in indices:
        out.update(gates[i].support)
    return out


def inclusion_minimal_surplus(gates: list[Gate]) -> list[int]:
    active = list(range(len(gates)))
    if len(active) <= len(support_of(gates, active)):
        raise ValueError("the output family has no positive support surplus")
    changed = True
    while changed:
        changed = False
        for i in list(active):
            trial = [j for j in active if j != i]
            if len(trial) > len(support_of(gates, trial)):
                active = trial
                changed = True
                break
    neighborhood = support_of(gates, active)
    if len(active) != len(neighborhood) + 1:
        raise AssertionError("an inclusion-minimal positive-surplus family has surplus exactly one")
    return active


def _target_for_source(gate: Gate, source: int, value: int) -> int:
    pos = gate.support.index(source)
    return 1 ^ gate.polarity[pos] ^ value


def _implication_graph(num_vars: int):
    return [[] for _ in range(2 * num_vars)]


def _add_implication(graph, u: int, u_value: int, v: int, v_value: int):
    graph[2 * u + u_value].append(2 * v + v_value)


def _add_virtual_clause(graph, path: VirtualPath, phase: int):
    u, v = path.vertices[0], path.vertices[-1]
    out = phase ^ path.parity
    _add_implication(graph, u, phase, v, out)
    _add_implication(graph, v, 1 ^ out, u, 1 ^ phase)


def _add_majority_target(graph, gate: Gate, target: int):
    good = [target ^ p for p in gate.polarity]
    bad = [1 ^ bit for bit in good]
    for i, j in PAIR_POSITIONS:
        u, v = gate.support[i], gate.support[j]
        _add_implication(graph, u, bad[i], v, good[j])
        _add_implication(graph, v, bad[j], u, good[i])


def _scc(graph):
    n = len(graph)
    reverse = [[] for _ in range(n)]
    for u, outs in enumerate(graph):
        for v in outs:
            reverse[v].append(u)
    seen = [False] * n
    order = []
    for start in range(n):
        if seen[start]:
            continue
        stack = [(start, 0)]
        seen[start] = True
        while stack:
            u, pos = stack[-1]
            if pos < len(graph[u]):
                v = graph[u][pos]
                stack[-1] = (u, pos + 1)
                if not seen[v]:
                    seen[v] = True
                    stack.append((v, 0))
            else:
                order.append(u)
                stack.pop()
    comp = [-1] * n
    cid = 0
    for start in reversed(order):
        if comp[start] != -1:
            continue
        comp[start] = cid
        stack = [start]
        while stack:
            u = stack.pop()
            for v in reverse[u]:
                if comp[v] == -1:
                    comp[v] = cid
                    stack.append(v)
        cid += 1
    return comp


def _unsat(graph, variables: set[int]) -> bool:
    comp = _scc(graph)
    return any(comp[2 * v] == comp[2 * v + 1] for v in variables)


def _components(n: int, selected: list[Candidate]):
    adjacency = [[] for _ in range(n)]
    for ei, edge in enumerate(selected):
        adjacency[edge.u].append((edge.v, ei))
        adjacency[edge.v].append((edge.u, ei))
    comp_id = [-1] * n
    components = []
    for start in range(n):
        if comp_id[start] != -1 or not adjacency[start]:
            continue
        cid = len(components)
        vertices = set([start])
        edge_ids = set()
        comp_id[start] = cid
        stack = [start]
        while stack:
            u = stack.pop()
            for v, ei in adjacency[u]:
                edge_ids.add(ei)
                if comp_id[v] == -1:
                    comp_id[v] = cid
                    vertices.add(v)
                    stack.append(v)
        components.append((vertices, edge_ids))
    return adjacency, comp_id, components


def _cycle_core(vertices: set[int], edge_ids: set[int], selected: list[Candidate]):
    incident = {v: set() for v in vertices}
    for ei in edge_ids:
        e = selected[ei]
        incident[e.u].add(ei)
        incident[e.v].add(ei)
    active_v = set(vertices)
    active_e = set(edge_ids)
    queue = deque(v for v in active_v if len(incident[v]) < 2)
    while queue:
        v = queue.popleft()
        if v not in active_v:
            continue
        live = incident[v] & active_e
        if len(live) >= 2:
            continue
        active_v.remove(v)
        for ei in list(live):
            active_e.remove(ei)
            e = selected[ei]
            w = e.v if e.u == v else e.u
            if w in active_v and len(incident[w] & active_e) < 2:
                queue.append(w)
    if not active_e:
        raise AssertionError("frame-basis component has no cycle")
    parity = 0
    for ei in active_e:
        parity ^= selected[ei].delta
    if parity != 1:
        raise AssertionError("frame-basis component cycle must be unbalanced")
    return active_v, active_e


def _ordered_cycle(core_v: set[int], core_e: set[int], selected: list[Candidate]) -> VirtualPath:
    incident = {v: [] for v in core_v}
    for ei in core_e:
        e = selected[ei]
        incident[e.u].append(ei)
        incident[e.v].append(ei)
    start = min(core_v)
    first = incident[start][0]
    vertices = [start]
    edge_ids = []
    current, edge_id = start, first
    used = set()
    while True:
        if edge_id in used:
            raise AssertionError("cycle traversal repeated an edge")
        used.add(edge_id)
        edge_ids.append(edge_id)
        edge = selected[edge_id]
        nxt = edge.v if edge.u == current else edge.u
        vertices.append(nxt)
        if nxt == start:
            break
        candidates = [ei for ei in incident[nxt] if ei != edge_id]
        if len(candidates) != 1:
            raise AssertionError("cycle core is not degree two")
        current, edge_id = nxt, candidates[0]
    if used != core_e:
        raise AssertionError("cycle traversal did not use the full core")
    parity = 0
    for ei in edge_ids:
        parity ^= selected[ei].delta
    return VirtualPath(tuple(vertices), tuple(edge_ids), parity)


def _tree_path(adjacency, selected, start: int, targets: set[int], blocked_edges: set[int]):
    queue = deque([start])
    parent: dict[int, tuple[int, int] | None] = {start: None}
    endpoint = start if start in targets else None
    while queue and endpoint is None:
        u = queue.popleft()
        for v, ei in adjacency[u]:
            if ei in blocked_edges or v in parent:
                continue
            parent[v] = (u, ei)
            if v in targets:
                endpoint = v
                break
            queue.append(v)
    if endpoint is None:
        raise AssertionError("terminal is not connected to its cycle")
    vertices = [endpoint]
    edge_ids = []
    cur = endpoint
    while parent[cur] is not None:
        prev, ei = parent[cur]
        vertices.append(prev)
        edge_ids.append(ei)
        cur = prev
    vertices.reverse()
    edge_ids.reverse()
    # start -> cycle endpoint
    return tuple(vertices), tuple(edge_ids)


def _minimal_unicyclic_subgraph(n, selected, component, terminals):
    vertices, edge_ids = component
    adjacency, _, _ = _components(n, selected)
    core_v, core_e = _cycle_core(vertices, edge_ids, selected)
    relevant = set(core_e)
    for terminal in terminals:
        path_v, path_e = _tree_path(adjacency, selected, terminal, core_v, core_e)
        relevant.update(path_e)
    rel_vertices = set()
    degree = {}
    for ei in relevant:
        e = selected[ei]
        rel_vertices.update((e.u, e.v))
        degree[e.u] = degree.get(e.u, 0) + 1
        degree[e.v] = degree.get(e.v, 0) + 1
    important = set(terminals) | {v for v in rel_vertices if degree.get(v, 0) != 2}
    if not important:
        raise AssertionError("three terminals guarantee an important vertex")

    incident = {v: [] for v in rel_vertices}
    for ei in relevant:
        e = selected[ei]
        incident[e.u].append(ei)
        incident[e.v].append(ei)

    used = set()
    paths = []
    for start in sorted(important):
        for first in incident[start]:
            if first in used:
                continue
            walk_vertices = [start]
            walk_edges = []
            current, ei = start, first
            parity = 0
            while True:
                if ei in used:
                    raise AssertionError("virtual-path decomposition repeated an edge")
                used.add(ei)
                walk_edges.append(ei)
                parity ^= selected[ei].delta
                edge = selected[ei]
                nxt = edge.v if edge.u == current else edge.u
                walk_vertices.append(nxt)
                if nxt in important:
                    break
                candidates = [x for x in incident[nxt] if x != ei]
                if len(candidates) != 1:
                    raise AssertionError("suppressed vertex is not degree two")
                current, ei = nxt, candidates[0]
            paths.append(VirtualPath(tuple(walk_vertices), tuple(walk_edges), parity))
    if used != relevant:
        raise AssertionError("virtual-path decomposition omitted relevant edges")
    if len(paths) > 6:
        raise AssertionError("three-terminal reduced unicyclic kernel must have at most six paths")
    return paths, important


def _lift_virtual_phase(targets, gates, selected, path: VirtualPath, phase: int):
    value = phase
    for j, edge_id in enumerate(path.edge_ids):
        edge = selected[edge_id]
        source = path.vertices[j]
        target = _target_for_source(gates[edge.gate_index], source, value)
        old = targets[edge.gate_index]
        if old is not None and old != target:
            raise AssertionError("edge-disjoint virtual paths must not assign conflicting gate targets")
        targets[edge.gate_index] = target
        value ^= edge.delta


def _kernel_target(n, gates, missing: int, selected: list[Candidate], component, terminals):
    paths, important = _minimal_unicyclic_subgraph(n, selected, component, terminals)
    variables = set(important) | set(terminals)
    for phases in product((0, 1), repeat=len(paths)):
        for missing_target in (0, 1):
            graph = _implication_graph(n)
            for path, phase in zip(paths, phases):
                _add_virtual_clause(graph, path, phase)
            _add_majority_target(graph, gates[missing], missing_target)
            if not _unsat(graph, variables):
                continue
            targets: list[int | None] = [None] * len(gates)
            for path, phase in zip(paths, phases):
                _lift_virtual_phase(targets, gates, selected, path, phase)
            targets[missing] = missing_target
            return targets, {
                "case": "unicyclic_three_terminal_kernel",
                "virtual_paths": len(paths),
                "kernel_vertices": len(important),
                "phases": phases,
                "missing_target": missing_target,
            }
    raise AssertionError("V107 reduced-kernel theorem falsified by this component")


def _cycle_and_attachment_walk(component, terminal, n, selected):
    adjacency, _, _ = _components(n, selected)
    vertices, edge_ids = component
    core_v, core_e = _cycle_core(vertices, edge_ids, selected)
    cycle = _ordered_cycle(core_v, core_e, selected)
    term_to_cycle_v, term_to_cycle_e = _tree_path(adjacency, selected, terminal, core_v, core_e)
    # tree path was terminal -> cycle; connector wants cycle -> terminal
    cycle_vertex = term_to_cycle_v[-1]
    outward = VirtualPath(
        tuple(reversed(term_to_cycle_v)),
        tuple(reversed(term_to_cycle_e)),
        0,
    )
    parity = 0
    for ei in outward.edge_ids:
        parity ^= selected[ei].delta
    outward = VirtualPath(outward.vertices, outward.edge_ids, parity)
    return cycle, cycle_vertex, outward


def _cross_component_target(n, gates, missing, selected, components, comp_id, terminals):
    pair = None
    for choice, (i, j) in enumerate(PAIR_POSITIONS):
        u, v = terminals[i], terminals[j]
        if comp_id[u] != comp_id[v]:
            pair = (choice, u, v)
            break
    if pair is None:
        raise AssertionError("cross-component case has no cross-component terminal pair")
    choice, u, v = pair
    cu, cv = comp_id[u], comp_id[v]
    left_cycle, left_root, left_out = _cycle_and_attachment_walk(components[cu], u, n, selected)
    right_cycle, right_root, right_out = _cycle_and_attachment_walk(components[cv], v, n, selected)
    connector_edge = candidate_for(missing, gates[missing], choice)

    targets: list[int | None] = [None] * len(gates)

    def apply_existing(path: VirtualPath, start_value: int) -> int:
        value = start_value
        for j, ei in enumerate(path.edge_ids):
            edge = selected[ei]
            source = path.vertices[j]
            targets[edge.gate_index] = _target_for_source(gates[edge.gate_index], source, value)
            value ^= edge.delta
        return value

    # Rotate each cycle so it starts at the attachment root.
    def rotate_cycle(cycle: VirtualPath, root: int) -> VirtualPath:
        verts = list(cycle.vertices[:-1])
        idx = verts.index(root)
        edges = list(cycle.edge_ids)
        new_edges = edges[idx:] + edges[:idx]
        new_verts = verts[idx:] + verts[:idx] + [root]
        return VirtualPath(tuple(new_verts), tuple(new_edges), cycle.parity)

    left_cycle = rotate_cycle(left_cycle, left_root)
    right_cycle = rotate_cycle(right_cycle, right_root)
    if apply_existing(left_cycle, 0) != 1:
        raise AssertionError("left basis cycle is not odd")
    value = 1
    value = apply_existing(left_out, value)
    targets[missing] = _target_for_source(gates[missing], u, value)
    value ^= connector_edge.delta
    # right_out is root -> terminal, so traverse it backwards from terminal -> root.
    inward = VirtualPath(tuple(reversed(right_out.vertices)), tuple(reversed(right_out.edge_ids)), right_out.parity)
    value = apply_existing(inward, value)
    right_cycle = rotate_cycle(right_cycle, right_root)
    if apply_existing(right_cycle, value) != (value ^ 1):
        raise AssertionError("right basis cycle is not odd")
    return targets, {
        "case": "cross_component_handcuff",
        "missing_pair_choice": choice,
        "left_component": cu,
        "right_component": cv,
    }


def avoid_essential_signed_majority(n: int, gates: list[Gate]):
    """Construct a missing output for the V107 essential signed-majority class.

    The only nontrivial global primitive is ordinary unweighted matroid
    intersection on a partition matroid and a signed-frame matroid, both with
    explicit polynomial-time independence tests.
    """
    if len(gates) <= n:
        raise ValueError("range avoidance requires more outputs than inputs")

    block_global = inclusion_minimal_surplus(gates)
    variables = sorted(support_of(gates, block_global))
    remap = {v: i for i, v in enumerate(variables)}
    local_gates = [
        Gate(tuple(remap[v] for v in gates[i].support), gates[i].polarity)
        for i in block_global
    ]
    local_n = len(variables)
    if len(local_gates) != local_n + 1:
        raise AssertionError("minimal surplus block must have exact stretch one")

    missing = len(local_gates) - 1
    remaining = list(range(missing))
    selected = matroid_intersection_transversal(local_n, local_gates, remaining)
    if len(selected) != local_n or not frame_independent(local_n, selected):
        raise AssertionError("failed to construct the Rado frame basis")

    adjacency, comp_id, components = _components(local_n, selected)
    if any(cid < 0 for cid in comp_id):
        raise AssertionError("rank-n frame basis must touch every local input")
    for component in components:
        vset, eset = component
        if len(eset) != len(vset):
            raise AssertionError("every rank-tight frame-basis component must be unicyclic")
        _cycle_core(vset, eset, selected)

    terminals = local_gates[missing].support
    terminal_components = {comp_id[v] for v in terminals}
    if len(terminal_components) > 1:
        local_targets, meta = _cross_component_target(
            local_n, local_gates, missing, selected, components, comp_id, terminals
        )
    else:
        component = components[next(iter(terminal_components))]
        local_targets, meta = _kernel_target(
            local_n, local_gates, missing, selected, component, terminals
        )

    local_word = [0 if bit is None else bit for bit in local_targets]
    global_word = [0] * len(gates)
    for local_index, global_index in enumerate(block_global):
        global_word[global_index] = local_word[local_index]
    meta.update({
        "minimal_surplus_outputs": len(block_global),
        "minimal_surplus_inputs": local_n,
        "frame_basis_components": len(components),
    })
    return tuple(global_word), meta


def in_range(n: int, gates: list[Gate], y: tuple[int, ...]) -> bool:
    return any(
        tuple(g.value(x) for g in gates) == y
        for x in product((0, 1), repeat=n)
    )
