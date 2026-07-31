# Formal correction to Laboratory V53

The V53 union-free substitution lemma remains correct. The following claims are retracted:

1. `incidence girth > 4t => t-union-free`;
2. the derived stretch-one `AND3` family with syndrome degree `Omega(log n)`.

The error was assuming that, after deleting common edges from equal-union families, both residual families were nonempty. Nested collisions do not satisfy this assumption and need not create a cycle.

An acyclic counterexample is

```text
e={0,1,2}, f0={0,3,4}, f1={1,5,6}, f2={2,7,8},
union({f0,f1,f2})=union({e,f0,f1,f2}).
```

V54 proves the stronger corrected fact: every positive-excess `k`-uniform hypergraph has a nonempty 2-core, so pure `AND_k` has an explicit separator of degree at most `k+1`. For `AND3`, the universal bound is four.

The UF2 and UF3 finite examples remain correct, with exact degrees three and four. No email asserting the retracted asymptotic theorem was sent.
