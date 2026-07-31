# Laboratory promotion policy — effective V63

## Required lifecycle

Every completed laboratory follows this lifecycle:

```text
current main
  -> dedicated laboratory branch
  -> versioned package and verifiers
  -> non-draft pull request
  -> quick and full GitHub Actions
  -> squash merge into main
```

## Rules

1. **One laboratory per PR.** A PR may contain fixes needed by that laboratory, but may not silently bundle the next version.
2. **Base is current `main`.** A laboratory does not branch from an obsolete long-lived research branch.
3. **Completed PRs are not drafts.** Drafts may be used only while the package is incomplete.
4. **CI is a merge gate.** Both quick and full jobs must pass. Justified `SKIP` rows are permitted when recorded by policy.
5. **Preferred merge method is squash.** The `main` history receives one promotion commit per laboratory.
6. **No silent historical rewriting.** Corrections are explicit commits or later laboratories with a reason.
7. **External review is asynchronous.** Pending replies do not block promotion of internally consistent, conservatively worded packages.
8. **Scientific boundaries persist.** A merge does not imply peer review, novelty, priority or a P-versus-NP consequence.
9. **Artifacts are versioned.** Every lab includes a README, results record, primary verifier, independent verifier and next-context file.
10. **Main is the source of truth.** After merge, the next laboratory branches from the updated `main`.

## Legacy transition

PR `#1` consolidated V16–V62 and was merged into `main` as commit:

```text
968ac5d1b1b480484db1f4f22425e680f4204de9
```

V63 is the first laboratory governed by one-PR-per-version promotion.
