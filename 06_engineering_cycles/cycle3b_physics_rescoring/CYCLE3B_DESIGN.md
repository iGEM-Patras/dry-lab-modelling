# Cycle 3b: Can a physics-based observable resolve δ/μ selectivity where ipTM could not?

**Status:** pre-registered · written **before** any Cycle 3b simulation was run
**Type:** method-change cycle: new observable, same design space
**Supersedes:** the original Cycle 3b premise (combine V4+V5 "wins"), **withdrawn**:
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

**1. ipTM has no physical units; ΔΔG does.** ipTM is a confidence score: there is no
conversion from "Δ_sel = 0.007" to a selectivity ratio. A binding free energy in kcal/mol
maps directly onto measurable selectivity via ΔΔG = RT·ln(ratio), which means every
prediction this cycle makes is falsifiable against a radioligand number.

**2. MD removes the approximation that limited every previous cycle.** Boltz-2 cannot
represent D-amino acids or C-terminal amidation. A classical force field can represent both:
but **not out of the box**, and the original wording here ("force fields represent both
routinely") was too glib. See the *Verified software stack* section: amidation is a stock
capping residue, whereas D-residues required a construction step that had to be validated
before this cycle could proceed. It now has been. Two consequences:

- **The real δ-selective controls become available.** Deltorphin I/II carry D-Ala² and a
  C-terminal amide. We could never model them before, so we had no positive control: every
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

**MM-GBSA ΔΔG uncertainty is typically 1–2 kcal/mol.** A 10-fold selectivity improvement,
already an ambitious target for a single-residue change, sits *at or below* that noise
floor. Stated plainly:

> **MM-GBSA is very likely also unable to resolve our designs.** The honest detection floor
> at 2× noise is ≈ 100-fold selectivity; nothing in our panel is expected to reach it.

This is pre-registered as an expected outcome, not discovered afterwards. It is also why
the cycle is **gated**: a method that cannot separate deltorphin II from endomorphin-1 , 
8.4 kcal/mol apart, has no business being applied to a panel separated by ≤ 1 kcal/mol.

---

## Design: a two-stage gate

### Stage 1: method validation on experimental controls (**runs first, decides Stage 2**)

Four peptides with published binding data spanning ≈ 8.4 kcal/mol, each against OPRD1 and
OPRM1 (8 systems × 3 replicates = 24 runs).

| control | sequence | selectivity (lit.) | expected ΔΔG_sel | role |
|---|---|---|---|---|
| Deltorphin II | Tyr-**D-Ala**-Phe-Glu-Val-Val-Gly-**NH₂** | δ, 8448× | **+5.39** | δ anchor |
| Deltorphin I | Tyr-**D-Ala**-Phe-Asp-Val-Val-Gly-**NH₂** | δ, 14318× | **+5.70** | fine-discrimination test |
| Endomorphin-1 | Tyr-Pro-Trp-Phe-**NH₂** | μ, 150× (conservative) | **−2.99** | μ anchor |
| Met-enkephalin | Tyr-Gly-Gly-Phe-Met (free acid) | weakly δ | ≈ 0 | neutral reference |

Sign convention: ΔΔG_sel = ΔG_bind(μ) − ΔG_bind(δ), positive = δ-preferring.

**Gate criteria: all three must hold to run Stage 2:**

- **G1 (sign + rank):** Deltorphin II and Deltorphin I both positive, Endomorphin-1
  negative, with deltorphins ranked above endomorphin-1.
- **G2 (noise floor):** replicate SD of ΔΔG_sel ≤ 1.5 kcal/mol on every control.
- **G3 (calibration slope):** regression of computed vs experimental ΔΔG_sel has positive
  slope with 95 % CI excluding zero (n = 4).

**If the gate fails, Cycle 3b terminates and reports a negative methodological result.**
The modelling line then closes and the project's recommendation stands unchanged: radioligand
competition binding on `YGGFEVVG` and `YGGFDIIG`. No Stage 2 systems will be run in that
case: this is committed in advance precisely so a failed gate cannot be quietly reframed.

### Stage 2: design panel (**conditional on the gate**)

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
  igb = 8 with mbondi3 radii, salt 0.15 M. Entropy **not** estimated: quasi-harmonic and
  normal-mode entropies are unreliable for flexible peptides and would add noise, not
  accuracy. This means we report an **enthalpy-dominated binding effective energy, not a
  true free energy**, and any comparison to experimental ΔΔG inherits that bias.
- **Reported statistic:** mean ± SD across the 3 replicates (replicate-level, not
  snapshot-level, error: snapshot SEM understates uncertainty by ignoring the dominant
  source of variance). Per the Cycle 1 correction, no single-run numbers are reported.

---

## Predictions (committed before any run)

| # | Prediction | Falsified if |
|---|---|---|
| **P1** | Gate criterion G1 passes: deltorphins positive, endomorphin-1 negative | any control has the wrong sign |
| **P2** | Gate criterion G2 passes: replicate SD ≤ 1.5 kcal/mol | any control's SD exceeds 1.5 |
| **P3** | The method **cannot** separate Deltorphin I from II (Δ_exp = 0.31 kcal/mol, far below noise) | they separate with non-overlapping error bars |
| **P4** | **No Stage 2 design reaches ΔΔG_sel ≥ 1.37 kcal/mol** (10-fold) with error bars excluding zero | any design does |
| **P5** | Amidation changes ΔΔG_sel by ≥ 0.5 kcal/mol for at least one design: i.e. the free-acid modelling in Cycles 1–3a was on the wrong species in a way that *mattered* | all acid/amide pairs agree within 0.5 |
| **P6** | Computed ΔΔG_sel magnitudes are **systematically too large** vs experiment (a known MM-GBSA pathology from the missing entropy term and implicit solvent) | slope of computed vs experimental ≤ 1 |

P3, P4 and P6 predict **limitations of our own method**. P4 in particular predicts this
cycle will not find a winner. If P4 is falsified, that is a genuine positive result; if it
holds, the cycle's contribution is a quantitative bound on what the computational screen
could ever have detected, which is the thing Cycles 1–3a lacked.

---

## Compute budget (stated in advance)

Stage 1 is 24 runs × ~20 ns. On one RTX 2080 Ti at ~40–50 ns/day for a ~100 k-atom membrane
system, that is ≈ 11 GPU-days sequentially, less if several GPUs are free. **Stage 1 is the
only committed spend.** Stage 2 (30 runs, ≈ 14 GPU-days) is not authorised unless the gate
passes.

Software availability is **verified**: see the section below.

---

## Verified software stack (probed 2026-07-28, before any production run)

Recorded as required by the pre-registration. Three of these findings **corrected the
assumptions written above**, which is why the probe was a gate on starting rather than a
formality.

| component | verified state | note |
|---|---|---|
| **MD engine** | `gmxcuda`: **GROMACS 2024.5, CUDA**, mixed precision | ✅ runs on `pgpu` (tested via `srun`, gpu:1) |
| MM-GBSA | `gmxmmpbsa`: `gmx_MMPBSA` **v1.5.0.3** + AmberTools (`MMPBSA.py`, `tleap`, `antechamber`, `parmchk2`) | reads GROMACS structures/trajectories (`-cs/-ct/-cp`) |
| protein FF | `leaprc.protein.ff14SB` | ✅ as designed |
| lipid FF | `leaprc.lipid21`; `lipid21.lib` provides **PC, OL, PA** (the POPC building blocks) | ✅ as designed |
| membrane builder | `packmol-memgen` + `packmol` | bilayer construction |
| prep libraries | `parmed` 4.3.1, `numpy` 1.26.4, `scipy` 1.15.2 | `MDAnalysis` **absent** (installable; not required) |
| CHARMM36m | **not on disk** | the design's stated alternative is unavailable → **Amber ff14SB/Lipid21 is the choice, not a preference** |

**Correction 1, the MD and rescoring engines are different builds.** `gmxmmpbsa` ships
GROMACS **2023.4 with OpenCL**, not the CUDA 2024.5 my host notes claimed. OpenCL on NVIDIA
is deprecated and materially slower. Production MD therefore runs in `gmxcuda` (2024.5/CUDA)
and rescoring in `gmxmmpbsa`; trajectories are written in a format both read. The recorded
host note has been fixed.

**Correction 2, there are no D-amino-acid templates in this AmberTools install.**
`amino12.lib`, `aminont12.lib`, `aminoct12.lib` and every library under `dat/leap/` contain
**only L-residues**; no `DALA`/`DAL` template exists anywhere, and `ff14SB_modAA` does not
supply one. The claim that D-residues come free was wrong.

**The workaround is valid, and here is the evidence rather than the assertion.** Chirality at
the α-carbon in ff14SB is encoded **purely geometrically**: the improper-torsion section of
`parm10.dat` contains **zero terms involving the `CX` sp3 α-carbon atom type**, so no energy
term references handedness. A D-residue is therefore the L-residue's parameters at mirrored
coordinates. Reflecting the α-substituents (`HA`, `CB`, `HB1-3`) through the N–Cα–C plane was
tested on the deltorphin II backbone:

| check | result |
|---|---|
| signed volume (N-Cα-C · Cβ), L as built | **+2.535** |
| signed volume after mirroring 5 atoms | **−2.535** (exact sign flip) |
| Cα–Cβ bond length | 1.525 Å → **1.525 Å** (unchanged) |
| `tleap` reparametrization of the mirrored PDB | **0 errors**; bonded sections **byte-identical** to the L topology |
| signed volume after reparametrization | **−2.535** (chirality survives) |

Byte-identical bonded sections are the key result: it confirms the force field genuinely
cannot distinguish the two enantiomers by energy terms, so the D-form carries no
parametrization penalty. `packmol-memgen`/`tleap` will not spontaneously re-invert it.

**Caveat this introduces:** because the topology is enantiomer-blind, nothing in the pipeline
will *warn* if a D-centre inverts through a bad minimisation step. The signed-volume check
above therefore runs as an automated assertion on every control system **after** minimisation
and **after** equilibration, and any run that inverts is discarded rather than analysed.

**Correction 3, amidation is genuinely free.** `NHE` is a stock C-terminal capping residue
in `aminoct12.lib`. A test build of `NTYR-ALA-PHE-GLU-VAL-VAL-GLY-NHE` completed with 0
errors and 110 atoms, C-terminus resolving as `GLY`+`NHE`. The acid/amide comparison (P5)
needs no special handling.

**Not yet verified:** achievable ns/day for a ~100 k-atom membrane system on the `pgpu` RTX
2080 Ti. The ≈11 GPU-day Stage 1 estimate rests on a literature-typical 40–50 ns/day and will
be replaced by a measured benchmark from the first equilibration before the remaining 23 runs
are committed.

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
