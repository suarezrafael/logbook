# Laboratory V85 — theorem package

## 1. Completeness of the V84 hard branch

Let `A` be unrestricted `NC0_3-Avoid`, and let `A_exp(L)` be its promise
restriction satisfying

```text
|N(S)| >= |S| for every output set S with |S|<=L.
```

For every fixed `c>0` and `L=c log(n+m)`, `A` and `A_exp(L)` are equivalent
under deterministic search-Turing reductions in `FP^NP`.

The restriction-to-full direction is the identity. In the other direction,
run V84. If the exact transversal girth is at most `L`, V84 extracts a shortest
circuit and constructs an avoided output. Otherwise V84 returns the original
circuit together with the promise defining `A_exp(L)`. Calling the promised
solver therefore needs no nontrivial pullback. This is a search-Turing theorem,
not a many-one completeness claim.

## 2. Support-only candidate lists

Fix a support system `H=(S_1,...,S_m)` on `n` inputs. A support-only list is
computed without seeing the gates' truth tables.

### 2.1 No universal pair

Assume each support has three essential variables. Given arbitrary targets
`y^0,y^1`, use witnesses `0^n,1^n`. At each gate prescribe

```text
f_i(000)=y^0_i,   f_i(111)=y^1_i.
```

Equal endpoint values extend to NAE or its complement; unequal endpoints
extend to MAJORITY or its complement. All three variables remain essential.
Thus both targets can be placed in the range. No support-only singleton or pair
works universally.

### 2.2 Counting existence

Let `F_i` be the allowed truth-table family and

```text
Q = sum_i log2 |F_i|.
```

There are at most `2^Q` circuits and `2^(nk)` ordered witness tuples. Hence at
most `2^(Q+nk)` ordered target lists can be simultaneously covered, while the
number of ordered `k`-lists is `2^(mk)`. Therefore a universal support-only
list exists whenever

```text
k(m-n) > Q.
```

For arbitrary ternary tables, `Q<=8m`, so

```text
k = floor(8m/(m-n)) + 1
```

suffices. At `m=n+n^(2/3)`, this is `O(n^(1/3))`. The result is existential,
not an efficient construction.

### 2.3 The `Eval_H` reduction

`Eval_H` receives all local truth tables and `k` input witnesses, and outputs
the concatenation of the `k` circuit evaluations. Its dimensions are

```text
input  = Q + nk,
output = mk.
```

A missing output is exactly a universal support-only candidate list. Each
output coordinate is an adaptive depth-four decision tree, or a nonadaptive
junta of at most eleven bits. Constructing the counting list is therefore a
structured local range-avoidance problem.

## 3. Exact ternary Fourier lemma

The 256 ternary Boolean predicates partition as

```text
16 affine,
184 non-affine unbalanced,
56 balanced non-affine.
```

There are 16 affine predicates. Of the `binom(8,4)=70` balanced predicates, 14
are nonconstant affine characters or complements, leaving 56.

Let a balanced non-affine sign predicate be `g`. Its constant Fourier
coefficient is zero. If every degree-one and degree-two coefficient vanished,
Parseval would force the cubic coefficient to have magnitude one, making `g`
three-variable parity or its complement. Thus a low-degree coefficient is
nonzero. Inner products between balanced sign vectors on eight points lie in

```text
{-1,-1/2,0,1/2,1}.
```

Magnitude one would again imply affinity. Hence the best degree-one or
degree-two correlation has magnitude exactly `1/2`, giving agreement exactly
`3/4` with a dictator or a two-variable parity, possibly complemented.

The finite census splits the 56 functions into profiles `32+24`: 32 have three
nonzero low-degree coefficients and cubic magnitude `1/2`; 24 have four
nonzero low-degree coefficients and zero cubic coefficient.

This local lemma does not yield a global avoidance certificate. The affine
approximation has coordinate error about `m/4`, much larger than the additive
redundancy `n^(2/3)`, and the known Fourier-to-XOR route still needs strong
global refutation.

