# Projected residual DAG model

## State definition

For a fixed gate order, a V68 state is

```text
(next gate index, canonical affine constraints on variables appearing in remaining gates).
```

After adding a cell's equations, the engine existentially projects every variable absent from all remaining supports. The resulting affine system is reduced to canonical RREF over `GF(2)` and hashed directly.

This quotient is denoted `G_proj`.

## Why projection matters

In the spine family, different completed motifs leave different equations on variables that will never be read again. Keeping those dead coordinates would prevent merging even though they cannot affect any future gate. Existential projection removes exactly that irrelevant history.

For each free motif, two branch paths merge after its second gate, giving three nonterminal states per motif and `G_proj=3k+4` overall.

## Distinction from earlier metrics

- `G_aff` in V66/V67 counted states reached by a selected tree policy while retaining the full feasible input set.
- `G_proj` quotients by existential projection onto future-active variables.
- neither quantity is asserted to equal a minimum DAG size;
- no standard variable-order, read-once, OBDD, FBDD, resolution, or proof-system semantics are imported automatically.

Any comparison with an established model requires an explicit simulation theorem preserving size and acceptance/refutation semantics.
