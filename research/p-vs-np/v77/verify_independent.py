#!/usr/bin/env python3
"""Independent V77 audit.

This verifier imports neither the topology certificate engine nor the V77
generator.  It reconstructs the static hierarchy, five-variable orbit counts,
height-capped widths, the two-edge witness, and selected repository controls.
"""
from __future__ import annotations

from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations
from json import dumps, loads
from math import ceil, log2
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def validate_tree(adjacency: dict[int, set[int]]) -> None:
    if not adjacency:
        raise AssertionError("empty source tree")
    if any(len(neighbors) > 3 for neighbors in adjacency.values()):
        raise AssertionError("source tree is not subcubic")
    for vertex, neighbors in adjacency.items():
        for neighbor in neighbors:
            if vertex not in adjacency.get(neighbor, set()):
                raise AssertionError("asymmetric adjacency")
    if sum(len(neighbors) for neighbors in adjacency.values()) // 2 != len(adjacency) - 1:
        raise AssertionError("source graph is not a tree")
    seen: set[int] = set()
    stack = [next(iter(adjacency))]
    while stack:
        vertex = stack.pop()
        if vertex in seen:
            continue
        seen.add(vertex)
        stack.extend(adjacency[vertex] - seen)
    if len(seen) != len(adjacency):
        raise AssertionError("source graph is disconnected")


def raw_boundary_edges(adjacency: dict[int, set[int]], vertices: set[int]) -> list[list[int]]:
    return [
        [vertex, neighbor]
        for vertex in sorted(vertices)
        for neighbor in sorted(adjacency[vertex])
        if neighbor not in vertices
    ]


def audit_static_certificate(results: dict[str, object]) -> dict[str, int]:
    path = HERE / "STATIC_TOPOLOGY_CERTIFICATE.json"
    raw_text = path.read_text(encoding="utf-8")
    data = loads(raw_text)
    normalized = (dumps(data, indent=2, sort_keys=True) + "\n").encode()
    if sha256(normalized).hexdigest() != results["static_certificate"]["sha256"]:
        raise AssertionError("static certificate digest mismatch")

    adjacency = {
        int(vertex): set(map(int, neighbors))
        for vertex, neighbors in data["source_adjacency"].items()
    }
    labels = {int(vertex): int(label) for vertex, label in data["labels"].items()}
    validate_tree(adjacency)
    if any(len(adjacency[vertex]) != 1 for vertex in labels):
        raise AssertionError("gate labels must lie on degree-one source vertices")
    if len(set(labels.values())) != len(labels):
        raise AssertionError("gate labels are not unique")

    clusters = {int(item["cluster_id"]): item for item in data["clusters"]}
    root = int(data["root"])
    if root not in clusters:
        raise AssertionError("missing certificate root")
    degree_histogram = {0: 0, 1: 0, 2: 0, 3: 0}
    for cluster_id, cluster in clusters.items():
        vertices = set(map(int, cluster["vertices"]))
        if not vertices:
            raise AssertionError("empty topology cluster")
        expected_boundary = raw_boundary_edges(adjacency, vertices)
        if expected_boundary != cluster["boundary_edges"]:
            raise AssertionError("static boundary-edge list is incorrect")
        external_degree = len(expected_boundary)
        if external_degree > 3:
            raise AssertionError("topology cluster external degree exceeds three")
        if external_degree == 3 and len(vertices) != 1:
            raise AssertionError("degree-three topology cluster is not singleton")
        degree_histogram[external_degree] += 1
        children = tuple(map(int, cluster["children"]))
        if not children:
            if len(vertices) != 1 or int(cluster["level"]) != 0:
                raise AssertionError("malformed base cluster")
            continue
        if len(children) not in (1, 2):
            raise AssertionError("topology hierarchy is not unary/binary")
        child_vertices: list[set[int]] = [set(map(int, clusters[child]["vertices"])) for child in children]
        if len(children) == 2 and child_vertices[0] & child_vertices[1]:
            raise AssertionError("topology children overlap")
        if set().union(*child_vertices) != vertices:
            raise AssertionError("parent cluster differs from child union")
        child_levels = {int(clusters[child]["level"]) for child in children}
        if len(child_levels) != 1 or int(cluster["level"]) != next(iter(child_levels)) + 1:
            raise AssertionError("topology levels are inconsistent")
        if len(children) == 2:
            crossing = sum(
                neighbor in child_vertices[1]
                for vertex in child_vertices[0]
                for neighbor in adjacency[vertex]
            )
            if crossing != 1:
                raise AssertionError("binary children lack one connecting tree edge")
    if set(map(int, clusters[root]["vertices"])) != set(adjacency):
        raise AssertionError("root does not cover the source tree")

    descendant_labels: dict[int, frozenset[int]] = {}
    retained_degree_histogram = {0: 0, 1: 0, 2: 0}
    retained = 0

    def visit(cluster_id: int) -> frozenset[int]:
        nonlocal retained
        cluster = clusters[cluster_id]
        children = tuple(map(int, cluster["children"]))
        if not children:
            vertex = int(cluster["vertices"][0])
            labels_here = frozenset((labels[vertex],)) if vertex in labels else frozenset()
        else:
            labels_here = frozenset(label for child in children for label in visit(child))
        descendant_labels[cluster_id] = labels_here
        nonempty_children = [child for child in children if descendant_labels[child]]
        is_retained = bool(labels_here) and (not children or len(nonempty_children) == 2)
        if is_retained:
            external_degree = len(cluster["boundary_edges"])
            if external_degree > 2:
                raise AssertionError("retained label cluster has more than two boundary edges")
            retained_degree_histogram[external_degree] += 1
            retained += 1
        return labels_here

    if visit(root) != frozenset(labels.values()):
        raise AssertionError("static certificate loses gate labels")
    if int(data["height"]) != max(int(cluster["level"]) for cluster in clusters.values()):
        raise AssertionError("static topology height is incorrect")
    return {
        "vertices": len(adjacency),
        "clusters": len(clusters),
        "retained": retained,
        "retained_degree_two": retained_degree_histogram[2],
    }


