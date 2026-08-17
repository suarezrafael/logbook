from __future__ import annotations

import signed_majority_kernel as core

Gate = core.Gate
in_range = core.in_range


def _matching(n: int, gates: list[Gate], indices) -> dict[int, int] | None:
    """Return gate->input matching covering all `indices`, or None."""
    indices = list(indices)
    owner: list[int | None] = [None] * n

    def augment(gate_index: int, seen: set[int]) -> bool:
        for v in gates[gate_index].support:
            if v in seen:
                continue
            seen.add(v)
            previous = owner[v]
            if previous is None or augment(previous, seen):
                owner[v] = gate_index
                return True
        return False

    for gate_index in indices:
        if not augment(gate_index, set()):
            return None
    return {gate_index: v for v, gate_index in enumerate(owner) if gate_index is not None}


def _maximum_matching(n: int, gates: list[Gate], indices) -> dict[int, int]:
    """Maximum-cardinality matching by the standard augmenting-path algorithm."""
    owner: list[int | None] = [None] * n

    def augment(gate_index: int, seen: set[int]) -> bool:
        for v in gates[gate_index].support:
            if v in seen:
                continue
            seen.add(v)
            previous = owner[v]
            if previous is None or augment(previous, seen):
                owner[v] = gate_index
                return True
        return False

    for gate_index in indices:
        augment(gate_index, set())
    return {gate_index: v for v, gate_index in enumerate(owner) if gate_index is not None}


def fundamental_hall_circuit(n: int, gates: list[Gate]) -> list[int]:
    """Extract a minimal Hall-deficient output set in polynomial time.

    Outputs form the ground set of the transversal matroid defined by the
    output-input support graph.  A maximum matching supplies an independent
    basis I.  Since m>n (and hence m exceeds the support rank), choose an
    unmatched output e.  The unique fundamental circuit C(e,I) is

        {e} union {f in I : I-f+e is matchable}.

    Every proper subset of C is matchable.  Hall's theorem therefore forces
    |N(C)|=|C|-1.
    """
    all_indices = list(range(len(gates)))
    basis_matching = _maximum_matching(n, gates, all_indices)
    basis = set(basis_matching)
    unmatched = [i for i in all_indices if i not in basis]
    if not unmatched:
        raise ValueError("output support family is matchable; no Hall-deficient block found")
    e = unmatched[0]

    circuit = {e}
    for f in sorted(basis):
        trial = (basis - {f}) | {e}
        if _matching(n, gates, trial) is not None:
            circuit.add(f)

    ordered = sorted(circuit)
    if _matching(n, gates, ordered) is not None:
        raise AssertionError("fundamental circuit unexpectedly matchable")
    for removed in ordered:
        if _matching(n, gates, [i for i in ordered if i != removed]) is None:
            raise AssertionError("fundamental circuit is not inclusion-minimal")

    neighborhood = core.support_of(gates, ordered)
    if len(ordered) != len(neighborhood) + 1:
        raise AssertionError("minimal transversal circuit must have exact Hall deficiency one")
    return ordered


def avoid_essential_signed_majority(n: int, gates: list[Gate]):
    """V107 avoider with rigorous polynomial Hall-circuit extraction."""
    if len(gates) <= n:
        raise ValueError("range avoidance requires more outputs than inputs")

    block_global = fundamental_hall_circuit(n, gates)
    variables = sorted(core.support_of(gates, block_global))
    remap = {v: i for i, v in enumerate(variables)}
    local_gates = [
        Gate(tuple(remap[v] for v in gates[i].support), gates[i].polarity)
        for i in block_global
    ]
    local_n = len(variables)
    if len(local_gates) != local_n + 1:
        raise AssertionError("Hall circuit must have exact stretch one")

    # Any deletion from a matroid circuit is independent; choose the last gate.
    missing = len(local_gates) - 1
    remaining = list(range(missing))
    selected = core.matroid_intersection_transversal(local_n, local_gates, remaining)
    if len(selected) != local_n or not core.frame_independent(local_n, selected):
        raise AssertionError("failed to construct the Rado frame basis")

    _adjacency, comp_id, components = core._components(local_n, selected)
    if any(cid < 0 for cid in comp_id):
        raise AssertionError("rank-n frame basis must touch every local input")
    for component in components:
        vset, eset = component
        if len(eset) != len(vset):
            raise AssertionError("every rank-tight frame-basis component must be unicyclic")
        core._cycle_core(vset, eset, selected)

    terminals = local_gates[missing].support
    terminal_components = {comp_id[v] for v in terminals}
    if len(terminal_components) > 1:
        local_targets, meta = core._cross_component_target(
            local_n, local_gates, missing, selected, components, comp_id, terminals
        )
    else:
        component = components[next(iter(terminal_components))]
        local_targets, meta = core._kernel_target(
            local_n, local_gates, missing, selected, component, terminals
        )

    local_word = [0 if bit is None else bit for bit in local_targets]
    global_word = [0] * len(gates)
    for local_index, global_index in enumerate(block_global):
        global_word[global_index] = local_word[local_index]
    meta.update({
        "hall_circuit_outputs": len(block_global),
        "hall_circuit_inputs": local_n,
        "frame_basis_components": len(components),
        "surplus_extraction": "transversal_fundamental_circuit",
    })
    return tuple(global_word), meta
