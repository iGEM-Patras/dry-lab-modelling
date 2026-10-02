# Methods that can address the δ/μ selectivity problem — a reference analysis

**1 October 2026.** Every method is scored against one criterion derived from the project's own
data, not from general merit.

---

## 0 · The acceptance criterion

The quantity to resolve is a **ΔΔG of about 1 kcal/mol**:

| reference | ΔΔG |
|---|---|
| native Met-enkephalin, published | +0.81 |
| our calibrated co-folding estimate for engPENK | +1.23 |
| our free-energy control, replicate 1 | +0.97 |

So **a method is only useful here if its error on a ΔΔG is ≤ 1.0 kcal/mol.**

Two consequences that eliminate most of the field before any benchmarking:

**(a) Methods that predict affinity pay a √2 penalty.** Selectivity is a difference of two
predictions, so a per-prediction RMSE of *e* becomes *e*·√2 on a ΔΔG. To clear 1.0 kcal/mol a
method needs per-prediction RMSE ≤ 0.71 kcal/mol = **0.52 log₁₀ units**. Almost nothing does.

**(b) The reference data has its own ceiling.** Our records hold two published values for
endomorphin-1 — −2.99 and −4.82 — differing by **1.83 kcal/mol**, which is larger than the
effect. Any method *calibrated against published affinities* inherits that noise, whatever its
internal accuracy. This is why five methods have already failed (see
`BINDPRED_REJECTED.md`), and it is a property of the data, not of the methods.

---

## 1 · THE QUESTION HAS CHANGED — read this before the method list

Both met-enkephalin legs and both engPENK legs now exist, so the control can be used as an
anchor rather than just a pass/fail:

```
ddG(engPENK)  - ddG(Met-enk)  =  -8.75 - (+0.97)  =  -9.72 +/- 3.34 kcal/mol
anchored to the measured Met-enk value (+0.81)    =  -8.91 +/- 3.34 kcal/mol
the protocol's raw answer for engPENK was            -8.75 +/- 3.19 kcal/mol
```

**Anchoring moves it by 0.16 kcal/mol.** The control detects **no systematic bias** for this
peptide class, so the control does *not* rescue the −8.75.

And yet the number is physically impossible. −8.91 kcal/mol implies **~3.4 million-fold**
μ-preference. The most μ-preferring ligand among 3,579 compounds with measured Kᵢ at both
receptors sits at −7.30, i.e. **~7,700-fold**. The protocol's answer is ~440× beyond anything
ever measured for any opioid ligand.

**Control passed. Answer impossible.** Those two facts together localise the fault: it is not
the protocol in general — it is **the engPENK legs specifically**. The three candidate causes,
in order of prior likelihood:

> **CORRECTION, 2026-10-02 — the first of those two facts is false.** The met-enkephalin
> control did **not** pass. The value it rested on (+0.97 ± 1.00) was computed while
> `c3b_menk_MOR_rep1` windows 21 and 23 were ~1 ns short each, despite the status query
> reporting the leg 27/27 complete. On verified-complete sampling the control is
> **−3.12 ± 2.29 kcal/mol — the wrong sign** against a published +0.81, and it fails the sign
> test. So the fault is **not** localised to the engPENK legs: the protocol gets the sign
> wrong on a peptide whose answer is known and whose pose Cycle 12 independently corroborated
> at 0.93–1.63 Å. The heading above is left in place because the reasoning that followed from
> it shaped this document, and the correction is more useful next to it than in place of it.
> Causes 1–3 below remain candidates for the engPENK legs, but a fourth now outranks them:
> the free-energy protocol itself. See `data/control_correction.json`.


1. **the starting pose is wrong** — a free-energy calculation converges to the free energy of
   the basin you put it in, and reports a tight error bar while doing so;
2. **those legs have not converged** — the earlier campaign showed 6.32 kcal/mol spread between
   replicates of the *same* system;
3. a setup error specific to those systems that the control systems do not share.

**This reframes what a new method is for.** We do not primarily need another selectivity
predictor — five have failed and the data has a resolution ceiling. We need an **independent
pose** for the engPENK–receptor complexes, to test cause (1).

**That is exactly where AutoDock earns a place, and it is why the suggestion was right.**

---

## 2 · TIER A — addresses the pose question (the live problem)

### A1 · AutoDock CrankPep (ADCP) — RECOMMENDED, start here

Zhang & Sanner, *Bioinformatics* 2019;35(24):5121-5127, **doi:10.1093/bioinformatics/btz459**
(160 citations). Open source, LGPL 2.0, `adcp.scripps.edu`, `github.com/ccsb-scripps/ADCP`.

This is the member of the AutoDock family built for our ligand class. From the paper:

- *"a novel approach to dock flexible peptides into rigid receptors. ADCP folds a peptide in the
  potential field created by the protein to predict the protein-peptide complex"*
- *"it outperforms leading peptide docking methods on two protein-peptide datasets commonly used
  for benchmarking docking methods: LEADS-PEP and peptiDB, comprised of peptides with up to 15
  amino acids in length"*
