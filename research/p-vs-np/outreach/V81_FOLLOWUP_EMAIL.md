# Follow-up email after a public preprint exists

**Suggested subject:** Question about a hypergraph branchwidth lemma

Dear Professor [Name],

I am writing with a narrow literature question about a short lemma in a preprint of mine, rather than asking for a review of the broader project.

For a finite hypergraph with hyperedge set `M`, active vertex set `X=N(M)`, and

```text
sigma = |M|-|X|,
delta(S) = |S|-|N(S)|,
lambda(S) = |N(S) intersect N(M\S)|,
```

the lemma uses the identity

```text
delta(S)+delta(M\S)=sigma-lambda(S)
```

and derives a balanced-cut consequence for a supplied branch decomposition of width `w`: one balanced side has deficiency at least `ceil((sigma-w)/2)`.

The statement and proof are available here: [preprint or public-question link].

Do you know whether this identity or the quantitative consequence is standard under another name, or whether a known connectivity-function theorem subsumes it? A citation, convention correction, or counterexample would be very helpful.

Thank you for your time,

Rafael Suarez
