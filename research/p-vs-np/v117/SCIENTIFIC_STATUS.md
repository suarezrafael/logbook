# V117 scientific status

**Classification:** barrier / frontier narrowing.

## Established internally

- parameter-preserving subdivision from DAG edge-disjoint routing to gate-resource routing;
- preservation of the two-parallel-demand-class promise as two request chains;
- exact equivalence of source edge-disjointness and transformed gate-resource disjointness;
- prescribed feedback closure of the two chains with `tau=k-2` when both chains are nonempty;
- exact equivalence between chain solutions and the two prescribed gate-simple feedback walks.

## Imported external theorem

Slivkins (2010) supplies the W[1]-hard source theorem for DAG Edge-Disjoint Paths and explicitly states that hardness remains when the demand graph consists of two sets of parallel edges.

The complexity hardness is therefore a transfer/corollary, not an independently reproved W[1]-hardness theorem.

## Verification

The primary verifier cross-checks 500 small promised DAG instances by exhaustive edge-path enumeration before and after the edge-to-gate transfer and audits `tau=k-2`.

The independent verifier reconstructs the mechanics without importing the V117 reducer and checks a fresh seeded population.

Finite verification tests the reduction mechanics only; it is not evidence for W[1]-hardness beyond the imported theorem.

## Boundary

The result closes the generic two-chain residual abstraction, not the signed-MUX problem itself. The missing bridge is whether the hard gate-routing instances can be embedded while preserving essential ternary MUX structure, V113 dominator-stage semantics, opposite phases, target compatibility, and positive stretch.