- *"ADCP reliably docked a set of protein-peptide complexes containing peptides ranging in
  lengths from 16 to 20 amino acids"*

**Why it fits.** `YGGFEVVG` is 8 residues — mid-range for ADCP, well inside validated territory.
It folds the peptide *in the receptor field*, so it does not need a template or a donor pose.
That matters because our pose-graft route was **closed by measurement** (`GRAFT_ROUTE_REJECTED.md`)
and co-folding is currently the only pose source we have — i.e. the pose entering the
free-energy calculation has never been independently corroborated.

**What it does NOT do.** ADCP predicts **structure, not affinity.** Its benchmarks are pose
RMSD and success rate; the paper reports no binding-affinity accuracy. So it cannot answer the
selectivity question by itself and must not be scored on ΔΔG.

**Its real limitation for us:** *"dock flexible peptides into **rigid** receptors"*. GPCR
orthosteric pockets are induced-fit. Mitigation: dock into several receptor conformers (the
equilibrated snapshots we already have from the TI setup), not one.

**The experiment it enables, and its cost.** Dock `YGGFEVVG` into DOR and MOR with ADCP. Then:
- if the ADCP pose **agrees** with the co-folded pose → cause (1) is excluded, and attention
  moves to convergence;
- if it **disagrees** → re-run one TI leg from the ADCP pose. A changed answer identifies the
  −8.75 as a pose artifact; an unchanged answer strengthens it considerably.

Docking is minutes-to-hours of CPU. One confirmatory TI leg is ~81 ns, around half a day on the
current pool. **Cheapest decisive experiment available.**

### A2 · Rosetta FlexPepDock — second opinion on the pose

Mature flexible peptide–protein docking, with active development
(`InterPepScore`, *Bioinformatics* 2022, a deep-learning refinement score for the FlexPepDock
protocol). Use only if ADCP and co-folding disagree and a third opinion is needed; it is
substantially more work to set up and answers the same question.

### A3 · HADDOCK + dMM-PBSA — pose plus an affinity attempt

*"Information-Driven, Ensemble Flexible Peptide Docking Using HADDOCK"*, Methods Mol Biol 2017.
Its affinity-scoring extension is **dMM-PBSA** (Spiliotopoulos et al., *Front Mol Biosci*
2016;3:46, doi:10.3389/fmolb.2016.00046, 60 citations), whose own framing is honest about the
difficulty: *"predicting binding affinity is one of the most critical and challenging components
of computer-aided structure-based drug design."* It is a Poisson-Boltzmann endpoint method — the
same family as the MM-GBSA we already ran, which **passed on direction and failed its own
magnitude gate**. Expect the same. Useful for ensemble docking with our existing restraint
knowledge; not an affinity answer.

---

## 3 · TIER B — could plausibly reach ≤ 1 kcal/mol on a ΔΔG

### B1 · Exact high-throughput ABFE (2025) — best new candidate

*"A formally exact method for high-throughput absolute binding-free-energy calculations"*,
*Nature Computational Science* 2025, **doi:10.1038/s43588-025-00821-w**. Reported:

- *"For 34 complexes with validated force-field accuracy, our method achieves an average
  unsigned error of less than 1 kcal mol⁻¹ and a hysteresis below 0.5 kcal mol⁻¹"*
- *"it efficiently manages flexible peptide ligands through a potential-of-mean-force
  calculation, adding less than 5% extra simulation time"*

**Two things make this directly relevant.** It explicitly handles **flexible peptide ligands**,
which is the hard part of our system. And **hysteresis below 0.5 kcal/mol** is a *convergence*
diagnostic — precisely the failure mode our 6.32 kcal/mol replicate spread represents.

Conservatively, AUE < 1 kcal/mol on an absolute ΔG gives ~1.41 kcal/mol on a ΔΔG, which is above
our requirement. **But that √2 is pessimistic here**, because the same ligand in two homologous
receptors shares its force-field and finite-size errors, which cancel in the difference. Our own
data supports that: replicate 1 agreed with experiment to **0.16 kcal/mol**, better than its own
±1.00 error bar — consistent with cancellation.

**Recommendation:** read the paper's SI for the peptide cases and its software availability
before committing. It is the only published method found today whose stated accuracy is in the
right range *and* which handles peptides.

### B2 · Relative FEP for selectivity between homologous receptors — precedent exists

*"Application of Free Energy Perturbation (FEP+) to Understanding Ligand Selectivity"*, *J Chem
Inf Model* 2019;59(6), **doi:10.1021/acs.jcim.9b00106**. The precedent is close to ours: the
targets *"share a highly conserved catalytic site (about 50%), thus making the design of
selective drug candidates very challenging with classical structure-based design approaches"*.
OPRD1/OPRM1 are ~60% identical — the same problem shape, one step harder.

Note FEP+ is commercial (Schrödinger). The transferable idea is free: **anchor on a reference
ligand instead of computing two absolute values.** We have now done the anchoring arithmetically
(§1); doing it *alchemically* — transforming `YGGFM` → `YGGFEVVG` at each receptor — would cancel
the ligand's self-energy terms exactly rather than approximately, and never fully decouples
anything. Worth costing against B1.

