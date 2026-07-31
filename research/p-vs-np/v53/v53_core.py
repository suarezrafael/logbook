#!/usr/bin/env python3
"""Core routines for Laboratory V53."""
from __future__ import annotations
from itertools import combinations
from typing import Iterable, Sequence


def edge_mask(edge: Sequence[int]) -> int:
    value = 0
    for v in edge:
        value |= 1 << int(v)
    return value


def subset_unions(edges: Sequence[Sequence[int]], max_size: int):
    masks = [edge_mask(e) for e in edges]
    for size in range(max_size + 1):
        for chosen in combinations(range(len(edges)), size):
            union = 0
            for index in chosen:
                union |= masks[index]
            yield chosen, union


def union_free_certificate(edges: Sequence[Sequence[int]], t: int):
    seen = {}
    for chosen, union in subset_unions(edges, t):
        if union in seen:
            return False, seen, (seen[union], chosen, union)
        seen[union] = chosen
    return True, seen, None


def and3_output(assignment: int, edges: Sequence[Sequence[int]]) -> int:
    output = 0
    for i, edge in enumerate(edges):
        bit = 1
        for v in edge:
            bit &= (assignment >> int(v)) & 1
        output |= bit << i
    return output


def circuit_image(n: int, edges: Sequence[Sequence[int]], output_flip_mask: int = 0):
    return sorted({and3_output(x, edges) ^ output_flip_mask for x in range(1 << n)})


def monomials(m: int, max_degree: int):
    result = [()]
    for degree in range(1, max_degree + 1):
        result.extend(combinations(range(m), degree))
    return result


def eval_monomial(point: int, monomial: Sequence[int]) -> int:
    return int(all((point >> index) & 1 for index in monomial))


def evaluation_matrix(image: Sequence[int], m: int, max_degree: int):
    mons = monomials(m, max_degree)
    return [[eval_monomial(point, monomial) for monomial in mons] for point in image]


def rank_mod(matrix: Sequence[Sequence[int]], prime: int) -> int:
    if not matrix:
        return 0
    a = [[value % prime for value in row] for row in matrix]
    rows, cols = len(a), len(a[0])
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, rows) if a[r][col] % prime), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inverse = pow(a[rank][col], -1, prime)
        a[rank] = [(v * inverse) % prime for v in a[rank]]
        for r in range(rows):
            if r == rank or not a[r][col] % prime:
                continue
            factor = a[r][col] % prime
            a[r] = [(a[r][c] - factor * a[rank][c]) % prime for c in range(cols)]
        rank += 1
        if rank == rows:
            break
    return rank


def exact_syndrome_degree_gf2(image: Sequence[int], m: int, max_degree: int | None = None):
    if max_degree is None:
        max_degree = m
    row_count = len(image)
    full_column = (1 << row_count) - 1
    coordinate_columns = []
    for coordinate in range(m):
        column = 0
        for row, point in enumerate(image):
            if (point >> coordinate) & 1:
                column |= 1 << row
        coordinate_columns.append(column)
    pivots = {}
    for degree in range(max_degree + 1):
        degree_monomials: Iterable[tuple[int, ...]]
        degree_monomials = [()] if degree == 0 else combinations(range(m), degree)
        for monomial in degree_monomials:
            column = full_column
            for coordinate in monomial:
                column &= coordinate_columns[coordinate]
            value = column
            while value:
                pivot = value.bit_length() - 1
                if pivot in pivots:
                    value ^= pivots[pivot]
                else:
                    pivots[pivot] = value
                    break
            if not value:
                return degree
    return None


FINITE_EXAMPLES = {
    "UF2": {
        "t": 2, "n": 8, "output_flip_mask": int("101001011", 2),
        "edges": [[1,3,5],[1,3,4],[1,3,7],[0,2,4],[0,5,6],[0,3,5],[1,2,7],[2,6,7],[0,2,6]],
    },
    "UF3": {
        "t": 3, "n": 15, "output_flip_mask": int("1011001010010110", 2),
        "edges": [[4,7,11],[5,10,13],[1,4,10],[8,11,12],[0,1,7],[3,7,12],[2,4,5],[5,8,14],[2,3,14],[2,10,12],[3,9,13],[2,9,11],[0,6,12],[0,8,13],[4,6,9],[1,9,14]],
    },
}
