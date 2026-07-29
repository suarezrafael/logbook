# Detailed proofs — V56

## 1. Minimal inconsistent systems have at most `n+1` equations

Represent an affine equation `a x=b` by the augmented vector `(a,b)` in `GF(2)^(n+1)`. An affine system is inconsistent exactly when `(0,1)` belongs to the span of its augmented equation vectors.

Let `E` be inclusion-minimal with this property. If its augmented vectors were linearly dependent, one vector could be removed without changing their span, contradicting minimality. Therefore they are independent and

```text
|E|<=n+1.
```

If `G` is the set of gates owning equations in `E`, no input can activate every gate in `G`. Hence `product_{i in G}Z_i` separates the constructed target and has degree at most `n+1`.

## 2. Block-subspace redundancy lemma

Let `W_1,...,W_m` be subspaces of a vector space `V` of dimension `r`.

**Lemma.** If `m>r`, then some block satisfies

```text
W_i <= sum_{j != i} W_j.
```

Otherwise choose `w_i in W_i` outside the sum of all other blocks. The vectors `w_1,...,w_m` are independent: any nontrivial relation would put one selected vector in the sum of the others. Thus `m<=r`, a contradiction.

Algorithmically, block `i` is redundant exactly when deleting it does not reduce the total row rank.

## 3. Consistency removes the affine constant coordinate

Suppose all selected fibers have a common solution `x*`. Substituting `x=z+x*` into `a x=b` gives `a z=0`, because `a x*=b`.

Thus all translated constraints live in `GF(2)^n`, rather than the augmented space `GF(2)^(n+1)`. This is the step that strengthens V55 from `m>n+1` to `m>n`.

## 4. Coefficient dependencies preserve right-hand sides

If a redundant row satisfies `a=a_1+...+a_t`, then evaluation at the common solution gives

```text
b=a x*=(a_1+...+a_t)x*=b_1+...+b_t.
```

Therefore the same linear combination reconstructs the full affine equation, not only its coefficient row.

## 5. Small source set and separator

Choose an independent coefficient basis from gates other than the redundant gate. It has at most `r<=n` rows. Let `J` be the distinct gates owning the basis rows used to reconstruct the redundant block. Then `|J|<=n`.

Activating every gate in `J` forces every equation of the redundant gate. Requesting that gate inactive produces

```text
(1-Z_i) product_{j in J}Z_j,
```

a separator of degree at most `n+1`.

## 6. Local affine fibers lift globally

A ternary support, including repeated variables, is a linear map `pi:GF(2)^n->GF(2)^3`. The preimage of an affine set under a linear map is affine or empty. An empty preimage produces an equation `0=1` and is handled immediately by the inconsistent branch.

## 7. Projection barrier

If `A=u+U` is affine and `P` is linear, then `P(A)=P(u)+P(U)` is affine. Existentially quantifying hidden variables from one affine system is a projection. Therefore hidden affine selector variables cannot encode a non-affine fiber exactly.

## 8. Complexity and implementation audit

For fixed fan-in, local affine recognition is constant-size work. The global steps are Gaussian elimination, rank tests, subsystem minimization, and row reconstruction, all polynomial in `n+m`.

During the final defensive audit, the stored representative solution was corrected to use substitution in pivot order rather than reading pivot right-hand sides independently. This metadata bug did not affect target construction; the primary verifier now checks the stored solution against every equation.
