# Support branchwidth up to sqrt(log m): constructive remote points

## Inputs from V75 and V77

V75 proves that a supplied gate branch tree of support-boundary width `b`
compiles to a monotone arithmetic DAG of size

```text
S = O(m A(b)^2 poly(n,m)),
```

where `A(b)` is the number of nonempty affine subspaces of `GF(2)^b`.

V77 composes the Korhonen--Oum connectivity-function algorithm with its
balanced topology-tree transfer. For support connectivity branchwidth `k`, it
constructs a gate tree of width at most `2k` in

```text
2^{O(k^2)} gamma m^6 log m
```

time, where `gamma=O(m)` for explicit fan-in-three supports.

V85 evaluates the resulting V75 DAG over truncated distance polynomials and
uses exact prefix pair counting to construct a target farther than radius `r`
whenever `2^n B(m,r)<2^m`.

## Elementary bound on A(b)

The number of `d`-dimensional linear subspaces of `GF(2)^b` is the Gaussian
binomial

```text
[b choose d]_2 = product_{i=0}^{d-1} (2^b-2^i)/(2^d-2^i).
```

Every denominator factor is at least `2^(d-1)` and every numerator factor is
at most `2^b`, so

```text
[b choose d]_2 <= 2^(d(b-d+1)).
```

Each such subspace has `2^(b-d)` affine cosets. Therefore

```text
A(b)
 <= sum_{d=0}^b 2^(b-d) 2^(d(b-d+1))
 =  sum_{d=0}^b 2^(d(b-d)+b)
 <= (b+1) 2^(floor(b^2/4)+b).
```

For the V77 width `b=2k`,

```text
A(2k)^2 <= (2k+1)^2 2^(2k^2+4k).
```

## Runtime theorem

Let `sigma=m-n`, and choose any radius satisfying `B(m,r)<2^sigma`. The V85
distance evaluator performs at most two full truncated-polynomial DAG
evaluations per output coordinate. With naive convolution, the total time is

```text
2^{O(k^2)} gamma m^6 log m
 + O(m^2 A(2k)^2 r^2 poly(n,m)).
```

All coefficients count subsets of `{0,1}^n x {0,1}^m`, so their bit length is
at most `n+m+1`.

### Corollary

If

```text
k = O(sqrt(log m)),
```

then both `2^{O(k^2)}` and `A(2k)^2` are polynomial in `m`. Since `r<=m`, the
entire algorithm is polynomial time, starting from the explicit circuit and
without a supplied decomposition.

Using `B(m,r)<=(em/r)^r`, one obtains

```text
r = Omega((m-n)/log m).
```

Hence fan-in-three circuits of support connectivity branchwidth
`O(sqrt(log m))` admit deterministic polynomial-time construction of a point
at Hamming distance

```text
Omega((m-n)/log m)
```

from their range.

At the laboratory's additive stretch `m-n=n^(2/3)`, the guaranteed distance is
`Omega(n^(2/3)/log n)`.

## Precision

The hidden constants in `O(k^2)` determine the polynomial degree but do not
affect polynomiality for `k<=c sqrt(log m)` with fixed `c`. This theorem does
not imply that the V84 Hall-expander branch has small support branchwidth, and
therefore does not solve unrestricted `NC0_3-Avoid`.
