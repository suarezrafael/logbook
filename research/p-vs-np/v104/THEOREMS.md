# V104 theorem ledger — functional DAG plus affine root rank

## Definition — hybrid certificate

For `C:{0,1}^n->{0,1}^m`, `m>n`, a hybrid certificate consists of two disjoint
sets of output coordinates.

The functional set `F` carries V101-style target/head certificates. Heads are
distinct and the tail-to-head dependency graph is acyclic. Let `f=|F|` and let
`Q` be the non-head variables, so `|Q|=n-f`. Each assignment to `Q` extends
uniquely through the total functional graph relaxations.

The affine set `A` carries canonical target fibers whose affine-hull equations
are supported entirely on the root variables `Q`. Greedily retain an affine
output block only when its root equations increase rank. Let the resulting root
rank be `R` and the number of retained affine blocks be `s_A`.

Define

```text
eta = |Q| - R = n - f - R.
```

The certificate is polynomially checkable: functionality, distinct heads,
acyclicity, local affine hulls, root support, consistency, and GF(2) rank are all
polynomial-time tests.

## Theorem 1 — safe hybrid relaxation

Every exact selected functional fiber is contained in its total functional graph
relaxation, and every exact selected affine fiber is contained in its affine
hull. Therefore imposing all selected relaxed relations only enlarges the set of
inputs that could realize the selected target bits. A word missing from the
relaxed image lifts to a word missing from the original image.

## Theorem 2 — root-rank avoider

Given a valid hybrid certificate, a missing output can be constructed
deterministically in

```text
O(2^eta poly(N)).
```

### Proof

The functional DAG leaves exactly `|Q|=n-f` roots. The consistent rank-`R`
affine system on those roots has exactly `2^(|Q|-R)=2^eta` solutions. Every root
solution extends uniquely through the functional DAG, so the entire hybrid
relaxed domain also has exactly `2^eta` assignments.

Every retained affine output block increases rank, hence `s_A<=R`. After
deleting the selected functional and affine output coordinates, the number of
remaining outputs is

```text
m - f - s_A >= m - f - R > n - f - R = eta.
```

Evaluate the original remaining output gates on all `2^eta` relaxed assignments.
At most `2^eta` residual words occur, while the residual output cube contains
strictly more. Hash the observed residual words, choose one not observed, and
reinsert all selected target bits. Any original input producing this full word
would satisfy all selected exact fibers and therefore all relaxed constraints,
contradicting the missing residual word.

If a selected affine target fiber is empty, or the selected root affine hulls
are inconsistent, the corresponding selected target pattern already certifies
an absent full output after arbitrary completion of the remaining coordinates.

## Theorem 3 — strict infinite-family separation

For every `k>=1`, construct two blocks, each on `4k` variables.

### Functional block A

On variables `A_0,...,A_(4k-1)`, put canonical `0x1e` gates on every cyclic
triple

```text
(A_i,A_(i+1),A_(i+2)) mod 4k.
```

There are `4k` outputs. Select the first `4k-2` with target zero. Canonical
`0x1e` target zero is the graph

```text
A_(i+2) = A_i OR A_(i+1).
```

Thus only roots `A_0,A_1` remain.

### Affine-rank block B

On variables `(a_j,b_j,c_j,d_j)` for `j=0,...,k-1`, put canonical `0x16`
EXACT-ONE gates on `abc`, `abd`, `acd`, plus bridges
`(d_(j-1),b_j,c_j)` for `j>=1`. There are `4k-1` such outputs. Their canonical
target-one affine hulls are parity-one equations and have rank `4k-1`.

Add one `0x17` majority output inside B and one `0x17` cross-block output on
`(A_0,a_0,b_0)`. Total input size is `n=8k` and total output size is
`m=n+1`.

The functional heads live only in A, so every B variable remains a root. The
B affine equations are therefore root-supported. We have

```text
f = 4k-2,
|Q| = 4k+2,
R = 4k-1,
eta = 3.
```

Exactly eight relaxed assignments remain and four output coordinates are
unselected, so the hybrid avoider searches a constant-size domain for every
`k`.

## Theorem 4 — previous parameters stay large

On the same family:

```text
V97:  lambda = 8k.
V101: mu     = k+3.
V102: beta   = Theta(k), in particular beta >= 3k.
V103: nu     = 4k+1.
V104: eta    = 3.
```

For V97, the support is connected and every input has degree at least two, while
all gates are essential ternary, so the unused/leaf/unary reducer leaves every
input.

For V101, the A cycle admits at most `4k-2` acyclic distinct heads and attains
that bound. The B `0x16` block admits exactly `3k-1` heads as proved in V103;
majority outputs admit none. The blocks have disjoint possible heads, yielding
`(4k-2)+(3k-1)=7k-3` selected heads and exactly `k+3` roots.

For V102, the three internal `0x16` supports in every B gadget force at least
three conditioned B variables, hence `beta>=3k`. Conditioning all A variables
and `b_j,c_j,d_j` in every B gadget gives a linear-size backdoor, so
`beta=Theta(k)`.

For V103, all `0x1e` and `0x17` canonical fibers have full affine hull; only the
B `0x16` block contributes rank, exactly `4k-1`. Thus
`nu=8k-(4k-1)=4k+1`.

## Boundary

V104 does not provide a polynomial-time algorithm for finding an optimal hybrid
certificate. The theorem is constructive given a polynomially checkable
certificate, and the strict family has an explicit certificate. No unrestricted
polynomial-time `NC0_3-Avoid` algorithm, published worst-case improvement,
novelty claim, circuit lower bound, or P-versus-NP resolution follows.
