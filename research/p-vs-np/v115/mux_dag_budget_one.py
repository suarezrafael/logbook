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
from mux_gate_flow import FlowNetwork, MuxGate  # noqa: E402
from mux_dominator_dp import common_gate_dominator_chain  # noqa: E402


@dataclass(frozen=True)
class DAGBudgetOneCertificate:
    selector: int
    first_gate0: int
    first_branch0: int
    first_gate1: int
    first_branch1: int
    common_gates: tuple[int, ...]
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


def _flow_paths(
    n: int,
    gates: list[MuxGate],
    allowed_gates: set[int],
    starts: tuple[int, int],
    sink: int,
) -> tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]] | None:
    active = [i for i, start in enumerate(starts) if start != sink]
    decoded: dict[int, tuple[tuple[int, int], ...]] = {
        i: () for i, start in enumerate(starts) if start == sink
    }
    if not active:
        return decoded[0], decoded[1]

    ordered = tuple(sorted(allowed_gates))
    gate_pos = {gi: pos for pos, gi in enumerate(ordered)}
    source = n + 2 * len(ordered)
    net = FlowNetwork(source + 1)
    for gi in ordered:
        pos = gate_pos[gi]
        gin = n + 2 * pos
        gout = gin + 1
        gate = gates[gi]
        net.add_edge(gate.selector, gin, 2)
        net.add_edge(gin, gout, 1, ("gate", gi))
        net.add_edge(gout, gate.data0, 2, ("branch", gi, 0))
        net.add_edge(gout, gate.data1, 2, ("branch", gi, 1))
    for route in active:
        net.add_edge(source, starts[route], 1, ("source", route))

    if net.max_flow(source, sink, len(active)) != len(active):
        return None
    raw = net.positive_flow_paths(source, sink, len(active))
    for path in raw:
        tags = [meta for meta in path if meta and meta[0] == "source"]
        if len(tags) != 1:
            raise AssertionError("local flow path lost its source label")
        route = tags[0][1]
        decoded[route] = tuple(
            (meta[1], meta[2])
            for meta in path
            if meta and meta[0] == "branch"
        )
    if set(decoded) != {0, 1}:
        raise AssertionError("local two-flow did not decode both routes")
    return decoded[0], decoded[1]


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


def _first_options(
    gates: list[MuxGate],
    stage: tuple[int, ...],
    stage_index: int,
    allowed_stage: set[int],
    start: int,
    sink: int,
):
    options = []
    for gi in sorted(allowed_stage):
        gate = gates[gi]
        if gate.selector != start:
            continue
        for branch in (0, 1):
            _s, dest, alpha, _pd = gate.branch(branch)
            if dest != sink and stage[dest] != stage_index:
                continue
            options.append((gi, branch, dest, ((gi, branch),), alpha))
    return options


def _ordinary_segment(
    n: int,
    gates: list[MuxGate],
    stage: tuple[int, ...],
    stage_index: int,
    allowed_stage: set[int],
    starts: tuple[int, int],
    sink: int,
    previous_gate: int,
    previous_branches: tuple[int, int],
    initial_alphas: tuple[int, int],
    next_gate: int | None = None,
    next_branches: tuple[int, int] | None = None,
):
    options = []
    for route, start in enumerate(starts):
        if start == sink:
            if next_gate is not None:
                assert next_branches is not None
                desired = gates[next_gate].branch(next_branches[route])[2]
            else:
                desired = 1 ^ initial_alphas[route]
            options.append([(None, None, sink, (), desired)])
            continue
        if stage[start] != stage_index:
            return None
        current = _first_options(
            gates, stage, stage_index, allowed_stage, start, sink
        )
        if not current:
            return None
        options.append(current)

    for first0 in options[0]:
        for first1 in options[1]:
            gi0, _b0, tail0, prefix0, desired0 = first0
            gi1, _b1, tail1, prefix1, desired1 = first1
            if gi0 is not None and gi0 == gi1:
                continue
            target0 = gates[previous_gate].target_for_arrival(
                previous_branches[0], desired0
            )
            target1 = gates[previous_gate].target_for_arrival(
                previous_branches[1], desired1
            )
            if target0 != target1:
                continue
            consumed = {gi for gi in (gi0, gi1) if gi is not None}
            tails = _flow_paths(
                n,
                gates,
                allowed_stage - consumed,
                (tail0, tail1),
                sink,
            )
            if tails is not None:
                return prefix0 + tails[0], prefix1 + tails[1]
    return None


