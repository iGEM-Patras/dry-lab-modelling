# Safety: the pharmacology of the payload

**Written to slot into the existing Safety page, after *Patient Safety*.**

Our Safety page already covers the laboratory: the two chassis and why each is handled as it
is, the reagents, cobalt(II) chloride, environmental containment, and a bow-tie analysis of
losing containment of HEK293T material. It also covers patient safety as a question of the
delivery interface, where a dosing error is the realistic hazard.

What it does not yet cover is the safety of the molecule itself. Three questions were put to
us about the payload and the carrier, and we answered all three with evidence. One of the
answers is uncomfortable for us, and it is here anyway.

---

## Does δ-opioid agonism cause seizures?

This was raised against us directly, and it is the right question to ask of a payload
engineered towards the δ receptor. We went to the primary literature rather than to review
summaries, and we deliberately looked in three directions: the convulsant reports and which
receptor they implicate, whether the liability separates from analgesia, and what is known
about the endogenous peptide specifically. We committed to reporting what the third strand
showed before we knew what it would show.

The liability is real for certain synthetic δ agonists, and it is genuinely δ-receptor
mediated. We are not minimising that. What the literature does not support is treating it as
a property of δ agonism as such: it is ligand-specific, and compounds exist in which the
convulsant activity and the analgesia come apart. For the peptide enkephalins the evidence
points the other way again, and inhibiting enkephalin degradation, which is precisely what
our silencing arm does, has been associated with reduced rather than increased seizure
activity.

The evidence that settles it for us is clinical rather than preclinical. A gene therapy
expressing preproenkephalin has completed Phase 1 in chronic cancer pain, which is our exact
indication, with safety data published (NCT00804076 and NCT01291901). A payload of this class
has been given to patients in this disease, and the trial read out.

We would rather state the gaps in that argument ourselves than have them found. That vector
expressed the native precursor, where ours is engineered with every opioid cassette recoded.
It was delivered peripherally, where ours is intranasal. A Phase 1 establishes tolerability
at the doses tested and cannot exclude a rare event. And our own computational estimate of
δ-preference has a confidence interval that includes zero, so the δ bias on which the safety
argument for δ over μ depends is a design goal rather than a demonstrated result. The cAMP
assay is what will settle that, and it has not run yet.

## Will antibodies against the carrier clear a repeat dose?

Our formulation is PEGylated and the therapy is intended for repeat dosing, which raises
accelerated blood clearance: antibodies raised against PEG by the first dose clear the
second one faster.

One finding here is directly actionable. Pre-existing anti-PEG IgM binding depends on how the
PEG chain terminates, and the hydroxyl-terminated form is bound less than the methoxy form
our current lipid carries. Substituting hydroxyl-terminated PEG2000-DMG would be a change of
one reagent: the same lipid, the same anchor, the same molar fraction, the same protocol.

There is also something we expected to find and did not. Accelerated clearance is
characterised with repeated intravenous dosing, where the particles reach the spleen and
prime a B-cell response, and our route is intranasal. We looked for evidence that the
intranasal route escapes the phenomenon and found none in either direction. It is plausible
that limited systemic exposure reduces priming; it is equally plausible that
nasal-associated lymphoid tissue provides its own. We are recording this as an open question
and not as a reassurance, because writing "intranasal avoids this" would be a claim we cannot
support. Nor is the faster shedding of our C14 anchor an exemption, since accelerated
clearance has been reported without the expected rise in antibody titre.

## Is the engineered peptide more immunogenic than the one it replaces?

Our construct replaces a human epitope with an engineered one, so we screened MHC class I
presentation across 6,120 allele-peptide pairs. The engineered payload gives 1.86 % strong
binders against 1.77 % for the native epitope it replaces, which is not a meaningful
increase. The highest of the three groups we tested was the P2A remnant junction at 2.07 %,
which is a concrete argument in favour of the IRES constructs if immunogenicity of a
persistently expressed product turns out to matter.

This is a screen and not a clearance, and the distinction is worth stating plainly. Class I
prediction speaks to CD8 recognition of a product presented from inside the cell. It says
nothing about an antibody response to a peptide that has been secreted, which is a different
mechanism and would need a different experiment.

## What we have not resolved

A safety section that lists only the questions it managed to answer is not doing its job.

The δ bias is not demonstrated, and the safety case for preferring δ over μ rests on it.
Whether the intranasal route changes the anti-PEG picture is unknown rather than favourable.
No commercial antibody detects our engineered product, so a custom polyclonal sits on the
critical path and the maturation readout is LC-MS/MS rather than ELISA. And none of this has
been to the bench yet: the constructs have been designed and ordered, and nothing has been
expressed, purified or dosed.
