# Engineering

> Four cycles. Each one changed a design, and three of them changed it because something
> did not work.

## Overview

Epione hands the cell a proenkephalin precursor and lets the cell's own enzymes release the
analgesic peptides. Building that required solving four problems in sequence, and the
engineering record below is the account of getting each one wrong first.

| cycle | the problem | what the Learn step changed |
|---|---|---|
| **1** | one plasmid must yield two proteins | two coding sequences back to back translate as **one** fused polypeptide, burying the terminal opioid core. An IRES or P2A element goes between them, and both gene orders are built for each |
| **2** | the precursor must be purified | at roughly 30 kDa it is an unremarkable size among host proteins, so size exclusion cannot isolate it. **The purification problem became a construct problem**: a His6 tag was added and capture moved to IMAC |
| **3** | the precursor must be cut | PC1/3 plus PC2 covers one enzymatic activity twice and the other not at all. CPE was added, and then its required cobalt turned out to **inhibit PC2**, splitting one reaction into two |
| **4** | the product must work | a plate-bound binding assay would report weakly for reasons unrelated to binding, so the readout moved to a **cellular functional** assay |

Every cycle follows Design, Build, Test, Learn, and is counted only where the Learn step
altered the next Design. **Two of the four were corrected before any reagent was consumed**,
which is the cheapest place to be wrong.

The dry lab appears inside these cycles as support rather than as cycles of its own; the
modelling record in full is on the Model page.

---

## Cycle 1 · Getting two proteins from one plasmid

One plasmid has to deliver proenkephalin, which is the product, and mEGFP, which reports
that the cell received the construct.

### Design

The economical version: a single CMV promoter, a Kozak sequence, and the two coding
sequences placed one after the other. One promoter, one transcript, two proteins, or so the
map suggests.

### Build

The construct was assembled **in silico** first, as a complete annotated map. Doing that
before ordering DNA is what made the next step cost nothing.

### Test

The construct was translated in silico from the Kozak sequence onward, and the predicted
product examined rather than assumed.

### Learn

**It does not make two proteins.** With nothing between the genes, the ribosome reads
through from the first start codon to the last stop codon and produces one continuous
PENK-mEGFP polypeptide.

That defeats both purposes at once. Proenkephalin's last opioid core **is** its own carboxy
terminus, so a fluorescent protein hanging off that end buries the core where the processing
enzymes cannot reach it. The conclusion is structural rather than a matter of optimisation:
something has to sit between the genes, and what sits there defines the next iteration.

### Re-Design

Two elements give two proteins from one transcript by different mechanisms. An **IRES**
allows a second independent initiation on the same mRNA, so each protein keeps its native
ends. **P2A** gives near-stoichiometric ratios through ribosomal skipping, at the cost of a
residual peptide scar.

First principles did not settle which gene should come first, so rather than guess,
**both orders were built for each element**.

### Re-Build

Four plasmids on the same pcDNA3.1(+) backbone and the same CMV promoter, differing only in
the separating element and the gene order.

### Re-Test

Each construct translated in silico as before, and the predicted products inspected: how
many polypeptides come out, and what each carries at its ends.

### Re-Learn

**All four solve the problem of iteration 1.** Every one yields two separate proteins, so
the question changes rather than closes. What the four do not share is what they cost: the
IRES constructs leave both proteins with native ends but put one gene in a weaker
cap-independent position, while P2A balances expression and leaves a scar. The decision now
rests on predicted yield and on where each scar falls, which is what the four constructs
were built to measure.

---

## Cycle 2 · Purifying the precursor

### Design

**Size exclusion chromatography.** Filter away the media proteins by size and recover ours.

### Build

SEC was to be run at the **Hellenic Pasteur Institute** under the supervision of
Dr. M. Zouridakis, using a small analytical column.

### Test

Evaluation in group meetings revealed the limitation. The precursor is approximately
**30 kDa**, a size shared by a great many host cellular proteins, so SEC alone cannot reach
useful specificity.

### Rebuild

The purification approach had to change, and changing it **changed the construct**: a
His6 tag was incorporated next to proenkephalin.

### Retest

The His-tagged protein enables high-precision capture by **IMAC**, performed again at the
Hellenic Pasteur Institute on a Ni-NTA FPLC.

### Learn

The precursor cannot be isolated efficiently on size alone, because that size is
unremarkable among cellular proteins. Affinity capture succeeds where a physical property
shared with the background fails.

> **The revision this forced, recorded rather than smoothed over.** Our first-generation
> constructs carried **no affinity tag at all**, because purification had been treated as a
> step that came after expression. Taking the question to domain experts gave an answer that
> was obvious in hindsight: IMAC is affinity capture on immobilised nickel, and without a
> polyhistidine tag there is nothing for the column to hold.
>
> That turned a purification decision into a construct decision, and the two could no longer
> be made separately. For native PENK the constructs were re-ordered from Twist with the tag
> included, and those second-generation plasmids are what everything downstream used. For the
> **engineered** PENK sequence there was no time left to order complete plasmids, since full
> plasmid synthesis turns round more slowly than a linear gene fragment and the season would
> have closed first. The first-generation plasmids therefore served only as backbones for the
> engineered constructs and entered **no** expression, purification or maturation experiment.
>
> **The correction is to the order of work, not to the design.** The purification route
> should be specified alongside the expression cassette, because the former constrains the
> latter.

### Where the tag had to go

Once a tag was required, its position was not free. A carboxy-terminal tag would be carried
into the terminal Met-enkephalin-Arg-Phe peptide and **destroy one of the seven products**.
It therefore sits at the amino terminus of the mature protein, immediately downstream of the
native signal peptide so that the signal peptide remains amino-terminal and secretion is
unaffected. Verified in the ordered sequences: residues 1 to 24 are the native signal
peptide, His6 begins at residue 25.

