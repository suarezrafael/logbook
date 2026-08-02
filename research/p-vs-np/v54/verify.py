#!/usr/bin/env python3
from itertools import combinations

import v54_core as c


def check_case(n, edges, expected):
    cert = c.certificate(n, edges)
    m = len(edges)
    y = c.target(m, cert)
    image = {c.output(x, edges) for x in range(1 << n)}
    assert y not in image
    assert cert["degree"] == expected
    assert c.union_free(edges, expected - 1)
    for prime in (2, 3, 5):
        assert c.relation(y, cert, prime) == 1
        assert all(c.relation(z, cert, prime) == 0 for z in image)
    return {
        "n": n,
        "m": m,
        "range_size": len(image),
        "certificate": cert,
        "target": y,
        "exact_sepdeg": expected,
    }


def main():
    triples = list(combinations(range(5), 3))
    exhaustive = 0
    distribution = {}
    for size in range(6, 11):
        for inds in combinations(range(10), size):
            edges = [triples[i] for i in inds]
            cert = c.certificate(5, edges)
            y = c.target(len(edges), cert)
            assert y not in {c.output(x, edges) for x in range(32)}
            distribution[cert["degree"]] = distribution.get(cert["degree"], 0) + 1
            exhaustive += 1

    # Acyclic nested-union counterexample to the retracted girth claim.
    tree = [(0, 1, 2), (0, 3, 4), (1, 5, 6), (2, 7, 8)]
    assert set().union(*(set(tree[i]) for i in (1, 2, 3))) == set().union(
        *(set(tree[i]) for i in (0, 1, 2, 3))
    )
    assert sum(map(len, tree)) == len(tree) + 9 - 1

    classes = c.npn_classes()
    singleton = sum(c.singleton_fiber(f) for f in range(256))
    assert len(classes) == 14 and singleton == 16

    results = {
        "status": "passed",
        "UF2": check_case(8, c.UF2, 3),
        "UF3": check_case(15, c.UF3, 4),
        "exhaustive_n5": exhaustive,
        "degree_distribution": distribution,
        "npn_classes": 14,
        "singleton_fiber_functions": 16,
        "failures": 0,
    }
    assert results["exhaustive_n5"] == 386
    assert sum(results["degree_distribution"].values()) == 386
    print("V54 verification passed:", results)
    print("  diagnostics are recomputed in memory; no repository snapshot is written.")


if __name__ == "__main__":
    main()
