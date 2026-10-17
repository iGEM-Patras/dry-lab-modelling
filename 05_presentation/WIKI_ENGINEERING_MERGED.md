# Engineering

> Four cycles. Every one of them changed a design, and three changed it because something did
> not work. The wet lab's record is the spine of this page; where the dry lab fed a decision,
> its contribution is marked in an indented block inside the relevant cycle.

Each cycle below follows Design, Build, Test, Learn, and is counted only where the Learn step
altered the next Design. The dry-lab work that supports these cycles, including the cycles
that produced no usable result, is documented separately on our Model page and in the
repository.

## Overview

| cycle | what it had to solve | what changed, and why |
|---|---|---|
| 1 | one plasmid, two proteins | two coding sequences in a row translate as one fused protein, so a separating element was required and all four architectures were built |
| 2 | isolating a 30 kDa precursor | size exclusion cannot separate it from host proteins of the same size, which turned a purification decision into a construct decision |
| 3 | maturation in a tube | the cobalt that carboxypeptidase E needs inhibits the convertase that must act first, so one reaction became two in sequence |
| 4 | does the product work | a weak ELISA signal would not have meant a misfolded peptide, so the readout moved to a functional cAMP assay |


---

## Cycle 1 · One plasmid, two proteins

One plasmid has to deliver proenkephalin, which is the product, and mEGFP, which reports that the cell received the construct. Getting two proteins instead of one took three turns of the loop. Pick an iteration, then click a quadrant of the wheel.


**Two genes, nothing between them**


### Design

The first design was the economical one: a single CMV promoter, a Kozak sequence, and the two coding sequences placed one after the other. One promoter, one transcript, two proteins , or so the map suggested. It needed no additional parts and kept the plasmid small.

A mammalian promoter transcribes one mRNA, and a ribosome that starts at the first AUG translates until it meets a stop codon. That fact is what the design quietly assumed away.


### Build

The construct was assembled in silico first, as a complete annotated map. Doing that before ordering any DNA is what made the next step possible at no cost.


### Test

The construct was translated in silico from the Kozak sequence onward, and the predicted product was examined rather than assumed.


### Learn

The construct does not make two proteins. With nothing between them, the ribosome reads through from the first start codon to the last stop codon and produces one continuous PENK-mEGFP polypeptide.

That defeats both purposes at once. Proenkephalin's last opioid core is its own C-terminal sequence, so a whole fluorescent protein hanging off that end buries the core where the processing enzymes cannot release it. mEGFP is tethered to a protein carrying a signal peptide and is pulled into the secretory pathway instead of staying in the cytosol where it folds and reports. And since the two are one molecule, purifying one purifies the other.

The conclusion is structural, not a matter of optimisation: something has to sit between the genes, and what sits there defines the next iteration.


**Two ways to separate, two orders for each**


### Re-Design

Two elements can give two proteins from one transcript, by different mechanisms. An internal ribosome entry site allows a second, independent initiation on the same mRNA, so each gene keeps its own start and stop codon and each protein is made whole and unmodified. A P2A peptide keeps one reading frame but makes the ribosome skip the formation of one peptide bond, releasing two polypeptides from a single translation event.

A second question followed immediately, and first principles did not settle it: which gene should come first. Rather than guess, both orders were built for each element.


### Re-Build

Four plasmids on the same backbone and the same CMV promoter, differing only in the separating element and the order of the two genes.


### Re-Test

Each construct was translated in silico, as in iteration 1, and the predicted products inspected: how many polypeptides come out, and what each one carries at its ends.


### Re-Learn

All four solve the problem of iteration 1 ,  every one yields two separate proteins ,  so the question changes rather than closes.

What the four do not share is what they cost. The two IRES constructs leave both proteins with native ends but place one gene in the strong cap-dependent position and the other in a weaker, independently initiated one. The two P2A constructs make both proteins from one event but leave a peptide scar on each: about twenty residues on the C-terminus of whichever protein comes first, and a proline on the N-terminus of the second. Since proenkephalin's C-terminal residues are themselves an opioid core, the two P2A constructs are not interchangeable with each other either.

The decision now rests on predicted yield and on where each scar falls.


> **Dry lab contribution.** The failure in this cycle was found by translating the proposed
> arrangement rather than by building it. Reading the two coding sequences as one open
> reading frame returns a single continuous polypeptide, which places the carboxy-terminal
> opioid core inside a fusion protein where the maturation enzymes cannot reach it. That
> result cost nothing and was available before any DNA was ordered.
>
> The dry lab also built all four candidate architectures in silico and checked each against
> the synthesis vendor's constraints before ordering. The first ordering-ready set was
> rejected, and the cause was not the payload: the two terminal flanking sequences were exact
> reverse complements of each other, a defect inherited from existing files rather than
> introduced here. All four corrected constructs were subsequently accepted.


