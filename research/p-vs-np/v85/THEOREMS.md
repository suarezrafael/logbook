# V84 hard-branch completeness theorem

## Problem classes

Let `A` be unrestricted `NC0_3-Avoid` at the target stretch. Let `A_exp(L)` be
the promise restriction in which every output set `S` with `|S|<=L` satisfies

```text
|N(S)| >= |S|.
```

For `L=c log(n+m)`, call this the logarithmic Hall-expander branch.

## Theorem

For every fixed `c>0`, unrestricted `NC0_3-Avoid` and its logarithmic
Hall-expander restriction are equivalent under deterministic search-Turing
reductions computable in `FP^NP`.

## Proof

The restriction-to-full direction is the identity: an algorithm for the full
problem solves every promised instance.

For the full-to-restriction direction, run the V84 preprocessing procedure with
`L=c log(n+m)`.

- If the exact transversal girth is at most `L`, V84 extracts a canonical
  shortest circuit, enumerates its `g-1` input neighborhood, and returns an
  avoided global output.
- Otherwise, V84 returns the original circuit. The proof of its dichotomy
  guarantees `|N(S)|>=|S|` for every output set of size at most `L`. Invoke the
  solver for the promised branch on that same circuit and return its output.

The second branch needs no nontrivial solution pullback because the promised
instance is the original circuit. The preprocessing uses an NP oracle for exact
girth and canonical-circuit extraction. Therefore the reduction is a search
Turing reduction in `FP^NP`.

## Precision

This is not a polynomial-time many-one completeness theorem and does not place
the promise problem in a standard decision-complexity class. It is a structural
completeness statement for the laboratory's total-search task under the exact
V84 preprocessing interface.

# V85 proof kernel: support-only lists and ternary Fourier census

## 1. Model

Fix a support hypergraph `H=(S_1,...,S_m)` on `n` Boolean inputs. Output `i` applies an arbitrary Boolean table `f_i` to the variables in `S_i`, with `|S_i|<=3`.

A support-only list is an ordered set of candidate strings `Y=(y^1,...,y^k)` computed without reading the local truth tables. It succeeds for a circuit when at least one candidate is outside the circuit range.

## 2. Two-candidate impossibility

Assume every support has size exactly three and must be essential. For arbitrary targets `y^0,y^1`, choose witnesses `x^0=0^n` and `x^1=1^n`.

For each output coordinate `i`, prescribe

```text
f_i(000)=y^0_i,
f_i(111)=y^1_i.
```

These endpoint conditions can always be completed to an essential ternary function:

- equal endpoint values: use NAE or its complement;
- unequal endpoint values: use MAJORITY or its complement.

Therefore both targets lie in the range. No truth-table-blind singleton or pair is a universal list-solution, even when all three declared variables are essential.

## 3. Counting existence theorem

Let `F_i` be the allowed family of truth tables for output `i`, and write

```text
Q = sum_i log2 |F_i|.
```

There are `2^Q` circuits. For an ordered `k`-tuple of input witnesses there are `2^(nk)` choices. Every pair consisting of a circuit and witness tuple determines one ordered `k`-list of outputs. Hence the number of simultaneously coverable ordered lists is at most

```text
2^(Q+nk).
```

There are `2^(mk)` ordered target lists. Consequently, if

```text
k(m-n) > Q,
```

some support-only list is not simultaneously coverable by any allowed truth-table assignment. Such a list is a universal list-solution for the fixed support system.

For arbitrary ternary gates, `Q<=8m`, so it is enough to choose

```text
k = floor(8m/(m-n)) + 1.
```

At `m=n+n^(2/3)`, this is at most `8n^(1/3)+9` up to integer rounding. Thus the proposed claim that no polynomial support-only list can work is false.

The theorem is existential. It does not provide a polynomial-time construction of the list.

## 4. Evaluation-circuit reduction

Define `Eval_H` as follows. Its input consists of:

1. the truth tables of all output gates (`Q` bits), and
2. `k` independent candidate witnesses (`nk` bits).

Its output is the concatenation of the `k` circuit evaluations (`mk` bits).

A string outside `Range(Eval_H)` is exactly a support-only `k`-list that no circuit on `H` can cover simultaneously. The output length exceeds the input length precisely when `k(m-n)>Q`.

