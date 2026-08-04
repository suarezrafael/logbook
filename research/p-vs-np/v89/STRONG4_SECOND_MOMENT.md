# V89 strong-four second-moment reduction

This module attacks the missing asymptotic bridge behind the eight-row
addressing theorem.  It does **not** claim that the bridge is closed.

## 1. Why strong four-coloring is the correct random model

A proper four-coloring of the primal graph is equivalent to a strong
four-coloring of the ternary support hypergraph: every support must receive
three distinct colors.  Composing those four colors with the cap

```text
001, 010, 100, 111
```

gives an `F_2^3` basis coloring and therefore the eight-row address family from
the main V89 theorem.

The primal graph is a union of correlated triangles, so ordinary
`G(n,d/n)` chromatic thresholds cannot be substituted for this model.

## 2. First moment

Restrict to balanced four-colorings.  A uniformly sampled ternary support is
rainbow with probability

```text
(4 * 3 * 2) / 4^3 = 3/8.
```

At edge density `m/n -> c`, the exponential first-moment base is

```text
4 * (3/8)^c.
```

At `c=1` this is `3/2`, so the expected number of balanced strong
four-colorings is exponentially large.  The first-moment obstruction appears
only at

```text
c = ln(4) / ln(8/3) = 1.413390105223...
```

This does not prove existence because correlations between colorings remain.

## 3. Exact overlap identity

Let two balanced colorings have overlap matrix `A`, where `A_ij` is the
fraction of vertices receiving color `i` in the first coloring and color `j`
in the second.  Every row and column sum of `A` equals `1/4`.

Let `q(A)` be the probability that a random ordered triple is rainbow under
both colorings.  Direct expansion over the injective choices of three row
colors and three column colors, followed by the row/column-sum identities,
gives

```text
q(A) = 1/8 + 4 * sum_ij A_ij^3.
```

Writing `B=4A`, so that `B` is doubly stochastic,

```text
q(B) = (2 + sum_ij B_ij^3) / 16.
```

The executable audit checks the direct injective sum against the cubic formula
on all `2,314` integer overlap matrices with margins one through three, with
zero mismatches.

## 4. Continuous Birkhoff-polytope problem

After dividing the second moment by the square of the first moment, the
relative exponential objective is

```text
Phi_c(B)
  = H(B)/4 - ln(4)
    + c ln(4(2 + sum_ij B_ij^3)/9),
```

where

```text
H(B) = -sum_ij B_ij ln B_ij.
```

The uniform matrix `J/4` has `Phi_c(J/4)=0` for every `c`.

A sufficient analytic bridge is therefore:

> Find one fixed `c0>1` such that `Phi_c0(B)<=0` for every `4x4` doubly
> stochastic matrix `B`, with equality only at `J/4`.

Because the V87 density is `1+O(n^(-1/3))`, any fixed margin `c0>1` would
cover all sufficiently large V87 scales.  A bounded second-moment ratio would
give positive probability of a strong four-coloring; a separate sharp-threshold
or monotonicity step would then be needed for a high-probability statement.

At density one the global inequality becomes

```text
ln(2 + sum_ij B_ij^3)
  - (1/4) sum_ij B_ij ln B_ij
  <= ln(9).
```

This is now the exact unresolved analytic core of the four-color route.

## 5. Exact local stability

Put

```text
A = J/16 + X,
```

where every row and column sum of `X` is zero.  Around the uniform overlap,

```text
H(A)-H(J/16) = -8 ||X||_2^2 + O(||X||_2^3),
```

and the cubic identity gives

```text
ln q(A)-ln q(J/16)
  = (16/3) ||X||_2^2 + O(||X||_2^3).
```

Hence the quadratic coefficient is

```text
-8 + (16/3)c.
```

The uniform overlap is a strict local maximum for every

```text
c < 3/2.
```

In particular, the target density `c=1` has exact local margin `8/3`.  Thus the
remaining obstruction is global, not an infinitesimal symmetry-breaking mode.

## 6. Finite evidence and its limit

The primary audit enumerates all `52,637` rational doubly stochastic matrices
with common integer margin at most five.  At densities

```text
1.00, 1.01, 1.02, 1.05
```

every sampled objective is nonpositive; whenever the uniform matrix is present
in the grid, it is the unique maximizer.

The symmetric diagonal/off-diagonal family has a scanned transition near

```text
c = 1.086445038539.
```

These computations are diagnostics only.  A finite rational grid cannot prove
the continuous inequality, and the one-dimensional family cannot exclude a
nonsymmetric global maximizer.

## 7. Literature boundary

Strong colorability of sparse random hypergraphs is an established research
area and is analyzed by second-moment methods.  The 2021 Balobanov--Shabanov
paper gives asymptotic bounds for sufficiently large numbers of colors.  The
2023 Khuzieva--Matveeva--Shabanov paper studies fixed `r>=k>=3` and gives tight
threshold bounds.  The present laboratory has not imported an exact theorem
from those papers at the specific point `k=3`, `r=4`, `c=1`; the internal
Birkhoff reduction is retained until that parameter transfer is checked line
by line.

## 8. Current status

Proved internally:

- the exact cubic overlap identity;
- the exact second-moment objective;
- strict local stability through density `3/2`;
- finite rational-grid and symmetric-family audits.

Still open:

- the global Birkhoff inequality for any fixed `c0>1`;
- strong four-colorability of the V87 model with positive probability or with
  high probability;
- the nine-row support-only constructor lower bound.
