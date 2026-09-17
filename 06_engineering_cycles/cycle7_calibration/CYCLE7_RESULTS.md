# Cycle 7 — expanded calibration, ligand QSAR, and the first calibrated δ/μ estimate

**Status: CLOSED.** Gates pre-registered in `data/cycle7_predictions.csv` before submission.

## Verdict

| Gate | Required | Observed | |
|---|---|---|---|
| **B1** affinity head vs published ΔΔG | \|r\| > 0.553 (n=13) | **r = +0.805, p = 0.001** | **PASS** |
| **B2** ipTM difference vs published ΔΔG | \|r\| > 0.553 | r = +0.522, p = 0.067 | FAIL |
| **B3** report engPENK on a passing metric | — | reported on B1 | — |

Sign agreement 12/13. The single miss is clocinnamox, published ΔΔG **+0.06** — no
meaningful preference, so its sign flips on noise.

**The same method failed all three gates at n=4** (Cycle 6: r = 0.72, p = 0.28, deltorphin II
called μ-preferring). The difference is sample size. Expanding the calibration set rather
than accepting the first negative is what produced a usable method.

## Result — `YGGFEVVG`

**ΔΔG(δ/μ) = +1.23 ± 1.76 kcal/mol → ≈7× δ-preferring, NOT significant.**

The interval spans no-preference. Honest reading: *nominally δ-preferring, statistically
indistinguishable from no preference, and indistinguishable from native Met-enkephalin*
(published +0.81 kcal/mol). This is the project's first calibrated selectivity estimate —
every prior number came from an uncalibrated or failed method.

It is **consistent with the Cycle 2 null**, but now for a different and better reason: not
"our metric could not resolve it" but "a metric calibrated against 13 ligands of known
pharmacology puts it near zero with a stated uncertainty".

## Three limits on what may be claimed

1. **Slope 0.31 — magnitudes compressed 3.2×.** Predicted range 2.66 kcal/mol against a
   published range of 6.95. Direction and ranking are calibrated; absolute ΔΔG is not. The
   reported value is slope-corrected, which is why the uncertainty is ±1.76 and not smaller.
2. **No control above +2.13 kcal/mol.** Deltorphins I (+5.70) and II (+5.39) are absent
   because they failed the **pre-stated** inclusion criterion (≥3 published Ki at *both*
   receptors in ChEMBL) — not a post-hoc filter. But they are exactly the two compounds the
   method called with the wrong sign at n=4. **The calibration holds on [−4.82, +2.13] and
   is untested in the strongly δ-selective regime**, which is where a "δ-selective" claim
   would live. Do not extrapolate.
3. **Binding, not efficacy.** Every ΔΔG here — computed and reference — is a binding
   quantity. A δ-preferring binder can still be a poor δ agonist.

**Recorded dropout:** buprenorphine returned no co-fold (28 records of 30 expected), cause
unknown. Gates were scored on the 13 references that returned.

---

## Sub-result A — ligand QSAR screen of the DNA-encodable space

![QSAR screen]({{artifact:art_d8d63c13-6644-43bf-9462-467d4a47f42c}})

Random forest on Morgan fingerprints, trained on **2873 ChEMBL ligands with Ki at both**
receptors. Honest validation by **scaffold-grouped** 5-fold CV: **r = 0.768, RMSE 1.07
kcal/mol** (random-split r = 0.839; baseline 1.68). Conformal 90 % half-width **1.71
kcal/mol** from out-of-fold residuals.

Screened **306 candidates** — every single substitution of `YGGFEVVG` at all 8 positions,
the Cycle 2 panel, the cassette products, and every PAM-accessible amide. All 306 inside the
applicability domain (max Tanimoto to training set 0.66 for the parent).

**Result: of 151 message-intact candidates, ZERO exceed the base beyond the conformal
interval.** Best is `YGGFRVV`-NH₂ at +0.50 kcal/mol over base — inside the noise.

**A pre-committed sanity check caught a real artifact.** The unrestricted top 12 were *all*
substitutions of **Tyr¹**, the essential opioid pharmacophore. They score well because the
model predicts a **ratio**: a peptide that binds neither receptor has an arbitrary ratio,
not a good one. Ranking blind would have recommended destroying the pharmacophore. All
reporting is therefore restricted to candidates preserving `YGGF`.

**PAM amidation: consistent in direction, negligible in size.** 117 of 138 substrate/product
pairs shift δ-ward (Wilcoxon p = 7×10⁻¹⁷), but the mean shift is **+0.040 kcal/mol** — **43×
below** the method's own resolution — and the paired t-test is p = 0.14. Amidation is not a
selectivity lever. It may still matter for potency, which this model does not address.

**Design constraint found while enumerating:** all 19 substitutions at position 8 destroy
the C-terminal Gly, which is the **PAM recognition signal**. Position 8 is not a free design
position, and any mutation there forfeits the amidation route entirely.

## Sub-result B — pose convergence, already in the Cycle 2 data and never analysed

![Convergence re-analysis]({{artifact:art_1d7d190d-64d8-4b41-b44b-a6e79c1e5b1b}})

Cycle 2 recorded `pose_conv_DOR_A` and `pose_conv_MOR_A` and then judged selectivity on
ipTM. Their **ratio** separates the panel **8.9-fold**, while ipTM Δ_sel spans 0.031 against
a mean SEM of 0.008. Signal-to-noise: **45× versus 4×** — same co-folds, same 5 samples,
zero extra compute. That is why four of five Cycle 2 predictions came back inconclusive:
the discriminating quantity was measured and unused.

It is not redundant with ipTM (r = 0.708, p = 0.075). Ranking by it: **V5 `YAFEVVG` 9.4×**,
V4 `YGGFDIIG` 4.5×, base `YGGFEVVG` 3.6×, native `YGGFM` 1.3×, and the μ-ward V1/V2 invert
to 0.4× / 0.6× — agreeing with ipTM where Cycle 2 was confident and discriminating where it
was not.

**Caveat:** the 0.20 Å noise floor used for the signal-to-noise figure is an assumption from
the tightest replicate spread, not a measured replicate SD of the ratio itself. Re-running
the panel with per-sample RMSDs would give a real error bar (~2 h GPU). **Note also that
B2 failed** — the ipTM *difference* does not track selectivity — so a structural metric
passing here would need its own calibration; convergence ratio is not yet calibrated against
experiment at all.

## Files

- `data/cycle7_affinity_raw.csv` — raw Boltz-2 output, 28 records
- `data/cycle7_scored.csv` — per-compound predicted vs published ΔΔG
- `data/cycle7_verdict.json` — gates, slope, target estimate, recorded dropout
- `data/cycle7_panel.csv`, `data/cycle7_candidate_pool.csv` — the 14 selected and the 46 screened
- `data/qsar_screen_message_intact.csv` — 151 ranked candidates with conformal intervals
- `data/qsar_screen_raw.csv` — all 306, Tyr¹ artifacts included so the failure mode is auditable
- `data/qsar_amidation_paired.csv` — the 138 substrate/product pairs
- `data/cycle2_convergence_reanalysis.csv` — convergence ratios for the Cycle 2 panel
