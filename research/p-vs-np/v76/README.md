# Laboratory V76 — top-tree width/depth transfer

V76 removes the arbitrary-depth obstruction left by V75 for a **supplied** gate
branch decomposition. The transfer combines standard labelled top trees with a
new support-boundary cover lemma:

```text
supplied width b
    -> rooted binary width at most 4b
    -> height O(log m)
    -> external path length O(m log m).
```

Rebuilding the V75 symbolic residual circuit on the transferred tree gives

```text
O(m log m A(4b)^2 poly(n,m))
```

incremental prefix-avoidance time.

The logarithmic-height top-tree construction is prior art. V76 contributes the
four-cut support-boundary transfer, a certificate auditor, and an exact
width/height/EPL finite classification. It does not solve unrestricted
`NC0_3-Avoid`, prove a standard-model lower bound, or resolve P versus NP.

## Main files

- `TOP_TREE_TRANSFER.md` — theorem, proof, prior-art boundary, and failed-route record;
- `decomposition_pareto.py` — exact width/height/EPL Pareto dynamic programs;
- `cluster_cut_cover.py` — labelled-cluster four-cut certificate auditor;
- `v76_top_tree_transfer.py` — deterministic result generator;
- `EXHAUSTIVE_RESULTS.md` — finite audit ledger;
- `V76_TOP_TREE_TRANSFER_THEOREM.tex` — formal theorem module;
- `verify.py` — primary deterministic verifier;
- `verify_independent.py` — raw-incidence and independently coded cluster audit;
- `RESULTS.json` — deterministic snapshot;
- `V77_CORE_CONTEXT.md` — frozen next-step constraints.

## Reproduce

```bash
python verify.py
python verify_independent.py
```
