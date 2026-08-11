# Laboratory V97 — comparison-free peeling kernels

## 1. Setup

Let

```text
C:{0,1}^N -> {0,1}^{N+1}
```

be an explicit `NC0_3` circuit.  Every output truth table is normalized to its
**essential support**: an input coordinate is removed from a listed support when
flipping it never changes the output truth table.  Because every local table has
at most eight rows, this normalization is constant work per gate.

Build the bipartite support-incidence graph between inputs and outputs using
these essential supports.  For a connected component `K`, write `n_K` for its
input vertices and `m_K` for its output vertices.  As in V96,

```text
sum_K (m_K-n_K)=1,
```

so some component has positive surplus.

V97 starts from any positive-surplus component and applies only reductions that
preserve the implication

```text
missing output in the reduced circuit => missing output in the original circuit.
```

No exact child-count comparison is used.

## 2. Safe reductions

### Lemma 2.1 — unused input deletion

If an active input appears in no active output, deleting the input preserves the
range of the active output map.  The surplus `m-n` increases by one.

### Lemma 2.2 — leaf input/output pair deletion

Suppose input `x` occurs in exactly one active output `g`.  Delete both `x` and
`g`.  If `y'` is absent from the reduced output map, then extending `y'` by an
arbitrary target bit for `g` gives an output absent from the original map.

**Proof.** Every original assignment realizing the extension would, after
forgetting `x` and output `g`, realize `y'` on all surviving outputs.  But no
surviving output depends on `x`, because `x` had incidence degree one.  This
contradicts absence of `y'`.  The operation removes one input and one output, so
surplus is unchanged. QED.

### Lemma 2.3 — constant output termination

If an active output is constant, set its target bit to the opposite value and
all other still-active target bits arbitrarily.  This is immediately outside the
range.

### Lemma 2.4 — unary output forcing

Suppose an active output `g` has essential support `{x}`.  Then `g` is identity
or negation.  Choose target `g=0`; there is a unique bit `a` such that `g(a)=0`.
Delete output `g` and input `x`, substitute `x=a` into every surviving local
truth table, and normalize supports again.

If `y'` is absent from the restricted circuit, then `(g=0,y')` is absent from
the pre-restriction circuit.

**Proof.** Any assignment realizing `g=0` must have `x=a`.  Its remaining
outputs therefore equal the restricted circuit on the remaining inputs, which
cannot realize `y'`.  Again one input and one output are removed, so surplus is
unchanged. QED.

## 3. Deterministic peeling kernel

Apply the reductions in the fixed priority order

```text
constant output,
unused input,
smallest leaf input,
smallest unary output,
repeat.
```

When none applies, call the surviving active circuit the **V97 peeling kernel**.
For one starting positive-surplus component `K`, let

```text
lambda(K) = number of inputs in its peeling kernel,
```

with `lambda(K)=0` if constant-output termination occurs.  Define

```text
lambda(C) = min { lambda(K) : m_K>n_K }.
```

The deterministic tie/order convention makes `lambda(C)` executable; V97 does
not define it as an optimization over all possible reduction sequences.

### Lemma 3.1 — positive surplus survives

Unless the process terminates at a constant output, the final kernel satisfies

```text
m_* > n_* = lambda(K).
```

**Proof.** The starting component has positive surplus.  Unused-input deletion
increases surplus; leaf-pair and unary-forcing reductions preserve it.  Hence a
nonterminated residual circuit still has positive surplus. QED.

The irreducible kernel additionally has:

```text
no unused or degree-one input,
no constant output,
no essential unary output.
```

These properties are descriptive only; V97 does not claim they solve the
remaining kernel.

## 4. Main algorithm

### Theorem 4.1 — peeling-kernel avoider

Every explicit stretch-one `NC0_3` circuit has a deterministic comparison-free
avoider with running time

```text
O(2^lambda(C) * poly(N)).
```

**Proof.** Compute all positive-surplus components and their deterministic
peeling kernels, and select one minimizing `lambda`.  If a constant output was
found, use Lemma 2.3.

Otherwise enumerate all `2^lambda` assignments to the kernel inputs and record
the exact kernel output range.  By Lemma 3.1 the kernel has `m_*>lambda`
outputs, so its range has at most `2^lambda` words inside a larger output cube.
It is enough to inspect the first `2^lambda+1` lexicographic kernel words; one is
absent.

