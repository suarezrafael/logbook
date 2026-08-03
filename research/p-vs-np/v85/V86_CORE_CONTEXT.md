# V86 core context — constructive remote points and certificate hardness

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

## Priority one — source-level V75 integration

Load the historical paired generating-polynomial implementation and prove that
its width parameter supports the distance marker required by V85. The output
must be either:

- a verified polynomial-time remote-point algorithm for bounded branchwidth;
- an explicit runtime or state-space obstruction;
- a counterexample to the proposed specialization.

Do not infer the integration only from the abstract recurrence.

## Priority two — constructive `Eval_H`

Exploit truth-table reuse across the candidate layers. Test splitters, perfect
hash families, small-bias spaces, and codes aligned with the support
hypergraph. A valid result must construct the missing list, not merely prove it
exists.

## Priority three — local-surjectivity certificates

Separate polynomially checkable reasons for a local map to be non-surjective:
Hall deficiency, affine syndromes, bounded-width exact enumeration, and other
algebraic certificates. Audit the complexity of recognizing surjectivity for
finite locality-three maps. No `Pi_2^P`-completeness claim is allowed without a
surjectivity-preserving bounded-locality gadget.

## Priority four — proof-complexity match

Compare the exact V80 obstruction generators with PRG-tautology lower-bound
hypotheses. Record failures of parameter matching as results. Expansion alone
is not sufficient for inheritance.

## Nonclaims

V86 remains below explicit rigidity, unrestricted circuit lower bounds, and
`P != NP` unless a separate fully verified theorem crosses those boundaries.
