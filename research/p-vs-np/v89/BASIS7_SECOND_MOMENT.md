# V89/V90 — seven-state basis-CSP second moment

The empty-core shortcut fails, but the full seven-state CSP has substantially
better local overlap geometry than the strong-four specialization.

## Model

Let

```text
D = F_2^3 \ {0},  |D|=7,
R = {(a,b,c) in D^3 : a,b,c form a basis},  |R|=168.
```

A uniformly random ordered triple of labels is a basis with probability

```text
p = 168/7^3 = 24/49.
```

Hence the expected number of basis colorings at edge density `c=m/n` has
exponential base

```text
7 p^c.
```

At density one this base is `24/7=3.428571...`; the first-moment upper density
is `ln(7)/ln(49/24)=2.726256...`.

## Exact overlap objective

For two balanced colorings let `A` be their `7x7` joint distribution, with
margins `1/7`, and write `B=7A`. Thus `B` is doubly stochastic. Define

```text
q(B)
  = 7^-3 sum_{x in R, y in R}
      B[x1,y1] B[x2,y2] B[x3,y3].
```

The relative second-moment exponent is

```text
Psi_c(B)
  = H(B)/7 - ln(7)
    + c ln(q(B)/(24/49)^2).
```

The uniform matrix has value zero.

Equivalently, writing

```text
D(B) = ln(7) - H(B)/7,
L(B) = ln(q(B)/(24/49)^2),
```

the global bridge asks for one fixed `c0>1` such that

```text
c0 L(B) <= D(B)
```

for every doubly stochastic `B`, with equality only at the uniform matrix.
This is a finite-dimensional entropy-contraction inequality.

## Exact local theorem

Let `B=U+tD`, where `U` is uniform and the perturbation `D` has every row and
column sum zero. Exact enumeration of all ordered basis pairs proves

```text
H(U+tD)/7 - ln(7)
  = -t^2 ||D||_F^2/2 + O(t^3),

ln(q(U+tD)/p^2)
  =  t^2 ||D||_F^2/12 + O(t^3).
```

Therefore

```text
Psi_c(U+tD)
  = -(6-c)t^2 ||D||_F^2/12 + O(t^3).
```

The uniform overlap is a strict local maximum for every `c<6`. At the target
density `c=1`, the exact quadratic coefficient is `-5/12`.

The executable certificate constructs a 36-element tangent basis and checks all
`36^2=1,296` bilinear Hessian identities exactly over the rationals, with zero
mismatches. The energy-log Hessian is precisely `(1/6)I` on the tangent space.

## Boundary diagnostics

All `7!=5,040` permutation overlaps are classified exactly. The number of
ordered bases mapped to ordered bases is distributed as

```text
126 : 1,344 permutations
132 : 2,352 permutations
144 : 1,176 permutations
168 :   168 permutations.
```

The final class consists of the 168 automorphisms of the Fano geometry.

For the diagonal/off-diagonal family, ordered basis pairs have coordinate-match
counts

```text
0 matches: 17,976
1 match:    8,568
2 matches:  1,512
3 matches:    168.
```

A deterministic 20,000-point scan places the minimum critical density in this
one-dimensional family near

```text
c = 2.520745085422,
diagonal parameter = 0.833714285714.
```

This is diagnostic only. It does not certify the full `7x7` Birkhoff polytope.

## Consequence for V90

The local obstruction at density one is decisively absent for the full basis
CSP. The remaining task is global: prove a contraction ratio

```text
sup_{B != U} L(B)/D(B) < 1,
```

or find a concrete counterexample. Any explicit bound below one would give a
fixed `c0>1`; for example, `L(B)<=D(B)/2` would certify the bridge through
density two before fixed-edge bookkeeping.

No such global inequality is claimed here. The result identifies a sharper and
more promising target than universal core peeling, while preserving the V90
stop rule.
