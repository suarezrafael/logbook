# V91 naturalness and barrier audit

This document separates three statements that must not be conflated:

1. an efficiently verifiable certificate on a succinct circuit or support
   description;
2. a property that occurs often in a chosen random structured model;
3. a Razborov--Rudich natural property on Boolean truth tables that is
   constructive, large, and useful against a precise circuit class.

Only the third statement invokes the natural-proofs barrier.

## 1. Audit protocol

For every proposed lower-bound property `P_n`, record:

```text
universe       = all truth tables of n-variable Boolean functions, or another
                 explicitly justified universe
representation = full truth table, succinct circuit, support hypergraph, etc.
constructive   = deterministic recognition complexity measured in the required
                 representation
large          = density of P_n in the stated universe
useful         = circuit class and size bound excluded by membership in P_n
cryptographic assumption = exact PRF/PRG hardness assumption used by the barrier
```

A row is marked `natural` only when constructivity, largeness, and usefulness
are all proved in the same universe and at compatible parameters.

Witness verification is not the same as deterministic recognition. A property
in NP because a certificate can be checked in polynomial time is not thereby a
P-constructive natural property.

## 2. Relativization and algebrization protocol

### Relativization

Ask whether every machine, reduction, and diagonalization step remains valid
relative to an arbitrary oracle. If it does, compare the target separation with
known oracle worlds. A relativizing proof cannot alone settle a separation that
has both positive and negative relativized worlds.

This does not imply that a relativizing structural lemma, restricted circuit
lower bound, or algorithmic theorem is valueless.

### Algebrization

Ask whether the argument remains valid when machines receive both oracle access
and access to a low-degree extension of the oracle. Record the exact class
inclusion or separation known to algebrize in opposite directions. Do not label
an argument `nonalgebrizing` merely because it uses algebra.

## 3. Retroactive certificate audit

| Mechanism | Efficient on laboratory representation? | Large in relevant truth-table universe? | Useful against a strong circuit class? | Formal natural-property status | Operational status |
|---|---:|---:|---:|---|---|
| small Hall deficiency | yes on explicit supports | not proved; the V86/V87 resistant model avoids the targeted local deficiencies | gives an avoidance algorithm on one branch, not a general circuit lower bound | not established | closed as a generic certificate route |
| constant output syndrome | yes by linear algebra for the represented circuit | not proved; simple `NOR3` supports have no nonzero syndrome | solves selected avoidance instances, not a truth-table lower-bound property | not established | closed as a generic certificate route |
| low support branchwidth | decomposition is FPT; a supplied decomposition is efficiently checkable | false on the V87 resistant model and not defined on the full truth-table universe | gives a parameterized algorithm, not a strong circuit lower bound | not established | retained only as an algorithmic parameter |
| Property B / support two-coloring | a coloring witness is efficiently verifiable, but deterministic recognition is not supplied | not a truth-table density statement | yields constant-row coverability in the constructor model | not established | constructor-specific; no new generic certificate search |
| basis coloring / eight-row addressing | a proposed coloring is efficiently verifiable | not a truth-table density statement | constant-row addressing only | not established | bounded by the V90 stop rule |
| collision normal form | exact and efficiently checkable for a fixed target list | not a truth-table property | reformulates coverability; no strong lower-bound usefulness | not established | retained as infrastructure |

## 4. What V86 and V87 actually prove

V86 and V87 do not prove the natural-proofs barrier for the certificate ladder.
They prove an internal structural no-go:

1. one simple rank-three family can avoid the small-Hall certificate;
2. assigning `NOR3` removes every nonzero constant syndrome;
3. the same random support model has linear support branchwidth;
4. therefore the three accumulated mechanisms do not cover even that one
   resistant family.

This is sufficient to close indiscriminate certificate accumulation. It is not
sufficient to conclude that every future polynomial-time certificate is barred
by Razborov--Rudich.

## 5. Reopening rule

A certificate program may be reopened only if its proposal proves one of:

- the induced lower-bound property is useful but quantitatively non-large;
- deterministic recognition is intentionally outside the constructivity
  regime of the relevant natural-proofs theorem;
- the property is defined on an explicit function or a thin promise universe
  and the exact bridge to a recognized lower bound is supplied;
- an interactive, algebraic, proof-complexity, or nondeterministic mechanism
  is used with a theorem explaining why the prior audit does not apply;
- a parameter-preserving reduction turns the certificate into progress on a
  named complete or frontier problem.

Merely changing the local predicate, certificate syntax, random generator, or
finite search scale is not an escape clause.

## 6. Barrier audit for the Williams front

The algorithms-to-lower-bounds method must not be described as escaping natural
proofs simply because it contains nondeterminism.

The safer statement is:

- the proof derives a lower bound from a nontrivial SAT or `#SAT` algorithm plus
  hierarchy/diagonalization machinery;
- it does not proceed by presenting a large, efficiently recognizable useful
  truth-table property of the standard Razborov--Rudich form;
- the exact reason the framework avoids the largeness condition must be taken
  from the selected primary theorem, not inferred from a slogan.

The V91 theorem audit must separately record relativization and algebrization
behavior of the chosen transference result.

## 7. Permanent conclusion

The certificate ladder is closed because it lacks an external implication chain
and because the laboratory proved a common resistant family, not because a
formal natural-property theorem has already been established.

Future documents must use one of these labels:

```text
formal natural property
candidate natural property
compatible with a natural-proofs warning
not in the natural-proofs formalism as stated
barrier status unknown
```

The phrase `Razborov--Rudich explains the experiment` is prohibited unless the
constructivity, largeness, usefulness, universe, and cryptographic assumption
are all written and proved.
