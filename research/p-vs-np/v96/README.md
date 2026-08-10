# Laboratory V96 — universal hitlist compression and surplus-component avoidance

V96 follows the V95 stop rule: it does not try to reproduce the exact V92
canonical word.  Instead it studies alternative candidate outputs and structural
certificates that expose a missing word without exact child comparison.

## Main compression result

The list-size question is information-theoretically easy even at exact stretch
`M=N+1`:

- for a fixed ordered locality-three support pattern `S`, a universal list of
  size `1 + sum_i 2^{|S_i|} <= 8(N+1)+1` exists;
- one list depending only on `N` and universal for **all** stretch-one `NC0_3`
  circuits exists with size `O(N log N)`;
- no constant circuit-oblivious list can work: every list of at most
  `3 floor(log_2(N/3))` targets can be embedded in the range of a monotone
  3-local OR circuit;
- when all outputs share one fixed input triple, the exact universal-list number
  is `9`.

The two general upper bounds are existential/nonuniform.  They do **not** give
the constructive polynomial-time list required to solve unrestricted range
avoidance.

## Constructive comparison-free branch

Form the bipartite support-incidence graph between inputs and outputs.  For a
component `K`, write `n_K` and `m_K` for its input/output counts.  Since

```text
sum_K (m_K-n_K)=1,
```

some component has positive surplus `m_K>n_K`.  Define

```text
rho(C)=min {n_K : m_K>n_K}.
```

Enumerating only the `2^rho` assignments of such a component constructs its
local range.  Because it has more output bits than input bits, one of the first
`2^rho+1` local candidate words is absent; extending that local absence
arbitrarily to the other outputs gives a global avoided word.  Therefore V96
obtains a deterministic comparison-free algorithm with runtime

```text
O(2^rho * poly(N)).
```

It is polynomial whenever `rho=O(log N)`.  This is a real constructive control,
but not an all-instance polynomial-time algorithm because `rho` may be linear.

## Uniformization barrier

If a polynomial-size support-conditioned universal list could be generated in
`FP^NP` for arbitrary support patterns, then testing each candidate with the NP
predicate

```text
exists x : C(x)=y
```

would put `NC0_3-Avoid[N,N+1]` in `FP^NP`.  Minimal stretch then transfers to
all larger stretches by output truncation.  This calibrates the missing
uniformization step against the published `NC0_3-Avoid` lower-bound-transfer
frontier rather than pretending that the nonuniform existence theorem is an
algorithm.

The new component theorem narrows that missing bridge further: only support
instances whose positive-surplus components are all superlogarithmic remain
outside this constructive branch.

## Executable audit

- `hitlist_compression.py` checks the counting formulas and constructs monotone-OR
  shattering witnesses for 80 deterministic cases over `N=6,12,24,48,96`,
  embedding 720 target rows with zero failures;
- the same module checks 32 eight-target embeddings for the fixed-common-triple
  control;
- `component_avoidance.py` checks 56 partitioned support circuits over
  `N=4,...,10`, with 16,256 brute-force input evaluations and zero absent-word
  failures;
- `verify_independent.py` recreates the OR and surplus-component constructions
  without importing either V96 implementation module.

The finite audits are regression evidence only.  The asymptotic claims are
proved symbolically in `THEOREMS.md`, `SURPLUS_COMPONENT_THEOREM.md`, and the
formal LaTeX modules.

## Status

V96 is a **barrier-and-closure with a constructive restricted branch**:
polynomial candidate-list cardinality is closed as the primary obstacle, and
small positive-surplus components are solved comparison-free.  The surviving
hard support regime is a large positive-surplus connected component requiring
uniform extraction, separators, or a new certificate mechanism.

No P-versus-NP resolution, no unrestricted polynomial-time avoider, and no
worst-case Huang--Li--Zhong runtime improvement are claimed.
