# V104 canonical affine-first theorem

This file supersedes the supplied-certificate formulation as the intended V104
algorithm.

## Canonical preprocessing

For `C:{0,1}^n->{0,1}^m`, `m>n`:

1. For each output choose the canonical target bit: minority value, tie to zero.
2. Replace that target fiber by its affine hull and scan output blocks in order.
   Retain a block iff its equations increase the current GF(2) rank. If the
   system becomes inconsistent, the retained target pattern already certifies
   an absent output.
3. Let `R` be the final affine rank. Protect every input variable occurring with
   nonzero coefficient in any retained affine equation.
4. Scan outputs not retained in the affine basis. For each, scan support
   variables in increasing index order. Add the first canonical functional
   anchor whose head is unprotected, unused, and whose tail-to-head edges keep
   the dependency graph acyclic.
5. Let `f` be the number of selected functional heads and define

```text
eta_AF(C) = n - R - f.
```

Every step above is polynomial time for bounded-locality gates.

## Theorem

The canonical preprocessing constructs an avoided output deterministically in

```text
O(2^eta_AF(C) poly(N)).
```

### Proof

Let `P` be the protected variables. By construction every retained affine row is
supported on `P`. No variable of `P` is ever chosen as a functional head, so
`P` is contained in the final root set `Q` of the functional DAG.

The retained affine equations therefore remain a rank-`R` linear system on the
root variables. The functional phase selects `f` distinct heads, so

```text
|Q| = n-f.
```

Because each selected functional fiber is relaxed to a total graph relation,
every root assignment has exactly one extension through the acyclic dependency
DAG. The consistent affine root system has exactly

```text
2^(|Q|-R) = 2^(n-f-R) = 2^eta_AF
```

solutions, hence the complete canonical relaxed domain has exactly that many
assignments.

If `s_A` output blocks were retained during the affine phase, each increased
rank by at least one, hence `s_A<=R`. After removing the `s_A+f` selected output
coordinates,

```text
m-s_A-f >= m-R-f > n-R-f = eta_AF.
```

Evaluate all unselected original gates on the `2^eta_AF` relaxed assignments.
At most `2^eta_AF` residual words occur in a cube of dimension strictly larger
than `eta_AF`. Choose a residual word not observed and restore all selected
target bits. Any original input producing the resulting full word would satisfy
every selected exact fiber, hence every affine-hull and functional-graph
relaxation, contradicting the missing residual word.

If a canonical fiber is empty, its canonical output value is immediately
absent. If the canonical affine system becomes inconsistent while adding a
block, the target values of the retained blocks plus the conflicting block
cannot be realized simultaneously, so arbitrary completion of the other output
bits gives an avoided word.

## Strict-family behavior

On the V104 `n=8k,m=n+1` family, the affine-first phase retains exactly the
`4k-1` independent `0x16` parity-hull blocks and protects the entire second
`4k`-variable group. The `0x1e` and `0x17` canonical fibers have full affine
hull and contribute no rank.

The functional phase then scans the cyclic `0x1e` outputs. Their canonical
zero-fiber has the unique graph head `A_(i+2)`, so the first `4k-2` anchors are
accepted and the final two are rejected by acyclicity. No `0x17` output has a
functional anchor. Therefore

```text
R=4k-1,
f=4k-2,
eta_AF=8k-(4k-1)-(4k-2)=3.
```

This behavior is produced by the deterministic algorithm itself; no certificate
is supplied.

## Falsification snapshot

Before candidate registration:

- 1,800 random exact-stretch circuits with `2<=n<=7` checked against their
  complete original ranges: zero failures;
- strict-family canonical output checked against the complete original range at
  `k=1,2`;
- canonical preprocessing gives `eta_AF=3` on the strict family for `k=1..7`;
- an additional 712 random mutations of the strict family's four residual gates
  were checked against complete original ranges: zero failures.

These are regression evidence; the theorem is the symbolic argument above.

## Nonclaims

The canonical parameter `eta_AF` may be linear on worst-case circuits. No
unrestricted polynomial-time algorithm, improved general worst-case exponent,
novelty claim, circuit lower bound, peer review, or P-versus-NP resolution is
asserted.
