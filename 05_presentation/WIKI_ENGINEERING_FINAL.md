# Engineering

> Nineteen design cycles. Eight of them failed, and the failures are on this page because
> they are what the record is worth.

Every cycle on this page follows Design, Build, Test, Learn, and a cycle is counted only
when the Learn step changed the next Design. Gates were written into the repository and
pushed **before** the test that scored them, so the pass or fail is auditable in version
history rather than asserted afterwards.

---

## Why a precursor, and the problem that creates

Enkephalins cannot be expressed as peptides. The native route is proenkephalin, a single
precursor carrying seven opioid cores separated by paired basic residues. Releasing them
takes two enzyme activities in a fixed order: an endoprotease, proprotein convertase 2,
cuts at the paired sites with its chaperone 7B2, and carboxypeptidase E then trims the
basic residues left behind.

**HEK293T cells, our expression host, carry the constitutive convertases and not the
neuroendocrine ones, and have no regulated secretory pathway at all.** We therefore treat
expression and maturation as two separable engineering problems rather than assuming the
cell solves both. That decision generated the first pair of cycles.

---

## Cycles 1 to 2 · The enzyme set, corrected on paper

**Design.** The literature names PC1/3 and PC2 as the endoproteases acting on neuropeptide
precursors, often in the same granules. The first plan supplied both and let them cut
proenkephalin between them.

**Learn.** That set is chemically incomplete. Two endoproteases cover one activity twice
and the other not at all. The basic residues left at each new carboxy terminus need an
**exopeptidase**, which neither convertase performs.

**Cycle 2 Design.** PC1/3 dropped, CPE added. And CPE is never a specification on its own:
it is a metallopeptidase whose activity requires a divalent metal, reported at **2 mM
cobalt**. The metal belongs to the enzyme, not to a later optimisation.

**The cycle's real finding, and it was found on paper.** The working assumption had been
one granule-like buffer with both enzymes in the same tube. **The same cobalt CPE requires
inhibits PC2.** What looked like one reaction with two enzymes is two reactions in
sequence: PC2 first in acidic calcium conditions, then CPE with its cobalt once PC2 has
finished.

**What it cannot claim.** The conclusion concerns the enzyme set, not yield. Which cores
are released in what proportion is not something a literature check settles.

**And the digestion is a model, not the therapy.** CNS neurons carry PC2, CPE and a
regulated secretory pathway of their own, so what is reconstructed on the bench happens
endogenously in the patient.

---

## Cycles 3 to 6 · Four constructs, and a vendor rejection that was ours

**Design.** A 2x2 matrix varying two parameters independently: the bicistronic linker
(IRES or P2A) and the position of the fluorescent reporter. IRES permits cap-independent
translation of the second cistron but typically reduces its expression; P2A gives
near-stoichiometric ratios at the cost of a residual peptide tag. All four sit in a
pcDNA3.1(+) backbone onboarded as a custom Twist vector.

**The tag decision.** In all four constructs the His6 tag sits at the amino terminus of the
mature protein, immediately **after** the native signal peptide rather than before it, so
the signal peptide stays amino-terminal and secretion is unaffected. A carboxy-terminal tag
would be carried into the terminal Met-enkephalin-Arg-Phe peptide and destroy one of the
seven products. Verified in the ordered sequences: residues 1 to 24 are the native signal
peptide, His6 begins at residue 25.

**Build failure, and the diagnosis.** The vendor rejected the first ordering-ready set. The
fault was not in the payload: two terminal flanking sequences were exact reverse
complements of each other, a defect inherited from existing lab files and carried forward
untested as a pair.

**Learn.** Inherited sequence is still untested sequence. Every flank is now scanned on
both strands before an order leaves.

---

## Cycle 7 · Calibrating before predicting

**Design.** No selectivity prediction means anything without knowing the method's error on
compounds whose answer is published. Thirteen reference opioids, gates committed first.

**Test.** Correlation with published delta/mu selectivity **r = 0.805, p = 0.0009**, with
the **correct sign on 12 of 13**.

**Result.** Applied to the engineered payload: **+1.23 +/- 1.76 kcal/mol** delta over mu.

**Learn, and this governs the whole project.** That interval **includes zero**. The payload
is not statistically separable from native Met-enkephalin on this measure.
**Delta preference is a design goal, not a demonstrated result**, and no later cycle changed
that.

---

## Cycle 14 · The free-energy ladder: right diagnosis, failed calculation

**Design.** An earlier alchemical attempt had failed its control, with replicates differing
only by thermostat seed giving opposite signs. Rather than call the method noisy, we
measured why: work distributions overlapped poorly, concentrated in the engineered-peptide
legs, and the cause was **lambda spacing rather than sampling time**, because at fixed
spacing the perturbation per window grows with the size of the decoupled solute.

**Build.** The ladder was rebuilt from 27 to **57 windows** spaced by equal thermodynamic
length rather than by subdivision. Gates were committed before any window ran.

**Test.**

| gate | result |
|---|---|
| phase-space overlap | **PASS**, decisively: 0 of 56 intervals above threshold, against 20 to 21 of 25 on the old ladder |
| replicate reproducibility | **FAIL**: +0.72 +/- 3.13 and +14.47 +/- 3.28 kcal/mol, a 13.75 spread against a combined error of 4.53 |

