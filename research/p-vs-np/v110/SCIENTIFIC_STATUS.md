# V110 scientific status

## Established inside the candidate package

- A V109 one-gate bottleneck can be upgraded by giving only the bottleneck output capacity two.
- If the resulting two return routes share exactly that output and require the same target bit on it, their two opposite-phase contradictions compose into one missing output.
- The certificate is recognized and lifted in deterministic polynomial time.
- There is an infinite exact-stretch family with `n=4k+2`, `m=n+1`, distinct central supports, a forced V109 bottleneck, and a V110 shared-gate certificate.
- The strict family is Hall-minimal and has no V108 SCC-separated certificate under any deletion budget.
- Its V102 strong-affine backdoor is exactly `beta = 2 + 4 ceil(k/2) = Theta(n)`.
- Primary and implementation-independent verifier suites are present.

## Still open

- The `phase-conflict` residual, where the two routes demand opposite target bits on the shared MUX.
- The `nested-bottleneck` residual, where capacity two on the first bottleneck still leaves max-flow one.
- Polynomial-time avoidance for every essential MUX/bijunctive `0x1b` circuit.
- Unrestricted `NC0_3-Avoid`.
- Any new general circuit lower bound.
- P versus NP.

## Validation status

The claim is currently internal to the laboratory. Targeted primary-source calibration still places low-stretch `NC0_3` range avoidance at a difficult frontier; the 2025 Kuntewar--Sarma result gives exact-stretch polynomial time for monotone `NC0_3` and a larger-stretch result for majority, not a matching MUX shared-gate theorem. Search absence is not novelty evidence. No novelty, priority, or peer-review claim is made.
