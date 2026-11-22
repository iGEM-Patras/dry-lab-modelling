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

---

## Added 22 Nov 2026: the two arms the model was missing

The October model could answer only one question, *how much yield is needed to reach the
EC50*. It had no upper bound and no repeat dosing, so it could not be used for the safety
question the route actually raises. Both arms are now in `dose_model.py`.

### 1 · An upper bound, and how weakly it is anchored

`max_tolerated_yield()` is the upper counterpart of `required_yield_for_ec50()`, and
`exposure_margin()` reports where a given yield sits between them.

Because every term in the chain is linear in yield, the therapeutic window is **exactly**
`tolerated_multiple_of_ec50` and nothing else in the model affects it. At midpoint that is
**6.5-fold**, and the code asserts this identity rather than reporting it, so a future change
that breaks the linearity will fail loudly.

That is the honest statement of how little this model constrains safety: the entire window
is one assumed number. The number is anchored as well as the literature allows, and no
better. **No convulsant threshold has been measured for the engineered payload.** The range
3 to 10 comes from SNC80 in rhesus monkeys, where 10 mg/kg IM produced behavioural
convulsions and EEG seizures in one of four animals, 3.2 mg/kg produced neither, and the
convulsant dose was 3 to 10 fold above doses producing other behavioural effects
(PMID 17112570). SNC80 is a high-efficacy non-peptidic δ agonist, the ligand class in which
the liability is established (PMID 37004753); for peptide enkephalins the reported direction
is the opposite one. See `DELTA_SEIZURE_SAFETY.md`. The anchor is therefore conservative by
construction, and it is still a placeholder for a measurement.

### 2 · Repeat dosing, which the model previously forbade

`dosing_interval_days()` returned `expression_days` unchanged, so the dosing interval could
never be shorter than the expression window and doses could never overlap. Accumulation was
not assumed away; it was unrepresentable.

`dose_interval_days` is now an independent parameter and `accumulation_factor()` superposes
overlapping doses. One dose expresses for 3 to 14 days, so **daily dosing accumulates 3 to
14-fold** over the single-dose concentration, 8.5-fold at midpoint. Against a 6.5-fold
window, daily dosing crosses the ceiling on the strength of the schedule alone, before any
uncertainty in the biology is considered.

The superposition is linear, and for intranasal delivery that is the optimistic case rather
than the worst one. Repeated nasal instillation in mice produced **5 to 17-fold higher brain
bioaccumulation factors at low dose than at high dose** (PMID 42296265), i.e. disproportionate
retention rather than proportionality. A model that accumulates linearly will understate it.

The sensitivity ranking changes as a result, which is the test that the parameters are really
wired in: `dose_interval_days` enters at ρ = −0.28, the fifth strongest driver, and
`expression_days` rises from ρ = +0.01, where it was effectively inert, to +0.13.

### 3 · What our own dot blot bounds, and what it does not

The free variable no longer has to wait for LC-MS/MS to be bounded from above. Every lysate
dot sits below the weakest calibrator on the membrane, 1.5 µg of purified His-tagged protein,
so `wetlab_yield_ceiling()` converts that into a ceiling on molecules per transfected cell
per day. Taking the seeded count of 3 × 10⁵ cells, 90 % mEGFP-positive (Table 3 on the
Results page) and 3 days of expression, the ceiling is **6.9 × 10⁷ molecules per cell per
day for each mL of lysate**.

The bound is deliberately generous: it uses the seeded cell count rather than the count after
three days of growth, treats the entire sub-threshold mass as intact tagged precursor, and
ignores harvest losses. It is also **weak**, sitting about 69-fold above the top of the
plausible expression range of 10⁴ to 10⁶ molecules per cell per day, so it excludes nothing
that was plausible to begin with.

It is nonetheless worth having, because the headline conclusion survives it. Reaching an EC50
across bulk CSF requires about 2.8 × 10¹⁴ molecules per cell per day, roughly **3.6 million
times the most generous yield our own data permit**. Result 1 is not a consequence of
pessimistic assumptions about expression; it holds against the ceiling the wet lab sets.

**The blot cannot be read as a quantity, only as a bound.** `dotblot_is_quantitative()`
checks this from the blot's own data and returns false. Doubling the applied volume from 500
to 1000 µL changed the lysate signal by a factor of **0.88**, where a linear response gives
2.0, and the calibrator series spans a 10-fold mass range for a 1.12-fold change in signal.
The readout is saturated, so no mass may be interpolated from it. Loading two volumes was
intended to bracket the detection threshold; what it actually demonstrated is that the
response is flat in load.

**It bounds the intracellular pool only.** The supernatant dots span −6 to +6 grey levels
against a negative control occupying −6 to +5: indistinguishable, so nothing was detected.
That is not a bound on secretion, because the signal peptide is removed on entry to the
secretory pathway and takes the N-terminal tag with it, making correctly exported precursor
invisible to an anti-His antibody by construction. `secretion_is_bounded()` returns
`bounds_secretion: false` for exactly this reason. **`f_cns` remains unmeasured by us.**

### 4 · One parameter moves from assumption toward literature

`f_cns`, the fraction of secreted peptide entering the CNS compartment, was declared an
assumption spanning 0.05 to 0.5 and is the fourth strongest driver. A 2026 nose-to-brain
pharmacokinetic study gives it a reference point: intranasal cannabidiol-loaded nanoparticles
in rats reached **28.5 % brain bioavailability** relative to IV, with **56 % of absorbed drug
entering by the direct nose-to-brain route** and a brain t_max of 10 minutes (PMID 41901301).
That sits inside the assumed range and toward its upper end.

It is a reference point and not a substitution: a lipophilic small molecule in a starch
nanoparticle, dosed into a rat nose, is not a peptide secreted by transfected epithelium.
The range stays as it is, and the source class stays `assumption`, until something closer is
measured.

### References added with this revision

| PMID | why it is cited here |
|---|---|
| 17112570 | SNC80 in rhesus monkeys: the only primate margin available, and the anchor for `tolerated_multiple_of_ec50` |
| 42296265 | repeated nasal instillation gives disproportionate brain accumulation at low dose, so linear superposition is optimistic |
| 41901301 | nose-to-brain PK: 28.5 % brain bioavailability, 56 % by the direct route, a reference point for `f_cns` |
| 37004753 | δ-agonist seizure liability is ligand-specific, not a class effect |
| 25447299 | δ receptors on forebrain GABAergic neurons mediate SNC80 seizures |

*Correction, 22 Nov 2026: `dose_model_result.json` recorded the required yield as exactly
2.73e14 where the midpoint parameters give 2.77e14, and the silencing ceiling as 70.30984
against a recomputed 70.31472. Both are roundings rather than errors, and neither changes a
conclusion, but the file presents as machine output and should be regenerated rather than
edited. The runner that regenerates it is now committed in `dose_model.py` under
`__main__`, which it previously was not.*
