# Cycle 8: Alchemical free energy (TI) for δ/μ selectivity

**Status:** designed, pre-registered, not yet run. Written 2026-09-17 **before** any
production window is launched.

**Why this cycle exists.** Three routes to a δ/μ ΔΔG have now been tried and all three
are closed:

| Route | Outcome | Evidence |
|---|---|---|
| ipTM co-folding (Cycle 1–2) | Δ_sel smaller than its own SEM; 4 of 5 predictions falsified | `cycle2_delta_selectivity/` |
| MM-GBSA, n=5 (Cycle 3b) | gate FAIL: G2′ and G3 failed; met-enkephalin off by 26 kcal/mol | `cycle3b_physics_rescoring/docs/GATE_VERDICT_BOUND.md` |
| Boltz-2 affinity head (Cycle 6) | gate FAIL: all 3 gates; deltorphin II called μ-preferring | `cycle6_*` artifacts |

A QSAR screen (Cycle 7, ligand-based, scaffold-split r = 0.768, RMSE 1.07 kcal/mol) then
screened the **entire DNA-encodable single-substitution space** (151 message-intact
candidates) and found **none** exceeding `YGGFEVVG` beyond the conformal 90% interval of
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

The solvent leg cancels in the difference, but is still run: it is the convergence
control, and a solvent leg that disagrees between the two receptor arms means the
sampling is broken.

**Sign convention: ΔΔG > 0 is δ-preferring**, matching every other table in this repo.

## 2. Protocol

- **λ schedule** (`data/lambda_schedule.csv`): 27 windows, 11 decoupling electrostatics
  at full vdW, then 16 decoupling vdW, dense near the endpoint where ∂H/∂λ is steepest.
  Soft-core `sc-alpha = 0.5`, `sc-power = 1`, `sc-sigma = 0.3`.
- **10 ns per window**, Langevin (`integrator = sd`), dt = 2 fs, `couple-intramol = no`.
- **2 independent replicates** per system-receptor pair, different `ld-seed`.
- Semi-isotropic C-rescale barostat at 310 K / 1 bar for the bilayer.
- GROMACS **2024.5 CUDA** from `/data/users/kzanaj/envs/gmxcuda`, called by absolute
  path, because these env dirs have no `bin/activate` (host notes).
- Analysis by `gmx bar` (built in). `alchemlyb`/`pymbar` are **not** installed and are
  not needed.

## 3. Compute budget: measured, not assumed

Using the host's own recorded throughput (**71.5 ns/day**, 270 k-atom POPC+GPCR+peptide,
1 GPU / 8 threads) rather than a literature estimate:

| Design | legs | total ns | pgpu only | pibu only | both |
|---|---|---|---|---|---|
| "max settings" 5 peptides × 3 reps × 20 ns | 30 | 16 200 | 113 d | 68 d | 42 d |
| **this cycle: 8 systems × 2 reps × 10 ns** | **32** | **8 640** | 60 d | 36 d | **22.6 d** |

Literal max settings are **not feasible**: 113 GPU-days against a 28-day wall cap on a
single shared node. The dual-partition split the host notes recommend (longest-first to
the 2 GPU slots, remainder to ~20 `pibu_el8` CPU slots) brings the calibrated design to
**~23 days**, inside the wall limit.

`pgpu` start estimates are **identical for 8 h, 48 h and 168 h requests** (all 2026-09-17
21:38), so long walltime is free here and is requested generously.

## 4. Calibration set, and the force-field trap that shaped it

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

**Why no deltorphins.** The obvious δ-selective peptide controls, deltorphin I/II, DPDPE,
DAMGO, all contain **D-residues or non-standard residues**, and this host has *no
D-amino-acid templates* (`amino12.lib` and all of `dat/leap` are L-only; host notes).
Building them requires hand-mirroring the α-substituents, and because `parm10.dat` has
**zero improper terms on the CX α-carbon**, chirality is purely geometric and *the force
field cannot detect an accidental inversion*. Rather than put that risk in the calibration
set, δ-selectivity is supplied by **small molecules** (naltrindole, clocinnamox), which go
through GAFF/antechamber from 3D structures where chirality is handled correctly.

