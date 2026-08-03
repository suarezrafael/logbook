# Laboratory V87 — linear branchwidth from a random-pair shadow

V87 completes the three-certificate obstruction program started in V86.

The target distribution is unchanged:

```text
m = n + ceil(n^(2/3))
```

supports are sampled independently and uniformly from the 3-subsets of `[n]`,
and the final family is required to have no repeated support.

## Main correction

The proposed direct proof by McDiarmid plus a union bound over every balanced
gate cut does not close.

Replacing one support changes

```text
lambda_H(S) = |N(S) intersect N(M\S)|
```

by at most six. Even granting the impossible best deviation `t=n`,
McDiarmid supplies exponent at most

```text
2 n^2 / (36 m) = (1/18 + o(1)) n.
```

The number of gate subsets of size `m/3` has exponential rate

```text
H(1/3) m = (0.6365... + o(1)) n.
```

Thus this concentration inequality is too weak by more than an order of
magnitude in the exponent. V87 records this as a no-go rather than hiding the
constant failure.

## Random-pair shadow

For every random support `{a,b,c}`, independently select one of its three
pairs uniformly.

Each selected pair is an independent uniform element of `binom([n],2)`.
The first `floor(3n/4)` selected pairs therefore form the ordinary sparse
random-graph process at edge density `3n/4`, up to `O_p(1)` repeated pairs.

This process is supercritical. The theorem of Lee, Lee, and Oum implies that
its simple underlying graph has treewidth `Omega(n)` asymptotically almost
surely.

The selected graph is a subgraph of the primal graph of the support
hypergraph.

## Rank-three transfer lemma

For every rank-at-most-three hypergraph `H`,

```text
tw(primal(H)) + 1 <= max(3, ceil(3 bw(H) / 2)).
```

The proof constructs a tree decomposition from any branch decomposition.
At an internal node, use the vertices incident with hyperedges in at least
two of the three incident branches. Such a vertex is counted in at least two
of the three branch boundaries, so the bag has size at most `3k/2` when the
branch decomposition has width `k`.

Consequently, linear treewidth of the pair shadow forces

```text
bw(H) = Omega(n).
```

## Three-certificate obstruction theorem

V86 already proved that the same random support model has, with probability
bounded away from zero:

1. no Hall-deficient gate set of size at most `n/(16e^2)`;
2. no repeated support.

V87 proves that linear support branchwidth holds with probability tending to
one. The three events therefore intersect with positive probability for all
sufficiently large `n`.

Assigning `NOR3` to every support then gives one family satisfying
simultaneously:

```text
linear-scale local Hall expansion;
no nonzero constant output-parity syndrome;
support branchwidth Omega(n).
```

This is an existence theorem. It is not an explicit deterministic
construction.

## Fixed-cut calibration

For a fixed gate set `S` of size `s`, the exact expectation is

```text
E lambda_H(S)
 = n [1 - (1-3/n)^s - (1-3/n)^(m-s) + (1-3/n)^m].
```

At `s/m -> 1/3` and `m/n -> 1`, the limit is

```text
1 - e^(-1) - e^(-2) + e^(-3)
= 0.546572... .
```

The heuristic `0.63 + 0.86 - 1 = 0.49` subtracts all `n` variables instead
of the active set and omits the unused-vertex term `e^(-3)`.

This is the expectation of one fixed cut. It is not a lower bound for the
minimum over exponentially many balanced cuts.

## Finite audit

The executable census includes:

- exact pair-shadow uniformity on all triples over six variables;
- `837` rank-three transfer cases on five variables;
- exact minimum balanced connectivity of the three V80 controls;
- `17,601,500` balanced cuts across eight deterministic random samples;
- the fixed-cut expectation correction;
- the McDiarmid exponent comparison.

The finite samples have minimum balanced-connectivity ratios between
`0.3125` and `0.5`. They support linear scaling but do not establish the
asymptotic theorem; the theorem comes from the random-graph shadow.

## Strategic consequence

The V85 `O(sqrt(log m))` algorithm remains valuable for low-width instances,
but no sublinear-width extension can solve the V87 obstruction family through
that mechanism. This closes width optimization as a route against this
specific resistant family.

It does not prove that every instance in the V84 Hall-expander promise branch
has linear width.

## Files

- `LINEAR_BRANCHWIDTH_THEOREM.md` — formal theorem packet;
- `LITERATURE_BOUNDARY.md` — external theorem boundary and nonnovelty audit;
- `linear_branchwidth.py` — exact finite census;
- `RESULTS.json` — committed evidence;
- `verify.py` and `verify_independent.py` — independent verification paths;
- `V88_CORE_CONTEXT.md` — next laboratory priorities.

## Nonclaims

V87 does not give an explicit deterministic obstruction family, construct the
V85 support-only list, solve `Eval_H`, solve unrestricted `NC0_3-Avoid`,
construct rigid matrices, prove a new unrestricted circuit lower bound,
establish novelty or peer review, or resolve `P` versus `NP`.
