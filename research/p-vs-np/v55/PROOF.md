# Detailed proofs — V55

## 1. Block-subspace lemma

Let `U` have dimension `D`. Suppose every `W_i` is not contained in the sum of the other blocks. Choose

```text
w_i in W_i \ sum_{j != i} W_j.
```

The vectors `w_1,...,w_m` are linearly independent: any nontrivial linear relation would express one selected `w_i` using vectors from the other blocks. Hence `m<=D`, contradicting `m>D`.

Algorithmically, `W_i` is contained in the sum of the other blocks exactly when deleting all rows of block `i` does not lower the total rank.

## 2. Affine fibers as equation blocks

Write the active fiber as `F_i=p_i+L_i`. If `q_1,...,q_r` is a basis of `L_i^perp`, then membership is characterized by

```text
q_s dot z = q_s dot p_i.
```

After substituting the three global input coordinates and adding a constant coordinate, these equations span `W_i subseteq GF(2)^(n+1)`. The normalized output `Z_i` equals one exactly when all equations in `W_i` vanish on `(x,1)`.

## 3. Missing-target construction

Assume `W_i` is contained in the sum of blocks indexed by `J`. If an input realized `Z_j=1` for every `j in J`, every lifted row from those blocks would vanish. Their span contains `W_i`, so all equations of the active fiber of gate `i` would vanish, forcing `Z_i=1`. Therefore the target with selected gates active and gate `i` inactive is absent.

A basis spanning `W_i` uses at most `D` rows and therefore at most `D` gate blocks. The product

```text
(1-Z_i) product_{j in J} Z_j
```

is a separator of degree at most `D+1`.

## 4. General affine threshold

All lifted rows have `n` input coefficients and one constant coefficient, so the ambient dimension is at most `n+1`. More than `n+1` gate blocks force a redundant block. The argument counts complete output gates as blocks, even when a gate contributes two or three independent equations.

## 5. Antipodal-pair invariant

Canonical mask `0x18` accepts `011` and `100`, whose difference is `111`. NPN input negations translate this pair, input permutations preserve direction `111`, and output complementation swaps which output value is active.

An equation coefficient `q` annihilates direction `111` exactly when `q` has even Hamming parity. After embedding into the global inputs, every coefficient vector remains even parity. Thus all augmented rows lie in an `n`-dimensional space: `(n-1)` dimensions for even-parity input coefficients and one for the constant coordinate.

With `m>n`, block redundancy applies and gives the stretch-one algorithm.

## 6. Exact ternary classification

The verifier applies all six input permutations, eight input-negation patterns, and output complementation to all 256 truth tables. It obtains canonical masks

```text
00, 01, 03, 06, 07, 0f, 16,
17, 18, 19, 1b, 1e, 3c, 69.
```

Testing each output fiber for closure after translation identifies affine-orientable classes

```text
00, 01, 03, 06, 0f, 18, 3c, 69.
```

The essential affine classes are `01`, `06`, `18`, and `69`. The six essential non-affine classes are `07`, `16`, `17`, `19`, `1b`, and `1e`.

## 7. Complexity and boundaries

All local descriptions have constant size. Gaussian elimination, block-deletion rank tests, and greedy sparsification run in polynomial time. Exhaustive enumeration is used only for finite verification.

The theorem does not handle gates from the six essential non-affine classes or arbitrary mixtures containing them. Equivalent formulations may be standard in affine CSP or matroid language; novelty is not claimed without specialist review.
