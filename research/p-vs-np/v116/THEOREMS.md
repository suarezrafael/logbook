# V116 theorem ledger — one-feedback-gate cyclic stages

## Definitions

Fix an opposite-phase signed-MUX first pair and its V113 common gate-dominator decomposition. Let `H=(h_1,...,h_d)` be the common return-gate dominators, so V113 gives

```text
minimum_overlap = d.
```

For a non-common dominator stage `S`, its **feedback-gate number** `tau_g(S)` is the minimum number of output gates whose deletion makes the directed stage branch graph acyclic.

V116 studies fixed pairs satisfying

```text
max_S tau_g(S) <= 1
```

and asks whether a target-compatible return pair exists with overlap at most `d+1`.

---

## Lemma V116.1 — unique non-common shared gate

Any return pair with overlap at most `d+1` shares at most one non-common output gate.

### Proof
Every return pair shares all `d` common gate dominators by V113. Only one unit of overlap remains. Every non-common gate belongs to exactly one dominator stage. ∎

---

## Lemma V116.2 — one-feedback stage decomposition

Let a stage have feedback-gate number at most one and choose a gate `f` whose deletion makes the stage acyclic (or `f=None` if the stage is already acyclic). Fix a candidate unique extra shared gate `q` and two gate-simple route segments through the stage.

After fixing which route uses `f`, the order of `f` and `q` on that route, and all branches at these special gates, deleting `f` and `q` decomposes the two route segments into at most five pairwise gate-disjoint requests in a DAG.

### Proof
A gate-simple route uses `f` and `q` at most once. If `q` is absent, at most one route may use `f` unless `f` itself is the unique shared gate. If `q=f`, each route is split into a prefix and suffix, giving at most four requests. If `q!=f`, both routes use `q`, while at most one route may also use `f`; the route using both special gates contributes at most three DAG pieces and the other contributes at most two, for at most five requests. Removing `f` makes the stage acyclic, and removing `q` cannot create a cycle. Every remaining piece lies in this residual DAG. Any gate shared by two pieces would be reused by one route or would be a second non-common shared gate, both forbidden. ∎

---

## Lemma V116.3 — fixed-request gate-disjoint linkage in a DAG

For every fixed constant `r`, `r` ordered source-target requests can be tested for pairwise output-gate-disjoint realization in a directed acyclic MUX branch graph in polynomial time. In V116, `r<=5`.

### Proof
Split every output gate into a capacity-one resource node between its selector variable and its two data destinations. Variable nodes retain unlimited sharing. The resulting graph is a DAG.

Use a product state containing the current node of each of the `r` requests. At each state, advance only a token whose current node has minimum topological rank among unfinished tokens. A token may not enter a gate-resource node currently occupied by another token.

No history set is required. When a token leaves a resource node `g`, every unfinished token is already at topological rank at least that of `g`. Any later traversal of `g` would require first occupying the selector predecessor of `g`, which has smaller rank, impossible in a DAG. Thus every accepted product walk uses each gate resource at most once globally.

Conversely, given pairwise gate-disjoint request paths, repeatedly advance an unfinished token of minimum current topological rank along its prescribed path. Because the prescribed paths are gate-disjoint, this serialization never encounters an occupied resource conflict and reaches the target product state. Hence the product DP is complete.

For fixed `r`, the product graph has polynomial size. With `r<=5`, V116 is polynomial. ∎

---

## Lemma V116.4 — local phase sufficiency

For a fixed special-gate plan in a stage, global target compatibility introduces cross-route constraints only at the preceding common gate and at the optional extra shared gate `q`.

### Proof
All residual stage gates are gate-disjoint between the two routes, so their target bits may be assigned independently. The feedback gate `f` is also private unless `f=q`. The preceding common gate is shared by construction, and `q`, when present, is the unique shared non-common gate. The target bit induced at either shared gate is determined by its chosen branch and the source phase of the next gate on that route, or by the next common-gate/closing phase when the local suffix is empty. Equality of the two induced bits is therefore necessary and sufficient locally. ∎

