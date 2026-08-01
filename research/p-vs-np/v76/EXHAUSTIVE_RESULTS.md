# V76 finite validation ledger

## Exact Pareto recurrence

The exact subset recurrence for nondominated `(width,height,EPL)` states was
checked against direct enumeration of every rooted unordered binary tree for
all simple rank-at-most-three support families on four variables with at most
four gates:

```text
1,470 support families,
16,212 rooted-tree evaluations,
zero disagreements.
```

## Exhaustive four-variable classification

The support universe consists of the `14` nonempty subsets of four variables of
size at most three. Every simple family of size one through seven was analyzed:

```text
m=1:      14
m=2:      91
m=3:     364
m=4:   1,001
m=5:   2,002
m=6:   3,003
m=7:   3,432
----------------
total: 9,907
```

No family through six gates needs extra width at the perfect height cap
`ceil(log2 m)`. Among the `3,432` seven-gate families, exactly **six** have
additive inflation one. They are variable-renamings of the canonical witness.

## Canonical perfect-height witness

For

```text
{0}, {1}, {0,2}, {0,3}, {1,2}, {1,3}, {2,3},
```

direct enumeration of all `10,395` gate trees gives

```text
(2,4,21), (3,3,20).
```

The first triple minimizes width; the second attains minimum possible height.
This separates the width optimum from perfect height, not from asymptotic
logarithmic height.

## Labelled-cluster four-cut audit

The primary verifier reconstructs unrooted supplied trees and exhausts connected
labelled clusters with at most two boundary vertices. It permits gate labels to
be omitted at cluster leaf vertices, matching the labelled-top-tree boundary
rule. The deterministic audit covered

```text
47,565 connected vertex clusters,
101,213 valid labelled cluster states,
1,470 exact width-optimal source trees through n=4,m=4,
128 sampled source trees for the seven-gate witness,
64 seeded random rank-at-most-three instances,
seed 760076.
```

Every state was covered by at most four original branch-edge middle sets. The
maximum four was attained. The independent verifier repeats the raw-incidence
logic with separately written code on 256 witness source trees.

## Regression families

- OR paths were recomputed through eight gates and retain their exact width
  profiles.
- V72 private-vertex complete-binary-tree supports were recomputed at underlying
  heights one, two, and three (`m=2,6,14`).
- At `m=14`, the exact frontier is `(2,5,55),(3,4,54)`, another finite separation
  between width optimum and perfect height.

All deterministic values are stored in `RESULTS.json`.
