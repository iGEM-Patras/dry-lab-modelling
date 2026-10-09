# Cycle 3b Stage-1 gate: final verdict on the complete n=5 dataset

**Date:** 2026-08-31
**Input:** all 40 replicates, conditional bound-state MM-GBSA (GB, one frame definition)
**Verdict:** **FAIL** (Stage 2 is not authorised.)

## What changed since the last run

The previous gate evaluation could not produce a verdict at all. `gate.py` pairs the two
receptor arms *within* each replicate, so a replicate contributes only if BOTH arms scored.
Nine runs had been refused by the membrane gate, which collapsed both deltorphins to n=1
and left the SEM undefined.

All 40 runs have now been rescored in BOUND_MODE: frames are selected from the whole
trajectory where the peptide is in the pocket (ligand–lipid min distance > 0.4 nm AND
ligand RMSD to the docked pose <= 0.52 nm), then subsampled to 100. Every arm is n=5.

Rescoring **all** 40 rather than splicing 9 new values into the old 31 was deliberate: a
conditional bound-state energy and a last-10ns energy are different quantities and must
not be pooled. The recomputation cost ~2 h of `pshort_el8` time and removes the ambiguity.

**The two definitions agree closely where both exist.** For the 31 runs scoreable either
way, median |shift| = 1.04 kcal/mol, mean 1.50, max 4.59, within MM-GBSA's own
1–2 kcal/mol uncertainty. The bound-frame restriction does not distort the runs that never
left the pocket; it only rescues the ones that did.

## Verdict detail

| control | n | computed ΔΔG | SD | SEM | experimental |
|---|---|---|---|---|---|
| met-enkephalin | 5 | +26.38 | 3.27 | 1.46 | 0.00 |
| deltorphin I | 5 | +15.18 | 11.08 | 4.95 | +5.70 |
| deltorphin II | 5 | +7.48 | 7.25 | 3.24 | +5.39 |
| endomorphin-1 | 5 | −0.91 | 7.41 | 3.32 | −2.99 |

- **G1 PASS**: all four sign/ranking checks hold: both deltorphins > 0, endomorphin-1 < 0,
  and the deltorphins rank above endomorphin-1. The method gets the *direction* right.
- **G2′ FAIL**: only met-enkephalin (SEM 1.46) is under the 1.5 kcal/mol threshold.
  The other three are 3.2–5.0.
- **G3 FAIL**: slope 0.594, 95% CI [−1.024, 2.213], r = 0.179 over 20 points. The CI
  spans zero, so the computed–experimental correlation is not distinguishable from none.

## Reading

The failure is replicate scatter, not a broken pipeline. Per-replicate ΔΔG values within a
single control span 27 kcal/mol for deltorphin I (+2.5 to +28.4). With that dispersion, 5
replicates cannot pin a mean to the 1.5 kcal/mol the gate demands.

Met-enkephalin is the informative outlier: it has the *tightest* replicate agreement
(SEM 1.46) and is also the *most wrong* (+26.4 computed vs 0.0 experimental). A reproducible
large error is a systematic one. This is consistent with the standing caveat that these are
enthalpy-dominated effective energies with no entropy term: met-enkephalin is the smallest
and most flexible of the four, so the missing configurational-entropy penalty should hit it
hardest, and it does.

## Consequence

Per the pre-registration, cycle 3b terminates and reports a negative methodological result:
**single-trajectory MM-GBSA at n=5 does not resolve δ/μ selectivity for these peptides.**
The project recommendation is unchanged: radioligand competition binding on YGGFEVVG and
YGGFDIIG.

## Residency caveat (mandatory when quoting any single value)

A bound-state ΔG says how tight the pose is *while it exists*, not how strong the binding
is. Three runs have residency < 50%: deltorphin II μ rep1 (10.7%), rep3 (13.6%), and
deltorphin II δ rep2 (49.9%). `merge_bound_results.py` refuses to emit a ΔG without its
residency fraction, and every consumer should carry both.

Residency itself is a reportable observable and does not depend on the energy model:
deltorphin II holds the δ pocket in 82–100% of frames but the μ pocket in as little as
10.7%. That difference is in the right direction for a δ-selective peptide and is
measured, not modelled.
