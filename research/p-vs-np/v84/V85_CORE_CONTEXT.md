# V85 core context — the logarithmic Hall-expander branch

## Frozen input from V84

For an `NC0_3` support presentation with `m>n`, a deterministic `FP^NP`
procedure computes the exact girth, a deletion-canonical shortest circuit, and
its minimum Hall neighborhood using at most

```text
ceil(log2 m) + m
```

oracle queries. If the girth is at most `L`, local enumeration over `g-1`
variables constructs an avoided global output. Otherwise every output set of
size at most `L` is Hall-noncontracting.

With `L=c log(n+m)`, the unresolved branch is therefore the promise class of
logarithmic Hall expanders.

## Priority one: candidate lists on the hard branch

Determine whether the logarithmic Hall-expansion promise, together with
left degree three and target stretch `m=n+ceil(n^(2/3))`, yields a polynomial
candidate list of outputs containing a point outside the range.

The output must be one of:

1. a deterministic polynomial-size candidate-list theorem;
2. a reduction from the promised support family to a known certifiable remote
   point or CSP-refutation framework with all parameter losses explicit;
3. a counterfamily proving that Hall expansion alone is insufficient, thereby
   identifying the next necessary invariant.

Do not treat randomized sampling, an NP membership query over exponentially
many candidates, or the identity promise reduction as a completed solver.

## Priority two: align with the 2025 upper bound

Guruswami, Lyu, and Yuan give deterministic polynomial-time avoidance for

```text
m >= c_t n^((t-1)/2) log n.
```

For `t=3`, compare their refutation/certification mechanism with the V84 hard
branch. Isolate precisely which density or pseudorandomness property is
missing at `m=n+n^(2/3)` and whether support Hall expansion supplies any part
of it.

## Priority three: stronger expansion scales

Parameterize V84 by larger `L` even when `2^L` is no longer polynomial.
Combine V77 width decompositions, V80 branchwidth lower bounds, and V81
deficiency conservation to seek a structural win-win:

- low width exposes a quantitatively deficient cut;
- short girth gives a local avoided projection;
- large girth plus high width must either yield a certifiable pseudorandom
  structure or an explicit obstruction family.

## Lower-bound discipline

At `m=n+n^(2/3)`, a complete `FP^NP` solver would imply explicit matrix
rigidity and superlinear lower bounds for log-depth circuits. Polynomial
stretch `AC0-Avoid` already has consequences against `NC1`. These are
historical lower-bound targets, not a direct path to `P != NP`.

## Publication audit

Search for prior work on:

- oracle self-reduction for matroid girth and canonical circuits;
- local range avoidance from Hall-deficient support sets;
- promise reductions to small-set vertex expansion;
- certifiable remote points for sparse local maps.

Downgrade novelty immediately if an equivalent extraction theorem is found.
