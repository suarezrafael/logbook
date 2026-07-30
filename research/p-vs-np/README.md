# NC0_k-Avoid Laboratory

> Historical path: `research/p-vs-np/`. The current research product is a structural study of range avoidance for local Boolean circuits. It is **not** presented as an active route to resolving P versus NP.

## Start here

- [STATE.md](STATE.md) — compact cumulative scientific state.
- [LEDGER.json](LEDGER.json) — machine-readable version, claim and reproducibility ledger.
- [SCIENTIFIC_METHOD.md](SCIENTIFIC_METHOD.md) — claim, verification and retraction policy.
- [`v61/`](v61/) — current reproducibility and prior-art audit.
- [`verify_all.sh`](verify_all.sh) — one-command verifier runner.

## Current position

Laboratory V61 converts the V60 strategic repositioning into manuscript discipline:

1. V22 is reclassified as a historical proof candidate whose original 125 serialized certificates are absent from the repository;
2. the cumulative runner reports V22 as `SKIP` with an explicit reason instead of executing an impossible command;
3. the main manuscript narrative is the positive/negative pair: affine fibers are algorithmically tractable, while the direct affine-style redundancy argument fails for bijunctive fibers;
4. the four-input V25 classification is moved to optional supplementary material;
5. prior-art claims are separated into known background, direct overlap, apparently specific contributions and unresolved novelty questions.

The project does **not** claim a deterministic algorithm for general `NC0_3-Avoid`, unrestricted circuit lower bounds, or a resolution of P versus NP.

## Contribution chain

| Version | Main contribution | Current status |
|---|---|---|
| V16 | Minimum signed-MAJ3 obstruction classification | Finite computer-assisted result |
| V17–V19 | Finite-locality barriers and path-relation tools | Preserved historical line |
| V20–V21 | Effective-dimension candidates and validation preparation | Historical proof candidates |
| V22 | Zero-set-polynomial dependency candidate | Proof candidate; original certificate dataset absent |
| V25 | Complete four-input NPN and zero-set-degree classification | Finite result; supplementary to current manuscript |
| V26–V27 | Literature alignment and affine-parity certificates for hard four-input classes | Internal proof candidates |
| V53 | Union-free substitution lemma; false girth implication retracted | Partially preserved, formally corrected |
| V54 | Degree-at-most-`k+1` separator for positive-stretch pure `AND_k` | Internally verified; monotone `k=3` must be compared with 2025 prior work |
| V55 | Fourteen ternary NPN classes and affine-fiber methods | Valid, strengthened by V56 |
| V56 | Consistency-or-redundancy algorithm for affine fibers at `m>n` | Internally verified; novelty unconfirmed |
| V57 | Orbit-`0x07` bijunctive irredundancy barrier and direct sums | Internally verified specific construction |
| V58 | Orientation depth and `m^{O(d)} poly(n+m)` algorithm | Internally verified parameterized result |
| V59 | Isoperimetric abundance and flat-potential barrier | Internally verified geometric/negative result |
| V60 | Easy-membership Las Vegas theorem and program consolidation | Internally verified scope result |
| V61 | Reproducibility repair, prior-art audit and manuscript refocus | Current laboratory |

Versions V23–V24 and V28–V52 are not represented by promoted package directories in this branch. Their absence must not be interpreted as missing theorems.

## Reproducibility

```bash
bash ./verify_all.sh
bash ./verify_all.sh --full
```

Each row reports `PASS`, `FAIL` or `SKIP`. `SKIP` must include a reason. A verifier that requires an absent historical artifact is not a pass and is not executed.

## Publication direction

The preferred paper is organized around:

- the affine-fiber positive algorithm;
- the bijunctive failure of the natural block-redundancy extension;
- orientation depth as the deterministic localization parameter;
- boundary abundance and explicit barriers to simple walking potentials;
- a precise separation between randomized avoidance and derandomization.

The V25 four-input classification is supplementary rather than part of the main theorem chain. External mathematical and prior-art review remains the next promotion gate. No external message is considered sent unless both the version package and `LEDGER.json` record it.
