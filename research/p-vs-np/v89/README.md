# Laboratory V89 — eight-row addressing boundary

V89 begins with the proposed orthogonal-array route, but separates its exact
finite theorem from the unproved random-model bridge.

## Main result

If the variables can be labeled by nonzero vectors of `F_2^3` so that every
ternary support receives a basis, then eight fixed affine witness rows give all
eight local addresses on every support.  Consequently **every** target matrix
with at most eight rows is coverable.

A proper four-coloring of the primal graph is one sufficient way to obtain this
basis labeling, using the four-point cap

```text
001, 010, 100, 111.
```

The committed `OA(8,4,2,3)` audit verifies the equivalent even-parity
`[4,3,2]` code construction.

## Correction to the initial asymptotic proposal

The V80 and deterministic V87 controls are not primal-four-colorable.  Their
exact primal chromatic numbers are

```text
6, 5, 5, 5, 6, 5, 5, 5, 5, 5, 6.
```

Therefore average primal degree near six cannot be used as a substitute for a
four-colorability theorem.

All eleven controls do, however, admit the more general `F_2^3` basis coloring.
Thus the eight-row construction survives every committed finite control, even
where the four-color argument fails.

## Exact uniform ceiling

A ternary support has eight local addresses.  Hence target-independent
injective addressing cannot cover nine rows.  Eight is attained by the affine
basis construction.

This ceiling applies only to one witness family chosen independently of the
target matrix.  Target-dependent collision arguments may behave differently.

## Candidate status

V89 is a draft candidate.  The promoted constructor lower bound remains four
rows.  Raising it to nine requires a rigorous asymptotic bridge showing that a
V87-resistant target-stretch family also admits basis addressing with positive
probability.

## Research budget

V89 and V90 are the final two laboratories allocated to the `Eval_H`
constructor front.  Without a superconstant lower bound, a constructive
`O(n^(1/3))` list, or an asymptotic eight-row bridge by the end of V90, this
front closes and effort returns to rigidity/average-case bridges or proof
complexity.

## Files

- `OA8_ADDRESSING.md` — theorem packet and proof boundaries;
- `oa8_addressing.py` — exact OA, code, chromatic, and basis-coloring audits;
- `RESULTS.json` — immutable finite evidence;
- `verify.py` — primary verifier;
- `verify_independent.py` — independent reconstruction;
- `LITERATURE_BOUNDARY.md` — source and model-transfer boundary;
- `VALIDATION.md` — execution record;
- `V90_CORE_CONTEXT.md` — continuation and stop rule.

## Nonclaims

V89 does not yet prove a nine-row constructor lower bound, asymptotic
four-colorability or basis-colorability of the V87 model, a constructive
support-only list, unrestricted `NC0_3-Avoid`, rigidity, a circuit lower bound,
or `P != NP`.