def _prefix_to_extra(
    n: int,
    gates: list[MuxGate],
    stage: tuple[int, ...],
    stage_index: int,
    allowed_stage: set[int],
    starts: tuple[int, int],
    extra_gate: int,
    extra_branches: tuple[int, int],
    previous_gate: int | None,
    previous_branches: tuple[int, int] | None,
):
    extra_selector = gates[extra_gate].selector
    options = []
    for route, start in enumerate(starts):
        if start == extra_selector:
            desired = gates[extra_gate].branch(extra_branches[route])[2]
            options.append([(None, None, extra_selector, (), desired)])
            continue
        if stage[start] != stage_index:
            return None
        current = _first_options(
            gates,
            stage,
            stage_index,
            allowed_stage - {extra_gate},
            start,
            extra_selector,
        )
        if not current:
            return None
        options.append(current)

    for first0 in options[0]:
        for first1 in options[1]:
            gi0, _b0, tail0, prefix0, desired0 = first0
            gi1, _b1, tail1, prefix1, desired1 = first1
            if gi0 is not None and gi0 == gi1:
                continue
            if previous_gate is not None:
                assert previous_branches is not None
                t0 = gates[previous_gate].target_for_arrival(
                    previous_branches[0], desired0
                )
                t1 = gates[previous_gate].target_for_arrival(
                    previous_branches[1], desired1
                )
                if t0 != t1:
                    continue
            consumed = {gi for gi in (gi0, gi1) if gi is not None}
            tails = _flow_paths(
                n,
                gates,
                allowed_stage - {extra_gate} - consumed,
                (tail0, tail1),
                extra_selector,
            )
            if tails is not None:
                return prefix0 + tails[0], prefix1 + tails[1]
    return None


def _suffix_from_extra(
    n: int,
    gates: list[MuxGate],
    stage: tuple[int, ...],
    stage_index: int,
    allowed_stage: set[int],
    sink: int,
    extra_gate: int,
    extra_branches: tuple[int, int],
    initial_alphas: tuple[int, int],
    next_gate: int | None,
    next_branches: tuple[int, int] | None,
):
    options = []
    for route, branch in enumerate(extra_branches):
        dest = gates[extra_gate].branch(branch)[1]
        if dest == sink:
            if next_gate is not None:
                assert next_branches is not None
                desired = gates[next_gate].branch(next_branches[route])[2]
            else:
                desired = 1 ^ initial_alphas[route]
            options.append([(None, None, sink, (), desired)])
            continue
        if stage[dest] != stage_index:
            return None
        current = _first_options(
            gates,
            stage,
            stage_index,
            allowed_stage - {extra_gate},
            dest,
            sink,
        )
        if not current:
            return None
        options.append(current)

    for first0 in options[0]:
        for first1 in options[1]:
            gi0, _b0, tail0, prefix0, desired0 = first0
            gi1, _b1, tail1, prefix1, desired1 = first1
            if gi0 is not None and gi0 == gi1:
                continue
            t0 = gates[extra_gate].target_for_arrival(
                extra_branches[0], desired0
            )
            t1 = gates[extra_gate].target_for_arrival(
                extra_branches[1], desired1
            )
            if t0 != t1:
                continue
            consumed = {gi for gi in (gi0, gi1) if gi is not None}
            tails = _flow_paths(
                n,
                gates,
                allowed_stage - {extra_gate} - consumed,
                (tail0, tail1),
                sink,
            )
            if tails is not None:
                return prefix0 + tails[0], prefix1 + tails[1]
    return None


