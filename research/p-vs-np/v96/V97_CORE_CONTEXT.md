# V97 core context — uniform extraction inside a large surplus component

## Starting point

V96 separates list cardinality from uniform construction.

At exact stretch `M=N+1`:

- a support-conditioned universal list of size at most `8(N+1)+1` exists
  nonuniformly;
- an `N`-only universal list of size `O(N log N)` exists nonuniformly;
- every circuit-oblivious list needs `Omega(log N)` candidates in general;
- if a positive-surplus support-incidence component has `rho` inputs, an actual
  missing output can be found deterministically in `O(2^rho poly(N))` time.

Therefore all instances with `rho=O(log N)` are already comparison-free
polynomial controls.  The residual support regime has every positive-surplus
component of superlogarithmic size; the extremal case is one large connected
component carrying the whole stretch surplus.

## Mandatory separation

V97 must not spend a laboratory improving the nonuniform `O(N log N)` list
constant.  A promoted result must concern **uniform extraction** or a structural
obstruction to it.

Exact V92 child-count comparison is still forbidden as the main engine by the
V95 stop rule.

## Track A — surplus localization through separators

Let `K` be a large positive-surplus incidence component.  Search for a theorem
that converts a small input separator, articulation structure, tree/cactus
structure, or another explicit decomposition into a missing local/global word
without computing exact canonical child comparisons.

First target:

> Given a separator of size `s` in a positive-surplus component, characterize
> when enumerating its `2^s` assignments forces one residual piece or one
> polynomial candidate list to expose an absent output.

Promotion requires an end-to-end constructor with a proved runtime, not merely
a decomposition identity.

## Track B — uniform support-conditioned hitlist

Try to derandomize the V96 support-conditioned union bound on a nontrivial
support family.  Candidate families include incidence forests, bounded
feedback-vertex sets, bounded treewidth, laminar supports, or support systems
with an explicit Hall-type surplus witness.

The output must be an explicit candidate list, polynomial in `N` for the stated
family, and its universality must hold for **all truth tables** on those
supports.

## Track C — obstruction to local uniformizers

If uniformization fails even on simple connected patterns, formalize a model of
local/greedy candidate generators and construct a family on which every such
generator needs superpolynomially many candidates or must recover hard global
information.  A finite census alone is not promotion.

## Transfer discipline

A full `FP^NP` support-conditioned universal-list constructor for arbitrary
locality-three supports would put stretch-one `NC0_3-Avoid` in `FP^NP`.  By
truncation this reaches the larger-stretch regime used by the published
Gajulapalli--Golovnev--Nagargoje--Saraogi transfer.  Treat such a result as a
breakthrough-level bridge and recheck every uniformity and oracle detail before
claiming it.

## Runtime benchmark

The unrestricted comparison remains the Huang--Li--Zhong `k=3` bound

```text
O(N * 2^(N/2)).
```

For a structural algorithm, report both its parameterized runtime and the
largest support class on which the parameter is guaranteed small.  Instancewise
speedups are not worst-case speedups.

## Stop rule

If separator-based uniformization only reproduces exact prefix counting already
available from the V75/V77 width machinery, record that equivalence and switch
to a genuinely weaker certificate model.  Do not relabel an old bounded-width
algorithm as a new all-instance advance.
