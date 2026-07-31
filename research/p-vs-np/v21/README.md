# Laboratory V21

## Purpose

V21 does not introduce another empirical heuristic. Its purpose is to convert the V20 theorem candidate into a package that can be independently reviewed, corrected, submitted, and archived.

## Deliverables

- [Validation and publication plan](VALIDATION_AND_PUBLICATION.md)
- [Mathematical review checklist](REVIEW_CHECKLIST.md)
- [Submission metadata draft](SUBMISSION_METADATA.md)
- LaTeX preprint source and rendered PDF in the release artifact
- independent verifier and V20 certificate corpus
- public tracking issue for review and publication tasks

## Current theorem candidate

```text
m > |V_T| + rank_GF2(A_P) + rank_GF3(A_R)
```

for range avoidance of symmetric Boolean output gates of fan-in at most three.

Uniform corollary:

```text
m > 3n
```

## Audit outcome

The V21 internal audit found no flaw in:

- coordinatewise normalization;
- the finite taxonomy;
- the GF(2) left-null certificate;
- the GF(3) equation-dependency certificate;
- the effective-dimension pigeonhole step.

This does not establish novelty or external correctness.

## External validation priority

1. Ask Neha Kuntewar and Jayalal Sarma, authors of the closest result.
2. Ask an independent circuit-complexity researcher to review the GF(3) lemma and overall reduction.
3. Revise or withdraw the claim in response to any flaw or prior-art reference.
4. Submit a stable mathematical note to ECCC.
5. Submit a preprint to arXiv `cs.CC` after endorsement/moderation requirements are satisfied.
6. Archive a stable dedicated-repository release through Zenodo.

## Scientific status

```text
internal: level-4 candidate
external conservative status: 3.5
peer reviewed: no
novelty established: no
P versus NP resolved: no
```
