# Cycle 14 — final verdict: the control fails its replicate-agreement gate

**Scored 8 Oct 2026 against gates committed in `data/cycle14_prereg.json` before any
window ran. 684 ns across 228 windows, all four legs complete.**

## The result

| | ΔΔG (δ over μ) |
|---|---|
| replicate 1 | **+0.72 ± 3.13 kcal/mol** |
| replicate 2 | **+14.47 ± 3.28 kcal/mol** |
| published met-enkephalin | +0.81 |
| **spread** | **13.75**, against a combined error of 4.53 |

## Gates

| Gate | Criterion | Result |
|---|---|---|
| G1 | sign correct | pass — both positive |
| G2 | interval covers published | rep1 pass, **rep2 fail** |
| G3 | λ-interval overlap | pass — ~1.0 kT, vs the old ladder's max 10.56 |
| G4 | **replicate agreement** | **FAIL** — 13.75 apart, 3× the combined error |

## Replicate 1 was luck, and the gate is what caught it

Reported two days ago, rep1 landed 0.09 kcal/mol from the literature — the closest this
project had come, and on its own it reads as a vindication of the re-spaced ladder. It
was coincidence. Replicate 2, identical protocol and an independent equilibration, gives
**+14.47**, which implies 4×10¹⁰-fold δ-preference. The most δ-selective compound in our
own 13-compound calibration panel is ~31-fold and nothing in the opioid literature
exceeds ~1000-fold, so rep2 is not a measurement at all.

Had the campaign stopped at one replicate we would have published a number that looked
like a success. This is exactly the outcome G4 was pre-registered to catch.

## Why it fails — not one bad window

| leg | r1 | r2 | shift |
|---|---|---|---|
| δ | 2349.53 | 2379.08 kJ/mol | **+29.6** |
| μ | 2346.53 | 2318.53 kJ/mol | **−28.0** |

The legs moved in **opposite directions**, so their errors add rather than cancel in the
difference.

Decomposed per λ interval (`data/` holds every value):

- largest single-interval replicate difference: **3.49 kJ/mol**
- intervals exceeding 5 kJ/mol: **0 of 55 (δ), 0 of 56 (μ)**
- mean |difference| per interval: **~1 kJ/mol**
- **40 of 55 and 40 of 56 intervals share the sign of their leg's total**

That last figure is the finding. At 50% the deviations would be random noise and would
partly cancel; at ~73% they are systematically biased within a replicate, so they
accumulate monotonically along the path to ≈30 kJ/mol — about **7 kcal/mol of replicate
variation in each absolute free energy**, when the quantity we need is a difference of two
of them and the effect is 0.81.

## The re-spacing fixed overlap, not precision

| ladder | replicates | spread |
|---|---|---|
| old, 27 windows | −3.12, +5.41 | 8.53 |
| new, 57 windows | +0.72, +14.47 | **13.75** |

The Cycle 13 diagnosis was right that λ spacing was too coarse, and G3 confirms the
overlap problem is solved. But precision did not improve — it got worse, and plausibly
*because* doubling the windows doubles the number of terms whose small biases accumulate.
Fixing overlap was necessary and insufficient.

## Consequence, per the pre-registration

**No value for `YGGFEVVG` may be quoted from this method.** The engPENK stage does not
run. The campaign stops here.

This is the fifth independent route to the selectivity question to fail, and the only one
that did not interpolate from published affinities. The cAMP assay is the arbiter, as
stated before any of this ran.

## What stands

Nothing here touches the structural results. The Cycle 12/13 pose findings use no
free-energy number and are unaffected, as is the calibrated Cycle 7 estimate
(+1.23 ± 1.76 kcal/mol, δ-preferring but not separable from no preference). The poster's
position — *design goal, not demonstrated result* — remains correct and is now better
supported than when it was written.
