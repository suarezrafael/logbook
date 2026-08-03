# Laboratory V88 — repeated-table `Eval_H` collision geometry

V88 begins the constructivity program reserved by V87. The first step is to
use the repeated truth-table structure of `Eval_H` rather than treating it as
an arbitrary locality-eleven circuit.

## Main result

A `k`-row target list is coverable exactly when one can assign each input
variable a normalized pattern in `{0,1}^{k-1}` such that every pair of target
rows that differs at output `i` is separated by at least one variable of the
support `S_i`.

This gives an exact CSP with alphabet `2^(k-1)` and local arity at most three.
The proof is elementary but strategically important: it isolates the sole
obstruction created by repeated truth-table coordinates—collisions of local
addresses carrying incompatible target bits.

## Immediate consequences

- Every two-row target list is coverable by an explicit union-of-supports
  witness. Therefore a universal support-only list must exploit interactions
  among at least three rows.
- For three rows, coverability is exactly a labeled three-color hypergraph
  problem. A nonconstant target column labels its support by its unique equal
  row pair; a valid coloring may make that support monochromatic only in the
  labeled color.
- The smallest complete census, over all simple ternary support families on
  four variables and every target matrix with at most three rows, contains
  `7,264` instances and zero formulation mismatches. All are coverable.

## Why this direction was selected

V87 produced a probabilistic family simultaneously resistant to Hall,
constant-syndrome, and bounded-width certificates, but it did not construct a
support-only target list. V85 had already reduced that missing construction to
a remote point of `Eval_H`. The collision normal form is the first reduction
that uses the repeated table coordinates explicitly and turns the target-list
problem into a combinatorial object that can be attacked by coding, coloring,
small-bias, or constructor-lower-bound methods.

## Files

- `COLLISION_NORMAL_FORM.md` — theorem packet and proofs;
- `collision_normal_form.py` — executable normal form, pair constructor,
  three-row reduction, and exact census;
- `RESULTS.json` — immutable audit summary;
- `verify.py` — primary verifier;
- `verify_independent.py` — independent direct truth-table audit;
- `V89_CORE_CONTEXT.md` — continuation targets, conditional on V88 progress.

## Candidate status

V88 is opened as a **draft candidate**, not a promoted laboratory. The current
packet does not yet satisfy the V88 stop conditions. Promotion requires a
constructive `Eval_H` list, a rigorous lower bound for a precise constructor
model, an explicit deterministic three-certificate family, a complete remote-
point bridge ledger, or a verified bounded-arithmetic boundary.

## Nonclaims

V88 has not constructed the `O(n^(1/3))` target list, solved unrestricted
`NC0_3-Avoid`, derandomized V87, produced rigid matrices, proved a new circuit
or proof-complexity lower bound, confirmed novelty, passed peer review, or
resolved `P` versus `NP`.
