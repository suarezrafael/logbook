# Zero-Set Polynomial Dependencies for Symmetric Local Range Avoidance

**Computer-assisted research note — Laboratory V22**

**Author:** Rafael Vieira Suarez  
**Status:** Not peer reviewed. Novelty and priority are not established.

## Abstract

If Boolean outputs are zero-set indicators of polynomials in a `D`-dimensional vector space, then `m>D` yields an avoided output from a nonzero linear dependency. Applying output complementation and finite-field interpolation to symmetric fan-in-`k` gates gives the sufficient threshold

```text
m > sum_{j=0}^{floor((k+1)/2)} binom(n,j).
```

For fan-in four this becomes

```text
m > 1+n+binom(n,2).
```

A separate implementation verified 1,022 symmetric truth tables and 125 complete circuit certificates, including exhaustive range enumeration. The result remains a proof candidate pending external review and prior-art confirmation.

## Why this matters

For symmetric fan-in-four outputs, the sufficient threshold is quadratic rather than the approximately cubic generic deterministic `NC0_4-Avoid` scale. The result remains far above the small-stretch regime associated with major explicit-construction and lower-bound consequences.

## Limitations

- restricted to symmetric local output functions;
- does not solve arbitrary `NC0_4-Avoid`;
- does not establish a general circuit lower bound;
- does not resolve P versus NP;
- novelty has not been confirmed.
