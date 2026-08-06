# Targeted follow-up email template

Use only after identifying a specific paper, theorem, convention, or constant that plausibly overlaps the claim. Replace every bracketed field. Do not send a generic mass email.

## V81 version

Subject: Question about [paper/theorem] and a hypergraph branch-cut identity

Dear Professor [Surname],

I am checking whether a short hypergraph identity I derived is already covered by [paper or theorem]. Under the active-vertex convention `X=N(M)`, for a hyperedge subset `S` I define

```text
delta(S)=|S|-|N(S)|,
lambda(S)=|N(S) intersect N(M\S)|,
sigma=|M|-|X|.
```

The identity is

```text
delta(S)+delta(M\S)=sigma-lambda(S).
```

Together with a balanced edge of a supplied subcubic branch decomposition of width `w`, it gives a balanced side with deficiency at least `ceil((sigma-w)/2)`.

Does [Theorem X / definition Y] already subsume this statement, possibly under different terminology? I would be grateful for a reference or a correction to the convention or rounding. A short technical note is available at [stable preprint or public-note link].

Thank you for your time,
Rafael Suarez

## V87 version

Subject: Does [Theorem X] cover this rank-three hypergraph width transfer?

Dear Professor [Surname],

I am checking a rank-three conversion between a hyperedge-boundary branch decomposition and a tree decomposition of the primal graph.

For a rank-at-most-three hypergraph `H`, with branchwidth defined by the number of vertices incident with hyperedges on both sides of a cut, the claimed bound is

```text
tw(primal(H))+1 <= max(3, ceil(3 bw(H)/2)).
```

The construction puts in each internal decomposition-tree node the vertices whose incident hyperedges occupy at least two of the three branches. The bag-size estimate follows from double counting the three cut boundaries.

Does [Theorem X / framework Y] already imply this bound under the same convention? In particular, I am unsure whether the best integer form uses `ceil(3k/2)` or `floor(3k/2)`, and whether repeated hyperedges require a convention adjustment. The isolated statement and proof are available at [stable preprint or public-note link].

Thank you for any reference or correction,
Rafael Suarez

## Sending rules

- one recipient chosen for a specific technical reason;
- one claim per email;
- stable link rather than the full laboratory history;
- no attachment unless requested;
- no mention of solving P versus NP;
- no request to review the entire project;
- record date, recipient description, theorem targeted, and evidence of sending in the external-validation ledger.
