# Effective-Dimension Range Avoidance for Symmetric NC0_3 Circuits

**Computer-assisted research note — Laboratory V20**

**Author:** Rafael Vieira Suarez  
**Status:** Not peer reviewed. Novelty and priority are not established.

## Abstract

We give a candidate deterministic polynomial-time range-avoidance algorithm for symmetric Boolean output gates of fan-in at most three. Coordinatewise output complementation normalizes every nonconstant symmetric gate into one of three families: monotone thresholds, parity gates, or ternary exact-residue indicators modulo three.

Let `d_T` be the number of variables used by threshold outputs, let `r_2` be the GF(2) rank of the parity incidence matrix, and let `r_3` be the GF(3) rank of the exact-residue incidence matrix. The candidate theorem gives range avoidance under

```text
m > d_T + r_2 + r_3.
```

This yields the uniform sufficient condition `m > 3n`. The threshold branch uses the published polynomial algorithm for monotone NC0_3-Avoid. The parity branch uses a left-null separating vector. The exact-residue branch uses a GF(3) dependency to produce either an inconsistent all-equations-true output or an output with exactly one impossible violated equation in a dependency support.

A separate implementation classifies all 30 symmetric truth tables of arities zero through three and verifies 342 generated certificates by exact range enumeration.

## Version context

The first ECCC version of the Turan-type range-avoidance paper states an `m > 8n` result for symmetric NC0_3 circuits. The later arXiv version and the peer-reviewed conference paper omit the symmetric section. We do not infer the reason for this version difference.

## Validation

- 30/30 symmetric truth tables classified;
- 234 mixed/generated benchmark circuits;
- 108 homogeneous branch circuits;
- 342/342 missing outputs confirmed by exhaustive enumeration;
- both GF(3) certificate modes exercised;
- independent verifier accepted every claim.

## Limitations

The result is not peer reviewed. Prior art has not been exhausted. The mathematical polynomial-time claim relies on the published monotone theorem. This work does not resolve P versus NP and does not establish an unrestricted circuit lower bound.
