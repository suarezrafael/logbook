# Laboratory V109 — MUX gate-flow dichotomy

V109 attacks the one-SCC residual isolated by V108.

A fixed signed MUX output gives two exact branch implications.  If two directed cycles start at the same selector with opposite source phases and use disjoint output gates, their targets can be chosen so the two cycles force opposite values on that selector.  V109 searches for these cycles by a gate-capacitated max-flow construction.

## Flow-or-bottleneck alternative

For two outputs sharing a selector `v`, choose branches with opposite selector phases and send one unit from each branch destination back to `v`.  Every other output gate has capacity one.

- max-flow `2` gives two output-gate-disjoint return routes and a constructive missing output;
- max-flow `1` gives, by min-cut, one explicit output gate that lies on every return path from either destination to `v`.

For a strongly connected branch graph with `m>n`, a repeated selector always exists, so this yields a polynomial structural dichotomy: **missing-output certificate or one-gate bottleneck**.  The bottleneck branch is not yet solved.

## Strict family

The V109 family has one central selector `v`, two central MUX outputs, and two return lobes.  It has

```text
n=2k+1,
m=n+1,
```

is Hall-minimal, has a strongly connected branch graph, and has exact V102 backdoor

```text
beta = 1 + 2 ceil(k/2) = Theta(n).
```

More strongly, the family has **no V108 SCC-separated certificate for any ignored-output set**, yet V109 finds two gate-disjoint opposite-phase cycles immediately.

## Verification

`verify.py` runs the implemented max-flow construction, strict-family soundness against complete original ranges, signed switchings, exact small beta, Hall minimality, exhaustive separation from V108 on the first members, a deterministic bottleneck control, and random strongly connected dichotomy tests.

`verify_independent.py` does not import the V109 implementation.  It reconstructs the strict family and explicit target, verifies unsatisfiability with an independent 2-SAT SCC engine through growing `k`, brute-forces small original ranges, independently checks Hall minimality and beta, and exhaustively reconstructs the V108 no-certificate property on the first members.

## Boundary

V109 does not yet convert the one-gate bottleneck into a missing output.  Therefore it does not prove all essential MUX/bijunctive `0x1b` circuits are in P.  It does not solve unrestricted `NC0_3-Avoid`, prove a new general circuit lower bound, or resolve P versus NP.
