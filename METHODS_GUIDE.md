# Methods guide

**For a team member who knows the project but not the computational methods.** You know what
Epione is and why δ-selectivity matters. This explains *how* the dry lab answers its questions:
what each technique actually computes, why we picked it, what its numbers mean, and where it
breaks. Written assuming programming literacy and no chemistry background.

Companion: [`GLOSSARY.md`](GLOSSARY.md) for term lookup. Tool versions and citations:
[`methods_references.md`](methods_references.md).

---

## 0. The one convention that shapes everything

Every cycle has a `*_DESIGN.md` written and **pushed to git before the test runs**, containing
the hypothesis, the predictions, and a **gate** — a numeric pass/fail threshold fixed in
advance. The matching `*_RESULTS.md` scores every prediction as confirmed, falsified, or
unresolved.

This is not bureaucracy. Computational methods are unusually easy to fool yourself with,
because you can re-run an analysis fifty times and report the run that looked best. A gate
committed beforehand makes that impossible to do silently — the commit order is checkable.

Two derived rules you will see enforced in code:

- **A method must be calibrated against known answers before its output is quoted.** If the
  calibration fails, the target number is withheld — not reported with a caveat. See §5.
- **Compute the threshold, don't pick it.** Our correlation gates come from the sample size
  (`critical_r(n)`), not from judgement.

---

## 1. Sequence work — the foundation

**What it is:** proteins and DNA as strings, with domain rules. Library: **Biopython**.

The operations that recur:

| Operation | What it does |
|---|---|
| Translation | DNA → protein, 3 letters per amino acid |
| ORF finding | Locate where a coding sequence starts (after a Kozak motif) and ends (stop codon) |
| Motif search | Find cleavage sites (`KR`, `KK`, `RR`), restriction sites, repeats |
| Molecular weight | Exact mass of a peptide — needed to tell mass spec what to look for |
| Isoelectric point (pI) | The pH at which a protein has zero net charge |

**Why pI matters and where it bit us:** a protein is least soluble near its pI. Our mature
chain has pI ≈ 5.19 and the processing enzymes need pH 5.5 — so the digest runs exactly where
the protein is most likely to fall out of solution. We could not raise the pH because the whole
enzyme panel has acidic optima, so it is documented as a risk in
[`07_invitro_penk/`](07_invitro_penk/) rather than solved.

**Failure mode we hit:** a parser that returned the uncleaved read-through instead of the
cleaved product, because it searched for the payload's start motif without bounding the end.
Lesson: when you slice a sequence, assert the length you expect.

---

## 2. Signal peptide prediction — DeepSig

**Question:** will the cell actually secrete this protein?

A **signal peptide** is a ~20-residue tag at the protein's N-terminus meaning "export me". It
is cut off during secretion. If our engineering accidentally breaks it, the protein stays
inside the cell and the whole scheme fails.

**DeepSig** is a neural network that takes a protein sequence and returns whether a signal
peptide is present, its cleavage position, and a confidence score. We ran it on every
engineered N-terminus — including the unusual case where a construct's protein begins with a
self-cleaving-peptide remnant rather than a normal start.

**How to read the output:** a probability plus a predicted cleavage site. What you care about
is that the cleavage site is where you designed it. A high probability with the cut in the
wrong place is a failure, not a pass.

---

## 3. Codon and GC design, and synthesis complexity

**Question:** will the DNA synthesis company physically make this?

Several DNA codons encode the same amino acid, so you can rewrite DNA without touching the
protein — **synonymous recoding**. We use this to hit a target **GC content** (40–45 %) because
synthesis fails outside a workable range.

The cost is **CAI** (codon adaptation index, 0–1): how well codon choice matches what human
cells prefer. Optimising GC pushes CAI down. Ours land at 0.65–0.74. That is a real trade, and
[`09_codon_gc_design/`](09_codon_gc_design/) states it rather than hiding it.

**Cycle 4 is the interesting part, methodologically.** The vendor rejects a sequence with a
"complexity score" but does not publish the rules. So we treated it as a black-box
reverse-engineering problem: take the rejection reports, infer scoring rules, predict the next
submission's score, submit, compare. Two rules were recovered:

1. **Repeats** — including a *terminal inverted repeat*, where the sequence's two ends are
   reverse complements of each other. The checker finds it twice, once from each end.
2. **Local composition** — a window dominated by one base.

The v4 failure was in flanking sequence **inherited from existing lab files** that nobody had
tested as a pair. Standing rule adopted: *inherited sequence is still untested sequence.*

---

## 4. Structure prediction and co-folding — Boltz-2