---

## Theorem V116.5 — budget one with one feedback gate per stage

For a fixed opposite-phase signed-MUX first pair whose every non-common V113 dominator stage has feedback-gate number at most one, the existence of a target-compatible return pair satisfying

```text
overlap <= minimum_overlap + 1
```

is decidable in polynomial time, and a witness can be constructed.

### Proof
Compute the V113 common-dominator chain and stages. For each stage, detect whether it is acyclic or find one output gate `f` whose deletion makes it acyclic; rejection of all such deletions proves the input is outside the V116 class.

Process stages in dominator order. The dynamic-programming state is the ordered branch pair at the current common gate together with one bit indicating whether the unique excess-overlap budget has already been used.

For each transition, enumerate `q=None` or a candidate stage gate `q`, the finitely many possibilities for route use/order of `f` and `q`, and their Boolean branches. By Lemma V116.2, the remaining problem has at most five gate-disjoint requests in a DAG; solve it by Lemma V116.3. Apply Lemma V116.4 to reject phase-incompatible transitions. The concrete `q` is witness metadata only and is not part of the future DP key.

Lemma V116.1 gives completeness: every feasible `d+1` witness has exactly this form in one stage (or uses no excess gate). Soundness follows from the gate-disjoint residual linkage, gate-simple special pattern, local phase checks, and the V113 dominator ordering. The number of stage/gate/branch scans and every fixed-five-token product DP are polynomial. ∎

---

## Theorem V116.6 — strict cyclic exact-stretch separation family

For every integer `t>=0`, `strict_tau_one_delta_one_family(t)` is an essential signed-MUX instance with

```text
n = 8+t,
m = 9+t = n+1,
minimum_overlap = 1,
minimum_target_compatible_overlap = 2,
Delta = 1.
```

Its final non-common dominator stage is cyclic and has feedback-gate number exactly one. Hence it lies outside the V115 all-DAG-stage class but inside V116.

### Proof
The construction is the V115 strict family with one formerly dead branch changed to `split -> left`, producing the directed cycle

```text
left -> split -> left.
```

Deleting the left-to-split repair gate (and also deleting the modified split gate) destroys that cycle, while the unmodified stage is cyclic, so its feedback-gate number is exactly one.

The new branch cannot occur in a gate-simple return to the root: reaching `split` through `left` already consumes the repair gate, and taking `split -> left` would require that same gate again to continue. Thus the set of gate-simple return routes relevant to the fixed pair is unchanged from the V115 strict family. V115's minimum-face incompatibility therefore persists: minimum overlap is one and every such pair conflicts on the common gate. The same `Delta=1` witness sharing the repair gate remains compatible and has overlap two. The branch mutation changes neither `n` nor `m`, so exact stretch `m=n+1` is preserved. ∎

---

## Parameterized observation — not promoted as an FPT theorem

The proof pattern extends naively to a supplied feedback-gate set of size `tau`: enumerate how the two gate-simple routes visit the feedback gates and the optional extra shared gate, then solve the residual DAG pieces by a product DP. This yields an XP-style `N^{O(tau)}` route, and therefore polynomial time for each fixed constant `tau`.

This is **not** an FPT result. The number of residual DAG requests grows with `tau`, and generic directed disjoint paths on DAGs is W[1]-hard when parameterized by the number of requests. V117 must either exploit the special two-route ordered-piece structure to beat this generic barrier or establish a matching hardness boundary.

---

## Nonclaims

V116 does not prove:

- FPT parameterization by arbitrary feedback-gate number;
- polynomial time for unrestricted cyclic stages or one arbitrary large SCC;
- `Delta<=1` polynomial time for all signed-MUX circuits;
- all MUX/bijunctive `0x1b` circuits are in P;
- unrestricted `NC0_3-Avoid` is in P;
- a general circuit lower bound;
- `P=NP` or `P!=NP`.

Novelty and peer review are not claimed.
