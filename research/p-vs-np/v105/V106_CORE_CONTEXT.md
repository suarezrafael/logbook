# V106 core context — adaptive pair selection for signed majority

## Starting point

V105 proves a polynomial missing-output construction when the **canonical**
first-two-variable pair graph contains a simple bicyclic odd barbell or
figure-eight. This uses only one of the three exact pair clauses available from
each signed-majority target.

A signed-majority gate on variables `(u,v,w)` actually offers three possible
pair transports:

```text
delta_uv = 1 XOR p_u XOR p_v,
delta_uw = 1 XOR p_u XOR p_w,
delta_vw = 1 XOR p_v XOR p_w.
```

They always satisfy

```text
delta_uv XOR delta_uw XOR delta_vw = 1.
```

Thus every output contributes an **odd signed triangle of selectable pair
edges**. V105 fixes one edge in advance; V106 should exploit the freedom to
choose one of the three pairs before choosing the output target.

## Preliminary evidence — not a theorem

The smallest canonical theta core can evade the fixed-pair V105 detector. When
one pair is allowed to be selected independently from each output, however, an
unsatisfiable implication witness appears immediately.

A brute-force falsification search over pair choices and target bits then found:

- an apparent `n=3,m=4` counterexample, but it was degenerate: two output gates
  represented the same signed-majority function under support permutation, so a
  missing output is immediate by assigning those two output bits differently;
- after excluding pairs of outputs that are identical or complementary as
  Boolean functions, all **16 exhaustive nondegenerate `n=3` function classes**
  admitted a one-pair-per-output contradiction;
- no counterexample in the recorded random nondegenerate samples at `n=4`,
  `n=5`, or `n=6`.

These searches used exponential enumeration of pair/target choices. They are
hypothesis evidence only and do not imply a polynomial algorithm.

## Track A — polynomial selector theorem

Define the pair-selection problem:

> choose one of the three input pairs for each signed-majority output and then
> choose the output target so that the selected 2-CNF pair clauses are
> unsatisfiable.

The highest-value target is a polynomial algorithm that either finds such a
selection or returns a simple structural obstruction.

Potential formulations:

- partition-matroid style selection: exactly one pair edge from each output
  triangle;
- signed-cycle/bicycle packing with one edge per color class (output);
- target-compatible GraphSAT minor search under edge colors;
- parity matroid or delta-matroid formulations using the odd-triangle identity.

Do not infer tractability from the small searches; exact selection currently has
an obvious `3^m 2^m` brute-force formulation.

## Track B — smallest genuine obstruction

In parallel, search systematically for a nondegenerate circuit with `m>n` for
which **every** one-pair-per-output selection and every target assignment yields
a satisfiable pair formula.

Exclude trivial cases first:

- identical output functions;
- complementary output functions;
- literal-graph peels already solved by V100;
- switching-balanced components already solved by V98;
- proper positive-surplus subcircuits already covered by earlier decomposition.

If a genuine obstruction exists, minimize it by inputs, outputs, support
multiplicity and switching class. Its structure should determine whether V106
needs two pair clauses from some gate, all three clauses, or a non-2-SAT
certificate.

## Track C — use all three exact clauses

A fixed target automatically selects all three pair clauses, not just the one
used by the transport proof. Even if one-pair selection fails, these extra
clauses can create implication SCCs that are invisible in the selected support
graph.

A broader formulation may attach a target variable `y_e` to each output and
analyze how the three induced clauses change as `y_e` flips. Seek a polynomial
criterion for choosing `y` so the resulting 2-SAT instance is inconsistent.

## Relation to known GraphSAT structure

Karve--Hirani characterize simple support graphs that can support **some**
unsatisfiable 2-CNF by four forbidden topological minors. V105 independently
classifies which transport signings of those four skeletons are compatible with
the restricted complementary clauses induced by signed majority.

V106 should not rediscover those support obstructions. The new object is a
**colored selection problem**: each majority output supplies three candidate
pair edges but one common target bit controls the associated clauses.

## Relation to P versus NP

Even a polynomial algorithm for all signed-majority `NC0_3-Avoid` would solve
only one residual predicate orbit. It would be a substantial range-avoidance
advance, not a P-versus-NP proof by itself.

If an all-signed-majority theorem is obtained, immediately recompute the
post-V100 residual NPN orbits and test whether restrictions, substitutions or
hybrid reductions transfer the method to the remaining balanced-nonaffine
orbits before invoking any published lower-bound transfer.

## Promotion criterion

V106 must provide at least one of:

1. a polynomial pair-selector theorem with a proved guarantee;
2. an all-signed-majority exact-stretch theorem using selectable/all three pair
   clauses;
3. a rigorous smallest scalable nondegenerate obstruction that falsifies the
   selector hypothesis and forces a new invariant.

More finite sampling alone is not sufficient.
