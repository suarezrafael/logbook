# V117 theorem ledger

## Definition — PARALLEL-TWO-CHAIN-GATE-LINKAGE-DAG

An instance contains an acyclic directed variable graph represented by capacity-one gate resources and two ordered chains of terminal requests. Variable vertices may be reused; no capacity-one gate resource may occur in two request paths. In the restricted `parallel` promise, all requests inside each chain have the same ordered terminal pair.

The parameter is the total number `k` of requests.

## Theorem 1 — parameter-preserving edge-to-gate transfer

`PARALLEL-TWO-CHAIN-GATE-LINKAGE-DAG` is W[1]-hard parameterized by `k`.

### Proof

Slivkins (2010) proves W[1]-hardness of Edge-Disjoint Paths on DAGs parameterized by the number of requests even when the demand graph is the union of two sets of parallel edges. We may assume both parallel classes are nonempty: if one class is empty, add two fresh vertices joined by one private source edge and add the forced request between them as the missing class. This preserves yes/no, preserves acyclicity and increases `k` by exactly one.

For every source DAG edge `e=(u,v)`, introduce a fresh capacity-one gate resource `g_e` and replace the edge by `u -> g_e -> v`. Keep the source terminals and place the two nonempty parallel demand classes into the two chains.

The transformed graph is acyclic: contracting every `g_e` recovers the source DAG, so a directed cycle after subdivision would contract to a directed cycle before subdivision.

A source path uses an edge `e` iff the transformed path uses `g_e`. Hence a family of source paths is edge-disjoint iff the corresponding transformed family is gate-resource-disjoint. The number of requests changes by at most the one-request padding above. This is an FPT parameter-preserving reduction.

## Definition — prescribed two-route feedback closure

Given the two request chains, reconnect the target of request `i` in a chain to the source of request `i+1` by a fresh private feedback gate. A solution is required to traverse the feedback gates of each chain in their prescribed order. Deleting all feedback gates leaves the gate-subdivided DAG.

## Theorem 2 — supplied-feedback barrier

For two nonempty chains with total `k` requests, the feedback closure uses

`tau=(|C0|-1)+(|C1|-1)=k-2`

feedback gates. Feasibility of the prescribed two-route feedback instance is equivalent to feasibility of the two-chain gate-linkage instance. Consequently this prescribed feedback-routing problem is W[1]-hard parameterized by the size `tau` of the supplied feedback interface.

### Proof

Concatenate the request paths of one chain with its private feedback gates. Gate-resource disjointness of the request paths makes the resulting walk gate-simple. Conversely split any accepting prescribed walk at the private feedback gates; the pieces solve the original request chain. Private feedback gates are distinct between chains and do not consume any base DAG resource. The parameter identity above is immediate. Combined with the optional one-request padding in Theorem 1, `tau` differs from the original hard parameter by only an additive constant.

## Corollary — generic XP-to-FPT compression is blocked

Unless FPT=W[1], the V116 `N^O(tau)` residual solver cannot be turned into `f(tau) poly(N)` using only the facts that the residual graph is a DAG and its requests form two prescribed chains.

## Nonclaims

V117 does not prove W[1]-hardness of signed-MUX `Delta<=1`, does not prove hardness parameterized by the *minimum* feedback-gate number of a MUX stage, does not prove all MUX/bijunctive circuits hard, and does not resolve unrestricted `NC0_3-Avoid` or P versus NP.
