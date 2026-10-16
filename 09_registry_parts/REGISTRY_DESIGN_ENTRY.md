# Registry entry, Type: **Design**

**Paste everything below the line into the editor box. Markdown only, no HTML.**
**Title:** `Engineered proenkephalin precursor: recoding seven payload cassettes while preserving native processing`
**Affiliation:** Patras UPAT (2026)
**Part:** `BBa_26J864WV`

---

## Overview

This part is the coding sequence of a human preproenkephalin precursor in which all seven
enkephalin payload cassettes have been recoded from the native `YGGFM` / `YGGFL` to
`YGGFEVVG`, an octapeptide carrying the deltorphin C-terminal address on the enkephalin
message. Everything else about the precursor is preserved: the native signal peptide, all
twelve dibasic processing sites at native spacing, the cysteine positions and the overall
length.

The design intent is to raise local enkephalin tone with a payload biased toward the
delta-opioid receptor, while letting the host cell's own proprotein convertases perform
release exactly as they do for the native precursor.

867 bp, 289 codons, 288 aa product, GC 59.2 %. Clean for RFC10 and RFC1000 on both strands.

## About

**What it is and what it is designed to do.**

Enkephalins cannot be expressed directly as peptides. The native route is a precursor
protein carrying several payload copies separated by dibasic (KR, KK, RR) recognition sites;
proprotein convertases cut at those sites inside secretory granules and liberate the mature
peptides at the point of release.

This part supplies that precursor with a modified payload. On expression it should be:

1. directed into the secretory pathway by its retained native signal peptide (residues 1-24),
2. trafficked to dense-core granules,
3. cleaved at the twelve preserved dibasic sites,
4. releasing seven copies of `YGGFEVVG` plus a C-terminal `YGGFEVVGRF` decapeptide.

**Why a precursor and not a direct peptide.** Keeping the native scaffold means no
engineered release mechanism is required. The part is a drop-in replacement for the native
precursor in any cell that already processes preproenkephalin, and the processing machinery
is the cell's own.

**What was deliberately not changed.** The signal peptide, the twelve dibasic sites and
their spacing, the cysteines, and the precursor length. Each of these is load-bearing for
trafficking or cleavage, and altering them would have converted a payload swap into a
redesign of the release mechanism.

## Literature

**Where the sequence comes from.** Human proenkephalin-A, UniProt **P01210**. The native
precursor carries six copies of Met-enkephalin and one of Leu-enkephalin.

**What the native part has been shown to do.** A herpes-simplex vector expressing *native*
human preproenkephalin (NP2) completed a Phase 1 trial in intractable cancer pain
(ClinicalTrials.gov **NCT00804076**; Wolfe, Mata & Fink, *Gene Ther* 2009, PMID 19242524,
doi:10.1038/gt.2009.17), with a follow-on study registered as **NCT01291901**. Dose-related
analgesia was reported and the approach was taken into further development. This is the
closest precedent for the part's intended use, and it establishes that enkephalin-precursor
gene delivery is tractable in humans.

**Why a delta bias.** Delta-opioid receptor agonism is associated with analgesia carrying
less respiratory depression than mu agonism. Native Met-enkephalin is only mildly
delta-preferring, so the payload was re-engineered to carry the deltorphin address.

**The safety literature we checked before committing to delta.** A reported seizure
liability for delta agonists does not hold as a class claim. Convulsant effects are
documented for specific agonists (PMID 8246164, doi:10.1016/s0022-3565(25)39544-3;
PMID 16537798, doi:10.1124/jpet.105.095810), with delta receptors on parvalbumin
interneurons implicated (PMID 42213967, doi:10.1097/fbp.0000000000000882). The liability is
ligand-specific: multiple delta agonists do not produce seizures
(PMID 37004753, doi:10.1016/j.neuropharm.2023.109526). Enkephalin itself and enkephalinase
inhibition have been reported to *reduce* rather than provoke seizure activity
(PMID 8272192, doi:10.1007/bf00975045).

## Dry lab / computational analysis

All work below preceded synthesis. Each analysis is reported with what it does **not**
establish, because several of them failed.

**Selectivity estimate, and its limits.** A delta/mu selectivity model was calibrated
against thirteen published reference opioids, reaching r = 0.805 (p = 0.0009) with the
correct sign on twelve of thirteen. Applied to the engineered payload it gives
**+1.23 +/- 1.76 kcal/mol** delta-over-mu.

**That interval includes zero.** The payload is not statistically separable from native
Met-enkephalin on this measure. A later alchemical free-energy calculation gave a
mu-preferring estimate and then failed its own pre-registered reproducibility gate, with two
replicates disagreeing by several times their combined error; we treat it as uninformative
rather than as evidence in either direction. **Delta preference is a design goal, not a
demonstrated result.**

