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

Targeted searches for combinations of

```text
signed majority + range avoidance + 2-SAT,
majority + implication graph + range avoidance,
dumbbell/bicycle + range avoidance
```

did not locate the exact V105 construction.

## What V105 does and does not overlap

V105 does **not** claim a new algorithm for monotone majority: that is already
inside the Kuntewar--Sarma monotone theorem at exact stretch.

The strict V105 family deliberately inserts a literal-sign inconsistency so the
whole positive-surplus component is not switching-equivalent to monotone under
the V98 incidence equations. The new certificate then uses a different fact:
a fixed signed-majority output target contains three exact binary clauses, and a
selected pair clause can transport a literal through a signed graph path.

The resulting odd-triangle-dumbbell contradiction is therefore best understood
as a 2-SAT implication certificate inside a restricted signed-majority regime,
not as a new Turan theorem for monotone circuits.

## Novelty discipline

Search absence is not evidence of novelty. The ingredients—2-SAT implication
graphs, signed graph parity, majority's binary-clause characterization, and
dumbbell/bicycle obstructions—are standard or classical in adjacent areas.

The laboratory has not established whether their exact composition for
exact-stretch signed-majority range avoidance is known. V105 must not be
presented as novel, priority-establishing, or peer reviewed without external
specialist review.

## External validation target

Before any novelty claim, ask experts in range avoidance / Boolean CSPs whether
the following exact statement is known:

> A signed-majority `NC0_3` circuit whose canonical pair graph contains two
> vertex-disjoint odd-transport triangles connected by a disjoint path admits a
> deterministic polynomial-time missing-output construction via a contradictory
> 2-SAT implication SCC.

A useful prior-art search should also include signed 2-SAT bicycles, implication
minors, switching classes of majority constraints, and oriented Boolean CSPs.
