# Intranasal dose model, parametric until the transfection returns

**16 Oct 2026.** The model is built and runs. The one input it needs is the expression yield
from the first transfection, which has not come back, so yield is carried as a free variable
and everything else is solved around it. When the number arrives this is a substitution, not
a week of work.

Code: `dose_model.py`. Figure: `dose_model.png`.

---

## What it computes

The chain from one spray actuation to a concentration at the receptor.

    dose of lipoplex
      -> plasmid deposited in the olfactory region     (f_olf, spray coverage)
      -> nuclei transfected                            (eta_tf)
      -> peptide molecules per cell per day            (YIELD, the free variable)
      -> peptide reaching the CNS compartment          (f_cns)
      -> steady state = production / clearance
      -> compared against the receptor EC50

Clearance runs by two routes in parallel: enzymatic degradation, which the siRNA arm is
designed to slow, and bulk CSF turnover, which it cannot touch. Keeping them separate is why
the silencing arm appears in the model at all.

## Three results that do not depend on the missing number

**1. Bulk CSF dilution is fatal, so the peptide has to act locally.** Reaching an EC50 of
25 nM across 155 mL of CSF would need 2.7e14 peptide molecules per transfected cell per day.
A strong transgene makes of order 1e4 to 1e6. The therapy cannot work by raising a
whole-CSF concentration, and the model only becomes satisfiable at effective distribution
volumes below about a microlitre, which is the scale of a local perineuronal space rather
than a compartment.

This is a constraint on how the therapy is described, not a verdict on whether it works.
Locally acting peptide release is a coherent mechanism; a bulk CSF concentration is not the
quantity to quote, and we should not put one on a poster.

**2. Enzymatic clearance dominates bulk turnover by about 25-fold**, 5.04 per hour against
0.20 per hour at midpoint parameters. That is the quantitative case for the silencing arm:
almost all of the peptide that disappears is being digested rather than washed out.

**3. The silencing arm has a hard ceiling, and it is set by a route the siRNA cannot
touch.** At the midpoint it buys 2.7-fold. Complete removal of enzymatic clearance would buy
70-fold and no more, because bulk CSF turnover then sets the rate. Useful to know before
anyone argues that a better knockdown is the main lever.

## What the answer is actually sensitive to

Spearman rank correlation against CNS concentration, 20,000 samples across every parameter
range.

| parameter | rho | source |
|---|---|---|
| transfection efficiency | +0.53 | **assumption** |
| cells exposed | +0.40 | physiological |
| fraction reaching the olfactory region | +0.40 | literature range |
| fraction entering the CNS | +0.39 | **assumption** |
| native peptide half-life | +0.29 | literature range |
| knockdown fold | +0.18 | **assumption** |
| spray volume | +0.07 | device |
| CSF volume | -0.03 | physiological |
| expression days | +0.01 | sets redosing interval, not concentration |
| CSF turnover | +0.00 | swamped by enzymatic clearance, see result 2 |

**Two of the top four are assumptions nobody has measured**, and that is the honest headline.
The precision of this model is limited by transfection efficiency and by the fraction of
secreted peptide that reaches the CNS, not by anything about the peptide.

## What the transfection needs to report

One number unblocks the model: **peptide molecules secreted per transfected cell per day**.
In practice that means quantifying the peptide in the supernatant by LC-MS/MS, counting
transfected cells by mEGFP, and dividing. A concentration alone is not enough; the cell count
is what converts it into the per-cell yield the model takes.

Two further numbers would narrow the two dominant assumptions, and are worth collecting if
they are cheap: the fraction of cells transfected at the dose used, and how much of the
secreted peptide crosses an epithelial barrier if a transwell is available.

## Limits, stated rather than discovered later

It is a steady-state compartment model, not a spatially resolved one, so within a compartment
it assumes mixing. That overestimates concentration far from the secreting cells and
underestimates it nearby, which is precisely why result 1 should be read as "the compartment
is wrong" rather than "the therapy fails".

It says nothing about which receptor the peptide prefers. Selectivity is a separate question
and the computational routes to it are closed; the cAMP assay settles it.

Parameter ranges are wide and several are declared assumptions. The model is for deciding
what to measure and how to describe the mechanism, not for quoting a dose.

**One defect found and fixed during the build**, recorded because the fix changed the
conclusions: a first version declared the olfactory fraction and spray volume in the
parameter table but never used them in the concentration chain, so the sensitivity analysis
reported them as having no influence. That was an artefact of the code rather than a property
of the system. Once they were wired in, the olfactory fraction became the third-strongest
driver.
