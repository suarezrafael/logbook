# Laboratory V89 — eight-row addressing boundary

V89 separates exact finite theorems from the still-unproved random-model
bridge.

## Main result

If variables can be labeled by nonzero vectors of `F_2^3` so that every ternary
support receives a basis, then eight fixed affine witness rows realize all
eight local addresses on every support. Consequently every target matrix with
at most eight rows is coverable.

A proper four-coloring of the primal graph is one sufficient special case,
using the four-point cap

```text
001, 010, 100, 111.
```

The committed `OA(8,4,2,3)` audit verifies the equivalent even-parity
`[4,3,2]` construction.

## Finite correction to the four-color proposal

The V80 and deterministic V87 controls are not primal-four-colorable. Their
exact primal chromatic numbers are

```text
6, 5, 5, 5, 6, 5, 5, 5, 5, 5, 6.
```

All eleven nevertheless admit the more general `F_2^3` basis coloring and pass
the eight-row injectivity audit.

## Strong-four second-moment reduction

For two balanced strong four-colorings with overlap matrix `A`,

```text
q(A) = 1/8 + 4 sum_ij A_ij^3.
```

Writing `B=4A`, the relative exponent is

```text
Phi_c(B)
  = H(B)/4 - ln(4)
    + c ln(4(2 + sum_ij B_ij^3)/9).
```

The uniform overlap is a strict local maximum for every `c<3/2`. The executable
packet verifies `2,314` exact overlap identities and `52,637` rational
Birkhoff points. The remaining obstruction is global.

## Empty-core peeling boundary

The density-one V87 model lies below the 3-core threshold for random
3-uniform hypergraphs, which suggested a reverse-peeling construction for the
seven-state basis CSP. V89 closes that universal shortcut negatively.

An exact eight-vertex, ten-edge hypergraph has empty 3-core but no `F_2^3`
basis coloring. It has a short affine-coset contradiction, zero satisfying
assignments among `7^5=16,807` normalized possibilities, and becomes colorable
after deleting any edge.

A bitset census checks all `212,625` maximal ordered empty-core hypergraphs on
seven vertices and finds all colorable, so the obstruction is vertex-minimal in
that class. A separate 12-vertex, 14-edge obstruction is linear, has
pair-codegree one, and is also edge-critical and noncolorable.

Thus neither empty 3-core nor empty 3-core plus linearity implies the basis
condition. A successful asymptotic bridge must use additional random structure.

## Full seven-state second moment

The seven-state basis relation has `168` ordered bases among `7^3` ordered
triples, so one random support is satisfied with probability `24/49`.

For a balanced pair-overlap `A=B/7`, where `B` is `7x7` doubly stochastic, the
exact relative exponent is

```text
Psi_c(B)
  = H(B)/7 - ln(7)
    + c ln(q(B)/(24/49)^2),
```

where

```text
q(B)=7^-3 sum_{x,y ordered bases}
     B[x1,y1] B[x2,y2] B[x3,y3].
```

On the 36-dimensional tangent space at the uniform overlap, exact rational
calculation gives energy-log Hessian `(1/6)I` and total Hessian

```text
-I + (c/6)I.
```

Therefore the uniform overlap is a strict local maximum for every `c<6`; at the
target density one the quadratic coefficient is `-5/12`. This local margin is
much stronger than the strong-four specialization.

All `5,040` permutation overlaps are classified exactly. A deterministic
20,000-point diagonal-family scan places its first diagnostic transition near
`c=2.520745085422`. Neither result proves the global `7x7` inequality.

The clean V90 target is now the entropy contraction

```text
c0 ln(q(B)/(24/49)^2)
  <= ln(7)-H(B)/7
```

for one fixed `c0>1`, with equality only at the uniform matrix.

## Exact uniform ceiling

A ternary support has eight local addresses. Hence target-independent injective
addressing cannot cover nine rows. Eight is attained by the affine basis
construction. This ceiling does not rule out target-dependent collision
arguments.

## Candidate status

V89 remains a draft candidate. The promoted constructor lower bound is still
four rows. Raising it to nine requires a rigorous global overlap theorem or a
separate asymptotic basis-addressing bridge, followed by fixed-edge
second-moment bookkeeping.

## Research budget

V89 and V90 are the final two laboratories allocated to the `Eval_H`
constructor front. Without a superconstant lower bound, a constructive
`O(n^(1/3))` list, or an asymptotic eight-row bridge by the end of V90, this
front closes and effort returns to rigidity/average-case bridges or proof
complexity.

## Files

- `OA8_ADDRESSING.md`, `oa8_addressing.py`, `RESULTS.json` — eight-row theorem;
- `STRONG4_SECOND_MOMENT.md`, `strong4_second_moment.py`,
  `STRONG4_RESULTS.json` — strong-four overlap geometry;
- `BASIS_CORE_OBSTRUCTION.md`, `basis_core_obstruction.py`,
  `BASIS_CORE_RESULTS.json` — exact peeling obstructions and minimality census;
- `BASIS7_SECOND_MOMENT.md`, `basis7_second_moment.py`,
  `BASIS7_RESULTS.json` — full seven-state overlap geometry;
- `verify.py` and the independent verifiers — executable reconstruction;
- `LITERATURE_BOUNDARY.md`, `VALIDATION.md`, `V90_CORE_CONTEXT.md` — source,
  validation, continuation, and stop-rule boundaries.

## Nonclaims

V89 does not prove either global Birkhoff inequality, asymptotic strong
four-colorability or basis-colorability of the V87 model, a nine-row constructor
lower bound, a constructive support-only list, unrestricted `NC0_3-Avoid`,
rigidity, a circuit lower bound, or `P != NP`.
