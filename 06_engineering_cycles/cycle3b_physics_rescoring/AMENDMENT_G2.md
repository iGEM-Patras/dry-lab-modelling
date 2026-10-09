# Pre-registration amendment: Cycle 3b gate criterion G2

**Filed 2026-07-31, before any Stage-1 `dG_bind` value existed.**

That timing is the whole justification. Changing a pre-registered criterion
after seeing the data it judges is how a failed hypothesis gets quietly
reframed as a passed one: the exact failure the cycle-3b pre-registration was
written to prevent. This amendment is filed while Stage 1 is still running its
first pilot build and no MM-GBSA number has been computed. If it had been
proposed after Stage 1 returned, the correct response would have been to
report the pre-registered result and note the defect for the next cycle.

## What is changing

| | pre-registered | amended |
|---|---|---|
| **G1** (sign + rank) | unchanged | unchanged |
| **G2** | replicate **SD** of ΔΔG_sel ≤ 1.5 kcal/mol on every control | **G2′**: replicate **SEM** of ΔΔG_sel ≤ 1.5 kcal/mol on every control |
| **G3** (calibration slope) | unchanged | unchanged |

Everything else, the controls, the experimental anchors, the sign convention,
the consequence of failure, is untouched. **A failed gate still terminates
cycle 3b and reports a negative methodological result.**

## Why G2 as written cannot be passed

G2 was written to mean "the method is precise enough to resolve the controls".
It does not measure that. Four findings, all from Monte-Carlo over the
pre-registered anchors (ΔΔG_sel = +5.39, +5.70, −2.99, 0.00 kcal/mol):

1. **It demands precision the method is not claimed to have.**
   ΔΔG_sel is a difference of two independent ΔG_bind values, so
   SD(ΔΔG) = σ_rep·√2. Requiring SD ≤ 1.5 demands **σ_rep ≤ 1.06 kcal/mol**:
   below the **1–2 kcal/mol** MM-GBSA uncertainty that `CYCLE3B_DESIGN.md`
   itself states two sections earlier. The design document contradicts itself.

2. **A 3-sample SD is a 2-df estimate, and the criterion is applied four times.**
   With the true SD exactly at the limit, one control passes with p ≈ 0.68 and
   all four with 0.68⁴ = **0.21**.

3. **A perfect method fails it.** Simulating a method with calibration slope
   exactly 1.0: all three gates pass **21%** of the time at σ_rep = 1.0, **3%**
   at σ_rep = 1.5, **0.5%** at σ_rep = 2.0.

4. **The decisive one: power falls as sampling rises.** At σ_rep = 1.5,
   P(pass) for a perfect method goes **0.076 → 0.022 → 0.008 → 0.006 → 0.002 →
   0.001 → 0.000** for n = 2, 3, 4, 5, 6, 8, 10 replicates. More sampling makes
   a correct method fail more often, because a larger sample estimates the true
   SD more accurately and the true SD exceeds the threshold. This is the
   signature of an estimator defect rather than a property of the method under
   test, and it means **no compute budget can rescue the criterion.**

## Why G2′ is the right repair, and why it is not a weakening

The SEM is the precision of the quantity the gate actually reports: the mean
ΔΔG_sel per control. Thresholding it asks "is our estimate of this control's
selectivity tight enough to act on?", which is the question G2 was reaching for.

| | G2 as written | G2′ (SEM) |
|---|---|---|
| power at σ_rep = 1.5, n = 3 | 0.030 | 0.353 |
| power at σ_rep = 1.5, n = 5 | 0.006 | 0.846 |
| power at σ_rep = 1.5, n = 10 | 0.000 | 1.000 |
| **false pass, null method** | **~0.02** | **~0.02** |
| σ_rep tolerated at 50% power | 0.81 | 1.36 (n=3), 1.85 (n=5) |

The false-pass rate against a method with no signal is **unchanged at ~2%**.
G2′ is not more permissive toward a bad method; it stops rejecting good ones.
And it responds to sampling in the correct direction, which restores the
option of buying discrimination with replicates.

## Consequence for Stage 1

`CYCLE3B_DESIGN.md` commits Stage 1 to **3 replicates**. At n = 3, G2′ has
**35% power** at σ_rep = 1.5, better than the 3% it replaces, but still low.
Two honest readings, both recorded here in advance:

- If the gate **passes** at n = 3, that is a strong result: it passed despite
  low power.
- If the gate **fails** at n = 3, the failure is **not** decisive evidence
  against the method, because at this replicate count the gate would also fail
  a perfect method about two-thirds of the time. The pre-registered
  consequence still applies: cycle 3b terminates, but the report must state
  the power, not present the failure as a clean refutation.

**Recommended, not yet authorised:** extend Stage 1 to **n = 5** (40 runs
instead of 24, ~5.8 GPU-days at the measured 71.5 ns/day, still under the
pre-registered 6.7 GPU-day Stage-1 budget), which lifts power to 85%. This is a
separate decision and is not taken as part of this amendment.

## Evidence

- `gate_calibration.png` (power and false-pass curves, all four panels)
- `gate_calibration.csv` (the underlying numbers)
- `scripts/gate.py` (the evaluator implementing G1/G2′/G3, with a five-case
  test matrix (clean pass, null, sign-flipped, too-noisy, dropped replicate)
  verified before any real data

## What was NOT changed, and why that matters

The temptation with a defective gate is to relax the threshold: 1.5 → 2.5
kcal/mol would also have "fixed" the pass rate. That would have been a genuine
weakening: it raises the false-pass rate against a null method. The defect here
is in the **statistic**, not the **threshold**, so the statistic is what
changed and the threshold value stays at 1.5.
