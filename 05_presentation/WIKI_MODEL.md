# Model

> A model that cannot state its own error is not a model. Everything on this page is
> reported with the calibration that bounds it, and where a method failed its own test we
> say so rather than quoting the number it produced.

---

## 1 · What is being modelled, and why it is hard

The engineered payload `YGGFEVVG` grafts the deltorphin carboxy-terminal address onto the
enkephalin message, with the aim of biasing the precursor's sevenfold amplification toward
the delta-opioid receptor and away from mu, where tolerance builds.

**The quantity to resolve is small.** Native Met-enkephalin's published delta over mu
selectivity corresponds to **0.81 kcal/mol**. The most delta-preferring compound in our own
thirteen-compound reference panel is about 31-fold, roughly 2.1 kcal/mol. Any method whose
reported error exceeds the effect cannot answer the question, however sophisticated it is.

**That single criterion has governed every method decision in this project**, and it has
ruled out eight routes.

---

## 2 · Calibration before prediction

A selectivity model was calibrated against **thirteen published reference opioids** spanning
mu-selective, delta-selective and mixed pharmacology, before being applied to our own
sequence.

| | |
|---|---|
| correlation with published selectivity | **r = 0.805** |
| significance | **p = 0.0009** |
| direction correct | **12 of 13 compounds** |

This is the figure we would defend first, because it is the only one that licenses anything
else on this page.

### What the calibrated model says about our payload

**+1.23 +/- 1.76 kcal/mol** delta over mu.

**The interval includes zero.** The payload is not statistically separable from native
Met-enkephalin on this measure. Throughout the project, in the abstract, on the poster and
in the Registry entry, we therefore say **delta preference is a design goal, not a
demonstrated result**. No later work changed that, and two later methods pushed against it.

---

## 3 · The free-energy calculation, and why we do not quote its number

An alchemical free-energy calculation was built to test the same question from first
principles. It is the most expensive thing the dry lab attempted, and it **failed its own
pre-registered gate**. The number it produced is not on this page as a result, and the
reason is worth more than the number would have been.

**First attempt.** Replicates differing only by thermostat seed gave opposite signs. Rather
than calling the method noisy, per-interval overlap diagnostics identified the cause: work
distributions overlapped poorly, concentrated in the engineered-peptide legs, and the driver
was **lambda spacing rather than sampling time**, because at fixed spacing the perturbation
per window grows with the size of the decoupled solute.

**Rebuild.** 27 windows to **57**, spaced by equal thermodynamic length. Gates committed
before any window ran.

**Outcome.**

| gate | result |
|---|---|
| phase-space overlap | **PASS**, 0 of 56 intervals above threshold against 20 to 21 of 25 before |
| replicate reproducibility | **FAIL**, +0.72 +/- 3.13 versus +14.47 +/- 3.28 kcal/mol |

The diagnosis was right and the fix worked. The calculation failed for a reason the fix
created: **doubling the windows to repair overlap doubled the number of terms whose small
biases accumulate.** No single interval was pathological, but most shared their leg's sign,
and the two legs drifted in opposite directions so errors added instead of cancelling.

**The first replicate landed close to the published control value.** Reporting it alone would
have looked like a success. The reproducibility gate, written before either replicate ran,
is what prevented that.

---

## 4 · A learned method, validated rather than cited

A graph neural network over peptide-GPCR complexes was suggested independently by a
bioinformatician colleague. Before spending compute on our receptors, we reproduced the
authors' own result on their data, with their weights.

**A detail that changes the arithmetic**, read from the weight files rather than the
documentation: the ten pretrained models are a **phylogenetic leave-one-out set**, each
excluding one receptor clade. Scoring a listed receptor with the full ensemble is leaky.

| scoring an unseen receptor clade, 41 agonists among 339 peptides | AUC |
|---|---|
| full ensemble (9 of 10 trained on that clade) | 0.944 |
| **held-out model, honest** | **0.893** (p = 3.2e-16) |

**It also discriminates which receptor**, which is the shape of our own question. Of 42
peptides binding exactly one of two receptors, the score favours the correct one 39 times.
**That figure alone is confounded**, because 41 of the 42 bind the same receptor and a
constant score offset would reproduce it with no discrimination at all. The offset is real:
among peptides binding **neither** receptor, one scores higher 76.1% of the time. Measured
against that null instead of against chance, the binders still come out higher,
**p = 0.003**, and the within-peptide score gap gives p = 7e-10 independently.

