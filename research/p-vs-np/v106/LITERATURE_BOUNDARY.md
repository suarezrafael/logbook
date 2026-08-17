# V106 literature boundary

## Range avoidance

The range-avoidance calibration remains the Kuntewar--Sarma and subsequent
range-avoidance line.  In particular, published polynomial algorithms for
majority `NC0_3` use substantially larger stretch than the exact-stretch
`m=n+1` regime studied here, while monotone `NC0_3` is known at exact stretch.
V106 does not claim to improve the unrestricted published worst-case bound.

Primary calibration used by the laboratory:

- Neha Kuntewar and Jayalal Sarma, *Range Avoidance in Boolean Circuits via
  Turan-type Bounds*, ECCC TR25-034 (2025).

## Signed/biased graphs and frame matroids

The facts used in the Hall/Rado bridge are standard signed-/biased-graph matroid
facts: an unbalanced candidate triangle is a signed-graph object, the associated
frame matroid has the usual balanced-component rank formula, and its circuits
include balanced cycles and handcuff-type unions of unbalanced cycles.

Useful primary/technical references checked include work of Zaslavsky and modern
biased-graph/frame-matroid treatments such as Chen--DeVos--Funk--Pivotto,
*Graphical representations of graphic frame matroids* (arXiv:1403.7733), and
Florez--Zaslavsky, *The Projective Planarity Question for Matroids of 3-Nets and
Biased Graphs* (arXiv:1708.00095).

## Rado / matroid transversals

The independent-transversal step is an application of the standard Rado
matroid-marriage theorem: one representative can be selected from every member
of a family while remaining independent exactly when every subfamily has enough
matroid rank.  V106's observation is only the specialization that, for the
three-pair candidate set supplied by signed majority, that rank becomes the
ordinary support-neighborhood size.

No novelty is claimed for Rado's theorem, frame matroids, signed graphs, 2-SAT
implication SCCs, or FPT enumeration by Hamming distance from a canonical
selection.

## What may be specific to this laboratory

The item requiring external specialist review is the exact composition:

1. expose the three majority pair clauses as an unbalanced signed triangle;
2. identify support Hall rank with the candidate-pair frame rank;
3. use bounded distance from the V105 odd-handcuff class as a range-avoidance
   parameter;
4. study minimal positive surplus as a colorful frame-circuit selection problem.

Search absence is not evidence of novelty.  V106 must not be presented as a new
matroid theorem or a new range-avoidance theorem beyond the precise proved
parameterized statement without external review.

## External prior-art questions

Ask experts whether any of the following are already standard under another
name:

- minimum recoloring/representative changes needed to obtain a handcuff circuit
  in a signed-graphic frame matroid;
- colorful/rainbow circuit extraction from a minimally Rado-deficient family;
- selecting one edge from each unbalanced triangle so the first dependence is a
  handcuff rather than a balanced cycle;
- grouped 2-SAT clause-pair selection specialized to majority constraints.
