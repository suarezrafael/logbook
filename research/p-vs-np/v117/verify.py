from __future__ import annotations

import random

from two_chain_feedback_barrier import (
    GateChainInstance,
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


def check_noncontiguous_feedback_ids() -> None:
    instance = GateChainInstance(
        3,
        ((10, 0, 1), (40, 1, 2)),
        ((0, 2), (0, 2)),
        ((1, 2), (1, 2)),
    )
    closed = close_parallel_chains_with_feedback(instance)
    base_ids = {resource_id for resource_id, _u, _v in instance.resources}
    feedback_ids = {gate_id for gate_id, _chain, _u, _v in closed.feedback}
    assert base_ids.isdisjoint(feedback_ids)
    assert min(feedback_ids) == 41
    assert closed.tau == 2


def check_malformed_gate_chain_rejected() -> None:
    bad_endpoint = GateChainInstance(2, ((7, 0, 2),), ((0, 1),), ((0, 1),))
    bad_terminal = GateChainInstance(2, ((7, 0, 1),), ((0, 2),), ((0, 1),))
    for instance in (bad_endpoint, bad_terminal):
        try:
            gate_chain_feasible(instance)
        except ValueError:
            pass
        else:
            raise AssertionError("malformed gate-chain instance was not rejected")


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
    check_noncontiguous_feedback_ids()
    check_malformed_gate_chain_rejected()
    assert yes and no
    print(
        "V117 primary verifier passed: 500 promised two-parallel-demand DAG "
        f"instances; edge/gate equivalence exact ({yes} yes, {no} no); "
        "tau=k-2, sparse feedback IDs, and malformed-input rejection checked."
    )


if __name__ == "__main__":
    main()
