# V109 theorem ledger — gate-capacitated MUX flow dichotomy

## Setting

For a signed essential ternary MUX output

```text
g = o XOR MUX(s XOR p_s, a XOR p_a, b XOR p_b),
```

branch `r` supplies an exact fixed-target implication

```text
x_s = alpha_r  ->  x_d = beta_r(target),
```

with opposite selector source phases `alpha_0=p_s` and `alpha_1=1 XOR p_s`.
The output target chooses the arrival phase on the selected branch.  As in V108,
unused branch clauses only strengthen a contradiction.

## Lemma 1 — gate-disjoint opposite-phase double cycles

Suppose two directed branch cycles start at the same selector variable `v`, use
pairwise disjoint output gates, and their first arcs have opposite source phases
`alpha_0 != alpha_1`.

Target each cycle so every selected implication arrives at the source phase of
the next arc, except that the final implication arrives at the complement of the
first source phase.  Cycle `j` then contains

```text
x_v = alpha_j -> x_v = 1 XOR alpha_j,
```

so every satisfying assignment would have to set

```text
x_v = 1 XOR alpha_j.
```

Because the two `alpha_j` are opposite, the two cycles force opposite Boolean
values on `v`.  Their output-gate sets are disjoint, so all targets are compatible.
Hence the fixed-output 2-CNF is unsatisfiable and extends to a missing full output.

The target construction is linear in the two cycle lengths.

## Definition — gate-capacitated return network

Fix a selector `v`, two distinct outputs `g_0,g_1` with selector `v`, and choose
one branch from each so their source phases are opposite.  Let their destinations
be `d_0,d_1`.

Delete every output whose selector is `v` from the return network.  Split every
remaining output gate `h` into `h_in -> h_out` with capacity one.  Variable-to-gate
and gate-to-data arcs have capacity two.  A super-source sends one unit to each
of `d_0,d_1`; the sink is variable `v`.

An integral flow of value two is exactly two return routes that are disjoint in
output gates.  Prepending the two selected first branches gives the cycles of
Lemma 1.

## Lemma 2 — return reachability survives deleting selector-v outputs

If the full branch graph is strongly connected, each destination `d_i` has a
return path to `v` that uses no output whose selector is `v`.

### Proof

Take a simple directed path from `d_i` to `v`.  Before its final vertex it never
visits `v`, so it never traverses an outgoing branch arc whose source/selector is
`v`.

## Theorem 3 — flow-or-one-gate-bottleneck dichotomy

Assume the branch graph is strongly connected.  For the pair above, the maximum
flow in the gate-capacitated return network is either one or two.

- If it is two, Lemma 1 constructs a missing output.
- If it is one, a minimum cut of capacity one consists of a single gate-capacity
  edge.  Therefore one explicit output gate `h` lies on **every** directed return
  path from either `d_0` or `d_1` to `v` after selector-`v` outputs are removed.

### Proof of the cut statement

Lemma 2 gives a path from each source destination to `v`, so the flow value is at
least one.  The super-source has total capacity two, so it is at most two.  If the
value is one, max-flow/min-cut gives a unit cut.  All non-gate internal edges have
capacity two.  A single capacity-one super-source edge cannot separate the sink,
because the other destination independently reaches `v`.  Hence the unit cut is
a gate split edge `h_in -> h_out`.  Removing `h` destroys every source-to-sink
path, so it dominates both return cones.

## Corollary 4 — strongly connected exact-stretch structural alternative

For a MUX circuit with `m>n`, some input is the selector of at least two outputs.
If its branch graph is strongly connected, V109 finds in polynomial time either

1. a gate-disjoint opposite-phase double-cycle missing-output certificate, or
2. a one-output gate bottleneck witnessing the residual obstruction.

The implementation scans repeated-selector gate pairs and opposite-phase branch
choices.  It returns a double cycle whenever one is found; otherwise it returns
an explicit bottleneck.  **The bottleneck alternative is structural progress, not
yet a range-avoidance algorithm.**

