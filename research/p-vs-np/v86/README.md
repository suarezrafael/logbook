# Laboratory V86 — intersection of Hall, syndrome, and width certificates

V86 tests whether one support family can simultaneously defeat the three constructive certificate mechanisms accumulated by the laboratory:

1. a Hall-deficient projection with a small active neighborhood;
2. a nonzero constant output syndrome;
3. exact enumeration through low support branchwidth.

The answer from the three finite V80 obstruction controls is negative, but the audit isolates a stronger two-barrier family and clarifies which missing invariant remains.

## 1. The three V80 controls are not C4-free

The seven-, eight-, and nine-variable examples contain respectively

```text
15, 17, and 18
```

four-cycles in their bipartite incidence graphs. Their incidence girth is four.

This rules out the hoped-for shortcut that the existing finite examples already inherit the V85 C4-free syndrome theorem.

## 2. C4 is necessary, not sufficient

Assign the same essential nonlinear gate to every distinct ternary support:

```text
NOR3(a,b,c)=1 exactly on 000.
```

Over `F_2`, its algebraic normal form is

```text
1+a+b+c+ab+ac+bc+abc.
```

For a simple 3-uniform support family, every output has a cubic monomial equal to its own support triple. Distinct supports give distinct cubic monomials. In the XOR of any nonempty set of outputs, the cubic monomial of each selected gate appears exactly once and therefore cannot cancel.

Hence the nonconstant ANF vectors of all outputs are linearly independent and there is no nonzero constant syndrome. This remains true even when the incidence graph contains many C4s.

The V80 examples have ranks `11`, `12`, and `14`, equal to their output counts, and exhaustive selector enumeration finds zero nonzero constant syndromes.

This sharpens V85:

> A C4 is necessary for nonlinear cancellation between different ternary gates, but the existence of a C4 is far from sufficient.

## 3. The finite controls do not defeat all three certificates

The measured table is:

| family | C4s | minimum Hall set | Hall neighborhood | branchwidth | constant syndromes under NOR3 |
|---|---:|---:|---:|---:|---:|
| seven variables | 15 | 7 | 6 | 5 | 0 |
| eight variables | 17 | 8 | 7 | 5 | 0 |
| nine variables | 18 | 9 | 8 | 6 | 0 |

Thus `NOR3` defeats the syndrome certificate, but:

- the Hall neighborhoods are still constant-sized and directly enumerable;
- the support branchwidths are still `5`, `5`, and `6`, so the V77→V75→V85 exact algorithm applies.

No finite V80 control is a simultaneous obstruction to all three certificate families.

## 4. An asymptotic two-barrier family

Modify the V80 random model so every gate independently chooses a uniformly random 3-subset of `[n]`.

The V80 Hall union bound remains valid because for `t<=n`,

```text
binom(t,3)/binom(n,3) <= (t/n)^3.
```

The probability of any duplicate support is at most

```text
binom(m,2)/binom(n,3)=O(1/n).
```

The Hall bad-event sum is at most `8/49`. Therefore, for all sufficiently large `n`, the combined probability of either a duplicate support or a Hall-deficient gate set of size at most `n/(16e^2)` is less than one.

Consequently there exists a simple 3-uniform support family at the target stretch with:

1. no Hall-deficient gate set of size at most `n/(16e^2)`;
2. no nonzero constant syndrome after assigning `NOR3` to every gate.

This is the first family in the laboratory proved to block the small-Hall and syndrome mechanisms simultaneously.

What is not proved is high support branchwidth for the same family. That missing third property is now the precise certificate-intersection target.

## 5. Calibration against the V84 hard branch

V80 gives

```text
balanced Hall expansion => branchwidth >= sigma=m-n.
```

At the target stretch, `sigma=Theta(n^(2/3))`. V85 is polynomial for branchwidth `O(sqrt(log m))`.

The ratio between these scales grows quickly:

```text
n=64       ratio ~ 6.36
n=512      ratio ~ 21.13
n=4096     ratio ~ 73.63
n=32768    ratio ~ 264.01
```

Improving the affine-state count from `sqrt(log m)` to `log m` or `log^2 m` would strengthen the bounded-width algorithm, but it would still remain asymptotically disjoint from the balanced-Hall hard branch. Such optimization is an algorithmic-paper direction, not by itself progress across the rigidity bridge.

## 6. Input restriction no-go

Fixing input variables only shrinks the range:

```text
Range(C restricted by rho) subseteq Range(C).
```

An output missing from the restricted map need not be missing from the original map. For example,

```text
C(x)=(x,0).
```

After restricting `x=0`, the word `(1,0)` is absent, but it belongs to the unrestricted range. Therefore random restrictions cannot be used merely to inflate the stretch and then pull an avoided output back.

## 7. V87 targets

The next laboratory should prioritize:

1. **Constructive `Eval_H` using repeated tables.** Treat the `k` layers as a repeated-factor map, not a generic locality-eleven circuit. Test cyclic automorphisms, repeated-base small-bias spaces, and tensor-compatible codes.
2. **Complete the three-certificate intersection.** Seek an explicit or probabilistic simple 3-uniform family with local Hall expansion, no constant syndrome, and branchwidth `Omega(n^(2/3))` or at least `n^Omega(1)`.
3. **Remote-point bridge calibration.** Quantify the exact distance and dimension parameters required by each rigidity or average-case-hardness bridge before claiming directional progress.
4. **Bounded arithmetic.** Recover the deferred `dWPHP/APC^1` formalization program for the historical range-avoidance certificates.
5. **Proof-complexity matching.** Require exact agreement of predicate, encoding, field, proof system, expansion parameters, and stretch. Every failed match is itself a recorded result.

## Nonclaims

V86 does not produce a family defeating all three certificate mechanisms, does not solve the V84 Hall-expander branch, does not construct the existential support-only list, does not prove high branchwidth for the asymptotic two-barrier family, does not establish a rigidity consequence, and does not resolve `P` versus `NP`.
