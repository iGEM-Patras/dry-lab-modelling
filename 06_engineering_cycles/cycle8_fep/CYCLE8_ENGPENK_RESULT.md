# Cycle 8: the engPENK free energy points AWAY from δ-preference

**Date:** 2026-09-27 · **Campaign complete:** 4/4 legs, 108/108 windows, 324 ns, 0 failures

## Result

All four legs verified 27/27 windows at ≥2999 ps before BAR was run.

| leg | ΔG decoupling (kJ/mol) |
|---|---|
| δ (OPRD1) rep1 | 3343.49 ± 5.97 |
| δ (OPRD1) rep2 | 3347.19 ± 4.71 |
| μ (OPRM1) rep1 | 3368.75 ± 9.37 |
| μ (OPRM1) rep2 | 3395.18 ± 3.20 |

Decoupling convention: tighter binding costs **more** to remove, so
ΔΔG(μ−δ) = ΔG_δ − ΔG_μ.

```
ΔΔG(μ−δ) = -8.75 ± 3.19 kcal/mol      95% CI [-15.13, -2.38]
direction: MU-preferring              CI excludes zero
```

**This is the opposite direction to the design goal.**

## It contradicts Cycle 7, and the intervals do not overlap

| method | ΔΔG(μ−δ) | 95% CI | reading |
|---|---|---|---|
| Cycle 7 co-folding affinity head (n=13 gate, r=0.805) | **+1.23 ± 1.76** | [−2.29, +4.75] | nominally δ, spans zero |
| Cycle 8 free energy, BAR (this work) | **−8.75 ± 3.19** | [−15.13, −2.38] | μ-preferring, excludes zero |

The estimates differ by **9.98 kcal/mol** and their 95% intervals are **disjoint**. At
least one method is miscalibrated for this peptide. That is the honest headline, and it is
not resolvable from the data in hand.

## Three reasons this is not a clean falsification either

1. **The protocol failed its own sign gate.** G1 required correct sign on both bracketing
   controls; endomorphin-1 came out **+1.37** against a published **−2.99**. A protocol that
   inverts a known μ-selective control cannot establish the sign of an unknown. The
   engPENK sign is therefore *suggestive, not established*.
2. **engPENK lies outside the calibrated range.** The controls span [+1.37, +29.04];
   engPENK sits at **−8.75**, below both. G3 (ranking) passed on a single binary comparison
   between two controls, so applying it to a point outside their span is **extrapolation**.
3. **The μ legs are under-sampled.** The two μ replicates differ by **6.32 kcal/mol** —
   larger than deltorphin II's entire published effect (5.39). δ replicates agree to
   0.44 kcal/mol; μ does not. The asymmetry is itself a warning.

## What can and cannot be claimed

**Can:** δ-selectivity is **not demonstrated** by either method. Two independent
calculations disagree on the sign, and the physics-based one — the method with no
regression slope to correct — places the peptide on the μ-preferring side.

**Cannot:** that engPENK *is* μ-selective. The protocol that produced that number gets a
known control's sign wrong, and the value is an extrapolation beyond the calibrated range.

**Wet-lab consequence:** radioligand competition binding at δ and μ becomes the decisive
experiment rather than a confirmatory one. The cAMP assay with selective antagonists
already specified in the abstract's Progress section is the right read-out; this result
raises its priority from *"confirm what modelling predicts"* to *"settle which of two
contradictory predictions is right."*

## Provenance

Window inputs were literal copies of `c3b_dtII_DOR_rep1/w00.mdp`–`w26.mdp`, the files that
produced the gated control result, so the λ schedule, soft-core settings and coupling
directives are identical to the comparators by construction. `couple-moltype = system2`
(110 atoms = the peptide) was verified from the tpr, not assumed.

## Method note

The first BAR job printed **empty** results for all four legs. Cause: `grep '^total'`
required the string at column 1, while `gmx bar` indents that line. The sampling was
complete and the calculation had run; only the extraction pattern failed. No number was
quoted from that output.

This is the fourth instance in this project of a pattern matching nothing and the blank
being mistaken for a result — after the unpadded window glob, the `head -3` legend
truncation, and the `*peg*` search that returned `libnvjpeg.so`. Standing rule reaffirmed:
**a limited instrument reporting absence is not evidence of absence**, and an extraction
pattern must be validated against known-present output before its silence is believed.
