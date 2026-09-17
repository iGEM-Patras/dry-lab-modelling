# δ/μ selectivity of `YGGFEVVG` — what six cycles actually established

**Compiled 2026-09-17.** Every number below is traceable to a committed data file.
Written so a reviewer can check each claim against the cycle that produced it.

## The one-line answer

`YGGFEVVG` is **nominally δ-preferring and statistically indistinguishable from
no-preference, and indistinguishable from native met-enkephalin**:
**+1.23 ± 1.76 kcal/mol** (≈7× δ, interval spans zero), from a method that passed a
pre-registered calibration gate at n=13 (r = 0.805, p = 0.001).

No engineered variant in the DNA-encodable space beat that. Whether the peptide is
*usefully* δ-selective is still open; whether the **methods** can detect selectivity is
now settled — three of four can, and we know which.

## Evidence table

| Cycle | Method | Gate | Outcome |
|---|---|---|---|
| 2 | Boltz-2 ipTM Δ_sel, 5 designed variants | pre-registered | **falsified** — address-hydrophobicity hypothesis rejected; 4 of 5 predictions inconclusive |
| 3b | MM-GBSA rescoring, membrane MD | pre-registered | **failed its own gate** — tightest-replicate control carried the largest error (systematic, not sampling) |
| 6 | Boltz-2 affinity head, n=4 panel | B1/B2/B3 | **failed all three** — most δ-selective reference predicted with the WRONG SIGN; target value withheld |
| 7 | Boltz-2 affinity head, n=13 panel | B1 \|r\|>0.553 | **PASSED** r = 0.805, p = 0.0009, signs 12/13 → the calibrated estimate |
| 7b | ipTM difference, same panel | B2 \|r\|>0.553 | **failed** r = 0.522, p = 0.067 — a structural proxy is not a selectivity metric by default |
| 9 | Pose convergence from MD replicates | ordinal, n=4 | **PASSED** ρ = 1.000, r = 0.980, p = 0.020 — ranks all four controls correctly |
| 8 | Alchemical TI, 27 λ windows | D1–D5 | **queued** — controls integration-ready, blocked on a downed GPU node |

## Why Cycle 7's number is trustworthy, and exactly how far

**Passed:** predicted vs published ΔΔG across 13 opioid ligands, single-source ChEMBL
medians, r = 0.805 (critical 0.553 at n=13), signs correct on 12 of 13. The one miss is
clocinnamox at ΔΔG +0.06 — effectively no preference, so its sign flips on noise.

**The same method failed all gates at n=4.** The difference was sample size, not tuning:
a 4-point panel requires |r| > 0.950, so a method with a true r of 0.8 fails on power
alone. That is why expansion was the right response to the first negative rather than
acceptance of it.

**Three limits that must travel with the number:**

1. **Magnitude is not calibrated.** Regression slope 0.309 → a 3.2× compression. Direction
   and ranking are calibrated; the absolute value is a back-projection with ±1.76.
2. **No control in the strongly δ-selective regime.** The panel's maximum is +2.13; the two
   most δ-selective peptides (deltorphin I +5.70, II +5.39) failed the ≥3-measurement
   inclusion criterion. **Those are exactly the two the method mis-signed at n=4** — so the
   calibration is untested precisely where a bold selectivity claim would live.
3. **Binding, not efficacy.** Ki-derived, and the panel mixes agonists with antagonists.
   It calibrates binding preference; it cannot calibrate agonist potency.

**Limit 2 is now partly closed — by Cycle 9, not by Cycle 7.** The convergence metric ranks
both deltorphins correctly (1.699 and 1.466, top two of four), so the strongly δ-selective
end is no longer a complete blind spot. But that is a *different measurement* on a
different axis and the two must not be pooled.

## The design space is closed, not merely sampled

- **151 message-intact single substitutions** screened by QSAR (fingerprint RF, scaffold-grouped
  CV, applicability domain checked). **None beat the base beyond its error bar.**
- **PAM C-terminal amidation** shifts ΔΔG in the δ-preferring direction with complete
  consistency and negligible magnitude — **43× below the method's resolution.**
- **Position 8 is not a design position.** All 19 substitutions destroy the C-terminal Gly
  that is the PAM recognition signal.
- Cycle 2's hypothesis — that address-region hydrophobicity buys δ-selectivity — was
  **falsified** on its own pre-registered terms.

It remains possible that **no DNA-encodable octapeptide is strongly δ-selective.** The
methods above improve the ability to find one and to prove it; they do not guarantee one
exists. That is a result, not a gap.

## What a reviewer should ask, and the honest answer

**"Is it δ-selective?"** Nominally δ-preferring, not significantly so, and not
distinguishable from the natural peptide. Two independent methods agree on that.

**"Could you be wrong?"** On direction, the risk is the uncalibrated strongly-selective
regime (limit 2). On magnitude, the compression slope means the true value could be
materially larger or smaller. On efficacy, we have not measured it at all.

**"What would settle it?"** A free-energy calculation with no compression slope, plus
wet-lab δ/μ functional data. The former is designed, pre-registered and queued (Cycle 8);
the latter is the transfection now in progress.

## Standing methodological results (transferable beyond this project)

1. **Size the panel from statistics, not convenience** — n=4 needs |r| > 0.950.
2. **Keep the reference axis single-source** — the project's own stored value and the
   database median disagreed by 1.84 kcal/mol *for the same molecule*.
3. **Include a non-correlation gate** — a deliberately non-converged dataset (15 kcal/mol
   replicate spread) still passed a sign-and-correlation gate at p = 0.03.
4. **Withhold the target when calibration fails** — Cycle 6's withheld value would have
   agreed with the earlier null and been mistaken for confirmation.
5. **Measure noise floors, don't assume them** — Cycle 9's measured replicate spread was
   ~2× the value that had been assumed, which deflated an earlier signal-to-noise claim.

Packaged as the `calibrated-prediction-gate` skill.

## Files

| Claim | File |
|---|---|
| Calibration, per-compound | `cycle7_calibration/data/cycle7_scored.csv` |
| Gate outcomes and slope | `cycle7_calibration/data/cycle7_verdict.json` |
| Headline estimate | `cycle7_calibration/data/cycle7_target.csv` |
| Convergence calibration | `cycle9_convergence_metric/data/convmetric_md_calibration.csv` |
| QSAR screen | `cycle7_calibration/data/qsar_screen_message_intact.csv` |
| Cycle 2 falsification | `cycle2_delta_selectivity/data/cycle2_results.csv` |
| TI protocol and gate | `cycle8_fep/CYCLE8_DESIGN.md` |
