# Model

Our dry lab did not describe the system. It decided it, and, more often than we expected,
it told us we were wrong.

Four workstreams made concrete decisions the wet lab acted on. A fifth tried to answer the
project's central pharmacological question and could not. Both are reported here, because a
model that cannot fail cannot inform.

## 1 · A calibrated selectivity model

The payload is engineered for δ-opioid receptor preference. The obvious question, *by how
much?* needs a model whose error is smaller than the effect, so we measured that first.

We assembled **13 published reference opioids** spanning four orders of magnitude of δ/μ
selectivity and asked our structural pipeline to reproduce their known values.

| | |
|---|---|
| correlation with published selectivity | **r = 0.805**, p = 0.0009 |
| critical r for n = 13 | 0.553 |
| sign predicted correctly | **12 of 13** |
| slope | 0.309: the model **compresses** the real range 3.2-fold |

The compression matters more than the correlation. A model that ranks correctly but
compresses must have its predictions expanded before they are quoted, and the expansion
inflates the uncertainty. Applying that correction to our engineered payload:

> **+1.23 ± 1.76 kcal/mol** δ-over-μ (≈ 7-fold)

Nominally δ-preferring. **The interval includes zero.** That is the honest state of the
prediction, and it is what our poster and abstract say.

## 2 · Free energy, and why we stopped quoting it

A calibrated structural score is an interpolation. To compute selectivity from physics
instead, we ran alchemical free-energy calculations, and pre-registered the gates that
would decide whether the answer could be quoted, before any window was run.

The first attempt failed its own control: replicates differing only by thermostat seed gave
opposite signs. Rather than call the method noisy we diagnosed it. Per-interval overlap
diagnostics showed poorly overlapping work distributions, concentrated in the legs with the
larger peptide: a **spacing** problem, not a sampling one, because at fixed spacing the
perturbation per window grows with the size of the solute being decoupled.

So we rebuilt the ladder, re-spacing it by equalising thermodynamic length rather than
subdividing interval by interval. The diagnosis was right:

| gate | result |
|---|---|
| overlap | **pass**: 0 of 56 intervals above threshold, against 20–21 of 25 on the old ladder |
| sign | pass: both replicates positive |
| accuracy | **fail** |
| reproducibility | **fail**: replicates differed by 13.75 kcal/mol against a combined error of 4.53 |

The fix worked and the calculation still failed. Doubling the windows to repair overlap also
doubled the number of terms whose small biases accumulate, and in the two legs those biases
ran in opposite directions, so they added instead of cancelling. **No free-energy value for
our peptide is quoted anywhere in this project.** The decision rule said so before we knew
the answer.

## 3 · The models that chose reagents

**Construct design.** Four bicistronic constructs as a two-by-two of linker strategy (IRES
vs P2A) and reporter orientation, sequence-verified by alignment before synthesis. A
sequence-level audit found a **real defect in one candidate**: a truncated enkephalin core,
and removed it from the build before money was spent. Tag placement was chosen so the
carboxy-terminal decapeptide survives processing.

**Silencing arm.** From an initial library of **206 duplex candidates** against the
neprilysin transcript, two were selected on predicted potency, seed-region binding energy,
transcriptome-wide off-target profile, local structural accessibility, and coverage of all
four transcript isoforms. A top-ranked candidate was **discarded** for a high-frequency SNP
in its target site. We then ran a screen absent from standard pipelines: because the vehicle
co-packages plasmid and siRNA in one lipoplex, every candidate was checked against our own
expression cassette to ensure it would not silence the transcript it exists to protect.

**Vehicle.** Coarse-grained MD across lipid formulations resolved the pH-dependent
DNA-binding switch that motivates an ionizable lipid over a permanent cation: a formulation
decision made by the model.

## 4 · Limitations, stated beside the results

- The selectivity model **compresses** the true range 3.2-fold; predictions are
  expansion-corrected and the correction dominates the error bar.
- Coarse-grained lipid topologies are **analogy models**; conclusions are comparative, not
  affinities.
- Accessibility folding ignores RNA-binding proteins in the cell.
- Peptide-backbone conformation is **not converged** in our 20 ns trajectories: replicates of
  the same system span the full range of the metric. We tested this explicitly and report it
  rather than building on it.

## 5 · What the model asks the bench to decide

Every output is written as a prediction with a named assay:

| model output | the experiment that would refute it |
|---|---|
| construct identity | two-enzyme restriction digest: we predict the exact gel |
| peptide is produced and secreted | LC-MS/MS on b5/b6/b7 transitions vs untransfected control |
| ≥70% neprilysin knockdown at 48 h | qPCR against scrambled control |
| δ-preference | cAMP at both receptors, engineered vs native, same cells, same day |

The last row is the one our own methods could not settle. We say so.
