# V96 constructive control — surplus-component avoidance

## Support-incidence decomposition

Form the bipartite graph whose left vertices are the `N` circuit inputs and
whose right vertices are the `M=N+1` outputs; output `i` is adjacent precisely
to the input coordinates in its support.  For every connected component `K`
write

```text
n_K = number of input vertices in K,
m_K = number of output vertices in K.
```

Unused inputs appear as components with `m_K=0`.  Constant outputs may appear as
components with `n_K=0`.

Because components partition all input and output vertices,

```text
sum_K (m_K-n_K) = (N+1)-N = 1.
```

Therefore at least one component has positive surplus `m_K>n_K`.

Define

```text
rho(C) = min { n_K : m_K>n_K }.
```

## Theorem — comparison-free FPT avoider

Every explicit stretch-one local circuit has a deterministic avoided-output
algorithm with running time

```text
O(2^{rho(C)} * poly(N)).
```

In particular, the algorithm is polynomial whenever `rho(C)=O(log N)`.

### Proof

Choose a positive-surplus component `K` attaining `rho=rho(C)`.  All outputs of
`K` depend only on the `rho` inputs in `K`.  Enumerate all `2^rho` assignments
to those inputs and evaluate the `m_K` local outputs.  This constructs the exact
local range

```text
R_K subset {0,1}^{m_K}
```

with

```text
|R_K| <= 2^rho < 2^{m_K},
```

because `m_K>rho`.

No enumeration of the `2^{m_K}` output space is needed.  Consider only the
first `2^rho+1` lexicographic `m_K`-bit words.  Since the local range has at most
`2^rho` members, one of these candidates is absent.  Find it by membership in
the explicitly enumerated local range.

Place that absent local word on the output coordinates of `K` and fill every
other output coordinate arbitrarily, say with zero.  If a global input mapped
to this full word, its restriction to component `K` would realize the absent
local word, contradiction.

The enumeration and candidate lookup require `2^rho poly(N)` work. QED.

## Interpretation

This is a genuinely constructive comparison-free branch of V96.  It does not
compute or approximate V92 child counts and does not need an NP oracle.  It
isolates a residual hard support regime:

```text
all positive-surplus components have omega(log N) inputs.
```

At exact stretch one there is always at least one positive-surplus component;
the only way this theorem fails to give polynomial time is for every such
component to be large.

## Relation to the universal-list theorem

For the selected component, the proof itself constructs a local list of only
`2^rho+1` candidates and searches it explicitly.  Thus support decomposition
provides uniformization when a positive-surplus component is small.  The
nonuniform `O(N)` / `O(N log N)` universal lists become relevant only when the
surplus is trapped in large connected support components.

## Nonclaims

The parameter `rho(C)` can be linear in `N`, for example on connected support
instances.  Therefore this theorem is not an all-instance polynomial-time
algorithm and does not improve the worst-case Huang--Li--Zhong bound.  It is an
instance-parameterized constructive control and a precise handoff to the next
large-connected-component frontier.
