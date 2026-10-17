# Integrated Human Practices: the dry-lab consultation

Written to match the format already used in `INTEGRATED.docx`: a Heading 4 of the form
`Name, Role: Short title`, then **Why we reached out**, **What we learned**, and
**How we integrated it**.

**Before pasting, fill in the name.** The notes record `Παναγιώτου - Χατζόπουλος για
ερωτήσεις`, which reads as two surnames listed as contacts for questions rather than
unambiguously as the professor's own name. We have not guessed which, because getting a
named consultant's name wrong on an Integrated Human Practices page is worse than leaving a
placeholder for ten seconds.

---

## [NAME], Professor, Department of Computer Engineering and Informatics, University of Patras: A Second Opinion on a Problem We Could Not Solve

**Why we reached out:** Our dry lab had failed at the central computational question of the
project. We wanted to know whether our engineered payload prefers the delta opioid receptor
over the mu receptor, and after eight attempts we could not answer it. Every method we tried
either inherited an uncertainty larger than the effect we were trying to measure, or
accumulated error faster than it accumulated signal. At that point the useful thing was not
another attempt from inside our own field. It was someone who would look at the problem as a
computational problem rather than as a biological one, so we went to the Department of
Computer Engineering and Informatics.

**What we learned:** He proposed a direction we had not taken seriously, and asked a question
we had not asked ourselves.

The direction was to stop treating the system as a set of coordinates to simulate and start
treating it as a **graph**. A receptor and a peptide in contact are a network of interacting
residues, and graph neural networks are built for exactly that shape of data. He suggested
graph embeddings, and then a combination of a graph neural network with a physics-informed
neural network so that energy equations could constrain what the model learns.

The question was sharper than the suggestion. He asked **why our simulations had failed, and
in what way we could correct them so that other teams would not repeat the same failure.**
That reframed our largest negative result from something we had to explain away into
something we owed other people.

**How we integrated it:**

1. **We followed the graph branch, and it is the only machine-learning method in this project
   with a demonstrated capability rather than an assumed one.** The search led us to
   DeorphaNN, a graph neural network over peptide-receptor complexes. We validated it on the
   authors' own held-out data before trusting it on anything of ours: on a receptor clade
   excluded from the model's training it ranks true agonists with an area under the curve of
   0.893, and peptides that bind one receptor and not another score higher at the correct
   receptor in 95.1% of cases, against a 76.1% baseline from a global offset between
   receptors. That control matters, because without it the result could have been an artefact
   of one receptor simply scoring higher than the other.

2. **We assessed the physics-informed branch and did not run it, and we wrote down why.**
   When we searched the literature for physics-informed neural networks applied to this kind
   of problem, almost everything that came back was continuum and partial-differential-
   equation work: soil temperature, turbine blades, hydrogel swelling. Those methods earn
   their keep where a governing equation constrains the solution. Our failure was not a
   missing physical constraint. It was correlated sampling bias accumulating along a
   calculation, which no physics term in a loss function removes. Recording that reasoning
   was more useful to us than running the method and reporting that it did not help.

3. **His question became a deliverable.** We wrote up why the free-energy calculations
   failed, in the form another team can act on. The short version is that our diagnosis was
   correct and our fix worked and the calculation still failed: we identified poor overlap
   between neighbouring windows, re-spaced the ladder by equal thermodynamic length, and the
   overlap problem went away completely. The calculation then failed reproducibility instead,
   because doubling the number of windows to fix overlap also doubled the number of terms
   whose small biases accumulate along the path. Two replicates differing only by a random
   seed disagreed by several times the effect we were trying to measure.

   The transferable lesson is the one we would not have written down without being asked for
   it: **a selectivity computed as the difference between two large absolute quantities is
   fragile regardless of how well each quantity is converged**, and improving one diagnostic
   can worsen another. A team attempting this should check reproducibility across independent
   replicates before trusting any overlap statistic, and should prefer methods that never
   form the large absolute quantity in the first place.

4. **We changed what we claim.** The consultation did not rescue the computational
   selectivity question, and we stopped trying to make it. Our calibrated estimate remains a
   delta preference of 1.23 kilocalories per mole with an uncertainty of 1.76, an interval
   that includes zero, and delta-preference is described throughout our wiki as the property
   the peptide was designed to have rather than one we have shown it has. The cAMP assay is
   named as the instrument that settles it.

**What we could not take up:** he also raised the possibility of using the graph model to
predict energies directly. We checked the reported accuracy of the published graph networks
that do this, and the best of them reports a mean absolute error around 2.3 kilocalories per
mole, against the 0.81 we would need to resolve. We recorded the check rather than the
attempt, for the same reason as above.

---

# Steps to Paris: yes, and it completes the count

Your section is headed **MAKING THE 6 STEPS TO PARIS** and currently contains five numbered
stops, between Departure and Arrival. The dry-lab consultation belongs there as **Stop 6**,
and adding it makes the heading correct.

It also meets the criterion the section sets for itself, that *"every waypoint below marks a
conversation that redirected the route"*. This one redirected the dry lab away from methods
that predict an energy and toward methods that classify, changed what the project claims
about its own peptide, and produced a write-up for other teams that would not otherwise
exist.

One thing worth noticing: it is the only stop on the map where the route was redirected by
something that **failed**. The other five are a vector abandoned, a gene changed, a
formulation chosen, a tag relocated and a laboratory opened. This one is a question asked
about a negative result, and the honest answer becoming a contribution. That is a different
kind of waypoint and it is worth having on the map for exactly that reason.

Paste after Stop 5, in the same format as the others.

---

**Stop 6 — Asking why the modelling failed**
**[NAME] — Department of Computer Engineering and Informatics, University of Patras**

The last stop was not about the bench. Our dry lab had tried eight ways to show that our
engineered peptide prefers the delta opioid receptor, and none of them could resolve an
effect that small. We took the problem to a computer scientist rather than another biologist.
He suggested we stop treating the complex as coordinates to simulate and start treating it as
a graph, which led us to the one machine-learning method in this project we were able to
validate rather than assume. Then he asked the question that mattered more: not whether we
could fix it, but why it had failed, and how we could write that down so another team would
not repeat it. Our largest negative result stopped being something to explain and became
something we owed other people.

---

## A note on Stop 4, for consistency

Stop 4 records Dr. Zouridakis confirming the polyhistidine tag had to sit at the N-terminus
to leave the terminal YGGFMRF peptide intact. That is correct and the dry lab verified it
independently from the ordered sequences: the signal peptide occupies residues 1 to 24 and
the tag begins at residue 25, immediately downstream of it.

Worth knowing, because a figure caption elsewhere in the project described the tag as sitting
*upstream* of the signal peptide. The design is right and the caption was wrong, and it has
been corrected. A judge reading both documents would otherwise find them disagreeing.

---

**One formatting note.** The Stop 6 heading above uses em dashes, because every other stop
heading in your document does: `Departure — Patras`, `Stop 1 — Leaving the viral vector
behind`. Consistency inside that section seemed worth more than the repository's no-em-dash
convention, which applies to the dry-lab repository rather than to your prose. The version of
`INTEGRATED.docx` you sent carries 21 em dashes of its own, so if you run a cleanup pass
over it later, these two will be caught by the same sweep and nothing breaks either way.