## 4. Constant syndromes and four-cycles

Write each gate's algebraic normal form over `F_2` as

```text
C_i(x)=b_i + ell_i(x) + R_i(x),
```

where every monomial in `R_i` has degree at least two.

### Theorem

If distinct supports intersect in at most one variable — equivalently, the
incidence graph is C4-free — an output parity `lambda^T C(x)` is constant if
and only if:

1. every selected gate is affine; and
2. the selected linear parts cancel.

Indeed, any nonlinear monomial selected from gate `i` could occur in another
gate only if the two supports shared all variables of that monomial, hence at
least two variables. C4-freeness makes that monomial unique, so it cannot
cancel.

Consequently, in the high-girth branch constant syndromes reduce exactly to
affine-subsystem dependencies and are found by Gaussian elimination.

A seven-output, six-input committed witness has a nonlinear constant syndrome
on four gates whose neighborhood has size six, so that selector is not Hall
deficient. The witness necessarily contains a C4. Thus algebraic certificates
can beat Hall deficiency before high-girth extraction, and the advantage
vanishes precisely when shared support pairs disappear.

## 5. Remote points from pair counting

For radius `r`, define

```text
B(m,r) = sum_{j=0}^r binom(m,j).
```

For an output prefix `p`, let

```text
A_r(p) = # {(x,z): z extends p and d_H(C(x),z)<=r}.
```

Then

```text
A_r(empty)=2^n B(m,r),
A_r(p)=A_r(p0)+A_r(p1).
```

If `2^n B(m,r)<2^m`, maintain the invariant

```text
A_r(p) < 2^(m-|p|)
```

by choosing a child satisfying the corresponding half-capacity inequality. At
a full target the nonnegative integer count is below one and therefore zero.
The output is farther than `r` from the entire range.

Writing `sigma=m-n` and using `B(m,r)<=(em/r)^r` gives the conservative radius

```text
r = Omega(sigma/log m).
```

At `sigma=n^(2/3)`, the distance is `Omega(n^(2/3)/log n)`.

## 6. Source-level composition with V75

V75 compiles the paired generating polynomial

```text
P_C(z) = sum_x product_i z_(i,C_i(x))
```

into a monotone arithmetic DAG of size `S`; under its supplied branch
decomposition, `S=O(m A(b)^2)` in the V75 notation.

Evaluate the same DAG in the truncated semiring

```text
Z[t]/(t^(r+1)).
```

For prefix coordinate `i`, assign paired-variable weights

```text
1 to agreement, t to disagreement.
```

For an unpinned coordinate, assign `1+t` to both paired variables. For each
input `x`, the product becomes

```text
t^(prefix mismatches) (1+t)^(remaining coordinates).
```

Therefore the coefficient of `t^d` is exactly the number of pairs `(x,z)` at
Hamming distance `d`, and the sum through degree `r` equals `A_r(p)`.

The branch tree and residual states are unchanged. Evaluating from scratch for
the two children at each of `m` prefix levels, with naive truncated
convolution, costs

```text
O(m S r^2 poly(n+m))
```

bit operations up to standard integer-arithmetic factors; coefficients have at
most `O(n+m)` bits. Hence every regime where the V75 DAG is polynomial-size —
in particular fixed bounded branchwidth — has a deterministic polynomial-time
remote-point algorithm with distance `Omega((m-n)/log m)`.

This composition is implemented in `distance_semiring.py` and audited against
brute force on cumulative prefix counts, exact distance coefficients, and
constructed radius-one remote points.

## 7. Nonclaims

V85 does not efficiently construct the existential `Eval_H` list, solve the
unrestricted logarithmic Hall-expander branch, prove locality-three
surjectivity hardness, inherit proof-complexity lower bounds automatically,
construct a rigid matrix, prove a new unrestricted circuit lower bound, or
resolve `P` versus `NP`. Novelty and peer-review status remain unconfirmed.
