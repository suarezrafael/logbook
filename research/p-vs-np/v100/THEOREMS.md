# Laboratory V100 — literal-substitution peeling

## 1. Literal-graph fibers

Let

```text
C : {0,1}^n -> {0,1}^m,  m>n,
```

be an explicit `NC0_3` circuit after essential-support normalization.

### Definition 1.1

An essential ternary output `g_e` has a **literal-graph fiber** if there are a
target bit `b` and either

```text
(A) a variable v and bit a with
    g_e(x)=b  =>  x_v=a,
```

or distinct variables `u,v` and a bit `c` with

```text
(B) g_e(x)=b  =>  x_v=x_u XOR c.
```

Call such an output **peelable**.

These are exactly fibers contained in the graph of a unary Boolean literal or
constant. The condition is invariant under input permutations, input
complements, and output complement.

## 2. Safe relaxation

### Lemma 2.1 — constant peel

Suppose `g_e=b` implies `x_v=a`. Delete output `e`, fix `x_v=a` in every
remaining gate, delete input `v`, and normalize essential supports. Let the
resulting circuit be `D`.

If `z` is outside `Range(D)`, then inserting target bit `b` at coordinate `e`
gives a word outside `Range(C)`.

**Proof.** Any input realizing the lifted target in `C` satisfies `g_e=b`, hence
must have `x_v=a`. Forgetting output `e` therefore gives an assignment of the
restricted variables whose surviving outputs are exactly `z`, contradicting
`z notin Range(D)`. QED.

### Lemma 2.2 — literal-substitution peel

Suppose `g_e=b` implies

```text
x_v=x_u XOR c.
```

Delete output `e`, substitute `x_v=x_u XOR c` into every remaining gate, delete
input `v`, and normalize essential supports. Again, any word outside the
resulting circuit lifts by inserting `b` to a word outside `Range(C)`.

**Proof.** Every realization of the lifted target satisfies the displayed
relation, so after eliminating `x_v` it induces an input of the substituted
circuit with the surviving target word. Contradiction. QED.

The reduction is intentionally a **relaxation**: after extracting the forced
literal relation, it does not retain the rest of the constraint `g_e=b`.
Relaxing the residual range can only make a missing residual word stronger for
lifting purposes.

### Lemma 2.3 — locality and surplus are preserved

Each peel removes exactly one input and one output, so

```text
(m-1)-(n-1)=m-n>0.
```

A constant substitution can only decrease locality. A substitution
`x_v=x_u XOR c` replaces occurrence of `v` by a literal on `u`; a support of
size at most three therefore remains of size at most three, and drops in size
when `u` was already present. Thus every residual circuit is still `NC0_3`.
QED.

## 3. General preprocessor

### Theorem 3.1 — literal-substitution kernelization

There is a deterministic polynomial-time preprocessing algorithm for arbitrary
`NC0_3-Avoid` that repeatedly applies Lemma 2.1 or Lemma 2.2 to the first active
peelable essential ternary output.

It returns a residual positive-surplus `NC0_3` circuit with no peelable
essential ternary output, together with a polynomial-time lifting map from any
residual missing word to an original missing word.

**Proof.** Each step is recognized from a constant-size truth table, removes one
active input, and preserves the two invariants in Lemma 2.3. Hence at most `n`
steps occur. Composition of Lemmas 2.1 and 2.2 gives the lifting map. QED.

## 4. Exact ternary NPN classification

Literal-graph peelability is NPN-invariant. Exhausting the 256 constant-size
ternary truth tables gives 218 essential tables in ten NPN orbits. Exactly five
orbits are peelable:

```text
canonical   orbit size   representative forced relation
--------------------------------------------------------
0x01           16        target 1 fixes a coordinate
0x06           24        target 1 fixes a coordinate
0x07           48        target 1 fixes a coordinate
0x18            8        target 1 forces x_0=x_1
0x19           48        target 1 forces x_0=x_1
--------------------------------------------------------
               144
```

The nonpeelable residual orbits are

```text
0x16 (16), 0x17 (8), 0x1b (24), 0x1e (24), 0x69 (2),
```

for 74 tables total.

The census is an exact constant-universe classification of which local truth
tables satisfy Definition 1.1; the range-avoidance theorem itself is symbolic
and does not rely on extrapolating a finite circuit census.

