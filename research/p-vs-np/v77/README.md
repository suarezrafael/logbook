# Laboratory V77 — restricted topology-tree transfer

V77 strengthens the V76 supplied-decomposition transfer from width `4b` to
width `2b`.

The logarithmic-height hierarchy is prior art: Frederickson's restricted
multilevel partitions/topology trees, as related to top trees by Alstrup,
Holm, de Lichtenberg, and Thorup. The V77 contribution is the leaf-label
pruning lemma and the resulting support-boundary transfer.

Given a supplied width-`b` subcubic gate branch decomposition, V77 constructs a
rooted binary gate tree with

```text
width <= 2b,
height = O(log m),
external path length = O(m log m).
```

Rebuilding the V75 symbolic residual circuit gives

```text
O(m log m A(2b)^2 poly(n,m))
```

incremental prefix-avoidance time in the supplied-decomposition regime.

## Files

- `TOPOLOGY_TREE_TRANSFER.md` — theorem, proof, prior-art boundary, and scope;
- `V77_TOPOLOGY_TREE_TRANSFER_THEOREM.tex` — formal theorem module;
- `topology_tree_certificate.py` — static constructor, verifier, pruning, and transfer auditor;
- `v77_topology_tree_transfer.py` — deterministic finite generator;
- `STATIC_TOPOLOGY_CERTIFICATE.json` — independently checkable representative certificate;
- `RESULTS.json` and `EXHAUSTIVE_RESULTS.md` — deterministic validation ledger;
- `verify.py` and `verify_independent.py` — primary and independently written audits;
- `V78_CORE_CONTEXT.md` — frozen next target.

## Nonclaims

V77 does not prove that factor two is globally optimal, does not refute a
width-preserving logarithmic-height transfer, does not solve unrestricted
`NC0_3-Avoid`, and does not resolve P versus NP. Novelty and peer review are
not claimed.
