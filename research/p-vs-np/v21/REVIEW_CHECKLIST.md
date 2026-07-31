# Mathematical Review Checklist

## Reviewer target

Please evaluate the proof independently rather than trusting the code or benchmark summary.

## A. Definitions and scope

- [ ] Is `SYMMETRIC-NC0_3-Avoid` defined consistently with the closest literature?
- [ ] Are fan-in-zero, fan-in-one, and fan-in-two outputs handled correctly?
- [ ] Are repeated input variables or constants in a gate permitted, and if so, does the taxonomy still cover them?
- [ ] Is the use of `m` consistent after removing constant coordinates?

## B. Taxonomy

- [ ] Does coordinatewise output complementation reduce every nonconstant symmetric gate of arity at most three to threshold, parity, or exact-residue MOD3?
- [ ] Are there any missed truth tables or overlapping classifications that affect the proof?
- [ ] Does lower arity require any special representation in the monotone branch?

## C. Threshold branch

- [ ] Does the published monotone theorem apply to all normalized threshold gates of fan-in at most three?
- [ ] Is replacing `n` by the number of actually used variables `|V_T|` legitimate?
- [ ] Can the avoided subvector be extended arbitrarily to a full avoided output?

## D. Parity branch

- [ ] Is the incidence matrix over GF(2) the correct affine/linear representation after output normalization?
- [ ] Does every nonzero left-null vector yield a Boolean output outside the image?
- [ ] Are complemented parity coordinates correctly undone?

## E. Exact-residue MOD3 branch

- [ ] Is each normalized gate exactly the indicator of one equation `a_i x = r_i mod 3` on Boolean inputs?
- [ ] In the case `lambda^T r != 0`, is the all-ones output impossible?
- [ ] In the case `lambda^T r = 0`, does setting one support coordinate to zero and the others to one force a contradiction?
- [ ] Are coordinates outside the dependency support irrelevant and safely assignable?
- [ ] Does the argument avoid the invalid identification of a Boolean indicator image with an affine GF(3) image?

## F. Pigeonhole and complexity

- [ ] If no branch fires, do the three inequalities sum to `m <= d_T+r_2+r_3`?
- [ ] Are constants removed or handled without breaking the count?
- [ ] Are classification, Gaussian elimination, certificate construction, and the monotone subroutine polynomial in the input representation size?

## G. Prior art and version history

- [ ] Is the `m>8n` symmetric result accurately attributed to ECCC TR25-034 v1?
- [ ] Is the omission from later versions described neutrally, without inferring a reason?
- [ ] Is an equivalent rank/effective-dimension theorem already known?

## H. Scientific claims

- [ ] Does the manuscript clearly say that it is not peer reviewed?
- [ ] Does it avoid claiming P versus NP progress beyond the restricted range-avoidance theorem?
- [ ] Are experiments described as validation rather than proof?

## Requested review outcome

Please return one of:

1. no flaw found, with any exposition suggestions;
2. a precise gap or counterexample;
3. a prior-art reference superseding the claim;
4. a recommendation for a more appropriate expert or venue.
