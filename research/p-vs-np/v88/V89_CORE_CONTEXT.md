# V89 core context — reserved continuation after V88

V89 is not active while V88 remains a candidate.

## Frozen starting point

V88 has established an exact collision normal form for repeated-table
`Eval_H`:

- normalized variable patterns use alphabet `2^(k-1)`;
- differing target pairs impose local separation constraints;
- every two-row list is coverable;
- three-row coverability is labeled three-color hypergraph coloring;
- the complete four-variable census has `7,264` instances and no obstruction.

## Continuation priorities

If V88 is promoted through a constructive or lower-bound result, the next
laboratory should preserve the exact normal form and pursue only one of:

1. deterministic target matrices from codes, small-bias sets, automorphisms,
   or tensor products;
2. a lower bound for a precisely defined row-separable, linear, cyclic, or
   low-degree constructor model;
3. explicit target-stretch hypergraphs that make the separation CSP
   unsatisfiable at `k=O(n^(1/3))`;
4. a quantitative bridge from the collision CSP to the V85 remote-point
   machinery.

## Discipline

Do not infer progress toward `P != NP` from an unsatisfiable finite CSP alone.
Every asymptotic claim must preserve the target stretch
`m=n+ceil(n^(2/3))`, polynomial-time constructibility, and the distinction
between an existential target list and an efficiently generated one.
