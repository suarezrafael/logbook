# V88 literature boundary

## Internal results

The following statements are proved directly in the V88 packets and verified
by executable audits:

- the collision normal form for repeated-table `Eval_H`;
- universal coverability of two-row target lists;
- the exact three-row labeled-hypergraph reduction;
- the fourteen-active-output lower barrier for three-row obstructions;
- the implication from Property B to coverability of every three-row target;
- the finite Property-B censuses for the V80 controls and V87 samples.

## External theorem used

V88 imports one asymptotic random-hypergraph theorem:

- Dimitris Achlioptas and Cristopher Moore,
  **On the 2-Colorability of Random Hypergraphs**, RANDOM 2002,
  Lecture Notes in Computer Science 2483, pages 78–90.

Their model `H_k(n,m)` selects `m` uniform `k`-subsets independently with
replacement. They prove that `H_k(n,rn)` is two-colorable with high probability
when

```text
r <= 2^(k-1) ln 2 - (ln 2)/2 - 1.
```

At `k=3`, the right-hand side is

```text
(7/2) ln 2 - 1 = 1.4260151319... .
```

V88 uses only the fixed-density consequence at `r_0=5/4`.

## Model conversion to V87

The V87 support model also samples ternary supports independently and uniformly
with replacement before imposing the simple-support event. Its density is

```text
(n+ceil(n^(2/3)))/n -> 1.
```

For all sufficiently large `n`, it is a subgraph, under the natural ordered-edge
coupling, of `H_3(n,ceil((5/4)n))`. Since two-colorability is preserved by edge
deletion, the Achlioptas–Moore theorem implies Property B for the V87 model
with high probability.

The V87 collision estimate separately shows that repeated supports occur with
probability `o(1)`. Therefore the Property-B conclusion survives intersection
with the simple-support event used by the V87 obstruction theorem.

## What the source does not supply automatically

The random-hypergraph theorem does not:

- construct a deterministic support family;
- produce a four-row missing output;
- solve `Eval_H` or unrestricted `NC0_3-Avoid`;
- imply Hall expansion or high branchwidth;
- establish a circuit or proof-complexity lower bound;
- resolve `P` versus `NP`.

Those distinctions remain explicit in `PROPERTY_B_BOUNDARY.md`.

## Adjacent areas requiring a separate source audit

Future work may touch:

- separating hash families and perfect hash families;
- small-bias sets and splitters;
- labeled hypergraph coloring beyond three rows;
- deterministic CSP unsatisfiability constructions;
- remote-point algorithms for structured local maps.

Before a later V88 or V89 claim uses one of these areas, the exact statement,
parameter scale, uniformity, and constructivity assumptions must be checked
against a primary source.

## Novelty discipline

The collision normal form and Property-B composition are useful internal
reductions, but no literature-first novelty claim is made. The constructor
lower bound concerns the precise model of support-dependent ordered lists with
at most three target rows. It should not be presented as an unrestricted lower
bound for range avoidance.

No claim is made that V88 resolves `P` versus `NP`, proves a new circuit lower
bound, constructs rigid matrices, or has passed external peer review.
