# V81 core context — deterministic candidate lists or explicit obstructions

## Established V80 starting point

V80 separates four facts:

1. Hall deficiency is automatic whenever `m>n` and is polynomially detectable by matching.
2. Counting plus NP range-membership gives a zero-error randomized expected-polynomial algorithm, already by using all outputs.
3. The lower-bound-relevant target of ECCC TR23-021 is deterministic `FP^NP`; the missing ingredient is derandomization or a polynomial canonical candidate list.
4. Balanced Hall expansion forces support branchwidth at least the stretch, while rank-three support families can avoid every Hall-deficient set of logarithmic size.

## Priority-one V81 theorem target

For `m=n+ceil(n^(2/3))`, design a polynomial-time procedure which, on every high-width instance, returns exactly one of:

1. a gate set `S` with `|N(S)|=O(log n)` and `|N(S)|<|S|`;
2. a polynomial-size list of projected output patterns guaranteed to contain a missing pattern, derived from affine pieces, sunflowers, or overlap compression;
3. a normalized obstruction certificate with high support branchwidth, no small-neighborhood Hall witness, no V56/V66 affine certificate, and robustness under every gate order in the sense of V69.

Outcome 1 permits projected-image enumeration. Outcome 2 permits NP range-membership selection. Outcome 3 becomes the next lower-bound test family.

## Exact computational program

- encode minimum-neighborhood Hall witnesses as a min-cost matching or submodular minimization problem;
- measure branchwidth, Hall girth, affine-piece rank, sunflower core size, and all-orders residual growth on the same finite families;
- search for a monotone inequality linking one candidate-list measure to support width;
- promote counterexamples before conjectures.

## Priority-two bounded-arithmetic front

Formalize the V56 affine-fiber avoidance certificate in `APC^1` before attempting the full V77 chain. Identify exactly which steps use polynomial-time comprehension, approximate counting or dual weak pigeonhole, stronger induction, and decomposition existence rather than verification.

No claim of `APC^1` provability should be made until a line-by-line formalization exists.

## Proof discipline

- Do not call the program a route to solving P versus NP.
- Keep deterministic `FP^NP`, randomized NP-oracle search, and existential counting separate.
- The target bridge is the rigidity/log-depth consequence of ECCC TR23-021.
- A finite obstruction is not an asymptotic lower bound.
- Conditional hardness results are warnings, not unconditional barriers.
