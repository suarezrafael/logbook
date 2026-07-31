# Workflow audit — V66

Infrastructure changes are kept separate from mathematical evidence.

## Runner coverage

A repository preflight now requires every laboratory directory at or after the one-laboratory-per-PR policy boundary (`V63`) that contains `verify.py` to have a primary runner entry. The current ledger version must also have both primary and independent entries. This prevents a newly added laboratory from being silently omitted.

Historical laboratories remain curated: the V22 missing artifact and V26 missing script retain explicit skip reasons.

## Transcripts

Quick and full commands write complete logs and upload them as distinct GitHub Actions artifacts. Artifact upload uses `actions/upload-artifact@v7`, selected after checking the official action documentation and release history.

## LaTeX

A separate `latex` job installs the minimum TeX Live packages required by the standalone V64 and V65 modules, compiles each twice with `pdflatex -halt-on-error`, and uploads PDFs and logs. LaTeX compilation is a publication-integrity check, not mathematical validation.

No pip cache is introduced because the verification suite uses only the Python standard library. An apt cache is also omitted because the new package installation is confined to one independent job and cache invalidation would add more maintenance surface than demonstrated benefit.
