# Safety

> Three safety questions were put to this project, and we answered all three with evidence
> rather than reassurance. One of the answers is uncomfortable for us and is on this page
> anyway.

---

## 1 · Organisms, vectors and containment

| | |
|---|---|
| **Cloning host** | *E. coli* NEB 10-beta, a K-12 derivative. **Risk Group 1** |
| **Expression host** | HEK293T, a human embryonic kidney line. **Risk Group 1**, handled as human-derived material |
| **Backbone** | pcDNA3.1(+), a standard non-integrating mammalian expression vector |
| **Delivery** | **non-viral**. A cationic / ionisable lipoplex co-packaging plasmid DNA and siRNA |

Nothing in this project uses a viral vector, a pathogen, a toxin gene, or any sequence on a
select-agent or export-control list. The payload is a human peptide hormone precursor with
its opioid cassettes recoded; the silencing arm targets a human housekeeping protease.

**The delivery choice is itself a safety decision.** A non-viral lipoplex does not integrate,
can be re-administered, and follows a better-established regulatory route than a viral
vector. It is also the reason the construct must be re-dosed, which is what makes the
anti-PEG question in §3 worth asking at all.

> *To be completed by the wet lab:* institutional biosafety level of the laboratory used,
> the local biosafety committee approval reference, and waste-handling procedure. These are
> facility facts the dry lab cannot supply.

---

## 2 · The payload: does δ-opioid agonism cause seizures?

This was raised against us directly, and it is the right question to ask of an opioid
payload engineered **towards** the δ receptor.

We assessed it across **twelve primary references**, deliberately in three directions: the
convulsant reports and the receptor implicated, whether the liability separates from
analgesia, and what is known about the **endogenous peptide** specifically. We committed in
advance to reporting whichever way the third strand pointed.

**The liability is real and δ-mediated for certain synthetic small molecules.** It is not in
dispute and we do not minimise it.

**It does not hold as a class property of δ agonism.** It is ligand-specific, and compounds
exist that separate analgesia from convulsant activity.

**For peptide enkephalins the evidence points the other way.** Inhibiting enkephalin
degradation, which is precisely what our silencing arm does, has literature associating it
with **reduced** seizure activity rather than increased.

**The decisive precedent is clinical.** A gene-therapy vector expressing preproenkephalin
completed **Phase 1 in chronic cancer pain**, our exact indication, with safety data
published: [`NCT00804076`](https://clinicaltrials.gov/study/NCT00804076) and
[`NCT01291901`](https://clinicaltrials.gov/study/NCT01291901).

### Four gaps we will not omit

1. That vector expressed the **native** precursor. Ours is engineered, with every opioid
   cassette recoded.
2. It was delivered **peripherally**. Ours is intranasal, nose-to-brain.
3. Phase 1 establishes tolerability at the doses tested, not absence of a rare event.
4. Our own selectivity estimate's interval **includes zero**, so we cannot claim the δ bias
   that the safety argument for δ over μ depends on. δ-preference is a design goal.

Full assessment with all twelve references:
[`DELTA_SEIZURE_SAFETY.md`](../DELTA_SEIZURE_SAFETY.md).

---

## 3 · The carrier: anti-PEG immunogenicity

A PEGylated carrier intended for **repeat dosing** raises accelerated blood clearance, where
anti-PEG antibodies clear the second dose faster than the first.

**One actionable finding.** Pre-existing anti-PEG IgM binding is modulated by the PEG
**terminus**, and the hydroxyl-terminated form evades it better than the methoxy form our
lipid carries. Substituting hydroxyl-terminated PEG2000-DMG is a **single-reagent change**:
same lipid, same anchor, same 1.5 mol%, same protocol.

**One thing we expected to find and did not.** We looked for evidence that the intranasal
route escapes accelerated clearance, since that phenomenon is characterised with repeated
**intravenous** dosing. Pairing the concept with intranasal, nose-to-brain and mucosal
delivery returned no evidence either way. It is recorded as an **open question, not a
reassurance.** Putting "intranasal avoids this" on a safety page would not survive a
follow-up question.

**And shedding is a mitigation, not an exemption.** The C14 anchor sheds faster than longer
alternatives, but accelerated clearance has been reported without the expected antibody
elevation.

Full assessment: [`ANTI_PEG_ASSESSMENT.md`](../10_immunogenicity_antibody/ANTI_PEG_ASSESSMENT.md).

---

## 4 · The product: is the engineered peptide more immunogenic?

The construct replaces a human epitope with an engineered one, so we screened MHC class I
presentation across **6,120 allele-peptide pairs**.

| epitope group | strong binders |
|---|---|
| native | 1.77 % |
| **engineered payload** | **1.86 %** |
| P2A remnant junction | **2.07 %** |

**The engineered epitope is not meaningfully more immunogenic than the one it replaces.**
The P2A junction ranks highest of the three, which is a concrete argument for the IRES
cassettes if immunogenicity of a persistently expressed product matters.

**This is a screen, not a clearance.** Class I prediction speaks to CD8 recognition of an
intracellular product and says nothing about antibody responses to a secreted peptide.

---

## 5 · What remains unresolved

Stated plainly, because a safety page that lists only solved problems is not a safety page.

- **The δ bias is not demonstrated.** The safety case for δ over μ rests on a preference our
  own interval does not establish. The cAMP assay settles it.
- **Whether the intranasal route changes the anti-PEG picture** is unknown, not favourable.
- **No bench data exists yet.** Everything here is literature assessment and prediction. The
  constructs have been ordered; nothing has been expressed, purified or dosed.
- **No antibody detects the engineered product**, so a custom polyclonal is on the critical
  path and the maturation readout is LC-MS/MS rather than ELISA.
