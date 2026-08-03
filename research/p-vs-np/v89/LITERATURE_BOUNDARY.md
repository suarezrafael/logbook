# V89 literature and model-transfer boundary

## Orthogonal-array component

The finite construction is elementary and verified directly:

- the eight even-parity binary words of length four form a `[4,3,2]` code;
- projection onto any three coordinates is a bijection onto `{0,1}^3`;
- equivalently, the four coordinate rows form `OA(8,4,2,3)`.

The laboratory does not claim novelty for this classical coding-theory object.

## Random graph results do not directly apply

Achlioptas--Naor determine two possible chromatic values for the
Erdős--Rényi model `G(n,d/n)`. The primal graph of the V87 support model is
not distributed as `G(n,d/n)`: every selected support inserts a correlated
triangle.

Therefore a threshold based only on matching average degree is not a valid
transfer theorem. Any asymptotic primal-colorability claim must be proved for
the random triangle/primal model itself or coupled by a rigorously justified
domination argument.

Primary source:

```text
D. Achlioptas and A. Naor,
The two possible values of the chromatic number of a random graph,
Annals of Mathematics 162 (2005), 1335–1351.
```

## Strong hypergraph coloring

Strong colorability of random 3-uniform hypergraphs is the directly adjacent
literature, because a strong four-coloring is exactly a proper four-coloring of
the primal graph.

The available asymptotic statements must be checked at the exact parameter
`r=4` and edge density `m/n -> 1`; large-`r` formulas are not automatically
valid at four colors.

Primary adjacent source:

```text
A. E. Balobanov and D. A. Shabanov,
On the strong chromatic number of a random 3-uniform hypergraph,
Discrete Mathematics 344 (2021), 112231.
```

## Random hypergraph cores

A possible alternative route is structural rather than chromatic: exploit the
low-density core decomposition of the V87 random hypergraph and prove that the
seven-state basis CSP extends through the resulting peeling order. No such
extension theorem is claimed in the current packet.

Primary adjacent source:

```text
K. Skubch,
The core in random hypergraphs and local weak convergence,
Random Structures & Algorithms 51 (2017), 381–424.
```

## Novelty discipline

The affine basis construction and the finite audits are internal mathematical
results. External novelty, a sharp random-model threshold, and peer review
remain unconfirmed.
