from __future__ import annotations

import sys
from collections import deque
from dataclasses import dataclass
from itertools import combinations, product
from pathlib import Path

V109_DIR = Path(__file__).resolve().parents[1] / "v109"
V113_DIR = Path(__file__).resolve().parents[1] / "v113"
sys.path.insert(0, str(V109_DIR))
sys.path.insert(0, str(V113_DIR))
from mux_gate_flow import MuxGate  # noqa: E402
from mux_dominator_dp import common_gate_dominator_chain  # noqa: E402


@dataclass(frozen=True)
class OneFeedbackBudgetOneCertificate:
    selector: int
    first_gate0: int
    first_branch0: int
    first_gate1: int
    first_branch1: int
    common_gates: tuple[int, ...]
    feedback_gates: tuple[int | None, ...]
    extra_gate: int | None
    return_path0: tuple[tuple[int, int], ...]
    return_path1: tuple[tuple[int, int], ...]
    target: tuple[int, ...]

    @property
    def cycle0(self) -> tuple[tuple[int, int], ...]:
        return ((self.first_gate0, self.first_branch0),) + self.return_path0

    @property
    def cycle1(self) -> tuple[tuple[int, int], ...]:
        return ((self.first_gate1, self.first_branch1),) + self.return_path1

    @property
    def overlap(self) -> tuple[int, ...]:
        a = {gi for gi, _ in self.return_path0}
        b = {gi for gi, _ in self.return_path1}
        return tuple(sorted(a & b))

    @property
    def delta(self) -> int:
        return int(self.extra_gate is not None)


def _valid_instance(n: int, gates: list[MuxGate]) -> bool:
    return n > 0 and all(
        0 <= x < n
        for gate in gates
        for x in (gate.selector, gate.data0, gate.data1)
    )


def _target_word(
    gates: list[MuxGate],
    cycle0: tuple[tuple[int, int], ...],
    cycle1: tuple[tuple[int, int], ...],
) -> tuple[int, ...] | None:
    target = [0] * len(gates)
    assigned: dict[int, int] = {}
    for cycle in (cycle0, cycle1):
        if not cycle:
            return None
        initial_alpha = gates[cycle[0][0]].branch(cycle[0][1])[2]
        for pos, (gi, branch) in enumerate(cycle):
            if pos + 1 < len(cycle):
                next_gi, next_branch = cycle[pos + 1]
                desired = gates[next_gi].branch(next_branch)[2]
            else:
                desired = 1 ^ initial_alpha
            bit = gates[gi].target_for_arrival(branch, desired)
            if gi in assigned and assigned[gi] != bit:
                return None
            assigned[gi] = bit
            target[gi] = bit
    return tuple(target)


