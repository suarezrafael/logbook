# V104 literature boundary

## Relation to the laboratory

V104 combines two previously separate internal mechanisms:

- V101 total functional-graph relaxation with distinct heads and an acyclic
  dependency graph;
- V103 affine-hull rank compression, restricted in V104 to equations that live
  entirely on the remaining functional roots.

This restriction is essential. Substituting an arbitrary two-input functional
relation into a neighboring local gate can raise locality, which V100/V101
explicitly avoided. V104 instead keeps the functional DAG as a global evaluator
and applies linear algebra only to root variables.

V102 backdoors are not required by the theorem. They remain a possible future
method for discovering or simplifying hybrid certificates.

## External range-avoidance calibration

The targeted search checked primary range-avoidance literature including ECCC
TR22-102, TR23-021, TR25-034, and the revised TR25-049. Those works establish
important polynomial special cases, low-depth algorithms, Turan-type methods,
and general/local exponential algorithms and hardness connections.

No source found in that targeted search stated the V104 certificate template:
a safe distinct-head functional DAG followed by affine-hull equations supported
only on the DAG roots, with exponent `eta=n-f-R`. This is only a search result,
not evidence that the theorem is new.

## Adjacent paradigms

Functional dependencies, affine closure, Gaussian elimination, and tractability
backdoors are established ideas in database/CSP/SAT/algebraic settings. A prior-
art review should therefore search by mechanism rather than by the internal term
`hybrid root rank`.

The external review target is specifically whether an equivalent composition
lemma or parameter appears in algebraic CSP decomposition, functional-dependency
elimination, proof-complexity generators, or remote-point/range-avoidance work.

## Nonclaim

`novelty_confirmed=false` and `peer_reviewed=false` remain mandatory. The V104
branch is an experimental internal theorem package until its larger verifier
suite and repository governance gates are completed in version order.
