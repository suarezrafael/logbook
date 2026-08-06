# Laboratory V92 — canonical all-instance completion and the runtime barrier

## Classification

V92 is an **algorithmic-interface and trajectory laboratory**. Under the repository implication taxonomy it is recorded as infrastructure, not completed frontier progress.

V91 identified a model mismatch: the inherited branchwidth engine returns an avoided output only under a low-width promise, while modern Range-Avoidance transfers require a total algorithm in an exact output model. V92 removes the output-model part of that mismatch by defining one canonical halving policy that both the inherited exact prefix-count engine and the Huang–Li–Zhong all-instance greedy algorithm can implement.

## Canonical policy

For a circuit `C:{0,1}^n->{0,1}^m`, with `m>=n+1`, process output coordinates in the order `0,1,...,m-1`.

At a current prefix `p`, compute the exact preimage counts

```text
N(p0) = |{x : C(x) starts with p0}|,
N(p1) = |{x : C(x) starts with p1}|.
```

Choose the child of smaller count, breaking ties toward zero. Once the selected count is zero, fill every remaining output bit with zero.

Because

```text
N(p0)+N(p1)=N(p),
```

the selected count is at most `N(p)/2`. Starting from `2^n`, the count is therefore zero after at most `n+1` nonempty steps. The completed word is outside the range.

This policy is single-valued: the output order, tie break, and empty-suffix convention are fixed.

## Two evaluators, one output semantics

The policy can be driven by either of two exact prefix-count evaluators:

1. **Low support branchwidth.** V75 compiles exact prefix counts into one arithmetic DAG; V77 discovers and balances a support decomposition. In the proved `O(sqrt(log m))` branchwidth regime, the canonical policy is polynomial-time.
2. **All instances.** Huang–Li–Zhong Algorithm 4 evaluates the same halving decision through connected preimage subspaces. It works on every `NC0_k` circuit, but the proven runtime is

```text
O(n * 2^((k-2)n/(k-1))).
```

Thus V92 supplies a total semantic completion, not a total polynomial-time completion.

## Executable audit

`canonical_halving.py` independently implements exact brute-force prefix counts and the connected-component factorization of fixed local outputs.

Committed checks:

```text
all n=2, m=3, locality-2 circuits       4,096 circuits
exact prefix-count comparisons          61,440
canonical avoided outputs                4,096
Claim 6.8 traversed-weight checks         8,448
seeded n=4, m=5, locality-3 circuits       512
seeded prefix-count comparisons           2,107
seeded Claim 6.8 checks                    1,595
```

There are zero count or Claim 6.8 mismatches.

The audit also compares the new canonical policy with V75's previous completion-capacity policy. They agree on 2,560 circuits and differ on 1,536. This confirms that V91's output-model mismatch was real rather than terminological.

## Runtime boundary

Huang–Li–Zhong prove that their greedy strategy has exponential worst-case runtime for `NC0_k-Avoid[n,O(n)]`. Random expanding, locally tree-like instances keep one major preimage component and provide few cycles from which the representation could compress.

The first remaining bridge is therefore:

```text
compute the canonical child comparison N(p0) <= N(p1)
for every target instance in the complexity required by a checked transfer,
without enumerating an exponentially large traversed decision space.
```

Improving constants in the low-width dynamic program does not solve this bridge.

## Files

- `canonical_halving.py` — canonical policy, exact component factorization, and finite audits;
- `RESULTS.json` — immutable quantitative snapshot;
- `CANONICAL_COMPLETION_THEOREM.md` — theorem and proof interface;
- `HLYZ_RUNTIME_CALIBRATION.md` — literature parameter and barrier audit;
- `IMPLICATION.json` — implication chain and first remaining bridge;
- `verify.py` and `verify_independent.py` — primary and independent checks;
- `V93_CORE_CONTEXT.md` — next runtime-compression gate.

## Nonclaims

V92 does not give a polynomial-time all-instance algorithm, reproduce the optimized Huang–Li–Zhong implementation, prove a new circuit lower bound, evade relativization or algebrization barriers, establish novelty, supply peer review, or resolve P versus NP.