def support_universe() -> tuple[int, ...]:
    return tuple(
        sum(1 << variable for variable in support)
        for rank in (1, 2, 3)
        for support in combinations(range(5), rank)
    )


def permutation_maps(universe: tuple[int, ...]) -> tuple[dict[int, int], ...]:
    answer = []
    for permutation in permutations(range(5)):
        mapping: dict[int, int] = {}
        for support in universe:
            image = 0
            for variable in range(5):
                if (support >> variable) & 1:
                    image |= 1 << permutation[variable]
            mapping[support] = image
        answer.append(mapping)
    return tuple(answer)


def canonical_family(family: tuple[int, ...], maps: tuple[dict[int, int], ...]) -> tuple[int, ...]:
    return min(tuple(sorted(mapping[support] for support in family)) for mapping in maps)


def boundary_sizes(family: tuple[int, ...]) -> tuple[int, ...]:
    m = len(family)
    unions = [0] * (1 << m)
    for mask in range(1, 1 << m):
        bit = mask & -mask
        index = bit.bit_length() - 1
        unions[mask] = unions[mask ^ bit] | family[index]
    full = (1 << m) - 1
    return tuple((unions[mask] & unions[full ^ mask]).bit_count() for mask in range(1 << m))


def minimum_width_with_height(family: tuple[int, ...], height: int) -> int:
    boundaries = boundary_sizes(family)
    m = len(family)
    infinity = 10**9

    @lru_cache(None)
    def solve(mask: int, remaining_height: int) -> int:
        if mask.bit_count() == 1:
            return boundaries[mask]
        if remaining_height == 0:
            return infinity
        anchor = mask & -mask
        best = infinity
        subset = (mask - 1) & mask
        while subset:
            if subset & anchor and subset != mask:
                complement = mask ^ subset
                best = min(
                    best,
                    max(
                        boundaries[mask],
                        solve(subset, remaining_height - 1),
                        solve(complement, remaining_height - 1),
                    ),
                )
            subset = (subset - 1) & mask
        return best

    return solve((1 << m) - 1, int(height))


