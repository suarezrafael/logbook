# V105 core context — canonical hybrid worst case

## Starting point

V104 no longer requires a supplied hybrid certificate. Its deterministic
affine-first preprocessing computes:

```text
R = rank of a greedy canonical affine-hull block basis,
f = number of subsequent unprotected acyclic functional heads,
eta_AF = n-R-f.
```

It then constructs an avoided output in

```text
O(2^eta_AF poly(N)).
```

An explicit connected exact-stretch family has `eta_AF=3` while V97 `lambda`,
V101 `mu`, V102 `beta`, and V103 `nu` are all linear. The new open problem is
therefore not certificate discovery but the **worst-case behavior and ordering
quality of the computable canonical parameter**.

## Track A — high-eta_AF obstruction

Construct an explicit exact-stretch family for which the canonical affine-first
rule satisfies

```text
eta_AF = Theta(n).
```

Prefer balanced non-affine gates, because they contribute no direct canonical
affine rank. The family should also resist V97/V101/V102/V103 so that it exposes
a genuine residual obstruction rather than a weakness already solved by an
older parameter.

Once such a family exists, inspect exactly why the affine-first protection rule
loses functional heads or why the functional scan fails to reduce the remaining
root dimension.

## Track B — ordering/intersection improvement

The affine-first rule is intentionally conservative: every variable occurring
in the retained affine basis is protected. Explore whether a different
polynomially computable choice can improve `R+f` while keeping all retained
linear equations root-supported.

Candidate formulations include:

- choosing an equivalent sparse affine row basis before protecting variables;
- matroid/intersection formulations coupling affine block rank and distinct
  functional heads;
- submodular or exchange arguments proving that one canonical ordering gives a
  constant-factor approximation to the maximum safe compression;
- alternating affine and functional phases with a monotone invariant that never
  invalidates earlier equations.

A successful theorem must preserve polynomial-time discoverability.

## Track C — comparison with optimum hybrid compression

Define `eta_*` as the minimum residual dimension over all valid hybrid
functional/root-affine certificates. V104 computes one specific `eta_AF`.
Investigate either

```text
eta_AF <= g(eta_*)
```

for a useful function `g`, or prove a scalable separation showing that the
canonical rule can be far from optimum. Either outcome gives a principled V105
frontier.

## Track D — external consequence

Even a much smaller structural parameter matters for P versus NP only if it
connects to a recognized range-avoidance/circuit-lower-bound transfer. If V105
obtains a broad worst-case bound, immediately test whether it crosses the
parameters required by the calibrated Huang--Li--Zhong / Missing-String route;
do not infer a lower bound merely from a faster special-family algorithm.

## Required promotion criterion

V105 must provide at least one of:

1. a proved worst-case sublinear bound on `eta_AF` for a meaningful residual
   class;
2. a polynomially computable hybrid rule with a strict infinite-family
   separation from V104;
3. an approximation theorem relating `eta_AF` to optimal hybrid compression;
4. a rigorous high-`eta_AF` obstruction/hardness theorem that closes this
   canonical route and identifies the next invariant.

Another truth-table census or another supplied-certificate theorem is not
sufficient.
