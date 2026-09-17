# The δ-opioid receptor connection — what is already shown, and Plan B

**Written 2026-09-17, before the wet lab runs any DOR assay.** Answers two questions from
the wet lab: (1) can the DOR interaction be shown *in silico*, and has it been done;
(2) what is the fallback if the wet-lab demonstration fails.
![DOR evidence status: what the co-folding shows, what selectivity does not, and the calibrated Plan B route]({{artifact:art_51962b67-a319-4b70-a4e5-f7c2bd8791f9}})
![DOR evidence status](/home/kay/.claude-science/orgs/6cf41134-f542-4332-8c2d-8b7df40cdb61/artifacts/proj_b5d9b81f671a/51962b67-a319-4b70-a4e5-f7c2bd8791f9/v777debf9_dor_evidence_status.png)

---

## 0. One terminology correction first

The request said "DOR **inhibitor**". DOR (δ-opioid receptor, gene `OPRD1`) is a
**Gi/o-coupled** GPCR, and enkephalins — native and engineered — are **agonists** at it.
The *inhibition* is downstream: agonist occupancy inhibits adenylyl cyclase and lowers
cAMP. So the peptide is an agonist whose cellular consequence is inhibitory; it is not a
receptor inhibitor (that would be an antagonist, e.g. naltrindole).

This is not pedantry — **it determines the assay.** An agonist is measured by the response
it *produces*; an antagonist by the response it *blocks*. Everything below assumes agonist.
If the wet lab has been planning an antagonist-style assay, that is worth catching now.

---

## 1. Yes — it is already done. Two independent lines.

### 1.1 Co-folded structure (Boltz-2)

| Complex | interface ipTM | complex ipTM | peptide pLDDT | file |
|---|---|---|---|---|
| **`YGGFEVVG`** + human OPRD1 | **0.809** | 0.972 | 81.3 | `04_structures/engPENK_octapeptide_YGGFEVVG_DORbound.pdb` |
| native `YGGFM` + human OPRD1 | 0.757 | 0.979 | 87.2 | `04_structures/native_MetEnkephalin_YGGFM_DORbound.pdb` |

Repeated across 5 diffusion samples per complex (Cycle 2, MSA = 1024):

| Peptide | ipTM at δ | ipTM at μ | δ-pose convergence |
|---|---|---|---|
| native `YGGFM` | 0.9754 ± 0.0071 | 0.9704 ± 0.0089 | 1.42 Å |
| **engineered `YGGFEVVG`** | **0.9671 ± 0.0085** | 0.9556 ± 0.0280 | **1.14 Å** |

**What this supports:** the engineered octapeptide is predicted to occupy the δ orthosteric
pocket with confidence statistically indistinguishable from native Met-enkephalin, and with
a *more* converged pose at δ than native. On interface ipTM in the single-complex run it
scores slightly *above* native (0.809 vs 0.757). This is a legitimate, showable in-silico
result and it is already in the repository.

**What it does not support: affinity.** ipTM is a structural-confidence metric, not a
binding energy. High ipTM at both receptors means "a plausible complex was built", not
"it binds tightly". Do not present ipTM as a surrogate for potency.

### 1.2 δ-selectivity — falsified, by our own dry lab

| Peptide | Δ_sel = ipTM(δ) − ipTM(μ) | p |
|---|---|---|
| native `YGGFM` | +0.0050 ± 0.0051 | 0.36 |
| engineered `YGGFEVVG` | +0.0114 ± 0.0131 | **0.43** |

`YGGFEVVG`'s δ-preference is **smaller than its own uncertainty** and indistinguishable
from zero, and from native (p = 0.60). Cycle 1's headline "**1.96× native selectivity**"
was **retracted** — it came from `model_0` alone and did not survive 5-sample statistics.
4 of 5 Cycle 2 pre-registered predictions were falsified, and the *only* statistically
significant selectivity in the whole panel (V1 `YGGFEIIG`, p = 0.021) points toward **μ**.