def _stage_is_acyclic(
    n: int,
    gates: list[MuxGate],
    stage: tuple[int, ...],
    stage_index: int,
    allowed_stage: set[int],
) -> bool:
    vertices = {v for v in range(n) if stage[v] == stage_index}
    adjacency: dict[int, list[int]] = {v: [] for v in vertices}
    indegree = {v: 0 for v in vertices}
    for gi in allowed_stage:
        gate = gates[gi]
        if gate.selector not in vertices:
            raise AssertionError("stage gate selector has the wrong dominator stage")
        for dest in (gate.data0, gate.data1):
            if dest in vertices:
                adjacency[gate.selector].append(dest)
                indegree[dest] += 1
    queue = deque(v for v in vertices if indegree[v] == 0)
    seen = 0
    while queue:
        u = queue.popleft()
        seen += 1
        for v in adjacency[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    return seen == len(vertices)


def _feedback_gate(
    n: int,
    gates: list[MuxGate],
    stage: tuple[int, ...],
    stage_index: int,
    allowed_stage: set[int],
) -> int | None:
    """Return a one-gate feedback set, or raise if the stage needs >1 gates."""
    if _stage_is_acyclic(n, gates, stage, stage_index, allowed_stage):
        return None
    for gi in sorted(allowed_stage):
        if _stage_is_acyclic(n, gates, stage, stage_index, allowed_stage - {gi}):
            return gi
    raise ValueError("non-common dominator stage has feedback-gate number > 1")


def _dag_gate_linkage(
    n: int,
    gates: list[MuxGate],
    allowed_gates: set[int],
    requests: list[tuple[int, int]],
) -> list[tuple[tuple[int, int], ...]] | None:
    """Fixed-request gate-disjoint linkage in a DAG by a product-state token DP.

    Variable nodes have unlimited capacity. Each output gate is replaced by one
    capacity-one resource node between its selector and the two data destinations.
    Only tokens at minimum topological rank are advanced. Once a capacity-one
    gate node is left, every unfinished token is already at that rank or later,
    so no history set is necessary. V116 uses at most five requests.
    """
    if not requests:
        return []
    if any(not (0 <= x < n) for request in requests for x in request):
        return None

    ordered = tuple(sorted(allowed_gates))
    gate_node = {gi: n + pos for pos, gi in enumerate(ordered)}
    size = n + len(ordered)
    adjacency: list[list[tuple[int, tuple[int, int] | None]]] = [[] for _ in range(size)]
    indegree = [0] * size
    resource = [False] * size

    for gi in ordered:
        node = gate_node[gi]
        resource[node] = True
        gate = gates[gi]
        adjacency[gate.selector].append((node, None))
        indegree[node] += 1
        adjacency[node].append((gate.data0, (gi, 0)))
        adjacency[node].append((gate.data1, (gi, 1)))
        indegree[gate.data0] += 1
        indegree[gate.data1] += 1

    queue = deque(v for v in range(size) if indegree[v] == 0)
    topo: list[int] = []
    while queue:
        u = queue.popleft()
        topo.append(u)
        for v, _tag in adjacency[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    if len(topo) != size:
        return None

    rank = [0] * size
    for pos, vertex in enumerate(topo):
        rank[vertex] = pos

    starts = tuple(source for source, _target in requests)
    targets = tuple(target for _source, target in requests)
    work = deque([starts])
    parent: dict[tuple[int, ...], tuple[int, ...] | None] = {starts: None}
    move: dict[tuple[int, ...], tuple[int, tuple[int, int] | None]] = {}
    final: tuple[int, ...] | None = None

    while work:
        state = work.popleft()
        if state == targets:
            final = state
            break
        active = [
            i
            for i, (vertex, target) in enumerate(zip(state, targets))
            if vertex != target
        ]
        if not active:
            continue
        minimum = min(rank[state[i]] for i in active)
        movers = [i for i in active if rank[state[i]] == minimum]
        for route in movers:
            u = state[route]
            for v, tag in adjacency[u]:
                if resource[v] and any(
                    other != route and state[other] == v
                    for other in range(len(state))
                ):
                    continue
                nxt = list(state)
                nxt[route] = v
                next_state = tuple(nxt)
                if next_state in parent:
                    continue
                parent[next_state] = state
                move[next_state] = (route, tag)
                work.append(next_state)

    if final is None:
        return None

    decoded: list[list[tuple[int, int]]] = [[] for _ in requests]
    steps: list[tuple[int, tuple[int, int] | None]] = []
    state = final
    while parent[state] is not None:
        steps.append(move[state])
        state = parent[state]  # type: ignore[assignment]
    for route, tag in reversed(steps):
        if tag is not None:
            decoded[route].append(tag)
    return [tuple(path) for path in decoded]


def _special_patterns(
    feedback: int | None,
    extra: int | None,
) -> tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]:
    if feedback is None:
        if extra is None:
            return (((), ()),)
        return (((extra,), (extra,)),)
    if extra is None:
        return (((), ()), ((feedback,), ()), ((), (feedback,)))
    if extra == feedback:
        return (((feedback,), (feedback,)),)
    return (
        ((extra,), (extra,)),
        ((feedback, extra), (extra,)),
        ((extra, feedback), (extra,)),
        ((extra,), (feedback, extra)),
        ((extra,), (extra, feedback)),
    )


def _branch_realizations(pattern: tuple[tuple[int, ...], tuple[int, ...]]):
    occurrences = sum(len(sequence) for sequence in pattern)
    for bits in product((0, 1), repeat=occurrences):
        cursor = 0
        realized: list[tuple[tuple[int, int], ...]] = []
        for sequence in pattern:
            current = []
            for gate in sequence:
                current.append((gate, bits[cursor]))
                cursor += 1
            realized.append(tuple(current))
        yield realized[0], realized[1]


def _realize_special_plan(
    n: int,
    gates: list[MuxGate],
    allowed_stage: set[int],
    starts: tuple[int, int],
    sink: int,
    special_routes: tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]],
) -> tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]] | None:
    special = {gi for route in special_routes for gi, _branch in route}
    residual = allowed_stage - special
    requests: list[tuple[int, int]] = []
    slots: list[list[int | None]] = [[], []]

    for route in (0, 1):
        current = starts[route]
        for gi, branch in special_routes[route]:
            target = gates[gi].selector
            if current == target:
                slots[route].append(None)
            else:
                slots[route].append(len(requests))
                requests.append((current, target))
            current = gates[gi].branch(branch)[1]
        if current == sink:
            slots[route].append(None)
        else:
            slots[route].append(len(requests))
            requests.append((current, sink))

    linkage = _dag_gate_linkage(n, gates, residual, requests)
    if linkage is None:
        return None

    output: list[tuple[tuple[int, int], ...]] = []
    for route in (0, 1):
        path: list[tuple[int, int]] = []
        for pos, special_gate in enumerate(special_routes[route]):
            slot = slots[route][pos]
            if slot is not None:
                path.extend(linkage[slot])
            path.append(special_gate)
        slot = slots[route][-1]
        if slot is not None:
            path.extend(linkage[slot])
        output.append(tuple(path))
    return output[0], output[1]


