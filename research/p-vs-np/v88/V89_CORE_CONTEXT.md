# V89 core context — four rows after the Property-B boundary

V89 is not active while V88 remains a candidate.

## Frozen starting point from V88

1. Repeated-table `Eval_H` coverability has an exact collision normal form with
   alphabet `2^(k-1)`.
2. Every two-row target list is coverable.
3. Three-row coverability is an exact labeled three-color hypergraph problem.
4. Every three-row target with at most fourteen active simple ternary outputs is
   coverable.
5. Property B implies coverability of every three-row target matrix.
6. The V87 random support model has Property B with high probability because
   its density tends to one, below the Achlioptas–Moore certified random
   3-uniform two-colorability density.
7. One target-stretch family therefore simultaneously has local Hall expansion,
   no constant `NOR3` syndrome, linear branchwidth, and Property B.
8. Consequently, no support-dependent ordered list of at most three target rows
   is universal. The constructor-model lower bound is four rows.
9. V88 does not construct a four-row missing output.

## Priority one — exact four-row geometry

For four target rows, normalized variable patterns lie in `{0,1}^3`. Quotient
these eight patterns by the row-pair separation relations they induce. Seek a
small combinatorial representation analogous to the three-row labeled-color
model.

Required deliverables:

- exact classification of the eight patterns and their six row-pair cuts;
- canonical constraint types for a ternary support;
- a primary and independent satisfiability engine;
- complete smallest-scale censuses;
- explicit separation between a finite obstruction and an asymptotic
  support-only constructor.

## Priority two — explicit four-row obstruction

Search first on:

1. the three V80 controls;
2. deterministic V87 samples;
3. minimal non-Property-B ternary hypergraphs;
4. target-stretch families near the smallest admissible scales.

A valid obstruction must be a target matrix determined from the support family
alone. Record whether it survives row permutation, target complementation, and
support automorphisms.

## Priority three — stronger constructor lower bounds

If four-row search remains satisfiable, formalize and rule out one precise
constructor class, such as:

- row-separable targets;
- affine or low-degree target columns;
- cyclic/automorphism-invariant constructors;
- bounded seed families;
- tensor products of constant-size gadgets.

Every lower bound must name the constructor model exactly and must not be
presented as unrestricted range-avoidance hardness.

## Priority four — deterministic non-Property-B obstruction families

The V87 probabilistic family is usually two-colorable, so the three certificate
barriers do not imply a small missing-output list. Seek explicit non-Property-B
families while preserving target stretch, local Hall expansion, support
uniqueness, and large branchwidth.

## Discipline

Do not infer proximity to `P != NP` from the four-row lower bound. Every
asymptotic claim must preserve

```text
m=n+ceil(n^(2/3)),
```

polynomial-time constructibility, and the distinction between existential and
efficiently generated target lists.
