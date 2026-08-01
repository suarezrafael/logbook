# Laboratory V75 — symbolic prefix-count circuit

## Status

Internally verified laboratory candidate. Promotion still requires quick, full, and LaTeX GitHub Actions on one final commit, followed by a final-diff Copilot review with no unresolved actionable finding.

## Main result

V75 compiles the V74 weighted affine-residual dynamic program into one monotone arithmetic DAG representing

```text
P_C(u_1,v_1,...,u_m,v_m)
  = sum_{x in {0,1}^n} product_i z_{i,C_i(x)},
```

where `z_{i,0}=u_i` and `z_{i,1}=v_i`.

The coefficient selected by one bit from each pair is exactly the preimage count of that output. Prefix counts are obtained by fixing the selected paired variables to `1/0` and leaving both variables of each unfixed output at one.

For a supplied gate branch decomposition of boundary width `b`, the arithmetic DAG has

```text
S = O(m A(b)^2)
```

operations, apart from polynomial-time affine operations. Incremental evaluation along one prefix-search path uses

```text
O(S + sum_i D_T(i))
```

arithmetic reevaluations, where `D_T(i)` is the dependency-cone size of output coordinate `i`. The branch construction gives

```text
D_T(i) = O(A(b)^2 depth_T(i)).
```

Thus a supplied height-`O(log m)` decomposition gives

```text
O(m log(m) A(b)^2 poly(n,m)).
```

This improves V74's repeated-DP `O(m^2 A(b)^2 poly(n,m))` bound only in the balanced or low-external-path-length regime. A caterpillar decomposition has external path length `Theta(m^2)`, so V75 does not establish an unconditional improvement for arbitrary supplied decompositions.

## Verification

- 4,096 exhaustive two-input, three-output circuits;
- 32,768 exact output coefficients;
- 61,440 exact prefix evaluations;
- 4,096 incrementally constructed avoided outputs;
- 48 seeded ternary circuits checked on balanced and caterpillar trees;
- 6,144 seeded coefficient checks and 12,192 seeded prefix checks across both shapes;
- fresh reevaluation after every dynamic change;
- independent truth-table verifier that imports neither the symbolic builder nor the affine engine;
- tree-shape identities through 64 leaves.

## Files

- `SYMBOLIC_PREFIX_CIRCUIT.md` — theorem, proof invariant, complexity, and literature boundary;
- `V75_SYMBOLIC_PREFIX_THEOREM.tex` — formal standalone module;
- `symbolic_prefix_circuit.py` — arithmetic DAG and incremental evaluator;
- `v75_symbolic_prefix.py` — deterministic exhaustive/seeded experiment generator;
- `verify.py` and `verify_independent.py` — primary and independent verification;
- `RESULTS.json` — frozen quantitative snapshot;
- `EXHAUSTIVE_RESULTS.md` — finite evidence summary;
- `V76_CORE_CONTEXT.md` — next laboratory handoff.

## Scientific boundary

V75 does not prove automatic width-preserving balancing, unrestricted `NC0_3-Avoid`, a general polynomial-time algorithm, a superpolynomial lower bound, a size-preserving simulation to a standard proof or branching model, novelty, peer review, or any consequence for P versus NP.
