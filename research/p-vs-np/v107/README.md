# V107 — essential signed-majority exact-stretch avoidance

V107 replaces V106's bounded pair-repair enumeration by a global construction
for circuits whose outputs are essential ternary signed-majority gates.

## Candidate theorem

For

```text
C : {0,1}^n -> {0,1}^m,  m>n,
```

if every output is an essential gate

```text
MAJ(x_a XOR p_a, x_b XOR p_b, x_c XOR p_c)
```

on three distinct input coordinates, V107 constructs a missing output in
deterministic polynomial time.

## Construction

1. Extract an inclusion-minimal positive-surplus output block `F`.  It has
   `|F|=|N(F)|+1`, and every proper subfamily satisfies Hall.
2. Omit one gate `g` from `F`.
3. Use V106's Hall/frame-rank identity plus ordinary matroid intersection to
   select one signed pair edge from every gate of `F\{g}` while remaining
   independent in the signed-frame matroid.
4. Rank tightness implies that every selected component is unbalanced
   unicyclic.
5. If two variables of `g` lie in different components, one pair of `g`
   directly joins two odd cycles, producing the V105 handcuff certificate.
6. Otherwise all three variables of `g` lie in one unbalanced-unicyclic
   component.  Keep the unique odd cycle plus the minimal attachment forest for
   those three terminals and suppress degree-two nonterminals.
7. The resulting kernel has at most six virtual paths.  Exhaust at most
   `2^6 * 2 = 128` virtual path phases / missing-gate targets, test the resulting
   2-SAT formula by SCC, and lift the successful virtual implications along the
   original paths.

## Computer-assisted finite lemma

The independent verifier generates every reduced three-terminal unicyclic
kernel allowed by the proof, not a stored hand-written table.  There are 164
kernel descriptions.  Across all edge-parity assignments with unbalanced unique
cycle and all eight signed-majority polarities, the verifier checks 16,032 exact
kernel instances.  Every instance has an unsatisfiable phase/target choice.

As a separately generated control, it directly enumerates all connected simple
unicyclic graphs at the first sizes and checks 32, 3,840, and 35,520 additional
cases at `n=3,4,5` respectively.

## Constructive algorithm verifier

The primary verifier calls the actual V107 implementation, including the
matroid-intersection routine, minimal-surplus extraction, graph compression,
kernel SCC search, and implication lifting.  It compares the produced word
against the complete original circuit range on an exhaustive `n=3` family and
on random exact/small-stretch circuits through `n=7`.

## Scientific boundary

V107 is restricted to the essential ternary signed-majority predicate orbit.
It does not solve arbitrary `NC0_3-Avoid`; in the V101 anchor-free frontier the
MUX/bijunctive `0x1b` orbit remains unrestricted.  No new general circuit lower
bound or P-versus-NP consequence is claimed.

The literature calibration used by the laboratory currently places the known
majority special case at substantially larger stretch, while monotone `NC0_3`
is known at exact positive stretch.  External specialist review is mandatory
before any novelty or priority statement about V107.
