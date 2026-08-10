# V95 literature boundary

## Huang–Li–Zhong, ITCS 2026

Shengtang Huang, Xin Li, and Yan Zhong, *Range Avoidance and Remote Point: New
Algorithms and Hardness*, ITCS 2026, LIPIcs 362:79.

Their published local algorithm for `NC0_k-Avoid[n,n+1]` runs in

```text
O(n * 2^(((k-2)/(k-1))*n)),
```

which is `O(n*2^(n/2))` for `k=3`. V95 does not improve that runtime. It proves
that one particular exact strategy — reproducing the V92 canonical halving word
— contains PP-hard information.

The distinction is mandatory: Huang–Li–Zhong solve the total search task of
finding *some* avoided output, whereas the V95 barrier concerns one specified
canonical output function.

## Fenner–Fortnow–Kurtz, JCSS 1994

Stephen A. Fenner, Lance J. Fortnow, and Stuart A. Kurtz, *Gap-definable counting
classes*, Journal of Computer and System Sciences 48(1):116–148, 1994.

Their GapP framework supplies the standard counting-complexity calibration
behind V94's source theorem `COMPARE-#3SAT_<=` being PP-complete. V95 reuses
that already-proved source theorem and changes only the target compiler: the
hard comparison is now read from a genuinely canonical next bit.

## Gajulapalli–Golovnev–Nagargoje–Saraogi, APPROX/RANDOM 2023

Karthik Gajulapalli, Alexander Golovnev, Satyajeet Nagargoje, and Sidhant
Saraogi, *Range Avoidance for Constant-Depth Circuits: Hardness and Algorithms*,
APPROX/RANDOM 2023.

Their work emphasizes that the complexity of `NC0_3-Avoid` at low stretch is a
central unresolved regime and gives conditional explicit-construction hardness
at larger-than-minimal stretch. V95 does not upgrade those total-search
hardness consequences. Its target is narrower: exact reproduction of the
canonical minority/tie-zero trajectory at minimal stretch.

## Prior-art search boundary

Targeted searches over arXiv, ECCC, and the current range-avoidance literature
for combinations of

```text
canonical prefix / canonical path,
minority or halving path,
PP-hard next bit,
range avoidance,
count-comparison trajectory
```

did not surface a direct statement matching the V95 balanced-definition loader
or the exact canonical-next-bit reduction.

This is **not** a novelty claim. Search coverage is incomplete, terminology may
differ, and the result has not been externally reviewed. V95 therefore keeps

```text
novelty_confirmed = false,
peer_reviewed = false.
```

## Exact boundary of the V95 theorem

Proved internally:

```text
fixed seven-type locality<=3 language + M=N+1
+ genuinely V92-canonical all-zero loader prefix
    -> specified next canonical bit is PP-hard.

exact full V92 canonical word in polynomial time
    -> P=PP -> P=NP.
```

Not proved:

```text
finding any avoided output
    -> PP-hard,

polynomial NC0_3-Avoid
    -> P=PP,

Huang-Li-Zhong's algorithm
    -> must reproduce the V92 word,

P != NP or P = NP.
```