---

## Cycle 2 · Purifying the precursor


**Engineering cycle (2)**


**Proenkephalin purification process**

Right after the cell cultures were complete, the most potent plasmid out of all four constructs was chosen. The next step was to extract the produced protein from the cells. In this following DBTL cycle, we document our troubleshooting process for finding out how we can maximize the amount and purity of our protein samples.


### Design

The purification method that was first chosen was Size Exclusion Chromatography (SEC). By SEC we can filter away all the proteins the media includes by size, and consequently only receive our protein of interest on a significantly higher percentage.


### Build

SEC was to be conducted at Hellenic Pasteur Institute, under the supervision of Dr.M.Zouridakis. A small analytical column would help us isolate proenkephalin, and his lab’s equipment would be of use for this experimental step.


### Test

Evaluation during group meetings revealed a critical limitation.

The size of the target protein (approximately 30 kDa) is shared by a great number of host cellular proteins, making isolation by SEC alone insufficient to achieve high specificity.

It became obvious that our protein purification approach had to be redesigned, in order to boost specificity.


### Re-build

A change in the protein purification approach was necessary.

Thus, we altered the plasmid construct to incorporate a His-tag sequence next to the one of proenkephalin.


### Re-test

The newly designed His-tagged protein enables high-precision extraction via IMAC. This method was performed again at Hellenic Pasteur Institute, under the supervision of Dr.M.Zouridakis. A Ni-NTA FPLC isolation column was used.


### Learn

The produced proenkephalin cannot be isolated efficiently, solely based on its size, as this is common among other cellular proteins. Nevertheless, thanks to the strong affinity of histidine for nickel ions, the His-tagged protein can easily be eluted from the column, and then be separated from the culture supernatant.


> **Dry lab contribution.** The tag position was decided on biological grounds before any
> technical criterion was applied. Proenkephalin terminates in Met-enkephalin-Arg-Phe, which
> is itself one of the seven products, so a carboxy-terminal tag would have been carried into
> that peptide and destroyed it. The tag therefore sits at the amino terminus of the mature
> protein, immediately downstream of the native signal peptide so that secretion is
> unaffected. Translating the ordered construct confirms the arrangement: the signal peptide
> occupies residues 1 to 24 and the tag begins at residue 25.
>
> A note for anyone reading our figures: an earlier caption described the tag as sitting
> upstream of the signal peptide. That is the wrong way round, and a tag genuinely upstream
> of a signal peptide would prevent secretion entirely. The design is correct; the caption
> was not, and has been fixed.


---

## Cycle 3 · In vitro maturation of proenkephalin


**In vitro maturation of proenkephalin**

Proenkephalin is not a drug. It is a precursor that becomes one only when it is cut in the right places, by the right enzymes, in the right order. Eight steps, two turns of the design-build-test-learn loop: the first supplied the two convertases the literature associates with neuropeptide precursors, the second replaced that set with the one this chemistry actually requires ,  an endoprotease followed by a carboxypeptidase with its cobalt cofactor ,  and specified a way of finding out whether it had worked. Both turns were closed on paper: each test is a check of the design against published biochemistry, not bench data.


### Design

The prohormone convertase literature names PC1/3 and PC2 as the two endoproteases that act on neuropeptide precursors, and the two are often found together in the same secretory granules.

So the plan was to supply both and let them cut proenkephalin between them.


**Testable hypothesis**

If the precursor is cleaved at its paired basic sites, enkephalins are released and the opioid receptors are activated.


**The chemistry that has to be reproduced**

Proenkephalin carries its opioid cores buried inside a single long chain, each one flanked by paired basic residues.

Releasing them takes two different enzymatic activities in a fixed order: an endoprotease cuts at the paired sites, an exopeptidase then removes the basic residues left at the new C-terminus.


### Build PC1/3 + PC2


**His-tagged PENK→IMAC→quantified substrate→digestion**


**Substrate**

The precursor is to be expressed with a His tag and isolated by immobilised metal affinity chromatography.

IMAC matters more than it first appears: it does not only remove contaminating protein, it gives a substrate that can be quantified, so every enzyme amount downstream can be defined per microgram of substrate.

Without a clean, measurable precursor there is no meaningful enzyme-to-substrate ratio.


