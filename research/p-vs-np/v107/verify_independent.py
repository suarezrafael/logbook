from __future__ import annotations

import heapq
import json
from itertools import combinations, permutations, product


PAIR_POSITIONS = ((0, 1), (0, 2), (1, 2))


def prufer_tree_edges(n, seq):
    if n == 1:
        return []
    degree = [1] * n
    for x in seq:
        degree[x] += 1
    leaves = [i for i, d in enumerate(degree) if d == 1]
    heapq.heapify(leaves)
    edges = []
    for x in seq:
        leaf = heapq.heappop(leaves)
        edges.append((leaf, x))
        degree[leaf] -= 1
        degree[x] -= 1
        if degree[x] == 1:
            heapq.heappush(leaves, x)
    a = heapq.heappop(leaves)
    b = heapq.heappop(leaves)
    edges.append((a, b))
    return edges


def rooted_tree_shapes(offcycle_terminals):
    k = offcycle_terminals
    if k == 0:
        return [()]
    shapes = set()
    for steiners in range(k):
        n = 1 + k + steiners
        sequences = [()] if n == 2 else product(range(n), repeat=n - 2)
        for seq in sequences:
            edges = prufer_tree_edges(n, seq)
            degree = [0] * n
            for u, v in edges:
                degree[u] += 1
                degree[v] += 1
            if any(degree[v] < 3 for v in range(1 + k, n)):
                continue
            branch = list(range(1 + k, n))
            reps = []
            for perm in permutations(branch):
                mapping = {i: i for i in range(1 + k)}
                for old, new in zip(branch, perm):
                    mapping[old] = new
                reps.append(tuple(sorted(
                    (min(mapping[u], mapping[v]), max(mapping[u], mapping[v]))
                    for u, v in edges
                )))
            shapes.add(min(reps) if reps else tuple(sorted(edges)))
    return sorted(shapes)


def surjective_assignments(roots):
    return [a for a in product(range(roots), repeat=3) if set(a) == set(range(roots))]


def generate_reduced_kernels():
    kernels = []
    for root_count in (1, 2, 3):
        for assignment in surjective_assignments(root_count):
            blocks = {
                root: [terminal for terminal in range(3) if assignment[terminal] == root]
                for root in range(root_count)
            }
            oncycle_options = [[None] + blocks[root] for root in range(root_count)]
            for oncycle in product(*oncycle_options):
                shape_options = []
                offcycle_lists = []
                for root in range(root_count):
                    offcycle = [t for t in blocks[root] if t != oncycle[root]]
                    offcycle_lists.append(offcycle)
                    shape_options.append(rooted_tree_shapes(len(offcycle)))
                for shapes in product(*shape_options):
                    next_vertex = root_count
                    terminal_vertex = [None] * 3
                    for root in range(root_count):
                        if oncycle[root] is not None:
                            terminal_vertex[oncycle[root]] = root
                    attachment_edges = []
                    for root, shape in enumerate(shapes):
                        offcycle = offcycle_lists[root]
                        local = {0: root}
                        for local_id, terminal in enumerate(offcycle, start=1):
                            local[local_id] = next_vertex
                            terminal_vertex[terminal] = next_vertex
                            next_vertex += 1
                        nodes = {v for edge in shape for v in edge}
                        for node in sorted(nodes):
                            if node not in local:
                                local[node] = next_vertex
                                next_vertex += 1
                        for u, v in shape:
                            attachment_edges.append((local[u], local[v]))
                    assert all(v is not None for v in terminal_vertex)
                    if root_count == 1:
                        cycle_edges = [(0, 0)]
                    elif root_count == 2:
                        cycle_edges = [(0, 1), (0, 1)]
                    else:
                        cycle_edges = [(0, 1), (1, 2), (2, 0)]
                    edges = tuple(cycle_edges + attachment_edges)
                    assert len(edges) <= 6
                    assert next_vertex <= 6
                    kernels.append((
                        root_count,
                        next_vertex,
                        tuple(terminal_vertex),
                        edges,
                        len(cycle_edges),
                    ))
    assert len(kernels) == 164
    return kernels


def _add_implication(graph, var_from, value_from, var_to, value_to):
    graph[2 * var_from + value_from].append(2 * var_to + value_to)


def add_virtual_clause(graph, u, v, delta, phase):
    # The path phase chooses the forbidden endpoint pair
    #   x_u = phase, x_v = 1 XOR phase XOR delta.
    # The corresponding 2-CNF clause supplies the two contraposed implications.
    bad_u = phase
    bad_v = 1 ^ phase ^ delta
    _add_implication(graph, u, bad_u, v, 1 ^ bad_v)
    _add_implication(graph, v, bad_v, u, 1 ^ bad_u)


