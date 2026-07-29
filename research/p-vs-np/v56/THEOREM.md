# V56 — Consistency-or-redundancy theorem for affine output fibers

## Definitions

Let `C=(C_1,...,C_m):{0,1}^n->{0,1}^m`. For each coordinate choose `alpha_i` and define

```text
F_i={x in GF(2)^n : C_i(x)=alpha_i}.
```

Assume a polynomial-time computable affine description `F_i={x:A_i x=b_i}`. Empty fibers are allowed and represented by an inconsistent system. Write `Z_i(y)=1` when output coordinate `i` equals `alpha_i`.

## Theorem 1 — minimum-stretch affine-fiber Avoid

If `m>n`, an output outside `Range(C)` can be constructed deterministically in polynomial time.

### Branch A — inconsistent active fibers

If all selected affine systems are jointly inconsistent, find an inclusion-minimal inconsistent equation subsystem `E` and let `G` be the gates represented in `E`.

The target that sets `Z_i=1` exactly for `i in G` is absent, and

```text
Q(Y)=product_{i in G} Z_i(Y)
```

vanishes on the range with degree at most `n+1`.

### Branch B — consistent active fibers

If all systems are consistent, choose a common solution `x*` and translate `z=x+x*`. Each gate becomes a homogeneous coefficient subspace

```text
W_i=rowspace(A_i)<=GF(2)^n.
```

Some index satisfies

```text
W_i <= sum_{j != i} W_j.
```

A set `J` of at most `n` other gates can be constructed whose active equations imply every equation of gate `i`. The target with `Z_j=1` for `j in J`, `Z_i=0`, and all other normalized coordinates zero is absent. The separator

```text
Q(Y)=(1-Z_i(Y)) product_{j in J} Z_j(Y)
```

has degree at most `n+1`.

## Theorem 2 — adaptive condition

The same algorithm succeeds without assuming `m>n` whenever the selected fibers are inconsistent or some complete coefficient block is contained in the sum of the remaining blocks. In particular, `m` greater than the total coefficient rank is sufficient.

## Corollary 3 — ternary affine-fiber classes

The preimage of an affine local fiber under a ternary support map is affine or empty, including repeated supports. Therefore arbitrary mixtures of the essential NPN classes

```text
0x01, 0x06, 0x18, 0x69
```

admit deterministic polynomial-time Range Avoidance for `m>n`.

## Corollary 4 — field-independent separator

The discovery algorithm uses `GF(2)` linear algebra, but the final product implication is a polynomial identity over every field. Every certificate uses at most `n+1` output coordinates.

## Theorem 5 — affine projection barrier

The image of an affine subspace under a linear projection is affine. Hence a non-affine Boolean fiber cannot be represented exactly as the existential projection of one affine system with hidden variables. Extending V56 to the remaining six classes requires genuine disjunction or a different state mechanism.

## Scientific boundary

The block lemma is elementary and may be standard in affine CSP, matroid, coding, or functional-dependency language. The exact Range-Avoidance formulation has not been externally reviewed, and novelty is not claimed.