**What it does not do.** The two receptors tested are different families. The delta and mu
opioid receptors share **18 of 29** orthosteric pocket residues, a far finer discrimination.
The training set is entirely *C. elegans*. And the output is an agonist score, never
kcal/mol, so it cannot produce a selectivity value. Before it is ever applied to our payload,
it runs against the thirteen-compound calibration panel: if it cannot rank compounds of known
delta/mu preference, it cannot rank ours.

---

## 5 · The rest of the modelling, each with its limit stated

**Lipoplex formulation.** Coarse-grained molecular dynamics, **200 ns across three
independent replicates**, confirmed the mechanism expected of an ionisable lipid:
protonation at endosomal pH drives the structural change underlying endosomal escape. The
formulation was evaluated rather than assumed.

**Structural grounding.** The delta-opioid receptor has been crystallised with deltorphin
bound (PDB **8F7S**), sharing five residues `FEVVG` with our payload. Blind docking recovered
that crystal pose to **3.41 A**, 4 of 32 models within 5 A. A deliberately under-sampled
control recovered **nothing** (39.05 A), which is what rules out an artefact of our own pose
selection. This validates the docking protocol; it is not a selectivity result.

**And the analysis we built on it failed its own control.** Having a working docking
protocol, we asked a further question from a 2026 preprint: do opioid peptides engage
message-domain first or address-domain first, and is one order more productive? The control
requirement was that deltorphin reproduce the published asymmetry, **18.8 % versus 5.0 %**,
before our payload was scored at all.

Over the full pre-registered campaign, **150 trajectories, 15 independent seeds**, it did
not. Address-first trajectories reached a native-like pose **13.8 %** of the time against
message-first at **11.8 %**: an odds ratio of **1.20** where the published effect corresponds
to roughly **4.4**, at p = 0.51 with **0.74 power** to detect the published effect. The
campaign ran to its designed size, so sample size is not an explanation available to us.

**Our payload was therefore never scored on this measure**, and we note that its partial
data looked *favourable*: an odds ratio of 2.78 in the published direction. We are not
reporting it. A measurement from a method that could not detect the effect on a positive
control is not weak evidence, it is not evidence, and the ordering that forbids reporting it
was registered before any simulation ran precisely so that this decision would not be ours
to make after seeing the number.

**Processing-site accessibility.** Predicted structures of the engineered and native
precursors, with solvent accessibility measured at all twelve dibasic sites. Across all
twelve corresponding sites: **0.411 native versus 0.343 engineered, p = 0.160.** No evidence
that recoding systematically buries the sites PC2 must cut.

Three sites initially appeared less accessible at p < 0.05. **We withdrew that finding.**
Prediction confidence was pLDDT 43 and 37, below the band where per-residue burial is
interpretable, and in the native control the site-to-site variation was smaller than the
scatter between repeated predictions of the same sequence. Our gate had asked whether sites
look exposed, which a disordered precursor satisfies trivially, rather than whether the
method can tell one site from another.

**Immunogenicity.** Predicted MHC class I binding across **6,120 allele-peptide pairs**:
1.86% strong binders for the engineered epitope against **1.77%** for the native epitope it
replaces. Not meaningfully more immunogenic than the sequence it displaces. A screen, not a
clearance: class I prediction addresses CD8 recognition of an intracellular product, not
antibody responses to a secreted peptide.

**Silencing arm.** From **206** duplex candidates against the neprilysin transcript, two were
selected on predicted potency, seed-region binding energy, transcriptome-wide off-target
profile, local structural accessibility and coverage of all four isoforms. One top-ranked
candidate was discarded for a high-frequency single-nucleotide polymorphism in its target
site. Every candidate was also screened against our own expression cassette, so the silencer
cannot target the transcript it exists to protect.

---

## 6 · What the modelling is for, and what it is not

**Eight routes to a computational selectivity number have been closed**, each on the same
criterion. Two failure modes rule out whole classes rather than individual tools: anything
anchored to published affinities inherits a between-source disagreement larger than the
effect, and anything computing selectivity as a difference of two large absolutes
accumulates correlated bias, which is precisely how the free-energy calculation failed.

The modelling did its job. It specified a payload, verified the sequences, placed the tag so
no product is destroyed, chose the linker comparison, evaluated the carrier, screened the
silencer against its own cassette, and asked whether the payload can even be released. **It
also told us, repeatedly, what it could not establish.**

**The best estimate stands at +1.23 +/- 1.76 kcal/mol, interval including zero.** A cAMP
assay at both receptors with selective antagonists is the instrument that settles it, and
no amount of further computation substitutes for it.
