# Directed audit: explicit lossless expanders as obstruction families

## Question

Can the probabilistic Hall-expanding families of V80 be replaced immediately by
an explicit family whose left degree is exactly three, whose two sides have
sizes

```text
m = n + ceil(n^(2/3)) and n,
```

and whose relevant small and balanced subsets have the expansion needed by the
V80/V81 obstruction program?

## Located primary sources

### Golowich, ECCC TR23-089 / arXiv:2306.07551

The paper constructs explicit one-sided lossless bipartite expanders of
constant degree with arbitrary constant ratio between side sizes. The theorem
requires a sufficiently large degree `D(beta,epsilon)`. Its parameter choice
uses `k=ceil(10/epsilon)` and a gadget degree, so it does not instantiate left
degree exactly three.

This source is directly relevant to the near-balanced ratio, and its families
are useful controls after translating parameters, but it is not a ready-made
rank-three support family.

### Chattopadhyay--Gurumukhani--Ringach--Zhao, ECCC TR24-133 / arXiv:2409.04549

This gives explicit two-sided lossless expanders in the polynomially unbalanced
setting. The regime and degree are not the exact near-balanced degree-three
parameters required here.

### Hsieh--Lubotzky--Mohanty--Reiner--Zhang, arXiv:2504.15087

This gives explicit constant-degree lossless vertex expanders and bipartite
extensions for sufficiently large degree. Again, the theorem does not provide
degree three.

### Viola--Wigderson, ECCC TR16-129

This includes explicit bipartite Ramanujan graphs of degree three. These are
spectral expanders. Spectral expansion alone is not sufficient for lossless
expansion; optimal spectral expanders can fail lossless expansion, as noted in
the modern lossless-expander literature.

## Conclusion

The directed search found strong explicit families but no theorem that can be
inserted unchanged as an exact degree-three obstruction at the V80 stretch.
The correct next action is parameter translation and finite instantiation, not
a claim that the explicit-obstruction arm has already been solved.

A V82 expander task should require all of the following before promotion:

1. exact left degree at most three after any reduction or encoding;
2. the target side sizes or a proved padding/restriction lemma preserving the
   required Hall and branchwidth properties;
3. polynomial-time explicit neighbor computation;
4. a proved expansion range strong enough to feed the all-orders obstruction
   program;
5. independent finite checks on the first constructible instances.

## References

- Louis Golowich, *New Explicit Constant-Degree Lossless Expanders*, ECCC
  TR23-089, arXiv:2306.07551.
- Eshan Chattopadhyay, Mohit Gurumukhani, Noam Ringach, and Yunya Zhao,
  *Two-Sided Lossless Expanders in the Unbalanced Setting*, ECCC TR24-133,
  arXiv:2409.04549.
- Jun-Ting Hsieh, Alexander Lubotzky, Sidhanth Mohanty, Assaf Reiner, and
  Rachel Yun Zhang, *Explicit Lossless Vertex Expanders*, arXiv:2504.15087.
- Emanuele Viola and Avi Wigderson, *Local Expanders*, ECCC TR16-129.
- Eden Chlamtac, Michael Dinitz, Christian Konrad, Guy Kortsarz, and George
  Rabanca, *The Densest k-Subhypergraph Problem*, arXiv:1605.04284.
- Eden Chlamtac, Michael Dinitz, and Yury Makarychev, *Minimizing the Union:
  Tight Approximations for Small Set Bipartite Vertex Expansion*,
  arXiv:1611.07866.
