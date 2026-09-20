# Cycle 8: the TI protocol fails its own control — result withheld

**Date:** 2026-09-20 · **Status:** campaign paused, no free energy reported

Per the Cycle 8 pre-registration, deltorphin II is in the panel *because* it has a
published δ/μ selectivity, and a failed control means the target peptide's number is not
reported. The control has now failed. **No ΔΔG for `YGGFEVVG` is claimed from this
campaign.**

## What was computed

Three legs reached 27/27 windows at 3 ns each, so a ΔΔG became computable for the first
time:

| leg | ΔG (kJ/mol) | BAR stat. error |
|---|---|---|
| dtII DOR rep1 | 2661.41 | ± 2.49 |
| dtII DOR rep2 | 2640.09 | ± 1.09 |
| dtII MOR rep1 | 2538.94 | ± 3.52 |

ΔΔG(μ−δ) = **−26.72 kcal/mol**, against a published **+5.39**. Sign wrong, magnitude ~5×.

## Three independent reasons the number is not usable

**1. The absolute values are physically implausible.** ~2650 kJ/mol is ~633 kcal/mol to
decouple a heptapeptide; the expected scale is O(100) kJ/mol. A result that far off scale
indicates the calculation is not doing what the protocol intends.

**2. The reported per-transition values do not sum to the reported total.** The printed
transitions near the decoupled end are small (−7.82, +0.63 kJ/mol) while the total is
2661 kJ/mol. Either a few transitions dominate enormously, or the total is being assembled
from something other than the printed path.

**3. The replicate spread exceeds the effect being measured.** The two δ replicates differ
by 21.3 kJ/mol = **5.10 kcal/mol**; the published effect is 5.39 kcal/mol. Even a correct
sign would carry no information at this sampling. Note also that BAR's own statistical
errors (±1–3 kJ/mol) are two orders of magnitude smaller than the replicate spread — the
classic signature of an under-converged calculation reporting a confidently wrong number.

## Root cause identified

The `dhdl.xvg` files contain **only three data series**:

```
@ s0 legend "Potential Energy (kJ/mol)"
@ s1 legend "dH/dl coul-lambda = ..."
@ s2 legend "dH/dl vdw-lambda = ..."
```

There are **no foreign-lambda ΔH columns** — no energy differences evaluated at
neighbouring λ states. BAR (Bennett acceptance ratio) is *defined* on those differences;
without them the estimator cannot do what its name says. The mdp needs
`calc-lambda-neighbors = -1` (all states) or at minimum `1`, which was never set.

This is a protocol defect in the window inputs, not a sampling shortfall. **More
simulation time would not have fixed it**, and the 271 ns banked so far cannot be rescued
into a BAR estimate — though the dH/dλ series remain valid for thermodynamic integration,
which is a separate (and weaker) estimator.

## What this costs and what it does not

- **Costs:** the campaign's 216 windows must be regenerated with foreign-lambda output
  before any BAR number exists. The banked sampling is not lost for TI, but TI over a
  27-point grid with this replicate spread will not resolve a 5 kcal/mol effect either.
- **Does not cost:** Cycle 7's calibrated estimate for `YGGFEVVG` (+1.23 ± 1.76 kcal/mol,
  n=13 gate, r = 0.805) is unaffected and remains the project's best selectivity number.

## Lesson

The pre-registration's control requirement is what caught this. Had the campaign run only
the engineered peptide, it would have returned ≈ −26 kcal/mol with a tight-looking ±2.5
error bar and nothing in the output would have looked wrong. A control with a published
value is the only thing that distinguishes "converged" from "confidently wrong".

Second lesson, on instrumentation: the failure was visible in the *absolute* values long
before the sign comparison. A protocol check should assert that a computed quantity falls
in a physically sensible range before it is compared to anything — 2650 kJ/mol for a
heptapeptide should have failed a range assertion at the first leg, not at the first ΔΔG.
