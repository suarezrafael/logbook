# Laboratory V84 — FP^NP girth extraction and Hall-expander promise reduction

V84 turns the V83 hardness theorem into an exact oracle interface for
`NC0_3-Avoid`. It closes the extraction machinery but deliberately does not
claim an unrestricted avoidance algorithm.

## Main theorem

Let `B=(M,X;E)` be the support presentation of an `NC0_3` circuit, with
`m=|M|`, and let

```text
D3-TRANSVERSAL-GIRTH(B,L)
```

ask whether the transversal matroid presented by `B` has a circuit of size at
most `L`.

A deterministic polynomial-time machine with this NP oracle computes:

1. the exact girth `g` using `ceil(log2 m)` queries when dependence is
   guaranteed (`m>|X|`), and one additional existence query otherwise;
2. a canonical shortest circuit using at most `m` deletion queries;
3. its neighborhood `N(C)`, which has size `g-1` and attains the exact minimum
   Hall-neighborhood value `h*=g-1`.

Deletion only removes left elements, so every oracle query preserves the
left-degree-three promise.

## Canonical deletion theorem

Fix an order on the output gates. Starting from all gates, process each gate
once and delete it whenever the oracle says that girth at most `g` remains.
Deletion cannot create a shorter circuit, so every accepted deletion preserves
girth exactly.

At termination, deleting any remaining gate destroys every shortest circuit.
Therefore every remaining gate belongs to every shortest circuit of the final
restriction. Since a shortest circuit is itself contained in the remaining
set, the remaining set is that unique circuit. The fixed order makes the
output canonical.

## Short-circuit avoidance

For a shortest circuit `C`, transversal minimality gives

```text
|N(C)| = |C|-1.
```

The local map on the gates in `C` therefore has at most
`2^(|C|-1)` possible outputs inside a cube of size `2^|C|`. Enumerate all
assignments to `N(C)`, choose the lexicographically first missing projection,
and set all output coordinates outside `C` to zero. The resulting global
string is outside the range of the original circuit.

Consequently, for any fixed constant `c`, the branch

```text
g <= c log2(n+m)
```

is solvable deterministically after the oracle extraction, in overall
`FP^NP` time.

## Hard branch

The theorem is parameterized by a threshold `L`:

- if `g<=L`, local enumeration costs `2^(g-1) poly(n+m)` and returns an avoided
  output;
- if `g>L`, every output set `S` of size at most `L` satisfies
  `|N(S)|>=|S|`.

Thus V84 is an `FP^NP` preprocessing dichotomy, or promise reduction, from
unrestricted degree-three avoidance to the `L`-Hall-expanding branch. It is
not a many-one reduction and it does not solve the large-girth branch. Taking
`L=c log(n+m)` gives a polynomial short-circuit arm and isolates the
logarithmic Hall-expander obstruction. The stronger V80 obstruction families,
which have no small deficient set up to much larger scales, lie inside this
hard branch.

## Exact finite audit

The committed census checks:

- 832 degree-at-most-three presentations;
- 7,872 nonempty subset states;
- 3,961 simulated oracle queries;
- 585 canonical shortest circuits and Hall witnesses;
- 272 complete Boolean truth-table combinations for local enumeration and
  global lift;
- path-circuit controls of girth 4, 6, 8, and 10.

## Literature boundary

Gajulapalli, Golovnev, Nagargoje, and Saraogi show that an `FP^NP` algorithm for
`NC0_3-Avoid` at `m=n+n^(2/3)` would yield explicit rigid matrices and
superlinear lower bounds for log-depth circuits. Guruswami, Lyu, and Yuan give
a deterministic polynomial-time algorithm when
`m >= c_t n^((t-1)/2) log n`; for `t=3`, this is the regime `m >= c n log n`.
Ren, Santhanam, and Wang show that even polynomial-stretch `AC0-Avoid` would
imply lower bounds against `NC1`.

The live interval is therefore not described as a route to `P != NP`. V84
only isolates a structural promise inside the still-hard range.

## Files

- `GIRTH_EXTRACTION_AND_HALL_PROMISE_REDUCTION.md` — full theorem and proofs;
- `V84_FP_NP_EXTRACTION_THEOREM.tex` — standalone formal module;
- `oracle_extraction.py` — exact algorithms and finite support/local-circuit
  machinery;
- `build_results.py` and `RESULTS.json` — deterministic evidence generator and
  immutable snapshot;
- `verify.py` and `verify_independent.py` — primary and independent read-only
  checks;
- `V85_CORE_CONTEXT.md` — next target for the Hall-expanding branch.

## Nonclaims

V84 does not solve unrestricted `NC0_3-Avoid`, does not produce the missing
large-girth candidate list, does not prove matrix rigidity or a circuit lower
bound, does not activate a direct route to `P != NP`, and does not claim
novelty or peer review.