Each output bit of `Eval_H` is computable by an adaptive decision tree of depth four: query the three witness bits, then query the selected truth-table bit. As a nonadaptive Boolean junta it uses at most eleven bits.

This is the correct remote-point reduction produced by V85. Its layered structure is stronger than an arbitrary locality-eleven circuit, but no polynomial-time avoidance theorem at the near-linear stretch is proved here.

## 5. Exact ternary Fourier lemma

Represent a Boolean predicate by `g:{-1,+1}^3->{-1,+1}`.

The count is elementary. There are `2^(3+1)=16` affine predicates. Among the `binom(8,4)=70` balanced predicates, exactly 14 are nonconstant affine characters or their complements. Hence the partition is

```text
16 affine,
184 non-affine unbalanced,
56 balanced non-affine.
```

Now let `g` be balanced and non-affine. Its constant Fourier coefficient is zero. If every degree-one and degree-two coefficient were zero, Parseval would force the only remaining coefficient, the cubic coefficient, to have magnitude one. Then `g` would be the three-variable parity or its complement, contradicting non-affinity. Therefore some degree-one or degree-two coefficient is nonzero.

Both `g` and every nonconstant Fourier character are balanced sign vectors on eight points. Their Hamming distance is even, so their normalized inner product belongs to

```text
{-1, -1/2, 0, 1/2, 1}.
```

Magnitude one would again make `g` affine. Thus the nonzero low-degree coefficient found above has magnitude exactly `1/2`. Equivalently, `g` agrees with a dictator or a two-variable parity, possibly complemented, on exactly `3/4` of the cube.

The exhaustive census further splits the 56 predicates into:

- 32 with three nonzero degree-one/two coefficients of magnitude `1/2` and one cubic coefficient of magnitude `1/2`;
- 24 with four nonzero degree-one/two coefficients of magnitude `1/2` and zero cubic coefficient.

Therefore no balanced non-affine ternary predicate is low-degree-Fourier-uncorrelated. The theorem is analytic; the 256-table program is an independent finite audit and supplies the profile counts.

## 6. Why the Fourier lemma does not close the hard branch

Coordinatewise correlation is not a global range-avoidance certificate. Replacing every gate by its best affine character creates an affine approximation with expected coordinate error `m/4`, while the guaranteed redundancy is only `m-n=n^(2/3)`. An arbitrary codimension-`n^(2/3)` affine image may have covering radius only `n^(2/3)`, far below `m/4`.

The known Fourier-to-XOR method therefore still needs a global strong-refutation argument. Current unconditional algorithms for general ternary-local avoidance operate at approximately `m >= c n log n`, while `m=n+O(n^(2/3))` is tied to explicit rigid-matrix constructions. The local 256-table census identifies available Fourier mass but does not remove that global threshold.

## 7. Claims and nonclaims

Proved and exhaustively verified here:

1. no support-only list of size at most two works for all essential ternary truth tables;
2. a support-only list of size `floor(Q/(m-n))+1` exists nonconstructively;
3. constructing that list is exactly a structured range-avoidance problem for `Eval_H`;
4. the `16/184/56` ternary classification and the exact `1/2` low-degree correlation lemma.

Not proved:

- an efficient construction of the counting list;
- a polynomial-time algorithm at `m=n+n^(2/3)`;
- a new rigid-matrix construction or circuit lower bound;
- `P != NP`.

# Constant syndromes, four-cycles, and the high-girth hard branch

## 1. Model

Let

\[
C:\{0,1\}^n\to\{0,1\}^m
\]

be a local Boolean circuit over `F_2`. Output gate `i` has support `S_i` and
unique algebraic normal form

\[
C_i(x)=b_i+\ell_i(x)+R_i(x),
\]

where `b_i` is constant, `ell_i` is the degree-one part, and every monomial of
`R_i` has degree at least two.

A parity selector is a vector `lambda in F_2^m`. It defines the output
syndrome

\[
S_\lambda(x)=\lambda^T C(x).
\]

The support system is **linear** when

\[
|S_i\cap S_j|\le 1\qquad(i\ne j).
\]

Equivalently, its bipartite incidence graph has no four-cycle.

## 2. Main theorem

**Theorem.** Assume the support system is linear. Then `S_lambda(x)` is
constant if and only if both conditions hold:

