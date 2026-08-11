# V97 literature boundary

## Kuntewar--Sarma, APPROX/RANDOM 2025

Neha Kuntewar and Jayalal Sarma, *Avoiding Range via Turan-Type Bounds*,
APPROX/RANDOM 2025, LIPIcs 353:62.

The paper formulates local-circuit range avoidance through labeled support
hypergraphs.  Its general interface says that a polynomially findable
subhypergraph carrying an edge coloring that no input coloring can induce gives
an avoided output.  For the monotone `NC0_3` class, the authors prove a new
Turan-type theorem: every connected 3-uniform linear hypergraph with more edges
than vertices contains a loose `X`-cycle of the needed form.  Combined with
additional reductions, this yields a deterministic polynomial-time algorithm
for Monotone-`NC0_3`-Avoid for every `m>n`.

V97 therefore makes no positive claim about the monotone class.  Its strict
separation family uses parity-of-three gates and lies outside both monotone
`NC0_3` and `NC0_2`.

The same paper is important for V98: after V97 peeling, the remaining
nonmonotone 3-local kernel may be attacked by keeping the hypergraph cycle
certificate while replacing the monotone/majority label argument with a
classification of general ternary gate labels.

## Huang--Li--Zhong, ITCS 2026

Shengtang Huang, Xin Li, and Yan Zhong, *Range Avoidance and Remote Point: New
Algorithms and Hardness*, ITCS 2026, LIPIcs 362:79.

For locality `k=3`, their all-instance local range-avoidance algorithm gives the
benchmark

```text
O(N*2^(N/2)).
```

V97 does not improve this worst-case runtime.  It gives an instance parameter
`lambda` with runtime `O(2^lambda poly(N))` and is therefore only an instancewise
speedup when the peeling kernel is sufficiently smaller than `N/2`.

## V84 internal boundary

Laboratory V84 already proved an `FP^NP` shortest-transversal-circuit / Hall
witness extraction theorem.  A Hall-deficient output set with logarithmic
neighborhood can then be solved by deterministic local range enumeration.

Accordingly, V97 does not count the observation "small deficient set implies a
small local range" as new progress.  The material step is the deterministic
reduction calculus that can *expose* a logarithmic residual kernel inside a
single component of linear input size, without an NP oracle.

## Novelty discipline

The safe leaf/unary reductions and the `lambda` parameter have not been checked
against the full prior-art corpus.  They are treated as internal research
results only.  No novelty or peer-review status is claimed.