def _one_extra_dag_segment(
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
):
    if not _stage_is_acyclic(n, gates, stage, stage_index, allowed_stage):
        raise ValueError("one-extra separation requires an acyclic stage")

    for extra_gate in sorted(allowed_stage):
        for extra_branches in product((0, 1), repeat=2):
            prefix = _prefix_to_extra(
                n,
                gates,
                stage,
                stage_index,
                allowed_stage,
                starts,
                extra_gate,
                extra_branches,
                previous_gate,
                previous_branches,
            )
            if prefix is None:
                continue
            suffix = _suffix_from_extra(
                n,
                gates,
                stage,
                stage_index,
                allowed_stage,
                sink,
                extra_gate,
                extra_branches,
                initial_alphas,
                next_gate,
                next_branches,
            )
            if suffix is None:
                continue
            path0 = prefix[0] + ((extra_gate, extra_branches[0]),) + suffix[0]
            path1 = prefix[1] + ((extra_gate, extra_branches[1]),) + suffix[1]
            used0 = {gi for gi, _ in path0}
            used1 = {gi for gi, _ in path1}
            if len(used0) != len(path0) or len(used1) != len(path1):
                raise AssertionError("DAG prefix/suffix factorization repeated a gate")
            if used0 & used1 != {extra_gate}:
                raise AssertionError(
                    "acyclic stage allowed cross-overlap around the unique extra gate"
                )
            return path0, path1, extra_gate
    return None


def _stage_partition(
    n: int,
    gates: list[MuxGate],
    selector: int,
    dest0: int,
    dest1: int,
):
    structure = common_gate_dominator_chain(n, gates, selector, dest0, dest1)
    if structure is None:
        return None
    common, stage, allowed = structure
    noncommon = set(allowed) - set(common)
    stages = tuple(
        frozenset(
            gi
            for gi in noncommon
            if stage[gates[gi].selector] == stage_index
        )
        for stage_index in range(len(common) + 1)
    )
    if not all(
        _stage_is_acyclic(n, gates, stage, j, set(stages[j]))
        for j in range(len(stages))
    ):
        return None
    return common, stage, stages


def fixed_pair_dag_budget_one_certificate(
    n: int,
    gates: list[MuxGate],
    selector: int,
    first_gate0: int,
    first_branch0: int,
    first_gate1: int,
    first_branch1: int,
) -> DAGBudgetOneCertificate | None:
    """Decide overlap <= minOverlap+1 for the all-DAG-stage fixed-pair class.

    Raises ValueError when the prescribed pair is malformed, unreachable, or its
    non-common dominator stages are not all acyclic.  Within the stated class,
    None is a genuine negative answer for budget one.
    """
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
        raise ValueError("fixed pair is unreachable or has a cyclic non-common stage")
    common, stage, stage_sets = partition
    d = len(common)
    initial_alphas = (alpha0, alpha1)

    def finish(return0, return1, extra_gate):
        target = _target_word(
            gates,
            ((first_gate0, first_branch0),) + return0,
            ((first_gate1, first_branch1),) + return1,
        )
        if target is None:
            return None
        cert = DAGBudgetOneCertificate(
            selector,
            first_gate0,
            first_branch0,
            first_gate1,
            first_branch1,
            common,
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

    if d == 0:
        ordinary = _flow_paths(
            n, gates, set(stage_sets[0]), (dest0, dest1), selector
        )
        if ordinary is not None:
            cert = finish(ordinary[0], ordinary[1], None)
            if cert is not None:
                return cert
        extra = _one_extra_dag_segment(
            n,
            gates,
            stage,
            0,
            set(stage_sets[0]),
            (dest0, dest1),
            selector,
            initial_alphas,
        )
        if extra is None:
            return None
        return finish(extra[0], extra[1], extra[2])

    first_common = common[0]
    first_sink = gates[first_common].selector
    # Key = (branch pair at current common gate, extra gate already used).
    dp: dict[
        tuple[tuple[int, int], int | None],
        tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]],
    ] = {}

    ordinary = _flow_paths(
        n, gates, set(stage_sets[0]), (dest0, dest1), first_sink
    )
    if ordinary is not None:
        for next_state in product((0, 1), repeat=2):
            dp[(next_state, None)] = (
                ordinary[0] + ((first_common, next_state[0]),),
                ordinary[1] + ((first_common, next_state[1]),),
            )

    for next_state in product((0, 1), repeat=2):
        extra = _one_extra_dag_segment(
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
        )
        if extra is not None:
            dp[(next_state, extra[2])] = (
                extra[0] + ((first_common, next_state[0]),),
                extra[1] + ((first_common, next_state[1]),),
            )

    for j in range(d - 1):
        previous = common[j]
        nxt = common[j + 1]
        sink = gates[nxt].selector
        new_dp = {}
        for (state, used_extra), prefixes in sorted(
            dp.items(), key=lambda item: (item[0][0], -1 if item[0][1] is None else item[0][1])
        ):
            starts = (
                gates[previous].branch(state[0])[1],
                gates[previous].branch(state[1])[1],
            )
            for next_state in product((0, 1), repeat=2):
                segment = _ordinary_segment(
                    n,
                    gates,
                    stage,
                    j + 1,
                    set(stage_sets[j + 1]),
                    starts,
                    sink,
                    previous,
                    state,
                    initial_alphas,
                    nxt,
                    next_state,
                )
                key = (next_state, used_extra)
                if segment is not None and key not in new_dp:
                    new_dp[key] = (
                        prefixes[0] + segment[0] + ((nxt, next_state[0]),),
                        prefixes[1] + segment[1] + ((nxt, next_state[1]),),
                    )
                if used_extra is not None:
                    continue
                extra = _one_extra_dag_segment(
                    n,
                    gates,
                    stage,
                    j + 1,
                    set(stage_sets[j + 1]),
                    starts,
                    sink,
                    initial_alphas,
                    previous,
                    state,
                    nxt,
                    next_state,
                )
                if extra is None:
                    continue
                key = (next_state, extra[2])
                if key not in new_dp:
                    new_dp[key] = (
                        prefixes[0] + extra[0] + ((nxt, next_state[0]),),
                        prefixes[1] + extra[1] + ((nxt, next_state[1]),),
                    )
        dp = new_dp
        if not dp:
            return None

    last = common[-1]
    for (state, used_extra), prefixes in sorted(
        dp.items(), key=lambda item: (item[0][0], -1 if item[0][1] is None else item[0][1])
    ):
        starts = (
            gates[last].branch(state[0])[1],
            gates[last].branch(state[1])[1],
        )
        segment = _ordinary_segment(
            n,
            gates,
            stage,
            d,
            set(stage_sets[d]),
            starts,
            selector,
            last,
            state,
            initial_alphas,
        )
        if segment is not None:
            cert = finish(
                prefixes[0] + segment[0],
                prefixes[1] + segment[1],
                used_extra,
            )
            if cert is not None:
                return cert
        if used_extra is not None:
            continue
        extra = _one_extra_dag_segment(
            n,
            gates,
            stage,
            d,
            set(stage_sets[d]),
            starts,
            selector,
            initial_alphas,
            last,
            state,
        )
        if extra is not None:
            cert = finish(
                prefixes[0] + extra[0],
                prefixes[1] + extra[1],
                extra[2],
            )
            if cert is not None:
                return cert
    return None


