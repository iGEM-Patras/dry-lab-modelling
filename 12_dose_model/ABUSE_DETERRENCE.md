# Limiting the maximal dose: four layers, ranked by what they actually bound

**Raised at the 2026 judging session:** patients in pain will spray more than the label
allows, and the product remains an opioid however closely the payload resembles an
endogenous one. This document answers that with specific parts, specific numbers, and the
cheapest experiment that discriminates between them.

Code: `data/abuse_resistance.py`. Figure: `abuse_resistance.png`. Ceiling, accumulation and
EC50 all come from `data/dose_model.py`; nothing here re-derives them.

---

## 0 · First, what kind of abuse this is

The reinforcing property of an opioid tracks the **rate of rise** of receptor occupancy, not
the peak. Insufflated heroin reinforces because brain concentration climbs in seconds. A
DNA-encoded peptide cannot do that: the plasmid must be taken up, transcribed, translated,
processed by PC2/CPE and secreted, so exposure climbs over hours and plateaus over days.
**The euphoric spike that drives recreational use is absent by construction.**

What is *not* absent is dose escalation by a patient whose pain is not controlled, spraying
again because the last one did not work. That is the realistic failure mode, it is a
foreseeable use rather than misuse, and our own model says it is dangerous: at midpoint the
therapeutic window is 6.5-fold and **daily dosing already accumulates 8.5-fold**. The
schedule alone can cross the ceiling, before anyone misuses anything.

It is also worth saying plainly that the payload is not strongly δ-selective on our own
calibrated estimate, so μ activity is present and μ is the receptor that carries reward and
respiratory depression. We should not argue that the peptide is safe because it is
"natural". Met-enkephalin is natural and it is an opioid agonist.

**For an acute overdose the answer is not a genetic circuit.** Naloxone acts in minutes;
any transcriptional limiter acts in hours. Every design below is a *chronic exposure
limiter*, and presenting one as an antidote would be wrong.

---

## 1 · What each limiter can and cannot bound

This is the part that decides the choice, and it follows from the model rather than from
preference.

Accumulation has two sources. Spraying more puts **more plasmid into each cell** the
formulation reaches, and it **reaches more cells**. A limiter that senses plasmid copy
number clamps the first and is blind to the second. A limiter that senses the peptide
clamps both, because the peptide is shared across the tissue regardless of which cell made
it. Neither dominates; they fail in different directions, which is why layering them
multiplies.

| architecture | 3 sprays/day | 6/day | 12/day | crosses 6.5 × EC50 at |
|---|---|---|---|---|
| open loop (what we built) | 3.00× | 6.00× | 12.00× | **6.5 sprays/day** |
| product feedback (CRE promoter), h = 2 | 2.64× | 4.28× | 6.32× | 12.7 sprays/day |
| copy-number clamp (miRNA IFFL) | 1.73× | 2.45× | 3.46× | 42.2 sprays/day |
| both layers | 1.66× | 2.24× | 2.94× | **161 sprays/day** |

Six sprays a day is reachable by a determined patient. A hundred and sixty is not, and a
metered device with an actuation counter closes the remainder.

**No layer gives a hard cap.** Negative feedback compresses; it does not saturate. A
first-order loop reaches the ceiling at 11 sprays a day and a cooperative one at 13, so
cooperativity buys surprisingly little. Anyone claiming a circuit makes overdose impossible
has not solved the equation.

---

## 2 · The four layers

### Layer 1 · Product-sensing feedback — swap the promoter, add no parts

**What:** replace the CMV promoter in pcDNA3.1(+) with the human *PENK* proximal promoter,
or with a synthetic 4×CRE–minimal promoter.

**Why it closes:** δ and μ receptors are Gi-coupled, so agonist occupancy lowers adenylyl
cyclase activity, lowers cAMP, lowers CREB phosphorylation and lowers transcription from a
CRE. Proenkephalin transcription is natively CREB-dependent (PMID 7724644), and enkephalin
biosynthesis is transcriptionally coupled to secretory activity through transcription of the
*PENK* gene itself (PMID 1364196). **This is native regulation restored, not a circuit
invented for the purpose.** The CMV promoter is what throws it away: we replaced a
feedback-regulated promoter with a constitutive viral one and inherited an open loop.

**Cost:** one promoter swap. No new coding sequence, no change to the payload, no change to
the four architectures already built.

**The catch, stated because it decides feasibility:** the loop closes only if the
*producing* cell senses the peptide, which requires it to express an opioid receptor.
Either co-deliver OPRD1 on the same plasmid, which costs ~1.1 kb of cargo and makes the
construct a two-gene device, or accept that the loop reports on something else.

I tried to settle this from the expression atlases and **it cannot be settled that way.**
Querying OPRD1 (ENSG00000116329) baseline expression in Open Targets returns records from
GTEx and Tabula Sapiens only, and **neither samples olfactory epithelium**: across every
record retrieved there are *zero* nasal, olfactory, airway, bronchial or tracheal rows. The
highest values sit in pancreatic islet cell types and pituitary. So the honest status is not
"olfactory epithelium does not express OPRD1" but "the standard atlases do not look there".

Settling it needs either a published nasal/olfactory single-cell dataset or an RT-PCR on
primary nasal epithelial cells, which is a cheap bench experiment and a better use of a week
than cloning a promoter whose feedback may never close.

### Layer 2 · Copy-number clamp — the direct answer to over-spraying

