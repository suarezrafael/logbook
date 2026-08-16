# V103 literature boundary

## Internal relation to earlier laboratories

V56 proved polynomial-time avoidance when selected fibers are already exact
affine systems. V103 does not assume exact affinity: it enlarges each canonical
fiber to its affine hull, keeps only a rank-increasing basis of output blocks,
and enumerates the residual affine dimension `nu=n-R`.

V101 uses functional graph relations and requires an acyclic distinct-head
selection. V103 instead accepts arbitrary cycles when the safe relaxation can be
expressed by affine equations, because Gaussian elimination handles the entire
cycle globally.

V102 uses strong affine backdoors: every assignment to the backdoor must make all
remaining gates affine. V103 is one-sided in a different sense: it chooses one
canonical target fiber per output and asks only whether its affine hull provides
global rank.

## External calibration

The targeted search reviewed primary range-avoidance sources including:

- ECCC TR22-102, Guruswami--Lyu--Wang, on low-depth range avoidance and the
  polynomial-time `NC0_2` case;
- ECCC TR23-072, Chen--Huang--Li--Ren, on range avoidance through the algorithmic
  method and satisfying-pairs machinery;
- ECCC TR23-193, Chung et al., which introduces a different total-search problem
  named `AffineAvoid` in a cryptographic/meta-complexity setting;
- ECCC TR25-034, Kuntewar--Sarma, on Turan-type range-avoidance bounds;
- ECCC TR25-049, Huang--Li--Zhong, on improved general/local algorithms and
  hardness connections.

Affine hulls, rank, and Gaussian elimination themselves are standard linear
algebra and are not claimed as novel. The search did not locate a statement
matching the exact V103 template: safe per-fiber affine-hull relaxation, a
rank-increasing output-block basis, and enumeration parameterized by `n-R`.
Absence from this targeted search is not evidence of novelty or priority.

## Naming caution

The V103 parameter is an internal `affine-hull rank` parameter for ordinary
Range Avoidance. It is unrelated to the externally named `AffineAvoid` problem
of ECCC TR23-193 except that both use affine terminology.

## External validation target

A subject-matter review should specifically ask whether this block-rank
relaxation appears in CSP closure methods, range-avoidance work, proof
complexity generators, or coding-theoretic remote-point arguments under another
name. Until then, `novelty_confirmed=false` remains mandatory.
