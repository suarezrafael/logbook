# P versus NP Laboratory V56

## Consistency-or-redundancy range avoidance for affine fibers

**Scientific status:** internally verified theorem package; not peer reviewed; novelty and priority are not established. This work does not solve general `NC0_3-Avoid`, prove an unrestricted circuit lower bound, or resolve P versus NP.

## Main result

Let

```text
C : {0,1}^n -> {0,1}^m,  m>n.
```

For every output coordinate `i`, choose an output value `alpha_i` whose preimage is describable by a polynomial-size affine system over `GF(2)`:

```text
A_i x = b_i.
```

The selected preimage may be empty; that is detected immediately.

V56 gives a deterministic polynomial-time range-avoidance algorithm by a dichotomy:

1. **Inconsistency.** If all chosen fibers cannot be active simultaneously, a minimal inconsistent subsystem yields an absent output and a separator of degree at most `n+1`.
2. **Redundancy.** If they are consistent, translate by a common solution. The affine systems become homogeneous subspaces `W_i <= GF(2)^n`. Because `m>n`, some complete block `W_i` lies in the span of the other blocks. Activating a spanning set of those gates forces gate `i` active, so requesting it inactive gives an absent output.

Therefore:

```text
Every mixture of efficiently represented affine output fibers
is avoidable in deterministic polynomial time for m>n.
```

## Ternary consequence

The 256 ternary truth tables form 14 NPN classes. Eight classes admit an affine output orientation. The four essential classes are:

```text
0x01  singleton fiber
0x06  distance-two affine pair
0x18  antipodal affine pair
0x69  ternary parity
```

V56 solves arbitrary mixtures of these classes at minimum positive stretch `m>n`.

This strengthens:

- V55's mixed-affine threshold from `m>n+1` to `m>n`;
- V55's `0x06` result from `m>n+1` to `m>n`;
- V54's arbitrary-polarity singleton threshold from `m>2n` to `m>n`.

## Remaining ternary frontier

The six essential NPN classes with no affine output fiber are:

```text
0x07  0x16  0x17  0x19  0x1b  0x1e
```

Each of their two fibers has minimum disjoint affine-partition number exactly two.

The classes `0x07`, `0x17`, and `0x1b` have bijunctive fibers on both sides and form the first V57 target. The remaining classes `0x16`, `0x19`, and `0x1e` require genuinely non-bijunctive state systems.

## Affine-extension barrier

A projection of an affine subspace is affine. Consequently, a non-affine fiber cannot be represented exactly as the existential projection of one affine system with hidden selector variables. Any extension of V56 to the six remaining classes must use a real disjunction, branching state, or a different certificate family.

## Reproduce

The full local package contains `verify.py` and `verify_independent.py`. The repository also contains `verify_index.py`, a compact standalone recomputation of the NPN/affine frontier and block lemma.

Expected full validation summary:

```text
14/14 ternary NPN classes classified
17,550 exhaustive 0x06 stretch-one multisets
3,876 exhaustive singleton stretch-one multisets
910 mixed/repeated-support circuit cases
720 abstract block-subspace checks
307 affine-projection checks
zero failures
```

A defensive audit additionally verifies that the representative solution stored in every consistent certificate satisfies every affine equation.
