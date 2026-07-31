# V54 terminology and prior-art survey

## Established language

The laboratory's `sepdeg_F(S,y)` is the minimum degree of a polynomial separator of the point `y` from `S`. Equivalently, it is the first degree at which `y` leaves the finite degree Zariski closure of `S`. Hilbert-function and degree-closure language is established in the literature.

Relevant primary sources include Guardo–Van Tuyl on separators of points, Nie–Wang on finite-degree Zariski closure, and Golovnev–Guo–Hatami–Nagargoje–Yan on Hilbert functions and low-degree randomness extractors.

## Cover-free correction

The V53 girth argument missed nested collisions. The relevant combinatorial obstruction is cover-freeness: an edge must not be contained in the union of a bounded number of other edges. A positive-excess `k`-uniform hypergraph has a nonempty 2-core, so some edge is contained in the union of at most `k` others.

## Range Avoidance positioning

GGNS identify stretch-one `NC0_3-Avoid` as open and prove a rigidity consequence at stretch `n+n^(2/3)`. Kuntewar–Sarma solve monotone `NC0_3-Avoid` for every positive stretch via Turan-type bounds. V54's pure-AND certificate is a narrower algebraic reformulation and does not claim priority over that algorithm.

## Monomial maps

Hypergraph monomial maps and their kernels are studied through edge subrings and toric ideals. V54 works after Boolean multilinearization `X_v^2=X_v`, so equal unions, including nested cover collisions, govern the kernel rather than equality of exponent sums with multiplicity.

## Novelty status

The 2-core-to-separator observation may be folklore or subsumed by the monotone Range-Avoidance literature. It is published only as an internally verified reformulation pending specialist feedback.
