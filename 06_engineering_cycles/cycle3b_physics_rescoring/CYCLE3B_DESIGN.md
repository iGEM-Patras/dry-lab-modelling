# Cycle 3b — Can a physics-based observable resolve δ/μ selectivity where ipTM could not?

**Status:** pre-registered · written **before** any Cycle 3b simulation was run
**Type:** method-change cycle — new observable, same design space
**Supersedes:** the original Cycle 3b premise (combine V4+V5 "wins"), **withdrawn** —
V5's win was +0.0032 ± 0.004 at n=20, and combining two within-noise effects is not a
design rationale.

---

## Learn → Design edge

Cycle 3a established that **Boltz-2 ipTM cannot resolve δ/μ preference at the effect sizes
DNA-encodable designs produce**: all Δ_sel ≤ 0.007 with SEM ≈ 0.004 at n=20, effect sizes
shrinking as n grows, and the pose-convergence alternative failing replication. The
diagnosis was not "we need more samples" but **"the observable has no dynamic range."**

So Cycle 3b changes the observable rather than the sequences. Two things make this a real
methodological step and not a rescoring exercise:

**1. ipTM has no physical units; ΔΔG does.** ipTM is a confidence score — there is no
conversion from "Δ_sel = 0.007" to a selectivity ratio. A binding free energy in kcal/mol
maps directly onto measurable selectivity via ΔΔG = RT·ln(ratio), which means every
prediction this cycle makes is falsifiable against a radioligand number.

**2. MD removes the approximation that limited every previous cycle.** Boltz-2 cannot
represent D-amino acids or C-terminal amidation. Classical force fields represent both
routinely (D-residues are the same parameters at inverted chirality; C-terminal `-NH₂` is a
standard capping group). Two consequences:

- **The real δ-selective controls become available.** Deltorphin I/II carry D-Ala² and a
  C-terminal amide. We could never model them before, so we had no positive control — every
  previous cycle was uncalibrated.
- **We can finally model the actual therapeutic species.** Our payload ends in Gly, the
  recognition motif for **PAM** (peptidylglycine α-amidating monooxygenase), so the peptide
  released *in vivo* is `...VV-NH₂`, not the free acid. **Every Boltz-2 number in Cycles 1–3a
  was computed on the wrong chemical species.** This cycle models both forms.

---

## The honest arithmetic that shapes this design

At 300 K, RT = 0.596 kcal/mol, so selectivity maps to free energy as:

| selectivity | ΔΔG needed |
|---|---|
| 2-fold | 0.41 kcal/mol |
| 10-fold | **1.37 kcal/mol** |
| 100-fold | 2.75 kcal/mol |
| 8448-fold (deltorphin II) | 5.39 kcal/mol |

**MM-GBSA ΔΔG uncertainty is typically 1–2 kcal/mol.** A 10-fold selectivity improvement —
already an ambitious target for a single-residue change — sits *at or below* that noise
floor. Stated plainly:

> **MM-GBSA is very likely also unable to resolve our designs.** The honest detection floor
> at 2× noise is ≈ 100-fold selectivity; nothing in our panel is expected to reach it.

This is pre-registered as an expected outcome, not discovered afterwards. It is also why
the cycle is **gated**: a method that cannot separate deltorphin II from endomorphin-1 —
8.4 kcal/mol apart — has no business being applied to a panel separated by ≤ 1 kcal/mol.

---

## Design: a two-stage gate

### Stage 1 — method validation on experimental controls (**runs first, decides Stage 2**)

Four peptides with published binding data spanning ≈ 8.4 kcal/mol, each against OPRD1 and
OPRM1 (8 systems × 3 replicates = 24 runs).

| control | sequence | selectivity (lit.) | expected ΔΔG_sel | role |
|---|---|---|---|---|
| Deltorphin II | Tyr-**D-Ala**-Phe-Glu-Val-Val-Gly-**NH₂** | δ, 8448× | **+5.39** | δ anchor |
| Deltorphin I | Tyr-**D-Ala**-Phe-Asp-Val-Val-Gly-**NH₂** | δ, 14318× | **+5.70** | fine-discrimination test |
| Endomorphin-1 | Tyr-Pro-Trp-Phe-**NH₂** | μ, 150× (conservative) | **−2.99** | μ anchor |
| Met-enkephalin | Tyr-Gly-Gly-Phe-Met (free acid) | weakly δ | ≈ 0 | neutral reference |

Sign convention: ΔΔG_sel = ΔG_bind(μ) − ΔG_bind(δ), positive = δ-preferring.

**Gate criteria — all three must hold to run Stage 2:**

- **G1 (sign + rank):** Deltorphin II and Deltorphin I both positive, Endomorphin-1
  negative, with deltorphins ranked above endomorphin-1.
- **G2 (noise floor):** replicate SD of ΔΔG_sel ≤ 1.5 kcal/mol on every control.
- **G3 (calibration slope):** regression of computed vs experimental ΔΔG_sel has positive
  slope with 95 % CI excluding zero (n = 4).

