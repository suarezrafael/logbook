from __future__ import annotations

import sys
from collections import defaultdict, deque
from dataclasses import dataclass
from itertools import product
from pathlib import Path

V109_DIR = Path(__file__).resolve().parents[1] / "v109"
V113_DIR = Path(__file__).resolve().parents[1] / "v113"
sys.path.insert(0, str(V109_DIR))
sys.path.insert(0, str(V113_DIR))
from mux_gate_flow import MuxGate  # noqa: E402
from mux_dominator_dp import common_gate_dominator_chain  # noqa: E402


@dataclass(frozen=True)
class CloneBankBudgetOneCertificate:
    selector: int
    first_gate0: int
    first_branch0: int
    first_gate1: int
    first_branch1: int
    common_gates: tuple[int, ...]
    clone_banks: tuple[tuple[int, ...], ...]
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


def _gate_signature(gate: MuxGate) -> tuple[object, ...]:
    return (
        gate.selector,
        gate.data0,
        gate.data1,
        gate.polarity,
        gate.out_flip,
    )


def _clone_bank(
    n: int,
    gates: list[MuxGate],
    stage: tuple[int, ...],
    stage_index: int,
    allowed_stage: set[int],
) -> tuple[int, ...]:
    """Return one exact-clone deletion class exposing a DAG, or raise."""
    if _stage_is_acyclic(n, gates, stage, stage_index, allowed_stage):
        return ()
    groups: dict[tuple[object, ...], list[int]] = defaultdict(list)
    for gi in sorted(allowed_stage):
        groups[_gate_signature(gates[gi])].append(gi)
    for ids in sorted(groups.values(), key=lambda values: (values[0], len(values))):
        bank = set(ids)
        if _stage_is_acyclic(
            n, gates, stage, stage_index, allowed_stage - bank
        ):
            return tuple(ids)
    raise ValueError(
        "non-common dominator stage is neither a DAG nor DAG-after-one-exact-clone-bank"
    )


def _dag_gate_linkage(
    n: int,
    gates: list[MuxGate],
    allowed_gates: set[int],
    requests: list[tuple[int, int]],
) -> list[tuple[tuple[int, int], ...]] | None:
    """Fixed-cardinality gate-disjoint linkage in a DAG by product-state DP."""
    if not requests:
        return []
    if any(not (0 <= x < n) for request in requests for x in request):
        return None

    ordered = tuple(sorted(allowed_gates))
    gate_node = {gi: n + pos for pos, gi in enumerate(ordered)}
    size = n + len(ordered)
    adjacency: list[list[tuple[int, tuple[int, int] | None]]] = [
        [] for _ in range(size)
    ]
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


def _dag_linkage_with_first_alphas(
    n: int,
    gates: list[MuxGate],
    allowed_gates: set[int],
    requests: list[tuple[int, int]],
    first_alphas: dict[int, int],
) -> list[tuple[tuple[int, int], ...]] | None:
    """DAG linkage with phase constraints on at most four first traversals."""
    constrained = sorted(first_alphas)
    choices: list[list[tuple[int, int, int]]] = []
    for request_index in constrained:
        source, _target = requests[request_index]
        desired = first_alphas[request_index]
        options: list[tuple[int, int, int]] = []
        for gi in sorted(allowed_gates):
            gate = gates[gi]
            if gate.selector != source:
                continue
            for branch in (0, 1):
                _s, dest, alpha, _pd = gate.branch(branch)
                if alpha == desired:
                    options.append((gi, branch, dest))
        if not options:
            return None
        choices.append(options)

    if not constrained:
        return _dag_gate_linkage(n, gates, allowed_gates, requests)

    for selected in product(*choices):
        selected_ids = [gi for gi, _branch, _dest in selected]
        if len(set(selected_ids)) != len(selected_ids):
            continue
        adjusted = list(requests)
        prefixes: dict[int, tuple[int, int]] = {}
        for request_index, (gi, branch, dest) in zip(constrained, selected):
            _source, target = adjusted[request_index]
            adjusted[request_index] = (dest, target)
            prefixes[request_index] = (gi, branch)
        tails = _dag_gate_linkage(
            n,
            gates,
            allowed_gates - set(selected_ids),
            adjusted,
        )
        if tails is None:
            continue
        output = list(tails)
        for request_index, prefix in prefixes.items():
            output[request_index] = (prefix,) + output[request_index]
        return output
    return None


