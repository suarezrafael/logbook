# V89 literature and model-transfer boundary

## Orthogonal-array component

The finite construction is elementary and verified directly:

- the eight even-parity binary words of length four form a `[4,3,2]` code;
- projection onto any three coordinates is a bijection onto `{0,1}^3`;
- equivalently, the four coordinate rows form `OA(8,4,2,3)`.

The laboratory does not claim novelty for this classical coding-theory object.

## Random graph results do not directly apply

Achlioptas--Naor determine two possible chromatic values for the Erdős--Rényi
model `G(n,d/n)`. The primal graph of the V87 support model is not distributed
as `G(n,d/n)`: every selected support inserts a correlated triangle.

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

Balobanov--Shabanov analyze this model by the second-moment method and state an
explicit lower-density formula for sufficiently large numbers of colors. That
large-`r` formula is not automatically valid at `r=4`.

```text
A. E. Balobanov and D. A. Shabanov,
On the strong chromatic number of a random 3-uniform hypergraph,
Discrete Mathematics 344 (2021), 112231.
DOI 10.1016/j.disc.2020.112231.
```

Khuzieva--Matveeva--Shabanov subsequently study fixed `r>=k>=3` in the sparse
regime and report tight threshold bounds. The V89 packet does not cite that
abstract as an exact `k=3,r=4,c=1` theorem. Promotion of the nine-row lower bound
requires checking the paper's hypotheses and normalization line by line.

```text
A. Khuzieva, T. Matveeva and D. A. Shabanov,
Estimating the strong r-colorability threshold in random hypergraphs,
Moscow Journal of Combinatorics and Number Theory 12 (2023), 57–88.
DOI 10.2140/moscow.2023.12.57.
```

## Internal second-moment reduction

V89 independently derives the balanced four-color overlap objective. For a
`4x4` overlap matrix `A` with every margin `1/4`,

```text
q(A)=1/8+4 sum_ij A_ij^3.
```

After normalization `B=4A`, the remaining continuous problem is an
entropy/cubic inequality on the Birkhoff polytope. This reduction is internal;
it is not presented as a new threshold theorem.

The uniform overlap is locally stable for all densities below `3/2`. Finite
rational grids support global maximality near density one, but do not prove it.

## Random hypergraph cores

Skubch states the standard threshold for the `k`-core of the binomial random
`r`-uniform hypergraph `H_r(n,d/n^(r-1))`:

```text
d_r,k = inf_{lambda>0}
        lambda (r-1)! / Pr[Po(lambda)>=k-1]^(r-1).
```

For `r=k=3`, numerical minimization gives

```text
d_3,3 = 9.316979644...,
expected edge density d_3,3/6 = 1.552829940... .
```

Thus the V87 density `m/n -> 1` is below the 3-core threshold. This correctly
implies an empty 3-core with high probability, but it does not imply the
seven-state basis CSP is satisfiable.

The committed V89 continuation gives an exact eight-vertex empty-core
noncolorable support family and a separate linear empty-core obstruction. These
examples refute the proposed universal reverse-peeling extension theorem. They
do not refute a random-specific theorem, because each fixed dense obstruction
has vanishing occurrence probability in the sparse model.

Primary adjacent source:

```text
K. Skubch,
The core in random hypergraphs and local weak convergence,
Random Structures & Algorithms 51 (2017), 381–424.
```

## Novelty discipline

The affine basis construction, cubic overlap identity, finite audits, and exact
core-peeling obstructions are internal mathematical results. External novelty,
a sharp `r=4` random-model threshold, and peer review remain unconfirmed.