**If the gate fails, Cycle 3b terminates and reports a negative methodological result.**
The modelling line then closes and the project's recommendation stands unchanged: radioligand
competition binding on `YGGFEVVG` and `YGGFDIIG`. No Stage 2 systems will be run in that
case — this is committed in advance precisely so a failed gate cannot be quietly reframed.

### Stage 2 — design panel (**conditional on the gate**)

Only the two survivors of the Cycle 3a screen, each in **both** chemical forms, plus native:

| id | sequence | form | rationale |
|---|---|---|---|
| C1-acid | `YGGFEVVG` | free acid | as modelled in Cycles 1–3a |
| C1-amide | `YGGFEVV-NH₂` | amidated | **the actual in-vivo species after PAM** |
| V4-acid | `YGGFDIIG` | free acid | co-leading candidate |
| V4-amide | `YGGFDII-NH₂` | amidated | its in-vivo species |
| native | `YGGFM` | free acid | baseline |

5 peptides × 2 receptors × 3 replicates = 30 runs.

---

## Method (fixed in advance)

- **Starting poses:** Boltz-2 model_0 complexes from Cycles 1–3a, so this is a rescoring of
  *the same* binding modes rather than a fresh docking exercise. Control peptides are built
  onto the corresponding receptor by superposing the shared Tyr¹ message anchor.
- **System:** receptor embedded in a POPC bilayer, TIP3P water, 0.15 M NaCl, neutralised.
  Amber ff14SB / Lipid21 or CHARMM36m (whichever the cluster provides; recorded before use).
- **Protocol:** minimisation → NVT 100 ps → NPT restrained 1 ns → **5 ns free equilibration
  → 15 ns production**, 2 fs step, h-bond constraints, PME, 300 K, 1 bar.
- **Replicates:** 3 per system, differing only in initial velocity seed.
- **MM-GBSA:** 100 snapshots from the **last 10 ns only** (equilibration discarded),
  igb = 8 with mbondi3 radii, salt 0.15 M. Entropy **not** estimated — quasi-harmonic and
  normal-mode entropies are unreliable for flexible peptides and would add noise, not
  accuracy. This means we report an **enthalpy-dominated binding effective energy, not a
  true free energy**, and any comparison to experimental ΔΔG inherits that bias.
- **Reported statistic:** mean ± SD across the 3 replicates (replicate-level, not
  snapshot-level, error — snapshot SEM understates uncertainty by ignoring the dominant
  source of variance). Per the Cycle 1 correction, no single-run numbers are reported.

---

## Predictions (committed before any run)

| # | Prediction | Falsified if |
|---|---|---|
| **P1** | Gate criterion G1 passes — deltorphins positive, endomorphin-1 negative | any control has the wrong sign |
| **P2** | Gate criterion G2 passes — replicate SD ≤ 1.5 kcal/mol | any control's SD exceeds 1.5 |
| **P3** | The method **cannot** separate Deltorphin I from II (Δ_exp = 0.31 kcal/mol, far below noise) | they separate with non-overlapping error bars |
| **P4** | **No Stage 2 design reaches ΔΔG_sel ≥ 1.37 kcal/mol** (10-fold) with error bars excluding zero | any design does |
| **P5** | Amidation changes ΔΔG_sel by ≥ 0.5 kcal/mol for at least one design — i.e. the free-acid modelling in Cycles 1–3a was on the wrong species in a way that *mattered* | all acid/amide pairs agree within 0.5 |
| **P6** | Computed ΔΔG_sel magnitudes are **systematically too large** vs experiment (a known MM-GBSA pathology from the missing entropy term and implicit solvent) | slope of computed vs experimental ≤ 1 |

P3, P4 and P6 predict **limitations of our own method**. P4 in particular predicts this
cycle will not find a winner. If P4 is falsified, that is a genuine positive result; if it
holds, the cycle's contribution is a quantitative bound on what the computational screen
could ever have detected — which is the thing Cycles 1–3a lacked.

---

## Compute budget (stated in advance)

Stage 1 is 24 runs × ~20 ns. On one RTX 2080 Ti at ~40–50 ns/day for a ~100 k-atom membrane
system, that is ≈ 11 GPU-days sequentially, less if several GPUs are free. **Stage 1 is the
only committed spend.** Stage 2 (30 runs, ≈ 14 GPU-days) is not authorised unless the gate
passes.

Software availability has **not** yet been verified — the cluster login node became
unresponsive during the probe for this cycle. The MD engine, force field, and MM-GBSA
implementation will be recorded here before the first production run.

---

## Interpretation limits (carried forward, unchanged)

- MM-GBSA effective energies are **not** binding free energies; no entropy term is computed.
  Radioligand competition binding at OPRD1/OPRM1 remains the only real test.
- Starting poses are Boltz-2 predictions. If a pose is wrong, its rescoring is wrong with
  higher precision and no more accuracy. 20 ns cannot repair a misdocked peptide.
- Every metric is a mean ± SD over replicates; single-run numbers are not reported.
- A membrane-embedded 20 ns simulation is short. Convergence of the interaction energy will
  be shown as a cumulative-mean trace, as in the lipoplex workstream, and non-convergence
  will be reported rather than averaged over.
