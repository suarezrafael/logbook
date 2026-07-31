# Cumulative scientific state

**Current laboratory:** V70  
**Updated:** 2026-07-31  
**Program name:** `NC0_k-Avoid Laboratory`  
**P-versus-NP research active:** exploratory  
**Direct P-versus-NP route active:** no  
**P versus NP resolved:** no  
**External review:** requested, replies pending  
**External contact:** sent

## Current scientific position

V68 gives an explicit stretch-one family with exponentially many complete branching-tree leaves while the same family has a linear projected residual DAG.

V69 defines the order-robust parameter

```text
G*_proj = min over gate orders pi of G_proj(pi)
```

and proves that it is the shortest-path cost in the subset lattice of processed gate sets. This is an exact exponential-time audit algorithm.

V70 introduces the support frontier

```text
F(S) = union(processed supports) intersect union(unprocessed supports).
```

If `w(S)` is the projected residual layer width and `A(b)` is the number of nonempty affine subspaces of `GF(2)^b`, then

```text
w(S) <= min(2^|S|, A(|F(S)|)).
```

For an order with frontier profile `b_i` and maximum frontier `q`,

```text
G_proj(pi) <= sum_i min(2^i, A(b_i)) <= m A(q).
```

This proves an FPT-size upper bound parameterized by support-frontier width. It does not prove that a sufficiently small-frontier order always exists or is always findable in polynomial time.

## Component structure

The projected residual-state set factors exactly across connected components of the processed support-incidence graph. V70 verifies this identity on every subset cut of two representative systems, for 640 exact component checks.

## V70 finite scope

Support-only deterministic heuristics give:

```text
n=6:  natural 48  -> lookahead 26; exact G*=15
n=8:  natural 99  -> lookahead 25; exact G*=15
n=10: natural 263 -> lookahead 33; exact G*=17
n=12: natural 580 -> lookahead 52; exact G*=29
n=14: natural 583 -> lookahead 41; exact optimum not computed
```

A separate exact-objective mutation search preserves new finite records:

```text
n=8:  G*_proj=29
n=10: G*_proj=30
```

These are budget records, not global maxima and not asymptotic evidence.

## Consequence for the projected-DAG program

The next mathematical target is to relate support-frontier width to a standard hypergraph pathwidth or treewidth notion and derive constructible orders or sharper decomposition algorithms. The competing target remains an explicit family whose `G*_proj` is superpolynomial under every order.

No simulation to OBDD, FBDD, resolution, Res-Lin, or communication complexity has been proved. Existing lower bounds in those models cannot be imported.

## Publication and discovery

`PUBLICATION_INDEX.md` is now the academic entry point. The repository remains an audit artifact, not a substitute for an indexed manuscript. V71 is reserved for an English LaTeX consolidation and reviewed release metadata. No ECCC, arXiv, or Zenodo publication is claimed by V70.

The earliest planned external follow-up remains **2026-08-24**. Silence is not evidence of novelty, correctness, or approval.

## Lower-bound route gates

1. Resolve projected-DAG order complexity across all six non-affine classes.
2. Reach unrestricted `NC0_3-Avoid` in a lower-bound-relevant stretch regime.
3. Establish a complete reduction to a lower bound strong enough to bear on NP versus polynomial-size circuits.
4. Only then evaluate a logical P-versus-NP consequence.

## Historical corrections

**V22 reproducibility correction:** the original `full_certificate_cases.json` is absent. V22 remains a proof candidate without repository-reproduced finite evidence. V26 remains a justified missing-script skip. The incomplete `n=9` search remains falsification/regression only.

## Repository entry points

- `PUBLICATION_INDEX.md` — theorem-status and discovery index;
- `v70/SUPPORT_FRONTIER_THEOREM.md` — theorem and proof;
- `v70/COMPONENT_FACTORISATION.md` — exact product lemma;
- `v70/HEURISTIC_BENCHMARK.md` — reproducible benchmark;
- `v70/RESULTS.json` and `v70/WITNESSES.json` — exact records;
- `v70/V70_SUPPORT_FRONTIER_THEOREM.tex` — standalone formal module;
- `v70/V71_CORE_CONTEXT.md` — next laboratory constraints.
