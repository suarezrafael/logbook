# Spine family theorem

## Convention

For local coordinates `(a,b,c)`, use truth-table index `4a+2b+c`. The positive fiber of mask `0x07` is

```text
{000, 001, 010}.
```

Thus every point in this fiber pins the first coordinate to zero.

## Construction

Fix `k>=1`. Use variables

```text
s, (u_0,v_0), ..., (u_{k-1},v_{k-1}).
```

Hence `n=2k+1`.

For each `t`, add two motif gates on `(s,u_t,v_t)` and `(s,v_t,u_t)`. Each uses the affine-cell partition

```text
C^0 = {000}
C^1 = {001,010}.
```

The singleton is affine. The second cell is the affine line

```text
s=0, u_t xor v_t=1.
```

Add two anchors on `(s,u_0,v_0)`:

```text
mask 0x0b: {000} dot-union {001,011}
mask 0x0d: {000} dot-union {010,011}.
```

Both masks are in the NPN orbit of `0x07`; all four anchor cells are affine. The total number of gates is

```text
m=2k+2=n+1.
```

## Theorem

The number of consistent complete branch signatures is

```text
c(S_k)=2^(k-1)=2^((n-3)/2).
```

Consequently every complete inconsistency-pruned affine-cell branching tree has at least `2^((n-3)/2)` leaves.

Under the fixed order

```text
M_0a, M_0b, A_0b, A_0d, M_1a, M_1b, ..., M_{k-1}a, M_{k-1}b,
```

and after existentially projecting variables absent from all remaining supports, the residual-state DAG has exactly

```text
G_proj=3k+4
```

nonterminal states, plus shared accepting and inconsistent terminals.

## Proof of the branch count

Every cell pins `s=0`.

For a free motif `t>=1`, the assignment `(u_t,v_t)=(0,0)` gives branch pair `00`. The assignments `(0,1)` and `(1,0)` both give branch pair `11`. The assignment `(1,1)` is outside the motif fiber. Therefore each free motif contributes exactly two branch signatures.

For motif zero, the first anchor excludes `(u_0,v_0)=(1,0)` and the second excludes `(0,1)`. The motif itself excludes `(1,1)`. Only `(0,0)` remains, so all four motif-zero/anchor branch bits are fixed.

Conditioned on `s=0`, different free motifs use disjoint variable pairs. Their branch choices therefore form a Cartesian product of size `2^(k-1)`.

A complete consistent signature cannot share a terminal leaf with a different complete signature. Thus `L_aff>=c(S_k)`.

## Proof of the projected DAG bound

After motif zero and its anchors, the projected residual on variables used later is only `s=0`; this prefix contributes seven nonterminal states.

For every free motif, the first gate creates two feasible affine states: `u_t=v_t=0` and `u_t xor v_t=1`, both with `s=0`. The second duplicate gate has one forced consistent branch in each state. Once both gates are consumed, `u_t,v_t` no longer occur, so existential projection removes their equations and both paths merge back to the same residual `s=0`.

Each free motif therefore adds exactly three nonterminal states. The total is

```text
7+3(k-1)=3k+4.
```

This is an explicit upper bound in the repository-local projected model. It is not a lower bound or equivalence result for a standard branching-program or proof system.