_BRANCH_PATTERNS: tuple[tuple[int, ...], ...] = (
    (),
    (0,),
    (1,),
    (0, 1),
    (1, 0),
)


def _clone_special_routes(
    gates: list[MuxGate],
    bank: tuple[int, ...],
    extra: int | None,
    extra_branches: tuple[int, int] | None,
    patterns: tuple[
        tuple[int, ...],
        tuple[int, ...],
        tuple[int, ...],
        tuple[int, ...],
    ],
) -> tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]] | None:
    available = [gi for gi in bank if gi != extra]
    needed = sum(len(pattern) for pattern in patterns)
    if needed > len(available):
        return None
    cursor = 0
    realized: list[list[tuple[int, int]]] = [[], []]
    for route in (0, 1):
        before = patterns[2 * route]
        after = patterns[2 * route + 1]
        for branch in before:
            gi = available[cursor]
            cursor += 1
            realized[route].append((gi, branch))
        if extra is not None:
            assert extra_branches is not None
            realized[route].append((extra, extra_branches[route]))
        for branch in after:
            gi = available[cursor]
            cursor += 1
            realized[route].append((gi, branch))
    return tuple(realized[0]), tuple(realized[1])


def _external_phase(
    gates: list[MuxGate],
    route: int,
    initial_alphas: tuple[int, int],
    next_gate: int | None,
    next_branches: tuple[int, int] | None,
) -> int:
    if next_gate is not None:
        assert next_branches is not None
        return gates[next_gate].branch(next_branches[route])[2]
    return 1 ^ initial_alphas[route]


def _boundary_descriptor(
    gates: list[MuxGate],
    route: int,
    specials: tuple[tuple[int, int], ...],
    segment_slots: list[int | None],
    after_special: int,
    initial_alphas: tuple[int, int],
    next_gate: int | None,
    next_branches: tuple[int, int] | None,
) -> tuple[str, int]:
    segment_index = after_special + 1
    slot = segment_slots[segment_index]
    if slot is not None:
        return ("request", slot)
    next_special = segment_index
    if next_special < len(specials):
        gi, branch = specials[next_special]
        return ("fixed", gates[gi].branch(branch)[2])
    return (
        "fixed",
        _external_phase(
            gates, route, initial_alphas, next_gate, next_branches
        ),
    )


def _compatible_alpha_assignments(
    gates: list[MuxGate],
    shared_gate: int,
    shared_branches: tuple[int, int],
    descriptors: tuple[tuple[str, int], tuple[str, int]],
) -> list[dict[int, int]]:
    answers: list[dict[int, int]] = []
    for alpha0, alpha1 in product((0, 1), repeat=2):
        alphas = (alpha0, alpha1)
        ok = True
        constraints: dict[int, int] = {}
        for route, descriptor in enumerate(descriptors):
            kind, value = descriptor
            if kind == "fixed":
                if alphas[route] != value:
                    ok = False
                    break
            else:
                old = constraints.get(value)
                if old is not None and old != alphas[route]:
                    ok = False
                    break
                constraints[value] = alphas[route]
        if not ok:
            continue
        bit0 = gates[shared_gate].target_for_arrival(
            shared_branches[0], alpha0
        )
        bit1 = gates[shared_gate].target_for_arrival(
            shared_branches[1], alpha1
        )
        if bit0 == bit1:
            answers.append(constraints)
    return answers


def _merge_constraints(
    left: dict[int, int], right: dict[int, int]
) -> dict[int, int] | None:
    output = dict(left)
    for key, value in right.items():
        if key in output and output[key] != value:
            return None
        output[key] = value
    return output


