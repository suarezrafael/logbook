# V111 theorem ledger — target-compatible minimum-overlap MUX flows

## Setting

For a signed essential ternary MUX gate

```text
g = o XOR MUX(s XOR p_s, a XOR p_a, b XOR p_b),
```

fixing its output gives two exact binary clauses.  Selecting branch `r` yields an implication

```text
x_s = alpha_r  ->  x_d = beta_r(target),
```

where the target bit chooses the arrival phase.

V109 used two return routes that were disjoint in output gates.  V110 allowed exactly one shared output gate provided both routes required the same target bit on it.  V111 removes the constant-overlap restriction.

## Lemma 1 — arbitrary target-compatible overlap is sound

Let two directed branch cycles start at the same selector `v`, with opposite first source phases.  Output gates may occur in both cycles.  Suppose that whenever an output gate occurs in both cycles, the target bit required by the first cycle equals the target bit required by the second cycle.

Then the union of the two target assignments extends to a full output word outside the circuit range.

### Proof

On each cycle choose each selected MUX target so that the selected implication arrives at the source phase of the next branch, except the last implication, which arrives at the complement of the first source phase.  A cycle beginning with phase `alpha` therefore contains

```text
x_v = alpha  ->  x_v = 1 XOR alpha,
```

so any satisfying assignment must set `x_v=1 XOR alpha`.  The two initial phases are opposite, hence the cycles force opposite values of `x_v`.

The only possible conflict while combining the two target assignments is an output gate used by both cycles.  The hypothesis says that every such target requirement agrees.  Therefore all selected clauses coexist in one fixed-output 2-CNF and are already contradictory.  The unselected clause of every fixed MUX gate can only strengthen that formula.  Arbitrary targets on unused outputs extend the partial target to a full missing word.

## Definition 2 — minimum-overlap return flow

Fix two distinct outputs with common selector `v` and choose first branches with opposite source phases.  Let their destinations be `d_0,d_1`.  Remove outputs whose selector is `v` from the return network.

For every remaining output gate `h`, split it into `h_in -> h_out` using two parallel capacity-one arcs:

```text
first unit:  cost 0
second unit: cost 1
```

All variable-to-gate and gate-to-data arcs have capacity two and cost zero.  A super-source sends one unit to each `d_i`; the sink is `v`.

For an integral two-flow, the total cost is exactly the number of output gates used by both decomposed source-to-sink routes.

## Lemma 3 — polynomial minimum-overlap computation

A minimum-cost integral two-flow in the network above is computable in polynomial time by successive shortest augmenting paths in the residual network.  Only two augmentations are needed.  Residual reverse arcs may have negative cost, so the reference implementation uses Bellman-Ford/SPFA rather than a nonnegative-cost Dijkstra assumption.

The resulting integral flow decomposes into two source-labeled return routes.  The implementation checks that the flow cost equals the number of shared output gates in the decoded routes.

## Theorem 4 — recognizable target-compatible min-overlap class is in P

There is a deterministic polynomial-time procedure that scans repeated selectors and opposite-phase first-branch choices, computes the deterministic minimum-overlap two-flow above, and, whenever its decoded routes are target-compatible on every shared output gate, constructs a missing output word.

### Important completeness boundary

The procedure is a sound recognizer for this class.  It does **not** prove that, whenever some target-compatible pair of return routes exists, the particular deterministic minimum-cost decomposition chosen by the implementation will find one.  Nor does it search exponentially over all equal-cost flow decompositions.

## Theorem 5 — unbounded nested-bottleneck family

For every integer `d>=1`, set `k=2` in `strict_nested_chain_family`.  The construction has `d+1` two-lobe layers separated by `d` shared hub MUX gates.

Its exact size is

```text
n = 5(d+1),
m = n+1.
```

The two central outputs have distinct supports.  Every non-hub input is selector of one output; each internal hub is selector of exactly one shared output.

### Minimum overlap is exactly d

Every return route from either central branch destination to the root selector must cross each of the `d` hub layers.  The only output whose selector is a hub and leaves that hub is the corresponding shared MUX output.  Hence both return routes must use every shared gate, so every two-flow has overlap cost at least `d`.

The canonical left and right routes use disjoint lobe outputs and share exactly the `d` hub gates.  Therefore

```text
minimum overlap cost = d.
```

At shared gate `j`, the left route uses branch zero and the right route uses branch one.  The canonical phase propagation makes both traversals require the same fixed output target.  Thus Lemma 1 applies for every `d`.

### Separation from V109 and V110

V109 gives a one-gate bottleneck at the first shared hub instead of a gate-disjoint double cycle.

For `d=1`, V110 raises that gate to capacity two and succeeds.  For every `d>=2`, after the first shared gate is upgraded, the next shared hub remains a unit-capacity bottleneck.  Thus the V110 procedure returns its `NestedBottleneck` alternative, while V111 crosses all `d` shared gates in one polynomial min-cost computation.

This is an unbounded structural separation: the number of shared bottlenecks can grow linearly with the instance size, yet V111 remains polynomial on the family.

## Theorem 6 — exact V102 backdoor on the k=2 chain

For the depth-`d` family,

```text
beta_V102 = 3(d+1) = 3n/5.
```

### Proof

Each layer contains two two-variable lobes and exits through one hub variable `z` (the root selector is the exit hub for the final layer).  For one lobe with variables `x_0,x_1`, the V102 MUX backdoor constraints reduce to

```text
x_0 in B OR (x_1 in B AND z in B),
x_1 in B OR (z in B AND x_0 in B).
```

If `z` is selected, at least one of `x_0,x_1` is necessary and sufficient.  If `z` is not selected, both are forced.  Therefore the two lobes of a layer cost at least two selected lobe variables when its exit hub is selected, and at least four otherwise.

Summing the two-lobe cost plus the `(d+1)` exit-hub variables gives

```text
sum_j (4 - 2 z_j) + sum_j z_j
 = 4(d+1) - sum_j z_j
 >= 3(d+1).
```

For the matching upper bound, select all `d+1` hubs and one variable from each of the `2(d+1)` lobes.  Every local MUX backdoor constraint is satisfied, including the central and shared hub gates.  Hence equality holds.

Consequently the V102 branch count is exponential, `2^(3n/5)`, on a family handled polynomially by V111.

## Hall and V108 audits

The support family has positive stretch exactly one.  The primary verifier checks that deleting any one output leaves a perfect support matching through depth 20; the independent verifier repeats the audit through depth 40.  The first two depths are also exhaustively checked against every ignored-output set of the V108 SCC-bridge recognizer and expose no V108 certificate.

These finite audits are deliberately not promoted into an unproved all-depth V108-separation theorem.

## Boundary

V111 does not prove that all phase-conflict or nested-bottleneck MUX instances are solvable.  It does not provide a complete polynomial algorithm for finding a target-compatible pair among all possible equal-cost or higher-cost flow decompositions.  It therefore does not prove all essential MUX/bijunctive `0x1b` circuits are in P, does not solve unrestricted `NC0_3-Avoid`, does not establish a new general circuit lower bound, and does not resolve P versus NP.
