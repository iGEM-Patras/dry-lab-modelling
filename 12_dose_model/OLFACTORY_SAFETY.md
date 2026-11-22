# The olfactory epithelium is a tissue at risk, not just a delivery barrier

**Status: a gap in our own work, found 22 Nov 2026 and not yet closed by any experiment.**

Across the whole repository and the whole wiki there are **zero** occurrences of *anosmia*,
*smell*, *ciliotoxicity*, *nasal toxicity*, *epithelial damage* or any in vitro nasal model.
The words *cilia* and *mucociliary* appear only inside the dose model, and only as a
**competitor for uptake** — something that removes our formulation before it can transfect.
The epithelium is treated throughout as an obstacle to get past. It is also the tissue the
patient has to keep.

That asymmetry is the finding. What follows is the arithmetic that makes it urgent, the
reason the obvious fix makes it worse, and the one assay that would settle it.

---

## 1 · The arithmetic nobody ran

Take the formulation as specified in `04_lipoplex_md/targeting/lipoplex_formulation_spec.csv`:
**635 µg of DOTAP per 100 µg of nucleic acid** for formulation A, and **1,167 µg of
DLin-MC3-DMA per 100 µg** for B1. A 100 µg plasmid dose therefore carries 0.6–1.2 mg of
cationic lipid into the nose.

Suppose 1.8–5.3 % of it reaches the olfactory region — the range actually measured by
computational and SPECT/CT studies of human nasal casts, and reassuringly close to the
`f_olf` range of 0.5–5 % the dose model already assumed. The olfactory epithelium is
**2–10 cm²**, and it is covered by a mucus and periciliary film roughly **10 µm** deep,
which is **1 µL per cm²**.

A thin film over a small area is the problem. The deposited lipid does not dilute into a
compartment; it sits in a microlitre.

| | DOTAP lipoplex | MC3 LNP |
|---|---|---|
| local concentration in the mucus film | **159 – 15,876 µg/mL** | **292 – 29,186 µg/mL** |

Cationic nanoparticles produce dose-dependent viability loss in airway epithelial cells
across **3–200 µg/mL** (PMID 33407567). **Our most optimistic case sits at the top of that
range, and our most effective case sits 80–146-fold above it.**

This is an order-of-magnitude argument, not a prediction, and it rests on assumptions that
should be attacked: a different particle chemistry, submerged culture rather than an
air-liquid interface, mucus that binds cationic material and may be protective, and
mucociliary clearance that removes a fraction before it acts. Each of those could move the
number. **None of them has been checked, and the direction of the gap is not comfortable.**

## 2 · Why the obvious fix makes it worse

The instinct, on reading that only a few percent of the dose reaches the olfactory region,
is to build a better device. The dose model agrees: `f_olf` is its third-strongest driver.

But `f_olf` scales efficacy and local toxicity **by exactly the same factor**. Every
improvement in targeting concentrates a cationic lipid more tightly onto the one epithelium
whose damage is hardest to reverse. Panel (a) of `olfactory_safety.png` is a single family
of parallel lines for this reason: there is no combination of plasmid dose, deposited
fraction and epithelial area in the plausible ranges that reaches good olfactory delivery
while staying below the in vitro cytotoxic band.

**Targeting is not free, and we have been treating it as free.** If the device work succeeds,
the formulation work has to succeed first.

## 3 · The dose is not reproducible, and that feeds the abuse problem

Olfactory deposition depends on which nostril is open. Across 32 reconstructed human nasal
airways, median olfactory deposition on the less-patent side was **1.82 % (mild cycling),
4.89 % (mid) and 5.32 % (extreme)** — a **2.9-fold** spread, and the two sides of one nose
differ again within each class (PMID 41093085).

The nasal cycle turns over on a timescale of hours. **A patient spraying the same dose at
the same time each day receives a materially different olfactory dose from one day to the
next, and has no way to know it.** On a low day the relief is weaker, and the documented
response to weak relief is to spray again — the exact escalation path modelled in
`ABUSE_DETERRENCE.md`. Delivery variability and abuse liability are the same problem seen
from two ends.

## 4 · "A way to inhale the dose"

There is one, and it is not a conventional spray.