def _realize_plan(
    n: int,
    gates: list[MuxGate],
    allowed_stage: set[int],
    bank: tuple[int, ...],
    starts: tuple[int, int],
    sink: int,
    specials: tuple[
        tuple[tuple[int, int], ...],
        tuple[tuple[int, int], ...],
    ],
    previous_gate: int | None,
    previous_branches: tuple[int, int] | None,
    initial_alphas: tuple[int, int],
    next_gate: int | None,
    next_branches: tuple[int, int] | None,
    extra: int | None,
) -> tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]] | None:
    requests: list[tuple[int, int]] = []
    slots: list[list[int | None]] = [[], []]
    extra_positions: list[int | None] = [None, None]

    for route in (0, 1):
        current = starts[route]
        for pos, (gi, branch) in enumerate(specials[route]):
            selector = gates[gi].selector
            if current == selector:
                slots[route].append(None)
            else:
                slots[route].append(len(requests))
                requests.append((current, selector))
            if gi == extra:
                extra_positions[route] = pos
            current = gates[gi].branch(branch)[1]
        if current == sink:
            slots[route].append(None)
        else:
            slots[route].append(len(requests))
            requests.append((current, sink))

    constraint_sets: list[dict[int, int]] = [{}]
    if previous_gate is not None:
        assert previous_branches is not None
        descriptors = tuple(
            _boundary_descriptor(
                gates,
                route,
                specials[route],
                slots[route],
                -1,
                initial_alphas,
                next_gate,
                next_branches,
            )
            for route in (0, 1)
        )
        constraint_sets = _compatible_alpha_assignments(
            gates, previous_gate, previous_branches, descriptors
        )
        if not constraint_sets:
            return None

    if extra is not None:
        if any(position is None for position in extra_positions):
            return None
        extra_branches = tuple(
            specials[route][extra_positions[route]][1]  # type: ignore[index]
            for route in (0, 1)
        )
        descriptors = tuple(
            _boundary_descriptor(
                gates,
                route,
                specials[route],
                slots[route],
                int(extra_positions[route]),
                initial_alphas,
                next_gate,
                next_branches,
            )
            for route in (0, 1)
        )
        q_constraints = _compatible_alpha_assignments(
            gates, extra, extra_branches, descriptors
        )
        merged: list[dict[int, int]] = []
        for left in constraint_sets:
            for right in q_constraints:
                current = _merge_constraints(left, right)
                if current is not None:
                    merged.append(current)
        constraint_sets = merged
        if not constraint_sets:
            return None

    residual = allowed_stage - set(bank)
    if extra is not None:
        residual.discard(extra)

    for constraints in constraint_sets:
        linkage = _dag_linkage_with_first_alphas(
            n, gates, residual, requests, constraints
        )
        if linkage is None:
            continue
        output: list[tuple[tuple[int, int], ...]] = []
        for route in (0, 1):
            path: list[tuple[int, int]] = []
            for pos, special in enumerate(specials[route]):
                slot = slots[route][pos]
                if slot is not None:
                    path.extend(linkage[slot])
                path.append(special)
            slot = slots[route][-1]
            if slot is not None:
                path.extend(linkage[slot])
            output.append(tuple(path))
        used0 = [gi for gi, _ in output[0]]
        used1 = [gi for gi, _ in output[1]]
        if len(set(used0)) != len(used0) or len(set(used1)) != len(used1):
            continue
        expected = set() if extra is None else {extra}
        if set(used0) & set(used1) != expected:
            continue
        return output[0], output[1]
    return None


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
    bank = _clone_bank(n, gates, stage, stage_index, allowed_stage)
    extras: list[int | None] = [None]
    if allow_extra:
        extras.extend(sorted(allowed_stage))
    answers: dict[
        bool,
        tuple[
            tuple[tuple[int, int], ...],
            tuple[tuple[int, int], ...],
            int | None,
        ],
    ] = {}

    for extra in extras:
        used_budget = extra is not None
        if used_budget in answers:
            continue
        branch_pairs = ((0, 0),) if extra is None else tuple(product((0, 1), repeat=2))
        if not bank:
            pattern_iter = (((), (), (), ()),)
        elif extra is None:
            pattern_iter = tuple(
                (p0, (), p1, ())
                for p0 in _BRANCH_PATTERNS
                for p1 in _BRANCH_PATTERNS
            )
        else:
            pattern_iter = tuple(product(_BRANCH_PATTERNS, repeat=4))
        for extra_branches in branch_pairs:
            for raw_patterns in pattern_iter:
                patterns = tuple(raw_patterns)
                specials = _clone_special_routes(
                    gates,
                    bank,
                    extra,
                    None if extra is None else extra_branches,
                    patterns,
                )
                if specials is None:
                    continue
                realized = _realize_plan(
                    n,
                    gates,
                    allowed_stage,
                    bank,
                    starts,
                    sink,
                    specials,
                    previous_gate,
                    previous_branches,
                    initial_alphas,
                    next_gate,
                    next_branches,
                    extra,
                )
                if realized is None:
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
    tuple[tuple[int, ...], ...],
] | None:
    structure = common_gate_dominator_chain(n, gates, selector, dest0, dest1)
    if structure is None:
        return None
    common, stage, allowed = structure
    noncommon = set(allowed) - set(common)
    stage_sets: list[frozenset[int]] = []
    banks: list[tuple[int, ...]] = []
    try:
        for stage_index in range(len(common) + 1):
            current = frozenset(
                gi
                for gi in noncommon
                if stage[gates[gi].selector] == stage_index
            )
            stage_sets.append(current)
            banks.append(
                _clone_bank(
                    n, gates, stage, stage_index, set(current)
                )
            )
    except ValueError:
        return None
    return common, stage, tuple(stage_sets), tuple(banks)


