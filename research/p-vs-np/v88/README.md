# Laboratory V88 — repeated-table `Eval_H` collision geometry

V88 begins the constructivity program reserved by V87. The first step is to
use the repeated truth-table structure of `Eval_H` rather than treating it as
an arbitrary locality-eleven circuit.

## Collision normal form

A `k`-row target list is coverable exactly when one can assign each input
variable a normalized pattern in `{0,1}^{k-1}` such that every pair of target
rows that differs at output `i` is separated by at least one variable of the
support `S_i`.

This gives an exact CSP with alphabet `2^(k-1)` and local arity at most three.
The proof isolates the sole obstruction created by repeated truth-table
coordinates: collisions of local addresses carrying incompatible target bits.

## Row lower bounds

- Every two-row target list is coverable by an explicit union-of-supports
  witness.
- For three rows, coverability is exactly a labeled three-color hypergraph
  problem. A nonconstant target column labels its support by its unique equal
  row pair; a valid coloring may make that support monochromatic only in the
  labeled color.
- A new bad-cylinder intersection argument proves that **every three-row target
  list with at most fourteen active simple ternary output columns is
  coverable**. Hence a genuine three-row obstruction needs at least fifteen
  active outputs.
- At the target stretch `m=n+ceil(n^(2/3))`, this rules out three-row
  obstructions for every simple ternary scale `5 <= n <= 9`.
- All `3^7=2,187` labelings of the committed Fano support control remain
  coverable; the exact number of satisfying colorings ranges from `1,238` to
  `1,317`.

## Executable evidence

The initial complete census over all simple ternary support families on four
variables and every target matrix with at most three rows contains `7,264`
instances and zero formulation mismatches.

The extended barrier audit additionally checks:

- `1,710` labeled pairs of distinct ternary supports on six variables;
- the exact intersection formulas for support overlaps zero, one, and two;
- five explicit first/second-moment contradiction scales from `n=5` through
  `n=9`;
- every one of the `2,187` Fano labelings.

Both primary and independent implementations use exact integer bitsets for the
larger coloring censuses.

## Why this direction was selected

V87 produced a probabilistic family simultaneously resistant to Hall,
constant-syndrome, and bounded-width certificates, but it did not construct a
support-only target list. V85 had already reduced that missing construction to
a remote point of `Eval_H`. The collision normal form turns the target-list
problem into a combinatorial separation CSP that can be attacked by coding,
coloring, higher intersection moments, or constructor-model lower bounds.

## Files

- `COLLISION_NORMAL_FORM.md` — exact repeated-table normal form;
- `THREE_ROW_BARRIER.md` — fourteen-output theorem and proof;
- `collision_normal_form.py` — normal form, pair constructor, three-row
  reduction, and exact small census;
- `three_row_barrier.py` — bad-cylinder formulas, moment certificates, and Fano
  census;
- `RESULTS.json` — immutable audit summary;
- `verify.py` — primary verifier;
- `verify_independent.py` — independent direct audit;
- `LITERATURE_BOUNDARY.md` — novelty and source boundary;
- `VALIDATION.md` — execution record;
- `V89_CORE_CONTEXT.md` — continuation targets, conditional on V88 progress.

## Current frontier

The next focused questions are:

1. whether a fifteen-output three-row obstruction exists;
2. whether third or higher intersection moments raise the constant lower bound;
3. whether four-row target matrices admit a cleaner explicit obstruction;
4. whether a precise constructor class can be ruled out.

## Candidate status

V88 remains a **draft candidate**, not a promoted laboratory. The current
packet does not yet satisfy the promotion stop conditions. Promotion still
requires a constructive `Eval_H` list, a rigorous lower bound for a precise
constructor model, an explicit deterministic three-certificate family, a
complete remote-point bridge ledger, or a verified bounded-arithmetic
boundary.

## Nonclaims

V88 has not constructed the `O(n^(1/3))` target list, found a fifteen-output or
four-row obstruction, solved unrestricted `NC0_3-Avoid`, derandomized V87,
produced rigid matrices, proved a new circuit or proof-complexity lower bound,
confirmed novelty, passed peer review, or resolved `P` versus `NP`.
