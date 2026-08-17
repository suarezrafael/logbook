# V106 theorem ledger — adaptive signed-majority pair repair

## Definition — pair-repair distance

For every essential signed-majority output gate on support `(u,v,w)`, order the
three available pair clauses as `(u,v)`, `(u,w)`, `(v,w)`.  Choice zero is the
canonical V105 pair.  A **repair** changes a gate from choice zero to choice one
or two.

For a circuit `C`, let `sigma(C)` be the minimum number of repairs required so
that the selected signed pair graph contains a simple connected bicyclic
component whose 2-core is a barbell or figure-eight and whose two edge-disjoint
cycles both have transport parity one.  If no such selection exists, set
`sigma(C)=infinity`.

This parameter deliberately measures distance to the V105 implication class;
it is not claimed to characterize all target-compatible 2-SAT contradictions.

## Theorem 1 — FPT avoidance by pair repair

For an essential signed-majority `NC0_3` circuit `C:{0,1}^n->{0,1}^m`, `m>n`,
and integer `k`, there is a deterministic algorithm that either finds a V105
odd-handcuff missing output using at most `k` repaired gates or certifies that no
such selected-pair witness exists within that repair ball.  Its running time is

```text
sum_{j=0}^k binom(m,j) 2^j poly(N)
    = O((2m)^k poly(N)).
```

Consequently, the regime `sigma(C)=O(1)` is polynomial-time range avoidable.

### Proof

Enumerate the set of repaired output indices and, independently for each chosen
index, one of its two noncanonical pair choices.  All other gates keep the V105
canonical pair.  For every resulting selected signed graph run the deterministic
V105 simple-bicyclic detector.  If it finds a barbell or figure-eight with two
odd transport cycles, V105's implication-walk construction fixes a common output
target on the selected gates whose exact majority 2-CNF clauses contain a
variable and its negation in one implication SCC.  The full output word is
therefore outside the range.  The enumeration count is the displayed sum and
every detector/target-construction step is polynomial.

## Lemma 2 — every majority gate supplies an unbalanced transport triangle

Let the literal polarities of one signed-majority gate be `(p0,p1,p2)`.  Its
three pair transports are

```text
d01 = 1 XOR p0 XOR p1,
d02 = 1 XOR p0 XOR p2,
d12 = 1 XOR p1 XOR p2.
```

Then

```text
d01 XOR d02 XOR d12 = 1.
```

Hence the triangle formed by all three candidate pair edges is unbalanced.

## Lemma 3 — Hall/frame-rank identity for candidate-pair unions

For a nonempty subfamily `F` of essential signed-majority outputs, form the
signed multigraph `Sigma(F)` containing **all three** candidate pair edges from
every gate in `F`.  Every connected component of `Sigma(F)` contains an entire
gate triangle and is therefore unbalanced by Lemma 2.  For the signed-graphic
frame matroid,

```text
r_F(E(Sigma(F))) = |N(F)|,
```

where `N(F)` is the set of input variables touched by `F`.

Thus Rado's matroid-transversal criterion for selecting one candidate pair per
gate as a frame-independent transversal reduces exactly to the ordinary Hall
inequalities

```text
|N(J)| >= |J|    for every J subseteq F.
```

This is a bridge lemma, not an all-signed-majority avoidance theorem.  At
positive surplus, the full family is necessarily one step beyond the rank
budget; the unresolved issue is how to force the resulting colorful frame
dependence to be an odd handcuff rather than a balanced cycle.

## Theorem 4 — strict infinite one-repair family

For every integer `q>=0` there is a connected exact-stretch signed-majority
circuit `C_q` with

```text
n = 5 + 2q,
m = n + 1,
sigma(C_q) = 1.
```

Its canonical selected pair graph has a theta 2-core whose three cycle parities
are `(0,1,1)`, so V105's canonical barbell/figure-eight detector rejects it.
Changing exactly gate 4 from its canonical pair `(1,3)` to pair `(3,4)` produces
a figure-eight with two odd cycles.  No other one-gate repair works.

The resulting target is outside the original circuit range, not merely outside
a relaxation.

## Lemma 5 — exact V102 backdoor on the strict family

For `C_q`,

```text
beta(C_q) = q + 4 = (n+3)/2.
```

### Proof

A strong affine backdoor for signed majority must hit at least two variables of
every support.  Equivalently, its complement may contain at most one variable
from each support.  The five base variables induce a clique in the primal graph,
so the complement contains at most one base variable.  The `2q` subdivision
vertices lie on a path whose consecutive vertices co-occur with base variable
1, hence at most `q` of them can be selected in the complement.  Therefore the
complement has size at most `q+1`, giving `beta>=5+2q-(q+1)=q+4`.  Equality is
achieved by taking one base vertex away from the path together with every other
subdivision vertex.

## Separation from V101/V103/V104

All outputs of `C_q` are signed-majority.  The signed-majority orbit has no
functional anchor (V101) and its target fibers have full affine hull (V103).
Therefore on this family

```text
mu_V101 = n,
nu_V103 = n,
eta_AF_V104 = n,
```

while V106 has `sigma=1`.  The construction is also switching-unbalanced and
the full output set is the first positive-surplus set; finite and matching
checks are included in the primary verifier.

## Nonclaims

V106 does not prove that `sigma` is bounded on arbitrary signed-majority
circuits, does not give a polynomial algorithm for unrestricted signed-majority
`NC0_3-Avoid`, does not improve the unrestricted published worst-case range-
avoidance exponent, and does not prove a new circuit lower bound or resolve
P versus NP.
