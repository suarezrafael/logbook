# Appendix A — affine output-fiber avoidance

## Setting

Let

```text
C=(C_1,...,C_m): {0,1}^n -> {0,1}^m.
```

For each coordinate choose a target value `alpha_i`. Define the active fiber

```text
F_i = {x in GF(2)^n : C_i(x)=alpha_i}.
```

Assume each `F_i` is supplied by a polynomial-time computable affine system

```text
A_i x = b_i.
```

An empty fiber is represented by an inconsistent system. Let `Z_i(Y)` denote the output literal that is one exactly when output coordinate `i` equals `alpha_i`.

## Theorem A.1 — affine consistency or redundancy

If `m>n`, a word outside `Range(C)` can be constructed in deterministic polynomial time.

### Branch I — inconsistent selected fibers

Stack all equations from the `m` affine systems. If the combined system is inconsistent, Gaussian elimination can recover an inclusion-minimal inconsistent equation subsystem `E`.

Let `G` be the set of gate blocks contributing equations to `E`. Minimal inconsistency over `n` variables has at most `n+1` equations, hence at most `n+1` contributing gate blocks.

The output target that activates exactly the gates in `G` is absent. A separator is

```text
Q(Y) = product_{i in G} Z_i(Y).
```

Every range point makes at least one selected block inactive, so `Q` vanishes on the range. It evaluates to one at the missing target. Its degree is at most `n+1`.

### Branch II — consistent selected fibers

Let `x*` satisfy all active systems and translate `z=x+x*`. Every active block becomes homogeneous:

```text
W_i = rowspace(A_i) <= GF(2)^n.
```

Let `R=sum_i W_i`. Choose a minimal set of blocks whose sum is `R`. A minimal generating family has at most `dim(R)<=n` members. Since `m>n`, at least one block `W_i` is omitted and therefore

```text
W_i <= sum_{j in J} W_j
```

for some set `J` of at most `n` other blocks.

Thus activation of every block in `J` implies activation of block `i`. The target with all `Z_j=1` for `j in J`, with `Z_i=0`, and with arbitrary fixed values elsewhere is absent. A separator is

```text
Q(Y) = (1-Z_i(Y)) product_{j in J} Z_j(Y),
```

again of degree at most `n+1`.

## Algorithm

1. Construct the combined affine system.
2. Run Gaussian elimination.
3. If inconsistent, extract a minimal inconsistent subsystem and return the corresponding active-gate target.
4. If consistent, obtain one solution `x*`.
5. Compute a basis for each row space `W_i`.
6. Build a minimal block generating family for the total span.
7. Select an omitted block `i` and express its basis using at most `n` selected blocks.
8. Return the target that activates the implying blocks and deactivates block `i`.

All steps are polynomial in the explicit affine descriptions.

## Adaptive extension

The same algorithm works without `m>n` whenever:

- the selected systems are jointly inconsistent; or
- some complete coefficient block is contained in the sum of the other blocks.

In particular, the sufficient condition can be stated as

```text
m > total coefficient rank.
```

## Ternary consequence

For ternary gates whose selected local fibers are affine or empty, including repeated supports, preimages under the support map remain affine or empty. This covers mixtures of the essential NPN classes represented by:

```text
0x01, 0x06, 0x18, 0x69.
```

## Field-independent certificate

The search uses `GF(2)` linear algebra, but the final product implication is a Boolean polynomial identity and therefore holds over every field.

## Boundary and nonclaims

- The block lemma may be standard in affine CSP, matroid, coding or functional-dependency language.
- Exact prior art has not been confirmed.
- A non-affine Boolean fiber cannot be represented exactly as the existential projection of a single affine system, because affine projections remain affine.
- This appendix does not extend the algorithm to arbitrary ternary gates or general `NC0_3-Avoid`.
