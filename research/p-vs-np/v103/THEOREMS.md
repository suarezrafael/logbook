# V103 theorem ledger — affine-hull rank compression

## Theorem 1 — safe affine-hull relaxation

For output gate `g_i`, target bit `b_i`, and exact fiber `F_i`, replacing the
constraint `x in F_i` by `x in aff(F_i)` is safe for range avoidance because
`F_i subseteq aff(F_i)`. Therefore any output word proved impossible after the
relaxation is also impossible for the original circuit.

## Theorem 2 — rank-compressed avoider

Let `C:{0,1}^n->{0,1}^m`, `m>n`. Choose each target bit canonically as the
minority value, breaking ties toward zero. If a chosen fiber is empty, its target
bit is immediately absent. Otherwise lift affine equations defining every
chosen local hull to the global input variables.

If the combined affine system is inconsistent, the complete canonical target
word is outside the range.

Assume it is consistent and let its coefficient rank be `R`. Scan output blocks
and keep a block exactly when its equations increase the current rank. Let `s`
be the number of kept blocks. Every kept block increases rank at least once, so
`s<=R`, while the kept blocks span rank `R`. Their solution set therefore has
exactly

```text
2^(n-R) = 2^nu
```

points, where `nu=n-R`.

There are `m-s` unkept output coordinates and

```text
m-s >= m-R > n-R = nu.
```

Evaluate the original unkept gates on all relaxed solutions. At most `2^nu`
residual output words occur, while the residual cube has `2^(m-s)>2^nu` words.
A missing residual word can be found in `O(2^nu poly(N))` time by hashing the
observed words and testing `|observed|+1` fixed distinct candidate words.
Reinsert the kept canonical target bits. Any original input producing that full
word would satisfy the kept exact fibers, hence the kept affine hulls, and would
have produced the supposedly missing residual word, contradiction.

Thus the avoider is deterministic in `O(2^nu poly(N))` time.

## Theorem 3 — exact essential-ternary hull boundary

Among 218 essential ternary predicates, exactly 162 have a proper affine hull
for the canonical target fiber and exactly 56 have full affine hull.

For an unbalanced predicate, the canonical minority fiber has at most three
points, hence affine dimension at most two. For a balanced predicate the target
fiber has four points. If its affine hull is proper, four points in `GF(2)^3`
must form an affine plane; the complementary four points form the other coset,
so the predicate is affine. Conversely an affine balanced predicate has plane
fibers. Therefore the full-hull class is exactly the balanced non-affine class.
The `162/56` count is recomputed exhaustively by both verifiers.

## Theorem 4 — strict `nu=1` family

For `k>=1`, use `n=4k` variables grouped as `(a_j,b_j,c_j,d_j)`. Put `0x16`
gates on `abc`, `abd`, `acd` in every gadget and bridge consecutive gadgets by a
`0x16` gate on `(d_(j-1),b_j,c_j)`. Add two `0x17` outputs, yielding `m=n+1`.

Canonical `0x16` target one has hull equation `x xor y xor z = 1`. In a gadget,

```text
a+b+c=1
a+b+d=1
a+c+d=1
```

implies `a=1` and `b=c=d=t`. A bridge gives

```text
t_(j-1)+t_j+t_j = 1,
```

so `t_(j-1)=1`. Hence all `t_0,...,t_(k-2)` are one and only `t_(k-1)` is free.
The relaxed system has dimension one and rank `4k-1=n-1`, so `nu=1`.

## Theorem 5 — exact V101 parameter on the strict family

Only the `0x16` gates admit V101 functional anchors. For a fixed topological
order, a selected head is the maximum variable of its support. The three
internal triples `abc`, `abd`, `acd` have at most two distinct maxima in any
order on `a,b,c,d`; every bridge adds at most one further head. Thus at most

```text
2k+(k-1)=3k-1
```

heads can be selected and `mu>=4k-(3k-1)=k+1`.

Equality is attained. In gadget zero use heads `c_0,d_0`. For every later
gadget use the bridge with head `c_j`, then internal `abc` with head `a_j`, then
internal `abd` with head `d_j`. This is acyclic with distinct heads, so exactly
`3k-1` heads are selected and `mu=k+1`.

## Theorem 6 — exact V102 parameter on the strict family

For `0x16` EXACT-ONE, a strong affine backdoor must condition at least two of the
three support variables; any two suffice. In one four-variable gadget the three
supports `abc`, `abd`, `acd` therefore force at least three selected variables.
Thus `beta>=3k`.

Selecting `{b_j,c_j,d_j}` for every gadget has size `3k`. It meets every internal
support in two variables, fixes each bridge in all three local variables, and
fixes two variables of both `0x17` outputs. Hence it is a strong affine backdoor
and `beta=3k`.

## Corollary — four-parameter separation

The family satisfies

```text
lambda = 4k,
mu     = k+1,
beta   = 3k,
nu     = 1.
```

The support is connected with minimum input degree at least two, so V97 does not
peel. V100 performs zero graph-fiber peels because both `0x16` and `0x17` are in
its residual hard set. Thus V103 is a strict asymptotic extension of the V97,
V101, and V102 structural parameters on this family.

## Nonclaims

No theorem here bounds `nu` on arbitrary `NC0_3` circuits, proves unrestricted
polynomial-time range avoidance, improves the unrestricted worst-case exponent,
establishes a new circuit lower bound, confirms novelty, or resolves P versus NP.