> **Tell the wet lab to expect DOR *activity*, not δ-*selectivity*.** If the planned
> experiment is designed to demonstrate selectivity, our own dry lab predicts it will not
> show one — and that prediction is already on record, pre-registered, in `CYCLE2_RESULTS.md`.
> A null selectivity result would *confirm* our model, not refute the project.

---

## 2. The real gap — and it needs no wet lab

The MM-GBSA physics-rescoring pipeline (Cycle 3b) is **validated end-to-end** — four
defects found and fixed, including one silently emitting the ligand's absolute energy
instead of the binding delta. But its 8 systems are Met-enkephalin, endomorphin-1,
deltorphin I and deltorphin II. **It was never run on `YGGFEVVG`.**

So our own peptide has co-folding confidence only, while four benchmark peptides have
physics-based ΔΔG. Closing that is the single highest-value dry-lab action available, and
it does not depend on the transfection.

---

## 3. Wet-lab Plan B

### 3.1 A negative result is ambiguous — design to disambiguate it

"No DOR connection" has four causes, and the DOR assay alone cannot separate them:

1. No peptide was produced (digest failed)
2. Peptide produced but lost in handling — aggregation near its pI (`SUBSTRATE_PREP_BRIDGE.md` §3)
3. Assay not functioning
4. Peptide genuinely inactive at DOR

### 3.2 The one control that splits them: synthetic peptide, run in parallel

**`STD-ENGC` (`YGGFEVVG`) is already on the control-peptide order sheet**
(`07_invitro_penk/tables/control_peptides_order.csv`). Run the DOR assay on synthetic
`YGGFEVVG` alongside the digest-derived material, every time.

| Synthetic | Digest-derived | Native `YGGFM` | Conclusion |
|---|---|---|---|
| active | inactive | — | production/recovery problem (causes 1–2). **Pharmacology is fine.** |
| inactive | inactive | active | the peptide design is the problem (cause 4) |
| inactive | inactive | inactive | assay problem (cause 3) — nothing learned about the peptide |

Without the synthetic arm, a negative result is uninterpretable and the time is wasted.
`STD-MENK` (`YGGFM`) is also already on the sheet and is the assay's positive control.
**Both are commercial peptides — order them now, not after a failure.** Given the tight
timeline this is the highest-leverage thing the wet lab can do today.

### 3.3 Assay formats compatible with the no-animal / no-antibody constraint

DOR is Gi-coupled, so agonist → ↓cAMP. Ranked by fit to the standing constraints:

| Format | Readout | Fits? | Note |
|---|---|---|---|
| **cAMP reporter** (GloSensor or CRE-luciferase) | luminescence | **yes** — plasmid + plate reader | forskolin-stimulated; agonist *lowers* signal |
| **β-arrestin recruitment** (split-luciferase / NanoBiT) | luminescence | **yes** — plasmid only | orthogonal to G protein; catches biased agonism |
| **Gi BRET** (TRUPATH-style biosensor) | BRET ratio | **yes** — plasmid only | most direct G-protein readout |
| `[35S]`GTPγS binding | radioactivity | only if licensed | membrane prep, no live cells |
| Radioligand competition | radioactivity | only if licensed | gives K_i directly |

No antibodies and no animals in the top three. HEK293T is already the host, so DOR +
reporter co-transfection is the same workflow they just performed.

### 3.4 Controls that make a positive result defensible

- **SNC80** or **DPDPE** — δ-selective agonist: positive control and potency benchmark
- **naltrindole** — δ-selective antagonist. Must abolish the response. **Without this, a
  cAMP drop is not attributable to DOR.**
- **untransfected HEK293T** — receptor dependence (endogenous opioid receptor levels are negligible)
- **pertussis toxin** — abolishes Gi coupling; confirms mechanism
- **test MOR in parallel** — our prediction is activity at *both*. Assaying δ alone cannot falsify it.

### 3.5 If the peptide is active but weak

This is the likely partial-failure mode: `EVVG` replaces `M` as a DNA-encodability
compromise. Options, cheapest first:

