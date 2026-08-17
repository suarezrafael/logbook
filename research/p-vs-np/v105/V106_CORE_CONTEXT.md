# V106 core context — signed-majority implication minors

## Starting point

V105 turns every fixed signed-majority target into exact 2-CNF pair clauses and
uses the canonical first-two-variable pair graph. An edge carries transport

```text
delta_e = 1 XOR p_u XOR p_v.
```

For either starting polarity, the output target can be chosen so that the edge
transports that literal by `delta_e` and simultaneously supplies the reverse
contrapositive implication.

The current polynomial class detects two vertex-disjoint **odd transport
triangles** joined by a path. Their targets create a contradictory implication
SCC. The strict exact-stretch family defeats the preceding affine/functional
parameters and V98 switching balance.

## Track A — general odd-cycle dumbbells

The proof itself never uses triangle length three. It only needs two edge-disjoint
cycles with transport XOR one, connected by a path disjoint from their edges.

The mathematical statement therefore extends immediately to a supplied pair of
odd transport cycles. The unresolved algorithmic question is a clean,
self-contained polynomial detector for the broadest useful signed-cycle packing
class without importing a heavy graph-minor theorem unnecessarily.

First targets:

1. two vertex-disjoint odd transport cycles plus a connecting path;
2. figure-eight odd cycles sharing one vertex;
3. theta graphs, where cycles overlap in paths and target compatibility is more
   delicate.

A practical V106 should either implement a simple polynomial detector for a
strictly broader class than V105 or prove that one of the overlap types cannot
always be targeted consistently.

## Track B — implication bicycle characterization

For ordinary 2-SAT, unsatisfiability is equivalent to a variable and its
negation lying in one SCC, and minimal witnesses are often described by bicycle
structures. Here the clause signs are not arbitrary: each output target selects
three pair clauses simultaneously.

Characterize which signed implication bicycles are **target-compatible**, i.e.
all clauses using the same output gate demand one common target bit. A successful
characterization could replace the current canonical-pair restriction by a
search directly in the six implications available from every majority gate.

## Track C — structural forcing from exact stretch

The high-value target is a theorem of the form

```text
m>n + signed-majority residual conditions
    => target-compatible contradictory implication minor.
```

Do not assume this is true. V99 already showed that simple signed-majority
loose-X structures can be surjective in the nonzero switching classes. Search
for scalable counterexamples in parallel with positive forcing arguments.

Useful restrictions to test first:

- bounded pair multiplicity;
- minimum support degree at least two;
- no proper positive-surplus subcircuit;
- prescribed switching imbalance;
- canonical-pair graph cyclomatic rank or signed odd-cycle packing number.

## Track D — relation to P versus NP

Even a polynomial algorithm for all signed-majority outputs would still solve
only one residual predicate orbit. It would be an important `NC0_3-Avoid`
advance but not by itself a P-versus-NP resolution.

If V106 reaches a broad all-signed-majority theorem, immediately recompute the
post-V100 residual orbit set and check whether the remaining orbits can be
reduced to majority via literal substitutions or restrictions. Only then test
published Range-Avoidance-to-lower-bound transfers.

## Promotion criterion

V106 must provide at least one of:

1. a polynomial target-compatible implication-bicycle detector strictly broader
   than V105 with a new infinite-family separation;
2. a structural forcing theorem for a meaningful signed-majority exact-stretch
   class;
3. a rigorous scalable obstruction showing that implication bicycles cannot
   cover the remaining signed-majority regime, with a justified next invariant.

Another fixed triangle family or finite truth-table census is not sufficient.
