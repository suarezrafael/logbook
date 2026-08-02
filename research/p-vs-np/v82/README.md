# Laboratory V82 — transversal girth literature and complexity audit

V82 begins with the literature checkpoint requested by the V81 core context.
It does **not** start by proposing a new hardness reduction or algorithm.

The central observation is that the exact Hall-neighborhood objective already has
a standard matroid interpretation. Let `G=(M,X;E)` be the bipartite support
presentation, let `T(G)` be its transversal matroid on the gate set `M`, and set

```text
h*(G) = min { |N(S)| : S subseteq M and |N(S)| < |S| }.
```

Whenever dependent sets exist,

```text
h*(G) = girth(T(G)) - 1.
```

Every inclusion-minimal minimizer of `h*` is a circuit of `T(G)` and has Hall
deficiency exactly one. This formally separates two objectives that were only
operationally separated in V80–V81:

- minimizing the neighborhood produces a deficiency-one witness;
- maximizing deficiency improves the randomized NP-oracle success probability,
  but is a different optimization problem.

## Complexity boundary

The general problem is already hard. Colbourn and Elmallah, *Discrete
Mathematics* 114 (1993), Theorem 2.1, prove that determining the minimum circuit
cardinality of a transversal matroid is NP-hard by reduction from Clique. Their
article is the verified primary citation used by V82. A Stockmeyer attribution
appears in secondary sources, but V82 does not use it as primary provenance.

At left degree at most two, the support presentation is bicircular: gates become
edges or loops on the variable vertices, independent sets are pseudoforests, and
circuits are bicycles (theta graphs, tight handcuffs, or loose handcuffs). With
the presenting graph supplied, a shortest bicycle is polynomial-time computable
by enumerating its constant-size topology and using polynomial fixed-terminal
disjoint-path/min-cost-flow subroutines.

The unresolved boundary isolated by V82 is therefore:

```text
transversal girth with left degree at most three.
```

No located primary source settles this exact restriction.

## Parameterized-algorithm audit

Panolan, Ramanujan, and Saurabh (WADS 2015) give parameterized algorithms for
matroid girth, including treatment of transversal matroids that avoids an
exponential dependence on the large representation field. This does not yield
a polynomial algorithm for the laboratory's target regime: in the audited
families the transversal rank is `n`, and the shortest-circuit size also grows
with `n`. V82 records this parameter mismatch rather than treating FPT as a
closed algorithmic arm.

## Exact finite evidence

The primary and independent verifiers recompute the transversal rank, every
circuit, `h*`, and all inclusion-minimal `h*` minimizers for the three V80
rank-three families:

| family | rank | `h*` | transversal girth | girth circuits |
|---|---:|---:|---:|---:|
| seven variables | 7 | 6 | 7 | 9 |
| eight variables | 8 | 7 | 8 | 20 |
| nine variables | 9 | 8 | 9 | 44 |

Across these examples, 22,528 subset states are checked. Three degree-at-most-
two controls instantiate the theta, tight-handcuff, and loose-handcuff circuit
topologies.

## Route decision

The next focused attack is the degree-three boundary. The preferred first
attempt is hardness: replace the high-degree incidence in the general Clique
reduction by degree-three gadgets, with exhaustive finite gadget tests before a
proof. An algorithm that exploits degree three remains an equally valid
outcome.

The stop rule is explicit: after three focused mathematical iterations without
a closed reduction or algorithm, promote the extended structural census
(sunflowers, affine-cell invariant, `G*_proj`, and monotonicity counterexamples)
and move the next laboratory to explicit-obstruction tests.

`APC^1` remains deferred to the V56 affine certificate and escalates only after
a demonstrated blocker.

## Files

- `TRANSVERSAL_GIRTH_COMPLEXITY_AUDIT.md` — equivalence proof and literature map;
- `V82_TRANSVERSAL_GIRTH_EQUIVALENCE_THEOREM.tex` — formal standalone module;
- `transversal_girth.py` — exact transversal-matroid census;
- `RESULTS.json` — immutable evidence;
- `verify.py` and `verify_independent.py` — read-only audits;
- `V83_CORE_CONTEXT.md` — degree-three route and stopping rule.

## Nonclaims

V82 does not settle transversal girth for left degree three, does not prove a
new NP-hardness result, does not give a polynomial algorithm for the rank-three
support regime, does not produce the deterministic `FP^NP` candidate list,
does not prove an all-orders obstruction, does not formalize V56 in `APC^1`,
and does not resolve P versus NP.
