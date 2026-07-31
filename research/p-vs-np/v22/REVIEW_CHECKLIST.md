# V22 External Review Checklist

## Core zero-set lemma

- [ ] Check that a nonzero dependency among zero-set polynomials makes the one-violation Boolean target impossible.
- [ ] Check treatment of coefficients outside the dependency support.
- [ ] Check that the algorithm is polynomial when coefficient vectors are explicitly constructible.

## Symmetric fan-in-k representation

- [ ] Check coordinatewise output complementation.
- [ ] Check the bound `|S_i| <= floor((k+1)/2)`.
- [ ] Check that choosing a prime `q>k` prevents collisions between local Hamming weights.
- [ ] Check that multilinearization preserves the Boolean zero set and does not increase degree.
- [ ] Check the dimension `sum_{j=0}^d binom(n,j)`.
- [ ] Check constants, lower arities, and distinct-variable assumptions.

## Fan-in-four corollary

- [ ] Check `d=2` and `D(n,2)=1+n+binom(n,2)`.
- [ ] Search for prior work giving the same or stronger symmetric `NC0_4-Avoid` threshold.
- [ ] Compare precisely with generic deterministic `NC0_4-Avoid` results.

## Scientific safeguards

- [ ] Do not call the result novel before a substantive prior-art search.
- [ ] Preserve any counterexample or correction in the repository.
- [ ] Keep the PR as draft until review.
- [ ] Do not imply a resolution of P versus NP or an unrestricted circuit lower bound.
