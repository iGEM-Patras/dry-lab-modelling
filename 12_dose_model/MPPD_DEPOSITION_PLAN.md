# MPPD and the cheap deposition work: what it answers, what it cannot

**22 Nov 2026.** Written because the budget is the binding constraint. Everything here is
free software or a 3D print, and together it covers most of the deposition and local-dose
questions raised in `OLFACTORY_SAFETY.md` without a single animal or a bought assay.

---

## 1 · MPPD is the right tool for a question we have not been asking

The Multiple-Path Particle Dosimetry model (MPPD v3.04 from ARA, and the EPA MPPD v2.0 2025
build) is free, mechanistic, and accepted in regulatory inhalation risk assessment. It
calculates deposition and clearance of monodisperse and polydisperse aerosols in human
adults, children, rats and mice, for particles from **0.01 to 20 µm**, with output by
region, by lobe, by airway generation and as **surface dose in µg/cm²**.

That last output is the one we need, and the question it answers is **lung spillover**: of a
nebulised dose aimed at the nose, how much escapes to the tracheobronchial and pulmonary
regions, and at what surface concentration? We have never asked this. The project has
reasoned about the nose and about the brain, and treated everything in between as absent.
A cationic lipid reaching the deep lung is a different toxicology from a cationic lipid on
the nasal mucosa, and it is one with a large literature we have not touched.

The workflow is established. An inhaled-LNP development programme ran exactly this: MPPD
v3.04 with Yeh/Schum, Weibel and PNNL morphometries for a vibrating-mesh nebuliser at
**MMAD 4.93 µm**, found deposition ordered head > tracheobronchial > pulmonary, and compared
the predicted surface dose against an in vitro ciliary-function threshold expressed in
**µg/cm² per administration**. That is precisely the bridge we need between a dose and the
MucilAir ciliotoxicity numbers.

## 2 · What MPPD cannot do, stated plainly

**It does not resolve the olfactory cleft.** In MPPD the head — nose and mouth — is handled
by **empirical filtration efficiency functions**, not by a geometry. It returns one
extrathoracic number. There is no olfactory compartment, so MPPD cannot produce `f_olf`, and
any claim that it validated our olfactory targeting would be wrong. `f_olf` has to come from
CFD on segmented CT geometry or from a physical cast, which is what the papers cited in
`OLFACTORY_SAFETY.md` did.

**Its size range excludes our current device.** MPPD covers 0.01–20 µm. A conventional
metered nasal spray produces droplets of roughly 30–100 µm, **above the model's range**. A
vibrating-mesh nebuliser at 2–5 µm sits comfortably inside it.

So MPPD is usable *precisely if* we adopt the nebulised, breath-powered bidirectional route
that the deposition literature already favours, and not for the metered spray currently
described on the entrepreneurship page. The tool choice and the device choice are the same
decision.

## 3 · The run plan

Free, one afternoon, no consumables.

1. **Model**: human adult, nasal breathing. Run both the symmetric Yeh/Schum and the
   stochastic/asymmetric lung so the spread between morphometries is visible — in the
   worked example above those differed by 20 % vs 30 % deposition in the same region, which
   is the right order for an honest error bar.
2. **Aerosol**: sweep MMAD from 1 to 10 µm at a realistic GSD (1.5–2.2), covering vibrating
   mesh and jet nebulisers. Density from the formulation rather than 1 g/cm³.
3. **Breathing**: tidal volume and frequency for a seated adult, plus a reduced-flow case,
   since a patient in pain will not breathe like a healthy volunteer.
4. **Exposure**: the aerosol concentration implied by our own spec — 635 µg DOTAP or 1,167 µg
   MC3 per 100 µg nucleic acid — rather than a generic unit dose.
5. **Extract**: regional deposition fraction (head / TB / pulmonary) and **surface dose in
   µg/cm²** per administration, per region and per generation.

**The deliverable is one figure**: surface dose in µg/cm² against MMAD, for head, TB and
pulmonary, with the in vitro cytotoxic band drawn across it. That figure answers "which
droplet size keeps the dose in the nose and out of the lung", and it is the same axis as the
local-exposure calculation already in `OLFACTORY_SAFETY.md`.

## 4 · The cheap physical complement for the part MPPD misses

**A sectioned 3D-printed nasal cast.** A recent build segments a CT-derived human nasal
cavity into five regions — vestibule, **olfactory area**, middle and upper turbinates, lower
turbinate, nasopharynx — printed in polypropylene for chemical compatibility with a fixation
frame for airtight reassembly, and quantifies regional deposition by HPLC after automated
actuation (PMID 41751226). A university 3D printer and a fluorescent tracer replace the HPLC
step at essentially no cost. **This measures `f_olf` for our actual device**, which is the
single most valuable missing number and the model's third-strongest driver.

**And one experiment that costs almost nothing and may matter more than either.** In a 2026
preprint — *not peer reviewed, treat accordingly* — a mechanical nasal spray pump was run at
three spring compression forces (4.8, 8.0, 11.2 N) and actuation speeds of 80–180 mm/s with
mRNA-LNPs. Higher compression force shifted deposition toward the **superior turbinate**,
higher actuation speed toward the middle turbinate — and **LNP encapsulation efficiency fell
significantly after actuation** (doi:10.21203/rs.3.rs-11037329/v1).

If that holds for lipoplexes, **the act of spraying partly destroys the carrier**, and every
efficacy number we have assumes it does not. Testing it needs a DLS run and a dye-exclusion
or PicoGreen assay on the formulation before and after actuation through the device. That is
an afternoon with equipment the lab already uses, and it is a prerequisite for the device
work rather than a refinement of it.

## 5 · One number worth re-examining, because it may help us

The local-exposure calculation in `OLFACTORY_SAFETY.md` divides by an olfactory epithelial
area of 2–10 cm², taken from the dose model's own parameter note. CFD studies on segmented
CT geometry put the olfactory region at **7–10 % of total nasal cavity area** (PMID 38931844).
Local concentration scales **inversely** with that area, so if the true figure sits at the
upper end, the exposure estimate falls proportionally.

This is the parameter most worth pinning down, and it is the one that could move the
conclusion in our favour. It should be measured on the cast rather than argued about.

## 6 · Order of work, cheapest first

1. **Actuation-integrity test** — does our device break the lipoplex? Afternoon, existing kit.
2. **MPPD lung-spillover runs** — free software, one afternoon, gives µg/cm² by region.
3. **3D-printed sectioned cast** — measures `f_olf` and olfactory area for our device.
4. **MucilAir 14-day ciliotoxicity** — the one item with a real price tag, and the decisive
   safety experiment.

Steps 1 to 3 cost essentially nothing and between them close the deposition side. Step 4 is
the one to seek funding for, and the first three make the case for it.

## References

| source | used for |
|---|---|
| ARA MPPD v3.04 / EPA MPPD v2.0 (2025) | free dosimetry model; 0.01–20 µm; regional and µg/cm² output; head handled by empirical filtration functions |
| PMID 41751226 | sectioned 3D-printed nasal cast with a discrete olfactory region |
| PMID 38931844 | CFD of micron particle deposition in adult and paediatric olfactory regions; olfactory region is 7–10 % of nasal cavity area |
| PMID 42346986 | multiscale modelling of olfactory and alveolar deposition |
| doi:10.21203/rs.3.rs-11037329/v1 | **preprint**: actuation force and speed change regional deposition and reduce LNP encapsulation efficiency |

Full citations with links: [`REFERENCES.md`](REFERENCES.md).
