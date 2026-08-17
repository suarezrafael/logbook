# V105 literature boundary

## Primary range-avoidance references checked

The laboratory rechecked the primary range-avoidance line around the V105
signed-majority result.

- Gajulapalli--Golovnev--Nagargoje--Saraogi, *Range Avoidance for Constant-Depth
  Circuits: Hardness and Algorithms* (ECCC TR23-021), gives the general
  `NC0_3-Avoid` hardness/algorithm boundary.
- Kuntewar--Sarma, *Range Avoidance in Boolean Circuits via Turan-type Bounds*
  (ECCC TR25-034), gives deterministic polynomial-time monotone `NC0_3-Avoid`
  for `m>n`, a symmetric `NC0_3` algorithm at larger stretch, and a majority
  special case at quadratic stretch.
- Huang--Li--Zhong, *Range Avoidance and Remote Point: New Algorithms and
  Hardness* (ECCC TR25-049 and revisions), is the current general algorithmic
  and transfer calibration used by the laboratory.

Targeted searches for combinations of signed majority, range avoidance, 2-SAT,
implication graphs and signed bicycles did not locate the exact target-selection
specialization used by V105. Search absence is not evidence of novelty.

## Direct 2-SAT structural prior art

Karve--Hirani, *The complete set of minimal simple graphs that support
unsatisfiable 2-CNFs* (Discrete Applied Mathematics 283, 2020; arXiv:1812.10849),
gives a complete forbidden-topological-minor characterization of simple support
graphs on which **some** reduced unsatisfiable 2-CNF can live. Their four fixed
obstructions are

```text
K4,
Butterfly,
Bowtie,
K_{1,1,3}.
```

This is directly relevant. In particular, V105's original dumbbell is a Bowtie
subdivision, and a figure-eight is a Butterfly subdivision. Those support shapes
must not be described as novel V105 structures.

Karve--Hirani allow arbitrary literal choices on 2-CNF edges. V105 has a stricter
compatibility constraint inherited from the majority gate: for a canonical pair
edge, the local literal polarities fix one XOR transport sign, and the output
target selects only one of two complementary pair clauses.

The independent V105 census enumerates every transport-sign assignment and every
target choice on the four fixed obstruction skeletons. It obtains:

```text
K4:        compatible iff all four triangles are odd,
Butterfly: compatible iff both triangles are odd,
Bowtie:    compatible iff both triangles are odd,
K1,1,3:    compatible iff exactly two of the three triangles are odd.
```

Thus the laboratory-specific question is **signed target compatibility on known
2GraphSAT obstructions**, not the existence of those obstructions themselves.

A useful negative control is `K4` minus one edge: it has five edges on four
vertices but contains none of the four forbidden topological minors. Exact
enumeration confirms that no choice of the restricted canonical pair clauses is
unsatisfiable. This matches the GraphSAT boundary and disproves the tempting
claim that pair-edge surplus alone suffices.

## What V105 does and does not overlap

V105 does **not** claim a new algorithm for monotone majority: that is already
inside the Kuntewar--Sarma monotone theorem at exact stretch.

The strict V105 family deliberately inserts a literal-sign inconsistency so the
whole positive-surplus component is not switching-equivalent to monotone under
the V98 incidence equations. Its certificate uses the exact 2-CNF clauses inside
a fixed signed-majority target and transports literals along the canonical pair
graph.

The current polynomial detector handles simple bicyclic canonical-pair
components whose 2-core is a signed barbell or figure-eight with both cycles
odd. It identifies the core by leaf pruning and degree/path tracing, rather than
claiming a new general topological-minor algorithm.

## Novelty discipline

The ingredients—2-SAT implication graphs, signed graph parity, majority's
binary-clause characterization, and barbell/bicycle obstructions—are standard or
have direct prior art. The exact composition with signed-majority target choices
for range avoidance may also be known; this has not been ruled out.

V105 must not be presented as novel, priority-establishing, or peer reviewed
without external specialist review.

## External validation target

Before any novelty claim, ask experts in range avoidance / Boolean CSPs whether
the following specialization is known:

> Given a signed-majority `NC0_3` circuit, use the two target-selectable
> complementary clauses on each canonical input pair.  A simple bicyclic pair
> component whose barbell/figure-eight cycles both have odd transport yields a
> contradictory implication SCC and therefore a deterministic missing output.

Also ask whether the exact compatibility conditions for the four Karve--Hirani
obstructions have appeared under another signed-CSP or switching formulation.
