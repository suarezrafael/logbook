# V107 theorem ledger — essential signed-majority exact-stretch avoidance

## Setting

Every output is an **essential ternary signed-majority** gate

```text
MAJ(x_a XOR p_a, x_b XOR p_b, x_c XOR p_c)
```

on three distinct input variables. For pair `(i,j)` define its transport label

```text
d_ij = 1 XOR p_i XOR p_j.
```

As established in V105/V106, fixing the gate output exposes three exact binary
2-CNF clauses, and the three candidate transports XOR to one.

## Lemma 1 — polynomial Hall-circuit extraction

View the output-input support graph as a transversal matroid on the outputs: an
output set is independent exactly when it can be matched injectively to its
input neighborhood. Since `m>n`, the full output set is dependent.

Compute a maximum support matching and let `I` be its matched outputs. Choose an
unmatched output `e`. Because `I` is a basis of the transversal matroid restricted
to the full output family, the fundamental circuit is

```text
F = {e} union {f in I : I - f + e is matchable}.
```

It is computable with polynomially many bipartite-matching tests. By the
fundamental-circuit theorem, `F` is minimally dependent: every proper subset is
matchable. Hall's theorem therefore says the only violated Hall inequality in
`F` is the full one. Moreover a matching of `|F|-1` outputs exists, so

```text
|F| = |N(F)| + 1,
```

and every proper `J subset F` satisfies

```text
|N(J)| >= |J|.
```

A word missing from the restricted outputs `F` extends to a word missing from
the original circuit by filling all other output coordinates arbitrarily.

This matching construction is necessary: positive support surplus is not
monotone under inclusion, so a delete-while-the-current-set-stays-deficient
greedy rule is not valid in general. The primary verifier contains an explicit
regression where that old rule gets stuck although a four-output Hall circuit
exists.

## Lemma 2 — frame-independent pair transversal after one deletion

Fix any `g in F` and remove it. For every remaining gate expose its three
candidate signed pair edges. For every subfamily `J subset F\{g}`, the union of
all candidates has signed-frame rank

```text
r(J) = |N(J)| >= |J|.
```

The equality is V106's Hall/frame-rank bridge: every connected component of the
candidate union contains an entire unbalanced majority triangle, so no component
is balanced. Rado's theorem therefore gives one candidate pair per remaining
gate that is independent in the signed-frame matroid.

This transversal is constructible in polynomial time by ordinary unweighted
matroid intersection between

1. the partition matroid (at most one pair candidate from each gate), and
2. the signed-frame matroid.

The V107 implementation includes an explicit augmenting-path matroid-intersection
routine and a direct signed-frame independence oracle.

Let `r=|N(F)|`. The transversal has exactly `r` selected edges on exactly `r`
vertices. Since a frame-independent component is a tree or an unbalanced
unicyclic component, rank tightness implies that **every component is unbalanced
unicyclic**.

## Lemma 3 — cross-component handcuff

If two variables of the omitted gate lie in different transversal components,
choose their pair clause. The selected pair edge joins two unbalanced unicyclic
components. Their two odd cycles, together with the unique attachment paths and
the new pair edge, form a loose handcuff. The V105 implication walk therefore
constructs a contradictory 2-SAT SCC and a missing output.

Hence the only new case is when all three variables of the omitted majority gate
lie in one unbalanced-unicyclic transversal component.

## Lemma 4 — path compression/lifting

Let `B` be one connected unbalanced-unicyclic selected-pair component and let
`a,b,c` be the three variables of the omitted gate. Keep the unique cycle and
the minimal tree paths connecting `a,b,c` to that cycle; discard every other
branch. Suppress every nonterminal degree-two vertex.

Every suppressed path `P` is represented by one virtual edge whose transport is

```text
Delta(P) = XOR_{e in P} delta_e.
```

For either endpoint phase `s in {0,1}`, targets on the actual gates of `P` can
be chosen sequentially so the implication graph contains

```text
x_u=s  -> x_v=s XOR Delta(P)
```

and its contrapositive. Thus every virtual binary clause found on the reduced
kernel lifts to implication paths in the original component. Unsatisfiability
of the virtual formula implies unsatisfiability of the original selected-pair
formula.

## Lemma 5 — six-path kernel bound

The reduced three-terminal unicyclic kernel has at most **six virtual paths** and
at most six relevant vertices.

### Proof

