# Overlap branch-growth report

## Model

The probe uses the positive fiber of the ternary representative `0x07`:

```text
{000,001,010}.
```

It has three disjoint two-affine-cell partitions:

```text
{000} | {001,010}
{000,001} | {010}
{000,010} | {001}
```

Each gate chooses an ordered support of three distinct global variables and one of these partitions.

## Regular cyclic controls

For each `4<=n<=12`, two systems with `m=n+1` were checked:

- `constant`: every cyclic support `(i,i+1,i+2 mod n)` uses partition 0, with one extra partition-1 gate;
- `rotating`: cyclic gates use partitions `i mod 3`, with one additional nonlocal gate.

All 18 systems have `c=1`. This rules out growth for these explicit patterns only.

## Seeded random overlap probe

The deterministic generator uses seed `42` and samples 4,000 systems:

1. choose `n` uniformly from `4,...,12`;
2. put `m=n+1`;
3. for each gate, sample an ordered support without replacement;
4. choose one of the three partitions uniformly.

The first `n=10` system with exactly `c=16` occurs at iteration 344 and is preserved in `WITNESSES.json`.

The strongest system in this run occurs at iteration 2360:

```text
n=11
m=12
c=36
L_aff=61
L_greedy=62
G_aff=108
```

Maximum observed `c` by dimension:

```text
n=4: 4
n=5: 6
n=6: 8
n=7: 10
n=8: 16
n=9: 18
n=10: 26
n=11: 36
n=12: 30
```

These maxima are sample-dependent and are not monotonicity claims.

## Interpretation

The experiment refutes the idea that the small `n=3` and `n=4` branch counts remain uniformly tiny under overlapping supports. It does not show `2^Omega(n)` growth and does not prove a polynomial upper bound.

The main next question is whether one can extract an explicit scalable mechanism from the `c=36` witness. Tree and DAG complexity must remain separate: `c` lower-bounds tree leaves, while residual-state merging may still reduce a branching DAG.

## Scientific boundary

No unrestricted `NC0_3-Avoid` algorithm, proof-system lower bound, circuit lower bound, novelty claim, or P-versus-NP implication follows from this finite experiment.
