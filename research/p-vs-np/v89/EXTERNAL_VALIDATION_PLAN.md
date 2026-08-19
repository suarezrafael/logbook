# V91 external validation plan

Internal verifiers test consistency with the formalized claim. They do not test
novelty, omitted prior art, hidden convention mismatches, or a shared error in
the statement and verifier.

V91 therefore creates a permanent external-validation queue.

## 1. Packet A — V81 deficiency conservation

### Candidate material

- `v81/DEFICIENCY_CONSERVATION_AND_MIN_UNION.md`
- `v81/V81_DEFICIENCY_CONSERVATION_THEOREM.tex`
- `v81/deficiency_conservation.py`
- `v81/verify.py`

### Validation questions

1. Is the conservation identity already standard under another name in
   transversal matroids, Hall-deficiency theory, submodular optimization, or
   hypergraph matching?
2. Are the minimum-union consequences stated with the weakest necessary
   hypotheses?
3. Does the proof hide an assumption about repeated supports, empty sets, or
   the encoding of active outputs?
4. Is the theorem useful outside the laboratory's `NC0_3-Avoid` formulation?
5. Can the statement be shortened to one lemma and one corollary suitable for a
   note?

### Required packet

```text
Title page
Abstract of at most 150 words
Definitions and conventions
One main theorem
Proof
Two boundary examples
Prior-art comparison
Executable supplement
Nonclaims
```

### Initial venue strategy

First obtain one informal expert reading from a researcher in combinatorics,
matroid theory, or complexity. Only after the novelty audit should the note be
posted publicly or submitted to a workshop.

## 2. Packet B — V87 rank-three transfer

### Candidate material

- `v87/LINEAR_BRANCHWIDTH_THEOREM.md`
- `v87/linear_branchwidth.py`
- `v87/RESULTS.json`
- `v87/verify.py`
- `v87/verify_independent.py`

### Candidate statement

For every rank-at-most-three hypergraph `H`, the laboratory claims

```text
tw(primal(H)) + 1 <= max(3, ceil(3 bw(H)/2)).
```

The external packet must state the exact definition of hypergraph branchwidth
and compare it with all standard branchwidth, carving-width, incidence-graph,
and primal-graph conventions.

### Validation questions

1. Is this inequality already known in hypergraph width theory?
2. Does the `3k/2` bag-counting argument cover leaf, empty-edge, repeated-edge,
   and disconnected cases?
3. Does the conversion satisfy the running-intersection property for every
   vertex?
4. Is the constant `3/2` new, optimal, or merely a direct consequence of a
   stronger standard theorem?
5. Is the random-pair-shadow application using exactly the same width
   definition as the transfer lemma?

### Required packet

```text
Definition crosswalk
Theorem and proof
Diagram of the three-branch bag construction
Boundary cases
Comparison with known primal/incidence width inequalities
Independent finite audit
Nonclaims
```

### Initial venue strategy

Seek feedback from a researcher working on graph minors, hypergraph width, or
parameterized algorithms before asserting novelty. A workshop submission is
appropriate only if the prior-art search leaves a genuine contribution.

## 3. Meaning of external validation

The following count as external validation events:

- a written technical response from an identified researcher;
- an open-review thread with substantive mathematical comments;
- a workshop or conference referee report;
- a journal referee report;
- a public note that receives a documented correction or confirmation.

The following do not count by themselves:

- passing another internal verifier;
- having a second agent rewrite the proof;
- posting to arXiv without feedback;
- repository stars, views, or automated review;
- lack of reported objections.

ArXiv establishes a public timestamp and discoverability; it does not establish
peer review or novelty.

## 4. Feedback ledger

For every packet maintain:

| Date | Reviewer/source | Question | Severity | Resolution | Claim changed? |
|---|---|---|---|---|---:|
| | | | | | |

Severity values:

- `fatal`: theorem false or unsupported;
- `major`: proof gap, definition mismatch, or known stronger prior art;
- `minor`: exposition, notation, missing boundary case;
- `confirmation`: no issue found within the review scope.

A known-prior-art finding is not a failed laboratory. It changes the output
classification from possible contribution to exposition or infrastructure.

## 5. Submission gate

No packet is submitted until:

1. every definition is source-aligned;
2. the proof has an independent reconstruction;
3. a systematic literature search is recorded;
4. the novelty claim is phrased conditionally;
5. executable evidence is separated from proof;
6. the abstract contains no P-versus-NP proximity language;
7. all stronger nonclaims are explicit.

## 6. Permanent cadence

At least one external-validation packet must be active whenever two consecutive
laboratories have been completed without external feedback. Opening a third
internal laboratory does not replace this obligation.

## 7. Success criterion

The front succeeds when feedback changes confidence or direction. Acceptance is
not required. A correction, prior-art match, narrowed theorem, or rejection with
technical reasons is valuable because it breaks the closed-loop validation
problem of an agent-generated research program.
