# Laboratory V89 — eight-row addressing boundary

V89 begins with the proposed orthogonal-array route, but separates its exact
finite theorem from the unproved random-model bridge.

## Main result

If the variables can be labeled by nonzero vectors of `F_2^3` so that every
ternary support receives a basis, then eight fixed affine witness rows give all
eight local addresses on every support. Consequently **every** target matrix
with at most eight rows is coverable.

A proper four-coloring of the primal graph is one sufficient way to obtain this
basis labeling, using the four-point cap

```text
001, 010, 100, 111.
```

The committed `OA(8,4,2,3)` audit verifies the equivalent even-parity
`[4,3,2]` code construction.

## Correction to the initial asymptotic proposal

The V80 and deterministic V87 controls are not primal-four-colorable. Their
exact primal chromatic numbers are

```text
6, 5, 5, 5, 6, 5, 5, 5, 5, 5, 6.
```

Therefore average primal degree near six cannot be used as a substitute for a
four-colorability theorem.

All eleven controls do, however, admit the more general `F_2^3` basis coloring.
Thus the eight-row construction survives every committed finite control, even
where the four-color argument fails.

## Strong-four second-moment reduction

Strong four-coloring is the exact random-hypergraph formulation of primal
four-colorability. For two balanced four-colorings with overlap matrix `A`, the
joint probability that one random support is rainbow under both colorings is

```text
q(A) = 1/8 + 4 sum_ij A_ij^3.
```

Writing `B=4A`, the second-moment exponent relative to the uniform overlap is

```text
Phi_c(B)
  = H(B)/4 - ln(4)
    + c ln(4(2 + sum_ij B_ij^3)/9).
```

The V87 density tends to one. Closing the four-color bridge reduces to proving
`Phi_c0(B)<=0` on the `4x4` Birkhoff polytope for one fixed `c0>1`, with equality
only at the uniform matrix.

The uniform overlap is an exact strict local maximum for every `c<3/2` because
the quadratic coefficient is

```text
-8 + (16/3)c.
```

Thus the target regime has no local overlap instability. The remaining problem
is global.

The executable packet verifies the cubic identity on `2,314` exact rational
overlaps and audits `52,637` rational Birkhoff points through density `1.05`.
All tested exponents are nonpositive. These grids are evidence only and are not
recorded as a continuous proof.

## Empty-core peeling boundary

The density-one V87 model lies below the 3-core threshold for random
3-uniform hypergraphs, which initially suggested a reverse-peeling construction
for the seven-state basis CSP. V89 now closes that shortcut negatively.

An exact eight-vertex, ten-edge hypergraph has empty 3-core but no `F_2^3`
basis coloring. It has a short affine-coset contradiction, zero satisfying
assignments among `7^5=16,807` normalized possibilities, and becomes colorable
after deleting any edge.

A bitset census checks all `212,625` maximal ordered empty-core hypergraphs on
seven vertices and finds all of them colorable, so the obstruction is
vertex-minimal in that class. A separate 12-vertex, 14-edge obstruction is
linear, has pair-codegree one, and is also edge-critical and not basis-colorable.

Therefore neither empty 3-core nor empty 3-core plus linearity implies the
basis-coloring condition. The random-model bridge remains open and must exploit
additional probabilistic structure, the full seven-state overlap, or the
strong-four inequality.

## Exact uniform ceiling

A ternary support has eight local addresses. Hence target-independent injective
addressing cannot cover nine rows. Eight is attained by the affine basis
construction.

This ceiling applies only to one witness family chosen independently of the
target matrix. Target-dependent collision arguments may behave differently.

## Candidate status

V89 is a draft candidate. The promoted constructor lower bound remains four
rows. Raising it to nine requires a rigorous asymptotic bridge showing that a
V87-resistant target-stretch family also admits basis addressing or strong
four-coloring with positive probability.

## Research budget

V89 and V90 are the final two laboratories allocated to the `Eval_H`
constructor front. Without a superconstant lower bound, a constructive
`O(n^(1/3))` list, or an asymptotic eight-row bridge by the end of V90, this
front closes and effort returns to rigidity/average-case bridges or proof
complexity.

## Files

- `OA8_ADDRESSING.md` — eight-row theorem packet;
- `oa8_addressing.py` — exact OA, code, chromatic, and basis-coloring audits;
- `RESULTS.json` — immutable addressing evidence;
- `STRONG4_SECOND_MOMENT.md` — exact overlap reduction and analytic boundary;
- `strong4_second_moment.py` — exact overlap and rational-grid census;
- `STRONG4_RESULTS.json` — immutable strong-four evidence;
- `BASIS_CORE_OBSTRUCTION.md` — analytic and executable peeling boundary;
- `basis_core_obstruction.py` — exact obstructions and minimality census;
- `BASIS_CORE_RESULTS.json` — immutable core-obstruction evidence;
- `verify.py` — primary verifier;
- `verify_independent.py`, `verify_strong4_independent.py`, and
  `verify_basis_core_independent.py` — independent reconstructions;
- `LITERATURE_BOUNDARY.md` — source and model-transfer boundary;
- `VALIDATION.md` — execution record;
- `V90_CORE_CONTEXT.md` — continuation and stop rule.

## Nonclaims

V89 does not yet prove the global Birkhoff inequality, asymptotic strong
four-colorability or basis-colorability of the V87 model, a nine-row constructor
lower bound, a constructive support-only list, unrestricted `NC0_3-Avoid`,
rigidity, a circuit lower bound, or `P != NP`.
