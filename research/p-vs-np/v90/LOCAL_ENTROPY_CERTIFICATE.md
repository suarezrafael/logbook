# Finite local entropy-contraction certificate

## Setup

Let

```text
Omega = F_2^3 \ {0},   |Omega|=7,
```

and let `f:Omega^3->{0,1}` be the indicator that an ordered triple is a basis. There are `168` ordered bases, hence

```text
p = E[f] = 168/7^3 = 24/49.
```

Let `B` be a `7x7` doubly stochastic matrix. Couple two uniform points by

```text
Pr[X=x,Y=y] = B_xy/7.
```

Using three independent copies of this coupling,

```text
q(B)=E[f(X_1,X_2,X_3) f(Y_1,Y_2,Y_3)].
```

The second-moment exponent uses

```text
D(B)=ln(7)-H(B)/7,
L(B)=ln(q(B)/p^2).
```

Write `U` for the all-`1/7` matrix and `C=B-U`.

## Hoeffding decomposition

All one-coordinate projections of `f` vanish after centering, by transitivity of `GL(3,2)` on nonzero vectors. For one coordinate pair define

```text
h(x,y)=E_z[f(x,y,z)]-p.
```

Direct counting gives

```text
h(x,x) = -24/49,
h(x,y) =   4/49  for x != y.
```

Therefore

```text
||h||_2^2 = 96/2401.
```

The three pair components are orthogonal, so their total squared norm is

```text
3||h||_2^2 = 288/2401.
```

Since

```text
Var(f)=p(1-p)=600/2401,
```

the pure degree-three component `g` has

```text
||g||_2^2 = 312/2401.
```

Thus

```text
f = p + h_12 + h_13 + h_23 + g
```

is an orthogonal decomposition.

## Coupling operator

On mean-zero functions on `Omega`, define

```text
(T_C phi)(x)=sum_y C_xy phi(y).
```

Because `B` is doubly stochastic, `T_C` is the centered part of the Markov operator associated with the coupling. Let

```text
sigma=||T_C||_(2->2).
```

Every Markov operator is an `L_2` contraction, so

```text
sigma <= 1.
```

Also

```text
sigma <= ||C||_F.
```

Orthogonality of the Hoeffding levels under the product coupling gives

```text
q(B)-p^2
 = sum_{pairs} <h,(T_C tensor T_C)h>
   + <g,T_C^(tensor 3)g>.
```

The exact pair-level audit on the 36-dimensional doubly stochastic tangent space proves

```text
sum_{pairs} <h,(T_C tensor T_C)h>
  = (48/2401)||C||_F^2.
```

For the degree-three term, operator submultiplicativity gives

```text
|<g,T_C^(tensor 3)g>|
 <= ||g||_2^2 sigma^3
 = (312/2401)sigma^3.
```

Hence the exact decomposition and global envelope are

```text
q(B)
 = p^2 + (48/2401)||C||_F^2 + T_3(C),

|T_3(C)| <= (312/2401)sigma^3.
```

Dividing by

```text
p^2=576/2401
```

yields

```text
q(B)/p^2
 <= 1 + ||C||_F^2/12 + 13 sigma^3/24.
```

## Entropy bound in a finite ball

Assume

```text
||C||_F <= r.
```

Every entry on the segment from `U` to `B` is at most

```text
1/7+r.
```

For `phi(x)=x ln(7x)`, one has `phi''(x)=1/x`. Taylor's theorem, together with the zero row and column sums of `C`, gives

```text
D(B)
 = (1/7) sum_ij phi(B_ij)
 >= 1/[2(1+7r)] ||C||_F^2.
```

If `q(B)=0`, the desired second-moment inequality is immediate. Otherwise `ln z <= z-1`, and `sigma<=||C||_F<=r` gives

```text
L(B)
 <= [1/12 + (13/24)r] ||C||_F^2.
```

Therefore, for any density `c`,

```text
D(B)-cL(B)
 >= {1/[2(1+7r)] - c[1/12+(13/24)r]} ||C||_F^2.
```

## Certified constants

Choose

```text
r=1/5,
c=21/20.
```

Then

```text
1/[2(1+7r)] = 5/24,
1/12+(13/24)r = 23/120,
5/24-(21/20)(23/120) = 17/2400.
```

Thus

```text
D(B)-(21/20)L(B)
 >= (17/2400)||B-U||_F^2
```

for every doubly stochastic `B` satisfying

```text
||B-U||_F <= 1/5.
```

Equality occurs at the uniform matrix; every other matrix in the certified ball has a strict positive margin.

## Boundary

This theorem does not control the exterior region of the Birkhoff polytope. It is not a global second-moment theorem and does not imply basis-colorability with high probability by itself.
