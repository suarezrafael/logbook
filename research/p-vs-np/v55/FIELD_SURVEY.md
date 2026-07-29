# V55 field survey and prior-art positioning

Guruswami, Lyu, and Wang give a polynomial-time algorithm for `NC0_2-Avoid`. Gajulapalli, Golovnev, Nagargoje, and Saraogi identify stretch-one `NC0_3-Avoid` as open and show that an `FP^NP` algorithm at stretch `n+n^(2/3)` would imply explicit rigid matrices and super-linear log-depth circuit lower bounds. Kuntewar and Sarma solve monotone `NC0_3-Avoid` for every positive stretch.

The V55 antipodal-pair class is essential and nonmonotone, so its theorem is not a restatement of the monotone algorithm.

Affine Boolean relations and XOR systems are classical tractable CSP objects. The potentially distinctive point is the gate-block counting argument: counting one affine relation per output forces an entire output fiber to be implied once the number of gate blocks exceeds the ambient equation dimension.

A targeted search did not identify this exact formulation as a Range-Avoidance algorithm for the antipodal ternary NPN class. This is not a novelty determination; equivalent statements may exist in affine CSP, matroid, functional-dependency, coding, or bounded-arithmetic terminology.

Primary references:

1. Guruswami, Lyu, Wang, *Range Avoidance for Low-Depth Circuits and Connections to Pseudorandomness*, RANDOM 2022.
2. Gajulapalli, Golovnev, Nagargoje, Saraogi, *Range Avoidance for Constant-Depth Circuits: Hardness and Algorithms*, APPROX/RANDOM 2023.
3. Kuntewar, Sarma, *Avoiding Range via Turan-Type Bounds*, RANDOM 2025.

The theorem is internally checked by two implementations but not peer reviewed. General `NC0_3-Avoid` remains open.
