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

---

## Addendum, same day: the μ-preferring result is the outlier of three methods

The engPENK number was checked against the two other methods this project has run on the
same receptors, asking only whether each gets the **direction** right on peptides with
published values.

### MM-GBSA (Cycle 3b) — 4 of 4 directions correct

Computed from `cycle3b/results_stage1.csv`. MM-GBSA convention: more negative = tighter.

| peptide | ΔG_δ | ΔG_μ | δ−μ | called | published |
|---|---|---|---|---|---|
| Deltorphin I | −64.38 | −55.19 | −9.19 | δ | +5.70 δ ✓ |
| Deltorphin II | −66.72 | −56.45 | −10.27 | δ | +5.39 δ ✓ |
| Endomorphin-1 | −54.95 | −55.34 | **+0.40** | **μ** | **−2.99 μ ✓** |
| **Met-enkephalin** | **−69.57** | **−41.94** | **−27.63** | **δ** | **+0.81 δ ✓** |

Two results matter here. MM-GBSA gets **met-enkephalin** — the peptide chemically closest
to `YGGFEVVG`, same `YGGF` message domain, free acid, endogenous — correctly δ-preferring.
And it gets **endomorphin-1** correctly μ-preferring, which is precisely the control the TI
protocol inverted.

Its *ranking* is still wrong (Spearman ρ = +0.20, p = 0.80; it calls met-enkephalin the most
δ-selective of the four where published data puts it third), consistent with Cycle 3b having
passed its direction gate and failed its magnitude gate. So MM-GBSA supports **direction
only** — which is exactly what is being asked of it here.

### Three methods on the direction test

| method | directions correct | detail | gate |
|---|---|---|---|
| MM-GBSA (Cycle 3b) | **4/4** | incl. met-enkephalin δ and endomorphin-1 μ | magnitude failed |
| Co-folding affinity (Cycle 7) | **12/13** | r = 0.805, p = 0.0009 | **passed** |
| Free energy / BAR (Cycle 8) | **1/2** | endomorphin-1 sign inverted | **sign failed** |

**The only method placing `YGGFEVVG` on the μ side is the only one that failed its sign
gate, and the only one never tested on an enkephalin-family peptide.** That does not prove
it wrong, but it makes it the weakest of the three on exactly the question at issue.

### The decisive test, and why it was not run

Met-enkephalin TI legs do not exist and `npt.gro` is absent for `c3b_menk_DOR` and
`c3b_menk_MOR` — only `min.gro`, `system.top` and `index.ndx` are present. Running it means
equilibration plus 4 legs × 27 windows × 3 ns ≈ **324 ns ≈ 7 GPU-days**. Recorded as the
first thing to run if this question is revisited: if this protocol also calls met-enkephalin
μ-preferring, the engPENK value is a protocol artefact and can be set aside.

### Physical proportion

−8.75 kcal/mol at 310 K implies **~1.5 × 10⁶-fold μ-selectivity**, some 2,800× more
μ-selective than DAMGO, for a peptide built on the enkephalin message motif. Back-projecting
through the two-control calibration (`predicted = +11.24 + 3.30 × published`) gives −6.05,
still beyond the published panel's μ extreme of −4.82. Neither the raw value nor its
correction lands in physical range — and the correction rests on a two-point line whose
lower point has the wrong sign.

*Method caution recorded:* an earlier entry in this project called a 2650 kJ/mol decoupling
energy "physically implausible" and was **wrong** — that was intramolecular self-energy,
which cancels in a difference. Here the quantity **is** a difference, so the self-energy has
already cancelled and the implausibility argument applies. The two cases look alike and are
not.

### What this does and does not change about the project

**δ-*exclusivity* was never a reachable target and is not required by the mechanism.** Native
met-enkephalin is published at **+0.81 kcal/mol = 3.7× δ-preferring** — mildly δ-preferring,
not exclusive — and it is the endogenous analgesic this construct supplies. The most
δ-preferring compound in the Cycle 7 calibration panel is +2.12 (31×). Cycle 7 places
`YGGFEVVG` at +1.23 (7.4×), i.e. at or slightly above native.

Analgesia operates through both receptors; δ-selectivity reduces μ-mediated respiratory and
dependence risk. The former is the mechanism, the latter the differentiation. Today's result
bears on the differentiation claim, not on whether the construct can produce analgesic
peptides.
