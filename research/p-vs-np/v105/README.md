# Laboratory V105 — signed-majority implication dumbbells

## Status

Experimental theorem package on an isolated branch while V104 proceeds through
repository promotion. V105 is not the official candidate. Novelty, priority,
and peer review are not established.

## Main result

Every signed ternary majority gate has the form

```text
g(x_u,x_v,x_w) = MAJ(x_u XOR p_u, x_v XOR p_v, x_w XOR p_w).
```

After fixing an output target `t`, the condition `g=t` is a 2-CNF relation: for
each pair of inputs, the two corresponding bad endpoint values cannot occur
together. In particular, for the canonical first-two-variable pair `(u,v)`, a
chosen target can realize an implication

```text
x_u=a  ->  x_v=a XOR delta_e,
delta_e = 1 XOR p_u XOR p_v,
```

and the opposite implication supplied by the same binary clause is its
contrapositive.

V105 builds the **canonical pair graph** with one edge per output gate. It then
searches for two vertex-disjoint triangles whose edge-transport XOR is one,
connected by a path disjoint from the triangle edges and internally disjoint
from both triangles. Call this an **odd-triangle dumbbell**.

If such a dumbbell exists, choose targets so that

```text
left odd triangle:  a -> not a,
connecting path:    not a -> b,
right odd triangle: b -> not b.
```

The path clause simultaneously gives the contraposition `not b -> a`. Hence the
implication graph contains

```text
a -> not a -> b -> not b -> a,
```

so one variable and its negation lie in the same strongly connected component.
The selected target pattern is therefore impossible. All other output bits may
be completed arbitrarily.

The detector and constructor are polynomial time. The current implementation
enumerates odd canonical-pair triangles and uses BFS to connect disjoint pairs.

## Strict exact-stretch family

For every `r>=2`, let

```text
n = r+6,
m = n+1.
```

The canonical pair graph is a dumbbell consisting of:

- a left triangle;
- a path with `r` internal vertices;
- a right triangle.

Each graph edge becomes one signed-majority output gate. The gate support is the
pair edge plus a nearby third variable, so all gates remain essential ternary.
One left-triangle gate negates only its third literal. This leaves every
canonical pair transport equal to one, but makes the full signed-majority
incidence component switching-unbalanced.

Both triangles therefore have odd transport. The V105 constructor returns the
alternating target word

```text
101010...
```

and the implication proof certifies that it is absent.

The family is deliberately calibrated against the preceding laboratory routes:

```text
m = n+1 exactly;
no proper output subset has positive surplus;
V97 lambda = n;
V98 switching-balanced test fails;
V101 mu = n;
V102 beta = Theta(n) (finite exact checks match floor(2n/3));
V103 nu = n;
V104 eta_AF = n;
V105 odd-triangle dumbbell = polynomial time.
```

The no-proper-surplus claim follows already from the pair graph: every proper
edge subset of a dumbbell has at most as many edges as pair vertices, while the
full dumbbell has exactly one unit of surplus. A circuit support contains every
pair endpoint, so support surplus cannot appear earlier.

## Verification state

Before registration, the explicit family was checked against complete original
ranges for `8<=n<=15`, with zero failures.

The committed primary verifier additionally checks:

- all eight signed-majority masks;
- complete-range avoidance on the strict family;
- switching imbalance;
- minimum support degree and connectivity;
- exact small-instance V102 backdoor values;
- absence of proper positive-surplus subsets on small instances;
- 500 complete-range tests after random signed-literal mutations that preserve
  odd canonical-pair transport.

The independent verifier does not call the V105 detector. It constructs the
2-SAT implication graph directly, checks the contradictory SCC through
`n=106`, repeats complete-range checks on small instances, and performs 240
additional random-polarity complete-range audits.

Repository CI has not yet run V105 because V104 is still the official candidate.

## Literature boundary

Kuntewar--Sarma (2025) give polynomial algorithms for monotone `NC0_3-Avoid`
when `m>n`, for symmetric `NC0_3-Avoid` at larger stretch, and for majority
outputs at quadratic stretch. The laboratory's targeted primary-source search
did not locate this exact signed-majority 2-SAT dumbbell construction at exact
stretch. That absence is not evidence of novelty, and no novelty claim is made.

## Nonclaims

V105 does not solve all signed-majority `NC0_3-Avoid`, does not solve
unrestricted `NC0_3-Avoid`, does not improve the published unrestricted
worst-case exponent, does not establish a circuit lower bound, and does not
resolve P versus NP.
