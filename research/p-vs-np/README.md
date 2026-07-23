# P versus NP / Range-Avoidance Laboratory

## Scope

This directory indexes a long-running experimental and mathematical research program on:

- range avoidance for local Boolean circuits;
- proof-producing SAT and circuit refuters;
- finite obstruction classifications;
- constructive circuit lower-bound techniques;
- the methodological distance to P versus NP.

The project does **not** claim to resolve P versus NP.

## Scientific status vocabulary

| Label | Meaning |
|---|---|
| Reproduced | A published result was independently reimplemented or checked. |
| Finite computer-assisted result | Complete for an explicitly bounded universe, with a verifier. |
| Proof candidate | A human-readable argument exists but has not received external review. |
| Conjecture | Falsifiable statement under active investigation. |
| Counterexample | A preserved instance falsifying a stated hypothesis. |
| Confirmed theorem | Reserved for externally reviewed or formally checked results. |

## Active result

Laboratory V22 studies symmetric local range avoidance through zero-set polynomials. The current proof candidate states:

```text
For fixed fan-in k, let d=floor((k+1)/2).
SYMMETRIC-NC0_k-Avoid is deterministic polynomial time when
m > sum_{j=0}^d binom(n,j).
```

The general lemma applies whenever normalized outputs have the form `g_i(x)=1 iff p_i(x)=0` and the polynomial coefficient vectors are linearly dependent. For fan-in four the uniform corollary is:

```text
m > 1 + n + binom(n,2).
```

**Status:** internal level-4 candidate; not peer reviewed; novelty and priority not established.

The V20/V21 effective-dimension result for symmetric fan-in three remains a separate proof candidate:

```text
m > |V_T| + rank_GF2(A_P) + rank_GF3(A_R).
```

## Version map

| Version | Main contribution | Status |
|---|---|---|
| V16 | Minimum five-gate signed-MAJ3 obstruction classification | Finite computer-assisted result |
| V17 | Finite-locality barrier via high-girth hosts | Proof plus literature dependency |
| V18 | Six-state path relation algebra | Exact finite algebra |
| V19 | Multi-source parity finder and signed path algebra | Algorithmic optimization |
| V20 | Effective-dimension theorem candidate for symmetric `NC0_3-Avoid` | Proof candidate |
| V21 | External validation, publication preparation, and scientific repository organization | Validation stage |
| V22 | Zero-set polynomial dependency theorem candidate and quadratic symmetric fan-in-four corollary | Active proof candidate |

## Reproducibility standard

Every promoted result should include:

1. a precise theorem or falsifiable hypothesis;
2. executable code with deterministic seeds where relevant;
3. a second verifier that does not reuse the same critical implementation;
4. machine-readable results and SHA-256 hashes;
5. a limitations section;
6. a distinction between proof, experiment, reproduction, and conjecture;
7. a compact context file for the next laboratory version.

See [SCIENTIFIC_METHOD.md](SCIENTIFIC_METHOD.md) for the review protocol.

## Publication status

The current GitHub pull request is intentionally a draft. The intended sequence is:

1. external technical review;
2. correction or withdrawal of any flawed claim;
3. ECCC or arXiv preprint submission;
4. a dedicated repository release;
5. Zenodo archival and DOI assignment.

A DOI should not be minted for a theorem claim before the review package is stable.