def audit_five_variable_orbits(results: dict[str, object]) -> dict[str, object]:
    universe = support_universe()
    maps = permutation_maps(universe)
    orbit_counts = []
    raw_counts = []
    sampled_width_checks = 0
    for gate_count in range(1, 7):
        orbits: set[tuple[int, ...]] = set()
        raw = 0
        for family in combinations(universe, gate_count):
            raw += 1
            orbits.add(canonical_family(tuple(family), maps))
        orbit_counts.append(len(orbits))
        raw_counts.append(raw)
        cap = ceil(log2(gate_count)) if gate_count > 1 else 0
        iterable = sorted(orbits) if gate_count <= 5 else sorted(orbits)[::7]
        for family in iterable:
            unrestricted = minimum_width_with_height(family, gate_count - 1)
            perfect = minimum_width_with_height(family, cap)
            if perfect != unrestricted:
                raise AssertionError("unexpected five-variable perfect-height inflation")
            sampled_width_checks += 1
    expected = results["five_variable_isomorphism_audit"]
    if orbit_counts != [3, 12, 50, 193, 648, 1896]:
        raise AssertionError("five-variable orbit counts drifted")
    if raw_counts != [25, 300, 2300, 12650, 53130, 177100]:
        raise AssertionError("five-variable raw counts drifted")
    if sum(orbit_counts) != expected["isomorphism_orbits"]:
        raise AssertionError("committed orbit total mismatch")
    return {"orbit_counts": orbit_counts, "sampled_width_checks": sampled_width_checks}


def audit_v76_witnesses() -> None:
    witnesses = (
        (1, 2, 5, 9, 6, 10, 12),
        (1, 4, 3, 9, 6, 10, 12),
        (1, 8, 3, 5, 6, 10, 12),
        (2, 4, 3, 5, 9, 10, 12),
        (2, 8, 3, 5, 9, 6, 12),
        (4, 8, 3, 5, 9, 6, 10),
    )
    for family in witnesses:
        if minimum_width_with_height(family, 6) != 2:
            raise AssertionError("V76 witness minimum width drifted")
        if minimum_width_with_height(family, 3) != 3:
            raise AssertionError("V76 witness perfect-height width drifted")


def audit_two_edge_tightness(results: dict[str, object]) -> None:
    supports = ((0, 1, 2), (0, 1, 2), (3, 4, 5), (3, 4, 5))
    selected = {1, 2}
    left = set().union(*(supports[index] for index in selected))
    right = set().union(*(supports[index] for index in range(4) if index not in selected))
    boundary = left & right
    if len(boundary) != 6:
        raise AssertionError("independent tightness boundary failed")
    tight = results["two_edge_tightness_witness"]
    if tight["source_width_b"] != 3 or tight["cluster_width"] != 6:
        raise AssertionError("committed tightness witness drifted")


def gaussian_binomial_2(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    numerator = denominator = 1
    for index in range(k):
        numerator *= (1 << (n - index)) - 1
        denominator *= (1 << (k - index)) - 1
    return numerator // denominator


def affine_count(boundary: int) -> int:
    return sum(
        (1 << (boundary - codimension)) * gaussian_binomial_2(boundary, codimension)
        for codimension in range(boundary + 1)
    )


def main() -> None:
    results = loads((HERE / "RESULTS.json").read_text(encoding="utf-8"))
    static = audit_static_certificate(results)
    orbit = audit_five_variable_orbits(results)
    audit_v76_witnesses()
    audit_two_edge_tightness(results)

    for row in results["affine_cost_table"]:
        b = int(row["b"])
        if row["A_2b"] != affine_count(2 * b) or row["A_4b"] != affine_count(4 * b):
            raise AssertionError("affine cost table drifted")

    proof = (HERE / "TOPOLOGY_TREE_TRANSFER.md").read_text(encoding="utf-8")
    for token in (
        "cluster with three leaving edges consists of one vertex",
        "boundary_variables(S(C))",
        "A(2b)^2",
        "Novelty remains unconfirmed",
    ):
        if token not in proof:
            raise AssertionError(token)
    state = (ROOT / "STATE.md").read_text(encoding="utf-8")
    if "**Direct P-versus-NP route active:** no" not in state or "**P versus NP resolved:** no" not in state:
        raise AssertionError("repository nonclaim controls drifted")

    print(
        "V77 independent verification passed: static topology certificate reconstructed; retained two-edge invariant; "
        f"five-variable orbit counts {orbit['orbit_counts']}; {orbit['sampled_width_checks']} independent width checks; "
        f"static clusters={static['clusters']}; V76 witnesses and affine costs; zero failures."
    )


if __name__ == "__main__":
    main()
