# V53 primary-source field survey — corrected by V54

## Range Avoidance hierarchy

### `NC⁰₂`

Guruswami, Lyu, and Wang give a polynomial-time algorithm. Their work also connects small-locality Avoid to explicit constructions and circuit lower bounds.

### `NC⁰₃`

Gajulapalli, Golovnev, Nagargoje, and Saraogi identify stretch-one `NC⁰₃-Avoid` as open. They show that an efficient algorithm with an NP oracle at stretch `m=n+n^{2/3}` would yield rigid matrices and super-linear log-depth circuit lower bounds. They also give algorithms at larger stretch.

### Monotone `NC⁰₃`

Kuntewar and Sarma solve monotone `NC⁰₃-Avoid` for `m>n` using Turán-type structure. This remains essential context: pure `AND₃` is not a hard Avoid subclass.

### `NC⁰₄`

Prior reductions connect efficient `NC⁰₄-Avoid` algorithms to rigid matrices, optimal codes, Ramsey graphs, and other explicit objects. This supports keeping `NC⁰₃` as the active open target.

## Cryptographic barriers

Ilango, Li, and Williams connect deterministic Avoid algorithms with indistinguishability obfuscation and bounded arithmetic. These results advise caution but do not directly settle stretch-one `NC⁰₃-Avoid`.

## Algorithms to lower bounds

Ryan Williams' ACC lower-bound program exemplifies the principle:

```text
nontrivial circuit-analysis algorithm
                -> circuit lower bound.
```

Recent Range-Avoidance work follows related win-win and derandomization patterns. V53/V54 therefore prioritize precise restricted algorithms and barriers rather than direct P-versus-NP claims.

## Low-degree algebra

Razborov–Smolensky use low-degree polynomial approximations to prove lower bounds for bounded-depth circuits. The laboratory instead studies exact polynomials vanishing on circuit images.

The valid V53 observation is only:

```text
bounded-size union-distinctness
        -> injective monomial substitution
        -> no low-degree vanishing identity.
```

The original claim that high incidence girth supplies full bounded-size union-distinctness was false and is retracted.

## Union-free versus cover-free structure

Union-free set systems are established objects, but full union-freeness has two qualitatively different failure modes:

1. crossing collisions, where both edge families contain private edges;
2. nested collisions, where one family contains the other and an edge is covered by the union of other edges.

Incidence girth can control some crossing collisions, but it does not prevent nested coverage. The relevant additional language is cover-free families, superimposed codes, and group testing.

For positive-excess `k`-uniform hypergraphs, V54 gives an opposite structural ceiling: a nonempty 2-core supplies an edge covered by at most `k` witnesses and therefore a separator of degree at most `k+1` for pure `AND_k`.

## Natural Proofs and GCT

Natural Proofs, algebraic natural-proof barriers, and Geometric Complexity Theory remain background constraints. No GCT obstruction or natural property is produced by V53 or V54.

## Scientific status

- The union-free substitution lemma is preserved.
- The girth implication and `Ω(log n)` family are retracted.
- The finite UF2 and UF3 computations remain valid.
- The V54 2-core separator may be folklore or subsumed by monotone Avoid literature; novelty is not claimed.

## Sources

1. Gajulapalli, Golovnev, Nagargoje, Saraogi, *Range Avoidance for Constant-Depth Circuits: Hardness and Algorithms*, ECCC TR23-021 / APPROX-RANDOM 2023.
2. Kuntewar, Sarma, *Avoiding Range via Turan-Type Bounds*, APPROX-RANDOM 2025.
3. Ilango, Li, Williams, *Indistinguishability Obfuscation, Range Avoidance, and Bounded Arithmetic*, ECCC TR23-038 / STOC 2023.
4. Razborov, Rudich, *Natural Proofs*, JCSS 1997 / ECCC TR94-010.
5. Mulmuley, Sohoni, *Geometric Complexity Theory I*, SIAM Journal on Computing.
6. Ren, Williams, *Near-Maximum Circuit Lower Bounds for Exponential Time with Merlin-Arthur Queries*, ECCC TR26-118.
