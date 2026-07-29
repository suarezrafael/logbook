# V53 primary-source field survey

## Range Avoidance hierarchy

### `NC⁰₂`

Guruswami, Lyu, and Wang give a polynomial-time algorithm. Their work also relates small-locality Avoid to explicit constructions and circuit lower bounds.

### `NC⁰₃`

Gajulapalli, Golovnev, Nagargoje, and Saraogi identify stretch-one `NC⁰₃-Avoid` as open. They show that an efficient algorithm with an NP oracle at stretch `m=n+n^{2/3}` would yield rigid matrices and super-linear log-depth circuit lower bounds. They also give polynomial algorithms at much larger stretch.

### Monotone `NC⁰₃`

Kuntewar and Sarma solve monotone `NC⁰₃-Avoid` for `m>n` using Turán-type bounds. This is essential context for V53: the `AND₃` construction is not a hard Avoid family, despite its high syndrome degree.

### `NC⁰₄`

Prior reductions connect efficient `NC⁰₄-Avoid` algorithms to rigid matrices, optimal codes, Ramsey graphs, and other explicit objects. This made V52's original `NC⁰₄` target less attractive for isolating new algorithmic territory.

## Cryptographic barriers

Ilango, Li, and Williams connect deterministic Avoid algorithms with indistinguishability obfuscation and bounded arithmetic. Later work extends hardness evidence to nondeterministic algorithms and constant-depth representations under plausible cryptographic assumptions.

These results advise caution but do not directly settle `NC⁰₃-Avoid`.

## Algorithms to lower bounds

Ryan Williams' ACC lower-bound program exemplifies the modern principle:

```text
nontrivial circuit-analysis algorithm
                -> circuit lower bound.
```

Recent Range-Avoidance results follow a related path. Ren and Williams use Range Avoidance, PCP, and iterative win-win arguments to obtain near-maximum lower bounds for an exponential-time Merlin–Arthur class.

V53 therefore prioritizes precise subproblem algorithms and barriers over direct claims about P versus NP.

## Razborov–Smolensky and low-degree algebra

Razborov and Smolensky use low-degree polynomial approximations to prove lower bounds against bounded-depth circuits with modular gates. The V53 syndrome program is algebraic but different:

- their method approximates circuit functions;
- V53 searches for exact polynomials vanishing on a circuit image.

The V53 high-girth construction shows that exact constant-degree vanishing identities cannot be universal even for `AND₃` images.

## Natural Proofs and algebraic natural proofs

Razborov and Rudich show that large, constructive circuit properties face a pseudorandomness barrier. Algebraic variants relate efficient algebraic properties to PIT and succinct hitting sets.

V53 does not define a large property separating hard truth tables. Still, any future attempt to turn syndrome detection into a broad lower-bound property must be audited against these barriers.

## Geometric Complexity Theory

Mulmuley and Sohoni's GCT program attacks permanent-versus-determinant and related lower bounds using algebraic geometry and representation theory. Grochow's work shows that many known lower-bound methods fit a GCT framework.

The immediate V53 object is a finite Boolean image and its low-degree vanishing ideal. This has geometric language, but no direct GCT obstruction is obtained. GCT remains background rather than the next operational step.

## Union-free hypergraphs

Union-free set systems are established combinatorial objects. The V53 theorem uses a strong bounded-size union-distinctness condition. High incidence girth supplies it through a short-cycle argument.

The exact transfer to minimum Range-Avoidance syndrome degree may already exist under terminology from union-free or union-distinct hypergraphs, uniquely decipherable set systems, Hilbert functions of Boolean images, finite-degree Zariski closure, or evaluation codes. No novelty claim should be made until specialists check this terminology.

## Sources

1. Gajulapalli, Golovnev, Nagargoje, Saraogi, *Range Avoidance for Constant-Depth Circuits: Hardness and Algorithms*, ECCC TR23-021 / APPROX-RANDOM 2023.
2. Kuntewar, Sarma, *Avoiding Range via Turan-Type Bounds*, APPROX-RANDOM 2025.
3. Ilango, Li, Williams, *Indistinguishability Obfuscation, Range Avoidance, and Bounded Arithmetic*, ECCC TR23-038 / STOC 2023.
4. Linial, Simkin, *A Randomized Construction of High Girth Regular Graphs*, RSA 2021 / arXiv:1911.09640.
5. Razborov, Rudich, *Natural Proofs*, JCSS 1997 / ECCC TR94-010.
6. Mulmuley, Sohoni, *Geometric Complexity Theory I*, SIAM J. Computing.
7. Ren, Williams, *Near-Maximum Circuit Lower Bounds for Exponential Time with Merlin-Arthur Queries*, ECCC TR26-118.
