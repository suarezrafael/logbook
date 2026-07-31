# Rascunho de e-mail aos autores — não enviado

**Destinatários sugeridos:** Karthik Gajulapalli, Jayalal Sarma; CC Neha Kuntewar e demais coautores relevantes.

**Assunto:** Prior-art question: affine fibers, bijunctive blocks, and orientation depth in stretch-one NC0_3-Avoid

Dear Karthik, Professor Sarma, Neha, and colleagues,

I maintain a conservative and fully reproducible research log on restricted Range Avoidance. I am writing only to ask for prior-art and terminology guidance; I am not making a priority claim.

Draft PR:

https://github.com/suarezrafael/logbook/pull/1

A previous V53 claim was false because it overlooked nested cover collisions. That claim has been formally retracted, and the counterexample is now part of the regression suite.

The corrected line led to three observations:

1. A consistency-or-redundancy algorithm for circuits whose selected output fibers are affine over GF(2), giving deterministic avoidance for m>n. We expect this to be folklore linear algebra or standard affine-CSP reasoning.
2. An explicit classification of all 14 ternary NPN classes by affine and bijunctive output fibers.
3. A minimal stretch-one 0x07-orbit gadget showing that fixed-orientation block redundancy fails for bijunctive fibers, together with a direct-sum family.

The latest V58 note reinterprets adaptive orientation geometrically. For an orientation y in the image, a fiber block is redundant exactly when y has a Hamming neighbor outside the image. This gives an m^{O(d)} algorithm parameterized by the distance d from a baseline orientation to the internal vertex boundary. The 12 finite V57 obstructions form one variable-isomorphism class and all have orientation depth one. A complete normalized search found no one-flip counterexample for n=3 through n=8; no asymptotic claim is made.

Could you point us to existing formulations covering any of the following?

- affine-fiber block redundancy for Range Avoidance;
- ternary NPN fiber classification in this context;
- block-level irredundancy under 2-CNF entailment;
- adaptive reorientation or boundary-distance parameters for Avoid;
- known obstructions to a constant orientation-depth theorem for the 0x07 orbit.

Any correction or terminology pointer would be extremely helpful. The PR will remain a draft, and novelty will not be claimed without specialist confirmation.

Best regards,
Rafael Suarez
