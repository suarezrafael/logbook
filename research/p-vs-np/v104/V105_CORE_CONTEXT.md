# V105 core context — hybrid certificate detection

## Starting point

V104 gives a deterministic `O(2^eta poly(N))` avoider from a supplied,
polynomially checkable certificate combining:

- `f` distinct-head acyclic functional graph relaxations;
- rank `R` of additional affine-hull equations supported only on the remaining
  functional roots;
- `eta=n-f-R`.

An explicit connected exact-stretch family has `eta=3` while V97 `lambda`, V101
`mu`, V102 `beta`, and V103 `nu` are all linear.

The missing piece is **certificate discovery**. V104 must not be interpreted as
an FPT algorithm parameterized only by the optimum `eta` until such a detector
is proved.

## Track A — action-selection search tree

Each local output can contribute one of three actions:

```text
functional-head action,
affine-root-rank action,
leave residual.
```

Seek an FPT branching rule whose measure is the remaining hybrid dimension,
not the number of selected blocks. Any claimed branch must preserve distinct
heads, acyclicity, and root support of all affine equations.

A positive target is

```text
f(eta) poly(N)
```

certificate detection, which would convert V104 into a genuine FPT avoider.

## Track B — matroid/intersection formulation

The affine actions form a linear matroid on equation rows. Functional actions
consume distinct head variables and obey an acyclicity constraint. Investigate
whether the feasible union can be expressed as matroid intersection,
gammoid/branching structure, or a submodular rank maximization problem with an
exact or approximation guarantee.

The obstruction is that choosing functional heads changes the root set and can
invalidate affine actions whose equations touch newly consumed heads.

## Track C — hardness barrier

If exact certificate maximization is NP-hard or W[1]-hard even for a fixed small
ternary language, prove that barrier cleanly. A hardness result would redirect
the laboratory toward approximation, kernelization, or a different canonical
selection rule rather than silently assuming optimal certificates are easy.

## Required promotion criterion

V105 must provide one of:

1. an FPT/polytime detector with a proved guarantee tied to `eta`;
2. a polynomial approximation that still yields a new asymptotic avoidance
   regime on an infinite family;
3. a rigorous hardness/obstruction theorem for hybrid certificate discovery,
   together with a justified next route.

Another supplied-certificate theorem or truth-table census is not sufficient.
