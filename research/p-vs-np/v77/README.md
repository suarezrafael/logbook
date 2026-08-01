# Laboratory V77 — topology-tree transfer and support-width FPT composition

V77 strengthens the V76 supplied-decomposition transfer from width `4b` to
width `2b`, then removes the supplied-decomposition hypothesis by composing
with the 2026 Korhonen--Oum FPT branchwidth theorem.

## Transfer result

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

incremental prefix-avoidance time.

## FPT composition

For the support connectivity function

```text
lambda_C(S)
  = |union_{i in S} supp(i) intersect union_{i notin S} supp(i)|,
```

V77 proves directly that `lambda_C` is normalized, symmetric, and submodular.
Thus it is a connectivity function. Korhonen and Oum's prior-art algorithm
finds a width-`k` branch decomposition from oracle access in

```text
2^{O(k^2)} gamma m^6 log m,
```

where `k=branchwidth(lambda_C)` and `gamma=O(m)` for explicit rank-three
supports. Composing decomposition discovery with V77, V75, and V74 gives

```text
2^{O(k^2)} gamma m^6 log m
  + O(m log m A(2k)^2 poly(n,m))
```

avoidance time for `m>n`. Therefore `NC0_3-Avoid` is FPT parameterized by
support connectivity branchwidth, without assuming a supplied decomposition.

## Files

- `TOPOLOGY_TREE_TRANSFER.md` — `2b` transfer proof, prior-art boundary, and scope;
- `FPT_SUPPORT_WIDTH_COMPOSITION.md` — Korhonen--Oum → V77 → V75 → V74 composition;
- `V77_TOPOLOGY_TREE_TRANSFER_THEOREM.tex` — formal transfer module;
- `V77_FPT_SUPPORT_WIDTH_THEOREM.tex` — formal FPT composition module;
- `topology_tree_certificate.py` — static constructor, verifier, pruning, and transfer auditor;
- `support_connectivity_oracle.py` — explicit oracle and exhaustive connectivity audit;
- `v77_topology_tree_transfer.py` — deterministic finite transfer generator;
- `STATIC_TOPOLOGY_CERTIFICATE.json` — independently checkable representative certificate;
- `RESULTS.json`, `COMPOSITION_RESULTS.json`, and `EXHAUSTIVE_RESULTS.md` — deterministic ledgers;
- `verify.py`, `verify_independent.py`, `verify_composition.py`, and
  `verify_composition_independent.py` — primary and independent audits;
- `V78_CORE_CONTEXT.md` — reproducibility firewall, explicit decomposition APIs, and next theorem target.

## Nonclaims

V77 does not implement the Korhonen--Oum algorithm, does not prove bounded
support branchwidth for unrestricted circuits, does not prove that factor two
is globally optimal, and does not refute a width-preserving logarithmic-height
transfer. It does not solve unrestricted `NC0_3-Avoid` and does not resolve P
versus NP. Novelty and peer review are not claimed.
