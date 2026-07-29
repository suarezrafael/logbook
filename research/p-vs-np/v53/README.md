# P versus NP Laboratory V53

## NC⁰₃ union-free syndrome barrier

**Scientific status:** internal theorem candidate with two independent finite verifiers and a primary-source literature audit. This package does **not** solve `NC⁰₃-Avoid`, prove a circuit lower bound, or resolve P versus NP.

V53 redirects the laboratory from `NC⁰₄` to the genuinely open stretch-one boundary `NC⁰₃-Avoid`. The main result is a transfer theorem from union-free 3-uniform hypergraphs to the minimum degree of a polynomial identity vanishing on the image of an `AND₃` circuit.

For a 3-uniform hypergraph `H=(V,E)`, define

```text
C_H(x)_e = product_{v in e} x_v.
```

If distinct edge subfamilies of size at most `t` have distinct vertex unions, then no nonzero output polynomial of degree at most `t` vanishes on `Range(C_H)`, over **any field**. High-girth incidence graphs produce stretch-one families with syndrome degree `Omega(log n)`.

This is a barrier to the constant-degree syndrome strategy. It is **not** evidence that monotone `NC⁰₃-Avoid` is hard: that monotone subclass already has a polynomial-time algorithm in the literature.

## Reproduce

```bash
python verify.py
python verify_independent.py
```

Expected result:

```text
V53 primary verification passed:
  2/2 NC0_3 stretch-one examples;
  743 distinct subset unions checked;
  6 full-rank Reed-Muller evaluations over GF(2), GF(3), GF(5);
  exact syndrome degrees 3 and 4; output-complement controls preserved degree.

V53 independent verification passed:
  2 examples rebuilt from JSON;
  743 union values independently checked;
  exact GF(2) syndrome degrees independently reconstructed.
```

## Files

- `THEOREM.md` — theorem statements and boundaries.
- `PROOF.md` — detailed proofs.
- `DIRECTION_CHANGE.md` — why the target moved from `NC⁰₄` to `NC⁰₃`.
- `FIELD_SURVEY.md` — primary-source literature audit.
- `LAY_SUMMARY.md` — explanation for non-specialists.
- `v53_core.py` — exact combinatorial and algebraic routines.
- `verify.py` — primary verifier.
- `verify_independent.py` — independent implementation.
- `FINITE_EXAMPLES.json` — two exact finite examples.
- `RESULTS.json` — machine-readable results.
- `V54_CORE_CONTEXT.md` — next research program.
