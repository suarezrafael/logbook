# V87 core context — repeated-table Eval_H and the missing third obstruction

## Frozen output from V86

1. The three finite V80 controls contain `15`, `17`, and `18` C4 witnesses; none is C4-free.
2. C4 is necessary but not sufficient for nonlinear syndrome cancellation.
3. Every simple 3-uniform support family admits the uniform `NOR3` assignment with no nonzero constant syndrome, because every gate has a unique cubic ANF pivot.
4. For all sufficiently large `n`, a target-stretch family exists with no Hall-deficient set of size at most `n/(16e^2)` and no constant syndrome.
5. High support branchwidth is not proved for that same family.
6. The finite V80 controls remain solvable by both small-neighborhood Hall enumeration and bounded-width exact enumeration.
7. Input restrictions do not provide an avoidance pullback.
8. Polylogarithmic-width improvements remain asymptotically far from the V84 balanced-Hall branch of width `Omega(n^(2/3))`.

## Priority one — constructive Eval_H from repeated tables

Do not model `Eval_H` as an arbitrary locality-eleven circuit. Its `k` evaluation layers reuse the same truth-table bits. Exploit this repeated-factor structure.

Required probes:

- cyclic or transitive automorphisms acting on the witness layers;
- small-bias spaces generated over one shared table base;
- tensor, product-code, and diagonal-code constructions that preserve table reuse;
- deterministic candidate lists of size `O(n^(1/3))` or a rigorous obstruction to such a construction.

A negative theorem must specify the computational model of the list constructor. The V85 counting theorem already proves that an existential support-only list exists, so an unconditional nonexistence claim is forbidden.

## Priority two — complete the three-certificate intersection

Seek one support family satisfying simultaneously:

1. no Hall-deficient set below a linear threshold;
2. no constant syndrome under an explicit truth-table assignment;
3. support branchwidth `n^Omega(1)`, ideally `Omega(n^(2/3))`.

The V86 random simple-hypergraph model already supplies the first two properties. The missing task is a branchwidth lower bound for the same distribution or an explicit construction.

Possible measurements:

- cut connectivity profiles of random simple 3-uniform hypergraphs;
- expansion of the gate-intersection graph and its relation to support connectivity;
- rank or entropy lower bounds on `lambda_C(S)` across balanced cuts;
- exact small-instance census followed by a proof-oriented conjecture only after the data are stable.

## Priority three — calibrate remote point bridges

Prepare a parameter ledger for each external bridge before invoking it:

- ambient dimension;
- circuit or subspace dimension;
- guaranteed Hamming distance;
- field and encoding;
- uniformity and constructivity;
- required running time or oracle class.

Compare those requirements with the V85 guarantee `Omega((m-n)/log m)` in the `O(sqrt(log m))` support-branchwidth regime. Report multiplicative and exponent gaps, not qualitative proximity.

## Priority four — bounded arithmetic and dWPHP

Recover the deferred formalization front from V80. Determine which historical certificates can be proved in `PV`, `PV_1`, `APC^1`, or a theory with dual weak pigeonhole principles.

Start with the exact finite statements rather than the unrestricted target:

- V56 affine-certificate correctness;
- V75/V85 monotone-DAG pair-count conservation;
- the V86 simple-support `NOR3` syndrome theorem;
- the prefix pigeonhole step used for avoidance and remote points.

## Priority five — proof-complexity matching

A claimed inheritance must match all of:

```text
predicate, encoding, generator, field, proof system,
expansion notion, parameter scale, and target stretch.
```

Do not replace a missing match by analogy. Record every mismatch as a result and stop the branch when the required scale is impossible.

## Nonclaims

V87 does not begin with an active route to `P != NP`. The operative targets are constructive `Eval_H`, a genuine three-certificate obstruction family, and rigorous calibration of remote-point and proof-complexity bridges.