**What:** a single-transcript microRNA incoherent feedforward loop. The payload transcript
carries a synthetic miRNA in an intron and that miRNA's target sites in its own 3′ UTR, so
more plasmid in a cell makes more repressor in the same cell and per-cell output is held in
a narrow window.

**Why this one:** ComMAND (PMID 40300600) is exactly this architecture, is single-transcript
rather than two-gene, works at low copy number where two-gene versions fail, and was shown
to hold clinically relevant transgenes inside a narrow window in primary human T cells, rat
neurons and iPSCs. Dosage-controlled transgene expression is an established requirement in
gene therapy for dosage-sensitive cargoes (PMID 42646356); this is the same problem.

**Cost:** one cloning step into the 3′ UTR plus an intronic miRNA. It is compatible with
every architecture we have, because it does not touch the PENK or mEGFP coding sequences.

**Limit:** clamps per-cell output against copy number, not the number of cells recruited.
It is the better answer to a single large over-spray and the weaker answer to escalation
over days.

### Layer 3 · Prescriber-controlled switch — the only hard cap

**What:** make expression conditional on a companion small molecule. Either a Tet-On
promoter requiring doxycycline, or a destabilizing domain fused to the precursor requiring
its stabilising ligand (the ecDHFR/trimethoprim system is reviewed in PMID 42262317).

**Why it is different in kind:** every other layer leaves the patient in control of exposure.
This one moves the rate-limiting resource outside the patient, to a cheap, non-euphoric,
prescribed tablet. Spraying the whole bottle achieves nothing without it. It is also the
only option that answers the "silence it indefinitely" half of the question: withdrawing
the stabiliser clears a destabilising-domain fusion in hours.

**Cost:** a second regulatory element, a second drug in the regimen, and the honest downside
that a patient who cannot access the tablet loses analgesia. That is a human-practices
question, not a modelling one, and it should be put to the same clinicians already consulted.

### Layer 4 · A pharmacological ceiling — re-engineer the payload

**What:** design the payload for **low intrinsic efficacy** rather than high affinity.

**Why:** a partial agonist has a maximum attainable effect set by efficacy, not by
concentration. This is the buprenorphine principle, and it is the only ceiling that holds
when every circuit has failed, the plasmid has over-expressed and the patient has sprayed
the bottle. It also engages the δ-seizure literature directly: convulsant activity tracks
*high-efficacy* δ agonists, and efficacy requirements differ between antihyperalgesia and
convulsion (see `DELTA_SEIZURE_SAFETY.md`).

**Cost:** this is a payload redesign, so it invalidates the cycle-7 calibration and needs
the cAMP functional assay that is already specified but not yet run. It is the most
expensive option and the most durable one.

---

## 3 · The experiment that decides it, on one plate

The table above rests on one assumed number: `COPY_SHARE`, the share of escalation arriving
as extra plasmid copies per cell rather than as newly transfected cells. It is set to 0.5
and it is the difference between a clamp that buys 42 sprays a day and one that buys far
fewer. **It is measurable with the protocol already run in September.**

Transfect HEK293T in 6-well format, Lipofectamine 3000, seeded at 3 × 10⁵ per well exactly
as before, with a plasmid dose ladder — 0.25, 0.5, 1, 2, 4 µg per well — of
`mEGFP-P2A-His-PENK`, the architecture that gave ~90 % positive cells. At 48 h score two
quantities separately by fluorescence microscopy:

1. the **proportion** of mEGFP-positive cells — this is the cells-recruited axis;
2. the **mean intensity of positive cells** — this is the per-cell-output axis.

`COPY_SHARE` is the slope of log(intensity) against log(dose) divided by the slope of
log(total signal) against log(dose). An open-loop construct gives a per-cell slope near 1;
a working clamp gives a slope near 0. **The same plate, run on a clamped construct, is the
assay that demonstrates the clamp works** — one figure, one plate, no new readout, no new
equipment.

This is the cheapest decisive experiment available to us, and it uses the one protocol the
team has already executed successfully.

---

## 4 · What I would do, in order

1. **Establish whether olfactory epithelium expresses OPRD1.** Not from GTEx or Tabula
   Sapiens — I checked, and neither samples the tissue. It needs a nasal single-cell dataset
   or an RT-PCR. It decides whether Layer 1 is a promoter swap or a two-gene device, so it
   gates the cheapest option on the list.
2. **Run the dose ladder** on the existing `mEGFP-P2A-His-PENK` construct. It measures
   `COPY_SHARE`, costs one plate, and makes the table above empirical instead of assumed.
3. **Build the miRNA clamp**, because it is one cloning step, it is architecture-agnostic,
   and it has the largest effect per unit of work.
4. **Put Layer 3 to the clinicians** before building it. The engineering is easy and the
   human-practices question is not.
5. **Treat Layer 4 as the next project**, not this one.

Layers 1 to 3 are all compatible with each other and with the v6 engineered constructs,
which have not yet been transfected. Nothing here requires abandoning what was built.

---

## References

| PMID | used for |
|---|---|
| 7724644 | proenkephalin transcription is CREB-dependent — the basis of Layer 1 |
| 1364196 | enkephalin biosynthesis is transcriptionally coupled to secretory activity |
| 40300600 | ComMAND: single-transcript miRNA IFFL holding transgene output in a narrow window |
| 42646356 | dosage-controlled transgene expression as a gene-therapy safety requirement |
| 42262317 | destabilizing-domain systems for small-molecule control of protein level |
| 17112570 | the 3–10× margin that sets the ceiling these designs are measured against |
| 37004753 | δ-agonist seizure liability is efficacy- and ligand-dependent — the basis of Layer 4 |
