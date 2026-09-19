# Engineering Cycles — δ-selective enkephalin payload

This directory documents the iterative **Design → Build → Test → Learn (DBTL)** engineering
of the analgesic peptide payload expressed from the engineered PENK therapy plasmid.

## Why iterate on the peptide at all?

The therapy delivers a proenkephalin (PENK) cassette so that transduced cells secrete
enkephalin locally, plus an siRNA that silences neprilysin (MME) so the secreted peptide
is not immediately degraded. Enkephalin acts at two opioid receptors:

| Receptor | Gene | Consequence of agonism |
|---|---|---|
| **δ (DOR)** | `OPRD1` | analgesia, anxiolytic; **much lower respiratory-depression and dependence liability** |
| **μ (MOR)** | `OPRM1` | analgesia, but also respiratory depression, constipation, tolerance, dependence |

Native Met-enkephalin (`YGGFM`) is only weakly δ-preferring. **Biasing the payload toward
δ is therefore a safety-driven design goal**, not a cosmetic one: it retains analgesia while
reducing the μ-mediated adverse-effect profile that makes conventional opioids dangerous.

## Cycle index

| Cycle | Design concept | Payload | Status | Result |
|---|---|---|---|---|
| **1** | Graft the **deltorphin II address** onto the enkephalin message | `YGGFEVVG` | ✅ complete | Directionally δ-ward; **quantitative claim withdrawn** (see correction) |
| **2** | Enhance address hydrophobicity / anionic residue (literature-guided) | 5 variants | ✅ complete | **Primary hypothesis falsified** — 4 of 5 predictions wrong; V4/V5 retained |
| **3a** | Validate pose convergence as a selectivity metric | *no new sequences* | ✅ complete | **H3a rejected** — does not replicate; metric retired |
| **3b** | ~~Combine Cycle 2's two independent wins~~ → **change the observable**: explicit-solvent MD + MM-GBSA ΔΔG in kcal/mol | controls + 2 survivors, acid & amide | 📋 pre-registered, gated | Original premise **withdrawn** (V5's win within noise at n=20). Stage 1 must calibrate on experimental controls before the panel is run |
| **4** | **Can the cassette be manufactured?** Iteratively reverse-engineer the vendor's synthesis-complexity rules from its rejection reports | 4 constructs × 3 rounds (v4→v5→v6) | ✅ complete | v4 **denied 23.8** (inverted-repeat flanks, inherited from wet-lab files); v5 fixed 3 of 4; **v6 accepted — all four constructs ordered** |
| **5** | What should the first transfection actually produce? | *no new sequences* | 📋 pre-registered | Five falsifiable predictions committed before the bench runs; awaiting wet-lab data |
| **7** | Does the co-folding **affinity head** predict δ/μ selectivity, tested against published drugs? | *no new sequences* | ✅ **gate PASSED** | n=13, r = 0.805, p = 0.0009, signs correct 12/13. First calibrated number: `YGGFEVVG` **+1.23 ± 1.76 kcal/mol** (~7× δ), not separable from native |
| **8** | Rigorous **free-energy (TI)** ΔΔG for δ vs μ | controls + target | 🔄 **running** | 13 CPU workers; graft shortcut **rejected by measurement** (`GRAFT_ROUTE_REJECTED.md`) |
| **9** | Re-test **pose convergence**, this time calibrated against experiment | *no new sequences* | ✅ **gate PASSED** | ρ = 1.000 — ranks 4 reference peptides in exact agreement with published selectivity. Rehabilitates the metric Cycle 3a retired |

- [`cycle1_deltorphin_chimera/CYCLE1.md`](cycle1_deltorphin_chimera/CYCLE1.md) — retrospective writeup **+ correction notice**
- [`cycle2_delta_selectivity/CYCLE2_DESIGN.md`](cycle2_delta_selectivity/CYCLE2_DESIGN.md) — pre-registration (committed before the runs)
- [`cycle2_delta_selectivity/CYCLE2_RESULTS.md`](cycle2_delta_selectivity/CYCLE2_RESULTS.md) — results, prediction scoring, Cycle 1 correction
- [`cycle3a_convergence_metric/CYCLE3A_DESIGN.md`](cycle3a_convergence_metric/CYCLE3A_DESIGN.md) — pre-registration
- [`cycle3a_convergence_metric/CYCLE3A_RESULTS.md`](cycle3a_convergence_metric/CYCLE3A_RESULTS.md) — held-out replication, scorecard, recommendation
- [`cycle4_synthesizability/CYCLE4.md`](cycle4_synthesizability/CYCLE4.md) — the vendor-rules cycle, with its pre-registration scored
- [`cycle5_expression_processing/CYCLE5_DESIGN.md`](cycle5_expression_processing/CYCLE5_DESIGN.md) — pre-registration for the first transfection
- [`cycle7_calibration/CYCLE7_RESULTS.md`](cycle7_calibration/CYCLE7_RESULTS.md) — the calibrated estimate and its three stated limits
- [`cycle8_fep/CYCLE8_DESIGN.md`](cycle8_fep/CYCLE8_DESIGN.md) — protocol, measured throughput budget, gate dry-run
- [`cycle8_fep/GRAFT_ROUTE_REJECTED.md`](cycle8_fep/GRAFT_ROUTE_REJECTED.md) — a negative result, including two invalid attempts of our own
- [`cycle9_convergence_metric/`](cycle9_convergence_metric/) — the recalibrated metric that passed

### Reading this index

**There is no `cycle6/` directory.** Cycle 6 was a calibration attempt at n = 4 that failed
all its gates; its data is kept in [`cycle7_calibration/data/`](cycle7_calibration/data/),
since Cycle 7 is the same experiment repeated at an adequate sample size.

