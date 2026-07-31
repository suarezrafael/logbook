# V56 validation record

## Primary verifier

```text
14/14 ternary NPN classes and affine covers classified
17,550 exhaustive 0x06 canonical stretch-one multisets
3,876 exhaustive singleton-fiber canonical stretch-one multisets
350 consistent mixed affine-fiber stretch-one circuits
350 unconditioned mixed affine-fiber stretch-one circuits
210 repeated-support circuits
307 affine-extension projection checks
720 abstract block-subspace checks
zero failures
```

Branch counts across the primary suite:

```text
CONSISTENT_REDUNDANT_BLOCK:       1,349
INCONSISTENT_ALL_ACTIVE_SUBSYSTEM: 20,987
```

## Independent verifier

```text
14 ternary NPN classes rebuilt independently
17,550 exhaustive 0x06 canonical multisets
20 serialized targets checked
240 fresh mixed/repeated-support circuits
zero failures
```

## Compact repository verifier

`verify_index.py` independently recomputes:

- all 14 NPN representatives;
- the eight affine-orientable classes;
- the four essential affine classes;
- the six-class non-affine frontier;
- the bijunctive subfrontier;
- 1,200 block-subspace tests;
- scientific-status safeguards in `RESULTS.json`.

## Defensive implementation correction

The final audit found that the representative solution stored in consistent certificates was initially reconstructed by reading pivot right-hand sides independently. Because echelon rows can contain lower pivots, this metadata could be wrong. The solver now performs substitution in pivot order and both construction and verification check the representative against every equation.

The target construction, block containment proof, and previously generated absent outputs did not depend on that stored representative.

## Full package

```text
p_vs_np_lab_v56.zip
SHA-256: afefe00dc7a08816d96007a87effb1365df187324223429a99ba8d7b79c6c9f3
```

The complete archive contains the primary implementation, independent verifier, serialized certificates, full classification JSON, manifest, hashes, research notes, and V57 context.
