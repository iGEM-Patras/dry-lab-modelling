# Intranasal dose model

Parametric nose-to-brain dose model for the Epione spray. Built 16 October 2026 while the
expression yield from the first transfection was still outstanding, with that yield carried
as a free variable so the model is complete except for one substitution.

| file | contents |
|---|---|
| `DOSE_MODEL.md` | the write-up: results, sensitivity, what the transfection must report, limits |
| `dose_model.png` | required yield against distribution volume, and the sensitivity ranking |
| `data/dose_model.py` | the model. Importable, with self-checks in the docstrings |
| `data/dose_model_parameters.csv` | every parameter with its range, units and source class |
| `data/dose_model_sensitivity.csv` | Spearman ranking over 20,000 samples |
| `data/dose_model_result.json` | the headline numbers in machine-readable form |
| `data/dose_model_result_v2.json` | the upper-bound, repeat-dosing and wet-lab-ceiling numbers added 22 Nov |
| `data/dose_model_sensitivity_v2.csv` | Spearman ranking recomputed against the repeat-dosing concentration |
| `dose_references.csv` | the literature anchors, with what each one is used for |

## How to finish it

One number closes the model: peptide molecules secreted per transfected cell per day,
obtained by quantifying supernatant peptide with LC-MS/MS and dividing by the mEGFP-positive
cell count. As of 22 November the free variable is **bounded above** by our own dot blot at
6.9e7 molecules per cell per day per mL of lysate, which is 69-fold above the top of the
plausible range and so excludes nothing, but does let the headline conclusion be tested
against our own data rather than against an assumption. The one quantity needed to tighten
it is the lysate volume, which the notebook does not record. Then:

```python
from dose_model import sample, cns_concentration_nM, required_yield_for_ec50
import numpy as np
rng = np.random.default_rng(0)
p = sample(20000, rng)                       # or override parameters you have measured
conc = cns_concentration_nM(MEASURED_YIELD, p)
```

## What the model already settles

Bulk cerebrospinal fluid dilution is fatal to the mechanism as usually described: an EC50 of
25 nM across 155 mL would need 2.7e14 molecules per cell per day, against a plausible
cellular output of 1e4 to 1e6. The therapy has to act locally, and a whole-CSF concentration
is not a quantity we should quote.

Enzymatic clearance exceeds bulk CSF turnover by about 25-fold, which is the quantitative
argument for the neprilysin silencing arm. That arm buys roughly 2.7-fold at midpoint
parameters and cannot exceed 70-fold however complete the knockdown, because bulk turnover
then becomes the limiting route.

Two of the four strongest drivers are assumptions nobody has measured, so the precision of
any dose estimate is currently set by transfection efficiency and by the fraction of secreted
peptide reaching the central nervous system, rather than by anything about the peptide.

## Safety arms, added 22 November 2026

The model now has an upper bound as well as a target. `max_tolerated_yield()` and
`exposure_margin()` answer how much is too much; `accumulation_factor()` superposes repeat
doses, which the previous version made unrepresentable by returning the expression window as
the dosing interval.

Two results follow immediately. The therapeutic window is **exactly 6.5-fold** at midpoint
and is set entirely by one assumed number, `tolerated_multiple_of_ec50`, anchored to SNC80
in rhesus monkeys (PMID 17112570) because no convulsant threshold exists for our peptide.
And **daily dosing accumulates 3 to 14-fold**, 8.5-fold at midpoint, so the schedule alone
can cross that window before any biological uncertainty is considered. Full discussion in
`DOSE_MODEL.md`.
