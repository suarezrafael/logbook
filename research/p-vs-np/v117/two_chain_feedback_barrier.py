from __future__ import annotations

from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class ParallelTwoChainEDP:
    n: int
    edges: tuple[tuple[int, int], ...]
    chain0: tuple[tuple[int, int], ...]
    chain1: tuple[tuple[int, int], ...]

    @property
    def k(self) -> int:
        return len(self.chain0) + len(self.chain1)


@dataclass(frozen=True)
class GateChainInstance:
    n_variables: int
    resources: tuple[tuple[int, int, int], ...]
    chain0: tuple[tuple[int, int], ...]
    chain1: tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class PrescribedFeedbackInstance:
    base: GateChainInstance
    feedback: tuple[tuple[int, int, int, int], ...]
    prescribed0: tuple[int, ...]
    prescribed1: tuple[int, ...]

    @property
    def tau(self) -> int:
        return len(self.feedback)


def _is_dag(n: int, edges: tuple[tuple[int, int], ...]) -> bool:
    adjacency = [[] for _ in range(n)]
    indegree = [0] * n
    for u, v in edges:
        if not (0 <= u < n and 0 <= v < n):
            return False
        adjacency[u].append(v)
        indegree[v] += 1
    queue = deque(i for i in range(n) if indegree[i] == 0)
    seen = 0
    while queue:
        u = queue.popleft()
        seen += 1
        for v in adjacency[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    return seen == n


def _parallel(chain: tuple[tuple[int, int], ...]) -> bool:
    return not chain or len(set(chain)) == 1


def validate_source(instance: ParallelTwoChainEDP) -> None:
    if instance.n <= 0 or not _is_dag(instance.n, instance.edges):
        raise ValueError("source graph must be a DAG")
    if not instance.chain0 or not instance.chain1:
        raise ValueError(
            "this reducer expects the normalized nonempty-class promise; "
            "pad an empty parallel demand class by one private forced request first"
        )
    if not _parallel(instance.chain0) or not _parallel(instance.chain1):
        raise ValueError("each demand class must consist of parallel requests")
    for s, t in instance.chain0 + instance.chain1:
        if not (0 <= s < instance.n and 0 <= t < instance.n):
            raise ValueError("terminal outside source graph")


def edge_to_gate_chain(instance: ParallelTwoChainEDP) -> GateChainInstance:
    """Subdivide each source edge by one capacity-one gate resource."""
    validate_source(instance)
    resources = tuple((i, u, v) for i, (u, v) in enumerate(instance.edges))
    return GateChainInstance(
        instance.n,
        resources,
        instance.chain0,
        instance.chain1,
    )


def close_parallel_chains_with_feedback(
    instance: GateChainInstance,
) -> PrescribedFeedbackInstance:
    """Reconnect each repeated demand chain by private prescribed feedback gates."""
    feedback: list[tuple[int, int, int, int]] = []
    prescribed = [[], []]
    resource_ids = [resource_id for resource_id, _u, _v in instance.resources]
    if len(resource_ids) != len(set(resource_ids)):
        raise ValueError("base gate resource IDs must be unique")
    next_gate = 0 if not resource_ids else max(resource_ids) + 1
    for chain_index, chain in enumerate((instance.chain0, instance.chain1)):
        for pos in range(len(chain) - 1):
            target = chain[pos][1]
            source = chain[pos + 1][0]
            gate_id = next_gate
            next_gate += 1
            feedback.append((gate_id, chain_index, target, source))
            prescribed[chain_index].append(gate_id)
    return PrescribedFeedbackInstance(
        instance,
        tuple(feedback),
        tuple(prescribed[0]),
        tuple(prescribed[1]),
    )


def all_source_paths(
    instance: ParallelTwoChainEDP,
    request: tuple[int, int],
) -> tuple[tuple[int, ...], ...]:
    source, target = request
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(instance.n)]
    for edge_id, (u, v) in enumerate(instance.edges):
        adjacency[u].append((v, edge_id))
    output: list[tuple[int, ...]] = []

    def dfs(vertex: int, path: list[int]) -> None:
        if vertex == target:
            output.append(tuple(path))
            return
        for nxt, edge_id in adjacency[vertex]:
            dfs(nxt, path + [edge_id])

    dfs(source, [])
    return tuple(output)


def source_edge_disjoint_feasible(instance: ParallelTwoChainEDP) -> bool:
    validate_source(instance)
    requests = list(instance.chain0 + instance.chain1)
    path_lists = [all_source_paths(instance, request) for request in requests]
    order = sorted(range(len(requests)), key=lambda i: len(path_lists[i]))

    def search(pos: int, used: frozenset[int]) -> bool:
        if pos == len(order):
            return True
        index = order[pos]
        for path in path_lists[index]:
            resources = frozenset(path)
            if resources.isdisjoint(used) and search(pos + 1, used | resources):
                return True
        return False

    return search(0, frozenset())


def gate_chain_feasible(instance: GateChainInstance) -> bool:
    adjacency: list[list[tuple[int, int]]] = [
        [] for _ in range(instance.n_variables)
    ]
    for resource_id, u, v in instance.resources:
        adjacency[u].append((v, resource_id))

    def paths(request: tuple[int, int]) -> tuple[tuple[int, ...], ...]:
        source, target = request
        output: list[tuple[int, ...]] = []

        def dfs(vertex: int, path: list[int]) -> None:
            if vertex == target:
                output.append(tuple(path))
                return
            for nxt, resource_id in adjacency[vertex]:
                dfs(nxt, path + [resource_id])

        dfs(source, [])
        return tuple(output)

    requests = list(instance.chain0 + instance.chain1)
    path_lists = [paths(request) for request in requests]
    order = sorted(range(len(requests)), key=lambda i: len(path_lists[i]))

    def search(pos: int, used: frozenset[int]) -> bool:
        if pos == len(order):
            return True
        index = order[pos]
        for path in path_lists[index]:
            resources = frozenset(path)
            if resources.isdisjoint(used) and search(pos + 1, used | resources):
                return True
        return False

    return search(0, frozenset())
