from __future__ import annotations

import json
from itertools import combinations

from adaptive_pair_repair import (
    avoid_with_pair_repair,
    avoid_with_choices,
    edge_for_choice,
    in_range,
    selected_edges,
    strict_one_repair_family,
)


def exact_beta(n, gates):
    """Exact strong-affine-backdoor size for signed majority by complement search."""
    supports = [set(g.support) for g in gates]
    for free_size in range(n, -1, -1):
        for free in combinations(range(n), free_size):
            F = set(free)
            if all(len(F & support) <= 1 for support in supports):
                return n - free_size
    raise AssertionError("full input set is always a backdoor")


def no_proper_positive_surplus(n, gates):
    m = len(gates)
    for mask in range(1, (1 << m) - 1):
        used = set()
        count = 0
        for i, gate in enumerate(gates):
            if (mask >> i) & 1:
                count += 1
                used.update(gate.support)
        if count > len(used):
            return False
    return True


def matching_after_deletion(n, gates, deleted):
    """Check Hall-minimality by matching every remaining gate to a distinct input."""
    owner = [None] * n

    def augment(gate_index, seen):
        for v in gates[gate_index].support:
            if v in seen:
                continue
            seen.add(v)
            if owner[v] is None or augment(owner[v], seen):
                owner[v] = gate_index
                return True
        return False

    for i in range(len(gates)):
        if i == deleted:
            continue
        if not augment(i, set()):
            return False
    return True


def transport_triangle_identity(gate):
    deltas = [edge_for_choice(0, gate, choice).delta for choice in range(3)]
    return deltas[0] ^ deltas[1] ^ deltas[2]


def strict_family_checks():
    complete = []
    structural = []
    unique_repair = []

    for q in range(0, 5):
        n, gates, repair_gate = strict_one_repair_family(q)
        m = len(gates)
        assert m == n + 1
        assert all(transport_triangle_identity(g) == 1 for g in gates)

        # V105/canonical choice is sigma=0 and must fail on the theta core.
        try:
            avoid_with_pair_repair(n, gates, budget=0)
        except ValueError:
            pass
        else:
            raise AssertionError((q, "canonical selection unexpectedly found a barbell"))

        y, meta = avoid_with_pair_repair(n, gates, budget=1)
        assert meta["repair_distance"] == 1
        assert meta["kind"] == "figure_eight"
        assert meta["changed"] == ((repair_gate, 2),)
        assert not in_range(n, gates, y), (q, y, meta)
        complete.append(n)

        # Exhaust every one-switch repair: the designed switch is unique.
        hits = []
        for gate_index in range(m):
            for choice in (1, 2):
                choices = [0] * m
                choices[gate_index] = choice
                try:
                    _y, local = avoid_with_choices(n, gates, tuple(choices))
                except ValueError:
                    continue
                hits.append((gate_index, choice, local["kind"]))
        assert hits == [(repair_gate, 2, "figure_eight")], (q, hits)
        unique_repair.append(n)

    for q in range(0, 31):
        n, gates, repair_gate = strict_one_repair_family(q)
        y, meta = avoid_with_pair_repair(n, gates, budget=1)
        assert meta["repair_distance"] == 1
        assert meta["changed"] == ((repair_gate, 2),)
        assert meta["kind"] == "figure_eight"
        structural.append(n)

    beta_cases = {}
    for q in range(0, 6):
        n, gates, _ = strict_one_repair_family(q)
        beta = exact_beta(n, gates)
        assert beta == (n + 3) // 2, (n, beta)
        beta_cases[n] = beta

    surplus_cases = []
    for q in range(0, 4):
        n, gates, _ = strict_one_repair_family(q)
        assert no_proper_positive_surplus(n, gates)
        surplus_cases.append(n)

    hall_minimal = []
    for q in range(0, 21):
        n, gates, _ = strict_one_repair_family(q)
        assert all(matching_after_deletion(n, gates, deleted) for deleted in range(len(gates)))
        hall_minimal.append(n)

    return {
        "complete_original_range_n": complete,
        "structural_sigma_one_n_through": structural[-1],
        "unique_one_repair_n": unique_repair,
        "exact_beta": beta_cases,
        "no_proper_positive_surplus_n": surplus_cases,
        "single_deletion_hall_matching_n_through": hall_minimal[-1],
    }


def main():
    result = {
        "parameter": "sigma_pair_repair",
        "runtime": "O((2m)^sigma poly(N))",
        "strict_family": strict_family_checks(),
        "failures": 0,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
