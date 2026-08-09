# Laboratory V93 — affine-syndrome comparison no-go theorem

## 1. Certificate model

For an explicit `NC0_k` circuit `C=(C_0,...,C_{m-1}):{0,1}^n->{0,1}^m`, define the **global affine-syndrome certificate**

```text
AS(C) = (H(C), Sigma(C)),
```

where `H(C)` is the ordered list of essential supports and

```text
Sigma(C) = { (lambda,c) in F_2^m x F_2 :
             XOR_i lambda_i C_i(x) = c for every x }.
```

For constant locality, `AS(C)` is polynomial-time constructible. Expand every local truth table in algebraic normal form. Put the coefficient vectors of all nonconstant monomials into a matrix `M`; then the allowed `lambda` are exactly `ker(M)`, and the constant bit is the corresponding dot product with the vector of constant ANF coefficients. Gaussian elimination produces a canonical basis and verifies any claimed relation.

This model is deliberately stronger than the V85 C4 shortcut: it gives the decoder the entire global constant-syndrome relation, not just one found syndrome.

## 2. Track-A lemma: what the certificate can still do

Let `p=(p_0,...,p_{j-1})` be a nonempty canonical prefix. Suppose `Sigma(C)` contains `(lambda,c)` with `lambda_j=1` and `lambda_i=0` for every `i>j`. Then on every input consistent with the prefix,

```text
C_j(x) = c XOR (XOR_{i<j} lambda_i p_i).
```

Therefore one child of the prefix is empty, and `AS(C)` certifies that empty child in polynomial time. This is a genuine positive zero-detection subroutine. It does not compare two nonempty children in general.

## 3. Mandatory affine-comparison falsification theorem

Let `f:{0,1}^3->{0,1}` be any non-affine Boolean function and define

```text
C_f(x1,x2,x3)    = ( f(x), x1, x2, x3 )
C_notf(x1,x2,x3) = (1 XOR f(x), x1, x2, x3).
```

Both are `NC0_3-Avoid[3,4]` instances.

### Theorem 3.1 — identical certificate

`AS(C_f)=AS(C_notf)`.

**Proof.** The essential support of `f` equals the essential support of `1 XOR f`, and the projection supports are identical. If

```text
lambda_0 f(x) XOR lambda_1 x1 XOR lambda_2 x2 XOR lambda_3 x3
```

is constant, then `lambda_0=0` forces all linear coefficients to vanish, while `lambda_0=1` would express `f` as an affine function. Thus the syndrome relation is trivial. The same argument applies to `1 XOR f`. QED.

### Theorem 3.2 — no certificate-only avoided output

The two ranges are disjoint and partition `{0,1}^4`:

```text
Range(C_f) disjoint-union Range(C_notf) = {0,1}^4.
```

**Proof.** For every tail `(x1,x2,x3)`, exactly one first bit equals `f(x)` and the other equals `1 XOR f(x)`. The last three output bits reveal the input exactly. Hence each map is injective with eight outputs, the images are disjoint, and their union has all sixteen words. QED.

### Corollary 3.3 — single-valued no-go

There is no decoder `D:AS(C)->{0,1}^m` that returns a valid avoided word for every `NC0_3-Avoid[n,n+1]` circuit: `C_f` and `C_notf` have the same certificate but no common avoided word.

This closes the certificate-only single-valued-output role of the global affine-syndrome model.

## 4. Canonical comparison collision

Let `w(f)` be the truth-table Hamming weight. At the empty prefix,

```text
N_f(0)=8-w(f),   N_f(1)=w(f),
N_notf(0)=w(f),  N_notf(1)=8-w(f).
```

The V92 rule chooses zero iff `N(0)<=N(1)`. Whenever `f` is unbalanced, the two same-certificate circuits therefore have opposite canonical first bits.

For `f=AND3`:

```text
C_AND :  (N(0),N(1))=(7,1), canonical bit=1
C_NAND:  (N(0),N(1))=(1,7), canonical bit=0.
```

Both child counts are nonzero, so the obstruction is genuinely about comparison rather than empty-child detection.

## 5. High-width minimal-stretch lift

### Lemma 5.1 — zero-stretch high-width backgrounds exist

For arbitrarily large `N`, there exist rank-three support systems with `N` inputs, `N` outputs, and support branchwidth `Omega(N)`.

The proof is the V87 pair-shadow argument with `m=N`: its first `floor(3N/4)` independently sampled ternary supports already yield, after selecting one random pair per support and deleting `O(1)` repetitions, a supercritical sparse random graph with `(3/4+o(1))N` edges. The V87 primal-treewidth transfer then gives linear support branchwidth. The argument only needs those first `3N/4` supports and `m/N->1`, so the zero-stretch specialization is unchanged.

Assign any essential ternary truth table to each support to obtain `H_N:{0,1}^N->{0,1}^N`.

### Theorem 5.2 — high-width affine-syndrome comparison no-go

Form disjoint-variable direct sums

```text
A_N = C_AND  direct-sum H_N,
B_N = C_NAND direct-sum H_N,
```

with the four gadget outputs ordered first. Then

```text
input length  = N+3,
output length = N+4,
stretch       = 1,
support branchwidth = Omega(N),
AS(A_N)=AS(B_N),
canonical first bits are opposite.
```

**Proof.** Disjoint union cannot decrease the branchwidth of the background component. A parity over disjoint variables is constant only when its gadget and background parts are separately constant. The AND/NAND gadget has no nonzero syndrome, so every syndrome of the total circuit is background-only and the certificates coincide. At the empty prefix the background inputs are free, multiplying the gadget child counts by `2^N`; the two orderings remain `(7*2^N,1*2^N)` and `(1*2^N,7*2^N)`. QED.

### Corollary 5.3

No deterministic decoder using only essential supports plus the full global constant-syndrome relation can implement the V92 canonical child comparison on all high-branchwidth `NC0_3-Avoid[n,n+1]` instances.

This is a formal Track-B closure result. It does not rule out algorithms that use additional prefix-conditioned, counting, spectral, tensor, or other circuit information.

## 6. Exhaustive finite falsification gate

The executable audit enumerates all 256 ternary functions. It finds

```text
16 affine,
240 non-affine,
56 balanced non-affine,
184 unbalanced non-affine.
```

For all 240 non-affine functions, the function and its complement have the same `AS` certificate and complementary ranges. For all 184 unbalanced non-affine functions, the canonical first decisions are opposite, giving 92 complement-pair collisions.

The census is a regression/falsification gate, not the proof.

## 7. Scope and nonclaims

V93 does not prove that child comparison is hard when the full circuit is available, prove a lower bound for every high-width certificate model, show PP-hardness of canonical prefixes, improve Huang-Li-Zhong Theorem 1.14, give a new circuit lower bound, establish novelty or peer review, or resolve P versus NP.
