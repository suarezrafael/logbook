# V91 theorem calibration — CHR, Li, and Vyas–Williams

## Parameter dictionary

The papers switch between a succinct circuit input length `n` and an explicit Missing-String list length often denoted `N=2^n`. A circuit size written as `2^{poly(n)}` can therefore be quasipolynomial in the explicit parameter `N`. V91 records both views and does not translate “quasipolynomial” without stating the active parameter.

## Checked theorem table

| Source | Exact checked statement used by V91 | Length regime | Output/model | V91 status |
|---|---|---:|---|---|
| Chen–Hirahara–Ren 2023, Theorem 1.5 | For every constant size exponent, a randomized NP-oracle algorithm finds the paper's canonical string outside the range of an expanding circuit, or returns failure, with constant success probability | infinitely many input lengths | randomized NP-oracle; canonical output on success | historical algorithmic input; not reproduced in full |
| Chen–Hirahara–Ren 2023, Theorems 1.2–1.3 | Relativizing exponential circuit lower bounds, including a `2^n/n`-scale lower bound for the stated exponential-hierarchy classes | asymptotic | lower-bound consequence of the win-win | already established literature result |
| Li 2023, Theorem 1.1 | A single-valued `FS2P` algorithm outputs a string outside `Im(C)` for every expanding circuit `C:{0,1}^n->{0,1}^{n+1}` | every input length | single-valued search | decisive all-length improvement |
| Li 2023, Theorem 1.2 and Corollaries 1.3–1.4 | `S2E` is not contained in `i.o.-SIZE[2^n/n]`, with the stated consequences for `ZPE^NP` and `Sigma2E intersect Pi2E` | almost-everywhere lower-bound form | relativizing | already established literature result |
| Vyas–Williams theorem quoted as Li Theorem 1.7 plus Li Corollary 1.8 | The relativized lower-bound condition is equivalent to uniform bounded-depth circuits for Missing-String; Li's all-length lower bound supplies uniform depth-three AC0 circuits of quasipolynomial size in the explicit-list parameter | every relevant length after Li | uniform depth 3 | the natural Track-B target selected in V90 is closed |
| Vyas–Williams ECCC TR24-113, Theorems 1.5–1.6 | Generic Missing-String/lower-bound equivalences require exact depth, uniformity, list length, circuit size, and oracle quantifiers | theorem-specific | uniform circuit transfer | usable only after filling every parameter |
| Vyas–Williams ECCC TR24-113, Theorem 1.10 | The conference statement is incorrect; the appended erratum proves its negation | not applicable | oracle barrier claim | forbidden as a premise |

Notation above follows the source papers; ASCII spellings are used where repository tooling should remain encoding-stable.

## What is closed

The following V90 target is no longer admissible as an open objective:

```text
construct uniform depth-3 AC0 circuits of quasipolynomial size
for the Missing-String problem.
```

Li obtains this as a consequence of the all-length single-valued range-avoidance result and the Vyas–Williams equivalence.

## What remains relevant to this laboratory

V91 does not claim a complete catalog of every open theorem in the area. It isolates the requirements that a successor of the inherited engine would have to satisfy:

| Requirement | Why it matters | Current engine |
|---|---|---|
| all-instance coverage | transfer theorems quantify over every circuit in the selected class | fails: low-width promise only |
| exact representation | local multi-output maps must match the transfer theorem's circuit/list encoding | unproved |
| single-valuedness or uniformity | the literature consequence depends on the exact search/circuit model | unproved |
| correct size regime | the theorem may require polynomial, `2^{n^epsilon}`, or list-dependent size | not instantiated |
| correct saving | SAT-style transfers require a quantified saving, not merely FPT behavior | not instantiated |
| barrier escape | post-2025 Missing-String communication routes face an algebrization checkpoint | no escape identified |

## Primary sources

- Chen, Hirahara, Ren, *Symmetric Exponential Time Requires Near-Maximum Circuit Size*, arXiv:2309.12912.
- Li, *Symmetric Exponential Time Requires Near-Maximum Circuit Size: Simplified, Truly Uniform*, arXiv:2310.17762; ECCC TR23-156.
- Vyas and Williams, *On Oracles and Algorithmic Methods for Proving Lower Bounds*, ECCC TR24-113, July 2024 revision with appended erratum.