def add_majority_target(graph, terminals, polarity, target):
    good = [target ^ polarity[i] for i in range(3)]
    bad = [1 ^ bit for bit in good]
    for i, j in PAIR_POSITIONS:
        u, v = terminals[i], terminals[j]
        _add_implication(graph, u, bad[i], v, good[j])
        _add_implication(graph, v, bad[j], u, good[i])


def scc(graph):
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
        seen[start] = True
        stack = [(start, 0)]
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


def unsat_2sat(n, terminals, edges, deltas, phases, polarity, target):
    graph = [[] for _ in range(2 * n)]
    for (u, v), delta, phase in zip(edges, deltas, phases):
        add_virtual_clause(graph, u, v, delta, phase)
    add_majority_target(graph, terminals, polarity, target)
    comp = scc(graph)
    return any(comp[2 * v] == comp[2 * v + 1] for v in range(n))


def has_unsat_phase(n, terminals, edges, deltas, polarity):
    for phases in product((0, 1), repeat=len(edges)):
        for target in (0, 1):
            if unsat_2sat(n, terminals, edges, deltas, phases, polarity, target):
                return True
    return False


def kernel_census():
    cases = 0
    max_vertices = 0
    max_paths = 0
    for root_count, n, terminals, edges, cycle_count in generate_reduced_kernels():
        max_vertices = max(max_vertices, n)
        max_paths = max(max_paths, len(edges))
        for deltas in product((0, 1), repeat=len(edges)):
            cycle = deltas[:cycle_count]
            if root_count == 1:
                if cycle != (1,):
                    continue
            else:
                parity = 0
                for bit in cycle:
                    parity ^= bit
                if parity != 1:
                    continue
            for polarity in product((0, 1), repeat=3):
                cases += 1
                assert has_unsat_phase(n, terminals, edges, deltas, polarity), (
                    root_count, n, terminals, edges, deltas, polarity
                )
    assert cases == 16032
    return {
        "reduced_kernels": 164,
        "signed_polarity_cases": cases,
        "max_kernel_vertices": max_vertices,
        "max_virtual_paths": max_paths,
        "decision_engine": "independent_2sat_scc",
    }


def connected(n, edges):
    adjacency = [[] for _ in range(n)]
    for u, v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    seen = {0}
    stack = [0]
    while stack:
        u = stack.pop()
        for v in adjacency[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen) == n


def unique_cycle_parity(n, edges, deltas):
    adjacency = [[] for _ in range(n)]
    degree = [0] * n
    for i, (u, v) in enumerate(edges):
        adjacency[u].append((v, i))
        adjacency[v].append((u, i))
        degree[u] += 1
        degree[v] += 1
    alive = [True] * len(edges)
    queue = [v for v, d in enumerate(degree) if d == 1]
    while queue:
        u = queue.pop()
        for v, ei in adjacency[u]:
            if not alive[ei]:
                continue
            alive[ei] = False
            degree[u] -= 1
            degree[v] -= 1
            if degree[v] == 1:
                queue.append(v)
            break
    parity = 0
    for i, live in enumerate(alive):
        if live:
            parity ^= deltas[i]
    return parity


def direct_unicyclic_census(n, all_polarities):
    all_pairs = list(combinations(range(n), 2))
    cases = 0
    polarities = list(product((0, 1), repeat=3)) if all_polarities else [(0, 0, 0)]
    for edges in combinations(all_pairs, n):
        if not connected(n, edges):
            continue
        for deltas in product((0, 1), repeat=n):
            if unique_cycle_parity(n, edges, deltas) != 1:
                continue
            for terminals in combinations(range(n), 3):
                for polarity in polarities:
                    cases += 1
                    assert has_unsat_phase(n, terminals, edges, deltas, polarity)
    return cases


def main():
    exact = kernel_census()
    direct = {
        "n3_all_polarities": direct_unicyclic_census(3, True),
        "n4_all_polarities": direct_unicyclic_census(4, True),
        "n5_normalized_polarity": direct_unicyclic_census(5, False),
    }
    assert direct == {
        "n3_all_polarities": 32,
        "n4_all_polarities": 3840,
        "n5_normalized_polarity": 35520,
    }
    print(json.dumps({
        "kernel_census": exact,
        "direct_unicyclic_census": direct,
        "failures": 0,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
