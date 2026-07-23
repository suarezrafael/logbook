# V21 Validation and Publication Plan

## Theorem under review

For a symmetric fan-in-three Boolean circuit, complement output coordinates independently and partition the nonconstant normalized outputs into:

- monotone thresholds `T`;
- parity gates `P`;
- ternary exact-residue indicators `R`.

Let `d_T` be the number of variables used by `T`, let `r_2` be the GF(2) rank of the parity incidence matrix, and let `r_3` be the GF(3) rank of the exact-residue incidence matrix.

The proof candidate claims deterministic polynomial-time range avoidance when

```text
m > d_T + r_2 + r_3.
```

Uniform corollary: `m > 3n`.

## Internal V21 audit

The following components were rechecked independently:

1. coordinatewise output complementation preserves range avoidance;
2. the 30 symmetric truth tables of arity at most three fall into constants, normalized thresholds, parity, or exact-residue indicators;
3. the parity branch follows from a nonzero vector in the left nullspace over GF(2);
4. the exact-residue branch follows from a left-null dependency over GF(3), using either an inconsistent all-equations-true pattern or a one-violation dependency pattern;
5. the final inequality is a direct pigeonhole argument over the three effective dimensions;
6. the threshold branch is exactly the point where the published monotone `NC0_3-Avoid` theorem is invoked.

No internal flaw was found. This is not a substitute for expert review.

## Closest primary source

Neha Kuntewar and Jayalal Sarma, *Range Avoidance in Boolean Circuits via Turan-type Bounds*, ECCC TR25-034 / RANDOM 2025.

The ECCC v1 report states an `m>8n` result for the symmetric case. Later arXiv and conference versions omit that section. The V21 package asks the authors whether the omission reflects a known issue, revision of scope, or another reason.

## External review order

1. **Closest authors:** Neha Kuntewar and Jayalal Sarma.
2. **Independent complexity theorist:** a researcher in circuit complexity/range avoidance who is not an author of the source paper.
3. **Specialist screening:** ECCC submission after corrections from direct review.
4. **Preprint dissemination:** arXiv `cs.CC`, subject to registration, endorsement, and moderation.
5. **Archival software release:** dedicated GitHub repository plus Zenodo DOI after the mathematical package stabilizes.

## Publication channels

### ECCC

Best first formal channel for this result. ECCC accepts papers and short notes with a clear mathematical profile, complete proofs, readable presentation, and relevance to computational complexity. Submission is through an author account and a PDF upload. The report can later receive revisions or be marked withdrawn if necessary.

### arXiv

Recommended category: `cs.CC` (Computational Complexity). arXiv expects a topical, refereeable scientific contribution. New authors or new categories may require endorsement. TeX source is preferred, and submissions are moderated rather than peer reviewed.

### Zenodo

Zenodo is appropriate for archiving a stable software/data release and assigning a DOI. It should follow, not precede, stabilization of the theorem statement. The preferred route is a dedicated repository, a tagged GitHub release, `CITATION.cff`, and Zenodo GitHub integration.

## Release policy

The current pull request remains a draft. Do not mark it ready for review, merge it, create a permanent DOI, or submit to ECCC/arXiv until:

- the closest authors have had a reasonable opportunity to comment;
- the GF(3) lemma has been checked by an external reader;
- all references and version comparisons are accurate;
- the repository has a dedicated reproducibility entry point;
- the wording avoids claims of P versus NP resolution.