This costs range: the set tops out at +2.13 rather than deltorphin II's +5.39. Stated as a
limitation, not hidden: the gate below is correspondingly weaker on the δ-selective end.

**Source discipline.** All seven ΔΔG values are ChEMBL medians, a **single source**. The
repo's earlier literature values must not be mixed in: for endomorphin-1 the repo records
−2.99 and ChEMBL gives −4.82, a **1.84 kcal/mol disagreement on the same molecule**. The
median between-study scatter across the well-measured compounds is 0.71 kcal/mol, i.e.
~10 % of the 6.95 kcal/mol span, which is what makes the calibration viable at all.

## 5. PRE-REGISTERED gates, written before any window runs

| id | criterion | threshold |
|---|---|---|
| **C1** | signs of ΔΔG correct across the 7 controls | ≥6 of 7 |
| **C2** | Pearson r vs ChEMBL ΔΔG across the 7 controls | **\|r\| > 0.754** (p<0.05, n=7) |
| **C3** | per-window λ overlap adequate everywhere | no adjacent-window overlap below 0.03 |
| **C4** | replicate agreement | \|ΔΔG_rep1 − ΔΔG_rep2\| < 1.5 kcal/mol for every control |
| **C5** | report `YGGFEVVG` | **only if C1–C4 all pass** |

C1–C4 are gates. **If any fails, the ΔΔG for `YGGFEVVG` is not reported**, the same rule
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
- **Binding, not efficacy.** Every ΔΔG here (computed and reference) is a *binding*
  quantity. None of it predicts agonist potency or efficacy. A δ-preferring binder can
  still be a poor δ agonist; only a functional assay settles that.
- **One GPU, not two.** The second `pgpu` GPU is held by another user's job with ~4 d 21 h
  remaining, so the GPU arm starts at one slot and widens later.

## 7. Files

- `data/fep_controls.csv`: the 7 controls with ChEMBL ids, ΔΔG, evidence counts, route
- `data/lambda_schedule.csv`: the 27-window λ schedule
- `data/fep_budget.csv`: the measured-throughput budget table
- `mdp/ti_00.mdp` … `ti_26.mdp`: per-window production inputs

---

## 8. Gate script dry-run: C3/C4 are load-bearing, demonstrated not asserted

`scripts/gate_ti.py` scores C1–C5 and was dry-run on two synthetic datasets before any
real window exists (`dryrun/`). The well-behaved case passes and reports the target; the
non-converged case fails and withholds it. Exit codes 0 and 3 respectively.

**The finding that justifies adding C3 and C4.** In the deliberately non-converged case:
15.0 kcal/mol spread between replicates and λ overlap of 0.01, the *correlation* gate
still **passed** at r = 0.802, p = 0.03:

| gate | well-behaved | non-converged |
|---|---|---|
| C1 signs | PASS (6/7) | **PASS (6/7)** |
| C2 correlation | PASS (r = 0.997) | **PASS (r = 0.802)** |
| C3 λ overlap | PASS (0.10) | FAIL (0.01) |
| C4 replicate spread | PASS (1.0 kcal/mol) | FAIL (15.0 kcal/mol) |
| **C5 target** | reported | **withheld** |

So a campaign with unusable sampling would have cleared a correlation-and-sign gate of
exactly the kind used in Cycles 3b and 6, and produced a plausible ΔΔG for `YGGFEVVG`.
C3 and C4 are the only reason it is caught. This is the concrete form of the risk named in
§6: TI's characteristic failure is a smooth, believable number from unconverged windows.

Two implementation notes recorded because both cost a fix:
- `ndarray.ptp()` is removed in NumPy 2; use `np.ptp(arr)`.
- C4 is evaluated on controls only. The target has no reference value, so its replicate
  spread cannot be a pass criterion without circularity; it is reported alongside the ΔΔG.

---

## 9. Prerequisite validation: five errors caught before production (2026-09-17)

Five separate faults were found by staged validation jobs costing under two hours of
`pshort_el8` and ~20 min of GPU. Each would have failed or corrupted the full campaign.

