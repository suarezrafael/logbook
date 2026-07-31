# NC0_k-Avoid Laboratory V60

## Consolidation, regime separation and manuscript transition

**Scientific status:** internally verified consolidation package. The mathematical theorem in this version is elementary; its role is strategic rather than novel. The package is not peer reviewed, novelty is not established, and it does not resolve deterministic `NC0_3-Avoid`, unrestricted circuit lower bounds, or P versus NP.

## Main result

Let

```text
C : {0,1}^n -> {0,1}^m,  m>n,
```

and suppose membership in `Range(C)` is decidable in polynomial time. Sample `y` uniformly from `{0,1}^m` and return it when the membership test says `y` is outside the range.

Because `|Range(C)| <= 2^n`, every trial succeeds with probability at least

```text
1 - 2^(n-m).
```

The expected number of trials is at most

```text
1 / (1 - 2^(n-m)) <= 2.
```

For `m=n+1`, equality in the two-trial bound is possible when `C` is injective.

## Strategic consequence

For the stretch-one bijunctive regime studied in V57–V59, image membership is reduced to 2-SAT. Consequently, randomized range avoidance is already easy. The remaining challenge is deterministic derandomization or localization from structured starting information. That is a valid local-circuit problem, but the present repository does not establish a live bridge from it to unrestricted lower bounds or P versus NP.

V60 therefore changes the primary objective from extending the finite `n=9` search to:

1. consolidating the theorem and counterexample chain;
2. preparing a manuscript on `NC0_k-Avoid`;
3. obtaining external mathematical and prior-art review;
4. retaining exact search only for falsification, regression and reviewer-requested checks.

## Repository repairs

V60 adds stable entry points:

- `../STATE.md` — cumulative state in compact prose;
- `../LEDGER.json` — machine-readable claim and version ledger;
- `../verify_all.sh` — curated one-command verification;
- an updated `../README.md` pointing to V60 rather than V22.

The long-lived PR and branch naming are recorded as repository-governance issues. V60 does not merge the draft PR into `main`; that remains an explicit owner action after review.

## Reproduce

From this directory:

```bash
python verify.py
python verify_independent.py
```

From the parent directory:

```bash
bash ./verify_all.sh
bash ./verify_all.sh --full
```

## Files

- `THEOREM.md` — exact randomized easy-membership statement;
- `PROOF.md` — proof and tightness discussion;
- `SCIENTIFIC_STATUS.md` — claim boundaries and promotion decision;
- `MANUSCRIPT_PLAN.md` — paper outline and review gates;
- `RESULTS.json` — machine-readable V60 result;
- `EXTERNAL_CONTACT_STATUS.md` — no-contact record;
- `verify.py` and `verify_independent.py` — independent consistency checks;
- `VALIDATION_PRIMARY.txt` and `VALIDATION_INDEPENDENT.txt` — committed summaries;
- `SHA256SUMS.txt` and `PACKAGE_ZIP_SHA256.txt` — reproducibility hashes;
- `V61_CORE_CONTEXT.md` — frozen next-session context.
