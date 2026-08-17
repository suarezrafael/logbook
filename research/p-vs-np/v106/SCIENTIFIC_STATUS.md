# V106 scientific status

**Classification:** experimental frontier progress; pending repository CI and promotion gates.

Established in the package:

- a pair-repair parameter `sigma` measuring distance from the V105 canonical-pair class;
- deterministic `O((2m)^sigma poly(N))` range avoidance by bounded repair enumeration;
- the signed-majority transport-triangle identity `d01 XOR d02 XOR d12 = 1`;
- the frame-rank/support-neighborhood identity for unions of all pair candidates;
- the resulting Rado/Hall equivalence for frame-independent one-pair transversals;
- an infinite exact-stretch family with canonical theta signature `(0,1,1)` and `sigma=1`;
- exact strong-affine-backdoor size `beta=(n+3)/2` on that family;
- V101 `mu=n`, V103 `nu=n`, and V104 `eta_AF=n` on the same majority family.

The strict family is minimally positive-surplus: deleting any one output leaves a
perfect support matching, hence every proper output subset satisfies Hall.  A
symbolic matching proof is documented in the theorem ledger; the verifier also
checks the property through growing instances.

Not established:

- a polynomial algorithm for minimizing `sigma`;
- a sublinear or constant worst-case bound on `sigma`;
- an all-signed-majority exact-stretch avoidance theorem;
- a theorem forcing a target-compatible odd handcuff from minimal surplus alone;
- unrestricted polynomial-time `NC0_3-Avoid`;
- a new general circuit lower bound or P versus NP;
- novelty, priority, or peer review.

The next scientific bottleneck is no longer the existence of pair choices in
small examples.  It is the **colorful frame-circuit problem**: after Hall/Rado
puts a minimal surplus family one unit beyond frame independence, determine
whether the forced colorful dependence can be made an odd handcuff rather than
a balanced cycle, or exhibit a scalable obstruction proving that it cannot.
