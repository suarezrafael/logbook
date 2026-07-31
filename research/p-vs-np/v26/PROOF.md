# Mixed Active-Shadow Range Avoidance and the Cubic Redundancy Barrier

## Exact literature alignment

Reconstructing the 400 input-equivalence classes used in the arity-four non-redundancy catalogue gives:

\[
017f\mapsto356,\quad
01bf\mapsto327,\quad
01ef\mapsto321,\quad
01fe\mapsto320,
\]
\[
07f1\mapsto200,\quad
07f2\mapsto199,\quad
07f8\mapsto195.
\]

Each mapped predicate is equivalent to its complement using coordinate permutations and independent input negations.

## Cubic redundancy barrier

Each mapped predicate has an OR3 projection and a degree-three polynomial representation. The projection transfers the \(\Omega(n^3)\) lower bound from OR3, while the polynomial representation gives \(O(n^3)\). Hence

\[
\operatorname{NRD}_n(P)=\Theta(n^3).
\]

This concerns all-ones-except-one targets. It is not a lower bound for arbitrary range avoidance.

## Mixed active-feature theorem

Choose a GF(5) zero-set witness for every four-input local gate. Let \(\mathcal F(C)\) be the union of global monomials with nonzero coefficient. All coefficient rows lie in a space of dimension at most \(|\mathcal F(C)|\). Thus, if

\[
m>|\mathcal F(C)|,
\]

or more generally the coefficient rank is below \(m\), Gaussian elimination finds a nonzero dependency.

Request normalized output one on every dependency-support coordinate except one coordinate \(j\), where output zero is requested. The dependency forces the \(j\)-th polynomial to vanish, contradicting the target.

## Coarse active-shadow bound

Let \(V\) be the variables used, \(\partial_2H\) the pair shadow, and \(T_{\mathrm{active}}\) the cubic monomials appearing in the chosen hard-gate witnesses. Then

\[
|\mathcal F(C)|
\le
1+|V|+|\partial_2H|+|T_{\mathrm{active}}|.
\]

## Degeneracy corollary

If the primal graph is \(\delta\)-degenerate on \(v\) vertices, it has at most \(\delta v\) edges and at most \(\binom{\delta}{2}v\) triangles. Every active cubic monomial is a primal triangle. Therefore

\[
|\mathcal F(C)|
\le
1+v\left(1+\delta+\binom{\delta}{2}\right).
\]

Constant degeneracy gives linear stretch for arbitrary four-input local truth tables.

## Scope

Dense supports may activate all cubic monomials. The theorem is structural and does not improve worst-case general NC0_4-Avoid.
