# Submission Metadata Draft

## Title

Effective-Dimension Range Avoidance for Symmetric NC0_3 Circuits

## Author

Rafael Vieira Suarez

## Status line

Research note; not peer reviewed; novelty and priority are not established.

## Abstract

We give a candidate deterministic polynomial-time range-avoidance algorithm for circuits whose output coordinates are symmetric Boolean functions of at most three input variables. After independently complementing output coordinates, every nonconstant gate belongs to one of three normalized families: monotone thresholds, parity gates, or ternary exact-residue indicators modulo three. Let `d_T` be the number of input variables used by the threshold coordinates, let `r_2` be the GF(2) rank of the parity incidence matrix, and let `r_3` be the GF(3) rank of the exact-residue incidence matrix. We prove range avoidance under `m>d_T+r_2+r_3`, which implies the uniform sufficient condition `m>3n`. The threshold branch uses the published polynomial-time algorithm for monotone `NC0_3-Avoid`; the parity and exact-residue branches use explicit left-nullspace certificates. A separate implementation classifies all 30 symmetric truth tables of arity at most three and verifies 342 generated certificates by exact range enumeration. The result is released as a proof candidate for external review.

## Suggested classifications

- arXiv primary category: `cs.CC` - Computational Complexity
- Possible cross-list after expert advice: `math.CO` - Combinatorics
- ECCC keywords: circuit complexity, range avoidance, symmetric Boolean functions, finite-field rank, local circuits

## Primary references

1. Neha Kuntewar and Jayalal Sarma, *Range Avoidance in Boolean Circuits via Turan-type Bounds*, ECCC TR25-034 / RANDOM 2025.
2. Karthik Gajulapalli, Alexander Golovnev, Satyajeet Nagargoje, and Sidhant Saraogi, *Range Avoidance for Constant-Depth Circuits: Hardness and Algorithms*, ECCC TR23-021.

## Required files before submission

- [ ] LaTeX source that compiles without local paths
- [ ] PDF with theorem, complete proof, limitations, and references
- [ ] source archive for arXiv
- [ ] independent verification script
- [ ] machine-readable certificate summary
- [ ] `CITATION.cff`
- [ ] license statement
- [ ] exact repository commit hash
- [ ] disclosure that automated tools assisted experimentation and drafting, if required by the target venue

## Do not submit yet

Submission is blocked pending direct author contact and at least one independent technical review of the GF(3) lemma and taxonomy.
