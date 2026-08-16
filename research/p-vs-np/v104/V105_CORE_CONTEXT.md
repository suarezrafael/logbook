# V105 core context — signed-majority obstruction beyond canonical hybrid rank

## Starting point

V104 computes in polynomial time

```text
R = canonical affine-hull basis rank,
f = subsequent unprotected acyclic functional heads,
eta_AF = n-R-f,
```

and avoids the range in `O(2^eta_AF poly(N))`. Its strict mixed family has
`eta_AF=3` while V97/V101/V102/V103 parameters are linear.

However the next obstruction is already explicit: **pure signed majority**.
Every `0x17` target fiber is balanced non-affine and has full affine hull, while
V101 proved that `0x17` has no functional anchor. Consequently, on a circuit
containing only signed-majority gates,

```text
R=0,
f=0,
eta_AF=n
```

for every affine-first ordering and, in fact, for every hybrid certificate using
only the V101 functional-anchor and V103 affine-hull primitives. Reordering
cannot fix this blind spot.

## Explicit high-eta family

For `n>=4`, put one canonical majority gate on every cyclic triple

```text
(i,i+1,i+2) mod n
```

and duplicate one gate to obtain exact stretch `m=n+1`.

Then:

```text
V97:  lambda = n,
V100: zero peels,
V101: mu = n,
V103: nu = n,
V104: eta_AF = n.
```

For V102, every majority support requires at least two conditioned variables.
Equivalently the unconditioned set may contain at most one vertex in every
cyclic length-three window. Its maximum size is `floor(n/3)`, so the exact strong
affine-backdoor size is

```text
beta = n-floor(n/3) = ceil(2n/3).
```

Thus all currently constructive local-relaxation parameters remain linear on a
single connected exact-stretch majority family.

## Why naive branchwise V103 is not yet an algorithm

Fixing one input of a majority gate reduces it to a binary AND/OR-type gate, so
its *restricted canonical* fiber acquires a proper affine hull. This suggests a
smaller one-hit support set than the V102 two-hit backdoor.

But a missing word computed independently in each conditioned branch need not be
missing from the union of all branches. Likewise, the branch-dependent canonical
target bit of a restricted majority gate can change with the conditioned value.
Therefore it is invalid to claim a global avoider by simply running V103 in each
branch and combining the answers.

V105 must solve this composition problem explicitly rather than hiding it.

## Track A — branch-conditioned global invariant

Seek a target convention or relaxed relation that is simultaneously valid across
all assignments to a small conditioning set `B`. A positive theorem would need
to prove that one globally fixed output word is excluded from every branch while
using branchwise affine rank only as a computational aid.

Potential structures to test:

- paired target bits encoding the conditioned literal without changing the final
  output alphabet;
- a common affine separator obtained by intersecting or combining the branch
  hull systems;
- branchwise missing sets with a polynomially representable intersection;
- a symbolic prefix-count recurrence that sums branch contributions without
  solving arbitrary #2SAT.

## Track B — one-hit versus two-hit majority gap

For majority supports, a one-hit set makes every branch binary, while the V102
strong affine backdoor requires two hits per support. Determine whether the gap
can be exploited constructively for range avoidance or whether exact branch
composition is #P/PP-hard.

On the cyclic majority family the minimum one-hit support set is `ceil(n/3)`,
whereas

```text
beta = ceil(2n/3).
```

A rigorous algorithm with exponent near `n/3` would be a genuine new separation;
a hardness theorem for the needed branch-composition primitive would also be a
material barrier result.

## Track C — non-affine majority certificates

Since both functional graphs and affine hulls are blind to `0x17`, inspect
invariants native to majority:

- threshold/unate switching structure beyond the V99 loose-X certificate;
- implication systems after conditioning one literal;
- Fourier degree-two correlations from V85;
- combinatorial boundary certificates that remain globally target-consistent.

Any proposed certificate must construct a missing word, not merely prove that
one exists.

## External consequence discipline

A faster algorithm on the majority family is still a special-family result. It
must not be described as progress toward `P != NP` until it is connected to a
recognized range-avoidance/lower-bound transfer. Conversely, a hardness barrier
for the branch-composition primitive would guide the laboratory but would not by
itself resolve P versus NP.

## Required promotion criterion

V105 must provide at least one of:

1. a rigorous global composition theorem exploiting one-hit conditioning and
   branchwise rank;
2. a deterministic majority-specific constructor with a strict infinite-family
   asymptotic improvement over V102/V104;
3. a hardness/obstruction theorem showing that the branch-composition primitive
   is computationally intractable under a clearly stated reduction;
4. a new non-affine certificate that shrinks the cyclic-majority family.

Another ordering heuristic, truth-table census, or unsupported union-of-branches
argument is not sufficient.
