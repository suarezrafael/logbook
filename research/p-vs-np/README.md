# NC0_k-Avoid Laboratory

> Historical path: `research/p-vs-np/`. The current research product is a structural study of range avoidance for local Boolean circuits. It is **not** presented as an active route to resolving P versus NP.

## Start here

- [STATE.md](STATE.md) — compact cumulative scientific state.
- [LEDGER.json](LEDGER.json) — machine-readable version, claim, reproducibility and outreach ledger.
- [SCIENTIFIC_METHOD.md](SCIENTIFIC_METHOD.md) — claim, verification and retraction policy.
- [`v62/`](v62/) — integrated manuscript and external-review package.
- [`verify_all.sh`](verify_all.sh) — one-command verifier runner.

## Current position

Laboratory V62 converts the audit into a manuscript and review workflow:

1. the V56/V57 affine-positive versus bijunctive-negative pair is the central narrative;
2. V57 is translated into standard clause-level IES and grouped-block terminology;
3. V54 is explicitly compared with Kuntewar–Sarma's monotone `NC0_3-Avoid` theorem;
4. every manuscript claim is mapped to primary literature or a reproducible internal package;
5. exact prior art for V56 and orientation depth remains unresolved rather than presumed absent;
6. two external prior-art requests have been sent and are awaiting replies;
7. future laboratories use one coherent commit per version.

The project does **not** claim a deterministic algorithm for general `NC0_3-Avoid`, unrestricted circuit lower bounds, or a resolution of P versus NP.

## Contribution chain

| Version | Main contribution | Current status |
|---|---|---|
| V16 | Minimum signed-MAJ3 obstruction classification | Finite computer-assisted result |
| V17–V19 | Finite-locality barriers and path-relation tools | Preserved historical line |
| V20–V21 | Effective-dimension candidates and validation preparation | Historical proof candidates |
| V22 | Zero-set-polynomial dependency candidate | Proof candidate; original certificate dataset absent |
| V25 | Complete four-input NPN and zero-set-degree classification | Finite result; supplementary |
| V26–V27 | Affine-parity and related four-input certificates | Internal candidates; supplementary |
| V53 | Union-free lemma; false girth implication retracted | Partially preserved and corrected |
| V54 | Degree-at-most-`k+1` pure-`AND_k` separator | Verified; direct monotone-ternary overlap recorded |
| V55 | Fourteen ternary NPN classes and affine methods | Valid, strengthened by V56 |
| V56 | Affine consistency-or-redundancy at `m>n` | Verified; novelty unconfirmed |
| V57 | Orbit-`0x07` block-irredundancy and direct sums | Verified specific construction |
| V58 | Orientation depth and FPT avoidance | Verified parameterized result |
| V59 | Isoperimetry and flat-potential barrier | Verified geometric/negative result |
| V60 | Easy-membership Las Vegas theorem | Verified scope result, not novelty |
| V61 | V22 repair and prior-art audit | Verified audit |
| V62 | Integrated manuscript, source matrix and external outreach | Current laboratory |

## Reproducibility

```bash
bash ./verify_all.sh
bash ./verify_all.sh --full
```

Each row reports `PASS`, `FAIL` or `SKIP`. A `SKIP` must state a reason. The V22 verifier is skipped because its required original dataset is absent.

GitHub Actions runs both quick and full modes for changes under `research/p-vs-np/`.

## Publication direction

The paper is organized around:

- affine-fiber consistency or redundancy;
- failure of the natural bijunctive block analogue;
- orbit-constrained finite and infinite counterexamples;
- orientation depth and boundary localization;
- geometric abundance versus algorithmic barriers;
- separation of randomized avoidance from deterministic derandomization.

External responses are pending. No response, silence or negative search is treated as confirmation of novelty.
