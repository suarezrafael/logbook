# V89 validation record

## Addressing component

The candidate is generated with Python 3 using only the standard library. The
addressing generator recomputes:

- `OA(8,4,2,3)` injectivity;
- the exact uniform-code table for `j=3,...,10`;
- maximum primal cliques and exact primal chromatic numbers;
- deterministic `F_2^3` basis-coloring witnesses;
- eight-row address injectivity on all eleven controls.

Expected finite chromatic sequence:

```text
6, 5, 5, 5, 6, 5, 5, 5, 5, 5, 6
```

Every control has a verified basis coloring and an injective eight-row affine
address family.

## Strong-four overlap component

The primary generator additionally recomputes:

- the first-moment rainbow probability `3/8`;
- the exact identity `q(A)=1/8+4 sum A_ij^3`;
- the normalized Birkhoff second-moment exponent;
- the exact local coefficient `-8+(16/3)c`;
- all rational overlap matrices with common margins one through five;
- a deterministic diagonal/off-diagonal family scan.

Committed counts:

```text
2,314 exact direct-vs-cubic overlap identities,
52,637 rational Birkhoff-grid overlaps,
0 identity mismatches,
0 positive grid maxima at c=1.00,1.01,1.02,1.05.
```

The independent strong-four verifier reconstructs `306` exact identities and
`12,461` rational overlaps without importing the primary module.

The continuous Birkhoff inequality remains unproved. Finite grids and the
one-dimensional scan are explicitly diagnostic, not proof certificates.

## Repository gates

The earlier integrated draft quick gate passed `38` focused checks with zero
failures and a clean tree. The new overlap packet changes V89 mathematical
content and must pass a fresh integrated quick gate before the candidate can be
considered stable. Compatibility and any full replay required by runner changes
remain promotion prerequisites.

No promotion or nine-row constructor lower bound is implied by these audits.
