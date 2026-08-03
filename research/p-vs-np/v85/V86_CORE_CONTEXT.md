# V86 core context — constructive `Eval_H` and certificate hardness

## Frozen output from V85

1. V84's logarithmic Hall-expander restriction is complete for unrestricted
   `NC0_3-Avoid` under `FP^NP` search-Turing reductions.
2. Truth-table-blind lists of size one or two are impossible, but a universal
   list of size `floor(Q/(m-n))+1` exists nonconstructively.
3. Constructing such a list is exactly range avoidance for the structured
   evaluation map `Eval_H`.
4. Every balanced non-affine ternary predicate has low-degree Fourier
   correlation `1/2`; this local fact does not supply the missing global
   refutation.
5. On C4-free supports, constant output-parity syndromes use only affine gates.
6. Exact Hamming-ball pair counting constructs a remote point whenever
   `2^n B(m,r)<2^m`.
7. The actual V75 monotone arithmetic DAG supports truncated-polynomial distance
   evaluation without changing the branch decomposition.
8. Combining V77, V75, and the bound
   `A(b)<=(b+1)2^(floor(b^2/4)+b)` yields a polynomial-time remote-point
   algorithm directly from the circuit whenever support branchwidth is
   `O(sqrt(log m))`, with distance `Omega((m-n)/log m)`.

## Priority one — constructive `Eval_H`

Exploit truth-table reuse across the candidate layers. Test splitters, perfect
hash families, small-bias spaces, and codes aligned with the support
hypergraph. A valid result must construct the missing list, not merely prove it
exists.

The primary quantitative target is to beat generic locality-eleven avoidance
by using the fact that the same gate table is shared across all candidate
layers.

## Priority two — local-surjectivity certificates

Separate polynomially checkable reasons for a local map to be non-surjective:
Hall deficiency, affine syndromes, bounded-width exact distance enumeration,
and other algebraic certificates. Audit the complexity of recognizing
surjectivity for finite locality-three maps. No `Pi_2^P`-completeness claim is
allowed without a surjectivity-preserving bounded-locality gadget.

## Priority three — proof-complexity match

Compare the exact V80 obstruction generators with PRG-tautology lower-bound
hypotheses. Match the predicate, encoding, expansion parameters, proof system,
field, auxiliary variables, and stretch. Record every failed match as a result;
expansion alone is not sufficient for inheritance.

## Priority four — beyond the sqrt-log frontier

Determine whether the width boundary can exceed `O(sqrt(log m))` through:

- compressed or symmetry-quotiented affine residual states;
- faster truncated convolution and incremental semiring evaluation;
- rank-sensitive state bounds below the worst-case `A(2k)` count;
- approximation schemes strong enough to preserve the strict prefix
  pigeonhole invariant.

A valid improvement must either enlarge the polynomial width range, prove a
state-space obstruction, or produce an explicit family saturating the current
quadratic exponent.

## Nonclaims

V86 remains below explicit rigidity, unrestricted circuit lower bounds, and
`P != NP` unless a separate fully verified theorem crosses those boundaries.
