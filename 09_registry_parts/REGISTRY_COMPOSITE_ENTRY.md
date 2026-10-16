# Registry entry, composite part, Type: **Design**

**Paste everything below the line into the editor box. Markdown only, no HTML.**
**Title:** `Bicistronic engineered proenkephalin with IRES-driven mEGFP reporter`
**Affiliation:** Patras UPAT (2026)
**Complementary basic part:** `BBa_26J864WV`

---

## Overview

This composite part expresses two proteins from one transcript. The first cistron is our
engineered proenkephalin coding sequence, which carries seven copies of the payload peptide
in place of the native opioid cassettes. The second is mEGFP, translated from an
encephalomyocarditis virus internal ribosome entry site, which reports that the transcript
reached a cell and was translated.

The part is 2,164 bp and is organised as follows.

| component | position | length | source |
|---|---|---|---|
| Kozak consensus | 1 to 6 | 6 bp | GCCACC |
| engPENK coding sequence, cistron 1 | 7 to 873 | 867 bp | our basic part, verbatim |
| EMCV IRES | 874 to 1447 | 574 bp | encephalomyocarditis virus |
| mEGFP, cistron 2 | 1448 to 2164 | 717 bp | monomeric EGFP, A206K |

The first cistron encodes a 288-residue precursor beginning with the native proenkephalin
signal peptide and ending in the carboxy-terminal decapeptide. The second encodes a
238-residue mEGFP carrying the A206K substitution that prevents the weak dimerisation of
the parent protein.

## About

We needed a construct in which the payload and a reporter are expressed from the same
transcript, so that any cell showing green fluorescence is also a cell that received the
therapeutic cassette. The obvious first attempt was to place the two coding sequences one
after the other. Translating that arrangement in silico showed why it fails: the ribosome
reads straight through and produces a single fused protein, which buries the
carboxy-terminal opioid core that the maturation enzymes have to reach. We caught this
before any DNA was ordered, and it is documented as the first cycle on our Engineering page.

An element between the two genes is therefore not an optimisation but a requirement. We
built both of the usual options, an IRES and a P2A peptide, in both gene orders, and this
part is the arrangement we would recommend to another team.

We placed the payload first and the reporter second, rather than the reverse. Translation
from an IRES is less efficient than cap-dependent translation, so whichever cistron sits
second is expressed at a lower level. Putting the reporter there costs us reporter signal,
which we can afford, and protects payload yield, which we cannot.

We chose the IRES over P2A for this submission for a reason that is specific to our payload.
A P2A peptide self-cleaves during translation but leaves roughly twenty residues of itself
attached to the upstream protein. On our construct that remnant would sit on the
proenkephalin precursor, immediately adjacent to the sequence the processing enzymes must
recognise. An IRES leaves nothing behind, and the first cistron terminates at its own stop
codon exactly as the native gene does.

## Literature

The EMCV IRES is the best characterised of the picornaviral IRES elements and is the one
most widely used for bicistronic mammalian expression, which is why we selected it rather
than a less documented alternative. Its activity depends on RNA secondary structure rather
than on a reading frame, a point that mattered when we came to check the sequence against
the assembly standards.

The A206K substitution in mEGFP disrupts the hydrophobic interface responsible for the weak
dimerisation of wild-type GFP variants. We used the monomeric form because our reporter sits
on the same transcript as a secreted precursor, and we did not want a dimerising tag
introducing an artefact into any downstream fluorescence measurement.

## Dry lab / computational analysis

**The composite was clean against both assembly standards without modification.** We scanned
both strands for the RFC10 sites (EcoRI, XbaI, SpeI, PstI, NotI) and the RFC1000 Type IIS
sites (BsaI, SapI), and also against a wider Type IIS panel beyond what either standard
requires. The basic part needed eight synonymous changes to reach that state; the composite
needed none.

We did not recode the IRES, and we want to be explicit that this was a decision rather than
an oversight. The element carries internal sites, but its function depends on folding into a
particular RNA structure rather than on a reading frame, so there is no synonymous change
available: any substitution risks the element for no compliance gain. None of those sites is
forbidden by either standard.

**The basic part appears verbatim in this composite, beginning at nucleotide 7.** Anyone can
confirm this with a single substring search. We built the two submissions this way on
purpose, so that they read as one checkable pair rather than as two unrelated entries, and
so that a team wanting only the coding sequence can take the basic part knowing it is
exactly what sits inside this one.

We also asked whether recoding the payload cassettes had disturbed the sites the convertases
must cut. Both the engineered and the native precursor carry twelve dibasic sites of the
same types in the same order, and across all twelve the engineered precursor is not
systematically less accessible than the native one (0.411 against 0.343, p = 0.160). We
report this as a weak negative rather than as a result, because the structure predictions it
rests on came back at confidence too low for per-residue interpretation. The experiment that
settles it is mass spectrometry on the transfection supernatant.

## Complementary parts

This composite contains basic part `BBa_26J864WV` verbatim, and is intended to be read
alongside it. The basic part is the coding sequence on its own, for teams who want to supply
their own promoter, reporter or expression context.

## Conclusion

This part provides a bicistronic cassette in which an engineered proenkephalin payload and a
fluorescent reporter are expressed from one transcript, with the payload in the
cap-dependent position and no peptide remnant left on the precursor.

Two things should be said plainly. **Neither this part nor its basic component has
characterisation data.** We designed and ordered our constructs as linear gene fragments
rather than complete plasmids, because full plasmid synthesis would not have returned within
the season, and the engineered sequence therefore entered no expression, purification or
maturation experiment. The DNA we hold is the His-tagged, differently codon-optimised version
of the same design, so any bench data we generate later will support this part by close
correspondence rather than by identity.

And our selectivity estimate for the payload has a confidence interval that includes zero.
δ-preference is the design goal this part was built to serve; it is not a demonstrated
property of it.

## References

The references are those of the basic part entry `BBa_26J864WV`, which documents the payload
design, the safety literature and the computational record in full.
