# V110 next-front context — phase conflict versus nested bottleneck

V110 should not be extended by another unrestricted random census. Its residual is already structurally split.

## Residual A — phase conflict

The upgraded V109 bottleneck has flow two and the two routes share exactly the bottleneck gate `h`, but the two cycles demand opposite target bits on `h`.

This is the empirically dominant V110 failure mode in small strongly connected random MUX circuits. The next useful theorem would exploit the **unused branch clause** of the shared MUX, reroute one path through the other branch, or show that a short sequence of target/branch exchanges converts the conflict into a contradiction elsewhere.

A promising representation is to regard every traversal of `h` as imposing one affine one-bit demand on `y_h`. The conflict is then a parity obstruction attached to a flow pair. Search for a polynomial exchange theorem rather than enumerating all route pairs.

## Residual B — nested bottleneck

Even after raising the first V109 bottleneck `h` to capacity two, max-flow remains one. The new min-cut therefore exposes another capacity-one output gate downstream/upstream of the first bottleneck.

The target question is whether repeated bottlenecks form a provably shrinking dominator chain/decomposition. A promotion-worthy next-laboratory result would need one of:

- a polynomial bound on the depth of a canonical nested-bottleneck decomposition together with a constructive leaf rule;
- a monotone potential that drops after contracting a bottleneck block;
- an FPT parameter with an infinite strict family separating it from V108--V110;
- a counterexample showing that nested dominators alone cannot terminate efficiently.

## Stop rule

Do not claim all-MUX from V110. Do not promote the next laboratory from only random coverage. Require a symbolic exchange/decomposition theorem, a strict asymptotic separation, or a scalable obstruction.

## External calibration

Before strong claims, compare the phase-conflict exchange problem with standard 2-SAT implication-graph rerouting, directed disjoint-path variants, dominator decompositions, and bijunctive CSP structure. Standard graph-theoretic ingredients are not novelty claims.
