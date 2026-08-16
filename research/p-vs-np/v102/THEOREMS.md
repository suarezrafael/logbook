# V102 theorems

## Definition — strong affine backdoor

Let `C=(g_1,...,g_m)` be a Boolean circuit with input variables `x_1,...,x_n`. A set `B` of inputs is a strong affine backdoor if for every assignment `sigma in {0,1}^B` and every output `g_i`, the restricted Boolean function `g_i|sigma` is affine over `GF(2)` in the unassigned inputs.

Let `beta(C)` be the minimum cardinality of such a set.

## Theorem 1 — exact prefix counting from a supplied backdoor

Given `C`, a strong affine backdoor `B`, and an output prefix `p`, the preimage count

```text
M_C(p)=|{x in {0,1}^n : C(x) has prefix p}|
```

is computable in `O(2^|B| poly(N))` time.

### Proof

Partition all inputs by their restriction `sigma` to `B`. For fixed `sigma`, every restricted output gate is affine. Requiring the first `|p|` outputs to equal `p` is therefore a linear system over `GF(2)` in the `n-|B|` remaining variables. Gaussian elimination either finds inconsistency or computes its rank `r`, in which case the number of solutions is `2^(n-|B|-r)`. Sum this exact count over all `2^|B|` assignments `sigma`. The branches are disjoint because they fix different values of `B`. QED.

## Theorem 2 — constructive avoidance

If `m>n` and `B` is a strong affine backdoor, an output outside `Range(C)` can be constructed deterministically in `O(2^|B| poly(N))` time.

### Proof

Start with the empty prefix `p`. At each output position compute `M(p0)` and `M(p1)` using Theorem 1 and append a bit `b` minimizing the count. Because the two children partition the parent preimage,

```text
M(pb) <= M(p)/2.
```

Initially `M(empty)=2^n`. After all `m` output bits,

```text
M(y) <= 2^(n-m) < 1.
```

`M(y)` is a nonnegative integer, hence zero. Therefore no input maps to `y`. QED.

## Theorem 3 — FPT detection for output locality at most three

For a circuit whose output gates have arity at most three, deciding whether `beta(C)<=k` and producing such a backdoor when one exists can be done in `O(3^k poly(N))` time.

### Proof

Maintain a partial set `B`. If every gate is strongly affine under the local conditioned coordinates `B intersect supp(g)`, return `B`. Otherwise choose a violating gate `g` of arity at most three.

For this local truth table, enumerate the at most eight subsets of its support and retain the inclusion-minimal supersets of `B intersect supp(g)` that make every local restriction affine. Strong-affine goodness is upward closed under further conditioning. The inclusion-minimal good supersets therefore form an antichain in a three-element set, and by Sperner's theorem there are at most three.

Every global strong affine backdoor extending `B` must realize at least one of those local supersets. Branch on them. Since the chosen gate violates the current set, every branch adds at least one new variable. A depth-`k` tree with branching factor at most three has at most `3^k` nodes, and each node performs only constant-size local truth-table tests plus a scan of the circuit. QED.

## Corollary 4 — logarithmic backdoor regime

`beta(C)=O(log N)` implies deterministic polynomial-time range avoidance for locality-three circuits.

## Theorem 5 — exact `0x1b` local rule

For every mask in the ternary NPN orbit of `0x1b`, there is a unique selector coordinate `s` such that fixing `s` to either value leaves a unary literal on a different data coordinate. A local conditioned set `S` is a strong affine backdoor for the gate iff

```text
s in S
```

or both non-selector coordinates belong to `S`.

### Proof sketch

The canonical representative is a signed multiplexer

```text
g(s,a,b) = if s=0 then literal(a) else literal(b),
```

up to input permutations/negations and output negation. Fixing `s` leaves a unary literal. Fixing both data coordinates leaves a unary function of `s`. If `s` is free and at least one data coordinate is free, then after fixing any conditioned data coordinate the remaining two-variable restriction has a genuine product term `s * literal(data)` in its ANF for some branch assignment, so it is non-affine. NPN transformations preserve the statement. QED.

## Theorem 6 — exact signed-majority local rule

For every mask in the ternary signed-majority orbit `0x17`, a local conditioned set `S` is a strong affine backdoor iff `|S|>=2`.

### Proof sketch

After NPN normalization, the gate is majority on three signed literals. Fixing zero variables leaves an essential non-affine ternary function. Fixing exactly one input leaves, depending on its value, a signed AND or OR of the other two variables; both contain a degree-two ANF monomial. Fixing two variables leaves at most a unary Boolean function, which is affine. QED.

## Theorem 7 — strict V97/V100/V101 separation

For every `n>=5` there is an exact-stretch `m=n+1` pure-`0x1b` family satisfying

```text
beta=1,
lambda_V97=n,
V100 peels=0,
mu_V101=n.
```

### Construction and proof

Let `x0` be the selector in every gate. On the other `n-1` variables take a simple cycle and add two chords; this gives `n+1` distinct data edges. Put one canonical `0x1b` gate on each support `(x0,xa,xb)`.

Conditioning `x0` makes every output a literal, so `beta<=1`; the circuit is non-affine, so `beta=1`.

The support component is connected. Every data variable has cycle degree at least two, while `x0` occurs in all outputs. Hence V97 has no unused or leaf input, and all gates remain essential ternary, so its reducer leaves all `n` inputs. V100 classifies `0x1b` as residual hard, so no V100 literal-graph peel applies. V101 proves the entire `0x1b` orbit functional-anchor-free, so it selects no head and `mu=n`. QED.

## Nonclaims

These theorems do not imply a worst-case subexponential bound when `beta=Theta(n)`, do not put unrestricted `NC0_3-Avoid` in P, do not establish a circuit lower bound, and do not resolve P versus NP.
