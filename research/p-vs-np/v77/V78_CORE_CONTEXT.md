# V78 core context — reproducibility firewall and explicit decomposition APIs

## Established mathematical starting point

V77 now has two linked results.

First, the restricted topology-tree transfer maps a supplied width-`b`
subcubic gate decomposition to

```text
width <= 2b,
height = O(log m),
EPL = O(m log m).
```

Second, `lambda_C` is a connectivity function and the Korhonen--Oum exact FPT
algorithm discovers a width-`k` branch decomposition from oracle access, where
`k=branchwidth(lambda_C)`. Composing discovery, V77, V75, and V74 gives

```text
2^{O(k^2)} gamma m^6 log m
  + O(m log m A(2k)^2 poly(n,m))
```

avoidance time for `m>n`, without assuming a supplied decomposition.

## Priority-zero V78 problem: clean-checkout reproducibility

A clean `main` checkout currently becomes dirty after the cumulative verifier.
Before extending the theorem chain, V78 must make audit artifacts reproducible
and add a blocking clean-tree gate.

Required repairs:

1. run every generator/verifier in a clean temporary copy and inventory all
   modified versioned files;
2. remove wall-clock fields such as `elapsed_seconds` from committed snapshots,
   or move them to untracked benchmark outputs;
3. preserve the V53 retraction status in an immutable status file that its
   generator cannot overwrite;
4. reconcile stale V70 and V72 snapshots with their current generators;
5. canonicalize JSON indentation and key ordering;
6. make verification read-only whenever regeneration is not the test's purpose;
7. add a final CI step equivalent to `git diff --exit-code` and
   `git status --porcelain` after quick and full verification;
8. update `LEDGER.json` through the promoted laboratory and make runner coverage
   derive its current version from `STATE.md` or the filesystem, not a lagging
   ledger value;
9. replace the hand-maintained LaTeX list with a validated manifest or safe
   discovery rule.

No allowlist of unexplained dirty artifacts is acceptable as the final state.

## Priority-one API repair

Theoretical V74/V75 entry points must stop silently constructing
`balanced_branch_tree(range(m))` when no decomposition is provided.

Required API behavior:

```text
tree=None  -> explicit error in theorem-facing APIs.
```

Naive index-balanced and heuristic constructors may remain only in clearly
named convenience or experiment functions. Every result snapshot must record:

- decomposition source: supplied, exact FPT, approximation, or heuristic;
- measured support width;
- height and external path length;
- construction time separately from avoidance time;
- whether any theorem guarantee applies.

## Priority-two mathematical target

After the reproducibility and API gates are green, return to the remaining
factor-two question:

```text
Can logarithmic-height transfer preserve width, achieve b+O(1),
or beat (2-epsilon)b?
```

Promising routes remain source-tree-aware height-capped dynamic programming,
overlap/uncrossing of the two middle sets, and genuine logarithmic-height
lower-bound families.

## Proof discipline

- Korhonen--Oum decomposition discovery is prior art and is used as a black box.
- The FPT result is parameterized by support connectivity branchwidth; it is not
  an unrestricted polynomial-time algorithm.
- A cluster attaining `2b` does not imply every hierarchy needs `2b`.
- Perfect-height inflation is not an `O(log m)` lower bound.
- Keep the direct P-versus-NP route inactive absent an unrestricted,
  lower-bound-relevant consequence.
