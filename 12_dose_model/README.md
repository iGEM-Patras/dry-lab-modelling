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

## How to finish it

One number closes the model: peptide molecules secreted per transfected cell per day,
obtained by quantifying supernatant peptide with LC-MS/MS and dividing by the mEGFP-positive
cell count. Then:

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
