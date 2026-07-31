# Direct sums of affine-cell branching systems

## Setup

For an affine-cell branching system `A`, let:

- `c(A)` be the number of consistent complete cell-choice signatures;
- `L_aff(A)` be the minimum leaf count of an inconsistency-pruned adaptive tree under the V66 model.

Let `A \oplus B` denote the disjoint-variable direct sum: gates of `A` depend only on the first variable block and gates of `B` only on the second.

## Proposition

For disjoint systems,

```text
c(A \oplus B)=c(A)c(B).
```

Moreover,

```text
L_aff(A \oplus B)
  <= L_aff(A) + c(A)(L_aff(B)-1).
```

The asymmetric bound may also be applied in the opposite order.

## Proof

A complete branch of `A \oplus B` is consistent exactly when its restriction to `A` is consistent and its restriction to `B` is consistent. The input assignments factor over the two disjoint variable blocks, so consistent signatures are in bijection with pairs of consistent signatures. This proves multiplicativity.

Take an optimal tree for `A`. Every inconsistent leaf remains terminal. At each of its `c(A)` consistent leaves, graft a copy of an optimal tree for `B`. Replacing one leaf by a tree with `L_aff(B)` leaves adds `L_aff(B)-1` leaves. The displayed upper bound follows.

## Corollary for V57 direct sums

Every one of the 243 affine-cell partition systems of the V57 gadget has `c=1`. Therefore, for any direct sum of `k` such components,

```text
c=1
```

and iterating the grafting bound gives

```text
L_aff <= 1 + sum_i (L_aff(A_i)-1).
```

For identical components with leaf count `L`,

```text
L_aff <= 1 + k(L-1).
```

Thus the V57 direct-sum family cannot amplify the number of consistent branches and has a linear-in-components tree upper bound.

## Boundary

The corollary is specific to direct sums of components with `c=1`. Direct sums of components with `c>1` multiply `c` and may amplify growth. No general claim that all direct sums are easy is made.
