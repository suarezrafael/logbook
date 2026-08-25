# V117 — two-chain feedback-linkage barrier

V117 asks whether the XP algorithm inherited from V116 can be compressed to FPT by exploiting that the residual DAG requests come from only two original gate-simple routes.

The answer is **no for the generic two-chain routing abstraction**.

## Barrier theorem

Slivkins (SIDMA 2010, DOI `10.1137/070697781`) proves that Edge-Disjoint Paths on DAGs is W[1]-hard parameterized by the number `k` of requests even when the demand graph is the union of two sets of parallel edges.

V117 transfers that result to the gate-resource model used by the MUX laboratory:

1. subdivide every DAG edge by a capacity-one gate resource;
2. put the two parallel demand classes into the two request chains;
3. optionally reconnect consecutive requests in each chain by private prescribed feedback gates.

Edge-disjoint source paths are equivalent to globally gate-disjoint residual paths after subdivision. If both demand classes are nonempty, reconnecting `k` requests needs exactly `tau=k-2` prescribed feedback gates. Deleting those feedback gates exposes the subdivided DAG again.

Therefore a generic `f(tau) poly(N)` solver for the prescribed two-chain residual subproblem would imply FPT=W[1].

## What this closes

The following properties are not enough by themselves to obtain FPT:

- requests lie in a DAG after deleting a supplied feedback set;
- requests are partitioned into two ordered chains;
- each chain comes from one original gate-simple walk cut at prescribed feedback gates;
- the number of chain breaks is `O(tau)`.

V117 therefore closes the generic Track-A compression route from V116.

## What remains open

The reduction is a graph-level gate-resource transfer. It does **not** prove W[1]-hardness for the full signed-MUX `Delta<=1` problem parameterized by minimum feedback-gate number. A signed-MUX stage has additional constraints: essential ternary MUX realizability, opposite first-pair phases, local target compatibility, the V113 dominator decomposition, and the global `m>n` range-avoidance setting.

V118 is frozen around that realizability gap: either lift the barrier through those signed-MUX constraints or prove that one of them blocks the reduction strongly enough to yield a new FPT invariant.
