# V104 theorem ledger — canonical affine-first hybrid compression

## Definition — canonical affine-first parameter

For `C:{0,1}^n->{0,1}^m`, `m>n`, choose the canonical target bit of each output
as its minority value, breaking ties toward zero.

**Affine phase.** Replace each canonical target fiber by its affine hull and scan
output blocks in order. Retain a block exactly when its equations increase the
current GF(2) rank. Let the final rank be `R`. Protect every input variable
occurring with nonzero coefficient in any retained affine equation.

**Functional phase.** Scan outputs not retained by the affine phase. For each
output, scan its support variables in increasing index order. Add the first
canonical functional anchor whose head is unprotected, has not already been used
as a head, and keeps the tail-to-head dependency graph acyclic. Let the final
number of functional heads be `f`.

Define the deterministic parameter

```text
eta_AF(C) = n - R - f.
```

All local fiber tests, rank updates, variable protection, and cycle tests take
polynomial time for bounded-locality gates.

## Theorem 1 — safe affine-first relaxation

Every original input realizing all selected target bits also satisfies the
selected affine-hull equations and selected total functional graph relations.
Thus the combined relation is a safe relaxation: a residual word absent from the
relaxed image is absent from the original image after selected target bits are
restored.

## Theorem 2 — protected rank remains on functional roots

Every variable occurring in a retained affine equation is protected before the
functional phase. Protected variables are forbidden as functional heads.
Therefore every retained affine equation is supported entirely on the final root
set of the functional DAG, and its rank remains exactly `R` when the system is
viewed on those roots.

## Theorem 3 — canonical affine-first avoider

V104 constructs a missing output deterministically in

```text
O(2^eta_AF(C) poly(N)).
```

### Proof

The functional phase selects `f` distinct heads and keeps the dependency graph
acyclic, so the final root set `Q` has

```text
|Q| = n-f.
```

Every root assignment extends uniquely through the total functional graph
relations. By Theorem 2, the retained affine equations form a rank-`R` system on
`Q`. When consistent, they leave exactly

```text
2^(|Q|-R) = 2^(n-f-R) = 2^eta_AF
```

root assignments and therefore the same number of full relaxed assignments.

Let `s_A` be the number of retained affine output blocks. Every retained block
increased rank by at least one, hence `s_A<=R`. The number of unselected output
coordinates is therefore

```text
m-s_A-f >= m-R-f > n-R-f = eta_AF.
```

Evaluate every unselected original output gate on the relaxed assignments. At
most `2^eta_AF` residual words occur in a cube of dimension strictly greater
than `eta_AF`, so a missing residual word is found by hashing the observed words
and testing a fixed list of distinct candidates. Restore the canonical target
bits on all selected affine and functional coordinates. Any original preimage of
the resulting word would lie in the relaxed domain and produce the missing
residual word, contradiction.

If a canonical target fiber is empty, its target bit is immediately absent. If
the affine phase detects inconsistency when adding a block, the selected target
pattern through that block is unrealizable and arbitrary completion of the other
outputs gives a missing word.

## Theorem 4 — strict infinite-family separation

For every `k>=1`, build a circuit with `n=8k` and `m=n+1`.

### Block A — balanced functional cycle

On variables `A_0,...,A_(4k-1)`, put canonical `0x1e` gates on all cyclic
triples

```text
(A_i,A_(i+1),A_(i+2)) mod 4k.
```

Canonical `0x1e` is balanced non-affine, so its canonical fiber has full affine
hull and contributes no rank in the affine phase. Its target-zero fiber is the
total graph

```text
A_(i+2) = A_i OR A_(i+1).
```

In output order the functional phase accepts the first `4k-2` such relations;
the final two would create cycles and are rejected. Hence Block A contributes
`f=4k-2` functional heads.

### Block B — affine-hull rank chain

On another `4k` variables grouped as `(a_j,b_j,c_j,d_j)`, put `0x16`
EXACT-ONE gates on `abc`, `abd`, and `acd` for every gadget, plus bridge gates
`(d_(j-1),b_j,c_j)` for `j>=1`. There are `4k-1` gates. Their canonical
target-one hulls are parity-one equations and have rank exactly `4k-1`.
Therefore the affine phase retains all of them and protects every Block B
variable.

Add one `0x17` majority output inside B and one cross-block `0x17` output on
`(A_0,a_0,b_0)`. Majority canonical fibers have full affine hull and no
functional anchor.

The canonical algorithm itself therefore obtains

```text
R       = 4k-1,
f       = 4k-2,
eta_AF  = 8k-(4k-1)-(4k-2) = 3.
```

The relaxed domain always has eight assignments, and exactly four output
coordinates remain unselected.

## Theorem 5 — preceding parameters remain linear

On the same connected exact-stretch family:

```text
V97:  lambda = 8k,
V101: mu     = k+3,
V102: 3k <= beta <= 7k,
V103: nu     = 4k+1,
V104: eta_AF = 3.
```

The support is connected and every input has degree at least two, so V97 has no
unused/leaf/unary peel and `lambda=n`.

For V101, Block A contributes at most and exactly `4k-2` acyclic distinct heads.
Block B contributes at most and exactly `3k-1` heads by the V103 gadget theorem;
majority contributes none. The two head sets are disjoint, so the total maximum
is `7k-3` and `mu=8k-(7k-3)=k+3`.

For V102, every Block B gadget's three internal `0x16` triples require at least
three backdoor variables, giving `beta>=3k`. Fixing all `4k` Block A variables
plus `{b_j,c_j,d_j}` in every B gadget gives a strong affine backdoor of size
`7k`, so `beta=Theta(k)`.

For V103, `0x1e` and `0x17` canonical fibers have full affine hull. Only Block B
contributes rank `4k-1`, hence `nu=8k-(4k-1)=4k+1`.

## Falsification status

Before official candidate registration, the canonical implementation was checked
against complete original ranges on 1,800 random exact-stretch circuits with
`2<=n<=7`, with zero failures. The strict family was checked completely at
`k=1,2`, the canonical parameter identity `eta_AF=3` through `k=7`, and 712
additional random mutations of its residual outputs against complete original
ranges, again with zero failures.

## Nonclaims

No worst-case sublinear bound on `eta_AF` is proved. V104 does not put
unrestricted `NC0_3-Avoid` in P, improve the unrestricted published worst-case
exponent, establish a new circuit lower bound, confirm novelty or peer review,
or resolve P versus NP.
