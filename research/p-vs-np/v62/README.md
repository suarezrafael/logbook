# NC0_k-Avoid Laboratory V62

## Integrated manuscript and external-review package

**Scientific status:** internally verified editorial and reproducibility package. The mathematical results assembled here remain unreviewed externally. Novelty and priority are not confirmed. The project is not presented as an active route to P versus NP.

## Main outcomes

V62 converts the V61 audit into a reviewable paper package:

1. an integrated manuscript centered on the V56/V57 positive–negative dichotomy;
2. a formal translation of the V57 gadget into clause- and block-level 2-CNF irredundancy terminology;
3. an explicit comparison of the V54 forcing-core certificate with Kuntewar–Sarma's monotone `NC0_3-Avoid` algorithm;
4. a machine-readable source-to-claim matrix;
5. a documented negative prior-art search for grouped affine fibers and orientation depth;
6. two external prior-art requests sent on 2026-07-30;
7. a GitHub Actions workflow for quick and full repository verification.

## External contact

Two messages were sent:

- to Karthik Gajulapalli and Jayalal Sarma, with Neha Kuntewar copied, concerning Range Avoidance prior art;
- to Paolo Liberatore concerning grouped-clause and IES terminology for the V57 construction.

No answer is assumed. The status is `sent_awaiting_reply`.

## Reproduce V62

```bash
python verify.py
python verify_independent.py
```

From the parent directory:

```bash
bash ./verify_all.sh
bash ./verify_all.sh --full
```

The full historical runner could not be executed in the local ChatGPT container because the container could not resolve `github.com` to obtain a complete checkout. V62 adds CI so that the committed branch can run the same commands in a clean GitHub-hosted environment.

## Files

- `INTEGRATED_MANUSCRIPT.md` — first integrated article draft;
- `SOURCE_TO_CLAIM.md` and `SOURCE_TO_CLAIM.json` — citation and claim ledger;
- `V57_IES_TRANSLATION.md` — standard 2-CNF/IES translation;
- `V54_KUNTEWAR_SARMA_COMPARISON.md` — overlap and distinction table;
- `PRIOR_ART_SEARCH_LOG.md` — searches, nearby literature and unresolved novelty;
- `EXTERNAL_CONTACT_STATUS.md` — sent/awaiting-reply record;
- `RESULTS.json` — machine-readable V62 state;
- `verify.py` and `verify_independent.py` — independent package checks;
- `V63_CORE_CONTEXT.md` — frozen continuation context.

## Promotion decision

V62 is promoted as an **integrated manuscript and external-review package**. It is not promoted as:

- confirmation of novelty;
- a peer-reviewed theorem package;
- a solution to general `NC0_3-Avoid`;
- a completed `n=9` classification;
- an unrestricted circuit lower bound;
- progress toward resolving P versus NP.