**Can the payload be released?** This is the question that matters most for a precursor.
Structures of the engineered and native precursors were predicted and relative solvent
accessibility measured at all twelve dibasic sites. Across the twelve corresponding sites:
**0.411 native versus 0.343 engineered, difference 0.068, p = 0.160.** No evidence that
recoding systematically buries the processing sites.

We report this as a weak negative only. Both predictions had mean pLDDT of 43 and 37, below
the threshold at which per-residue burial is interpretable, and in the native control the
site-to-site variation was smaller than the scatter between repeated predictions of the same
sequence. Three engineered sites initially appeared less accessible; that apparent signal
did not survive the variance check and we withdraw it.

**Immunogenicity screen.** Predicted MHC class I binding across 6,120 allele-peptide pairs:
**1.86 % strong binders for the engineered epitope versus 1.77 % for the native epitope it
replaces.** Not meaningfully more immunogenic than the sequence it displaces. This is a
screen, not a clearance; class I prediction addresses CD8 recognition of an intracellular
product, not antibody responses to a secreted peptide.

**Structural grounding for the address graft.** The delta-opioid receptor has been
crystallised with deltorphin bound (PDB **8F7S**), and that structure shares the five-residue
stretch `FEVVG` with our payload. Blind docking into that receptor recovered the
crystallographic peptide pose to 3.41 A, with four of thirty-two models within 5 A, while a
deliberately under-sampled control recovered nothing (best 39 A). This validates the docking
protocol; it is not itself a selectivity result.

**Assembly-standard cleanup.** Eight synonymous single-base changes were required to clear
RFC10 (EcoRI, XbaI, SpeI, PstI, NotI) and RFC1000 (BsaI, SapI), scanned on both strands. The
encoded protein is identical before and after and all seven cassettes are intact. We widened
the enzyme panel past what either standard requires so the part is usable in other assembly
systems; that surfaced extra sites, including some nested inside longer recognition motifs
and some on the reverse strand.

## Complementary parts

**Our composite part** contains this basic part **verbatim**, beginning at nucleotide 7
immediately after the Kozak sequence:

```
composite (2164 bp) = Kozak (6) + THIS BASIC PART (867) + IRES (574) + mEGFP (717)
```

A single substring search verifies the relationship. The IRES allows the reporter to be
translated from the same transcript without fusing it to the payload, so mEGFP fluorescence
reports transfection without interfering with precursor processing.

**A neprilysin-targeting siRNA** is co-delivered in the same lipoplex. Neprilysin degrades
enkephalins within seconds, so the two arms are complementary: this part raises production
while the siRNA slows degradation. Each siRNA candidate was screened against this
part's own transcript to confirm it does not target the therapeutic cassette.

## Conclusion

The part is designed, sequence-verified and compliant with both assembly standards. The
design preserves everything required for native processing and changes only the payload.

**It has not been characterised at the bench, and we can say exactly why.** Our
purification route was specified after the expression cassette rather than alongside it, so
our first-generation constructs carried no affinity tag. Correcting that meant re-ordering.
For native proenkephalin the tagged constructs arrived and carried everything downstream.
For this engineered sequence **there was no time left to order complete plasmids**, since
full plasmid synthesis turns round more slowly than a linear gene fragment and the season
would have closed first. The first-generation plasmids therefore served only as backbones,
and **this sequence entered no expression, purification or maturation experiment.**

One further point we would rather state than have found: the DNA in our freezer is the
His-tagged, differently codon-optimised version. This part is that construct's coding
sequence minus the purification tag, so any future characterisation supports it by
**close correspondence rather than identity**.

The claims this entry supports are: the architecture is preserved, the sequence is clean,
the payload is no more immunogenic than the one it replaces, and there is no evidence the
processing sites are buried. The claim it does **not** support is a delta-selectivity value.
A functional cAMP assay at both receptors with selective antagonists is the instrument for
that, and it is the next experiment.

## References

1. UniProt **P01210**, human proenkephalin-A.
2. PDB **8F7S**, delta-opioid receptor in complex with deltorphin.
3. Wolfe D, Mata M, Fink DJ. *Gene Ther.* 2009;16(4):455-60. PMID 19242524,
   doi:10.1038/gt.2009.17
4. ClinicalTrials.gov **NCT00804076**, gene transfer for cancer pain, intervention NP2.
5. ClinicalTrials.gov **NCT01291901**, NP2 enkephalin for intractable pain.
6. PMID 8246164, doi:10.1016/s0022-3565(25)39544-3
7. PMID 16537798, doi:10.1124/jpet.105.095810
8. PMID 42213967, doi:10.1097/fbp.0000000000000882
9. PMID 37004753, doi:10.1016/j.neuropharm.2023.109526
10. PMID 8272192, doi:10.1007/bf00975045
11. PMID 38249734, doi:10.3389/fneur.2023.1298489
