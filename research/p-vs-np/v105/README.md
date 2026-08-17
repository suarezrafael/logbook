# Laboratory V105 — signed-majority implication barbells

## Status

Experimental theorem package on an isolated branch while V104 proceeds through
repository promotion. V105 is not the official candidate. Novelty, priority,
and peer review are not established.

## 1. Majority targets expose exact 2-SAT clauses

Every signed ternary majority gate has the form

```text
g(x_u,x_v,x_w) = MAJ(x_u XOR p_u, x_v XOR p_v, x_w XOR p_w).
```

After fixing an output target `t`, the exact condition `g=t` is a 2-CNF
relation: each pair of local literals contributes a binary clause saying that
the two endpoint literals cannot both disagree with `t`.

For the canonical first-two-variable pair `(u,v)`, a chosen target can realize

```text
x_u=a -> x_v=a XOR delta_e,
delta_e = 1 XOR p_u XOR p_v,
```

for either source value `a`. The same clause supplies the reverse
contrapositive. Thus an output target acts as a selectable signed transport on
one pair edge.

## 2. Polynomial bicyclic barbell theorem

Build the **canonical pair graph** with one edge per signed-majority output and
label edge `e` by `delta_e`.

V105 now recognizes a broad exact-stretch regime, not only triangle dumbbells.
For any connected **simple bicyclic** canonical-pair component

```text
|E| = |V| + 1,
```

leaf pruning preserves cycle rank and its 2-core has one of the elementary
bicyclic forms:

- a figure-eight: two edge-disjoint cycles sharing one vertex;
- a barbell: two vertex-disjoint cycles joined by a path;
- a theta core: three internally disjoint paths between two branch vertices.

The implementation identifies this structure directly from degrees and path
tracing, without invoking a graph-minor algorithm.

If the figure-eight/barbell has **odd transport on both cycles**, choose targets
so that the first odd cycle transports `a -> not a`. In the barbell case,
transport `not a` along the connector to a value `b`; the path clauses also give
the reverse contraposition `not b -> a`. Target the second odd cycle as
`b -> not b`. The implication graph then contains one variable and its negation
in the same SCC, so the selected exact output constraints are inconsistent.

For a figure-eight the connecting path has length zero: target one odd cycle as
`a -> not a` and the other from the opposite polarity as `not a -> a`.

The whole detector and missing-output constructor are polynomial time.

The original `odd_triangle_dumbbell` implementation is retained as a smaller,
easier-to-audit special case and regression oracle.

## 3. Relation to known 2GraphSAT structure

Karve--Hirani's 2GraphSAT work already characterizes which **simple support
graphs can support some unsatisfiable 2-CNF**: exactly those containing one of
four fixed graphs as a topological minor:

```text
K4,
Butterfly,
Bowtie,
K_{1,1,3}.
```

Therefore the Bowtie/barbell support shape itself is not new. V105's narrower
question is different: each canonical majority pair edge is not allowed an
arbitrary 2-CNF clause; its literal signs fix an edge transport and the output
bit selects only one of two complementary clauses.

An independent exhaustive census over every edge-sign pattern and every target
choice on the four Karve--Hirani skeletons gives the exact compatibility rules:

```text
K4:        good iff all four triangles have odd transport       (8 signings),
Butterfly: good iff its two triangles have odd transport        (16 signings),
Bowtie:    good iff its two triangles have odd transport        (32 signings),
K1,1,3:    good iff exactly two of its three triangles are odd  (48 signings).
```

These finite skeleton counts are regression evidence; the barbell/figure-eight
transport proof is symbolic and works through arbitrarily long subdivisions.

A useful negative calibration also appears immediately: `K4` minus one edge has
five edges on four vertices but avoids all four 2GraphSAT obstructions, and the
canonical pair clause census finds no target choice that makes its pair formula
unsatisfiable. Hence `m>|V_pair|` alone cannot make the one-pair-clause route
universal.

## 4. Strict exact-stretch separation family

For every `r>=2`, let

```text
n = r+6,
m = n+1.
```

The canonical pair graph is a barbell consisting of a left triangle, a path with
`r` internal vertices, and a right triangle. Every pair edge has transport one,
so both cycles are odd.

Each graph edge becomes one signed-majority output gate. One left-triangle gate
negates only its third literal. This keeps the pair transport unchanged but
makes the full signed-majority incidence component switching-unbalanced.

The V105 constructor returns an impossible target; the triangle-specialized
constructor happens to return the alternating word `101010...` on this ordered
family.

The family is calibrated against the preceding routes:

```text
m = n+1 exactly;
no proper output subset has positive surplus;
V97 lambda = n;
V98 switching-balanced test fails;
V99 simple-X certificate is not directly applicable;
V100 literal-graph peels = 0;
V101 mu = n;
V102 beta = floor(2n/3) exactly;
V103 nu = n;
V104 eta_AF = n;
V105 signed barbell = polynomial time.
```

For V102, if `U` is the complement of a strong affine backdoor, each majority
support contains at most one vertex of `U`. The path supports force a
distance-three packing, while each end triangle contributes at most one free
vertex. Exactly `ceil(n/3)` vertices can remain unconditioned, giving

```text
beta = n-ceil(n/3) = floor(2n/3).
```

## 5. Verification state

Pre-registration and committed checks include:

- complete original-range checks on the strict family for `8<=n<=15`;
- 500 random signed-literal mutations preserving odd pair transport, checked
  against complete original ranges by the primary construction;
- an independent exact 2-SAT implication implementation with 240 more random
  complete-range cases and SCC checks through `n=106`;
- exact small-instance V102 backdoor values and proper-surplus checks;
- primary checks of arbitrary-length odd barbells (`3/5/7` cycles), figure-eight
  cores, and explicit theta rejection;
- independent exhaustive sign/target classification of all four known
  2GraphSAT obstruction skeletons.

Repository CI has not yet run V105 because V104 is still the official candidate.

## 6. Literature boundary

Kuntewar--Sarma give polynomial-time monotone `NC0_3-Avoid` at `m>n`, symmetric
`NC0_3` at larger linear stretch, and a majority special case at quadratic
stretch. V105's strict family is intentionally switching-unbalanced, so it is
not merely the monotone case under the V98 switching reduction.

Karve--Hirani already supply the forbidden-support theory for arbitrary 2-CNF
signings. V105 must therefore not claim the Bowtie/Butterfly support structures
as new. The laboratory-specific object is the **target-compatibility problem for
the restricted complementary pair clauses induced by signed-majority outputs**.

Targeted search has not established whether this compatibility specialization
or its range-avoidance use is known. Search absence is not evidence of novelty.

## Nonclaims

V105 does not solve all signed-majority `NC0_3-Avoid`, does not solve
unrestricted `NC0_3-Avoid`, does not improve the published unrestricted
worst-case exponent, does not establish a circuit lower bound, and does not
resolve P versus NP.
