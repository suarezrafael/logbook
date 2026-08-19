# V110 literature boundary

## Primary range-avoidance calibration

The current external calibration remains conservative.

- Kuntewar and Sarma, **Range Avoidance in Boolean Circuits via Turan-type Bounds** (ECCC TR25-034 / arXiv:2503.17114), give deterministic polynomial-time algorithms for monotone `NC0_3-Avoid` at exact positive stretch `m>n`, for symmetric `NC0_3-Avoid` at larger linear stretch, and for majority outputs at substantially larger stretch. Their stated results do not supply the V110 signed-MUX shared-gate composition theorem.
- The broader range-avoidance literature continues to treat low-stretch `NC0_3` as a difficult regime connected to explicit construction and lower-bound questions.

V110 should therefore be described only as an internally proved certificate class for the essential MUX/bijunctive orbit. A targeted search did not reveal a prior theorem matching the exact combination

```text
V109 one-gate bottleneck
+ capacity-two upgrade on that output only
+ two otherwise gate-disjoint return cycles
+ equality of the required target bit on the shared MUX
=> constructive missing output.
```

Failure to find such a theorem is **not** evidence of novelty or priority.

## Standard ingredients that are not novelty claims

V110 uses standard tools and facts:

- max-flow/min-cut and integral flow decomposition;
- Menger-style gate-capacity reasoning;
- implication-graph semantics of 2-CNF;
- Hall matching for support minimality;
- the strong affine-backdoor rule already established in V102.

Any eventual novelty claim would have to concern the range-avoidance-specific composition and its strict separation from the preceding laboratory methods, not these standard ingredients.

## External validation targets

Before strong dissemination, ask an external complexity theorist to check:

1. the exact 2-CNF encoding of a signed MUX fixed-output fiber;
2. the single-shared-output target-compatibility lemma;
3. whether upgrading only the V109 bottleneck truly guarantees output-gate disjointness everywhere else after flow decomposition;
4. the infinite-family claims: Hall minimality, absence of V108 certificates, forced V109 bottleneck, and exact `beta`;
5. prior art in bijunctive/CSP range avoidance, signed implication graphs, and low-stretch `NC0_3-Avoid`.
