# Laboratory V96 — universal hitlist compression and the uniformization barrier

## 1. Object under study

Let

```text
C:{0,1}^N -> {0,1}^{N+1}
```

be an `NC0_3` circuit: every output depends on at most three input coordinates.
A **universal candidate list** for a family `F` of such circuits is a set

```text
H subset {0,1}^{N+1}
```

such that for every `C in F`, at least one `y in H` is absent from `Range(C)`.
Equivalently, `H` is never contained in the range of a member of `F`.

The word *universal* is important.  The list is allowed to depend on the family
being considered, but not on the individual truth tables of the circuit whose
missing output will later be requested.

V96 separates three questions:

1. how small such a list can be information-theoretically;
2. whether it can be constructed uniformly from the support pattern or from `N`;
3. whether a constructive list yields an actual range-avoidance algorithm.

Only (1) is closed in general here.  V96 does **not** supply the uniform
polynomial-time constructor required by (2).

## 2. The half-range fact

For every stretch-one circuit,

```text
|Range(C)| <= 2^N = 2^(N+1)/2.
```

Therefore a uniformly random output word belongs to `Range(C)` with probability
at most `1/2`.  This elementary density bound drives both universal-list upper
bounds below.

## 3. Support-conditioned linear-size existence theorem

Fix an ordered support pattern

```text
S=(S_0,...,S_N),    |S_i|<=3.
```

Let `F(S)` contain every circuit whose `i`-th output is an arbitrary Boolean
truth table on the listed coordinates `S_i`.  Put

```text
B(S)=sum_i 2^{|S_i|}.
```

### Lemma 3.1 — family-size bound

```text
|F(S)| <= 2^{B(S)}.
```

**Proof.**  A gate on support `S_i` has at most `2^{2^{|S_i|}}` truth tables.
Multiplying over the ordered outputs gives

```text
prod_i 2^{2^{|S_i|}} = 2^{sum_i 2^{|S_i|}}.
```

Allowing a truth table to ignore some listed coordinates can only overcount
representations, which is harmless. QED.

### Theorem 3.2 — support-conditioned universal list

For every ordered support pattern `S`, there exists a universal candidate list
for `F(S)` of size at most

```text
B(S)+1 <= 8(N+1)+1.
```

**Proof.**  Sample `L=B(S)+1` output words independently and uniformly.  For one
fixed circuit `C`, the half-range fact gives

```text
Pr[all L sampled words lie in Range(C)] <= 2^{-L}.
```

Union-bound over at most `2^{B(S)}` circuits:

```text
Pr[some C contains every sampled word]
 <= 2^{B(S)} 2^{-(B(S)+1)}
 = 1/2 < 1.
```

Hence a successful sample exists.  Removing duplicate sampled words preserves
the existence of an absent member, so a set of at most `L` words suffices. QED.

### Scope

The theorem is **nonuniform/existential**.  It does not provide a polynomial-time
algorithm that, given `S`, finds the successful sample.  In particular, it does
not solve Track B of the V96 contract.

## 4. Circuit-oblivious `O(N log N)` existence theorem

For one output coordinate, overcount all representations by choosing a support
of size `j<=3` and then an arbitrary truth table on that support:

```text
Q_N = sum_{j=0}^3 binom(N,j) 2^{2^j}.
```

Thus the number of represented `N -> N+1` circuits is at most

```text
Q_N^{N+1}.
```

### Theorem 4.1 — one list depending only on `N`

There exists a candidate list `H_N`, depending only on `N`, universal for every
stretch-one `NC0_3` circuit, with

```text
|H_N| <= (N+1) ceil(log_2 Q_N)+1 = O(N log N).
```

**Proof.**  Sample

```text
L=(N+1) ceil(log_2 Q_N)+1
```

uniform words.  For any fixed circuit the probability that all sampled words
lie in its range is at most `2^{-L}`.  Union-bound over at most `Q_N^{N+1}`
representations.  Since

```text
Q_N^{N+1} <= 2^{(N+1) ceil(log_2 Q_N)},
```

the failure probability is at most `1/2`. QED.

### Corollary 4.2 — nonuniform algorithmic interpretation

The list `H_N` can be supplied as polynomial advice: it contains `O(N log N)`
words of length `N+1`, or `O(N^2 log N)` advice bits.  With an NP oracle for the
predicate

```text
exists x : C(x)=y,
```

one can test the advised candidates and output the first absent one.  Thus the
existence theorem gives only a nonuniform `FP^NP/poly`-type consequence.  It is
not a uniform `FP^NP` algorithm.

## 5. Explicit logarithmic lower bound for circuit-oblivious lists

The preceding upper bound leaves open whether a constant universal list might
exist.  V96 rules this out, already for a very simple monotone subclass.

Let

```text
r=floor(log_2(N/3)),
t=3r,
```

for `N>=6`.

### Theorem 5.1 — arbitrary `t` targets can be embedded

