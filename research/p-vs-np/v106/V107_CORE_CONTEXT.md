# V107 core context — colorful frame circuits from minimal surplus

## Starting point

V106 gives two facts that should be treated together:

1. every signed-majority output offers an unbalanced triangle of three candidate
   pair edges;
2. for every gate subfamily `F`, the signed-frame rank of the union of all those
   candidates is exactly `|N(F)|`.

Therefore Rado's independent-transversal condition is exactly support Hall.
For a minimally positive-surplus family with `m=n+1`, every proper gate
subfamily satisfies the independent-transversal inequalities, while the full
family misses them by one.

This is the correct global formulation.  Do not return to larger finite
truth-table censuses.

## Central V107 question

Can a minimally Rado-deficient family of unbalanced candidate triangles be made
to yield a **colorful frame circuit of handcuff type** in polynomial time?

A frame circuit in a signed graph can be a balanced cycle or a handcuff-type
union of unbalanced cycles.  V105/V106 can turn the handcuff case directly into
a missing output.  The balanced-cycle case is the surviving obstruction.

## Track A — fundamental circuit repair

Use matroid intersection to choose an independent transversal for all but one
output.  Add one candidate edge from the missing gate and inspect its fundamental
frame circuit.

Questions:

- if the fundamental circuit is balanced, do either of the missing gate's other
  two candidate edges necessarily yield a handcuff?
- if not, characterize the placement of the three gate vertices relative to the
  unique unbalanced cycle of the selected basis;
- bound the number of local exchanges needed to escape a balanced circuit.

A theorem giving `O(1)` exchanges would immediately strengthen V106's `sigma`
parameter on minimally positive-surplus families.

## Track B — colorful/rainbow circuit algorithms

Search prior art for:

- rainbow circuits in matroids;
- colorful circuits under a partition matroid;
- circuit transversals for minimally Rado-deficient set systems;
- signed-graphic/frame-matroid specializations.

Do not assume the general colorful-circuit problem is polynomial.  If general
versions are hard, isolate which extra property matters here: every color class
is exactly the three edges of an unbalanced triangle.

## Track C — balanced-cycle obstruction family

In parallel, construct scalable instances in which every maximum
frame-independent transversal plus every single missing-gate edge produces a
balanced fundamental cycle.  If such families exist, measure the required
repair distance `sigma`.

Promotion-worthy negative outcomes include:

- an infinite family with `sigma=Omega(log n)` or `Omega(n)`;
- a reduction showing that minimizing `sigma` is NP-hard even for majority
  triangle color classes;
- a structural invariant explaining why pair-selection cannot cover all signed
  majority.

## Track D — all-signed-majority consequence

If the balanced-cycle obstruction is eliminated in polynomial time, immediately
combine:

```text
minimal surplus extraction
+ Hall/Rado pair selection
+ colorful handcuff construction
+ V105 implication target
```

and test whether this yields exact-stretch polynomial avoidance for every
essential signed-majority component.  Only after that should the laboratory
recompute the residual NPN orbits and assess consequences for general
`NC0_3-Avoid` and published lower-bound transfers.

## Stop rule

V107 must not be promoted for another constant-sigma example.  Require one of:

1. a polynomial handcuff/colorful-circuit selector for a substantially broader
   infinite class;
2. a proven asymptotic bound on `sigma`;
3. a scalable balanced-cycle obstruction or hardness result.
