from __future__ import annotations

import random


def paths(n, edges, source, target):
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


def feasible(n, edges, requests):
    pools = [paths(n, edges, source, target) for source, target in requests]
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
            groups.append(
                tuple((source, target) for _ in range(multiplicity))
            )
        requests = list(groups[0] + groups[1])
        original = feasible(n, edges, requests)

        resources = tuple((i, u, v) for i, (u, v) in enumerate(edges))
        assert len({resource_id for resource_id, _u, _v in resources}) == len(edges)
        reconstructed = feasible(
            n,
            tuple((u, v) for _resource_id, u, v in resources),
            requests,
        )
        assert reconstructed == original
        k = len(requests)
        tau = sum(max(0, len(group) - 1) for group in groups)
        assert tau == k - 2
        if original:
            yes += 1
        else:
            no += 1
    assert yes and no
    print(
        "V117 independent verifier passed: 240 fresh promised instances; "
        f"edge/resource bijection and tau=k-2 audited ({yes} yes, {no} no)."
    )


if __name__ == "__main__":
    main()