| # | Fault | How it would have presented |
|---|---|---|
| 1 | `tc-grps = SOLU MEMB SOLV`: no group named `SOLU` exists | all 864 windows fail identically at `grompp` |
| 2 | `couple-moltype = LIG`: topology names molecules `system1/2/3` | `grompp` fatal, "did not find any molecules of type 'LIG'" |
| 3 | `couple-intramol = no` with a flexible peptide | `mdrun` fatal: perturbed excluded pairs beyond the pair-list cutoff |
| 4 | calibration assumed n=7 with a correlation gate | only 4 peptide systems exist; correlation gate is unreachable |
| 5 | diagnostic scripts using `\| head` under `exec > >(tee …)` | SIGPIPE, exit 141: three jobs "failed" with truncated reports |

**Authoritative values, read from an existing `prod.tpr` rather than assumed:**
thermostat groups are **`Protein MEMB SOLV`** (grpname list: System, Protein, MEMB, SOLV,
rest), `ref-t 310 310 310`, `tau-t 1 1 1`.

**Ligand moleculetype is `system2`**, confirmed by atom count against chemical formula, not
by inference: `system1` = 5755 atoms (receptor), `system2` = **75 atoms**, `system3` = 134
atoms (POPC). Met-enkephalin is C27H35N5O7S = exactly **75 atoms**. Decoupling `system1` by
mistake would not have errored; it would have run for weeks and produced a number.

**`couple-intramol = yes` is exact here, not a compromise.** `no` gives the ideal-gas
reference required for an *absolute* ΔG. This cycle computes ΔΔG = ΔG(δ) − ΔG(μ) for the
**same** ligand, so intramolecular and solvent contributions are identical in both legs and
cancel exactly; the difference is unchanged. The solvent leg remains in the protocol as a
convergence control, not as a term in the answer.

### Chirality verification: the deltorphins are usable, which lifts Cycle 7's worst limit

Host notes warn that `parm10.dat` has **zero improper terms on the CX α-carbon**, so
chirality is purely geometric and the force field **cannot detect an inversion**.
`scripts/check_chirality.py` computes the signed volume (N−CA)×(C−CA)·(CB−CA) for every
chiral residue and uses the receptor's own L-residues as the internal reference, so no sign
convention is needed: a D-residue is whichever residue carries the minority sign.

| System | chiral residues | inverted | verdict |
|---|---|---|---|
| deltorphin I | 358 | **1**, resid 2, ALA | D-Ala² correct |
| deltorphin II | 358 | **1**, resid 2, ALA | D-Ala² correct |
| met-enkephalin | 355 | 0 | all-L correct |
| endomorphin-1 | 356 | 0 | all-L correct |

The two all-L peptides are the negative controls for the same test that produced the
positive result. **Consequence:** deltorphin I (+5.70) and II (+5.39) are available, so this
cycle covers the strongly δ-selective regime that Cycle 7's ChEMBL panel could not reach
(its maximum was +2.13). Those are also the two compounds the Boltz-2 affinity head called
with the **wrong sign** at n=4.

*Caveat on an argument, not on the result:* the inference that the peptide occupied low
residue numbers was wrong, the receptor is first in the file. The chirality conclusion
stands on a **differential**: all four systems share the same receptor, and the inverted
residue appears only in the two deltorphins. A receptor alanine would have appeared in all
four.

### Revised gate: ORDINAL, not correlational

Only 4 peptide systems exist on disk, so n=4 and the critical |r| is **0.950**, no honest
method clears that. **C2 is therefore replaced for this cycle:**

| id | criterion | threshold |
|---|---|---|
| C1 | signs of ΔΔG correct across the 4 controls | **4 of 4** |
| C2′ | ranking correct (Spearman ρ) | **ρ = 1.0** (note p = 0.33 at n=4; ordinal evidence, not significance) |
| C3 | per-window λ overlap | no adjacent overlap < 0.03 |
| C4 | replicate agreement | < 1.5 kcal/mol per control |
| C5 | report `YGGFEVVG` | only if C1–C4 pass |

**What TI adds over Cycle 7 is not statistical power**, Cycle 7 had n=13 and a real
correlation gate. It is (a) no compression slope to correct for, and (b) coverage of the
strongly δ-selective end. Both must be stated whenever this result is quoted next to
Cycle 7's.

