# Incremental bitset affine engine

`affine_bitset.py` represents each equation as one Python integer:

```text
coefficient bits | one RHS bit
```

## Operations

1. `insert_row` incrementally inserts a new equation into a canonical reduced basis.
2. `extend_basis` adds all equations of one affine cell without rebuilding the raw path system.
3. `project_basis` performs existential projection by giving eliminated variables pivot priority and retaining only constraints on active variables.
4. `build_projected_ordered_dag` hashes `(gate index, canonical projected basis)` states.

Python's native arbitrary-width integer XOR implements the bitset operations. The implementation is persistent rather than destructive, so recursive branches share immutable parent bases and require no unsafe rollback bookkeeping.

## Validation

The primary verifier checks the formula and bitset DAG for `k=1..64`. The independent verifier does not import this engine: it represents residual states as explicit projected relations and reconstructs the same `3k+4` state count for `k=1..5`.

## Scope

This is reusable infrastructure for future affine-cell DAG experiments. It is not yet a complete optimizer over gate order, tree decompositions, all six NPN classes, or mixed parity constructions.