def _desired_after(
    gates: list[MuxGate],
    route: tuple[tuple[int, int], ...],
    pos: int,
    next_gate: int | None,
    next_branch: int | None,
    initial_alpha: int,
) -> int:
    if pos + 1 < len(route):
        gi, branch = route[pos + 1]
        return gates[gi].branch(branch)[2]
    if next_gate is not None:
        assert next_branch is not None
        return gates[next_gate].branch(next_branch)[2]
    return 1 ^ initial_alpha


def _local_compatible(
    gates: list[MuxGate],
    routes: tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]],
    previous_gate: int | None,
    previous_branches: tuple[int, int] | None,
    initial_alphas: tuple[int, int],
    next_gate: int | None,
    next_branches: tuple[int, int] | None,
    extra_gate: int | None,
) -> bool:
    if previous_gate is not None:
        assert previous_branches is not None
        arrival: list[int] = []
        for route in (0, 1):
            if routes[route]:
                gi, branch = routes[route][0]
                desired = gates[gi].branch(branch)[2]
            elif next_gate is not None:
                assert next_branches is not None
                desired = gates[next_gate].branch(next_branches[route])[2]
            else:
                desired = 1 ^ initial_alphas[route]
            arrival.append(
                gates[previous_gate].target_for_arrival(previous_branches[route], desired)
            )
        if arrival[0] != arrival[1]:
            return False

    if extra_gate is not None:
        target_bits: list[int] = []
        for route in (0, 1):
            positions = [
                pos
                for pos, (gi, _branch) in enumerate(routes[route])
                if gi == extra_gate
            ]
            if len(positions) != 1:
                return False
            pos = positions[0]
            _gi, branch = routes[route][pos]
            desired = _desired_after(
                gates,
                routes[route],
                pos,
                next_gate,
                None if next_branches is None else next_branches[route],
                initial_alphas[route],
            )
            target_bits.append(gates[extra_gate].target_for_arrival(branch, desired))
        if target_bits[0] != target_bits[1]:
            return False
    return True


