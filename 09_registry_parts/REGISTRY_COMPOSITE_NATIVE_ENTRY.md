# Registry entry, native composite part, Type: **Design**

**Paste everything below the line into the editor box. Markdown only, no HTML.**
**Title:** `Bicistronic native proenkephalin with IRES-driven mEGFP reporter`
**Affiliation:** Patras UPAT (2026)
**Companion part:** the engineered composite, which differs from this one only in its first cistron

---

## Overview

This composite part expresses native human proenkephalin and a fluorescent reporter from a
single transcript. It is the control member of a matched pair: the companion composite is
identical except that its first cistron carries our engineered payload instead of the native
one. Anyone comparing a payload against the sequence evolution produced can do so by swapping
one part for the other and changing nothing else.

The part is 2,101 bp.

| component | position | length | source |
|---|---|---|---|
| Kozak consensus | 1 to 6 | 6 bp | GCCACC |
| native proenkephalin coding sequence | 7 to 810 | 804 bp | our native basic part, verbatim |
| EMCV IRES | 811 to 1384 | 574 bp | encephalomyocarditis virus |
| mEGFP, second cistron | 1385 to 2101 | 717 bp | monomeric EGFP, A206K |

The first cistron encodes the 267-residue human proenkephalin precursor. Its translated
protein is byte-identical to UniProt **P01210**, carrying six Met-enkephalin cores, one
Leu-enkephalin core, and the three extended products Met-enkephalin-Arg-Phe,
Met-enkephalin-Arg-Gly-Leu and the amino-terminal heptapeptide region.

## About

We built this part because our engineered payload needs something to be compared against,
and the honest comparator is not a buffer control. It is the same cassette carrying the
sequence evolution arrived at.

The two composites share the Kozak sequence, the IRES and the reporter, nucleotide for
nucleotide. The only difference between them is the first cistron. That makes the pair a
controlled comparison rather than two separate constructs: any difference in expression,
processing or activity can be attributed to the payload, because nothing else varies.

The reasoning behind the architecture is set out on the engineered composite's page and
applies identically here. In short, two coding sequences placed directly in series translate
as one fused protein, which buries the carboxy-terminal opioid core. An element between the
genes is therefore required. We put the payload in the first, cap-dependent position and the
reporter second, because translation from an IRES is less efficient and the second position
should cost reporter signal rather than payload. We chose an IRES over a P2A peptide because
P2A leaves roughly twenty residues attached to the upstream protein, which on a proenkephalin
precursor would sit immediately next to the sequence the processing enzymes must recognise.

## Literature

Native proenkephalin is the body's own precursor for Met- and Leu-enkephalin, the endogenous
agonists of the delta and mu opioid receptors. It is processed by prohormone convertase 2
acting at paired basic residues, followed by carboxypeptidase E, which removes the basic
residues the endoprotease leaves behind. Neither enzyme is present in HEK293T, which is why
our own maturation work reconstitutes the reaction in vitro rather than relying on the cell.

The precursor's architecture is unusual and worth stating for anyone using this part: it
carries seven opioid cores in one chain, so a single successful expression and processing
event yields seven peptides rather than one.

## Dry lab / computational analysis

**Provenance.** The coding sequence was read out of the wet lab's own as-received plasmid
rather than retrieved from a database, then translated and checked against UniProt P01210.
The translation is identical. We mention this because it establishes that the part is the
sequence actually in hand, not a reference sequence that resembles it.

**Two silent changes for assembly-standard compliance.** The native coding sequence carried
two PstI sites, which RFC10 forbids. Both were removed by single-nucleotide synonymous
substitutions at leucine codons 69 and 206, CTG to CTC in each case. We chose CTC rather than
the first synonymous codon that happened to destroy the site: CTG is the most frequent
leucine codon in human genes and CTC is the second, so the substitution does not trade
compliance for a rare codon. The translated protein is unchanged, verified residue by
residue, and all seven opioid cores and the three extended products are intact.

**Standards.** Both this composite and the native basic part inside it carry zero RFC10 sites
and zero RFC1000 Type IIS sites, on both strands.

Four sites from a wider Type IIS panel sit in the IRES and the reporter. They are identical
in both composites, because those elements are shared, so they are a property of the elements
rather than of either payload. **None of those enzymes is required by either standard, and we
did not recode the IRES.** Its activity depends on folding into a particular RNA structure
rather than on a reading frame, so no synonymous change exists there, and recoding it would
risk the element for no compliance gain.

**What the pair is for.** The two composites differ in 804 against 867 bp of first cistron
and in nothing else. Characterising them side by side separates payload effects from cassette
effects, which is a comparison neither part supports on its own.

## Complementary parts

This composite contains our native basic part verbatim, beginning at nucleotide 7, and is the
control member of a pair with the engineered composite. Teams wanting only the coding sequence
should take the basic part.

## Conclusion

This part provides native human proenkephalin and a reporter on one transcript, as the
controlled comparator for an engineered payload in an otherwise identical cassette.

**Neither member of this pair has characterisation data.** We designed and ordered our
constructs as linear gene fragments rather than complete plasmids, because full plasmid
synthesis would not have returned within the season. The native sequence here was recovered
from a plasmid the wet lab holds, so it is the sequence in hand; the parts as submitted,
however, have not themselves been expressed, purified or assayed. Any bench data we generate
later will support them by close correspondence rather than by identity, since the DNA in the
freezer also carries a purification tag these parts do not.

## References

UniProt P01210, human proenkephalin-A. Processing enzymes and the chassis limitation are
documented with citations on the engineered composite's page and in our repository.
