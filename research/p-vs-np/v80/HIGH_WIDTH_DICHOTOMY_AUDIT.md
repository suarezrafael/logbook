# High-width Hall/branchwidth dichotomy audit

## 1. Lower-bound-relevant target

Let

```text
C : {0,1}^n -> {0,1}^m,
```

where every output gate depends on at most three input variables and

```text
m = n + ceil(n^(2/3)).
```

ECCC TR23-021 shows that a deterministic polynomial-time algorithm with an NP oracle for this `NC0_3-Avoid` regime would imply explicit rigid matrices and super-linear lower bounds for logarithmic-depth circuits. This is a documented lower-bound bridge, not a direct implication for P versus NP.

V77 handles the low support-branchwidth regime by an FPT algorithm. V80 audits what a useful high-width alternative would actually have to prove.

## 2. Hall notation

Let `M` be the output gates and let `X` be the active input variables. For `S subseteq M`, define

```text
N(S) = union_{i in S} supp(i),
delta(S) = |S| - |N(S)|.
```

A set is Hall deficient when `delta(S)>0`.

Since `m>|X|`, the full set `M` is always Hall deficient. A maximum bipartite matching between gates and variables also returns a Hall witness in polynomial time. Therefore mere existence of a Hall witness cannot distinguish the high-width regime.

## 3. Projection lemma and the constructive gap

**Lemma 1 (Hall projection).** If `S` is Hall deficient, the projected circuit `C_S` has an output pattern outside its range. Every full output word extending that pattern avoids the range of `C`.

**Proof.** The projection depends only on `N(S)`, so its range contains at most `2^|N(S)|` patterns, fewer than the `2^|S|` possible patterns on `S`. If a full output word extending a missing pattern had a preimage under `C`, its restriction to `S` would be in the range of `C_S`, a contradiction. `□`

The lemma is existential. It has three distinct algorithmic readings.

### 3.1 Small neighborhood

If `|N(S)|=O(log n)`, enumerate all assignments to `N(S)`, evaluate `C_S`, store the polynomially many image patterns, and choose a missing pattern. This is deterministic polynomial time.

### 3.2 Randomized NP-oracle construction

Let `d=delta(S)>=1`. A uniformly random pattern on `S` lies in the range of `C_S` with probability at most

```text
2^|N(S)| / 2^|S| = 2^{-d}.
```

An NP oracle decides whether a proposed pattern has a preimage. Sampling until the oracle answers no is zero-error and has expected at most two trials. Taking `S=M` shows that randomized expected-polynomial avoidance with an NP oracle is already immediate for every `m>n` circuit. At the target stretch the probability of accidentally sampling an image point is at most `2^{-ceil(n^(2/3))}`.

### 3.3 Deterministic FP^NP does not follow

Counting does not supply a deterministic polynomial-size set of candidates guaranteed to contain a missing pattern. Asking whether a fixed candidate is in the range is NP, but asking whether a prefix has some missing completion has an additional universal quantifier. Thus the Hall argument by itself does not close the deterministic `FP^NP` gate in TR23-021.

A correct deterministic target is therefore:

**Candidate-list target.** Compute in polynomial time a list `L(C)` of polynomially many output words, or projected patterns with canonical extensions, such that at least one member is outside the range. NP range-membership queries then select an avoided word.

## 4. Hall/branchwidth identity

The support connectivity function is

```text
lambda_C(S) = |N(S) intersect N(M\S)|.
```

Because `N(S) union N(M\S)=X`, inclusion-exclusion gives the exact identity

```text
lambda_C(S) = |N(S)| + |N(M\S)| - |X|.
```

Hence, if both sides are Hall-nondeficient,

```text
|N(S)| >= |S|,
|N(M\S)| >= |M\S|,
```

then

```text
lambda_C(S) >= |M| - |X|.
```

Every subcubic branch decomposition has a balanced edge whose two gate sides have sizes between `m/3` and `2m/3`. Therefore:

**Theorem 2 (balanced Hall expansion forces width).** If every gate subset of size between `m/3` and `2m/3` is Hall-nondeficient, then

```text
branchwidth(lambda_C) >= m - |X|.
```

Equivalently, every branch decomposition of width below the stretch contains a balanced Hall-deficient side.

This theorem reverses the naive implication. High width does not automatically force a useful Hall certificate; rather, Hall expansion across balanced cuts is itself a mechanism forcing high width.

## 5. Linear local-expansion barrier

The naive high-width arm might be weakened to ask for a logarithmic-size Hall witness. Even that cannot hold for support families alone.

Choose `m=n+ceil(n^(2/3))` gates independently. Each gate makes three independent uniform choices from `[n]`; repeated choices are collapsed, so every support has rank at most three. Fix `s` gates and fewer than `s` variables. The probability that all `3s` choices land in those variables is at most `(s/n)^{3s}`.

For `s<=cn`, `c=1/(16e^2)`, and sufficiently large `n`, `m<=2n` and `s<=n/2`. A union bound gives

```text
Pr[some deficient S of size s]
 <= C(m,s) * s C(n,s) * (s/n)^{3s}
 <= s (2 e^2 s/n)^s
 <= s (1/8)^s.
```

Summing over all `s>=1` yields

```text
sum s(1/8)^s = 8/49 < 1.
```

Thus a support family exists with no Hall-deficient gate set of size at most `n/(16e^2)`.

This is an existence theorem only. It does not assert high branchwidth for every such family. It does prove that support rank three and target stretch do not force a logarithmic Hall witness.

## 6. Refined win-win program

The mathematically honest dichotomy is now:

### Low-width arm

Use V77 when support branchwidth is in the polynomially relevant parameter range. Since the decomposition cost and affine-state count are exponential in a quadratic function of width, the natural polynomial threshold is of order `sqrt(log n)`, up to constants hidden in the existing bounds.

### High-width arm

Produce one of the following in deterministic polynomial time:

1. a Hall witness with `O(log n)` active variables;
2. a polynomial candidate list obtained from affine pieces, sunflowers, or overlap compression;
3. a canonical all-orders obstruction proving that neither certificate exists.

The third outcome is not failure: it supplies the structured resistant families required by the V69 all-orders lower-bound program.

## 7. Bounded-arithmetic second front

The V56 affine certificate and V77 supplied-decomposition certificate are natural candidates for formalization in weak arithmetic, especially `APC^1`, where dual weak pigeonhole reasoning is available. V80 records this as the second front but does not claim a formalization. ECCC TR25-191 shows why the distinction between `PV_1`, `APC_1`, and proof-complexity generators is substantive rather than cosmetic.

## 8. Nonclaims

No deterministic `FP^NP` avoidance algorithm is proved. No implication from high branchwidth to affine or sunflower structure is proved. No lower bound, novelty claim, peer review, `APC^1` formalization, or P-versus-NP consequence is asserted.