**Digestion**

Both convertases together, in the granule-like acidic, calcium-containing conditions at which they work.


### Test PC1/3 + PC2

The test is done on the sequence, not at the bench: each candidate enzyme is mapped onto proenkephalin and against what the literature reports it does.

which sites it accounts for→do the two overlap?→state of the released fragments


**The two convertases, mapped onto proenkephalin**

The gap in the enzyme set is visible on paper, before any material is spent


### Learn PC1/3 + PC2

Two conclusions, one cheap and one fundamental.


**…YGGF-KR→extended intermediate→pharmacologically silent**


**The cheap one**

PC1/3 is not essential. On proenkephalin it cleaves the same paired basic motifs as PC2, and PC2 is the convertase associated with producing the enkephalins that act at the µ- and δ-opioid receptors. Supplying both adds cost without adding product.


**The fundamental one**

This version could not have worked, for a reason that had nothing to do with the choice between convertases.

Cleaving at a paired basic site leaves those residues attached to the C-terminus of the fragment, and a peptide ending in -KR or -R is an extended intermediate rather than an enkephalin.

Only after trimming does the YGGF motif sit at a free N-terminus, where the tyrosine amine can form the salt bridge with the conserved aspartate of the opioid receptor. Before that the molecule is silent ,  not weakly active, but silent.

What the enzyme set was missing was never a second endoprotease; it was a carboxypeptidase.


### Re-Design PC2 → CPE + Co²⁺

The enzyme set becomes PC2 followed by carboxypeptidase E with cobalt, and the order between them is a dependency rather than a preference.


**PC2 endoprotease→then CPE + Co²⁺→free N-terminal YGGF**


**The corrected set**

PC1/3 is dropped; CPE is added. The exopeptidase supplies the one activity no endoprotease performs.

CPE is never specified on its own. It is a metallopeptidase, its catalytic activity depends on a divalent metal ion, and the reported conditions for this chemistry carry cobalt at 2 mM. Cobalt is not an additive to consider later; it belongs to the enzyme.

Both enzymes are used as mature, catalytically active recombinant proteins, so the maturation of the enzymes themselves is not an additional variable.


**What this cycle adds**

What the first one lacked: the exopeptidase activity itself, and with it a set that can be checked for completeness rather than assumed to be complete.


### Re-Build  PC2 → CPE + Co²⁺

Two sequential reactions rather than one, and the metal is what forces the sequence.


**PC2 · acidic, Ca²⁺→finish→CPE + Co²⁺→trimmed product**


**Why the two stages cannot be combined**

The working assumption had been one granule-like buffer for both enzymes, with CPE added into the same tube.

That does not hold: the same ion CPE requires inhibits PC2. PC2 runs first in acidic calcium conditions, and only once it has finished is CPE added together with its cobalt.

What looked like one reaction with two enzymes is really two reactions in sequence.


**What stays fixed**

The same IMAC-purified, quantified precursor, so enzyme-to-substrate ratios carry over from the first cycle.

Acidic pH and calcium for the endoproteolytic stage ,  the conditions at which PC2 shows its optimum.


### Re-Test PC2 → CPE + Co²⁺

The second set is checked the same way as the first: each enzyme against what the literature reports it does, and the two against each other.

does the set cover both activities?→are the conditions compatible?→what is left at the ends?


**The two stages, checked against each other**


**What the check settles**

The set now covers both required activities, which the first one did not.

The incompatibility between the two stages is found on paper, where it costs nothing, rather than in a reaction that would simply have underperformed.

Two enzymes that each work do not make a working set until their conditions are compared.


### Re-Learn PC2 → CPE + Co²⁺

The design now closes: a chemically complete enzyme set, in the order and conditions its enzymes require.


**PC2 → CPE + Co²⁺→both activities covered→sequence fixed**


**What the two cycles establish**

Maturation needs two classes of enzyme, not two convertases: an endoprotease to cut at the paired basic sites, then a carboxypeptidase to remove them.

PC1/3 is redundant on this precursor, and dropping it costs nothing.

CPE and cobalt are a single specification; without the metal the trimming step is the one that limits everything downstream.


**What this cycle cannot claim**

The conclusion is about the enzyme set, not about yield. Which of the cores is released in what proportion is not something a literature check can settle, and the claim is kept at the level the design supports.


**What the cycle demonstrates**

A precursor is defined by the enzymes that process it, not only by its sequence. One turn removed an enzyme that was not working, the other added the activity without which the products are not drugs and the cofactor without which that activity does not run. Neither could have been found by looking at the plasmid, and neither needed a failed experiment to find ,  only the published biochemistry of the enzymes themselves.

