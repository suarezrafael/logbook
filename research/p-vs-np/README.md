# NC0_k-Avoid Laboratory

> Historical path: `research/p-vs-np/`. The current research product is a structural and algorithmic study of range avoidance for local Boolean circuits. It is **not** an active route to resolving P versus NP.

## Start here

- [STATE.md](STATE.md) — cumulative scientific state.
- [LEDGER.json](LEDGER.json) — machine-readable claims, reproducibility, outreach and promotion ledger.
- [SCIENTIFIC_METHOD.md](SCIENTIFIC_METHOD.md) — claim, verification and retraction policy.
- [`v63/`](v63/) — CI promotion record, reviewer packet and reproducible manuscript appendices.
- [`verify_all.sh`](verify_all.sh) — cumulative verifier runner.

## Current position

Laboratory V63 converts the V62 draft package into a continuously promotable research record:

1. the complete quick and full runners passed in a clean GitHub Actions checkout;
2. the historical V60 verifier was repaired so that past outreach state is checked in its versioned file rather than frozen in the current ledger;
3. the central V56, V57 and V58 results now have reviewer-facing appendices with explicit assumptions, algorithms, witnesses and nonclaims;
4. the two external prior-art requests were checked again and still have no replies;
5. silence is recorded only as `pending`, never as novelty evidence;
6. repository governance is now one laboratory per branch and pull request, followed by CI and merge into `main`;
7. laboratory pull requests are not left in draft after the package is complete.

The project does **not** claim a deterministic polynomial-time algorithm for general `NC0_3-Avoid`, unrestricted circuit lower bounds, or a resolution of P versus NP.

## Contribution chain

| Version | Main contribution | Current status |
|---|---|---|
| V16 | Minimum signed-MAJ3 obstruction classification | Finite computer-assisted result |
| V17–V19 | Finite-locality barriers and path-relation tools | Preserved historical line |
| V20–V22 | Effective-dimension and zero-set dependency candidates | Historical proof candidates; V22 artifact missing |
| V25 | Complete four-input NPN and zero-set-degree classification | Finite result; supplementary |
| V26–V27 | Affine-parity and related four-input certificates | Internal candidates; supplementary |
| V53 | Union-free lemma; false girth implication retracted | Partially preserved and corrected |
| V54 | Degree-at-most-`k+1` pure-`AND_k` separator | Verified; monotone ternary overlap recorded |
| V55 | Fourteen ternary NPN classes and affine methods | Valid, strengthened by V56 |
| V56 | Affine consistency-or-redundancy at `m>n` | Verified; novelty unconfirmed |
| V57 | Orbit-`0x07` block-irredundancy and direct sums | Verified specific construction |
| V58 | Orientation depth and FPT avoidance | Verified parameterized result |
| V59 | Isoperimetry and flat-potential barrier | Verified geometric/negative result |
| V60 | Easy-membership Las Vegas theorem | Verified scope result, not novelty |
| V61 | V22 repair and prior-art audit | Verified audit |
| V62 | Integrated manuscript, source matrix and external outreach | Verified editorial package |
| V63 | Clean-CI promotion, reviewer packet and reproducible appendices | Current laboratory |

## Reproducibility

```bash
bash ./verify_all.sh
bash ./verify_all.sh --full
```

Every row reports `PASS`, `FAIL` or `SKIP`. The V22 row remains a justified `SKIP` because the original serialized certificate dataset is absent. Missing historical scripts are also explicit skips rather than false passes.

## Promotion workflow

Each new laboratory follows:

```text
main -> laboratory branch -> non-draft PR -> quick/full CI -> squash merge to main
```

The laboratory package and its verifiers are merged only after both CI jobs pass. External responses may revise later laboratories but do not block routine promotion when the current claims and nonclaims are internally consistent.
