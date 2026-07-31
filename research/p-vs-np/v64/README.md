# Laboratory V64 — formal V57 module and workflow runtime maintenance

V64 converts the V57 reviewer appendix into a typeset theorem/proof module backed by a machine-readable specification and two independent exhaustive verifiers. It also upgrades the verification workflow from `actions/checkout@v4` to `actions/checkout@v6` after a separate runtime compatibility audit.

## Main files

- `V57_BLOCK_IRREDUNDANCY_THEOREM.tex` — standalone theorem/proof module;
- `V57_BLOCK_IRREDUNDANCY_SPEC.json` — normative clauses, blocks, masks and witnesses;
- `verify.py` — primary exhaustive verifier;
- `verify_independent.py` — independent reimplementation;
- `ACTION_RUNTIME_AUDIT.md` — non-scientific workflow maintenance audit;
- `EXTERNAL_RESPONSE_CHECK.md` — dated response check;
- `FORMALIZATION_NOTES.md` — formal scope and nonclaims;
- `RESULTS.json` — machine-readable V64 result;
- `V65_CORE_CONTEXT.md` — frozen next-laboratory context.

## Validation

```bash
python verify.py
python verify_independent.py
pdflatex -draftmode -interaction=nonstopmode V57_BLOCK_IRREDUNDANCY_THEOREM.tex
```

Local validation passed 116 primary checks, 91 independent checks and a LaTeX draft compilation. The module is not peer reviewed and makes no novelty or priority claim.
