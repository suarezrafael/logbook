# Laboratory V69 — gate-order robustness

V69 replaces fixed-order `G_proj` by

```text
G*_proj = min over gate orders pi of G_proj(pi).
```

The laboratory proves an exact subset-lattice dynamic program for `G*_proj`, preserves deterministic natural-order adversarial witnesses, and shows that the largest exactly checked fixed-order records collapse under reordering.

## Reproduce

```bash
python3 v69_order_robustness.py
python3 verify.py
python3 verify_independent.py
```

## Main files

- `ORDER_ROBUSTNESS_THEOREM.md` — set-layer invariance and exact DP;
- `EXPERIMENT_REPORT.md` — fixed-order records and optimized values;
- `WITNESSES.json` — exact systems, orders, and search provenance;
- `RESULTS.json` — generated results;
- `V69_ORDER_ROBUSTNESS_THEOREM.tex` — standalone formal module;
- `V70_CORE_CONTEXT.md` — next constraints.

No polynomial ordering theorem, all-orders lower bound, standard proof-system simulation, unrestricted `NC0_3-Avoid`, circuit lower bound, novelty claim, or P-versus-NP consequence is asserted.