- **Breath-powered bidirectional delivery** raised deposition in both the nasal cavity and
  the olfactory region relative to normal breathing, for both vibrating-mesh and jet
  nebulisers, with the vibrating mesh more responsive to the bidirectional pattern
  (PMID 27977306). Closing the soft palate stops the aerosol going to the lung and routes it
  over the olfactory cleft.
- **Administration plane and particle size are the dominant determinants** of olfactory
  cleft deposition under natural inhalation, while administration angle matters little —
  from 108 simulated conditions on a model built from 32 adult CT scans and validated by
  SPECT/CT in a 3D-printed nose (PMID 42249898). Plane and particle size are formulation and
  device parameters we can actually set.
- **Accessibility is anatomical and varies between people** (PMID 41149823), which argues
  for a device that tolerates variation rather than a protocol that assumes an average nose.

None of this is in our device thinking, and the entrepreneurship page describes a
conventional metered spray. **A conventional spray is the one delivery mode this literature
consistently shows is poor at reaching the olfactory cleft.**

## 5 · We are characterising the wrong formulation parameter

`lipoplex_charge_ratio_titration.csv` sweeps charge ratio, and the MD work reports zeta
potential. For toxicity, **surface charge density is a better predictor than zeta
potential**: five cationic nanoparticles matched for zeta potential (+20.6 to +26.9 mV) but
differing in electrokinetic charge (0.23 to 4.39 µmol/g) produced high, slight or no
viability loss in rank order of charge density, not of zeta (PMID 33407567).

Two particles that look identical on our current readout can differ completely in toxicity.
**The charge-ratio titration should be reported as charge density per unit mass, which is
computable from the data already in the spec file**, not only as a ratio and a zeta value.

## 6 · The assay that settles it, and why acute testing will not

Repeated dosing is the regime that matters, and it is not predicted by a single exposure.
Using reconstituted 3D human nasal epithelium (MucilAir) dosed **daily for two weeks**,
marketed nasal sprays at **clinically relevant doses** produced dose- and time-dependent
*cumulative* loss of ciliary beat frequency plus ultrastructural damage (PMID 34834166).
An approved product, used as directed, measurably injures the epithelium over two weeks.

So the protocol is established and the readouts are standard:

1. **Ciliary beat frequency** on a reconstituted 3D nasal epithelium, dosed daily for 14
   days at the intended clinical concentration, against vehicle and untreated controls.
2. **Barrier integrity** (TEER) and **cytotoxicity** (LDH release) on the same cultures.
3. **Both formulations**, DOTAP and MC3, since the ionizable lipid is only cationic at
   endosomal pH and should be gentler at the neutral surface — a prediction worth testing
   rather than assuming.

This is a bought-in model and a two-week run. It is the cheapest decisive safety experiment
available to the project, and it needs no animals.

## 7 · Why this matters more for our patients than for most

The indication is cancer pain. **Anosmia costs appetite**, because flavour is mostly
olfaction, and weight loss in advanced cancer is already a major driver of decline. A
therapy that controls pain while accelerating cachexia is not obviously a good trade, and
it is not a trade anyone in the project has so far been asked to make, because the
possibility was never written down.

Olfactory neurons regenerate from basal cells, so a single injury is often recoverable.
**Repeated injury on a daily schedule is the condition under which that regenerative
capacity fails**, and daily dosing is exactly what the dose model predicts will be needed.

---

## What I would add to the project

1. The 14-day MucilAir ciliary-beat and barrier study, on both formulations. Decisive, no
   animals, two weeks.
2. Report charge density, not only charge ratio and zeta potential.
3. State the local exposure arithmetic on the Safety page, with its assumptions, as an open
   risk rather than a solved one.
4. Treat smell as an outcome measure. If this ever reaches a patient, olfactory testing
   belongs in the protocol from the first dose.
5. Stop describing improved olfactory targeting as purely a benefit.

## References

