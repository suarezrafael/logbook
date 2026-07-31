# Affine-cover frontier after V56

## Solved affine-orientable classes

The 256 ternary truth tables form 14 NPN classes. Eight classes have an affine output orientation. The four essential classes are:

| Mask | Selected affine fiber | Status |
|---|---|---|
| `0x01` | singleton | solved at `m>n` |
| `0x06` | distance-two pair | solved at `m>n` |
| `0x18` | antipodal pair | solved at `m>n` |
| `0x69` | affine parity plane | solved at `m>n` |

The lower-arity affine classes are `0x00`, `0x03`, `0x0f`, and `0x3c`.

## Six essential non-affine classes

| Mask | Fiber sizes | Minimum affine partition | Both fibers bijunctive? |
|---|---|---|---|
| `0x07` | 5 / 3 | 2 / 2 | yes |
| `0x16` | 5 / 3 | 2 / 2 | no |
| `0x17` | 4 / 4 | 2 / 2 | yes |
| `0x19` | 5 / 3 | 2 / 2 | no; one side is bijunctive |
| `0x1b` | 4 / 4 | 2 / 2 | yes |
| `0x1e` | 4 / 4 | 2 / 2 | no |

Every fiber is the disjoint union of exactly two affine cells. This does not itself yield an algorithm because activating the output means satisfying a disjunction of affine states, whereas V56 handles conjunctions of affine equations.

## Bijunctive route

The fibers of `0x07`, `0x17`, and `0x1b` are closed under majority and admit 2-CNF descriptions. They are the first V57 targets:

```text
output state
  -> 2-CNF relation
  -> implication graph / SCC certificate
  -> block forcing or contradiction
```

`0x17` is the signed-majority orbit and reconnects with the earlier MAJ3 motif laboratories.

## Non-bijunctive route

The classes `0x16`, `0x19`, and `0x1e` require state systems beyond one affine relation or a 2-CNF description on both fibers. Candidate tools include two-cell affine disjunctions, bounded-state automata, polymorphism-sensitive decompositions, hitting sets, and Turán/loose-cycle certificates.

## Projection impossibility

A projection of an affine subspace is affine. Therefore hidden variables cannot compile a non-affine fiber into one larger affine block. A genuine branch or disjunction is unavoidable for this route.
