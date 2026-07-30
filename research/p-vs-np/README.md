# NC0_k-Avoid Laboratory

> Historical path: `research/p-vs-np/`. The current research product is a structural study of range avoidance for local Boolean circuits. It is **not** presented as an active route to resolving P versus NP.

## Start here

- [STATE.md](STATE.md) — compact cumulative scientific state.
- [LEDGER.json](LEDGER.json) — machine-readable version and claim ledger.
- [SCIENTIFIC_METHOD.md](SCIENTIFIC_METHOD.md) — claim, verification and retraction policy.
- [`v60/`](v60/) — current laboratory and program repositioning.
- [`verify_all.sh`](verify_all.sh) — one-command verifier runner.

## Current position

Laboratory V60 consolidates the results through V59 and makes the strategic boundary explicit:

1. the repository contains a coherent body of results about `NC0_k-Avoid`;
2. the current bijunctive stretch-one regime has polynomial-time image membership;
3. for `m>n`, uniform output sampling finds a missing word with success probability at least `1-2^(n-m)` per trial;
4. therefore this regime is randomized-easy, while deterministic localization remains a narrower derandomization question;
5. exact classification at `n=9` is retained for falsification and regression, not as the main scientific priority.

The project does **not** claim a deterministic algorithm for general `NC0_3-Avoid`, unrestricted circuit lower bounds, or a resolution of P versus NP.

## Stable contribution chain

| Version | Main contribution | Current status |
|---|---|---|
| V16 | Minimum signed-MAJ3 obstruction classification | Finite computer-assisted result |
| V17–V19 | Finite-locality barriers and path-relation tools | Preserved historical line |
| V20–V22 | Effective-dimension and zero-set-polynomial proof candidates | Internal, not externally reviewed |
| V25 | Complete four-input NPN and zero-set-degree classification | Finite computer-assisted result |
| V26–V27 | Literature alignment and affine-parity certificates for hard four-input classes | Internal proof candidates |
| V53 | Union-free substitution lemma; false girth implication retracted | Partially preserved, formally corrected |
| V54 | Degree-at-most-`k+1` separator for positive-stretch pure `AND_k` | Internally verified theorem package |
| V55 | Fourteen ternary NPN classes and affine-fiber methods | Valid, strengthened by V56 |
| V56 | Consistency-or-redundancy algorithm for affine fibers at `m>n` | Internally verified theorem package |
| V57 | Bijunctive irredundancy counterexample and infinite direct-sum family | Internally verified barrier |
| V58 | Orientation depth and `m^{O(d)} poly(n+m)` algorithm | Internally verified parameterized result |
| V59 | Isoperimetric abundance, randomized localization bound and flat-potential barrier | Internally verified geometric/negative result |
| V60 | Program consolidation, easy-membership randomized theorem and stable repository ledger | Current laboratory |

Versions V23–V24 and V28–V52 are not represented by promoted package directories in this branch. Their absence must not be interpreted as missing theorems.

## Reproducibility

From this directory:

```bash
bash ./verify_all.sh
```

The default run executes curated primary and independent checks while avoiding intentionally expensive exact searches. To include exact verifiers where available:

```bash
bash ./verify_all.sh --full
```

Each row reports `PASS`, `FAIL`, or `SKIP`; missing historical scripts are reported rather than silently ignored.

## Scientific status vocabulary

| Label | Meaning |
|---|---|
| Reproduced | A published result was independently reimplemented or checked. |
| Finite computer-assisted result | Complete for an explicitly bounded universe, with a verifier. |
| Internally verified theorem package | Human-readable proof plus executable checks; not peer reviewed. |
| Proof candidate | A human-readable argument exists but external review is pending. |
| Conjecture | Falsifiable statement under active investigation. |
| Counterexample | A preserved instance falsifying a stated hypothesis. |
| Retracted | The claim is false and retained only as part of the correction record. |
| Confirmed theorem | Reserved for externally reviewed or formally checked results. |

## Publication direction

The preferred product is a paper on local-circuit range avoidance covering:

- NPN classification and affine-fiber algorithms;
- the bijunctive block-redundancy barrier;
- orientation depth and its FPT algorithm;
- isoperimetric abundance versus deterministic localization;
- reproducible finite searches and explicit methodological limitations.

External mathematical review remains the next promotion gate. Contact drafts may exist in version packages, but no message is considered sent unless `EXTERNAL_CONTACT_STATUS` and the cumulative ledger record it explicitly.
