# Zero-Set Polynomial Dependencies for Symmetric Local Range Avoidance

## General lemma

Let `F` be a field and `V` a `D`-dimensional vector space of functions on `X`. Suppose Boolean outputs satisfy

```text
g_i(x)=1 iff p_i(x)=0, with p_i in V.
```

If `m>D`, Gaussian elimination finds nonzero coefficients such that

```text
sum_i lambda_i p_i = 0.
```

Choose `j` with `lambda_j != 0`. Request output one on every other coordinate in the dependency support and output zero at `j`. If an input realized the target, every other support polynomial would vanish; the dependency would force `p_j=0`, contradicting the requested zero.

## Symmetric fan-in-k corollary

Choose a prime `q>k`. For each output, complement it when necessary so its accepting weight set `S_i` has size at most

```text
d=floor((k+1)/2).
```

With local weight

```text
L_i(x)=sum_{v in vars(i)} x_v,
```

define

```text
p_i(x)=product_{r in S_i}(L_i(x)-r).
```

Since `q>k`, on Boolean inputs this polynomial vanishes exactly on the accepted weights. Multilinearization modulo `x_v^2=x_v` leaves degree at most `d`. The ambient dimension is

```text
D(n,d)=sum_{t=0}^d binom(n,t).
```

Therefore deterministic polynomial-time range avoidance holds for fixed `k` when

```text
m>D(n,d).
```

More generally, it holds whenever the actual polynomial coefficient vectors have rank smaller than `m`.

## Fan-in four

For `k=4`, `d=2`, hence

```text
m>1+n+binom(n,2)=(n^2+n+2)/2.
```

## Scientific status

Internally checked theorem candidate. Not peer reviewed. Novelty and priority are not established. This result covers symmetric local outputs, not arbitrary `NC0_4`, and does not resolve P versus NP.
