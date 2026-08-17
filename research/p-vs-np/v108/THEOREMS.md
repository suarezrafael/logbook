# V108 theorem ledger — MUX SCC-cycle bridge

## Setting

A signed essential ternary MUX gate is written

```text
g = o XOR MUX(s XOR p_s, a XOR p_a, b XOR p_b),
```

where `MUX(z,A,B)=A` for `z=0` and `B` for `z=1`.

Fixing an output target exposes exactly two binary clauses.  For branch `r in {0,1}` the corresponding implication has the form

```text
x_s = alpha_r  ->  x_d = beta_r(target),
```

where

```text
alpha_0 = p_s,
alpha_1 = 1 XOR p_s.
```

For either branch, choosing the gate target lets us choose the arrival phase on its data variable arbitrarily.  The unused branch clause is an additional constraint and therefore cannot repair a contradiction built from the selected branch clauses.

## Lemma 1 — directed-cycle forcing

Let selected branch arcs from pairwise distinct MUX outputs form a directed simple cycle

```text
v_0 -> v_1 -> ... -> v_{q-1} -> v_0.
```

Let `alpha_i` be the source phase of the selected branch leaving `v_i`.
Choose the target of gate `i` so its selected implication arrives at phase `alpha_{i+1}`, except for the final arc, which arrives at `1 XOR alpha_0`.

Then the fixed-output 2-CNF contains

```text
x_{v_0}=alpha_0 -> ... -> x_{v_0}=1 XOR alpha_0.
```

Hence every satisfying assignment is forced to satisfy

```text
x_{v_0}=1 XOR alpha_0.
```

The target choices are constructive and linear in the cycle length.

## Definition — SCC-separated bridge certificate

Omit one output gate `h`.  Build the directed branch graph from both branch arcs of every remaining MUX output.

An SCC-separated bridge certificate consists of:

1. a directed cycle in a cyclic SCC `L` through the selector `s_h` of `h`;
2. the selector value forced by that cycle;
3. the unique branch of `h` activated by that forced selector value;
4. the data variable reached by that branch lying in a **different** cyclic SCC `R`; and
5. a directed cycle in `R` through that data variable.

The two cycles use disjoint output gates because every branch of one MUX output has the same selector/source variable and distinct SCCs have disjoint source vertices.

## Theorem 2 — SCC-separated MUX avoidance

If an essential signed-MUX circuit contains an SCC-separated bridge certificate, a missing output word can be constructed deterministically in polynomial time.

### Proof

Use Lemma 1 on the left cycle.  If its first selected source phase is `alpha_L`, the selector of the omitted bridge gate is forced to `1 XOR alpha_L`.  This activates exactly one branch of the bridge gate.

Let `alpha_R` be the first selected source phase on the right cycle.  Target the right cycle as in Lemma 1, so the right data variable is forced to `1 XOR alpha_R`.  Now choose the bridge output target so its active branch forces that same variable to `alpha_R`.

The resulting fixed-output 2-CNF forces both Boolean values on the right data variable, hence is unsatisfiable.  Every clause used is an exact clause of the corresponding fixed MUX output; unused branch clauses only strengthen the formula.  Fill all other output coordinates arbitrarily.

SCC decomposition and cycle reconstruction are polynomial.

## Definition — deletion distance `kappa_SCC`

Let `kappa_SCC(C)` be the minimum number of output gates that can be ignored so that the remaining output family contains an SCC-separated bridge certificate.

Ignored outputs are safe because an impossible target on a subfamily extends to an impossible full output after arbitrary filling of the ignored coordinates.

## Theorem 3 — constant-distance hierarchy

Given a bound `k`, enumerate every set of at most `k` ignored outputs and run Theorem 2 on the remaining family.  The runtime is

```text
O(m^k poly(N)).
```

Thus every fixed-constant `kappa_SCC` class is polynomial-time range avoidable.  This is an XP parameterization; no FPT dependence `f(k) poly(N)` is claimed.

## Theorem 4 — strict infinite separation from V102

For every `k>=3`, let the input variables be two disjoint cycles

```text
L_0,...,L_{k-1}, R_0,...,R_{k-1}.
```

On each cycle add the `k` canonical MUX outputs

```text
MUX(X_i, X_{i+1}, X_{i+2})
```

(indices modulo `k`), and add the bridge

```text
MUX(L_0, L_2, R_0).
```

Then

```text
n = 2k,
m = 2k+1 = n+1,
kappa_SCC = 0.
```

### SCC certificate

After omitting the bridge, branch-0 arcs give the two directed cycles

```text
L_i -> L_{i+1},
R_i -> R_{i+1}.
```

They are distinct cyclic SCCs.  The left cycle can be targeted to force `L_0=1`, activating bridge branch 1 toward `R_0`; the right cycle can be targeted to force `R_0=1`, while the bridge is targeted to force `R_0=0`.

### Hall minimality

The support family has exact positive surplus one and is Hall-minimal.

- If the bridge is deleted, match every cycle gate to its selector.
- If left gate `g_j` is deleted, match the bridge to `L_0`.  If `j=0`, match every remaining left gate to its selector.  If `j>0`, match

```text
g_0 -> L_1, g_1 -> L_2, ..., g_{j-1} -> L_j,
```

and every later left gate to its selector.  Match all right gates to their selectors.
- The right-gate deletion case is symmetric, using the bridge-to-`R_0` matching.

Thus deletion of any one output leaves a perfect support matching.

### Exact V102 backdoor for `k` divisible by three

For one cycle, the V102 local rule is

```text
X_i in B  OR  (X_{i+1} in B AND X_{i+2} in B).
```

Therefore every zero in the cyclic membership word must be followed by two ones.  At most `k/3` positions can be zero when `3|k`, so every cycle contributes at least `2k/3` backdoor variables.

This lower bound is attained by placing zeros every third position while choosing the phase so `L_0` belongs to the backdoor; then the bridge condition is already satisfied.  Hence

```text
beta_V102 = 4k/3 = 2n/3.
```

Consequently this family has linear V102 backdoor but `kappa_SCC=0` and is solved by V108 in polynomial time.

## Boundary

V108 does **not** prove polynomial-time avoidance for all essential MUX/bijunctive `0x1b` circuits.  In particular, instances whose relevant branch cycles remain trapped in one cyclic SCC are not covered by Theorem 2.  V108 does not solve unrestricted `NC0_3-Avoid`, does not imply a new general circuit lower bound, and does not resolve P versus NP.
