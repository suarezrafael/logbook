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

The primary generator recomputes:

- the first-moment rainbow probability `3/8`;
- the exact identity `q(A)=1/8+4 sum A_ij^3`;
- the normalized Birkhoff second-moment exponent;
- the exact local coefficient `-8+(16/3)c`;
- every rational overlap matrix with common margins one through five;
- a deterministic diagonal/off-diagonal family scan.

Committed counts:

```text
2,314 exact direct-vs-cubic overlap identities,
52,637 rational Birkhoff-grid overlaps,
0 identity mismatches,
0 positive grid maxima at c=1.00,1.01,1.02,1.05.
```

The independent verifier reconstructs `306` exact identities and `12,461`
rational overlaps without importing the primary module. The continuous global
Birkhoff inequality remains unproved; the grids and scan are diagnostics only.

## Empty-core obstruction component

The exact obstruction packet verifies:

- the eight-vertex, ten-edge empty-3-core obstruction;
- zero satisfying assignments among `7^5=16,807` normalized colorings;
- colorability after deleting any one edge;
- the exact `212,625`-instance maximal seven-vertex census, with no obstruction;
- a separate 12-vertex, 14-edge linear empty-core obstruction;
- pair-codegree one and edge-minimal unsatisfiability of the linear example.

Thus neither empty 3-core nor empty 3-core plus linearity implies an
`F_2^3` basis coloring. These finite obstructions do not imply asymptotic
uncolorability of the random model.

## Seven-state overlap component

The full basis-CSP packet recomputes:

- the `168` ordered bases and single-edge probability `24/49`;
- the exact `7x7` overlap objective;
- a 36-dimensional tangent-space basis;
- all `1,296` rational Hessian bilinear identities;
- the Hessian identity `-I+(c/6)I`;
- local maximality of the uniform overlap for every density below `6`;
- all `5,040` permutation overlaps;
- the deterministic diagonal-family scan.

The global seven-state entropy-contraction inequality remains unproved. Local
stability and the one-dimensional scan are not global certificates.

## Integrated repository gates

The final draft quick gate for head `82989f2` completed successfully in GitHub
Actions run `30870527110`:

```text
38 focused checks executed,
46 documented skips,
0 failures,
V89 primary passed,
V89 independent passed,
0 verifier-generated mutations,
clean-tree assertion passed.
```

Before candidate merge, the pull request must be marked ready for review. The
ready-for-review event is required to execute historical compatibility, and the
runner-sensitive diff requires the cumulative full replay. Promotion to V89 is
a separate status-only change after the candidate merge and its successful
ready gates.

## Nonclaims

These audits do not prove either global overlap inequality, asymptotic basis
colorability, the nine-row constructor lower bound, unrestricted
`NC0_3-Avoid`, a new circuit lower bound, novelty, peer review, or `P != NP`.