def _local_stage_options(
    n: int,
    gates: list[MuxGate],
    stage: tuple[int, ...],
    stage_index: int,
    allowed_stage: set[int],
    starts: tuple[int, int],
    sink: int,
    initial_alphas: tuple[int, int],
    previous_gate: int | None = None,
    previous_branches: tuple[int, int] | None = None,
    next_gate: int | None = None,
    next_branches: tuple[int, int] | None = None,
    allow_extra: bool = True,
) -> dict[
    bool,
    tuple[
        tuple[tuple[int, int], ...],
        tuple[tuple[int, int], ...],
        int | None,
    ],
]:
    feedback = _feedback_gate(n, gates, stage, stage_index, allowed_stage)
    candidates: list[int | None] = [None]
    if allow_extra:
        candidates.extend(sorted(allowed_stage))

    answers: dict[
        bool,
        tuple[
            tuple[tuple[int, int], ...],
            tuple[tuple[int, int], ...],
            int | None,
        ],
    ] = {}
    for extra in candidates:
        used_budget = extra is not None
        if used_budget in answers:
            continue
        for pattern in _special_patterns(feedback, extra):
            for special_routes in _branch_realizations(pattern):
                realized = _realize_special_plan(
                    n, gates, allowed_stage, starts, sink, special_routes
                )
                if realized is None:
                    continue
                used0 = [gi for gi, _ in realized[0]]
                used1 = [gi for gi, _ in realized[1]]
                if len(set(used0)) != len(used0) or len(set(used1)) != len(used1):
                    continue
                overlap = set(used0) & set(used1)
                expected = set() if extra is None else {extra}
                if overlap != expected:
                    continue
                if not _local_compatible(
                    gates,
                    realized,
                    previous_gate,
                    previous_branches,
                    initial_alphas,
                    next_gate,
                    next_branches,
                    extra,
                ):
                    continue
                answers[used_budget] = (realized[0], realized[1], extra)
                break
            if used_budget in answers:
                break
    return answers


def _stage_partition(
    n: int,
    gates: list[MuxGate],
    selector: int,
    dest0: int,
    dest1: int,
) -> tuple[
    tuple[int, ...],
    tuple[int, ...],
    tuple[frozenset[int], ...],
    tuple[int | None, ...],
] | None:
    structure = common_gate_dominator_chain(n, gates, selector, dest0, dest1)
    if structure is None:
        return None
    common, stage, allowed = structure
    noncommon = set(allowed) - set(common)
    stages: list[frozenset[int]] = []
    feedback: list[int | None] = []
    try:
        for stage_index in range(len(common) + 1):
            current = frozenset(
                gi
                for gi in noncommon
                if stage[gates[gi].selector] == stage_index
            )
            stages.append(current)
            feedback.append(
                _feedback_gate(n, gates, stage, stage_index, set(current))
            )
    except ValueError:
        return None
    return common, stage, tuple(stages), tuple(feedback)


