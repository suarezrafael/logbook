# Laboratory V96 — universal hitlist compression

V96 follows the V95 stop rule: it does not try to reproduce the exact V92
canonical word.  Instead it studies whether a polynomial list of alternative
candidate outputs can be guaranteed to contain a missing word.

## Main result

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

The upper bounds are existential/nonuniform.  They do **not** give the
constructive polynomial-time list required to solve range avoidance.

## Uniformization barrier

If a polynomial-size support-conditioned universal list could be generated in
`FP^NP`, then testing each candidate with the NP predicate

```text
exists x : C(x)=y
```

would put `NC0_3-Avoid[N,N+1]` in `FP^NP`.  Minimal stretch then transfers to
all larger stretches by output truncation.  This calibrates the missing
uniformization step against the published `NC0_3-Avoid` lower-bound-transfer
frontier rather than pretending that the nonuniform existence theorem is an
algorithm.

## Executable audit

`hitlist_compression.py` checks the exact counting formulas and independently
constructs the monotone-OR shattering witnesses for 80 deterministic cases over
`N=6,12,24,48,96`, embedding 720 target rows with zero failures.  It also checks
32 eight-target embeddings for the fixed-common-triple control.

The finite audit is regression evidence only.  The asymptotic claims are proved
symbolically in `THEOREMS.md` and the LaTeX module.

## Status

V96 is a **barrier-and-closure** candidate: it closes candidate-list cardinality
as the primary bottleneck, but leaves polynomial-time uniform construction open.
No P-versus-NP resolution, no unrestricted polynomial-time avoider, and no
Huang--Li--Zhong runtime improvement are claimed.