---

## Cycle 3 · The enzyme set, corrected on paper

Proenkephalin carries its opioid cores buried inside one long chain, each flanked by paired
basic residues. **HEK293T cells carry the constitutive convertases and not the neuroendocrine
ones, and have no regulated secretory pathway at all**, so expression and maturation are
treated as two separable engineering problems rather than assuming the cell solves both.

### Design

The literature names PC1/3 and PC2 as the endoproteases acting on neuropeptide precursors,
often found together in the same secretory granules. Supply both and let them cut
proenkephalin between them.

### Build PC1/3 + PC2

The precursor expressed with a His tag and isolated by IMAC. **IMAC matters more than it
first appears**: it does not only remove contaminating protein, it yields a substrate that
can be **quantified**, so every enzyme amount downstream is defined per microgram of
substrate.

### Test PC1/3 + PC2

Each enzyme checked against what the literature reports it does, and the two checked against
each other.

### Learn PC1/3 + PC2

**The set is chemically incomplete.** Releasing the cores takes two different activities in a
fixed order: an endoprotease cuts at the paired sites, then an **exopeptidase** removes the
basic residues left at each new carboxy terminus. Two endoproteases cover the first activity
twice and the second not at all.

### Re-Design PC2 → CPE + Co²⁺

PC1/3 is dropped; **carboxypeptidase E** is added, supplying the one activity no endoprotease
performs. And CPE is never a specification on its own: it is a metallopeptidase whose
activity depends on a divalent metal, with reported conditions carrying **cobalt at 2 mM**.
The metal belongs to the enzyme, not to a later optimisation.

### Re-Build PC2 → CPE + Co²⁺

**Two sequential reactions rather than one, and the metal is what forces the sequence.**

The working assumption had been a single granule-like buffer with CPE added into the same
tube. That does not hold: **the same ion CPE requires inhibits PC2.** PC2 runs first in
acidic calcium conditions, and only once it has finished is CPE added with its cobalt. What
looked like one reaction with two enzymes is two reactions in sequence.

### Re-Test PC2 → CPE + Co²⁺

The second set checked the same way as the first: each enzyme against the literature, and
the two against each other. Does the set cover both activities? Are the conditions
compatible? What is left at the ends?

### Re-Learn PC2 → CPE + Co²⁺

The design closes: a chemically complete enzyme set, in the order and conditions its enzymes
require. **The incompatibility was found on paper, where it costs nothing, rather than in a
reaction that would simply have underperformed.** Two enzymes that each work do not make a
working set until their conditions are compared.

**What this cycle cannot claim.** The conclusion concerns the enzyme set, not yield. Which
cores are released in what proportion is not something a literature check settles.

**And the digestion is a model, not the therapy.** CNS neurons carry PC2, CPE and a regulated
secretory pathway of their own, so what is reconstructed here on the bench happens
endogenously in the patient.

*Dry lab support for this cycle:* predicted structures of both precursors, with solvent
accessibility measured at all twelve dibasic sites PC2 must cut. Across the twelve
corresponding sites, 0.411 native versus 0.343 engineered, p = 0.160. No evidence that
recoding buries the processing sites. Reported as a **weak negative only**, because
prediction confidence was below the band where per-residue burial is interpretable. Details
and the withdrawn finding are on the Model page.

---

## Cycle 4 · Testing that the product works

To test the matured peptide we have to examine its binding to the mu and delta opioid
receptors, both of which sit on the external cell surface.

### Design

The matured enkephalin must bind its receptors with high affinity, which requires that in
vitro maturation produced a product correctly cut and correctly folded.

### Build

Two 96-well ELISA plates coated separately with the two receptors, followed by reciprocal
dilutions of the matured peptide and detection of the receptor-peptide complex.

### Test

Evaluation made clear the ELISA signal might not meet expectations, **and that such weakness
is often unrelated to actual binding ability**. Replicating brain-like conditions in a
coated well is the difficulty, not the protein.

### Rebuild

Two additional plasmids were constructed, one for the mu receptor and one for the delta
receptor, and used to transfect cells as the original construct was. The readout moves from
a plate-bound binding assay to a **cellular functional** one.

### Retest

The **cAMP-Glo assay** with forskolin, following the protocol supplied with the commercial
kit.

### Learn

Two methodological conclusions. First, **a weak initial ELISA signal does not imply incorrect
protein structure**, since signal strength depends heavily on assay conditions. Second, a
functional readout in cells answers the question the plate assay was being asked to answer,
and answers it under conditions closer to the target tissue.

*Dry lab support for this cycle:* a delta/mu selectivity model calibrated against thirteen
published reference opioids, r = 0.805, p = 0.0009, correct sign on 12 of 13. Applied to the
engineered payload it gives +1.23 +/- 1.76 kcal/mol delta over mu. **That interval includes
zero**, so delta preference is stated throughout as a design goal rather than a demonstrated
result. The cAMP assay in this cycle is the instrument that settles it.

---

## Scope, stated plainly

This chain runs four steps: **construct design, expression, affinity capture, in vitro
maturation.** The season closed with that chain complete and no further.

Within it, the constructs are expressed **transiently** rather than from stable selected
lines, which suits a workflow whose purpose is to generate precursor for purification inside
a short window. The digestion is reconstituted enzymatically in a tube rather than carried
out by the cell, which gives control over it but does not demonstrate that a cell expressing
the construct performs the same chemistry.

**These are proof-of-principle results.** They establish that the construct expresses, that
the precursor can be captured, and that it is a substrate for the maturation reaction.
