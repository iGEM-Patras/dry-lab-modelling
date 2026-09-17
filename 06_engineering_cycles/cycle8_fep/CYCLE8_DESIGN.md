# Cycle 8 — Alchemical free energy (TI) for δ/μ selectivity

**Status:** designed, pre-registered, not yet run. Written 2026-09-17 **before** any
production window is launched.

**Why this cycle exists.** Three routes to a δ/μ ΔΔG have now been tried and all three
are closed:

| Route | Outcome | Evidence |
|---|---|---|
| ipTM co-folding (Cycle 1–2) | Δ_sel smaller than its own SEM; 4 of 5 predictions falsified | `cycle2_delta_selectivity/` |
| MM-GBSA, n=5 (Cycle 3b) | gate FAIL — G2′ and G3 failed; met-enkephalin off by 26 kcal/mol | `cycle3b_physics_rescoring/docs/GATE_VERDICT_BOUND.md` |
| Boltz-2 affinity head (Cycle 6) | gate FAIL — all 3 gates; deltorphin II called μ-preferring | `cycle6_*` artifacts |

A QSAR screen (Cycle 7, ligand-based, scaffold-split r = 0.768, RMSE 1.07 kcal/mol) then
screened the **entire DNA-encodable single-substitution space** — 151 message-intact
candidates — and found **none** exceeding `YGGFEVVG` beyond the conformal 90% interval of
1.71 kcal/mol. PAM amidation shifts ΔΔG by a consistent but negligible **+0.040 kcal/mol**,
43× below the method's own resolution.

**Consequence for this cycle's question.** There is no variant worth discriminating. The
question is therefore *not* "which sequence is most δ-selective" but:

> **Is `YGGFEVVG` δ-preferring at all, and by how much, with an error bar, from a method
> calibrated on this cluster against ligands of known δ/μ pharmacology?**

Thermodynamic integration is the only remaining route that includes the entropy term whose
absence is the documented cause of the MM-GBSA failure.

---

## 1. What is computed

Absolute-style decoupling of the ligand from (a) the receptor complex and (b) bulk water,
run independently at **OPRD1** and **OPRM1**. The reported quantity is

```
ΔΔG(δ/μ)  =  [ΔG_complex(δ) − ΔG_solvent]  −  [ΔG_complex(μ) − ΔG_solvent]
           =   ΔG_complex(δ) − ΔG_complex(μ)
```

The solvent leg cancels in the difference, but is still run — it is the convergence
control, and a solvent leg that disagrees between the two receptor arms means the
sampling is broken.

**Sign convention: ΔΔG > 0 is δ-preferring**, matching every other table in this repo.

## 2. Protocol

- **λ schedule** (`data/lambda_schedule.csv`): 27 windows — 11 decoupling electrostatics
  at full vdW, then 16 decoupling vdW, dense near the endpoint where ∂H/∂λ is steepest.
  Soft-core `sc-alpha = 0.5`, `sc-power = 1`, `sc-sigma = 0.3`.
- **10 ns per window**, Langevin (`integrator = sd`), dt = 2 fs, `couple-intramol = no`.
- **2 independent replicates** per system-receptor pair, different `ld-seed`.
- Semi-isotropic C-rescale barostat at 310 K / 1 bar for the bilayer.
- GROMACS **2024.5 CUDA** from `/data/users/kzanaj/envs/gmxcuda` — called by absolute
  path, because these env dirs have no `bin/activate` (host notes).
- Analysis by `gmx bar` (built in). `alchemlyb`/`pymbar` are **not** installed and are
  not needed.

## 3. Compute budget — measured, not assumed

Using the host's own recorded throughput (**71.5 ns/day**, 270 k-atom POPC+GPCR+peptide,
1 GPU / 8 threads) rather than a literature estimate:

| Design | legs | total ns | pgpu only | pibu only | both |
|---|---|---|---|---|---|
| "max settings" 5 peptides × 3 reps × 20 ns | 30 | 16 200 | 113 d | 68 d | 42 d |
| **this cycle: 8 systems × 2 reps × 10 ns** | **32** | **8 640** | 60 d | 36 d | **22.6 d** |

Literal max settings are **not feasible** — 113 GPU-days against a 28-day wall cap on a
single shared node. The dual-partition split the host notes recommend (longest-first to
the 2 GPU slots, remainder to ~20 `pibu_el8` CPU slots) brings the calibrated design to
**~23 days**, inside the wall limit.

`pgpu` start estimates are **identical for 8 h, 48 h and 168 h requests** (all 2026-09-17
21:38), so long walltime is free here and is requested generously.

