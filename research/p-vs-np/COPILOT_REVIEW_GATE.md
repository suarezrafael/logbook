# Copilot review gate

Every laboratory promotion uses the following sequence:

1. Create the laboratory branch from the promoted `main` commit.
2. Open a draft pull request and run quick, full, and LaTeX GitHub Actions.
3. After those jobs pass on a stable head SHA, mark the PR ready for review to trigger GitHub Copilot. Do not merge yet.
4. Wait for the Copilot review of that head and inspect the review summary, every inline thread, suppressed findings reported in the summary, and top-level comments.
5. Classify each finding as actionable, informational, obsolete, duplicate, or intentionally rejected with a recorded reason.
6. Fix every actionable finding and add a regression check when practical.
7. Any new commit invalidates both the previous CI result and the previous final-diff review. Run quick, full, and LaTeX again and request another Copilot review of the new head.
8. Merge only when:
   - quick, full, and LaTeX are successful on the same final SHA;
   - a Copilot review has completed for that final diff;
   - no unresolved actionable Copilot thread remains;
   - scientific and publication nonclaims remain intact.

A review arriving after merge indicates a process failure and must be audited in a follow-up maintenance PR before the next laboratory is concluded.
