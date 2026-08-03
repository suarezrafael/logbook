# V84 literature boundary

## Lower-bound-sensitive target

Gajulapalli, Golovnev, Nagargoje, and Saraogi, *Range Avoidance for
Constant-Depth Circuits: Hardness and Algorithms* (ECCC TR23-021;
arXiv:2303.05044), prove that a polynomial-time algorithm with an NP oracle for
`NC0_3-Avoid` at

```text
m = n + n^(2/3)
```

would give an explicit rigid matrix and hence a superlinear lower bound for
log-depth circuits.

Primary sources:

- https://eccc.weizmann.ac.il/report/2023/021/
- https://arxiv.org/abs/2303.05044

## 2025 deterministic upper regime

Guruswami, Lyu, and Yuan, *Cell-Probe Lower Bounds via Semi-Random CSP
Refutation: Simplified and the Odd-Locality Case* (arXiv:2507.22265), prove a
deterministic `n^O(t)` algorithm for `NC0_t-Avoid` whenever

```text
m >= c_t n^((t-1)/2) log n.
```

For `t=3`, the known deterministic regime is therefore `m >= c n log n`.
This leaves the target `n+n^(2/3)` well below the known upper regime.

Primary source:

- https://arxiv.org/abs/2507.22265

## Broader lower-bound warning

Ren, Santhanam, and Wang, *On the Range Avoidance Problem for Circuits*
(ECCC TR22-048), show among other consequences that an algorithm for
polynomial-stretch `AC0-Avoid` would imply lower bounds against `NC1`.

Primary source:

- https://eccc.weizmann.ac.il/report/2022/048/

## Interpretation for V84

The extraction and local-enumeration theorem is compatible with all three
sources. It solves only the short-girth branch in `FP^NP` and turns the
remaining branch into a logarithmic Hall-expansion promise. It does not bridge
the gap to the 2025 refutation algorithm, construct a rigid matrix, prove a
circuit lower bound, or resolve `P` versus `NP`.