Reverse the unary and leaf reduction records, inserting the fixed target bit
chosen at each deleted output.  Lemmas 2.2 and 2.4 inductively preserve absence.
Finally fill outputs outside the selected original component with zeros.  Any
full circuit input realizing this global target would realize the absent target
on the selected component, contradiction. QED.

### Corollary 4.2 — polynomial regime

If

```text
lambda(C)=O(log N),
```

then stretch-one range avoidance is deterministic polynomial time on that
instance family.

### Corollary 4.3 — instancewise exponential improvement

Compared with the Huang--Li--Zhong `k=3` all-instance baseline

```text
O(N*2^(N/2)),
```

V97 is exponentially faster on families satisfying

```text
lambda(C) <= (1/2-epsilon)N - O(log N)
```

for any fixed `epsilon>0`.  This is an instancewise statement, not a new
worst-case bound.

## 5. Strict domination of the V96 component parameter

V96 defined

```text
rho(C)=min { n_K : m_K>n_K }.
```

### Theorem 5.1

```text
lambda(C) <= rho(C)
```

for every circuit.

**Proof.** On every candidate positive-surplus component, the V97 reductions
only delete inputs.  Its final kernel therefore has no more inputs than that
component started with.  Taking the minimum proves the claim. QED.

### Theorem 5.2 — strict separation family

For every `N>=8` there is a connected, exact-stretch, genuinely ternary,
nonmonotone circuit family with

```text
rho(C_N)=N,
lambda(C_N)=ceil(log_2 N).
```

**Construction.** Let `h=max(3,ceil(log_2 N))`.  On the first `h` inputs place
`h+1` parity-of-three outputs on cyclic triples

```text
(i, i+1, i+2) mod h.
```

This is a connected positive-surplus core with `h` inputs and `h+1` outputs.
For every remaining input `z`, add one parity-of-three output on `(x_0,x_1,z)`.
The full incidence graph is connected and has `N` inputs, `N+1` outputs, so its
only positive-surplus component has `rho=N`.

Every attachment input `z` has degree one.  Leaf-pair deletion removes all
`N-h` attachments and leaves exactly the cyclic `h`-input, `h+1`-output core.
The parity gates have essential arity three, every core input has degree at
least two, and no unary/constant reduction applies.  Hence `lambda=h`. QED.

Therefore V97 turns a family on which the V96 `2^rho` algorithm is exponential
into a polynomial-time family.

## 6. Relation to earlier laboratories and current literature

V84 already gave an `FP^NP` mechanism for extracting a small Hall-deficient set
and enumerating its local range.  V97 does **not** restate that theorem and does
not claim a new general Hall-witness extractor.  Its new internal step is a
fully deterministic support/truth-table reduction that can expose a logarithmic
kernel inside one component whose total input size is linear.

Kuntewar and Sarma (APPROX/RANDOM 2025) prove deterministic polynomial-time
range avoidance for **monotone** `NC0_3` circuits for every `m>n`, using
Turan-type hypergraph arguments and loose `X`-cycles.  V97 is orthogonal: the
strict separation family above uses parity-of-three gates, so it is neither
monotone nor an `NC0_2` family.  No novelty claim is made without external
prior-art review.

## 7. Executable audit

The primary implementation checks:

```text
240 deterministic arbitrary local circuits for N=2,...,7,
76,384 brute-force input evaluations,
0 absent-output failures,
0 lambda>rho failures,
32 unary-cascade cases,
128 executed unary-forcing steps,
0 unary-cascade failures.
```

It also checks the strict family at

```text
N=8,16,32,64,128,
lambda=3,4,5,6,7,
rho=N,
```

and brute-force validates absence for `N=8,16`.

The finite audit is implementation evidence only.  The safe-reduction and
runtime claims are the symbolic theorems above.

## 8. Nonclaims

V97 does not solve the irreducible large-kernel regime, does not put unrestricted
`NC0_3-Avoid[N,N+1]` in polynomial time, does not improve the Huang--Li--Zhong
worst-case exponent, does not activate a published lower-bound transfer, does
not establish novelty or peer review, and does not resolve P versus NP.