Let `k` be the number of terminals off the cycle and let `c` be the number of
nonempty attachment trees. A reduced rooted attachment tree with `k_i`
off-cycle terminals has at most `2k_i-1` edges: every unlabeled nonterminal has
degree at least three, so there are at most `k_i-1` such branch vertices.
Summed over attachment trees this gives at most `2k-c` virtual attachment paths.

After suppressing unmarked degree-two cycle vertices, the cycle has one, two, or
three marked roots. Its virtual representation is respectively one loop, two
parallel root-to-root paths, or a triangle, so it contributes at most
`c+(3-k)` virtual paths. Therefore

```text
(2k-c) + (c+3-k) = k+3 <= 6.
```

The same counting bounds the relevant kernel vertices by six.

## Lemma 6 — exact reduced-kernel contradiction

For every reduced kernel allowed by Lemma 5, for every assignment of transport
parities whose unique cycle is unbalanced, and for every one of the eight
signed-majority polarities on the three terminals, there exist

1. one phase bit for every virtual path, and
2. one output target bit for the omitted majority gate,

such that the resulting virtual 2-CNF implication graph is unsatisfiable.

### Computer-assisted finite proof

The independent V107 verifier generates the reduced kernels from first
principles:

- one, two, or three marked cycle roots;
- every surjective assignment of the three labeled terminals to those roots;
- the possibility that at most one terminal equals each root;
- every reduced rooted tree on the remaining off-cycle terminals, generated by
  all Prüfer trees with at most `k-1` unlabeled degree-at-least-three Steiner
  vertices.

This generates 164 (not isomorphism-deduplicated) kernel descriptions. It then
enumerates every virtual-edge parity assignment with odd unique-cycle parity and
all eight missing-gate polarities. Across **16,032 exact signed/polarity cases**,
it exhausts at most `2^6 * 2 = 128` phase/target choices and finds an unsatisfiable
choice in every case.

As an independent coverage control, the same verifier directly enumerates all
connected simple unicyclic graphs on 3, 4, and 5 vertices, all unbalanced cycle
signatures, and all terminal triples (all polarities through `n=4`, normalized
polarity at `n=5`). The exact case counts are 32, 3,840, and 35,520, with zero
counterexamples.

The candidate algorithm does not rely on a stored table: it compresses its actual
component, enumerates at most 128 phase/target choices on that constant kernel,
checks SCC unsatisfiability, then lifts the chosen phases to the original paths.

## Theorem 7 — essential signed-majority `NC0_3-Avoid` is in P at exact stretch

For every explicit circuit

```text
C : {0,1}^n -> {0,1}^m,  m>n,
```

whose outputs are essential ternary signed-majority gates, a missing output word
can be constructed deterministically in polynomial time.

### Proof

1. Extract a fundamental Hall circuit `F` of the output-support transversal
   matroid (Lemma 1).
2. Omit one gate `g` and construct a frame-independent one-pair transversal for
   `F\{g}` by matroid intersection (Lemma 2).
3. If the variables of `g` meet different transversal components, use the
   cross-component odd handcuff (Lemma 3).
4. Otherwise compress their common unbalanced-unicyclic component to the
   constant three-terminal kernel (Lemmas 4 and 5), find an unsatisfiable kernel
   target by the exhaustive constant search guaranteed by Lemma 6, and lift it.
5. Every selected binary clause is an exact clause of the corresponding fixed
   majority output. The two unused clauses from each majority gate only add
   constraints and therefore cannot restore satisfiability. Hence the chosen
   output pattern on `F` has no preimage.
6. Extend it arbitrarily outside `F`.

All stages are polynomial: maximum matching and fundamental-circuit extraction
are polynomial, matroid intersection uses polynomial independence oracles, the
graph reductions are linear/polynomial, and the kernel search is constant-size.

## Scientific consequence and boundary

If externally validated, Theorem 7 improves the currently calibrated published
majority special case from quadratic stretch to exact positive stretch for the
**essential ternary signed-majority orbit**. It does **not** solve general
`NC0_3-Avoid`: the other V101 anchor-free orbit, MUX/bijunctive `0x1b`, remains
unrestricted. It does not establish a new general circuit lower bound and does
not resolve P versus NP.

Novelty is not confirmed. The proof uses standard transversal matroids,
Rado/matroid intersection, signed-frame matroids, 2-SAT SCCs, and a
new-to-this-laboratory constant-kernel composition that requires external
specialist review.
