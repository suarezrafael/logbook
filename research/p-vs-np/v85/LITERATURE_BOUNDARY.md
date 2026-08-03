# V85 literature boundary

## Algorithmic frontier

Gajulapalli, Golovnev, Nagargoje, and Saraogi, *Range Avoidance for
Constant-Depth Circuits: Hardness and Algorithms* (APPROX/RANDOM 2023; ECCC
TR23-021), prove that an `FP^NP` algorithm for `NC0_3-Avoid` at
`m=n+n^(2/3)` would yield explicit rigid matrices and superlinear lower bounds
for logarithmic-depth circuits.

Guruswami, Lyu, and Yuan, *Cell-Probe Lower Bounds via Semi-Random CSP
Refutation: Simplified and the Odd-Locality Case* (arXiv:2507.22265; SODA
2026), use a reduction to strong XOR refutation for odd locality. Their
avoidance regime for locality `t` requires roughly

```text
m >= c^t n^((t-1)/2) log n,
```

which is `Omega(n log n)` for `t=3`.

Korten, Pitassi, and Impagliazzo, *Stronger Cell Probe Lower Bounds via Local
PRGs* (FOCS 2025; ECCC TR25-030), establish a tight connection among local
PRG cryptanalysis, `NC0` range avoidance, and static data-structure lower
bounds.

## Remote point

Huang, Li, and Zhong, *Range Avoidance and Remote Point: New Algorithms and
Hardness* (ITCS 2026, LIPIcs 362:79), give modern algorithms and hardness
connections for Remote Point. The V85 prefix-pair theorem is an exact-counting
lemma; novelty can only attach to a verified composition with the historical
bounded-width engine.

## Proof complexity and surjectivity

Alekhnovich, Ben-Sasson, Razborov, and Wigderson study PRG tautologies in
propositional proof systems. Ren, Wang, and Zhong connect Avoid hardness and
proof-complexity generators through demi-bits at ITCS 2026. Neither result
transfers automatically to the V80 families: the predicate, encoding,
expansion parameters, proof system, field, and auxiliary variables must all be
matched.

Kari's cellular-automata surjectivity results are neighboring prior art, not a
finite `NC0_3` circuit-surjectivity theorem. The standard general-circuit
`Pi_2^P` reduction is retained only as calibration; locality-three hardness is
not claimed.

## Novelty discipline

- The support-only counting theorem corrects a false proposed impossibility
  statement; it is elementary and not presented as a literature-first result.
- The syndrome/C4 theorem is machine-audited but may have prior formulations in
  Tanner-graph, algebraic-hypergraph, or local-polynomial language.
- The ternary Fourier classification is a finite analytic lemma, not a new
  global avoidance algorithm.
- No result here crosses the `n+n^(2/3)` rigidity barrier.
