# Prior-art search log — V62

## Method

The search used primary papers, official proceedings, official author pages, arXiv and ECCC records. A failed keyword search is recorded only as “not located in this pass”; it is not evidence of novelty and is never treated as proof of novelty.

## 1. Grouped affine fibers

### Target statement

Given affine fibers `F_i={x:A_i x=b_i}` over `GF(2)`, if the selected systems are jointly consistent, translate by a common solution and write `W_i=rowspace(A_i)`. For `m>n`, some complete block satisfies

```text
W_i <= sum_{j != i} W_j.
```

This yields a missing output by activating a spanning collection of other blocks and deactivating block `i`.

### Queries

- affine CSP redundant grouped constraints;
- irredundant family of subspaces contained in the sum of the others;
- grouped linear equations redundancy matroid;
- affine relation clone Range Avoidance;
- coding-theoretic syndrome avoidance grouped parity checks.

### Nearby material located

- classical linear algebra on sums and dimensions of subspaces;
- affine CSPs represented by systems of linear equations;
- general CSP non-redundancy frameworks;
- linear and affine special cases of Range Avoidance.

### Result

No source was located that states the exact gate-block theorem and missing-output construction in the V56 form. The core dimension lemma is elementary and likely standard. Novelty remains unconfirmed.

## 2. Orientation depth

### Target definition

For `S=Range(C)` and `b in S`,

```text
rho_S(b) = min_{y in internal_boundary(S)} d_H(b,y).
```

For bijunctive fibers, enumerating orientations up to distance `d` yields an `m^{O(d)} poly(n+m)` algorithm whenever `rho_S(b)<=d`.

### Queries

- distance to boundary of a SAT/CSP solution space;
- Hamming boundary depth Boolean relation;
- 2-SAT solution graph boundary;
- nearest non-solution / nearest boundary in CSP reconfiguration;
- frozen variables and local-flip geometry;
- parameterized SAT boundary distance.

### Nearby material located

- Gopalan, Kolaitis, Maneva and Papadimitriou study connectivity, component diameter and induced hypercube subgraphs of Boolean solution spaces;
- later reconfiguration work studies reachability in solution graphs;
- random-CSP literature studies frozen variables and clusters;
- these notions concern input-assignment solution spaces, while V58 measures distance inside the **output image** to a missing-neighbor boundary.

### Result

No exact equivalent parameter or the same Range-Avoidance FPT use was located. The repository uses the phrase “we formulate orientation depth in this setting,” not “we introduce a new parameter.”

## 3. 2-CNF grouped irredundancy

Liberatore's CNF and 2-CNF work establishes redundancy and IES terminology. The V57 gadget becomes a clause-irredundant formula after duplicate unit clauses are collapsed. The remaining question is whether partitioned or grouped-clause irredundancy has established terminology directly matching gate blocks.

A focused question was sent to Paolo Liberatore.

## 4. V54 monotone overlap

Kuntewar–Sarma 2025 proves deterministic `MONOTONE-NC0_3-Avoid` for `m>n`. This directly overlaps the algorithmic conclusion of V54 for pure `AND3`. No priority claim is allowed. The unresolved issue is whether V54's degree-four forcing-core separator is explicit or implicit in their framework.

## 5. External-contact sources

Institutional or official pages were used to verify current professional addresses for the contacted researchers. The repository records names and purpose, not private mailbox metadata.

## Promotion rule

A later response may:

- confirm known terminology;
- identify direct prior art;
- suggest a narrower claim;
- find an error.

It may not be treated as peer review unless the respondent actually reviews the relevant proof or computation.
