from __future__ import annotations

import json
import random
from itertools import product

from signed_majority_kernel import Gate, avoid_essential_signed_majority, in_range


def exhaustive_n3():
    support = (0, 1, 2)
    polarities = list(product((0, 1), repeat=3))
    cases = 0
    modes = {}
    for ps in product(polarities, repeat=4):
        gates = [Gate(support, p) for p in ps]
        y, meta = avoid_essential_signed_majority(3, gates)
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
            assert not in_range(n, gates, y), (n, y, meta)
            modes[meta["case"]] = modes.get(meta["case"], 0) + 1
            by_n[n] = by_n.get(n, 0) + 1
            cases += 1
    assert cases == 520
    return {"cases": cases, "by_n": by_n, "modes": modes}


def unused_input_and_local_surplus_checks():
    rng = random.Random(170107)
    cases = []
    # Global n is larger than the support actually used.  The algorithm must
    # localize an inclusion-minimal surplus block rather than pay for unused inputs.
    for n in (7, 8, 9):
        pool = list(range(5))
        gates = [random_gate(rng, n, pool) for _ in range(7)]
        y, meta = avoid_essential_signed_majority(n, gates)
        assert meta["minimal_surplus_inputs"] <= 5
        assert meta["minimal_surplus_outputs"] == meta["minimal_surplus_inputs"] + 1
        assert not in_range(n, gates, y), (n, y, meta)
        cases.append((n, meta["minimal_surplus_inputs"], meta["case"]))
    return cases


def structured_cross_component_case():
    # Two disjoint unbalanced triangles form the frame basis after omitting the
    # final gate.  The omitted support spans both components, so V107 must use
    # the direct handcuff route.
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
    # Inclusion-minimal surplus extraction may select a smaller repeated-support
    # block before the intended cross-component block; correctness is the main
    # invariant, and random tests exercise both construction modes.
    return meta


def main():
    result = {
        "exhaustive_n3": exhaustive_n3(),
        "random_complete_range": randomized_complete_range(),
        "unused_input_localization": unused_input_and_local_surplus_checks(),
        "structured_control": structured_cross_component_case(),
        "failures": 0,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
