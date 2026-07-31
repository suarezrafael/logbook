# P versus NP Lab V20

V20 contains a candidate effective-dimension theorem for range avoidance in symmetric NC0_3 circuits.

## Candidate result

```text
m > |V_T| + rank_GF2(A_P) + rank_GF3(A_R)
```

Uniform corollary:

```text
m > 3n
```

## Files

- `RESEARCH_NOTE.md` — concise statement, context, and limitations;
- `FORMAL_PROOF.md` — human-readable proof candidate;
- `RESULTS.json` — verified finite results and scientific status;
- `verify.py` — compact independent finite verifier;
- `EXPERT_REVIEW_REQUEST.md` — review questions and publication caution.

## Verify

```bash
python v20/verify.py
```

## Scientific status

- internal level-4 candidate;
- external conservative level 3.5;
- not peer reviewed;
- novelty and priority not established;
- does not resolve P versus NP.
