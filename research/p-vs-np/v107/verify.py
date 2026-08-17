from __future__ import annotations

import json
import random
from itertools import product

from signed_majority_avoider import (
    Gate,
    avoid_essential_signed_majority,
    fundamental_hall_circuit,
    in_range,
)


def exhaustive_n3():
    support = (0, 1, 2)
    polarities = list(product((0, 1), repeat=3))
    cases = 0
    modes = {}
    for ps in product(polarities, repeat=4):
        gates = [Gate(support, p) for p in ps]
        y, meta = avoid_essential_signed_majority(3, gates)
        assert meta["surplus_extraction"] == "transversal_fundamental_circuit"
        assert not in_range(3, gates, y), (ps, y, meta)
        modes[meta["case"]] = modes.get(meta["case"], 0) + 1
        cases += 1
    assert cases == 4096
    return {"cases": cases, "modes": modes}


def random_gate(rng: random.Random, n: int, support_pool=None):
    pool = list(range(n)) if support_pool is None else list(support_pool)
    support = tuple(rng.sample(pool, 3))
    polarity = tuple(rng.randrange(2) for _ in range(3))
    return Gate(support, polarity)


def randomized_complete_range():
    rng = random.Random(107107)
    cases = 0
    modes = {}
    by_n = {}
    for n, trials in ((4, 180), (5, 160), (6, 120), (7, 60)):
        for _ in range(trials):
            extra = rng.randrange(1, 3)
            gates = [random_gate(rng, n) for _ in range(n + extra)]
            y, meta = avoid_essential_signed_majority(n, gates)
            assert meta["surplus_extraction"] == "transversal_fundamental_circuit"
            assert not in_range(n, gates, y), (n, y, meta)
            modes[meta["case"]] = modes.get(meta["case"], 0) + 1
            by_n[n] = by_n.get(n, 0) + 1
            cases += 1
    assert cases == 520
    return {"cases": cases, "by_n": by_n, "modes": modes}


def unused_input_and_local_surplus_checks():
    rng = random.Random(170107)
    cases = []
    for n in (7, 8, 9):
        pool = list(range(5))
        gates = [random_gate(rng, n, pool) for _ in range(7)]
        y, meta = avoid_essential_signed_majority(n, gates)
        assert meta["hall_circuit_inputs"] <= 5
        assert meta["hall_circuit_outputs"] == meta["hall_circuit_inputs"] + 1
        assert not in_range(n, gates, y), (n, y, meta)
        cases.append((n, meta["hall_circuit_inputs"], meta["case"]))
    return cases


def nonmonotone_surplus_regression():
    # The old delete-while-the-current-set-stays-deficient heuristic gets stuck
    # on all six outputs: deleting either support type can expose new variables
    # fast enough to kill the current surplus.  Nevertheless four A-support
    # outputs already form a Hall circuit on only three variables.
    supports = [
        (1, 2, 4),
        (1, 2, 4),
        (0, 3, 4),
        (1, 2, 4),
        (1, 2, 4),
        (0, 2, 3),
    ]
    gates = [Gate(s, (0, 0, 0)) for s in supports]
    circuit = fundamental_hall_circuit(5, gates)
    neighborhood = set()
    for i in circuit:
        neighborhood.update(gates[i].support)
    assert len(circuit) == 4
    assert len(neighborhood) == 3
    assert all(gates[i].support == (1, 2, 4) for i in circuit)
    y, meta = avoid_essential_signed_majority(5, gates)
    assert meta["hall_circuit_outputs"] == 4
    assert meta["hall_circuit_inputs"] == 3
    assert not in_range(5, gates, y), (y, meta)
    return {"circuit": circuit, "neighborhood": sorted(neighborhood)}


def structured_cross_component_case():
    gates = [
        Gate((0, 1, 2), (0, 0, 0)),
        Gate((0, 1, 2), (0, 0, 1)),
        Gate((0, 1, 2), (0, 1, 0)),
        Gate((3, 4, 5), (0, 0, 0)),
        Gate((3, 4, 5), (0, 0, 1)),
        Gate((3, 4, 5), (0, 1, 0)),
        Gate((0, 3, 5), (1, 0, 0)),
    ]
    y, meta = avoid_essential_signed_majority(6, gates)
    assert not in_range(6, gates, y), (y, meta)
    return meta


def main():
    result = {
        "exhaustive_n3": exhaustive_n3(),
        "random_complete_range": randomized_complete_range(),
        "unused_input_localization": unused_input_and_local_surplus_checks(),
        "nonmonotone_surplus_regression": nonmonotone_surplus_regression(),
        "structured_control": structured_cross_component_case(),
        "failures": 0,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