**Learn.** The diagnosis was correct and the fix did exactly what it was designed to do.
The calculation failed anyway, and for a reason the fix created: **doubling the windows to
repair overlap doubled the number of terms whose small biases accumulate.** Decomposing the
disagreement per interval found no pathological window, but a large majority of intervals
shared their leg's sign, with the two legs drifting in opposite directions so errors added
rather than cancelled.

**The first replicate landed close to the published control value.** Had we stopped there,
we would have reported a result that looked like a triumph. The reproducibility gate is
what caught it, and it was pre-registered precisely for this.

---

## Cycle 17 · Engagement order, with a control that recovered nothing

**Design.** Does the engineered payload engage the delta receptor in the same domain order
as deltorphin, whose address it carries? The delta receptor has been crystallised with
deltorphin bound (PDB 8F7S), and that structure shares the five residues `FEVVG` with our
payload. This is the first computational question in the project with an experimental bound
reference.

**Gate G1, native recovery.** Blind docking must re-find the crystal pose before anything
else is scored.

**Test.** Recovered to **3.41 A**, with 4 of 32 models within 5 A, from a random
conformation at a random location, and **without** the membrane term the source method used.

**What makes it believable.** A deliberately under-sampled run, written only as a pipeline
guard, recovered **nothing** (best 39.05 A). A bug in our own pose selection would have
produced low values in both. The signal being sampling-dependent is what rules out an
artefact.

**Status.** G2 and G3 are running: 15 simulations per arm, 150 replica trajectories each.
Deltorphin must reproduce the published engagement asymmetry before the engineered payload
is scored at all.

---

## Cycle 18 · Every gate passed, and we withdrew the result

**Design.** Can the payload be **released**? Nobody had asked that about a construct already
ordered, and it bears directly on the PC2 chemistry above. Structures of the engineered and
native precursors were predicted and solvent accessibility measured at all twelve dibasic
sites. Both precursors carry the same twelve dibasic types in the same order.

**Test.** All three gates passed. Three engineered cassettes came out less accessible than
any native site, each separable at p < 0.05. That reads as a clean, wet-lab-actionable
finding.

**Learn, and the fault is in our gate.** Two diagnostics overturn it:

1. **Confidence.** Mean pLDDT **43.2** native and **37.1** engineered, both below the band
   where per-residue burial is interpretable. Biologically unsurprising for a disordered
   secretory precursor, but not a measurement.
2. **The control has no site-level resolution.** In the native precursor, site-to-site
   variation was *smaller* than the scatter between repeated predictions of the same
   sequence.

Our control gate asked whether sites look exposed, which a disordered chain satisfies
trivially. It never asked whether the method can tell one site from another, which is the
capability the real question depends on. **The three flags are withdrawn.** The
pre-registration is recorded as inadequate rather than quietly amended.

**What is reportable**, and it needs no per-site resolution: across all twelve
corresponding sites, **0.411 native versus 0.343 engineered, p = 0.160**. No evidence that
recoding systematically buries the processing sites. A weak negative, and genuinely
reassuring about the ordered construct.

---

## Cycle 19 · A learned method, validated rather than assumed

**Design.** A graph neural network trained on peptide-GPCR complexes, suggested
independently by a bioinformatician colleague. Before spending any compute on our own
receptors, reproduce the authors' result on their data.

**Test, on an unseen receptor clade.** Reading the weight files rather than the
documentation showed the ten pretrained models are a **phylogenetic leave-one-out set**,
each excluding one receptor clade. Scoring a listed receptor with the full ensemble is
therefore leaky.

| | AUC |
|---|---|
| full ensemble (9 of 10 trained on this clade) | 0.944 |
| **held-out model** | **0.893**, p = 3.2e-16 |

**And it discriminates which receptor**, which is the shape of our own question. 42 peptides
bind exactly one of two receptors; the score favours the correct one 39 times. That number
alone is confounded, because 41 of the 42 bind the same receptor and a constant offset would
reproduce it. The offset is real and large: among peptides binding **neither** receptor, one
scores higher 76.1% of the time. Against that null rather than against chance, the binders
still come out higher at **p = 0.003**.

**Learn.** The capability is demonstrated rather than assumed. The limits are stated with
it: the two receptors tested are different families, where the delta and mu opioid receptors
share **18 of 29** orthosteric pocket residues, and the training set is entirely *C. elegans*.

---

## What the engineering record adds up to

**Eight routes to a computational selectivity number have now been ruled out**, each on the
same published criterion: the method's own reported error must be smaller than the
0.81 kcal/mol effect we need to resolve. Two general failure modes rule out classes rather
than instances. Anything anchored to published affinities inherits a between-source
disagreement larger than the effect. Anything computing selectivity as a difference of two
large absolutes accumulates correlated per-window bias, which is exactly how Cycle 14 failed.

**The project's best selectivity estimate remains Cycle 7's +1.23 +/- 1.76 kcal/mol, with
its interval including zero.**

The instrument that settles it is not a model. It is a cAMP assay at both receptors with
selective antagonists, and that is the next experiment.