Every collection of at most `t` words in `{0,1}^{N+1}` is contained in the
range of some circuit all of whose outputs are monotone ORs of three input
coordinates.

**Proof.**  Pad the target collection by repetitions until it has exactly `t`
rows.  Split the rows into three blocks of `r` rows.

For each block `b in {1,2,3}` and each pattern `u in {0,1}^r`, allocate an input
coordinate `x_{b,u}`.  This uses

```text
3*2^r <= N
```

inputs; any remaining inputs are unused.

For output coordinate `i`, let `u_{i,b}` be the `r`-bit column pattern formed by
restricting target column `i` to row block `b`.  Define

```text
C_i = OR(x_{1,u_{i,1}}, x_{2,u_{i,2}}, x_{3,u_{i,3}}).
```

Consider target row `(b,p)`, where `p` is its position in block `b`.  Its witness
input sets all variables outside block `b` to zero and, inside block `b`, sets

```text
x_{b,u}=u_p
```

for every pattern `u`.  On output coordinate `i`, only the selected variable
from block `b` can be one, and its value is exactly the desired bit
`(u_{i,b})_p`.  Hence every output coordinate equals target row `(b,p)`.
Therefore every target word is in the range. QED.

### Corollary 5.2 — logarithmic lower bound

Every circuit-oblivious universal candidate list has size at least

```text
3 floor(log_2(N/3))+1 = Omega(log N).
```

This lower bound is representation-independent and already holds against
monotone 3-local OR circuits.

## 6. Exact fixed-support control: the answer is nine

Suppose every output uses the same fixed three input coordinates.

### Theorem 6.1

The minimum size of a universal candidate list for this support pattern is
exactly `9`.

**Upper bound.**  The entire circuit depends on only three bits, so its range has
size at most `8`.  Any nine distinct output words therefore contain an absent
word.

**Lower bound.**  Take any at most eight target words.  Assign the distinct
target words to distinct three-bit input assignments.  For every output
coordinate, define its 3-bit truth table to equal the corresponding target
column on those assigned inputs.  The resulting circuit contains every target
word in its range. QED.

This exact control confirms that support information can reduce the required
universal-list size from the general `O(N log N)` counting bound to a constant.
The hard part is to exploit arbitrary support patterns uniformly.

## 7. Uniformization transfer

### Theorem 7.1 — support-list constructor implies `FP^NP` avoidance

Assume there is an `FP^NP` algorithm which, given any ordered locality-three
support pattern `S`, outputs a polynomial-size universal list for `F(S)`.  Then

```text
NC0_3-Avoid[N,N+1] is in FP^NP.
```

**Proof.**  Given the actual circuit `C`, read its support pattern `S`, construct
the universal list, and for every listed word `y` ask the NP question

```text
exists x : C(x)=y ?
```

Universality guarantees at least one NO answer.  Return the first such `y`.
All calls fit inside one `FP^NP` computation. QED.

The same conclusion follows from a uniform `FP^NP` construction of the
circuit-oblivious `H_N`.

### Lemma 7.2 — minimal stretch transfers upward by truncation

An algorithm for `N -> N+1` range avoidance solves every larger stretch `M>N`:
truncate the circuit to any `N+1` output coordinates, find an absent prefix, and
extend that prefix arbitrarily to `M` bits.  No full output can realize the
extension because its selected projection would realize the absent prefix.

Consequently a uniform `FP^NP` solution at minimal stretch would also solve the
larger-stretch regimes used in published lower-bound transfers.

## 8. Deterministic but expensive existence search

The probabilistic upper bounds can be made uniform without becoming efficient.
Enumerate every circuit in the relevant finite family.  At each round choose an
output word lying in the ranges of at most half the still-uncovered circuits;
such a word exists by averaging the half-range fact.  Remove all circuits that
do not contain the chosen word.  After logarithmically many rounds no circuit
remains uncovered.

For a fixed support pattern this exhaustive procedure is exponential in `N`;
for the circuit-oblivious family it is `2^{O(N log N)}` or worse under direct
representation enumeration.  The procedure is included only to distinguish
**existence** from **efficient uniformization**.

## 9. What V96 closes

V96 closes the hypothesis that polynomial candidate-list **cardinality** is the
main obstacle at stretch one:

```text
support known:       <= 8(N+1)+1 candidates exist,
only N known:        O(N log N) candidates exist,
universal lower:     Omega(log N) candidates are sometimes necessary.
```

The remaining bridge is algorithmic: select such candidates uniformly from a
support pattern, or bypass universal lists with a certificate-triggered policy.

## 10. Nonclaims

V96 does not construct the general universal list in polynomial time, does not
put unrestricted `NC0_3-Avoid[N,N+1]` in `FP^NP` or `P`, does not improve the
Huang--Li--Zhong `O(N*2^(N/2))` bound for `k=3`, does not establish a new circuit
lower bound, does not establish novelty or peer review, and does not resolve
P versus NP.
