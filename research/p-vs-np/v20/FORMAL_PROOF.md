# Effective-Dimension Range Avoidance for Symmetric NC0_3 Circuits

## Statement

Let `C:{0,1}^n -> {0,1}^m` be a circuit in which every output is a symmetric Boolean function of at most three input variables.

Complement output coordinates independently so that every nonconstant gate belongs to one of the following normalized families:

1. a monotone threshold gate;
2. a parity gate;
3. a ternary exact-residue gate `E_r(a,b,c)=1` iff `a+b+c = r (mod 3)`.

Let `T,P,R` be their output-index sets. Let `V_T` be the set of variables used by threshold outputs. Let `A_P` be the parity incidence matrix over GF(2), and `A_R` the exact-residue incidence matrix over GF(3).

If

```text
m > |V_T| + rank_GF2(A_P) + rank_GF3(A_R),
```

then an output outside the range of `C` can be found deterministically in polynomial time. Since all dimensions are at most `n`, a uniform sufficient condition is `m>3n`.

## Taxonomy lemma

A symmetric Boolean function of arity `k<=3` is represented by `(f(0),...,f(k))`. After possibly complementing the output:

- all monotone vectors are thresholds;
- the remaining nonconstant vectors of arity two are parity;
- the remaining vectors of arity three are parity or one of three exact-residue indicators.

The independent verifier checks all 30 symmetric tables of arities zero through three.

## Coordinatewise normalization lemma

Let `g_i=f_i xor c_i`, where every `c_i` is fixed. If `z` is outside the range of `g`, then `z xor c` is outside the range of `f`. Complements therefore do not require separate pigeonhole classes.

## Threshold branch

If `|T|>|V_T|`, renumber the variables in `V_T`. The threshold subcircuit is a monotone NC0_3 circuit with more outputs than inputs. Invoke the published deterministic polynomial algorithm for Monotone-NC0_3-Avoid, extend its avoided output arbitrarily on other coordinates, and undo the output complements.

## Parity branch

If `|P|>rank(A_P)`, choose nonzero `lambda` with `lambda^T A_P=0`. Every parity output `y=A_Px` satisfies `lambda^T y=0`. Choose a Boolean `y` with `lambda^T y=1`. It is outside the parity image.

## Exact-residue branch

For `i in R`, write the gate equation as `a_i^T x=r_i (mod 3)`. Its Boolean output indicates whether this equation holds. If `|R|>rank(A_R)`, choose nonzero `lambda` with `lambda^T A_R=0`.

### Case A: `lambda^T r != 0`

Request output one on every equation. If all equations held, then `0=(lambda^T A_R)x=lambda^T r`, a contradiction.

### Case B: `lambda^T r = 0`

Choose `j` with `lambda_j != 0`. Request output one for every equation in the support of `lambda` except `j`, and output zero at `j`. The dependency implies `lambda_j(a_j^T x-r_j)=0`; since `lambda_j` is nonzero, the `j`-th equation must hold, contradicting the requested zero.

## Theorem

If no branch fires, then

```text
|T| <= |V_T|
|P| <= rank_GF2(A_P)
|R| <= rank_GF3(A_R)
```

Adding the inequalities contradicts the effective-dimension condition. All operations are polynomial: classification is constant-time per output, finite-field dependencies use Gaussian elimination, and the threshold branch uses the published polynomial algorithm.

## Scientific status

This is an internally checked proof candidate. It has not been peer reviewed, and priority over unpublished or unindexed work has not been established.