def find_dag_budget_one_certificate(
    n: int,
    gates: list[MuxGate],
) -> DAGBudgetOneCertificate | None:
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
                    cert = fixed_pair_dag_budget_one_certificate(
                        n, gates, selector, g0, b0, g1, b1
                    )
                except ValueError:
                    continue
                if cert is not None:
                    return cert
    return None


def strict_dag_delta_one_family(
    depth: int,
) -> tuple[int, list[MuxGate], tuple[int, int, int, int]]:
    """Exact-stretch family rejected at Delta=0 and accepted at Delta=1."""
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
    for j, selector in enumerate(chain):
        nxt = chain[j + 1] if j + 1 < len(chain) else common_selector
        gates.append(MuxGate(selector, nxt, dead))
    gates.append(MuxGate(d1, common_selector, dead))

    common_gate = len(gates)
    gates.append(MuxGate(common_selector, left, right))
    extra_gate = len(gates)
    gates.append(MuxGate(left, split, dead))
    # Only branch zero returns, and its source phase is one.  Hence every
    # minimum-overlap left/right pair conflicts on the common gate.
    gates.append(MuxGate(right, root, dead, (1, 0, 0), 0))
    # Two semantically distinct exits let the Delta=1 pair share the left gate
    # and then separate without another shared output.
    gates.append(MuxGate(split, root, dead, (0, 0, 0), 0))
    gates.append(MuxGate(split, root, dead, (0, 0, 0), 1))

    if len(gates) != n + 1:
        raise AssertionError(("exact stretch family mismatch", n, len(gates)))
    return n, gates, (first0, first1, common_gate, extra_gate)