**Question:** what does the peptide–receptor complex look like, and how tightly does it bind?

**Boltz-2** is a neural network in the AlphaFold family. Give it sequences; it predicts the 3D
structure. Give it *two* molecules and it predicts them **together** — a **co-fold** — which is
how we model a peptide sitting in a receptor.

Input is a YAML declaring each chain. A peptide can be declared two ways, and **the choice has
consequences**:

- as a **protein chain** → you get a proper backbone with residues and atom names;
- as a **ligand** (SMILES string) → you get correct chemistry but the model writes it as one
  undifferentiated residue with no backbone topology.

Cycle 7 declared our peptide as a ligand. The atoms were all correct — element counts matched
the free-acid formula exactly — but force-field tools could not parametrise it, which is why
Cycle 8 needed a re-run. Worth knowing before you write a YAML.

### Reading the confidence scores

| Score | Range | Means |
|---|---|---|
| **ipTM** | 0–1 | Confidence in how the two chains sit *relative to each other* |
| **pLDDT** | 0–100 | Per-residue confidence in local structure |
| **affinity_pred_value** | — | The affinity head's binding prediction |

**These are confidence, not correctness, and ipTM is not binding strength.** Our co-folds score
ipTM 0.958 at δ and 0.957 at μ — nearly identical, which is *why* ipTM cannot serve as a
selectivity metric. That was Cycle 7's B2 gate failing, and it is a genuinely useful negative.

**Low pLDDT is not always bad.** Our payload is disordered by design; its low pLDDT reflects
real floppiness, not model failure. Interpreting the score requires knowing what the molecule
is supposed to be.

---

## 5. Calibration — the method that made Cycle 7 work

This is the most transferable idea in the repo.

A predictor gives you a number for your molecule. How do you know it means anything? You run
the *same predictor* on molecules whose answer is already published, and check.

The procedure:

1. **Build a reference panel** — compounds with published δ and μ binding values, all from a
   *single source* so the axis is internally consistent. We use ChEMBL. Mixing our own stored
   literature values with database medians produced disagreements for the same molecule, so the
   single-source rule is now standing.
2. **Set the gate before looking.** Required correlation is computed from sample size:
   `critical_r(13) = 0.553`. Not chosen — derived.
3. **Score.** Cycle 7: r = 0.805, p = 0.0009, signs correct on 12 of 13. Gate passed.
4. **Back-project the target through the fitted line** to get a corrected estimate with an
   uncertainty from the residual spread.

**Why a regression slope matters:** ours is 0.309, meaning predictions are compressed ~3.2×
versus reality. Direction and ranking are calibrated; absolute magnitudes are not. So we report
`YGGFEVVG` at **+1.23 ± 1.76 kcal/mol** and explicitly decline to treat the magnitude as
established.

**What calibration cost us, honestly:** the same method failed every gate at n = 4, getting the
sign wrong on the most strongly selective reference. Had we skipped the controls, the withheld
number would have agreed with our earlier null and been mistaken for confirmation. The controls
are the reason the n=13 result means something.

This procedure is packaged as a reusable skill, `calibrated-prediction-gate`, with helpers
`critical_r`, `min_n_for_r`, `calibration_fit`, `back_project`, `score_calibration`.

---

## 6. Molecular dynamics — GROMACS

**Question:** what does the complex do over time, rather than in one static snapshot?

MD integrates Newton's equations for every atom in femtosecond steps. Structure prediction
gives you one pose; MD tells you whether that pose is stable, how it moves, and — with the
right protocol — how strongly it binds.

**The pipeline**, and what each stage is for:

| Stage | Purpose |
|---|---|
| Build | Place the complex in a membrane, add water and ions |
| Minimise | Relieve atomic overlaps from the model-building step |
| Equilibrate (NVT → NPT) | Bring to target temperature, then pressure |
| Production | The run you actually analyse |

**Force field** = the parameter set defining how atoms interact. `ff14SB` for protein,
**MARTINI 2** for the coarse-grained lipoplex work in [`04_lipoplex_md/`](04_lipoplex_md/).

**File types you will meet:**

| Extension | Contents |
|---|---|
| `.mdp` | Run configuration — the input file you edit |
| `.gro` / `.pdb` | Coordinates. `npt.gro` = the equilibrated structure |
| `.top` / `.itp` | Topology — which atoms are bonded to which |
| `.ndx` | Index groups — named atom selections |
| `.tpr` | Compiled run input (config + topology + coordinates) |
| `.xtc` / `.trr` | Trajectory — coordinates over time. Large |
| `.edr` | Energies over time |
| `.xvg` | Plain-text numeric output. This is what analysis reads |
| `.cpt` | Checkpoint — lets an interrupted run resume |