1. **Raise concentration / extend incubation** — a weak agonist is not an inactive one
2. **Test the amidated form `STD-ENGA` (`YGGFEVV`-NH₂)** — already on the order sheet;
   C-terminal amidation frequently raises opioid potency
3. **Test the extended digest species** `YGGFEVVGRGL` (cassette 4) and `YGGFEVVGRF`
   (cassette 7) — these are real products, not artefacts, and may differ pharmacologically
4. **Switch peptide to V4 (`YGGFDIIG`)** — Cycle 2's top-ranked variant, best δ-pose
   convergence in the panel (0.81 Å). A single-cassette DNA change, fully encodable.
   Note its Δ_sel is also not significant (p = 0.15); it is a *potency* candidate, not a
   selectivity fix.

---

## 4. Dry-lab Plan B — available now, no waiting

Ordered by value:

1. **Run MM-GBSA on `YGGFEVVG` at δ and μ** on the validated Cycle 3b protocol, so the
   result is directly comparable to the four calibration peptides. Cost: 2 receptors × 5
   replicates, ~12 min each at 8 cores / 48 GB, no GPU.
   **Blocker: `gate.py` does not exist** — documented in `MMGBSA_STATUS.md` "Next actions"
   item 3. `rescore.sh` was written to feed it and `collect_dg.py` emits its input format,
   but the consumer was never written, so nothing can consume `results_stage1.csv`.
   Writing it is a prerequisite and is a dry-lab job.
2. **Pocket-residency time for `YGGFEVVG`.** Δ residency tracks experimental ΔΔG across the
   four calibration peptides at **r = 0.915 (p = 0.085, n = 4)** — suggestive but
   under-powered. It is the metric least sensitive to MM-GBSA's known weaknesses, and it
   uses the replicates the energy pipeline has to discard. Free once step 1's trajectories exist.
3. **Expand the calibration set.** n = 4 is *why* step 2 is not significant. Adding DPDPE,
   SNC80, DAMGO and β-endorphin — all with published δ/μ K_i — would establish whether
   residency is a usable predictor at all. This is the difference between a correlation and
   a calibrated instrument, and it is the honest prerequisite to quoting step 2.
4. **Pre-register the DOR predictions before the assay runs**, per project convention:
   `YGGFEVVG` is active at DOR; potency within ~10× of Met-enkephalin; **no** significant
   δ-over-μ selectivity; naltrindole abolishes the response.

---

## 5. What this plan does not fix

- **No in-silico route here produces an EC50.** ipTM and MM-GBSA both predict *interaction*,
  not potency. If the wet lab needs a potency number, it has to come from the assay.
- MM-GBSA effective energies carry **no entropy term**; absolute values are not affinities
  and only differences within one consistent protocol are interpretable.
- The residency calibration is **n = 4, p = 0.085**. It is not a validated predictor and
  must not be quoted as one until step 4.3 is done.
- Nothing here addresses whether the peptide is **stable in assay medium** over the
  incubation — serum peptidases degrade enkephalins rapidly, and that is untested.

---

## Sources in this repository

| Claim | File |
|---|---|
| Co-folded δ complexes, confidences | `04_structures/*_DORbound_AFformat_confidence.json` |
| 5-sample ipTM, Δ_sel, convergence | `06_engineering_cycles/cycle2_delta_selectivity/data/cycle2_results.csv` |
| Cycle 1 "1.96×" retraction | `cycle2_delta_selectivity/CYCLE2_RESULTS.md` |
| MM-GBSA validation, 4 defects, missing `gate.py` | `cycle3b_physics_rescoring/MMGBSA_STATUS.md` |
| Benchmark ΔΔG and residency | `cycle3b_physics_rescoring/mmgbsa_selectivity.csv`, `08_checkable_audit/tables/residency_vs_selectivity.csv` |
| Synthetic control peptides already specced | `07_invitro_penk/tables/control_peptides_order.csv` |
