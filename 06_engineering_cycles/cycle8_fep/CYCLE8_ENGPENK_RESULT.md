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
(110 atoms = the peptide) was verified from the **mdp**, not assumed.

**Correction (2026-09-27).** An earlier version of this line said the directive was "verified
from the tpr". That is not achievable: `gmx dump -s` does **not** emit a `couple-moltype`
field at all. Checked directly — `gmx dump` on this very tpr, the one that produced the
−8.75 result, returns **zero** matches for `couple-moltype`, as does the tpr for the
met-enkephalin control. The absence is a property of the dump tool, not of the files. The
verification behind the result was real but came from reading the mdp; the provenance
sentence overstated where it came from.

*Generalisable lesson, and the fifth instance of this class today:* a grep that matches
nothing looks identical to a grep whose subject is absent. What resolved it here was
running the same query against a **known-good artifact** — if the pattern also returns
nothing on a file that demonstrably worked, the pattern is wrong rather than the file.
Comparing against a working reference beats comparing against an expectation.

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

---

## The met-enkephalin control is running (launched 2026-09-27)

The decisive control identified above is no longer deferred. Both systems were equilibrated
on `pibu_el8` — the same CPU partition the gated control campaign ran on, chosen so the
control shares hardware as well as protocol with its comparators.

### Peptide identity settled three independent ways

Window generation **aborted on the first attempt**, correctly: an atom-count range of
40–200 matched two moleculetypes. Both were then identified by computed molecular formula:

| moleculetype | atoms | identity | formula | copies |
|---|---|---|---|---|
| `system2` | **75** | met-enkephalin `YGGFM` | C₂₇H₃₅N₅O₇S | **1** |
| `system3` | 134 | POPC | C₄₂H₈₂NO₈P | 339 (δ) / 219 (μ) |

Atom count, molecular formula and copy number all agree that `system2` is the peptide. The
guard's criterion was too loose, but it **failed safe** — refusing rather than taking the
first match, which would have decoupled a lipid and returned an ordinary-looking number
after days of compute. The retry asserts exactly 75.

### Coupling directive confirmed

```
free-energy      = yes
couple-moltype   = system2
couple-lambda0   = vdw-q
couple-lambda1   = none
couple-intramol  = yes
```

Identical on every free-energy line to `c3b_dtII_DOR_rep1/w00.mdp`, the leg that produced
the gated result. 108/108 window inputs built.

### Production

8 workers, atomic `mkdir` lock claiming, 3 ns per window, 324 ns total (~4–6 days). Leg
order is `DOR_rep1, MOR_rep1, DOR_rep2, MOR_rep2` — one replicate of **each** receptor
first, since a ΔΔG needs both, so a usable estimate exists at roughly half the sampling
rather than only at the end.

Each worker carries a **progress gate**: simulated time is recorded before and after every
attempt and the worker aborts if a window advances nothing. This is a direct fix for the
earlier defect where a retry loop treated a deterministic failure as transient and reported
success on a run that made zero progress.

### What the result will and will not settle

Stated before the data exists. Met-enkephalin's published ΔΔG(μ−δ) is **+0.81 kcal/mol** —
a small effect. This protocol already failed on endomorphin-1 at **−2.99**, an effect 3.7×
larger, so it probably cannot resolve +0.81 correctly either. This is a **magnitude-scale
test, not a sign test**:

- **near zero (−2 to +2)** → the protocol behaves sanely on an enkephalin-family peptide, so
  the engPENK −8.75 is anomalous rather than systematic;
- **−6 or worse** → systematic bias against δ for `YGGF`-motif peptides, and the engPENK
  value can be set aside as a protocol artefact;
- **mildly δ-preferring** → the protocol is better than its endomorphin-1 failure suggested,
  and −8.75 becomes harder to dismiss. This is the outcome that would matter.

Two of three outcomes support setting the engPENK value aside; the third is the one worth
knowing about.
