# Cycle 8: first free energies — control passes on sign, fails on magnitude

**Date:** 2026-09-20 · **Status:** campaign continuing · **Supersedes:** the first version
of this file, which claimed the control failed. That claim was wrong; see §5.

## Result

Three legs reached 27/27 windows at 3 ns. Thermodynamic integration over
⟨∂H/∂λ⟩, first 1 ns of each window discarded:

| leg | ΔG_decouple (kJ/mol) | coul | vdw |
|---|---|---|---|
| dtII DOR rep1 | 2661.71 | 2542.7 | 119.1 |
| dtII DOR rep2 | 2636.83 | 2544.2 | 92.6 |
| dtII MOR rep1 | 2539.59 | 2352.9 | 186.7 |

```
ΔG_bind(X)  = ΔG_decouple,water − ΔG_decouple,complex(X)
ΔΔG(μ−δ)    = ΔG_bind(μ) − ΔG_bind(δ) = ΔG_c(δ) − ΔG_c(μ)
            = 2649.27 − 2539.59 = +109.68 kJ/mol = +26.21 kcal/mol
```

**Published deltorphin II: +5.39 kcal/mol. Sign CORRECT (δ-selective).
Magnitude over-estimated ≈ 4.9×.**

Per-replicate: rep1 gives +29.16, rep2 gives +23.24 kcal/mol. **Replicate spread on the
δ side is 5.95 kcal/mol — larger than the published effect being measured.**

## Reading

**The sign is resolved; the magnitude is not.** A directional answer at 3 ns per window is
real information — it is what Cycle 7 could only give with a compressed regression slope.
But a 5.95 kcal/mol spread against a 5.39 kcal/mol effect means the *size* of the
selectivity is not yet resolvable, and ~5× over-estimation is consistent with that.

**No number is claimed for `YGGFEVVG`.** Its legs have not run. When they do, the same
caveat applies: direction interpretable, magnitude not, until the replicate spread comes
below the effect size.

## Two artefacts that look alarming and are not

**1. ΔG ≈ 2650 kJ/mol (≈633 kcal/mol) to decouple a heptapeptide.** This is annihilation,
not decoupling-to-vacuum: intramolecular electrostatics are switched off too, contributing
a large self-energy. **92.5 % of the Coulomb term is common to both receptors** and cancels
exactly in the difference. Absolute annihilation free energies are not comparable to
binding free energies and should not be sanity-checked against them.

**2. No foreign-lambda ΔH columns in the dhdl files.** `calc-lambda-neighbors` was never
set, so `gmx bar` cannot use the Bennett estimator and falls back to integrating ∂H/∂λ.
An independent TI implementation reproduces its output to ~0.1 % (2661.71 vs 2661.41),
confirming the fallback is doing the right thing. Setting `calc-lambda-neighbors = -1` in
future windows would enable BAR, which has better statistical efficiency — worth doing,
but the present numbers are not invalidated by its absence.

## 5. Correction record

The first version of this document asserted the control had failed, on three grounds. Two
were my errors and one was overstated:

| claim | verdict |
|---|---|
| "sign wrong, −26.72 kcal/mol" | **my error.** I computed μ−δ. For decoupling free energies tighter binding costs *more*, so ΔΔG = ΔG_c(δ) − ΔG_c(μ). Correct value +26.21, sign right. |
| "2650 kJ/mol physically implausible, so the calculation is wrong" | **category error.** Applied binding-free-energy intuition to an annihilation free energy. The large term is shared self-energy and cancels. |
| "replicate spread is an independent problem" | **overstated as independent** — I listed it alongside two claims that were themselves downstream of my own arithmetic. It is, however, a real limitation, and the only one of the three that survives. |

Acting on that document I also recommended cancelling the 13 running workers. That
recommendation was withdrawn before anything was cancelled.

**Lesson.** The instrument that caught the original "3 legs complete" claim was a filename
pattern that silently matched nothing — and the instrument that produced the false control
failure was a subtraction in the wrong order. Both times the *data* were fine and my
*analysis* was not. When a result contradicts a well-established literature value, the
prior should be that the new analysis code is wrong, not that the field is. Check the
analysis against a hand-worked case before concluding a control has failed.
