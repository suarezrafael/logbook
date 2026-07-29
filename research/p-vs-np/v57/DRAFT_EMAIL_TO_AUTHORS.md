# Rascunho de e-mail aos autores — não enviado

**Destinatários sugeridos:** Karthik Gajulapalli, Jayalal Sarma; CC Neha Kuntewar.

**Assunto:** Prior-art question: affine and bijunctive subclasses of stretch-one NC0_3-Avoid

Dear Karthik, Professor Sarma, and Neha,

I am maintaining a conservative, reproducible research log on restricted Range Avoidance. I am writing to ask for prior-art guidance, not to make a priority claim.

The draft PR is:
https://github.com/suarezrafael/logbook/pull/1

A previous V53 claim was false because it missed nested cover collisions; it has been formally retracted and added to regression tests.

The corrected line led to an elementary consistency-or-redundancy algorithm for circuits whose selected output fibers are affine over GF(2), giving deterministic avoidance for m>n. For ternary NPN classes this handles the essential classes 0x01, 0x06, 0x18, and 0x69, including arbitrary mixtures.

We suspect this affine theorem is folklore or standard affine-CSP linear algebra. The potentially useful object may be the explicit 14-class NPN map and its Range-Avoidance interpretation.

We have now tested the bijunctive frontier. A direct block-redundancy analogue is false already for five 0x07-orbit gates on four variables: all selected small fibers are jointly satisfiable, the common assignment is unique, and every gate block is essential. The construction extends to an infinite stretch-one family. This is consistent with the classical 2-CNF redundancy literature, but we have not found the same NC0_3-Avoid formulation.

Could you point us to existing formulations covering the affine block observation, the ternary NPN classification in a Range-Avoidance context, or block irredundancy for bijunctive output fibers?

Any correction or terminology pointer would be very helpful. We will keep the PR as a draft and will not claim novelty without specialist confirmation.

Best regards,
Rafael Suarez