### Reused assets and the remaining gap

**41 complete equilibrated replicates** exist at
`/data/users/kzanaj/boltz_dock/cycle3b/systems/c3b_{dtI,dtII,em1,menk}_{DOR,MOR}/rep{1..5}/`
(`npt.gro` + `system.top` + `index.ndx` + `prod.tpr`). The membrane build is therefore off
the critical path, this matters because Cycle 3b's membrane gate refused 9 of 40 runs.

Excluded pending confirmation: `c3b_bogus_DOR` (name suggests a deliberate negative control)
and `c3b_dtII_DOR/rep99` (looks like a re-run, not a 6th replicate; pooling it would
corrupt C4).

**Gap: `YGGFEVVG` has no equilibrated system.** All four on disk are controls. Build route
chosen: rebuild the peptide into an existing equilibrated receptor+bilayer box (route B),
because our peptide is all-L standard (no mirrored residue needed) and reusing the
validated box avoids the membrane gate. Post-build checks, all mandatory before any
production window: system2 atom count = **113** (C39H54N8O12 for YGGFEVVG), chirality check
returns **zero** inverted residues, all 27 windows grompp, and the peptide is still in the
orthosteric pocket.

### Execution architecture

λ windows are independent, so production runs as a **SLURM array over windows** on `pgpu`
rather than one monolithic job: short tasks backfill where a multi-week job cannot, a failed
window costs one window, and partial results can be scored continuously. `pgpu` returns the
same start estimate for 8 h / 48 h / 168 h requests, so walltime is free, but the partition
has only **2 GPUs**, so total wall time remains work ÷ 2 slots. `pibu_el8` is estimated
7 November at every request size and `pcmpg_el8` is not available to this account, so `pgpu`
is the only path.

---

## 10. Measured throughput, chosen scope, and launch (2026-09-17)

### The pilot replaced an estimate with a measurement

**44.8 ns/day per GPU** for FEP with soft-core decoupling on the 164k-atom system
(window 0 completed 250 ps in 488 s wall on an RTX 2080 Ti). The host's plain-MD
benchmark of 71.5 ns/day was measured on a *larger* 270k-atom system, so it was not a
conservative proxy: FEP costs a factor of **1.60x**, and the earlier budget was
optimistic by 60%. Every number in section 8 that derives from 71.5 ns/day is
superseded by `data/fep_budget_measured.csv`.

