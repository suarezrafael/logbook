# P versus NP Lab V16

Computer-assisted classification of minimal unsatisfiable signed-majority motifs in connected linear 3-uniform hypergraphs.

## Main result

- no unsatisfiable output labeling with at most four `MAJ3` gates;
- 792 unsatisfiable labelings with five gates;
- six signed isomorphism classes;
- three classes up to global complementation;
- every witness is minimally unsatisfiable;
- every witness has exactly three one-live-plus-cap decompositions.

## Scientific status

Open computational research note. Not peer reviewed. Novelty is not established. This work does **not** resolve P versus NP and does not prove a new asymptotic circuit lower bound.

## Reproduction

```bash
python verify.py
```

The script independently regenerates every connected linear 3-uniform hypergraph with at most five edges, tests every signed majority labeling through 2-SAT, checks every witness by exhaustive evaluation, and confirms the class counts.

## Files

- `PREPRINT.md` — research note and limitations;
- `verify.py` — standalone independent enumerator and verifier;
- `RESULTS.json` — certified counts and representatives;
- `CITATION.cff` — citation metadata.
