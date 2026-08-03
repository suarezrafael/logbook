# Laboratory V85 — support lists, syndrome/girth unification, and remote points

V85 attacks the logarithmic Hall-expander branch isolated by V84. Its first
result is corrective: the proposed theorem that no polynomial list depending
only on supports can work is false. Counting gives a small existential list,
while the constructive problem becomes a structured range-avoidance instance.

## Main results

### 1. Hard-branch completeness

For every fixed logarithmic threshold, unrestricted `NC0_3-Avoid` is
`FP^NP` search-Turing equivalent to its Hall-expander promise restriction. V84
solves the short-girth branch and returns the original circuit in the promised
branch, so no solution translation is needed. This is not a many-one claim.

### 2. Support-only candidate lists

For essential ternary gates, any support-only singleton or pair can be defeated
by selecting local truth tables after the targets are known.

Let `Q` be the total number of truth-table description bits. Counting proves
that a universal ordered list exists whenever

```text
k(m-n) > Q.
```

For unrestricted ternary tables, `Q<=8m`, so

```text
k = floor(8m/(m-n)) + 1
```

suffices. At `m=n+n^(2/3)`, this is `O(n^(1/3))`. The theorem is
nonconstructive.

The exact constructive formulation is `Eval_H`: its input contains all local
truth tables and `k` witnesses, and its output concatenates the `k` circuit
evaluations. A missing output of `Eval_H` is exactly a universal support-only
candidate list.

### 3. Exact ternary predicate census

The 256 ternary Boolean functions split as

```text
16 affine,
184 non-affine unbalanced,
56 balanced non-affine.
```

Every balanced non-affine predicate has normalized correlation exactly `1/2`
with a dictator or a two-variable parity, possibly complemented, and therefore
agrees with it on `3/4` of the cube. This local correlation does not by itself
give a global avoidance certificate at additive stretch `n^(2/3)`.

### 4. Syndrome/C4 theorem

If two distinct gates share at most one input variable, every monomial of
degree at least two belongs to at most one gate. Consequently a constant output
parity can select nonlinear gates only if the incidence graph contains a
four-cycle. On C4-free supports, constant syndromes reduce exactly to affine
subsystems with cancelling linear parts.

A committed seven-output witness shows that before C4 elimination a nonlinear
constant syndrome can solve a selector that is not Hall deficient.

### 5. Source-verified bounded-width remote points

For radius `r`, let `B(m,r)` be the Hamming-ball volume. If

```text
2^n B(m,r) < 2^m,
```

prefix counting of pairs `(x,z)` with `d_H(C(x),z)<=r` constructs a target at
distance greater than `r` from the whole range. At additive stretch
`sigma=m-n`, the elementary bound gives radius

```text
Omega(sigma/log m).
```

V85 now verifies the composition with the actual V75 arithmetic DAG. The V75
circuit represents

```text
P_C(z) = sum_x product_i z_(i,C_i(x)).
```

Evaluate the same DAG over truncated polynomials in `t`:

- on a fixed prefix coordinate, assign weight `1` to agreement and `t` to
  disagreement;
- on a free coordinate, assign `1+t` to both paired variables.

The coefficient of `t^d` is exactly the number of pairs at distance `d`.
Therefore the V75 prefix search lifts to a deterministic remote-point algorithm
without changing the branch decomposition or boundary width. With arithmetic
DAG size `S`, naive truncated convolution gives runtime

```text
O(m S r^2 poly(n+m)).
```

In particular, every regime where the V75 DAG is polynomial-size — including
fixed bounded branchwidth — now has a polynomial-time remote-point algorithm at
distance `Omega((m-n)/log m)`.

## Finite audit

The primary and independent paths check:

- all 256 ternary predicates;
- all four endpoint patterns for essential ternary pair embedding;
- the counting and `Eval_H` dimensions on eight parameter scales;
- 384 C4-free support instances and 866 constant syndromes;
- a symbolic nonlinear C4 witness;
- eight exact oracle-level remote-point controls;
- 12 V75 models with 840 cumulative prefix-pair comparisons and 12 constructed
  radius-one remote points;
- eight independent V75 models with 216 exact distance-coefficient comparisons
  and eight constructed remote points.

Run:

```bash
python3 verify.py
python3 verify_independent.py
```

## Files

- `THEOREMS.md` — completeness, support-list, Fourier, syndrome/C4, and
  remote-point proofs;
- `distance_semiring.py` — source-level V75 truncated-polynomial evaluator;
- `LITERATURE_BOUNDARY.md` — current primary-source boundary and novelty
  cautions;
- `support_lists.py`, `structural.py`, and `v85_core.py` — executable theorem
  kernels;
- `RESULTS.json` — compact immutable claim and audit summary;
- `verify.py` and `verify_independent.py` — registered primary and independent
  checks;
- `V86_CORE_CONTEXT.md` — next laboratory target.

## Nonclaims

V85 does not construct the existential support-only list efficiently, solve the
unrestricted Hall-expander branch, prove locality-three surjectivity hardness,
inherit proof-complexity lower bounds, construct a rigid matrix, prove a new
unrestricted circuit lower bound, or resolve `P` versus `NP`. Novelty and
peer-review status remain unconfirmed.