The pilot also found the `couple-intramol` fault (section 9, #3) and cost ~20 min of
GPU. Sizing the campaign on the unmeasured rate would have committed weeks on a
protocol that died in the first seconds of every window.

### Chosen scope: necessary first, extension if time allows

Rationale from the PI: do the absolutely necessary work, and extend toward a complete
picture only if time permits. Because every λ window is independent and the protocol is
identical across legs, the extension is **additive**, not a re-run, so both fit in one
priority-ordered work queue:

| Priority | Systems | Legs | Tasks | ns | Days @2 GPU |
|---|---|---|---|---|---|
| **Necessary** | deltorphin II, endomorphin-1 | 8 | 0–215 | 648 | ~7.2 |
| Extension | deltorphin I, met-enkephalin | 8 | 216–431 | 648 | ~7.2 |
| Blocked | engPENK (no system yet) | 4 | N/A | 324 | ~3.6 |

The two necessary controls **bracket the widest available range**: deltorphin II at
**+5.39** and endomorphin-1 at **−4.82**, a span of **10.21 kcal/mol**. They are also
the pair the Boltz-2 affinity head called with the **wrong sign** at n=4.

**Gate for the n=2 scope, written before submission:**

| id | criterion | threshold |
|---|---|---|
| D1 | signs correct | 2 of 2 |
| D2 | bracketing: dtII > 0, em1 < 0, computed span | ≥ 5 kcal/mol |
| D3 | adjacent-window λ overlap | none < 0.03 |
| D4 | replicate agreement per control | < 1.5 kcal/mol |
| D5 | report `YGGFEVVG` | only if D1–D4 pass |

**n=2 admits no correlation gate and no magnitude calibration.** If reported, the target
ΔΔG is a physics estimate *bracketed* by two controls, not a calibrated one. Cycle 7's
n=13 correlation gate remains the statistically stronger claim; this cycle's contribution
is the absence of a compression slope and coverage of the δ-selective extreme.

**Rejected: 1 replicate to save 15 days.** It makes D4 unscoreable, and D4 is one of the
two gates that catch non-convergence: the dry run (section 7) showed sign and
correlation gates *passing* on data with 15 kcal/mol replicate spread.

### Execution: work queue, not an array

`--array` is host-managed and cannot be nested, which forced a better design: a shared
work queue on `/data/users/kzanaj/cycle8_prod` with two workers claiming tasks atomically
via `mkdir` locks. Workers scan from index 0, so **queue order is priority order** and the
necessary set completes first. Each task checks for a complete `dH/dλ` output and skips
rather than repeats, so a node failure costs one window. Trajectories are deleted per
window: only `dH/dλ` is needed, which keeps 432 windows off the disk quota.

### Blocker: `pgpu` node down

`binfservas30` is **`down*`, reason "Not responding"** (`0/0/128/128`). Both workers are
`PD` with `ReqNodeNotAvail`; **0 of 432 tasks claimed**. The 27 mdp files are staged and
the queue is resume-safe, so nothing needs resubmitting when the node returns. The ~7-day
figure is wall-clock **from a running start**: the node's return time is the number that
decides whether this cycle lands inside the project deadline, and it is not visible from
here.

Note: the earlier pilot's `NODE_FAIL` (job 18440798, after 20:12) was this same node
failing, not a script fault. Window 0 had already produced the throughput measurement.

### engPENK system build: proceeding on CPU during the outage

`build_system.sh` has a `MIN_NB=cpu` code path; minimisation is the only GPU step, so the
build runs entirely on `pshort_el8` and the outage does not block it.

*(Correction, twice over. An earlier note credited [`MIN_ON_CPU.md`](../cycle3b_physics_rescoring/MIN_ON_CPU.md)
for sanctioning this. A `cat`/`find` on the cluster working directory returned nothing, so
that credit was retracted as unverified, but the search looked under
`$D/boltz_dock/cycle3b`, not the repository. **The document does exist**, at
`06_engineering_cycles/cycle3b_physics_rescoring/MIN_ON_CPU.md`, dated 2026-08-12, and it
states precisely what was originally claimed: minimisation is steepest descent to a
convergence criterion on 119,476 atoms, the GPU buys nothing that justifies the queue wait,
and `build_system.sh` now honours `MIN_NB=cpu` with `gpu` as the default. The original claim
was correct; the retraction was the error, caused by searching one filesystem and concluding
about another.)*

**Chemistry declared from the design table's own convention, not a default.**
`prod_all.txt` records all four designed peptides as `amide=yes` and met-enkephalin, the
neutral reference, as the single `amide=no` entry. `YGGFEVVG` as released by the digest is
a **free acid**, so `c8_engPENK_{DOR,MOR} → amide=no, dres=none` follows that convention.
Declared in a **separate** `prod_cycle8.txt` via the `PROD_TABLE` override; Cycle 3b's
table is untouched as the record of what Cycle 3b ran.

`scripts/peptide_spec.sh` documents why this is not a formality: on 2026-07-30 a positional
argument silently defaulting to `none` built the **all-L analog of deltorphin II**, and
because the chirality gate is itself skipped when that argument is `none`, *"a silent
default in the argument feeding a safety gate disables the gate."* The system passed every
downstream check.

**Consequence for our peptide, stated plainly:** `dres=none` is correct for `YGGFEVVG`, but
it also means **the build's own chirality gate will be skipped for the target system**. The
independent signed-volume check (`scripts/check_chirality.py`) is therefore the only
chirality verification the target system will receive, and running it post-build is
mandatory, not optional: it must return **zero** inverted residues.

**Starting poses** are Cycle 7's existing co-folds, with their own confidence on the
record: `engPENK_YGGFEVVG__OPRD1` ipTM **0.958**, pLDDT 0.836; `__OPRM1` ipTM **0.957**,
pLDDT 0.804.

**Mandatory post-build checks:** `system2` atom count = **113** (C39H54N8O12), chirality
returns zero inverted residues, all 27 windows grompp, peptide still in the orthosteric
pocket.

---

## 11. The campaign is no longer GPU-gated (2026-09-18)

`pgpu` has one node, `binfservas30`, `down*` / "Not responding" for >24 h. Both GPU
workers have been pending with `ReqNodeNotAvail` throughout and 0 of 432 windows were
claimed. Every CPU workaround for the *co-fold* failed (see `GRAFT_ROUTE_REJECTED.md` and
the two 2-hour wall kills), so the campaign looked blocked indefinitely.

### An error of mine that cost a day

I had recorded `pibu_el8` as unusable: "estimated 7 November at every request size". That
was a `--start` estimate for a **large, long** allocation, generalised into a dead
partition without ever testing a small request. Read directly:

```
pibu_el8   MaxTime=28-00:00:00   AllowAccounts=ALL   TotalCPUs=2864
pshort_el8 MaxTime=02:00:00      TotalCPUs=256
```

`sacctmgr` confirms this account holds a `pibu_el8` association with `normal` QoS, and
`sbatch --test-only` accepted both 6 h and 12 h requests with a start estimate four hours
out. In practice the scheduler backfilled the jobs **immediately**. The partition was
always available; the claim in §10 was wrong, and it is the same failure mode as assuming
`tc-grps = SOLU` instead of reading `prod.tpr`, an inference standing in for a
measurement. The user caught it by asking "no pibu_el left?".

### Measured CPU FEP throughput

**5.864 ns/day per 32-core job** (one pre-built λ window, 50 ps, `binfservas*`,
`-nb cpu -pme cpu`). Against the measured GPU rate of 44.801 ns/day that is **7.6× slower,
not the 10–20× I had guessed**: 131 core-hours per ns. At 3 ns/window that is
**12.3 h per window**, ~2 windows/worker/day.

| arm | legs | ns | job-days | wall @ 6 | wall @ 13 |
|---|---|---|---|---|---|
| necessary (dtII + em1) | 8 | 648 | 110.5 | 18.4 d | **8.5 d** |
| extension (dtI + menk) | 8 | 648 | 110.5 | 18.4 d | 8.5 d |
| target (engPENK) | 4 | 324 | 55.3 | 9.2 d | 4.3 d |

The necessary arm fits the 28-day wall with wide margin. All three arms together need ~10
concurrent workers to fit; 446 cores were idle, i.e. 13 jobs' worth.

### Running configuration

**13 CPU workers on `pibu_el8`**, 32 cores each, `-pin on`, 14-day wall, pulling the
**same** atomically-claimed queue as the two pending GPU workers, so CPU and GPU never
duplicate a window and `pgpu` returning now *accelerates* rather than *enables*. Priority
order is preserved (workers scan from index 0): the two bracketing controls complete before
the extension begins. `-cpi` means a node failure costs minutes, not a window.
Trajectories are deleted per window; only dH/dλ is retained.

First status check: 13 workers RUNNING, 13/432 claimed (one each, claiming verified),
0 complete, which is correct given 12.3 h/window against ≤1h52m of uptime. No mdrun errors.

### A failed optimisation, and why it was abandoned

A core-count scaling sweep (8/16/32/64, pin on/off) returned **zero for all eight
configurations**: the script sent `mdrun` output to `/dev/null`, discarding the diagnostic
needed to explain the failure. That is the third instrumentation self-own of this campaign
after the `| head` SIGPIPE kills and `find -printf '%f'` printing a basename where a size
was intended. It was not re-run: the campaign was already progressing at a measured rate,
and a possible 1.5× from re-sharding did not justify stalling a deadline-constrained run.
**Standing rule: a test whose purpose is to produce a number must never discard stderr.**

### What does and does not trade against precision

Core count and worker count affect **wall time only**: identical equations of motion,
identical dH/dλ statistics. The only precision lever is **ns/window**, held at 3 ns.
Dropping to 2 ns would save a third of the wall time and put the C3/C4 convergence gates at
genuine risk of a legitimate "did not converge", so it was not done.
