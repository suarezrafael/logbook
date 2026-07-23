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

Laboratory V20/V21 studies symmetric fan-in-three range avoidance. The current proof candidate states that a circuit with threshold, parity, and exact-residue output families can be avoided in deterministic polynomial time when

```text
m > |V_T| + rank_GF2(A_P) + rank_GF3(A_R).
```

The uniform corollary is `m > 3n`. The argument depends on the published polynomial-time algorithm for monotone `NC0_3-Avoid` and uses explicit finite-field dependency certificates for the other two branches.

**Status:** internal level-4 candidate; not peer reviewed; novelty and priority not established.

## Version map

| Version | Main contribution | Status |
|---|---|---|
| V16 | Minimum five-gate signed-MAJ3 obstruction classification | Finite computer-assisted result |
| V17 | Finite-locality barrier via high-girth hosts | Proof plus literature dependency |
| V18 | Six-state path relation algebra | Exact finite algebra |
| V19 | Multi-source parity finder and signed path algebra | Algorithmic optimization |
| V20 | Effective-dimension theorem candidate for symmetric `NC0_3-Avoid` | Proof candidate |
| V21 | External validation, publication preparation, and scientific repository organization | Active |

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