The digestion is a model, not the therapy: CNS neurons carry PC2, CPE and the regulated secretory pathway of their own, so what is reconstructed here on the bench happens endogenously in the patient.

Right enzymes, right order, right cofactor ,  established before a single reaction is set up.

file:///C:/Users/usert/Desktop/IGEM/Proenkephalin%20Maturation%20Cycles.html


> **Dry lab contribution.** The reason this reaction is reconstituted in a tube rather than
> left to the cell is a property of the chassis. HEK293T carries the constitutive secretory
> machinery but not the neuroendocrine convertases, and has no regulated secretory pathway,
> so a precursor expressed there is not matured by the cell that makes it. Separating
> expression from maturation was therefore a requirement rather than a convenience.
>
> The dry lab also mapped the paired basic sites on both the native and the engineered
> precursor. Both carry twelve dibasic sites of the same types in the same order, so recoding
> the payload cassettes did not add or remove a cleavage site. Whether recoding changed how
> accessible those sites are is a separate question, and our attempt to answer it
> computationally did not produce a result we are willing to stand behind: the structure
> predictions came back at confidence too low for per-residue interpretation. Across all
> twelve corresponding sites the engineered precursor was not systematically less accessible
> than the native one, which we report as a weak negative rather than as evidence. Mass
> spectrometry on the digest settles it directly.


---

## Cycle 4 · Protein functionality testing

In order to test the functionality of enkephalin, after its in vitro maturation, we have to examine its binding ability to the MOR and DOR receptors. These receptors are both located externally on the cellular membrane of neurons.


### Design

The matured enkephalin must bind to its receptors with high affinity, and in vitro maturation requires ensuring that the final product is properly cut and folded in three-dimensional space to interact with receptors without disruptions. To verify this, the initial approach was designed around an ELISA binding assay.


### Build

Two 96-well ELISA plates were coated separately with the two receptors, followed by the addition of reciprocal dilutions of the matured enkephalin. The resulting receptor-enkephalin complex was then detected through the specific binding of a signaling antibody.


### Test

During evaluation, it became clear that the ELISA signal might not meet expectations, and such weakness is often unrelated to the protein's actual binding ability. Replicating brain-like conditions in vitro is exceptionally difficult and demands extensive optimization. Because of these parameters and a restricted time frame, the team shifted toward measuring binding ability indirectly.


### Re-build

To implement this shift, two additional plasmids were constructed, one for the MOR receptor and one for the DOR receptor. These plasmids were used to transfect cells similarly to the original construct, except they directed the expression of the receptors on the cell membrane rather than secreting them. Matured enkephalin was subsequently added to the cell cultures to allow functional evaluation via a cAMP assay.


### Re-test

The cAMP-Glo assay was deployed alongside forskolin, following the standardized protocol provided directly as part of the commercial assay kit.


### Learn

The transition yielded two clear takeaways regarding methodology. First, a weak initial ELISA signal does not imply incorrect protein structure, as signal strength is heavily dependent on extensive assay optimization. Second, the cAMP assay avoids this bottleneck by functioning as a ready-to-use kit that requires no internal optimization. The results proved accurate and straightforward to interpret, since a reduction in cellular cAMP acts as a reliable indirect indicator of successful protein binding.


> **Dry lab contribution, and a limit we want stated here rather than found later.** This
> cycle is the arbiter for the central pharmacological claim of the project, and the dry lab
> could not settle that claim computationally. Nine routes were attempted and are documented
> with their pre-registered gates in the dry-lab repository. The best calibrated estimate the
> dry lab can offer is a delta-over-mu preference of +1.23 kcal/mol with an uncertainty of
> 1.76, an interval that includes zero and is not separable from native Met-enkephalin.
>
> Two general lessons rule out whole classes of method rather than individual attempts.
> Anything anchored to published affinity values inherits a disagreement between sources that
> is larger than the effect being measured, and anything computing selectivity as the
> difference between two large absolute energies accumulates correlated error along the
> calculation. A free-energy campaign built to avoid the second problem fixed the diagnostic
> it was designed to fix and still failed its reproducibility check.
>
> **Delta-preference is therefore a design goal and not a demonstrated result.** The cAMP
> assay in this cycle, with selective antagonists establishing specificity, is the instrument
> that measures it, and it is subject to none of the constraints above. This is the clearest
> case in the project of modelling defining an experiment rather than replacing one.
