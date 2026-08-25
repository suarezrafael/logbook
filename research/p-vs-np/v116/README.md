# V116 — one-feedback-gate cyclic-stage budget-one theorem

V116 extends the V115 signed-MUX `Delta<=1` algorithm from acyclic non-common dominator stages to the first genuinely cyclic class.

For a fixed opposite-phase first pair, let the V113 common gate-dominator chain partition the return graph into non-common stages. Define the **feedback-gate number** of a stage as the minimum number of non-common output gates whose deletion makes that stage branch graph acyclic.

## Main result

If every non-common stage has feedback-gate number at most one, then target-compatible overlap

```text
overlap <= minimum_overlap + 1
```

is decidable in polynomial time.

The algorithm preserves V113's four phase states and one global budget-used bit. Inside one stage it chooses a feedback gate `f` (if needed), enumerates the unique possible extra shared gate `q`, route usage/order of `f` and `q`, and their branches. Deleting `f` and `q` leaves a DAG and splits the two routes into at most five gate-disjoint DAG requests.

Those requests are solved by a self-contained product-state token DP on a gate-split DAG. The number of requests is at most five, so the product graph is polynomial. Target compatibility is then checked only at the preceding common gate and at the optional shared gate `q`.

## Strict cyclic separation family

For every `t>=0`, V116 gives an essential signed-MUX instance with

```text
n = 8+t
m = 9+t = n+1
minimum_overlap = 1
minimum_target_compatible_overlap = 2
Delta = 1
```

whose final non-common stage contains the directed cycle

```text
left -> split -> left.
```

Removing the shared repair gate breaks the cycle, so the stage has feedback-gate number one. The new cyclic branch cannot complete a gate-simple return route without reusing the repair gate; therefore the V115 strict-family route census and `Delta=0` rejection remain unchanged. V115 itself is inapplicable because the stage is cyclic, while V116 accepts with one extra shared gate.

## Verification

- `verify.py` cross-checks 300 seeded `tau<=1` fixed-pair instances against direct gate-simple route enumeration, checks the strict family through depth 40, confirms V113 optimum-face rejection and V115 non-applicability, and validates one complete original range.
- `verify_independent.py` imports no V116 code. It reconstructs the strict family, audits the one-gate feedback cycle and exact overlap profile through depth 60, and performs an independent full-image target check.

## Boundary

This is a polynomial theorem for feedback-gate number at most one. It is **not** an FPT theorem for arbitrary feedback-gate number, does not settle the one-large-SCC case, does not prove all MUX/bijunctive `0x1b` circuits are in P, and does not resolve unrestricted `NC0_3-Avoid` or P versus NP.
