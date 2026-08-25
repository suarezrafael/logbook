from __future__ import annotations

import random


def edge_paths(n, edges, source, target):
    adjacency = [[] for _ in range(n)]
    for edge_id, (u, v) in enumerate(edges):
        adjacency[u].append((v, edge_id))
    output = []

    def dfs(vertex, path):
        if vertex == target:
            output.append(tuple(path))
            return
        for nxt, edge_id in adjacency[vertex]:
            dfs(nxt, path + [edge_id])

    dfs(source, [])
    return output


def source_feasible(n, edges, requests):
    pools = [edge_paths(n, edges, source, target) for source, target in requests]
    order = sorted(range(len(requests)), key=lambda i: len(pools[i]))

    def search(pos, used):
        if pos == len(order):
            return True
        index = order[pos]
        for path in pools[index]:
            resource = set(path)
            if resource.isdisjoint(used) and search(pos + 1, used | resource):
                return True
        return False

    return search(0, set())


def build_gate_subdivision(n, edges):
    """Independent explicit graph: variable -> capacity-one gate node -> variable."""
    gate_node = {edge_id: n + edge_id for edge_id in range(len(edges))}
    adjacency = [[] for _ in range(n + len(edges))]
    node_resource = {}
    for edge_id, (u, v) in enumerate(edges):
        g = gate_node[edge_id]
        adjacency[u].append(g)
        adjacency[g].append(v)
        node_resource[g] = edge_id
    return adjacency, node_resource


def gate_paths(adjacency, node_resource, source, target):
    output = []

    def dfs(vertex, used_nodes, resources):
        if vertex == target:
            output.append(tuple(resources))
            return
        for nxt in adjacency[vertex]:
            if nxt in used_nodes:
                continue
            next_resources = resources
            if nxt in node_resource:
                next_resources = resources + [node_resource[nxt]]
            dfs(nxt, used_nodes | {nxt}, next_resources)

    dfs(source, {source}, [])
    return output


def transformed_feasible(n, edges, requests):
    adjacency, node_resource = build_gate_subdivision(n, edges)
    pools = [
        gate_paths(adjacency, node_resource, source, target)
        for source, target in requests
    ]
    order = sorted(range(len(requests)), key=lambda i: len(pools[i]))

    def search(pos, used):
        if pos == len(order):
            return True
        index = order[pos]
        for path in pools[index]:
            resources = set(path)
            if resources.isdisjoint(used) and search(pos + 1, used | resources):
                return True
        return False

    return search(0, set())


def main():
    yes = 0
    no = 0
    for seed in range(240):
        rng = random.Random(10000 + seed)
        n = 6
        edges = tuple(
            (u, v)
            for u in range(n)
            for v in range(u + 1, n)
            if rng.random() < 0.36
        )
        groups = []
        for _ in range(2):
            source = rng.randrange(n - 1)
            target = rng.randrange(source + 1, n)
            multiplicity = rng.choice((1, 2))
            groups.append(tuple((source, target) for _ in range(multiplicity)))
        requests = list(groups[0] + groups[1])

        original = source_feasible(n, edges, requests)
        transformed = transformed_feasible(n, edges, requests)
        assert transformed == original, (seed, original, transformed)

        adjacency, node_resource = build_gate_subdivision(n, edges)
        assert len(node_resource) == len(edges)
        assert len(adjacency) == n + len(edges)
        for edge_id, (u, v) in enumerate(edges):
            gate = n + edge_id
            assert adjacency[u].count(gate) == 1
            assert adjacency[gate] == [v]
            assert node_resource[gate] == edge_id

        k = len(requests)
        tau = sum(len(group) - 1 for group in groups)
        assert tau == k - 2
        if original:
            yes += 1
        else:
            no += 1

    assert yes and no
    print(
        "V117 independent verifier passed: 240 fresh promised instances; "
        f"explicit gate-node subdivision equivalence and tau=k-2 audited "
        f"({yes} yes, {no} no)."
    )


if __name__ == "__main__":
    main()