def fixed_pair_clone_bank_budget_one_certificate(
    n: int,
    gates: list[MuxGate],
    selector: int,
    first_gate0: int,
    first_branch0: int,
    first_gate1: int,
    first_branch1: int,
) -> CloneBankBudgetOneCertificate | None:
    """Decide Delta<=1 when every non-common stage is DAG-after-one clone bank."""
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
            "fixed pair is unreachable or some stage lacks a one-clone-bank DAG deletion"
        )
    common, stage, stage_sets, banks = partition
    initial_alphas = (alpha0, alpha1)
    depth = len(common)

    def finish(
        return0: tuple[tuple[int, int], ...],
        return1: tuple[tuple[int, int], ...],
        extra_gate: int | None,
    ) -> CloneBankBudgetOneCertificate | None:
        target = _target_word(
            gates,
            ((first_gate0, first_branch0),) + return0,
            ((first_gate1, first_branch1),) + return1,
        )
        if target is None:
            return None
        certificate = CloneBankBudgetOneCertificate(
            selector,
            first_gate0,
            first_branch0,
            first_gate1,
            first_branch1,
            common,
            banks,
            extra_gate,
            return0,
            return1,
            target,
        )
        expected = set(common)
        if extra_gate is not None:
            expected.add(extra_gate)
        if set(certificate.overlap) != expected:
            raise AssertionError(
                ("unexpected overlap", certificate.overlap, expected)
            )
        return certificate

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
            certificate = finish(return0, return1, extra)
            if certificate is not None:
                return certificate
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
            if key not in dp:
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
            certificate = finish(prefix0 + path0, prefix1 + path1, extra)
            if certificate is not None:
                return certificate
    return None


def strict_clone_bank_delta_one_family(
    depth: int,
    width: int,
) -> tuple[
    int,
    list[MuxGate],
    tuple[int, int, int, int, tuple[int, ...], tuple[int, ...]],
]:
    """Exact-stretch Delta=1 family with feedback-gate number exactly width."""
    if depth < 0:
        raise ValueError("depth must be nonnegative")
    if width < 2:
        raise ValueError("width must be at least two")

    root, d0, d1, common_selector, left, right, bank_in, bank_out, dead = range(9)
    chain = list(range(9, 9 + depth))
    padding = list(range(9 + depth, 9 + depth + 2 * width - 2))
    del padding
    n = 7 + depth + 2 * width
    gates: list[MuxGate] = []

    first0 = len(gates)
    gates.append(MuxGate(root, d0, dead, (0, 0, 0), 0))
    first1 = len(gates)
    gates.append(MuxGate(root, d1, dead, (1, 0, 0), 0))

    gates.append(
        MuxGate(d0, chain[0] if chain else common_selector, dead)
    )
    for pos, selector in enumerate(chain):
        nxt = chain[pos + 1] if pos + 1 < len(chain) else common_selector
        gates.append(MuxGate(selector, nxt, dead))
    gates.append(MuxGate(d1, common_selector, dead))

    common_gate = len(gates)
    gates.append(MuxGate(common_selector, left, right))
    extra_gate = len(gates)
    gates.append(MuxGate(left, bank_in, dead))
    gates.append(MuxGate(right, root, dead, (1, 0, 0), 0))

    forward: list[int] = []
    for _ in range(width):
        forward.append(len(gates))
        gates.append(MuxGate(bank_in, bank_out, dead))

    gates.append(MuxGate(bank_out, root, dead, (0, 0, 0), 0))

    backward: list[int] = []
    for _ in range(width):
        backward.append(len(gates))
        gates.append(MuxGate(bank_out, root, bank_in, (0, 0, 0), 1))

    if len(gates) != n + 1:
        raise AssertionError(("exact stretch family mismatch", n, len(gates)))
    return n, gates, (
        first0,
        first1,
        common_gate,
        extra_gate,
        tuple(forward),
        tuple(backward),
    )