### B3 · More replicates of the current protocol — computed, and it does not work

Already quantified: with an observed replicate spread of 6.32 kcal/mol, even **six** replicates
per receptor leave the standard error at ~2.6 kcal/mol, still ~3× the effect, for ~11 extra
days. **Replicates buy confidence in a number we cannot resolve; they do not resolve it.**
Longer windows or a better estimator are the levers, and both break protocol-matching with the
existing controls.

---

## 4 · TIER C — ruled out, with the number that rules them out

| method | ΔΔG error | why |
|---|---|---|
| **AutoDock Vina / AD4 scoring, for affinity** | ≳ 2.4 kcal/mol | see below |
| best modern ML scoring functions | **2.37** | best verified RMSE 1.23 pKd units (iScore, 2025) × 1.364 × √2 |
| TrGPCR | **3.48** | RMSE 1.804 pKd, its own best figure |
| Cycle 11 fingerprint QSAR (ours) | **1.06** | and the payload prediction is a nearest-neighbour lookup |
| Cycle 7 co-folding, calibrated | **1.76** | our own measured uncertainty |
| BindPred | not computable | ESM2 cannot represent D-residues; 5 encodable references |
| GPCRVS | n/a | opioid receptors absent |

**On AutoDock Vina specifically, since it was raised.** Vina's *scoring* function must not be
used for this question. The best **modern ML** scoring functions reach RMSE ≈ 1.23 pKd units
(iScore 2025, R = 0.78–0.81), which is already 2.37 kcal/mol on a ΔΔG — 2.4× our requirement.
Vina's classical empirical function is less accurate than these, and we have **already run
MM-GBSA**, a more rigorous endpoint method, which failed its own magnitude gate while getting
direction right. A Vina score cannot beat MM-GBSA on magnitude.

**The customisations are real but address throughput and pose, not accuracy.** Vina-GPU 2.1
(*IEEE/ACM TCBB* 2024) and AutoDock-GPU accelerate docking; flexible side chains, hydrated
docking and custom scoring change pose quality and search. None of them moves a ~2.4 kcal/mol
ΔΔG error below 1.0. **So use the AutoDock family for what it is excellent at — peptide pose
prediction via ADCP (§A1) — and not as a selectivity predictor.**

---

## 5 · TIER D — the experimental arbiter

No computational method found today resolves the effect with confidence. The fifth paper
assessed (*npj Drug Discovery* 2026;3:13, doi:10.1038/s44386-026-00046-5) reaches the same
conclusion from the opposite direction and recommends direct binding measurement, enabling
*"computational predictions of binding strength and selectivity to be tested against
experimentally determined equilibrium constants (Kd) without the use of tags."*

| route | gives | accessible to us |
|---|---|---|
| **cAMP** (planned) | functional **potency** (EC₅₀) | yes — in the wet-lab plan |
| radioligand displacement | **binding** Kᵢ at each receptor → experimental ΔΔG | plausible; previously set aside |
| SPR / BLI | label-free Kd | needs receptor in nanodiscs or VLPs; likely out of scope |
| FLOWER | label-free Kd, near-physiological | no — specialised instrument |

**Standing note:** every dry-lab number in this project is a ΔΔG of **binding**; cAMP measures
**potency**. If they disagree it may be ligand bias rather than a wrong prediction, and without
a binding measurement there is no way to tell which. The assay choice is the wet lab's; this is
recorded so the limitation is known rather than discovered.

---

## 6 · Recommended sequence

1. **ADCP dock** `YGGFEVVG` into DOR and MOR, using several equilibrated receptor conformers.
   *Cost: hours of CPU. Decides whether the −8.75 could be a pose artifact.*
2. **If the pose disagrees with co-folding**, re-run one engPENK TI leg from the ADCP pose.
   *Cost: ~81 ns, about half a day on the current pool. Decisive either way.*
3. **Finish replicate 2** of the met-enkephalin control (in progress). Confirms or undermines
   the +0.97 that the whole anchoring argument in §1 rests on.
4. **Read the Nature Comput Sci 2025 SI** (B1) for peptide performance and software
   availability before committing to any new free-energy framework.
5. **Do not** run Vina scoring, another fingerprint QSAR, or another published affinity
   predictor for this question. Four of five have been excluded with numbers, and the fifth
   recommends measuring instead.

## 7 · What we would say if asked why we have no selectivity number

We have assessed **eight** distinct computational routes — five published methods, our own
fingerprint QSAR, endpoint rescoring, and alchemical free energy — and documented with numbers
why each cannot resolve a ~1 kcal/mol selectivity difference for this peptide. The binding
constant is the limiting factor: the published reference data disagrees with itself by
1.83 kcal/mol on a single compound. Our best route passed its literature control this morning
and returns a value for our peptide that is physically impossible, which localises the problem
to that specific calculation rather than to the method. The next step is an independent pose,
and the arbiter is the wet-lab assay.