1. every selected gate `i` with `lambda_i=1` is affine, meaning `R_i=0`;
2. the selected linear parts cancel:

   \[
   \sum_{i:\lambda_i=1}\ell_i=0.
   \]

In that case the constant value is

\[
S_\lambda(x)=\sum_{i:\lambda_i=1}b_i.
\]

### Proof

The reverse implication is immediate.

For the forward implication, suppose a selected gate `i` is non-affine. Pick
one monomial `M` of degree at least two occurring in `R_i`. If the same
monomial occurred in another gate `j`, then `M subseteq S_i cap S_j`, so
`|S_i cap S_j|>=2`, contradicting linearity. Thus `M` is globally unique to
gate `i` and cannot cancel in the selected parity. Therefore the syndrome is
not constant. Hence every selected gate is affine. Constancy then forces the
remaining degree-one terms to cancel. QED.

## 3. Algorithmic corollary

On a linear support system, every constant parity certificate can be found in
polynomial time:

1. compute the exact ANF of every local truth table;
2. retain only affine gates;
3. form their linear coefficient matrix `A_aff`;
4. compute a nonzero vector in the left kernel of `A_aff`;
5. compute its constant syndrome value `c`;
6. return any target `y` with `lambda^T y != c`.

This works even when the full circuit contains non-affine gates: the
certificate may use an affine subsystem.

The certificate verifier only checks local ANFs, one nullspace identity, and
one output parity. It runs in deterministic polynomial time.

## 4. Consequence for the V84 branch

Whenever the V84 hard promise gives incidence girth greater than four, its
support system is linear. Therefore the proposed co-kernel strategy has an
exact classification:

> Constant co-kernel syndromes do not obtain cancellation from nonlinear
> residues in the high-girth branch. They are precisely affine-subsystem
> dependencies.

This sharpens the proposed statement "Hall expansion should prevent
cancellation." Hall expansion is not needed for this obstruction. Absence of
four-cycles already prevents every cancellation of a degree-two or degree-three
monomial across distinct ternary gates.

This reconnects the syndrome era and the expander era of the laboratory:

- before the high-girth reduction, shared pairs can create nonlinear constant
  syndromes;
- after the reduction, those shared pairs are absent, and the syndrome route
  collapses to affine dependencies.

## 5. Exact four-cycle counterexample

The executable artifact includes a circuit with six inputs and seven essential
ternary gates. The first four outputs are

\[
\begin{aligned}
g_0&=x_0x_1+x_2,\\
g_1&=x_0x_1+x_3,\\
g_2&=x_2+x_4+x_5,\\
g_3&=x_3+x_4+x_5.
\end{aligned}
\]

Hence

\[
g_0+g_1+g_2+g_3\equiv0.
\]

The selected four gates use six variables, so this selector is not Hall
deficient. Three additional essential affine gates are added so that the only
strict Hall deficiency is the full seven-output set on six inputs.

The incidence graph has girth four because the first two supports share the
pair `{x_0,x_1}`. Thus the witness demonstrates both facts:

1. an algebraic syndrome can be strictly stronger than strict Hall deficiency;
2. the improvement disappears as soon as four-cycles are forbidden.

## 6. Machine audit

The probe uses the twelve lines of the affine plane `AG(2,3)` as a 3-uniform
linear support family (`n=9`, `m=12`, incidence girth six).

- 384 deterministic truth-table assignments were tested;
- 866 nonzero constant syndromes were recomputed;
- zero constant syndromes selected a non-affine gate;
- the primary and independent verifiers use separate ANF and dependency code.

The experiment is a regression audit. The theorem itself is the uniqueness-of-
monomials proof above.

# Remote points from exact Hamming-ball pair counting

## 1. Distance version of range counting

Let

\[
C:\{0,1\}^n\to\{0,1\}^m
\]

and let

\[
B(m,r)=\sum_{j=0}^{r}\binom mj
\]

be the radius-`r` Hamming-ball volume.

**Theorem.** If

\[
2^n B(m,r)<2^m,
\]

then a target `y` satisfying

\[
\operatorname{dist}(y,\operatorname{Range}(C))>r
\]

can be constructed by a deterministic prefix search, provided the required
pair counts can be computed exactly.

## 2. Prefix pair count