## 5. Polynomial-time five-orbit class

### Theorem 5.1

Suppose every essential arity-three output in the initial circuit belongs to
one of

```text
0x01, 0x06, 0x07, 0x18, 0x19
```

under NPN equivalence. Then deterministic range avoidance is polynomial time
for every `m>n`.

**Proof.** Apply Theorem 3.1. If a substitution touches another ternary gate and
the keeper variable was not already in its support, the operation is only an
input rename/complement for that local truth table, so its NPN orbit is
unchanged. If the keeper was already present, its essential arity drops below
three. Constant substitution also drops arity whenever it touches a gate.
Therefore every surviving essential ternary gate remains in one of the five
peelable orbits and will eventually be removed.

The residual circuit has locality at most two and still has positive surplus.
Guruswami, Lyu, and Wang (APPROX/RANDOM 2022) give a deterministic
polynomial-time algorithm for `NC0_2-Avoid` when `m>n`. Apply that algorithm and
reverse the V100 peel records using Lemmas 2.1 and 2.2. QED.

### Corollary 5.2 — the V99 middle unate orbit closes

Every circuit whose essential ternary outputs lie in the 48-table `0x07` NPN
orbit admits deterministic polynomial-time range avoidance for `m>n`.

This resolves the V99/V100 target without requiring a target-selectable 2-SAT
contradiction theorem.

### Corollary 5.3 — all non-MAJ essential unate ternary labels

The essential ternary unate NPN orbits are `0x01`, `0x07`, and `0x17` (signed
`MAJ_3`). Therefore V100 gives deterministic polynomial-time avoidance for
arbitrary mixtures of the two non-MAJ unate orbits `0x01` and `0x07`, together
with arbitrary lower-locality outputs. The only essential ternary unate orbit
not covered by V100 peeling is signed `MAJ_3`.

### Corollary 5.4 — genuine non-unate extension

The theorem also covers all circuits built from the non-unate essential
ternary orbits `0x06`, `0x18`, and `0x19` (and arbitrary lower-locality outputs).
Thus the result is not only an unate switching theorem.

## 6. Strict pair-substitution family

### Theorem 6.1

For every `N>=5` there is a connected exact-stretch non-unate circuit with

```text
N inputs,
N+1 outputs,
V97 lambda=N,
```

whose ternary gates have **no constant-forcing fiber** but are solved by V100
literal substitution.

**Construction.** Put the canonical truth table `0x19` on cyclic supports

```text
(i,i+1,i+2) mod N
```

and duplicate the first support. The gate is essential in all three inputs,
non-unate, and its target-one fiber forces equality of its first two local
inputs, while neither fiber fixes an individual coordinate.

The support component is connected and every input has degree at least three,
so no V97 unused/leaf/unary/constant reduction applies and `lambda=N`. V98 is
inapplicable because the gates are non-unate. Theorem 5.1 nevertheless gives a
polynomial avoider. QED.

## 7. Relationship to the V56--V62 bijunctive barrier

The `0x07` orbit was previously used to prove that consistent selected 2-CNF
fibers at stretch one need not contain a redundant complete gate block, with an
infinite direct-sum family.

V100 does not contradict that theorem. Block redundancy asks whether one full
selected fiber follows from the others. Literal peeling instead selects one
fiber, extracts a single forced literal relation, and discards the rest of the
fiber before solving a larger residual range. The earlier irredundancy
certificate therefore does not obstruct V100.

## 8. Literature boundary

Kuntewar--Sarma's Theorem 22 reduces monotone `NC0_3-Avoid` to `MAJ3-Avoid` by
selecting outputs of non-MAJ monotone gates, fixing one or more forced input
values, and deleting an output together with inputs. V100 abstracts the same
safe-relaxation pattern to arbitrary local truth tables with a literal-graph
fiber, including nonmonotone NPN orbits. The exact prior-art status of this
abstraction is unresolved and no novelty claim is made.

The final residual call uses the published deterministic polynomial-time
`NC0_2-Avoid` algorithm of Guruswami--Lyu--Wang.

## 9. Nonclaims

V100 leaves five essential ternary NPN orbits after preprocessing. In
particular, it does not solve arbitrary signed-majority circuits, unrestricted
`NC0_3-Avoid`, improve the Huang--Li--Zhong unrestricted worst-case bound, or
resolve P versus NP.