**Two rules that exist because we violated them:**

- **Never quote a bound-state ΔG without its residency fraction.** Some runs have the peptide
  leaving the pocket most of the time; an energy conditional on "while bound" is meaningless
  without saying how often that was. The merge tooling refuses to emit one without the other.
- **Verify the molecule before you compute on it.** A chirality bug once let a wrong-handedness
  analogue pass every downstream check. `scripts/chirality.py` is an independent geometric
  check that exists specifically for that.

---

## 7. MM-GBSA — the fast approximation, and why it failed

**MM-GBSA** estimates binding energy from an MD trajectory by computing the energy of the
complex minus the free partners, with solvent treated by an implicit model rather than explicit
water molecules. Much faster than the rigorous route.

Cycle 3b tried it and **failed its own pre-registered gate**. The diagnostic was that the
control with the *tightest replicate agreement* also had the *largest error* against its known
value — agreement without accuracy, which points to systematic bias rather than insufficient
sampling. The cycle was terminated per its pre-registration rather than rescued.

Worth reading [`cycle3b_physics_rescoring/docs/GATE_VERDICT_BOUND.md`](06_engineering_cycles/cycle3b_physics_rescoring/docs/GATE_VERDICT_BOUND.md)
as an example of a gate doing its job.

---

## 8. Free-energy perturbation / thermodynamic integration — Cycle 8

**The rigorous method.** No empirical slope to correct, no dependence on having published
controls in the right range.

**How it works.** You cannot simulate a peptide "unbinding" directly — it takes far too long.
Instead you compute the free energy of an *alchemical* path: gradually switch off the peptide's
interactions with its surroundings, from fully coupled to fully decoupled, through a series of
intermediate states indexed by **λ** (we use **27 windows**). At each window you record
**dH/dλ** — how the energy changes with the coupling parameter. Integrating dH/dλ over λ gives
the free energy of removing the peptide.

Do that in the receptor and in water; the difference is binding free energy. Do that at δ and
at μ; the difference of differences is **ΔΔG** — the selectivity number.

**Key `.mdp` settings** (in `cycle8_fep/mdp/`):

| Setting | Role |
|---|---|
| `couple-moltype` | **Which molecule gets decoupled.** Naming the wrong one runs for weeks and returns a plausible, wrong number |
| `init-lambda-state` | Which window this run is |
| `coul-lambdas` / `vdw-lambdas` | The λ schedule — electrostatics switched off before van der Waals |
| `sc-alpha`, `sc-power`, `sc-sigma` | **Soft-core** parameters: prevent a singularity as atoms vanish |
| `nstdhdl` | How often dH/dλ is written |

**Scale:** 27 windows × 2 replicates × 2 receptors × 2 legs, 3 ns each ≈ 648 ns for the control
arm alone, days of wall time across 13 machines. This is why the cheap methods were tried first.

**How the windows are managed:** a shared work queue. Each worker scans window indices, claims
one with an atomic `mkdir` lock, runs it, and releases the lock if incomplete so another worker
can resume from checkpoint. Workers are independent and restart-safe.

**Progress is measured in nanoseconds banked, not windows finished.** A window at 1177 of
3000 ps is real accumulated sampling; a binary complete/incomplete count throws that away and
reads zero for hours while work is happening.

---

## 9. Cheminformatics and machine learning — Cycle 7's screen

**RDKit** handles small molecules. A molecule is a **SMILES** string (`CC(=O)O` is acetic
acid); RDKit parses it into a graph and computes descriptors.

**Morgan fingerprints** encode a molecule as a bit vector: for each atom, hash its
neighbourhood out to a radius, set those bits. Similar molecules share bits. **Tanimoto
similarity** is the overlap between two fingerprints.

The screen: train a random forest on fingerprints of compounds with measured δ and μ values,
predict ΔΔG for candidate variants.

**Two validation points that matter more than the accuracy number:**

- **Scaffold-grouped cross-validation, not random.** Random splits put near-identical molecules
  in train and test, inflating performance. Grouping by chemical scaffold forces the model to
  generalise. We report the scaffold-split number as the honest one.
- **Applicability domain.** A model only speaks to chemistry it has seen. Our peptide's maximum
  Tanimoto similarity to the training set is low — it sits *outside* the domain of a
  small-molecule model. Stated explicitly rather than quietly ignored.

---

## 10. Sequence database methods

