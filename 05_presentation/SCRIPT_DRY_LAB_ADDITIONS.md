# Presentation script: dry-lab additions, and two corrections

Read the two corrections first. One is a factual error that a judge who knows opioid
peptides will catch, and the other is a production note in the script that would put an
indefensible number on screen.

---

## Correction 1 · The engineered core is not "the Leu form"

**Where:** paragraph 117 and the visual cue at 118.

The script says the seven cores are rebuilt to the delta-preferring form, and the visual
direction is *"the same seven cores flipping, one by one, to the Leu form."*

Translating the ordered construct, the engineered core is **YGGFEVVG**, seven copies, and
there is not one YGGFL in it. Leu-enkephalin is YGGFL. The two share only the YGGF prefix.

**The real design is better than the one the script describes.** The payload keeps
Met-enkephalin's message domain, YGGF, and carries deltorphin's address domain, FEVVG, on the
end of it. That is a message-address graft from a naturally delta-selective peptide, not a
substitution of one residue. Deltorphin's own core is YAFEVVG, read from the crystal
structure 8F7S, and our payload shares FEVVG with it.

Replacement line for 117:

> S6: Our Engineered PENK rebuilds all seven cores on a different principle. Each one keeps
> the message domain that every enkephalin uses to switch the receptor on, and carries in its
> place the address domain of deltorphin, a frog peptide that is naturally far more
> delta-selective than anything the human precursor makes. Seven copies, one address.

Replacement visual for 118:

> [VISUAL] One core, split into two blocks: message and address. The message block stays. The
> address block is replaced by the deltorphin block, which then propagates to all seven cores.
> Then: arrow weighted to DOR.

The native-precursor line at 115 is **correct and should stay**: six Met cores and one Leu
core, verified against UniProt P01210.

---

## Correction 2 · Do not add the docking number

**Where:** the production note at paragraph 121, which proposes molecular docking of the
engineered peptides against DOR and MOR to produce *"a comparative binding-energy number"*
that turns predicted into *"predicted, and here is the prediction."*

**We attempted that, nine separate ways, and every one of them failed.** The attempts are
documented in the repository with gates written and committed before each test ran. Two
general findings rule out whole classes of method rather than individual attempts:

- anything anchored to published affinity values inherits a disagreement between sources
  larger than the effect being measured;
- anything computing selectivity as the difference between two large absolute energies
  accumulates correlated error along the calculation.

Docking scores fall in the second class, and their reported errors exceed the 0.81 kcal/mol
difference we would need to resolve. A comparative docking number put on screen would be a
number we cannot defend in Q&A, and the first judge to ask how it was validated would get an
answer that undoes the credibility the rest of the section earns.

**What to do instead** is the addition below, which is stronger: say that the question was
attacked and could not be settled computationally, and name the experiment that settles it.

---

## Addition 1 · The honest number, inside the peptide section

Insert after paragraph 119. Currently the section says the sequence is designed and
contributed, and stops. A judge asking *how much more delta-preferring?* gets silence, which
is the worst available answer because it sounds like the number is bad.

> S6: You should ask how much more selective. We calibrated a selectivity model against
> thirteen published reference opioids before we trusted it on our own peptide, and it
> reproduces the published ordering with a correlation of 0.805, getting the direction right
> for twelve of the thirteen. Applied to our payload it returns a delta preference of
> 1.23 kilocalories per mole, with an uncertainty of 1.76.
>
> That interval includes zero. We are not going to round it away. Delta-preference is the
> property this peptide was designed to have, and it is not yet a property we have shown it
> has.

> [VISUAL] The calibration scatter, thirteen reference compounds. Then our payload's estimate
> plotted with its error bar crossing zero.

**Why this helps rather than hurts.** It converts the weakest point in the section from
something a judge discovers into something you told them, and it is immediately followed by
the cAMP assay at 9:05, which is the experiment that resolves it. State the limit, then name
the instrument.

---

## Addition 2 · The falsification record, in achievements

Insert into the list at paragraph 185. The dry lab's strongest methodological asset is absent
from the whole script: predictions were committed to version control before the tests that
judged them, so the record is checkable rather than asserted.

> - pre-registered every computational prediction in version control before the test that
>   could falsify it, and scored twenty-two of them: eleven confirmed, eleven falsified,
>   with the falsifications on the wiki rather than removed from it.

> S2: Eleven of our own predictions were wrong, and the commit history shows we wrote them
> down before we found out. That is the part of this project we would most want another team
> to copy.

One line, and it is the line that separates a documented project from a presented one.

---

## Addition 3 · The dose model, in the validation plan

Insert after paragraph 155, before the production notes. The script closes the validation
plan on three experiments and the dry lab has one more deliverable that is already built and
waiting on one of them.

> S5: And one calculation is already waiting for the first of those results. We built the
> intranasal dose model with the expression yield left as a free variable, so the moment the
> transfection gives us a number, the dose follows. It has already told us something we did
> not expect: the enzymatic clearance our silencer targets outruns the natural washout of
> cerebrospinal fluid by about twenty-five times, which is the quantitative reason the
> silencer is in the design at all.

> [VISUAL] The dose model's sensitivity panel, with the clearance comparison highlighted.

This is the clearest example in the project of modelling that is complete except for a
measurement, and it gives the transfection result somewhere to land.

---

## Addition 4 · One sentence in the maturation passage

Paragraph 145 already states correctly that HEK293T has neither PC2 nor carboxypeptidase E.
One clause is worth adding at 146, because it answers the question a judge will ask next.

> ...and we checked that recoding the payload had not disturbed the sites those enzymes have
> to cut: the engineered precursor carries the same twelve paired basic sites as the native
> one, of the same types, in the same order.

That is verified from the sequences and is a stronger thing to say than it sounds, because
the obvious objection to recoding a precursor is that you have broken its processing.

---

## What is already right, and should not be touched

The validation-plan section at 9:05 is the best-argued part of the script and the dry lab's
reasoning is already correctly woven into it. Paragraph 145 names PC2 rather than PC1/3 and
gives the right reason. Paragraph 146 presents the chassis limitation as something identified
in advance and designed around, which is exactly what happened. Paragraph 151 frames the
question as whether the products work rather than what they are. Paragraph 157's instruction
to keep the tense exact is the right instruction and matters more than any addition here.

The lipoplex passage at 123 to 127 is accurate as written, including that the contact metrics
plateau early and that this is an observation from our own pipeline.

The silencer passage is accurate, including the two sentences the script correctly identifies
as the strongest in the section. The 206-candidate library, the discarded SNP candidate and
the self-targeting screen are all verified against the design record.
