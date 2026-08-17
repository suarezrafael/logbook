# V108 core context — MUX/bijunctive exact-stretch frontier

## Starting point

If V107 survives CI and external mathematical review, the essential
signed-majority orbit `0x17` is polynomial-time range avoidable at every positive
stretch `m>n`.

V101's functional-anchor classification left exactly two essential ternary
anchor-free NPN orbits:

- signed majority `0x17`;
- MUX/bijunctive selector `0x1b`.

V102 already showed that a MUX gate becomes affine after conditioning its unique
selector, but an arbitrary circuit may use linearly many distinct selectors.
Therefore V108 must not simply restate the strong-affine-backdoor parameter.

## Central problem

Develop an exact-stretch polynomial algorithm, or a genuine scalable barrier,
for circuits whose outputs lie in the essential ternary MUX/bijunctive orbit.

A canonical representative can be written as

```text
MUX(s,a,b) = (not s AND a) OR (s AND b),
```

up to input/output negations and permutations.  For a fixed output target, the
fiber has a selector-controlled pair of binary conditions.  The key question is
whether these local implications can be globally organized without branching on
all selectors.

## Track A — implication / 2-SAT view

For each MUX target, derive an exact CNF/implication representation and classify
which binary clauses are target-selectable.  Search for a graph/matroid object
analogous to V105--V107's signed-majority transport graph.

Do not assume the same signed-frame matroid appears: MUX has a distinguished
selector and asymmetric data inputs.

## Track B — selector elimination graph

Build a graph or directed hypergraph whose vertices are selectors and data
variables.  Try to orient dependencies so that selector cycles can be solved
simultaneously, analogous to V103 affine-rank cycle compression.

Useful targets:

- SCC decomposition where selector choices cancel or become affine;
- a bounded kernel around selector cycles;
- a matching/transversal theorem that chooses data branches without enumerating
  selectors.

## Track C — combine V101 functional anchors with MUX branches

Although the original MUX gate has no V101 functional anchor, fixing one
selector branch turns it into a literal.  Look for a global condition under
which a small set of branch decisions unlocks a large functional DAG.

A promotion-worthy parameter must beat V102's selector-count backdoor on an
infinite family; another restatement of `beta` is insufficient.

## Track D — barrier / hardness

If global selector elimination resists compression, test whether finding a
small selector set or a target-compatible branch orientation is NP-hard or
PP-hard.  A rigorous hardness result would be material because, after V107, MUX
is the principal local orbit still preventing the current structural program
from covering all essential ternary gates.

## Consequence discipline

Even a full MUX theorem would not automatically prove unrestricted
`NC0_3-Avoid` without re-running the V100/V101 reductions and verifying that all
other predicates preprocess into the solved classes without hidden parameter
loss.  Only after that should the laboratory test published Range-Avoidance to
circuit-lower-bound/meta-complexity transfers.

P versus NP must remain marked unresolved unless such a published transfer is
actually triggered with all hypotheses proved.

## Stop rule

V108 must provide at least one of:

1. an exact-stretch polynomial MUX/bijunctive avoider;
2. a new parameter with an infinite-family separation from V102 and a credible
   route to worst-case control;
3. a scalable hardness/barrier theorem for global selector orientation.

Another finite truth-table census or constant-size MUX gadget is not sufficient.
