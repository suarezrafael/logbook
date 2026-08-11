# V98 core context — irreducible nonmonotone Turan certificates

## Starting point

V97 strictly improves the V96 positive-component enumerator.  After essential
support normalization and safe leaf/unary reductions, it solves every instance
in

```text
O(2^lambda poly(N)),
```

where `lambda<=rho`, and there are connected nonmonotone ternary families with
`rho=N` but `lambda=Theta(log N)`.

The residual hard regime is a positive-surplus peeling kernel with:

```text
lambda=omega(log N),
no unused or degree-one input,
no constant output,
no essential unary output.
```

Exact V92 child comparison remains forbidden as the main engine.

## Current literature opportunity

Kuntewar--Sarma (APPROX/RANDOM 2025) prove that every connected 3-uniform
linear hypergraph with more edges than vertices contains a polynomially findable
loose X-cycle.  Their labeled-hypergraph interface converts a subhypergraph with
an edge coloring not induced by any input coloring into an avoided output.  For
monotone `NC0_3`, they use this to obtain a deterministic polynomial-time
algorithm for every `m>n`.

V98 should test whether the **structural cycle certificate survives beyond
monotonicity** when the edge labels are arbitrary ternary truth tables.

## Track A — labeled loose-X classification

Restrict first to irreducible kernels whose essential supports form a connected,
3-uniform linear hypergraph with positive surplus.  Use the published loose-X
cycle theorem only as the structural source.

For a found loose X-cycle `H` with gate-label map `phi`, study the induced map

```text
{0,1}^{V(H)} -> {0,1}^{E(H)}.
```

First theorem target:

> Characterize a nontrivial class of ternary gate labels for which every labeled
> loose X-cycle has a polynomially constructible edge coloring outside the
> induced image.

The class must strictly contain a published easy class or contain a genuinely
nonmonotone gate family not already reduced to `NC0_2`.

## Track B — transfer-matrix certificate

A loose X-cycle has bounded local interaction even when its length grows.  Try
to represent realizable edge-color sequences by a constant-state transfer
system.  Promotion is allowed if this yields either:

1. a polynomial algorithm producing a nonrealizable edge coloring for a broad
   labeled cycle class; or
2. a symbolic obstruction theorem identifying exactly when the cycle map can
   be surjective.

Finite enumeration of a few cycle lengths is discovery evidence only.

## Track C — nonuniform label obstruction

If arbitrary ternary labels can make every loose-X coloring realizable, build an
explicit labeled family proving that the Kuntewar--Sarma structural theorem
alone cannot solve general `NC0_3-Avoid`.  The obstruction must scale with cycle
length and survive the V97 irreducibility rules.

## Mandatory prior-art separation

Do not claim the monotone result: Monotone-`NC0_3` with `m>n` is already in P by
Kuntewar--Sarma 2025.  Do not restate V84's small-Hall-witness enumeration or
V75/V77 bounded-width prefix counting.

## Runtime benchmark

The all-instance benchmark remains Huang--Li--Zhong

```text
O(N*2^(N/2))
```

for `k=3`.  A V98 positive result should report whether it is polynomial on the
entire stated support/label class, not merely an instancewise exponent.

## Stop rule

Do not promote a finite truth-table census.  Promotion requires a symbolic
label theorem, an end-to-end constructor on an irreducible large-kernel class,
or an asymptotic obstruction that closes the loose-X extension route for a
precisely specified label model.