**Cycle 3a rejected the pose-convergence metric and Cycle 9 accepted it.** Not a contradiction:
3a evaluated the metric without calibrating it against experimental values, 9 evaluated it
against four peptides with published selectivity. The difference is whether the metric was
anchored to experimental values before being relied on.

**Cycles are counted by their Learn→Design edge**, not by construct count: a parallel
multi-arm panel is one cycle, and only a genuinely sequential dependency splits into two.

## What counts as a cycle here

A cycle is defined by its **Learn → Design edge**, not by the number of constructs it
contains. Variants that were all designed from the *same* Learn output, tested in
parallel, and interpreted against each other are **one cycle with a multi-arm panel** —
Cycle 2's five variants are controls for one another (V3 is the Asp-without-Ile control
for V4; V2 isolates β-branching from bulk in V1) and are meaningless in isolation.

Splitting a parallel panel into one "cycle" per variant would produce loops with
identical Design inputs and no Learn edges between them. That inflates cycle count while
reducing cycle depth. Conversely, Cycle 3 **is** split into 3a and 3b because 3a's
result determines what metric 3b is judged on — a genuine sequential dependency.

By the same rule, Cycle 4's three rounds (v4 → v5 → v6) are **one cycle**, not three. Each
round's design is determined by the previous round's rejection report, so they form a
sequential chain — but they share one hypothesis ("this cassette is manufacturable") and
one oracle. They are documented as rounds *within* Cycle 4 rather than as Cycles 4/5/6.

Cycle 4 is also the first **wet–dry** loop here: its Test step is an external
manufacturer's feasibility engine, not a simulation. The Learn edge crosses the
dry/wet boundary, which is what the project needs to demonstrate.

## Track record

Predictions are committed and pushed **before** the corresponding runs are launched, so
the falsification record is auditable in the git history.

| Cycle | Predictions made | Confirmed | Falsified | Pre-registration commit |
|---|---|---|---|---|
| 2 | 5 | 1 | **4** | `f2d6ade` (before job `ac2c837e`) |
| 3a | 5 | 3 | **2** (both decisive) | `ec7123d` (before job `1391bb2a`) |
| 4 (v4) | 1 | 0 | **1** | — (not pre-registered; see below) |
| 4 (v5) | 4 | 3 | **1** | — (not pre-registered; see below) |
| 4 (v6) | 5 | *pending* | *pending* | this commit (before vendor submission) |

**Cumulative: 15 predictions scored, 7 confirmed, 8 falsified** (+5 pending).

Cycle 4's first two rounds were **not** pre-registered — the v4 and v5 predictions were
made informally in conversation and only written down after the vendor had answered. They
are recorded in the scorecard for honesty, but they do not carry the same evidential
weight as a committed prediction and are marked as such. v6 is the first round of this
cycle to follow the project's own rule. This is itself a finding: the cheapest, fastest
oracle in the project was the one where pre-registration discipline slipped first. The two Cycle 3a falsifications
rejected the cycle's own hypothesis; the three confirmations include P5, which predicted
that our *previous* cycle's ranking was unreliable — and it was.

A high falsification rate is the intended outcome of honest pre-registration, not a
failure of the project.

## Shared method

All peptide–receptor complexes are predicted with **Boltz-2** co-folding against the
full-length human receptor (UniProt canonical sequence), under identical settings:

```
boltz predict <complex>.yaml --use_msa_server \
  --subsample_msa --num_subsampled_msa 1024 \
  --recycling_steps 3 --diffusion_samples 5 --sampling_steps 200
```

Receptor chain uses a full MSA (1024 sequences); the peptide chain uses `msa: empty`
(a 5–8-mer has no meaningful alignment). **All cycles use identical settings**, so
cross-variant comparisons are internally controlled.

### Selectivity metric

$$\Delta_{sel} = \text{ipTM}(\text{DOR complex}) - \text{ipTM}(\text{MOR complex})$$

ipTM is Boltz's predicted interface TM-score — a **confidence** measure for the
peptide–receptor interface. A larger $\Delta_{sel}$ means the model is more confident about
the δ interface than the μ interface for that same peptide.

### ⚠ Interpretation limits (read before quoting any number here)

- **ipTM is not binding affinity.** It is a structural-confidence score. It ranks and
  triages designs; it does **not** predict $K_i$, $IC_{50}$, or fold-selectivity.
- Differences of ~0.01–0.02 ipTM are near the noise floor. We therefore report
  **mean ± SD across the 5 diffusion samples** and treat only separated distributions
  as meaningful.
- Boltz sees the **unamidated, linear L-amino-acid** peptide. It cannot represent
  D-amino acids or C-terminal amidation, both of which matter for real deltorphin
  pharmacology (see Cycle 2 design notes).
- **Wet-lab radioligand competition binding at DOR vs MOR is the only real test.**
  These predictions exist to choose which 2–3 variants are worth synthesising.

## Constraint that shapes every design

The payload is **expressed from a plasmid**, so it must be encodable in DNA:
**20 standard L-amino acids only**. This rules out the classic high-selectivity
opioid-peptide tricks — D-amino acids (D-Ala²), penicillamine cyclisation (DPDPE),
N-methylation — which is why the design space here is the *address domain sequence*
rather than backbone chemistry.

One partial exception is exploited deliberately: a **C-terminal Gly is the recognition
signal for peptidylglycine α-amidating monooxygenase (PAM)** in mammalian secretory
granules, so a `...VVG` payload can be post-translationally converted to the
`...VV-NH₂` amide *in vivo* — recovering the amidation that natural deltorphins require.
The terminal Gly in every design is therefore load-bearing and must be retained.
