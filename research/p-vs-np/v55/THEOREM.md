# V55 — Affine-fiber block redundancy for ternary Range Avoidance

> **Strengthened by V56.** Every theorem below remains valid, but V56 replaces the general threshold `m>n+1` by `m>n` for arbitrary mixtures of affine fibers. The improvement separates inconsistent selected fibers from the consistent case; in the latter, translation by a common solution removes the augmented constant coordinate.

## Definitions

Let `C=(f_1,...,f_m): {0,1}^n -> {0,1}^m` be a local Boolean circuit. For each output gate choose an active value `alpha_i` and let

```text
F_i={z in {0,1}^3 : f_i(z)=alpha_i}.
```

A gate is affine-fiber orientable when `F_i` is a nonempty affine subspace of `GF(2)^3`. Lift a full-rank affine equation system for `F_i` to the `n` global variables plus one constant coordinate, and let `W_i` be its row space. Normalize `Z_i=1` iff the gate output equals `alpha_i`.

## Theorem 1 — block-subspace redundancy

Let `W_1,...,W_m` be subspaces of a vector space of dimension `D`. If `m>D`, then some block satisfies

```text
W_i subseteq sum_{j != i} W_j.
```

The index is found by comparing the total row rank with the rank after deleting each gate block.

## Theorem 2 — V55 augmented-space affine-fiber Avoid

If every output gate has an affine active fiber and `m>n+1`, a missing output can be constructed deterministically in polynomial time.

Choose a redundant block `W_i` and a set `J` of other blocks spanning it. Request

```text
Z_j=1 for j in J,
Z_i=0,
Z_k=0 otherwise.
```

Any input satisfying the selected fibers would satisfy every equation of `W_i`, forcing `Z_i=1`, a contradiction.

A set `J` of size at most `n+1` exists. Hence the constructed target has a separator `(1-Z_i) product_{j in J} Z_j` of degree at most `n+2`, valid over every field.

**Current strongest version:** V56 proves the same mixed-class conclusion for `m>n` and improves the separator bound to `n+1`.

## Theorem 3 — stretch-one antipodal-pair class

For the ternary NPN class with canonical mask `0x18`, an oriented active fiber is always an antipodal pair `{p,p xor 111}`. Its defining equation coefficients have even parity. All lifted augmented rows therefore lie in

```text
U_even={(a,c): sum a_i=0},
```

which has dimension `n`.

Therefore `m>n` already forces one complete gate block to be implied by the others. Homogeneous circuits whose gates belong to the full NPN orbit of `0x18` admit deterministic polynomial-time Range Avoidance at minimum positive stretch.

This class is genuinely ternary and nonmonotone.

## Corollaries and later strengthening

- V55 solved canonical `0x06` for `m>n+1`; V56 improves it to `m>n`.
- Canonical `0x69`, ternary parity and its complement, is solved for `m>n` by ordinary affine output rank.
- V56 also improves arbitrary singleton-fiber mixtures to `m>n`.

## Classification consequence

The 256 ternary functions form 14 NPN classes. Essential affine classes:

```text
0x01, 0x06, 0x18, 0x69.
```

Essential non-affine classes remaining:

```text
0x07, 0x16, 0x17, 0x19, 0x1b, 0x1e.
```

The V55 implementation assumes three distinct input positions for essential ternary gates. V56 removes that implementation restriction and validates repeated supports. Results are internal and independently verified, but not peer reviewed; priority is not established. General stretch-one `NC0_3-Avoid` remains open.