def fixed_pair_one_feedback_budget_one_certificate(
    n: int,
    gates: list[MuxGate],
    selector: int,
    first_gate0: int,
    first_branch0: int,
    first_gate1: int,
    first_branch1: int,
) -> OneFeedbackBudgetOneCertificate | None:
    """Decide Delta<=1 when every non-common stage has feedback-gate number <=1."""
    if not _valid_instance(n, gates):
        raise ValueError("invalid MUX instance")
    if first_gate0 == first_gate1:
        raise ValueError("first output gates must be distinct")
    g0 = gates[first_gate0]
    g1 = gates[first_gate1]
    s0, dest0, alpha0, _ = g0.branch(first_branch0)
    s1, dest1, alpha1, _ = g1.branch(first_branch1)
    if s0 != selector or s1 != selector or alpha0 == alpha1:
        raise ValueError("first arcs must share a selector and have opposite phases")

    partition = _stage_partition(n, gates, selector, dest0, dest1)
    if partition is None:
        raise ValueError(
            "fixed pair is unreachable or some stage has feedback-gate number >1"
        )
    common, stage, stage_sets, feedback = partition
    initial_alphas = (alpha0, alpha1)
    depth = len(common)

    def finish(
        return0: tuple[tuple[int, int], ...],
        return1: tuple[tuple[int, int], ...],
        extra_gate: int | None,
    ) -> OneFeedbackBudgetOneCertificate | None:
        target = _target_word(
            gates,
            ((first_gate0, first_branch0),) + return0,
            ((first_gate1, first_branch1),) + return1,
        )
        if target is None:
            return None
        cert = OneFeedbackBudgetOneCertificate(
            selector,
            first_gate0,
            first_branch0,
            first_gate1,
            first_branch1,
            common,
            feedback,
            extra_gate,
            return0,
            return1,
            target,
        )
        expected = set(common)
        if extra_gate is not None:
            expected.add(extra_gate)
        if set(cert.overlap) != expected:
            raise AssertionError(("unexpected overlap", cert.overlap, expected))
        return cert

    if depth == 0:
        options = _local_stage_options(
            n,
            gates,
            stage,
            0,
            set(stage_sets[0]),
            (dest0, dest1),
            selector,
            initial_alphas,
            allow_extra=True,
        )
        for used_budget in (False, True):
            if used_budget not in options:
                continue
            return0, return1, extra = options[used_budget]
            cert = finish(return0, return1, extra)
            if cert is not None:
                return cert
        return None

    first_common = common[0]
    first_sink = gates[first_common].selector
    dp: dict[
        tuple[tuple[int, int], bool],
        tuple[
            tuple[tuple[int, int], ...],
            tuple[tuple[int, int], ...],
            int | None,
        ],
    ] = {}
    for next_state in product((0, 1), repeat=2):
        options = _local_stage_options(
            n,
            gates,
            stage,
            0,
            set(stage_sets[0]),
            (dest0, dest1),
            first_sink,
            initial_alphas,
            next_gate=first_common,
            next_branches=next_state,
            allow_extra=True,
        )
        for used_budget, (path0, path1, extra) in options.items():
            key = (next_state, used_budget)
            if key in dp:
                continue
            dp[key] = (
                path0 + ((first_common, next_state[0]),),
                path1 + ((first_common, next_state[1]),),
                extra,
            )

    for stage_index in range(depth - 1):
        previous = common[stage_index]
        nxt = common[stage_index + 1]
        sink = gates[nxt].selector
        next_dp: dict[
            tuple[tuple[int, int], bool],
            tuple[
                tuple[tuple[int, int], ...],
                tuple[tuple[int, int], ...],
                int | None,
            ],
        ] = {}
        for (state, used_budget), (
            prefix0,
            prefix1,
            witness_extra,
        ) in sorted(dp.items(), key=lambda item: (item[0][0], item[0][1])):
            starts = (
                gates[previous].branch(state[0])[1],
                gates[previous].branch(state[1])[1],
            )
            for next_state in product((0, 1), repeat=2):
                options = _local_stage_options(
                    n,
                    gates,
                    stage,
                    stage_index + 1,
                    set(stage_sets[stage_index + 1]),
                    starts,
                    sink,
                    initial_alphas,
                    previous_gate=previous,
                    previous_branches=state,
                    next_gate=nxt,
                    next_branches=next_state,
                    allow_extra=not used_budget,
                )
                for local_used, (path0, path1, local_extra) in options.items():
                    if used_budget and local_used:
                        continue
                    total_used = used_budget or local_used
                    key = (next_state, total_used)
                    if key in next_dp:
                        continue
                    next_dp[key] = (
                        prefix0 + path0 + ((nxt, next_state[0]),),
                        prefix1 + path1 + ((nxt, next_state[1]),),
                        witness_extra if used_budget else local_extra,
                    )
        dp = next_dp
        if not dp:
            return None

    last = common[-1]
    for (state, used_budget), (
        prefix0,
        prefix1,
        witness_extra,
    ) in sorted(dp.items(), key=lambda item: (item[0][0], item[0][1])):
        starts = (
            gates[last].branch(state[0])[1],
            gates[last].branch(state[1])[1],
        )
        options = _local_stage_options(
            n,
            gates,
            stage,
            depth,
            set(stage_sets[depth]),
            starts,
            selector,
            initial_alphas,
            previous_gate=last,
            previous_branches=state,
            allow_extra=not used_budget,
        )
        for local_used, (path0, path1, local_extra) in sorted(
            options.items(), key=lambda item: item[0]
        ):
            if used_budget and local_used:
                continue
            extra = witness_extra if used_budget else local_extra
            cert = finish(prefix0 + path0, prefix1 + path1, extra)
            if cert is not None:
                return cert
    return None