## Theorem 5 — strict family beyond the entire V108 hierarchy

For every `k>=2`, use variables

```text
v,
A_1,...,A_k,
B_1,...,B_k,
```

so `n=2k+1`.  Add two central outputs

```text
h_0 = MUX(v,A_1,B_1),
h_1 = MUX(v,A_1,B_1),
```

and, for each lobe `X in {A,B}`, add

```text
MUX(X_i, X_{i+1}, v)       for i<k,
MUX(X_k, v, X_1).
```

There are

```text
m = 2+2k = n+1
```

outputs.

### V109 certificate

Use branch zero of `h_0`, followed by branch-zero gates along the `A` return
lobe.  Its initial source phase is zero.  Use branch one of `h_1`, followed by
branch-zero gates along the `B` lobe.  Its initial source phase is one.  The two
cycles are output-gate-disjoint and therefore satisfy Lemma 1.  The explicit
canonical target is all zeros except the final `A`-lobe output, which is one.

### One strongly connected SCC

With both central outputs present, `v` reaches both lobe entries.  Every lobe
vertex reaches `v` (directly by its second branch for `i<k`, and directly by the
final branch-zero edge for `i=k`).  Hence the full branch graph is strongly
connected.

### No V108 certificate under any ignored-output set

Consider any ignored set and any candidate V108 bridge output that remains.

- If the bridge is a lobe output, it is the unique output whose selector is that
  lobe variable.  V108 removes the bridge before computing SCCs, leaving its
  selector with no outgoing arcs; its left SCC is acyclic.
- If the bridge is `h_0` or `h_1` and the other central output is absent, `v` has
  no outgoing arc and is acyclic.
- If the other central output remains, it points directly from `v` to both
  `A_1` and `B_1`.  For either possible bridge terminal `X_1`, if its unique
  selector output remains then `X_1` has a direct branch back to `v`, so they
  lie in the same SCC.  If that selector output is ignored, `X_1` has no outgoing
  arcs and its SCC is acyclic.

Thus V108 can never obtain two distinct cyclic SCCs, no matter how many outputs
are ignored.  This family is outside the entire `kappa_SCC` certificate hierarchy.

### Hall minimality

Delete one central output: match the other central output to `v` and every lobe
output to its selector.

Delete lobe output `g_j` in lobe `A`: match `h_0` to `v`, `h_1` to `A_1`; if
`j>1`, shift

```text
g_1 -> A_2, ..., g_{j-1} -> A_j,
```

and match all later `A` outputs and all `B` outputs to their selectors.  For
`j=1`, simply match the remaining `A` outputs to their selectors.  The `B`
case is symmetric.  Hence deletion of any one output leaves a perfect support
matching.

### Exact V102 backdoor

If `v` is not in a strong-affine backdoor, every lobe selector must be in it, so
at least `2k` variables are selected.

If `v` is selected, every lobe constraint becomes

```text
X_i in B OR X_{i+1} in B
```

cyclically.  Thus each lobe requires a minimum vertex cover of a `k`-cycle,
namely `ceil(k/2)` variables.  The central gates are already satisfied by `v`.
Therefore

```text
beta_V102 = 1 + 2 ceil(k/2) = Theta(n).
```

For even `k`, `beta=(n+1)/2`; for odd `k`, `beta=(n+3)/2`.

So the same Hall-minimal exact-stretch family has a linear V102 backdoor, no V108
certificate for any deletion budget, yet is solved directly by V109.

## Boundary

V109 does not yet turn the one-gate bottleneck alternative into a polynomial
range-avoidance algorithm.  In particular it does **not** prove all essential
MUX/bijunctive `0x1b` circuits are in P.  The next front is to exploit the
bottleneck gate, either by a compatible shared-gate two-flow or by a provably
shrinking decomposition.  V109 does not solve unrestricted `NC0_3-Avoid`, does
not prove a general circuit lower bound, and does not resolve P versus NP.
