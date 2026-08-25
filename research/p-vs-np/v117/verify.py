from __future__ import annotations

import random

from two_chain_feedback_barrier import (
    ParallelTwoChainEDP,
    close_parallel_chains_with_feedback,
    edge_to_gate_chain,
    gate_chain_feasible,
    source_edge_disjoint_feasible,
)


def random_instance(seed: int) -> ParallelTwoChainEDP:
    rng = random.Random(seed)
    n = 6
    edges = tuple(
        (u, v)
        for u in range(n)
        for v in range(u + 1, n)
        if rng.random() < 0.33
    )
    chains = []
    for _ in range(2):
        source = rng.randrange(n - 1)
        target = rng.randrange(source + 1, n)
        multiplicity = rng.choice((1, 2))
        chains.append(tuple((source, target) for _ in range(multiplicity)))
    return ParallelTwoChainEDP(n, edges, chains[0], chains[1])


def main() -> None:
    yes = 0
    no = 0
    for seed in range(500):
        source = random_instance(seed)
        gate = edge_to_gate_chain(source)
        feedback = close_parallel_chains_with_feedback(gate)
        expected = source_edge_disjoint_feasible(source)
        actual = gate_chain_feasible(gate)
        assert actual == expected, (seed, expected, actual)
        assert feedback.tau == source.k - 2
        assert len(feedback.prescribed0) == len(source.chain0) - 1
        assert len(feedback.prescribed1) == len(source.chain1) - 1
        if actual:
            yes += 1
        else:
            no += 1
    assert yes and no
    print(
        "V117 primary verifier passed: 500 promised two-parallel-demand DAG "
        f"instances; edge/gate equivalence exact ({yes} yes, {no} no); "
        "tau=k-2 checked."
    )


if __name__ == "__main__":
    main()
