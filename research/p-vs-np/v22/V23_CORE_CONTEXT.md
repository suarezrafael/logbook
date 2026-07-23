# V23 Core Context

## Active theorem candidate

If normalized outputs satisfy `g_i(x)=1 iff p_i(x)=0` and the `p_i` lie in a `D`-dimensional vector space, then `m>D` gives an avoided output through a nonzero dependency and a one-violation target.

For symmetric outputs of fixed fan-in at most `k`, choose a prime `q>k`, complement each coordinate so the accepting weight set has size at most `d=floor((k+1)/2)`, and use

```text
p_i(x)=product_{r in S_i}(L_i(x)-r).
```

After multilinearization the degree is at most `d`, so the uniform condition is

```text
m > sum_{j=0}^d binom(n,j).
```

Fan-in four: `m>1+n+binom(n,2)`.

## Verification

- 1,022 truth-table normalizations;
- 65 above-threshold circuits;
- 60 rank-deficient circuits below the uniform threshold;
- 125/125 independently verified certificates;
- zero failures.

## Limitation

Independent polynomial families exist below the ambient dimension. Dimension counting alone cannot lower the bound. The theorem concerns symmetric outputs, not arbitrary `NC0_4`.

## V23 target

Combine sparse quadratic polynomial supports with incidence-hypergraph structure, degeneracy, treewidth, component decomposition, or sparse-matrix rank bounds to lower the symmetric fan-in-four threshold below `n^2/2`. Search for matching high-rank examples and preserve counterexamples to every proposed improvement.