## 4. Calibration set — and the force-field trap that shaped it

Seven reference ligands, each with **≥3 independent Ki measurements at both** human OPRD1
and OPRM1 in ChEMBL, spanning **6.95 kcal/mol** (`data/fep_controls.csv`):

| Ligand | ΔΔG_exp | min n | route |
|---|---|---|---|
| endomorphin-1 | −4.82 | 5 | ff14SB templates |
| fentanyl | −3.55 | 3 | GAFF |
| naltrexone | −2.57 | 40 | GAFF |
| JDTIC | −1.36 | 3 | GAFF |
| clocinnamox | +0.06 | 5 | GAFF |
| enkephalin | +0.81 | 5 | ff14SB templates |
| naltrindole | +2.13 | 13 | GAFF |

**Why no deltorphins.** The obvious δ-selective peptide controls — deltorphin I/II, DPDPE,
DAMGO — all contain **D-residues or non-standard residues**, and this host has *no
D-amino-acid templates* (`amino12.lib` and all of `dat/leap` are L-only; host notes).
Building them requires hand-mirroring the α-substituents, and because `parm10.dat` has
**zero improper terms on the CX α-carbon**, chirality is purely geometric and *the force
field cannot detect an accidental inversion*. Rather than put that risk in the calibration
set, δ-selectivity is supplied by **small molecules** (naltrindole, clocinnamox), which go
through GAFF/antechamber from 3D structures where chirality is handled correctly.

This costs range: the set tops out at +2.13 rather than deltorphin II's +5.39. Stated as a
limitation, not hidden — the gate below is correspondingly weaker on the δ-selective end.

**Source discipline.** All seven ΔΔG values are ChEMBL medians — a **single source**. The
repo's earlier literature values must not be mixed in: for endomorphin-1 the repo records
−2.99 and ChEMBL gives −4.82, a **1.84 kcal/mol disagreement on the same molecule**. The
median between-study scatter across the well-measured compounds is 0.71 kcal/mol, i.e.
~10 % of the 6.95 kcal/mol span, which is what makes the calibration viable at all.

## 5. PRE-REGISTERED gates — written before any window runs

| id | criterion | threshold |
|---|---|---|
| **C1** | signs of ΔΔG correct across the 7 controls | ≥6 of 7 |
| **C2** | Pearson r vs ChEMBL ΔΔG across the 7 controls | **\|r\| > 0.754** (p<0.05, n=7) |
| **C3** | per-window λ overlap adequate everywhere | no adjacent-window overlap below 0.03 |
| **C4** | replicate agreement | \|ΔΔG_rep1 − ΔΔG_rep2\| < 1.5 kcal/mol for every control |
| **C5** | report `YGGFEVVG` | **only if C1–C4 all pass** |

C1–C4 are gates. **If any fails, the ΔΔG for `YGGFEVVG` is not reported** — the same rule
that withheld the Cycle 6 number and would have prevented a meaningless agreement with the
Cycle 2 null being read as confirmation.

C3 and C4 are new relative to earlier cycles and are there because TI's characteristic
failure is *plausible-looking non-convergence*: a flexible peptide in a large pocket can
return a smooth, believable ΔΔG from unconverged windows. Overlap and replicate spread
make that visible instead of silent.

## 6. Known risks, named in advance

- **Convergence for a flexible peptide.** The same conformational freedom that made
  MM-GBSA fail on met-enkephalin by 26 kcal/mol threatens TI. C3/C4 are the detectors;
  if they fail the honest output is "TI does not converge for this system at this budget".
- **Membrane setup is the hard part, not the sampling.** Cycle 3b had 9 of 40 runs refused
  by its membrane gate. This cycle **reuses the validated Cycle 3b bilayer build** rather
  than constructing a new system.
- **Binding, not efficacy.** Every ΔΔG here — computed and reference — is a *binding*
  quantity. None of it predicts agonist potency or efficacy. A δ-preferring binder can
  still be a poor δ agonist; only a functional assay settles that.
- **One GPU, not two.** The second `pgpu` GPU is held by another user's job with ~4 d 21 h
  remaining, so the GPU arm starts at one slot and widens later.

## 7. Files

- `data/fep_controls.csv` — the 7 controls with ChEMBL ids, ΔΔG, evidence counts, route
- `data/lambda_schedule.csv` — the 27-window λ schedule
- `data/fep_budget.csv` — the measured-throughput budget table
- `mdp/ti_00.mdp` … `ti_26.mdp` — per-window production inputs