def find_one_feedback_budget_one_certificate(
    n: int,
    gates: list[MuxGate],
) -> OneFeedbackBudgetOneCertificate | None:
    if not _valid_instance(n, gates):
        return None
    by_selector: dict[int, list[int]] = {}
    for gi, gate in enumerate(gates):
        by_selector.setdefault(gate.selector, []).append(gi)
    for selector, ids in sorted(by_selector.items()):
        if len(ids) < 2:
            continue
        for g0, g1 in combinations(ids, 2):
            for b0, b1 in product((0, 1), repeat=2):
                if gates[g0].branch(b0)[2] == gates[g1].branch(b1)[2]:
                    continue
                try:
                    cert = fixed_pair_one_feedback_budget_one_certificate(
                        n, gates, selector, g0, b0, g1, b1
                    )
                except ValueError:
                    continue
                if cert is not None:
                    return cert
    return None


def strict_tau_one_delta_one_family(
    depth: int,
) -> tuple[int, list[MuxGate], tuple[int, int, int, int, int]]:
    """Exact-stretch family outside V115 with a relevant one-gate feedback cycle."""
    if depth < 0:
        raise ValueError("depth must be nonnegative")
    root, d0, d1, common_selector, left, right, split, dead = range(8)
    chain = list(range(8, 8 + depth))
    n = 8 + depth
    gates: list[MuxGate] = []

    first0 = len(gates)
    gates.append(MuxGate(root, d0, dead, (0, 0, 0), 0))
    first1 = len(gates)
    gates.append(MuxGate(root, d1, dead, (1, 0, 0), 0))

    gates.append(MuxGate(d0, chain[0] if chain else common_selector, dead))
    for pos, selector in enumerate(chain):
        nxt = chain[pos + 1] if pos + 1 < len(chain) else common_selector
        gates.append(MuxGate(selector, nxt, dead))
    gates.append(MuxGate(d1, common_selector, dead))

    common_gate = len(gates)
    gates.append(MuxGate(common_selector, left, right))
    feedback_extra = len(gates)
    gates.append(MuxGate(left, split, dead))
    gates.append(MuxGate(right, root, dead, (1, 0, 0), 0))
    gates.append(MuxGate(split, root, dead, (0, 0, 0), 0))
    cycle_gate = len(gates)
    # Branch zero is the V115 repair exit. The unused branch one returns to
    # `left`, creating left->split->left. Any gate-simple route taking that
    # branch would have to reuse `feedback_extra`, so the return-route set is unchanged.
    gates.append(MuxGate(split, root, left, (0, 0, 0), 1))

    if len(gates) != n + 1:
        raise AssertionError(("exact stretch family mismatch", n, len(gates)))
    return n, gates, (first0, first1, common_gate, feedback_extra, cycle_gate)
