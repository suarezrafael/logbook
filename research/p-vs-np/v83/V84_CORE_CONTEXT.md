# V84 core context — oracle extraction after exact hardness

## Frozen input from V83

Transversal girth is polynomial-time computable for presentations of left
degree at most two and NP-complete for presentations of left degree at most
three.

The V83 path-selector series expansion gives exact circuit correspondence. In
the left-regular case it scales every circuit cardinality by the common chain
length. Together with the Colbourn–Elmallah Clique presentation, this proves
NP-completeness without unintended short circuits.

Via V82,

```text
h* = minimum Hall-neighborhood = transversal girth - 1.
```

Therefore a polynomial exact optimizer for the first below-diagonal Minimum
`p`-Union point is blocked unless `P=NP`.

## Priority one: exact FP^NP extraction

The next laboratory must exploit, rather than ignore, the complexity result.
Build a deterministic polynomial-time algorithm with an NP oracle that returns:

1. the exact degree-three transversal girth;
2. a canonical shortest circuit;
3. the corresponding minimum-neighborhood Hall witness;
4. a polynomially bounded candidate list tailored to the range-avoidance step,
   or a proof that one shortest circuit is insufficient for that step.

The oracle predicate must be explicit and self-reduction must preserve the
left-degree-three promise. Query complexity and bit complexity must be stated.
Do not call generic binary search a completed candidate-list theorem.

## Priority two: approximation and promise structure

If the candidate-list interface fails, determine which weaker output is enough:

- constant-factor or additive approximation to girth / `h*`;
- enumeration of all shortest circuits under bounded width;
- promised high-branchwidth or large-deficiency certificates;
- a hybrid exact-parameterized algorithm using V77 decomposition discovery.

Every proposal must be tested against the V80–V83 obstruction families.

## Publication audit

Before novelty language, search specifically for:

- bounded-occurrence or bounded-left-degree transversal-matroid girth;
- series extensions of transversal presentations;
- circuit-preserving degree-reduction gadgets for matchings or gammoids.

Record any prior equivalent theorem and downgrade the V83 novelty status
accordingly. The proof remains useful even if the construction is known.

## Nonclaims

The direct P-versus-NP route remains inactive. An `FP^NP` extractor would not
be a polynomial algorithm and would not prove a lower bound.
