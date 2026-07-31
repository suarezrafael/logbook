# Affine-Parity Range Certificates for Cubic Four-Input Predicates

## Exact algebraic normal forms

Every Boolean output has a unique multilinear algebraic normal form over `GF(2)`. For the seven hard four-input predicate classes, the local degree is exactly three. Write

\[
f_i(x)=c_i+\langle a_i,\phi(x)\rangle.
\]

Let `A` be the matrix with rows `a_i`, and let `c` be the constant vector.

## Affine parity theorem

Let `H` have rows forming a basis of the left nullspace of `A`. Then `HA=0`, so every range output `y=f(x)` satisfies

\[
Hy=Hc+HA\phi(x)=Hc.
\]

Therefore the range is contained in the affine binary code

\[
\{y\in\mathbb F_2^m:Hy=Hc\}.
\]

Any target with a different syndrome is absent.

## Nullity amplification

If `t=m-rank(A)`, `H` has rank `t`. The affine container contains exactly `2^(m-t)` vectors. Hence at least

\[
2^m-2^{m-t}
\]

outputs are certified as absent, a fraction `1-2^(-t)`.

## Balanced target

Start with an alternating target. If it violates the syndrome, return it. Otherwise flip a coordinate whose column in `H` is nonzero. The syndrome changes and the Hamming weight moves by only one.

## Active-feature bounds

Let `A(C)` denote the union of nonconstant active ANF monomials. Then

\[
rank(A)\le |A(C)|.
\]

Thus `m>|A(C)|` suffices. If `V` is the used vertex set, `partial_2 H` the pair shadow, and `T_active` the active cubic shadow,

\[
|A(C)|\le |V|+|partial_2 H|+|T_active|.
\]

For primal degeneracy `delta`,

\[
m>v\left(1+\delta+\binom{\delta}{2}\right)
\]

is sufficient.

## Smallest local non-complement relation

Among the 1,280 hard truth tables there are 640 nonconstant vectors, each paired with its complement. The smallest non-complement affine relation has size three. One explicit triple is

```text
0x7f80, 0x078f, 0x780f
```

and its outputs always have even parity. Therefore `001`, `010`, `100`, and `111` are absent.

## Limitation

Dense hard-only circuits may attain the full cubic nonconstant feature rank. This theorem changes the form and multiplicity of the certificates but does not establish a subcubic worst-case algorithm for general `NC0_4-Avoid`.
