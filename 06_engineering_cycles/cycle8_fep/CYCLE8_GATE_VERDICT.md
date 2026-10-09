# Cycle 8 gate verdict: G1 FAIL, G2/G3 PASS: direction and ranking only

**Date:** 2026-09-24 · **Campaign complete:** 216/216 windows, 648/648 ns, 8/8 legs at 27/27

## Result

Both bracketing controls, two replicates per receptor. BAR, first 1 ns of each window
discarded. ΔΔG(μ−δ) = ΔG_ann(δ) − ΔG_ann(μ); 95 % CI from replicate half-spreads.

| control | predicted ΔΔG(μ−δ) | published | sign | published inside CI? |
|---|---|---|---|---|
| Deltorphin II (δ-selective) | **+29.04 ± 3.44** | +5.39 | correct | **no**, significantly over-estimated |
| Endomorphin-1 (μ-selective) | **+1.37 ± 5.14** | −2.99 | wrong | **yes**: CI spans −8.91 to +11.65 |

| gate | criterion | result |
|---|---|---|
| **G1** | sign correct on both controls | **FAIL** |
| **G2** | controls separated beyond combined error | **PASS** (27.67 vs 12.37) |
| **G3** | δ-selective control ranks above μ-selective | **PASS** |

Calibration slope through the two controls: **3.30**, the method *amplifies* the
selectivity scale ~3.3×. (Cycle 7's co-folding affinity head did the opposite: it
compressed.)

## Reading

**G1 fails for lack of power, not because the physics inverted.** Endomorphin-1's CI
contains its published value; the calculation does not contradict the literature, it simply
cannot resolve a 3 kcal/mol effect. Deltorphin II is the stricter failure: its CI excludes
+5.39, so its magnitude is *significantly* wrong even though its direction is right.

**The replicate scatter is the binding constraint.** Per-leg spread between the two
replicates, in kcal/mol: dtII δ 5.10, dtII μ 4.62, em1 δ 9.67, em1 μ 3.48, against
published effects of 5.39 and 2.99. Three of four legs scatter as much as or more than the
effect being measured. BAR's own statistical errors (±1–6 kJ/mol ≈ 0.2–1.4 kcal/mol) are
several-fold smaller than reproducibility, which is the standard signature of
under-sampling rather than converged statistics.

**Consequence, per the pre-registration.** G1 fails, so **no magnitude is reported for
`YGGFEVVG` from this campaign.** G2 and G3 passing means direction and ranking are usable:
this protocol can say *which* of two peptides is more δ-preferring, but not by how much.

Cycle 7's calibrated estimate remains the project's selectivity number:
**+1.23 ± 1.76 kcal/mol** (n=13 panel, r = 0.805, p = 0.001).

## What would fix it

The deficit is sampling, not protocol: the setup was verified from `mdout.mdp`
(`couple-moltype = system2`, 110 atoms = the peptide; 27 foreign-λ ΔH columns present, so
BAR is genuine Bennett acceptance). At 3 ns/window the replicate spread is ~5 kcal/mol; the
error on a mean scales as 1/√t, so resolving a 3 kcal/mol effect to ±1 kcal/mol needs
roughly an order of magnitude more sampling per window, or more replicates. That is a
multi-week campaign at the measured 44.8 ns/day per GPU and is **not** worth starting to
answer a question Cycle 7 already answers with a passing gate.

## Figure

`cycle8_gate.png`: (a) predicted vs published with 95 % CIs and the identity line;
(b) per-leg replicate deviation drawn at the scale of the published effect.
