# V118 theorem ledger

## Definition 1 — exact MUX clone bank

Two outputs are exact clones when their complete signed MUX descriptions agree: selector, `data0`, `data1`, the three input polarity bits, and output flip. A clone bank is one exact-clone equivalence class contained in one non-common V113 dominator stage.

A stage has the **one-clone-bank DAG property** when it is already acyclic or deletion of one clone bank makes its gate-expanded variable graph acyclic.

## Lemma 1 — signed loop erasure

Let `B` be a clone bank and let one gate-simple route segment contain two gates `g,h in B` traversed with the same branch `b`, with neither shared boundary strictly between them. Exact cloning gives the same selector `s`, the same branch destination `d_b`, and the same source phase `alpha_b` for both traversals.

The route contains

`g(b) -> d_b -> P -> s -> h(b) -> d_b`.

Delete `P` together with `h(b)` and splice the suffix after `h` directly after `g(b)`. The route remains valid because both splice points are the same variable `d_b`. Only gates are deleted, so gate-simplicity and the no-extra-overlap condition are preserved. The first traversal after either adjacent shared boundary is unchanged; therefore the target requirement at the previous common gate or at the unique extra shared gate is unchanged.

Repeated application leaves at most one branch-0 clone and one branch-1 clone in the segment.

## Corollary 2 — constant clone interface

Cut each route at the possible unique non-common shared gate `q`. There are at most two route segments per route. By Lemma 1, each segment contains at most two clone gates. Hence a normalized certificate contains at most four clone gates per route, independent of the bank size.

After deleting the bank and `q`, all remaining stage gates form a DAG. The two normalized routes induce at most twelve jointly gate-disjoint DAG requests.

Only the first traversal after a previous common gate and after `q` can affect a shared gate's target bit. There are at most four such traversals. Enumerating their signed source phases and concrete first gates costs only a fixed polynomial factor.

## Theorem 3 — polynomial `Delta<=1` decision for one-clone-bank stages

For a fixed opposite-phase repeated-selector first pair, suppose every non-common V113 dominator stage has the one-clone-bank DAG property. Then target-compatible gate-simple return-pair existence with

`overlap <= minimum_overlap + 1`

is decidable in deterministic polynomial time.

### Proof

V113 gives the ordered chain `H` of common return-gate dominators, and V111 gives `minimum_overlap=|H|`. A certificate within budget can therefore share only `H` plus at most one additional gate `q`.

For each stage, recognize a suitable clone bank by grouping outputs by exact signed MUX signature and testing acyclicity after deleting each group. Enumerate the location and two branch choices of `q` if the extra-overlap budget is used. By Corollary 2, enumerate the constant set of normalized clone-branch patterns. Remove the whole bank and `q`; the residual instance is a DAG with at most twelve fixed terminal requests. Enumerate the at most four phase-sensitive first traversals and solve the residual request system by the fixed-dimensional product-state DAG linkage DP.

This yields local transitions indexed only by `(next-common branch pair, extra-used)`. The branch pair has four values and the budget bit two values. Compose the stages exactly as in the V113/V116 dominator DP. At the end reconstruct both returns and verify the induced target word.

All enumerations have constant dimension except the choice of `q` and concrete first gates, so the running time is polynomial in the circuit size. Soundness follows from direct reconstruction. Completeness follows by applying Lemma 1 independently in every segment of any valid budget-one witness.

## Proposition 4 — unbounded-feedback exact-stretch separation

For every `depth>=0` and `width>=2`, `strict_clone_bank_delta_one_family(depth,width)` has

`n = 7 + depth + 2*width`,
`m = n+1`,
`minimum_overlap = 1`,
`minimum_compatible_overlap = 2`,

and post-common-stage feedback-gate number exactly `width`.

### Proof

The first two returns must both pass the unique common gate `H`, so overlap is at least one. There is an overlap-one pair using opposite branches of `H`: the left return reaches `q`, while the right return takes its private exit. The first post-`H` source phases are respectively 0 and 1, so `H` requires conflicting target bits. Any overlap-one pair must use those opposite branches: taking the left branch twice also shares the unique `q`, and taking the right branch twice shares the unique right exit. Hence no overlap-one pair is target-compatible.

For a compatible overlap-two pair, both routes take the left branch of `H`, share `q`, then use two distinct forward clones (possible because `width>=2`) and distinct exits from the bank output. The first phases after `H` and after `q` agree on the two routes, so the shared-gate target requirements agree.

The cyclic bank contains `width` forward clones from `A` to `B` and `width` backward clones with a branch from `B` to `A`. Every surviving forward/backward pair gives a directed two-step cycle. Deleting fewer than `width` gates leaves at least one gate of each class and hence one cycle; deleting all forward clones makes the stage acyclic. Therefore the feedback-gate number is exactly `width`.

The explicit count gives `m=n+1`.

## Nonclaims

Theorem 3 does not cover two unrelated clone banks per stage, near-clones, arbitrary supplied feedback sets, or arbitrary feedback-gate number without the clone promise. It is not a P-versus-NP result and does not solve unrestricted `NC0_3-Avoid`.