For an output prefix `p` of length `ell`, define

\[
A_r(p)=\left|\{(x,z):z_{<\ell}=p,\ d_H(C(x),z)\le r\}\right|.
\]

For a fixed input `x`, if `d_p(x)` is the number of disagreements between `p`
and the first `ell` bits of `C(x)`, then

\[
A_r(p)=\sum_x B(m-\ell,r-d_p(x)).
\]

The root satisfies

\[
A_r(\epsilon)=2^nB(m,r)<2^m.
\]

Every prefix obeys the exact conservation identity

\[
A_r(p)=A_r(p0)+A_r(p1).
\]

If `A_r(p)<2^{m-|p|}`, at least one child `pb` satisfies

\[
A_r(pb)<2^{m-|p|-1}.
\]

Choose such a child and continue. At a full-length leaf, the count is a
nonnegative integer smaller than one, hence zero. No range point lies within
radius `r` of the returned target.

## 3. Quantitative distance

Write `sigma=m-n`. The condition is equivalent to

\[
B(m,r)<2^\sigma.
\]

Using the elementary bound `B(m,r) <= (em/r)^r`, one may conservatively take

\[
r=\Omega\!\left(\frac{\sigma}{\log m}\right).
\]

Thus at the target stretch `sigma=n^(2/3)` and `m=Theta(n)`, exact pair
counting gives a remote point at distance

\[
\Omega\!\left(\frac{n^{2/3}}{\log n}\right).
\]

This is strictly stronger than merely producing one absent output.

## 4. Complexity interface

The theorem separates two components:

1. a universal, elementary prefix-selection argument;
2. a structural algorithm for computing `A_r(p)`.

For bounded-width circuits, the intended integration is to specialize the
paired generating-polynomial dynamic program so that it records Hamming
mismatch degree and prefix restrictions. Summing coefficients of degree at
most `r` gives `A_r(p)`.

This packet does **not** claim that the historical V75 implementation was
modified: its source was not available in the active working set. The packet
supplies:

- a complete proof of the oracle theorem;
- an executable exact oracle for small circuits;
- eight deterministic end-to-end remote-point controls;
- a precise integration contract for the V75 engine.

Any asymptotic bounded-branchwidth runtime must be inherited only after a
line-by-line audit of the V75 state space and arithmetic bounds.

## 5. Machine controls

Eight deterministic local circuits were tested with `n=4..6` and `m=8..13`.
In every case:

- the strict volume inequality was checked;
- prefix pair counts maintained the invariant;
- the terminal pair count was zero;
- exhaustive range enumeration confirmed distance strictly greater than `r`.

# Integration contract: V75 paired polynomial to remote-point counting

## Required API

For each output prefix `p` and radius cutoff `r`, expose a method

```text
count_pairs(prefix=p, max_distance=r) -> exact integer A_r(p)
```

where

```text
A_r(p) = # {(x,z): z extends p and dist(C(x),z) <= r}.
```

## Suggested polynomial specialization

At each output coordinate `i`, use a local mismatch marker `t`.

- If `i < |p|`, only the requested prefix bit is allowed; contribute `1` or
  `t` according to agreement with `C_i(x)`.
- If `i >= |p|`, sum over both target bits; contribute `1+t` locally.
- Truncate the polynomial after degree `r`.
- Sum coefficients of degree at most `r` after eliminating all circuit-input
  interfaces.

The resulting coefficient sum is exactly `A_r(p)`.

## Prefix driver

```text
p := empty
assert A_r(p) < 2^m
for ell in 0..m-1:
    a0 := A_r(p0)
    a1 := A_r(p1)
    assert a0 + a1 = A_r(p)
    choose b with ab < 2^(m-ell-1)
    p := pb
assert A_r(p) = 0
return p
```

## Audit obligations before claiming the bounded-width theorem

1. Verify that the paired V75 state already distinguishes the output value
   needed to attach the mismatch marker.
2. Verify that prefix pinning does not increase the structural width.
3. Bound coefficient bit length; counts can be as large as `2^(n+m)`.
4. Confirm that truncation at degree `r` is exact and closed under every join.
5. Run primary and independent comparison against brute force on all existing
   V75 small controls.
6. Preserve the distinction between the oracle theorem in this packet and the
   inherited V75 runtime.
