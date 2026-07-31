# Complete three-variable search

## Domain

The search starts from the six essential ternary NPN classes with no affine fiber:

```text
0x07  0x16  0x17  0x19  0x1b  0x1e
```

It generates every NPN transform, both output fibers, and every disjoint partition of each non-affine fiber into two nonempty affine cells.

Exact deduplication gives:

```text
168 distinct non-affine fibers
 56 of size 3
 56 of size 4
 56 of size 5

392 affine-cell gate variants
112 fibers with three partitions
 56 fibers with one partition
```

## Complete ordered state census

Exact signature-state dynamic programming considers all ordered systems of four gate variants without enumerating `392^4` histories separately. The number of distinct reachable states after `k` gates is:

```text
k = 0  1    2    3    4
    1 392  919  919  919
```

At four gates, reachable states are distributed by the number of consistent complete branches as follows:

```text
0 branches :   1 state
1 branch   :  50 states
2 branches : 420 states
3 branches : 392 states
4 branches :  56 states
```

No state in this exact domain has more than four consistent full branches.

## Canonical tree census

Using the six canonical representatives, both fibers and all affine partitions produces 30 canonical gate variants. All multisets of four variants are enumerated:

```text
C(30+4-1,4) = 40,920 systems.
```

The consistent-branch distribution is:

```text
0 : 26,658
1 :  9,111
2 :  3,122
3 :  1,908
4 :    121
```

The maximum optimal leaf count is `L_aff=11`, and the maximum residual-state count reached by the selected policy is `G_aff=17`.

One maximum-leaf witness uses canonical variant indices `[0,8,9,10]`: one partition of the `0x07` zero fiber together with all three affine partitions of the `0x17` zero fiber. All witness indices and the complete metric distribution are preserved in `RESULTS.json`.

## Interpretation

The complete `n=3` data show strong pruning, but finite saturation at 919 states does not imply an asymptotic bound. No theorem extrapolating these counts is claimed.
