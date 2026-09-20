# Cycle 8: first free-energy result — control passes on sign, magnitude unresolved

**Date:** 2026-09-20 · **Status:** campaign continuing, target peptide not yet run

> **File history.** Committed first as `CYCLE8_CONTROL_FAILURE.md` asserting the protocol
> had failed. That assertion was wrong, and so were two of the three reasons given for it.
> §5 records what was claimed, what was actually true, and why. Nothing has been deleted —
> commits `9abab47` and `3fd0a04` hold the superseded versions.

## 1. Result

Three legs reached 27/27 windows at 3 ns each. BAR (verified below to be genuine Bennett
acceptance, not a fallback), first 1 ns of each window discarded:

| leg | ΔG_annihilation (kJ/mol) | coul | vdw |
|---|---|---|---|
| dtII DOR rep1 | 2661.41 ± 2.49 | 2542.7 | 119.1 |
| dtII DOR rep2 | 2640.09 ± 1.09 | 2544.2 | 92.6 |
| dtII MOR rep1 | 2538.94 ± 3.52 | 2352.9 | 186.7 |

```
ΔG_bind(X) = ΔG_ann,water − ΔG_ann,complex(X)
ΔΔG(μ−δ)   = ΔG_bind(μ) − ΔG_bind(δ) = ΔG_ann,c(δ) − ΔG_ann,c(μ)
           = 2649.27 − 2539.59 = +109.68 kJ/mol = +26.21 kcal/mol
```

| | |
|---|---|
| **ΔΔG(μ−δ), deltorphin II** | **+26.21 kcal/mol** (rep1 +29.19, rep2 +23.24) |
| published | +5.39 kcal/mol |
| sign | **CORRECT — δ-selective** |
| over-estimation | ≈ 4.9× |
| δ replicate spread | **5.95 kcal/mol** |

## 2. Setup verified, not assumed

Read from `mdout.mdp` (what grompp actually used) and the tpr, after an earlier version of
this file asserted things that had not been checked:

```
couple-moltype  = system2        110 atoms
couple-lambda0  = vdw-q  →  couple-lambda1 = none      (full annihilation)
couple-intramol = yes
calc-lambda-neighbors = -1
```

- **system2 = 110 atoms** — deltorphin II (YaFEVVG-NH₂ with hydrogens). Independently,
  exactly 110 atoms carry differing A/B-state parameters, so the perturbed set is the
  peptide and nothing else.
- system1 = 5,755 atoms (receptor); system3 = 134 atoms × 274 (lipid).
- This closes the check flagged at campaign setup: decoupling the wrong molecule does not
  error, it runs for weeks and returns a plausible number.

## 3. Two features that look alarming and are not

**ΔG ≈ 2650 kJ/mol to annihilate a heptapeptide.** `couple-intramol = yes` means
intramolecular electrostatics are switched off as well, contributing a large self-energy.
**92.5 % of the Coulomb term is common to both receptors** and cancels in the difference.
Absolute annihilation free energies are not comparable to binding free energies and must
not be sanity-checked against them.

**TI reproduces BAR to ~0.1 %** (2661.71 vs 2661.41). This is good λ-overlap, which is the
expected result, not a sign that one estimator has degenerated into the other.

## 4. What is and is not claimed

**Claimed:** the protocol recovers the *direction* of a published δ/μ selectivity for a
control peptide at 3 ns per window.

**Not claimed:** any magnitude. A 5.95 kcal/mol replicate spread against a 5.39 kcal/mol
effect means the size of the selectivity is not resolvable at current sampling, and the
≈4.9× over-estimation is consistent with that.

**Not claimed:** anything about `YGGFEVVG`. Its legs have not run. When they do, direction
will be interpretable and magnitude will not, until the replicate spread falls below the
effect size. Cycle 7's calibrated estimate (+1.23 ± 1.76 kcal/mol, n=13 gate, r = 0.805)
remains the project's selectivity number.

## 5. Correction record

Three claims in the first version of this file were wrong. All three were errors in my
*analysis*, not in the data or the simulations.

| claim | reality | cause |
|---|---|---|
| "3 legs incomplete — windows 0–9 missing" | all 27 present | shell glob `w0_dhdl*` against files named `w00_dhdl`; `w1*` also matched `w10` |
| "sign wrong, ΔΔG = −26.72" | **+26.21, sign correct** | computed μ−δ; for annihilation free energies tighter binding costs *more*, so it is δ−μ |
| "no foreign-lambda ΔH columns, BAR invalid" | **27 ΔH columns, 32 data columns** | piped the legend grep through `head -3`, then read the truncation as absence |

A fourth claim — "the replicate spread is an independent problem" — was true but was
presented as independent evidence alongside two claims that were downstream of my own
arithmetic. It is the only limitation that survives.

Acting on the wrong document I also recommended cancelling the 13 running workers. The
recommendation was withdrawn before anything was cancelled.

**Standing lessons.**

1. **A limited instrument reporting absence is not evidence of absence.** Three failures
   today shared this shape: a glob that matched nothing, a `head -3` that hid 28 columns,
   and earlier a bead-count check that passed on unfolded coordinates. Enumerate the
   expected set and report what is missing; never conclude from what a filter happened to
   return.
2. **When a result contradicts a well-established literature value, the prior is that the
   new analysis code is wrong, not the field.** I inverted this twice in one session.
3. **Sanity-check a quantity against the right reference class.** 2650 kJ/mol is absurd
   for a binding free energy and unremarkable for an annihilation free energy with
   `couple-intramol = yes`.
