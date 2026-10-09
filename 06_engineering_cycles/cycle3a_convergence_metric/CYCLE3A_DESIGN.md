# Cycle 3a: Is pose convergence a better selectivity proxy than ipTM?

**Status:** pre-registered · written **before** any Cycle 3a analysis was run
**Type:** metric-validation cycle, no new chemistry, no new sequences
**Learn input:** Cycle 2 finding #4 (unplanned observation)

---

## Why this is its own cycle

Cycle 2's strongest signal was not one it was designed to find. Across the 7 peptides
tested, every δ-preferring variant had tight δ-pose convergence and every μ-preferring
variant had loose δ-pose convergence:

| Peptide | Δ_sel | δ-pose convergence |
|---|---|---|
| V4 `YGGFDIIG` | +0.0152 | 0.81 Å |
| V5 `YAFEVVG` | +0.0121 | 0.71 Å |
| C1 `YGGFEVVG` | +0.0114 | 1.14 Å |
| native `YGGFM` | +0.0050 | 1.42 Å |
| V3 `YGGFDVVG` | −0.0007 | 0.90 Å |
| V2 `YGGFELLG` | −0.0119 | 4.16 Å |
| V1 `YGGFEIIG` | −0.0162 | 5.89 Å |

The ipTM differences driving Δ_sel are all within noise (SEMs 0.005–0.013 against
effects of the same size). The convergence differences are **4–8×** and far outside it.
If convergence tracks selectivity, it is the better-powered readout and every subsequent
cycle should be judged on it.

**This finding was discovered, not predicted.** Testing it on the same data that
generated it would be circular. This cycle exists to state the hypothesis in advance and
test it on held-out evidence.

---

## HYPOTHESIS

**H3a:** Peptide pose convergence in the δ pocket is a monotonic predictor of Δ_sel
across the peptide panel, and is better-powered than ipTM.

**H3a-null:** The apparent relationship is driven by V1/V2 alone (the two bulky
aliphatic variants) and does not hold when they are excluded, or does not replicate on
independent samples.

---

## METHOD

No new sequences. Two independent tests:

**Test 1: replication on held-out samples.** All Cycle 1/2 numbers came from 5 diffusion
samples per complex. Generate **15 additional samples** per complex (distinct seeds) for
all 7 peptides × 2 receptors. Recompute Δ_sel and convergence on the new samples only.
The Cycle 2 relationship was fit on the first 5; this tests it on 15 it has never seen.

**Test 2: leave-the-outliers-out.** Refit the convergence↔Δ_sel relationship excluding
V1 and V2. If the correlation collapses, the signal was two outliers.

**Statistics.** Spearman ρ (rank-based, robust to small n and non-linearity) between
δ-convergence and Δ_sel, with a permutation p-value (10 000 shuffles) because n = 7 is
too small for a parametric correlation test. Power comparison: ratio of between-peptide
spread to within-peptide noise, computed the same way for each metric.

---

## PREDICTIONS (committed before running)

| # | Prediction | Falsified if |
|---|---|---|
| P1 | Spearman ρ(δ-convergence, Δ_sel) < 0 on the 15 held-out samples, permutation p < 0.05 | ρ ≥ 0 or p ≥ 0.05 |
| P2 | The relationship survives dropping V1 and V2 (ρ stays negative) | ρ flips sign without them |
| P3 | Convergence has a higher spread-to-noise ratio than ipTM | ipTM ratio ≥ convergence ratio |
| P4 | V4 and V5 remain the two best-converged δ complexes at n = 20 | either drops below C1-BASE |
| P5 | Δ_sel rankings shift at n = 20: the n = 5 ranking is not stable | top-2 unchanged *and* all SEMs shrink < 20 % |

P5 is deliberately a prediction that our **own Cycle 2 ranking is unreliable**. If it is
falsified: if the ranking is stable, that strengthens Cycle 2 rather than this cycle.

---

## SUCCESS CRITERION

H3a is accepted only if **P1 and P2 both hold**. Under that outcome, Cycle 3b judges the
combined variant primarily on convergence and reports ipTM as secondary.

If H3a is rejected, convergence is recorded as a Cycle 2 coincidence, Cycle 3b proceeds on
ipTM with increased n, and this document stands as the record of a hypothesis that failed.

---

## STANDING LIMITS (carried from the cycles README)

- ipTM and pose convergence are **structural-confidence measures, not binding affinity**.
  A well-converged pose means the model is self-consistent, which is not the same as a
  tight-binding one, and this cycle does not change that.
- Neither metric can be validated against ground truth here. Radioligand competition
  binding at OPRD1/OPRM1 remains the only real test.
- Boltz-2 cannot represent D-amino acids or C-terminal amidation, both central to real
  deltorphin pharmacology. All conclusions are conditional on the all-L, free-acid
  approximation.
- Every metric is reported as mean ± SD over all diffusion samples. Single-model numbers
  are not reported (see the Cycle 1 correction).