| PMID | used for |
|---|---|
| 33407567 | surface charge density predicts cationic nanoparticle toxicity better than zeta potential; 3–200 µg/mL cytotoxic range in airway epithelium |
| 34834166 | repeated daily dosing of marketed nasal sprays on 3D human nasal epithelium gives cumulative ciliotoxicity |
| 41093085 | nasal cycling changes olfactory deposition 1.82–5.32 % between cycling classes |
| 27977306 | bidirectional breath-powered delivery raises olfactory deposition for both nebuliser types |
| 42249898 | administration plane and particle size are the primary determinants of olfactory cleft deposition |
| 41149823 | olfactory region accessibility varies anatomically between individuals |
| 30912321 | intranasal drugs alter human mucociliary clearance and ciliary beat frequency |
| 32664676 | cytotoxicity and uptake of cationic carriers in a nasal delivery context |

Full citations with links: [`REFERENCES.md`](REFERENCES.md).


---

## 8 · Added 22 Nov: charge density computed, and a correction to section 6

Section 5 said charge density should be reported instead of zeta potential, and that it was
computable from `lipoplex_formulation_spec.csv`. It is, and the result corrects something
section 6 of this document got wrong.

Cationic charge per gram of total lipid, from the formal charges and the ionizable lipid's
pKa of 6.44 already recorded in the spec file. Data: `charge_density_vs_pH.csv`. Figure:
`charge_density_pH.png`.

| pH at the particle surface | DOTAP lipoplex | MC3 LNP + PEG | MC3 LNP (clinical) |
|---|---|---|---|
| 7.4 (plasma) | 756 | **74** | 84 |
| 7.0 | 756 | 161 | 184 |
| 6.44 (the lipid's pKa) | 756 | 372 | 426 |
| 6.0 | 756 | 546 | 625 |
| 5.5 | 756 | **668** | 765 |

*µmol of cationic charge per g of lipid. DOTAP is a permanent quaternary ammonium, so its
value does not move with pH; MC3 follows Henderson–Hasselbalch at pKa 6.44.*

**Section 6 of this document predicted that the ionizable lipid "should be gentler at the
neutral surface". That prediction holds only at pH 7.4, and the nasal surface is not pH 7.4.**
MC3's ten-fold charge advantage over DOTAP at plasma pH falls to **1.1-fold at pH 5.5** — the
two formulations become equivalent in cationic charge density.

This matters specifically for us because of *where* the formulation is meant to land. In 62
healthy adults, pH measured **within the olfactory cleft was significantly lower than over
the respiratory mucosa**, and olfactory-cleft pH correlated with odour identification score,
explaining 18 % of its variance (PMID 40346891). **The one region of the nose this therapy
is designed to reach is the more acidic one**, which is the condition under which the
ionizable lipid behaves most like a permanently cationic one.

Two consequences worth acting on.

**The MD rationale needs re-examining.** The lipoplex simulations are built around a protonated
and a neutral MC3 state, with the neutral state representing the extracellular surface and the
protonated state the endosome. If the delivery surface is appreciably below pH 6.44, the
neutral state is not the right model of the surface, and the pH switch the simulations were
designed to demonstrate is partly operating before the particle is taken up at all. This does
not invalidate the simulations; it changes which of the two states is the relevant surface
model, and that should be checked before any of the MD work is cited as evidence of surface
behaviour.

**The pKa should be measured, not assumed.** The 6.44 figure is the lipid's, not the
formulated particle's. Apparent pKa of an LNP shifts with the nucleic-acid cargo — 0.1 to 0.5
pH units with RNA size, and 0.15 units between same-length siRNA and miRNA, with the direction
depending on the ionizable lipid (PMID 42615507). Our cargo is a ~6 kb plasmid, far outside
the range tested. The standard measurement is a **TNS fluorescence titration**, which needs a
plate reader and a dye, and is among the cheapest experiments on any list in this repository.

**And the real surface pH should be measured too.** Nasal pH is measurable with a probe
(the study above used an oesophageal/airway pH catheter) and varies between the olfactory
cleft and the respiratory mucosa. Taking a literature value for the nose as a whole would
repeat the error this section is correcting.

| PMID | used for |
|---|---|
| 40346891 | olfactory-cleft pH is significantly lower than respiratory-mucosa pH, and correlates with odour identification |
| 42615507 | apparent pKa of an LNP shifts with nucleic-acid cargo, so the lipid's pKa is not the particle's |
