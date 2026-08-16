# V104 core context — high-nu balanced-nonaffine frontier

## Starting point

V103 safely relaxes one canonical target fiber per output to its affine hull. If
the combined system has rank `R`, then `nu=n-R` gives a deterministic
`O(2^nu poly(N))` avoider. It strictly separates from V97/V101/V102 on an
infinite exact-stretch family.

The exact local blind spot is now the **56 balanced non-affine essential ternary
truth tables**. Both fibers of every such predicate have full affine hull, so
V103 obtains no rank equation directly from them.

## Track A — hybrid functional + affine rank

V101 can still use functional graph relaxations on part of this class (notably
the `0x1e` orbit), while V103 can solve affine cycles globally. Seek a hybrid
constraint system in which functional equations are partially linearized or
eliminated and the residual affine rank is measured after substitution without
raising locality in neighboring gates.

Promotion requires a symbolic theorem, not a finite mask census.

## Track B — backdoor then hull rank

Condition a small set `B` as in V102, but do not require every restricted gate to
be affine. Instead require that in every branch the canonical affine-hull rank
leaves small residual dimension. Candidate parameter:

```text
tau(C) = min_B ( |B| + max_sigma nu(C|sigma) ).
```

A supplied `B` would suggest an `O(2^tau poly(N))` avoider by branchwise hull
compression. The critical tasks are to prove the lifting carefully, find `B`
constructively, and exhibit an infinite family with `tau=o(min{beta,nu})`.

## Track C — high-nu obstruction family

Construct an explicit exact-stretch residual family satisfying simultaneously

```text
lambda = Theta(n),
mu     = Theta(n),
beta   = Theta(n),
nu     = Theta(n).
```

Then search for a new invariant on that single family. Prefer signed-majority
`0x17`, mux `0x1b`, and balanced graph-of-AND `0x1e` mixtures, because they are
representative full-hull/nonlinear survivors of different earlier methods.

## Stop rule

Do not promote V104 for:

- another truth-table count;
- a finite improvement with no asymptotic family;
- a restatement of V102 backdoors or V103 rank;
- an argument that silently composes a two-input relation into a neighboring
  gate and raises locality.

Promotion requires either a rigorously constructive `tau`-type theorem with a
strict infinite-family separation, or a scalable obstruction theorem that
closes this hybrid route and redirects the laboratory.
