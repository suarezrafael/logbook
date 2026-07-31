# Cumulative scientific state

**Current laboratory:** V69  
**Updated:** 2026-07-31  
**Program name:** `NC0_k-Avoid Laboratory`  
**P-versus-NP research active:** exploratory  
**Direct P-versus-NP route active:** no  
**P versus NP resolved:** no  
**External review:** requested, replies pending  
**External contact:** sent

## Current scientific position

V68 gives an explicit stretch-one orbit-`0x07` family with exponentially many complete tree leaves,

```text
c=2^(k-1)=2^((n-3)/2),
```

while dead-variable projection yields a linear fixed-order residual DAG `G_proj=3k+4` for that same family.

V69 addresses order robustness. Define

```text
G*_proj = min over gate orders pi of G_proj(pi).
```

For a set `S` of processed gates, let `w(S)` be the number of distinct nonempty affine residuals after projecting onto variables appearing in unprocessed gates. V69 proves that `w(S)` depends only on `S`, not on the order used to reach it. Hence

```text
G_proj(pi)=sum_i w(prefix_i),
```

and `G*_proj` is the shortest-path cost in the subset lattice. This is an exact exponential-time audit algorithm, not a polynomial algorithm for unrestricted `NC0_3-Avoid`.

## V69 exact finite scope

Natural-order hill-climbing witnesses:

```text
n=6:  G_proj=48  -> exact G*_proj=15
n=8:  G_proj=99  -> exact G*_proj=15
n=10: G_proj=263 -> exact G*_proj=17
n=12: G_proj=580 -> exact G*_proj=29
n=14: G_proj=583 -> tested-order upper bound 147; exact optimum not computed
```

A separate search against the exact objective preserves search-budget records:

```text
n=6:  G*_proj=20
n=8:  G*_proj=28
n=10: G*_proj=24
```

These are finite records, not global maxima and not asymptotic evidence. The exactly checked large fixed-order records collapse under reordering, so fixed-order growth is insufficient for a general DAG lower bound.

## Consequence for the projected-DAG program

The next target is genuinely order robust:

1. prove a constructible polynomial-quality ordering theorem, perhaps parameterized by support separators or treewidth; or
2. construct a family with superpolynomial `G*_proj`, requiring an all-orders argument.

No standard simulation to OBDD, FBDD, resolution, Res-Lin, or best-partition communication complexity has been proved. Existing lower bounds in those models cannot be imported.

## Lower-bound route gates

1. Resolve projected-DAG order complexity across all six non-affine classes.
2. Reach unrestricted `NC0_3-Avoid` in a lower-bound-relevant stretch regime.
3. Establish a complete reduction to a lower bound strong enough to bear on NP versus polynomial-size circuits.
4. Only then evaluate a logical P-versus-NP consequence.

## External requests

The earliest planned follow-up date remains **2026-08-24**. The V68 PDF is suitable for a later conservative review request, but no early follow-up is sent in V69. Silence is not evidence of novelty, correctness, or approval.

## Historical corrections

**V22 reproducibility correction:** the original `full_certificate_cases.json` is absent. V22 remains a proof candidate without repository-reproduced finite evidence. V26 remains a justified missing-script skip. The incomplete `n=9` search remains falsification/regression only.

## Repository entry points

- `v69/ORDER_ROBUSTNESS_THEOREM.md` — set-layer theorem and exact recurrence;
- `v69/EXPERIMENT_REPORT.md` — natural-order collapse and finite exact records;
- `v69/seed_data.json` — full deterministic systems and search provenance;
- `v69/RESULTS.json` — metrics and optimal orders;
- `v69/V69_ORDER_ROBUSTNESS_THEOREM.tex` — standalone formal module;
- `v69/V70_CORE_CONTEXT.md` — next laboratory constraints.
