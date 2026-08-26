from __future__ import annotations

import sys
from dataclasses import dataclass
from itertools import combinations, permutations, product
from pathlib import Path

V109_DIR = Path(__file__).resolve().parents[1] / "v109"
V113_DIR = Path(__file__).resolve().parents[1] / "v113"
V118_DIR = Path(__file__).resolve().parents[1] / "v118"
sys.path.insert(0, str(V109_DIR))
sys.path.insert(0, str(V113_DIR))
sys.path.insert(0, str(V118_DIR))
from mux_gate_flow import MuxGate  # noqa: E402
from mux_dominator_dp import common_gate_dominator_chain  # noqa: E402
import mux_clone_bank as v118  # noqa: E402


@dataclass(frozen=True)
class BranchImageBudgetOneCertificate:
    selector: int
    first_gate0: int
    first_branch0: int
    first_gate1: int
    first_branch1: int
    common_gates: tuple[int, ...]
    image_sets: tuple[tuple[int, ...], ...]
    image_banks: tuple[tuple[int, ...], ...]
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
        left = {gi for gi, _ in self.return_path0}
        right = {gi for gi, _ in self.return_path1}
        return tuple(sorted(left & right))

    @property
    def delta(self) -> int:
        return int(self.extra_gate is not None)


def _branch_image_bank(
    n: int,
    gates: list[MuxGate],
    stage: tuple[int, ...],
    stage_index: int,
    allowed_stage: set[int],
    image_bound: int = 2,
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Find D, |D|<=image_bound, whose full two-branch bank deletion exposes a DAG."""
    if image_bound < 1:
        raise ValueError("image_bound must be positive")
    if v118._stage_is_acyclic(n, gates, stage, stage_index, allowed_stage):
        return (), ()

    destinations = sorted(
        {
            dest
            for gi in allowed_stage
            for dest in (gates[gi].data0, gates[gi].data1)
        }
    )
    for size in range(1, min(image_bound, len(destinations)) + 1):
        for raw_D in combinations(destinations, size):
            D = frozenset(raw_D)
            bank = tuple(
                gi
                for gi in sorted(allowed_stage)
                if gates[gi].data0 in D and gates[gi].data1 in D
            )
            if not bank:
                continue
            if v118._stage_is_acyclic(
                n, gates, stage, stage_index, allowed_stage - set(bank)
            ):
                return tuple(raw_D), bank
    raise ValueError(
        "non-common dominator stage is neither a DAG nor DAG-after-bounded-branch-image-bank"
    )


def _destination_patterns(D: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    patterns: list[tuple[int, ...]] = [()]
    for length in range(1, len(D) + 1):
        patterns.extend(permutations(D, length))
    return tuple(patterns)


def _segment_realizations(
    gates: list[MuxGate],
    bank: tuple[int, ...],
    D: tuple[int, ...],
    excluded_gate: int | None,
) -> tuple[tuple[tuple[int, int], ...], ...]:
    """Enumerate normalized bank traversals: no destination repeats inside the segment."""
    usable = [gi for gi in bank if gi != excluded_gate]
    by_destination: dict[int, list[tuple[int, int]]] = {dest: [] for dest in D}
    for gi in usable:
        for branch in (0, 1):
            dest = gates[gi].branch(branch)[1]
            if dest in by_destination:
                by_destination[dest].append((gi, branch))
    output: list[tuple[tuple[int, int], ...]] = []
    seen: set[tuple[tuple[int, int], ...]] = set()
    for pattern in _destination_patterns(D):
        if not pattern:
            candidate: tuple[tuple[int, int], ...] = ()
            output.append(candidate)
            seen.add(candidate)
            continue
        choices = [by_destination[dest] for dest in pattern]
        if any(not values for values in choices):
            continue
        for selected in product(*choices):
            ids = [gi for gi, _ in selected]
            if len(ids) != len(set(ids)):
                continue
            candidate = tuple(selected)
            if candidate not in seen:
                seen.add(candidate)
                output.append(candidate)
    return tuple(output)


def _route_special_options(
    segment_options: tuple[tuple[tuple[int, int], ...], ...],
    extra: int,
    branch: int,
) -> tuple[tuple[tuple[tuple[int, int], ...], frozenset[int]], ...]:
    """Join before/after segments and prune repeated private bank gates early."""
    output: list[tuple[tuple[tuple[int, int], ...], frozenset[int]]] = []
    for before, after in product(segment_options, repeat=2):
        bank_ids = tuple(gi for gi, _ in before + after)
        used_bank = frozenset(bank_ids)
        if len(used_bank) != len(bank_ids):
            continue
        output.append((before + ((extra, branch),) + after, used_bank))
    return tuple(output)


def _local_stage_options(
    n: int,
    gates: list[MuxGate],
    stage: tuple[int, ...],
    stage_index: int,
    allowed_stage: set[int],
    D: tuple[int, ...],
    bank: tuple[int, ...],
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
    # D and bank are computed once by _stage_partition and reused for every DP state.
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
        segment_options = _segment_realizations(gates, bank, D, extra)
        branch_pairs = ((0, 0),) if extra is None else tuple(product((0, 1), repeat=2))

        for extra_branches in branch_pairs:
            if extra is None:
                for route0, route1 in product(segment_options, repeat=2):
                    used0 = {gi for gi, _ in route0}
                    used1 = {gi for gi, _ in route1}
                    if used0 & used1:
                        continue
                    realized = v118._realize_plan(
                        n,
                        gates,
                        allowed_stage,
                        bank,
                        starts,
                        sink,
                        (route0, route1),
                        previous_gate,
                        previous_branches,
                        initial_alphas,
                        next_gate,
                        next_branches,
                        None,
                    )
                    if realized is not None:
                        answers[False] = (realized[0], realized[1], None)
                        break
            else:
                found = False
                route0_options = _route_special_options(
                    segment_options, extra, extra_branches[0]
                )
                route1_options = _route_special_options(
                    segment_options, extra, extra_branches[1]
                )
                for (specials0, used0), (specials1, used1) in product(
                    route0_options, route1_options
                ):
                    # The designated extra gate is the only allowed non-dominator overlap.
                    if used0 & used1:
                        continue
                    realized = v118._realize_plan(
                        n,
                        gates,
                        allowed_stage,
                        bank,
                        starts,
                        sink,
                        (specials0, specials1),
                        previous_gate,
                        previous_branches,
                        initial_alphas,
                        next_gate,
                        next_branches,
                        extra,
                    )
                    if realized is not None:
                        answers[True] = (realized[0], realized[1], extra)
                        found = True
                        break
                if found:
                    break
    return answers


def _stage_partition(
    n: int,
    gates: list[MuxGate],
    selector: int,
    dest0: int,
    dest1: int,
    image_bound: int = 2,
) -> tuple[
    tuple[int, ...],
    tuple[int, ...],
    tuple[frozenset[int], ...],
    tuple[tuple[int, ...], ...],
    tuple[tuple[int, ...], ...],
] | None:
    structure = common_gate_dominator_chain(n, gates, selector, dest0, dest1)
    if structure is None:
        return None
    common, stage, allowed = structure
    noncommon = set(allowed) - set(common)
    stage_sets: list[frozenset[int]] = []
    image_sets: list[tuple[int, ...]] = []
    banks: list[tuple[int, ...]] = []
    try:
        for stage_index in range(len(common) + 1):
            current = frozenset(
                gi
                for gi in noncommon
                if stage[gates[gi].selector] == stage_index
            )
            D, bank = _branch_image_bank(
                n,
                gates,
                stage,
                stage_index,
                set(current),
                image_bound=image_bound,
            )
            stage_sets.append(current)
            image_sets.append(D)
            banks.append(bank)
    except ValueError:
        return None
    return common, stage, tuple(stage_sets), tuple(image_sets), tuple(banks)


def fixed_pair_branch_image_budget_one_certificate(
    n: int,
    gates: list[MuxGate],
    selector: int,
    first_gate0: int,
    first_branch0: int,
    first_gate1: int,
    first_branch1: int,
    image_bound: int = 2,
) -> BranchImageBudgetOneCertificate | None:
    """Decide Delta<=1 under a bounded branch-image feedback-bank promise."""
    if not v118._valid_instance(n, gates):
        raise ValueError("invalid MUX instance")
    if image_bound < 1:
        raise ValueError("image_bound must be positive")
    if first_gate0 == first_gate1:
        raise ValueError("first output gates must be distinct")

    g0 = gates[first_gate0]
    g1 = gates[first_gate1]
    s0, dest0, alpha0, _ = g0.branch(first_branch0)
    s1, dest1, alpha1, _ = g1.branch(first_branch1)
    if s0 != selector or s1 != selector or alpha0 == alpha1:
        raise ValueError("first arcs must share a selector and have opposite phases")

    partition = _stage_partition(
        n, gates, selector, dest0, dest1, image_bound=image_bound
    )
    if partition is None:
        raise ValueError(
            "fixed pair is unreachable or some stage lacks a bounded branch-image DAG deletion"
        )
    common, stage, stage_sets, image_sets, banks = partition
    initial_alphas = (alpha0, alpha1)
    depth = len(common)

    def finish(
        return0: tuple[tuple[int, int], ...],
        return1: tuple[tuple[int, int], ...],
        extra_gate: int | None,
    ) -> BranchImageBudgetOneCertificate | None:
        target = v118._target_word(
            gates,
            ((first_gate0, first_branch0),) + return0,
            ((first_gate1, first_branch1),) + return1,
        )
        if target is None:
            return None
        certificate = BranchImageBudgetOneCertificate(
            selector,
            first_gate0,
            first_branch0,
            first_gate1,
            first_branch1,
            common,
            image_sets,
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
            raise AssertionError(("unexpected overlap", certificate.overlap, expected))
        return certificate

    if depth == 0:
        options = _local_stage_options(
            n,
            gates,
            stage,
            0,
            set(stage_sets[0]),
            image_sets[0],
            banks[0],
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
            image_sets[0],
            banks[0],
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
                local_stage_index = stage_index + 1
                options = _local_stage_options(
                    n,
                    gates,
                    stage,
                    local_stage_index,
                    set(stage_sets[local_stage_index]),
                    image_sets[local_stage_index],
                    banks[local_stage_index],
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
            image_sets[depth],
            banks[depth],
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


def strict_branch_image_delta_one_family(
    depth: int,
    width: int,
) -> tuple[
    int,
    list[MuxGate],
    tuple[int, int, int, int, tuple[int, ...], tuple[int, ...]],
]:
    """Exact-stretch Delta=1 family outside V118 exact-clone deletion for width>=2."""
    if depth < 0:
        raise ValueError("depth must be nonnegative")
    if width < 2:
        raise ValueError("width must be at least two")

    root, d0, d1, common_selector, left, right, bank_in, bank_out, dead = range(9)
    chain = list(range(9, 9 + depth))
    n = 7 + depth + 2 * width
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
    extra_gate = len(gates)
    gates.append(MuxGate(left, bank_in, dead))
    gates.append(MuxGate(right, root, dead, (1, 0, 0), 0))

    forward: list[int] = []
    for i in range(width):
        forward.append(len(gates))
        gates.append(
            MuxGate(
                bank_in,
                bank_out,
                dead,
                (0, i & 1, (i >> 1) & 1),
                (i >> 2) & 1,
            )
        )

    gates.append(MuxGate(bank_out, root, dead, (0, 0, 0), 0))

    backward: list[int] = []
    for i in range(width):
        backward.append(len(gates))
        gates.append(
            MuxGate(
                bank_out,
                root,
                bank_in,
                (0, i & 1, (i >> 1) & 1),
                1 ^ ((i >> 2) & 1),
            )
        )

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
