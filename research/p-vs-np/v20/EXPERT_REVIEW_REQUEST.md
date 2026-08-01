# Request for Mathematical Review — V20

Dear researcher,

I am seeking feedback on a short range-avoidance proof candidate for symmetric NC0_3 output gates. I am not claiming priority.

The proposed condition is

```text
m > |V_T| + rank_GF2(A_P) + rank_GF3(A_R),
```

with the uniform corollary `m>3n`. The proof normalizes output complements, uses the published Monotone-NC0_3-Avoid result for thresholds, a left-null certificate for parity, and a GF(3) dependency argument for ternary exact-residue indicators.

I would especially appreciate review of:

1. the completeness of the symmetric-function taxonomy;
2. the exact-residue dependency argument;
3. whether the result or effective-dimension formulation is already known;
4. whether the absence of the symmetric section from later versions of arXiv:2503.17114 was intentional or reflects a known issue.

The package includes a human-readable proof, 342 exhaustive validation cases, and an independently implemented verifier. I will revise or withdraw the claim if a flaw or prior result is identified.
