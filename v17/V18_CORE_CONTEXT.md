# V18 Core Context

## Goal

Advance toward P versus NP through rigorous circuit lower bounds, constructive refuters, proof complexity, and range avoidance. Never treat finite benchmarks as a proof of P=NP or P≠NP.

## Strongest accumulated results

- V6 reproduced the deterministic CDCL Ordering Principle separation.
- V15 classified minimum one-live MAJ3 motifs: four gates, three classes.
- V16 classified minimum unsatisfiable signed-MAJ3 motifs: five gates, 792 witnesses, three classes up to complement.
- V17 proves a locality barrier for the motif strategy.

## V17 barrier

Every unsatisfiable signed-MAJ3 motif has a cyclic underlying hypergraph, because every acyclic connected linear motif is satisfiable greedily.

For any finite family of constant-size unsatisfiable motifs, choose a 3-uniform linear hypergraph of larger Berge girth with vertex degree 4. Then edge size is 3, `m/n=4/3>1`, and none of the finite motifs occurs.

Machine witness:

- vertices: 450
- hyperedges: 600
- incidence girth: 10
- cycle rank: 751
- V16 maximum motif incidence girth: 8
- avoids all V16 supports: true

## Consequence

Stop expanding fixed-size motif catalogues as the main strategy. Variable-size or global certificates are necessary. This is consistent with loose chi-cycle methods in the published monotone NC0_3-Avoid algorithm.

## V18 primary experiment

Build a signed-cycle automaton:

1. Generate high-girth linear MAJ3 instances.
2. Extract Berge cycles and overlapping cycle chains of growing length.
3. Synthesize output signs that create implication paths `x→¬x` and `¬x→x`.
4. Learn a finite-state transition system, then derive it symbolically.
5. Test whether the automaton finds a certificate in every `m>n` benchmark.
6. Search automatically for the smallest counterexample.
7. Prove polynomial runtime only after an invariant is established.

## V18 parallel experiment

Complete the constructive DeMorgan XOR refuter without semantic fallback.

## Required evidence protocol

- Explicit falsifiable hypothesis.
- Independent verifier.
- Adversarial counterexample search.
- Machine-verifiable certificate.
- Separate reproduced theorem, new conjecture, and new proof.
- Preserve seeds and SHA-256 hashes.

Do not reload the full V2–V16 narrative unless a specific artifact is needed.
