# V93 certificate model

The certificate closed by V93 is exactly

```text
AS(C) = (H(C), Sigma(C)),
Sigma(C) = {(lambda,c): lambda^T C(x)=c for all x}.
```

`H(C)` is the ordered essential-support list. `Sigma(C)` is the complete global constant output-parity relation, not a sampled subset.

For constant-locality circuits this object is efficiently constructible from the explicit truth tables: expand each output in ANF, build the matrix whose columns/rows encode coefficients of nonconstant monomials, compute the kernel describing cancellation of all nonconstant terms, and recover the resulting constant bit from the constant ANF coefficients.

The no-go theorem has deliberately narrow quantifiers:

```text
There is no decoder depending only on AS(C) that, for every target circuit,
(a) returns the V92 canonical child decision, or
(b) returns a single avoided output.
```

It does not constrain decoders that inspect any other function of the truth tables or prefix-conditioned preimages.