**BLAST** ([`03_sirna_design/`](03_sirna_design/)) finds sequences similar to a query. Used for
siRNA off-target screening: a candidate that matches something other than its intended target
will silence the wrong gene. `blastn-short` is the variant tuned for short queries.

A result worth knowing: the original four-duplex panel was **withdrawn** because it
cross-reacted with mouse *Mme* — one guide a perfect 19/19 match. The corollary is that the
human-exclusive replacements cannot be validated in a mouse model.

**MHC-I binding prediction** ([`10_immunogenicity_antibody/`](10_immunogenicity_antibody/))
asks whether our engineered sequence produces fragments the immune system will flag. Scanning
6,120 allele–peptide pairs showed the engineered epitope is no more immunogenic than the native
one (1.86 % vs 1.77 % strong binders), but the **P2A junction is the worst of the three**
(2.07 %) — an argument for the IRES constructs.

---

## 11. Statistics as we use them

| Concept | How we use it |
|---|---|
| **Pearson r** | Linear correlation — does predicted track measured? |
| **Spearman ρ** | Rank correlation — does the *ordering* match? Used when a method ranks reliably but is miscalibrated in magnitude. Cycle 9: ρ = 1.000 |
| **critical r** | The correlation needed for significance at a given n. **Computed, not chosen** |
| **Power analysis** | Before expanding a failed test, we compute whether the larger n could actually detect the effect |
| **SEM vs spread** | A metric is only useful if panel spread exceeds measurement noise. Cycle 2's ipTM had spread ≈ 4× its SEM; convergence ratio ≈ 45× — which is why one worked |
| **Signs correct** | Simple, robust: did we get the direction right? 12/13 in Cycle 7 |
| **Residency fraction** | Proportion of simulation with the peptide actually bound. Gates every ΔG |

---

## 12. What runs where

**On a laptop:** all sequence work, cheminformatics, ML, plotting, and any analysis of
committed `.csv`/`.xvg` outputs. Python with Biopython, pandas, numpy, matplotlib, RDKit,
scikit-learn.

**On the cluster only:** MD, FEP, and Boltz-2 co-folds. Scheduler is **SLURM** (`sbatch` to
submit, `squeue -u $USER` to check). Partitions differ in wall-time limits — a 2-hour cap
killed two co-folds mid-inference before we moved to a longer-limit partition.

**You do not need to re-run simulations to work with results.** Every `.csv` and `.xvg` output
is committed.

**Small scripts worth reading**, because they show the house style:

| Script | Why |
|---|---|
| `cycle3b_physics_rescoring/scripts/gate.py` | Evaluates a pre-registered gate. The pattern the whole repo rests on |
| `.../scripts/chirality.py` | Independent geometric check; exists because a wrong molecule once passed everything else |
| `.../scripts/test_tilt.py` | An actual unit test of analysis code |
| `cycle8_fep/scripts/gate_ti.py` | Current campaign's gate |

---

## 13. Failure modes we actually hit

The most educational section. Each of these is documented in the repo.

**Confidence is not correctness.** ipTM 0.958 at δ and 0.957 at μ — high confidence, zero
discriminating power. A confident model can be confidently uninformative.

**Two checks sharing a bug look like corroboration.** A scan reported the peptide absent from a
structure file. It had used the same record-type filter that caused the original problem, so
it "confirmed" the earlier wrong conclusion. Independent checks must be *independent*.

**A gate can pass for the wrong reason.** A completion check once verified that a step *ran*
rather than that it *produced anything* — reporting success on a system containing zero peptide
atoms. Assert the property you care about, not that the code executed.

**A gate can also fail for the wrong reason.** A later pre-flight asserted snapshot values of
two windows that were actively being sampled. The values legitimately grew, so the gate rejected
healthy data. Never validate a moving quantity against a frozen snapshot — validate against a
synthetic fixture whose content you control.

**Testing the wrong input invalidates the answer.** A geometric test of whether a peptide could
extend to solvent returned "impossible" — measured on a raw predicted structure with 1.2–1.7 Å
pre-existing atomic overlaps, which guaranteed that answer regardless of the real geometry. The
corrected measurement on the equilibrated structure reached the same conclusion, but the first
result was not evidence. See [`cycle8_fep/GRAFT_ROUTE_REJECTED.md`](06_engineering_cycles/cycle8_fep/GRAFT_ROUTE_REJECTED.md).

**Agreeing with your expectation is not verification.** The pattern behind several of the above:
when a result matched what was expected, it got checked less carefully. What broke the loop each
time was printing a number that was not needed for the desired conclusion.

**Inherited sequence is untested sequence.** Cycle 4's rejection came from flanking DNA carried
forward from existing lab files, never checked as a pair.
