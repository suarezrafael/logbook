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

Thus every output contributes an **unbalanced signed triangle of three selectable
pair edges**. V105 fixes one edge in advance; V106 should exploit the freedom to
choose one of the three pairs before choosing the output target.

## Stronger falsification evidence — still not a theorem

The smallest canonical theta core can evade the fixed-pair V105 detector. When
one pair is allowed to be selected independently from each output, however, an
unsatisfiable implication witness appears immediately.

A brute-force falsification search then found:

- an apparent `n=3,m=4` counterexample, but it was degenerate: two output gates
  represented the same signed-majority function under support permutation, so a
  missing output is immediate by assigning those two output bits differently;
- after excluding identical/complementary output-function pairs, all **16
  exhaustive nondegenerate `n=3` function classes** admitted a one-pair-per-
  output contradiction;
- after quotienting signed-majority gates by output complement, `n=4` has 16
  gate classes; **all 4,368 choices of five distinct classes** were exhaustively
  checked, and every circuit admitted a pair-selection contradiction;
- an additional **20,000 random nondegenerate `n=5,m=6` circuits** were checked
  with no counterexample, on top of the earlier `n=4..6` random samples.

The exact search uses exponential enumeration of pair choices, with assignment
sets represented as bit masks. These results are hypothesis evidence only.

## Matroidal formulation

The selectable-pair system has a natural signed-graphic interpretation.

For each output gate create its three candidate pair edges, carrying the
transport labels above. The three edges form an unbalanced triangle. Partition
the candidate edge set into one three-element color class per output; V106 seeks
one representative edge from every color class.

The **frame matroid of a signed graph** is directly relevant. Its independent
sets have no balanced cycle and at most one unbalanced cycle in each connected
component. Its circuits include:

```text
balanced cycles,
two unbalanced cycles sharing one vertex,
two vertex-disjoint unbalanced cycles joined by a path.
```

The last two circuit types are exactly the tight/loose handcuffs underlying the
V105 implication construction.

Rado's matroid-transversal theorem says that a family of candidate sets has an
independent transversal precisely when every subfamily has sufficient matroid
rank. Since a frame matroid on `n` input vertices has rank at most `n`, a full
frame-independent transversal of `m>n` output triangles cannot exist.

This **does not yet prove V106**: a forced frame-matroid circuit may be a balanced
cycle rather than an unbalanced handcuff, and a balanced cycle alone does not
make the selected 2-CNF unsatisfiable. The missing theorem is an exchange or
selection argument showing that the odd-triangle color classes let us avoid the
balanced-cycle failure mode or convert it into a target-compatible obstruction.

This is now the preferred proof route because it explains both the exact-stretch
threshold and the V105 handcuff structure without a `3^m` search.

## Track A — frame-matroid transversal / exchange theorem

Let `T_e` be the unbalanced signed triangle of three candidate pair edges for
output `e`. Study a maximum transversal that is independent in the signed-graphic
frame matroid.

A minimal Rado-deficient subfamily has rank one below its number of color
classes. Represent all but one class by an independent transversal `I`. Every
edge of the final unbalanced triangle then lies in the closure of `I` and creates
a fundamental frame circuit.

The key question is:

> Can all three fundamental circuits be balanced cycles, under the odd parity of
> the omitted output triangle, without exposing a trivial equal/complement
> output relation or an exchange that moves to an unbalanced handcuff?

For a tree component of `I`, the three closure signs around a triangle have even
parity, so an unbalanced omitted triangle necessarily contains an augmenting
edge. The difficult case is when all three gate vertices lie inside an already
unbalanced unicyclic component, where closure alone does not distinguish a
balanced-cycle circuit from a handcuff.

A successful exchange lemma for that case would turn the small computational
pattern into a polynomial matroid-intersection/transversal algorithm.

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
multiplicity, switching class and the Rado-deficient frame-matroid subfamily. Its
structure should determine whether V106 needs two pair clauses from some gate,
all three clauses, or a non-2-SAT certificate.

## Track C — use all three exact clauses

A fixed target automatically supplies all three pair clauses, not just the one
used by the transport proof. Even if one-pair selection fails, these extra
clauses can create implication SCCs invisible in the selected support graph.

A broader formulation may attach a target variable `y_e` to each output and
analyze how the three induced clauses change as `y_e` flips. Seek a polynomial
criterion for choosing `y` so the resulting 2-SAT instance is inconsistent.

## Relation to known GraphSAT and minimal-unsatisfiability structure

Karve--Hirani characterize simple support graphs that can support **some**
unsatisfiable 2-CNF by four forbidden topological minors. V105 independently
classifies which transport signings of those four skeletons are compatible with
the restricted complementary clauses induced by signed majority.

Separately, minimally unsatisfiable 2-CNFs are known to have a weak-double-cycle
implication structure, and general work on deficiency/matching autarkies warns
that finding a desired deficiency-one MUS can be hard in less structured
settings. V106 therefore must exploit the special unbalanced-triangle color
classes; generic MUS machinery alone is not a polynomial-selector proof.

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

1. a polynomial pair-selector theorem, preferably via a frame-matroid
   transversal/exchange argument;
2. an all-signed-majority exact-stretch theorem using selectable/all three pair
   clauses;
3. a rigorous smallest scalable nondegenerate obstruction that falsifies the
   selector hypothesis and forces a new invariant.

More finite sampling alone is not sufficient.
