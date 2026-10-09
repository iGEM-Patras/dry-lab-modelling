# Antibody assessment for the lipoplex, from the wet-lab suggestion

Source: `LIPOPLEX(1).docx`. The document's antibody content is a **targeting** proposal
(surface ligands for neurotropism), not validation reagents. Assessed below against the
Antibody Registry, UniProt topology, and the project's own engineered insert.

## THE BLOCKING FINDING: no commercial antibody can detect this construct's product

`engPENK_insert_annotated.gb` (885 nt, CDS 13..879, 288 aa ORF) encodes **7 identical
copies of the octapeptide `YGGFEVVG`**, each flanked by dibasic KR/KK processing sites.

Native human PENK (P01210, 267 aa) carries 6x `YGGFM` + 1x `YGGFL` [2,3].
The engineered construct carries **0 copies of either**.

Every anti-enkephalin antibody in the registry is raised against the native mature
pentapeptide, so all of them miss the product:

| RRID | antibody | epitope | verdict |
|---|---|---|---|
| AB_2530349 | anti-Met-enkephalin mAb 1194/334 | YGGFM | **will not detect** |
| AB_2492947 | anti-Met-enkephalin pAb | PENK 237–241 (=YGGFM) | **will not detect** |
| AB_3430419 | anti-Met-enkephalin | Met-enkephalin | **will not detect** |
|, | custom anti-`YGGFEVVG`–KLH | the engineered octapeptide | **required; must be custom-raised** |
|, | precursor-directed anti-PENK | PENK backbone | precursor only; cannot show maturation |

The shared `YGGF` N-terminal core is not sufficient: anti-Met-enkephalin antibodies are
raised against the whole pentapeptide and typically require the free C-terminal Met,
which the product does not have. **Order a custom polyclonal against `YGGFEVVG`
(KLH-conjugated, ≥2 rabbits) now**, it is a 10–12 week lead time and it gates the
entire expression readout.

## Targeting: TfR is sound, TRPV1 is weak

**TfR (the document's own preferred target).** The transferrin receptor has been the
canonical brain-endothelium target since it was localised there [4], and
antibody–drug conjugates against it cross the barrier [5]. Verified in the registry; each clone is
strictly species-restricted, so the reagent must be chosen for the model, not the
target:

| clone | RRID | binds | note |
|---|---|---|---|
| OKT9 | AB_3714951 | human TFRC (P02786) | human cells only |
| OX-26 | AB_2573153 | rat TFRC (Q99376) | the classic BBB-transcytosis clone |
| RI7217 | AB_3715099 | mouse TFRC (Q62351) | most-cited low-avidity transcytosis clone |
| 8D3 | AB_1511006 | mouse TFRC | high avidity; binds BECs but transcytoses poorly |

Human vs mouse TfR is 77.2% identical (global alignment), below the ~90% where
cross-reactivity is usually retained. There is **no single TfR antibody that works in
both the rodent model and human cells.** The document's point about preferring low
affinity/avidity for transcytosis is correct [7,12] and is the reason to
prefer RI7217 over 8D3.

**TRPV1 (`anti-TRPV1` in the document) is a poor surface-targeting choice.** Two registry
antibodies are sold as "extracellular" and both check out against UniProt topology [16],
consistent with the cryo-EM structures [9,10]:
human aa 456–471 `RPVDGLPPFKMEKTGD` sits in the 456–472 extracellular domain, and rat
aa 605–619 in the 599–630 loop. But:

- **Only 56 of 839 residues (6.7%) of TRPV1 are extracellular**, in four loops of 17, 3,
  32 and 4 aa. There is very little surface to bind.
- Both are **polyclonal**: no orientation control for site-directed conjugation.
- The epitopes are only 56–60% conserved human↔rat, against 85.7% for the whole protein,
  so neither reagent transfers between models.
- The rat vendor peptide differs from UniProt O35433 at one position (Cys616→Ser);
  confirm with the vendor, as a Cys in the immunogen is also a conjugation handle.

Only 15 of 485 TRPV1 records mention flow cytometry; the set is dominated by western
(194) and IHC (145), i.e. fixed/permeabilised formats that say nothing about
live-cell surface accessibility.

**Recommendation:** keep the RVG peptide as the neuronal ligand [6] (it is a peptide, cheap,
and needs no antibody), use TfR for BBB transcytosis, and drop anti-TRPV1 as a targeting
ligand. If TRPV1 selectivity is wanted, a small-molecule TRPV1 ligand is the better
handle than an antibody against a 6.7%-exposed target.

## Formulation QC (available now, cheap)

| clone | RRID | detects |
|---|---|---|
| RM105 | AB_2716366 | mPEG methoxy terminus |
| B141M / B139M | AB_936779 / AB_936777 | PEG backbone |

Terminus + backbone pair supports a sandwich ELISA for surface PEG density, and screens
anti-PEG immunogenicity [14]: a real failure mode for the repeat-dosed PEG(2000)-CerC8
formulation the document specifies.

## siRNA arm: re-designed for human exclusivity

The wet lab requires the siRNA to be **exclusively human, with no mouse cross-reactivity.**
The previously delivered panel does not meet that constraint. Every one of its 11 guides is
a perfect 19/19 match to human *MME* (NM_000902.5), but tested against mouse *Mme*
(NM_008604.4) **none is exclusive**: 8 retain ≥17/19 identity and two (CDS1590, CDS1616)
are perfect 19/19 matches in mouse, i.e. fully cross-reactive.

Re-screening the whole human CDS (751 codons, 2253 nt) under the new constraint gives 307
composition- and asymmetry-filtered 19-mers, of which **26 fall to ≤15/19 against mouse.**
Ranking those by seed divergence, human off-target burden (BLASTn vs human refseq_rna,
word size 7, RID 6N566XEC014), duplex asymmetry [8] and GC content:

| rank | guide (5'→3') | CDS pos | GC% | mouse | seed MM | off-targets ≥17/19 | composite |
|---|---|---|---|---|---|---|---|
| 1 | `AAAGUUGCCGUAACGGGAGdTdT` | 303 | 52.6 | 14/19 | 2 | 0 | 85.8 |
| 2 | `UCCUCGACCACAUGUUUACdTdT` | 1307 | 47.4 | 14/19 | 2 | 4 | 74.3 |
| 3 | `UGGAGUUAACCGCAUACUCdTdT` | 2101 | 47.4 | 15/19 | 3 | 0 | 61.6 |
| 4 | `UACAAGACCUGUACAAUGCdTdT` | 412 | 42.1 | 15/19 | 2 | 1 | 57.8 |
| 5 | `UGAAUUACAUGAUUCACAGdTdT` | 635 | 31.6 | 14/19 | 3 | 84 | 54.5 |

SIRNA_FIGURE_PLACEHOLDER

**Recommended lead: CDS303**: guide `AAAGUUGCCGUAACGGGAGdTdT`, passenger
`CUCCCGUUACGGCAACUUUdTdT`. 19/19 on human *MME*, 14/19 on mouse *Mme* with 2 of
those mismatches inside the seed (guide positions 4,7), **zero** human
off-targets at ≥17/19, and favourable duplex asymmetry (ΔΔG = 4.20 kcal/mol,
guide 5'-end less stable, which loads the correct strand). CDS2101 is the best
three-seed-mismatch alternative and also has zero ≥17/19 off-targets; order both plus a
scrambled control.

Guide positions 2–8 are the seed; a mismatch there is the most reliable way to abolish
activity on an unintended transcript, which is why exclusivity was ranked on seed
divergence rather than on total identity alone. Note the corollary: **these guides cannot
be tested in a mouse model.** Knockdown validation must be done in human cells, and any
in-vivo rodent work needs a separate mouse-targeting surrogate, accepting that it is then
a different molecule, not the same one.

For the validation western, only **4 MME/neprilysin records** exist in the registry;
AB_2860234 (mouse mAb, CD10) is the lead. Confirm human reactivity and WB validation
before ordering.

## Note on the document's sources

Two links are NotebookLM notebooks (not citable) and one is a sci-hub mirror. That last
one resolves to a legitimate citation: Shimoni, Shi, Adlard & Bush, "Delivery of
Fluorescent Nanoparticles to the Brain", *Journal of Molecular Neuroscience* (2016),
doi:10.1007/s12031-016-0833-5 (ref. 15): cite that directly rather than the mirror.

## Consequence for the CG-MD work

Adding a conjugated antibody is **not** a parameter change to the existing lipoplex
model. An IgG is ~150 kDa against lipid components of a few hundred daltons, so it would
dominate box size and runtime, and there is no coarse-grained membrane skill available
here. If targeting ligands are going into the model, scFv or nanobody (as the document
itself suggests, ~28/15 kDa) is the only tractable option, and the DOTAP/MC3 replicate
results should be finished and reported on the bare formulation first.

## What the wet lab still needs to supply

For each antibody they recommend: **catalog number + vendor, clone ID or RRID, the
immunogen sequence or residue range, validated applications, species reactivity, and
whether it is carrier-free.** The immunogen sequence is the one most often omitted and
the one that decides whether a reagent works here, as the PENK finding above shows.

## Methods

Reagent records were retrieved from the Antibody Registry and are cited by RRID
[13]. Sequences and topological-domain annotation are from UniProt
[16]: human TRPV1 Q8NER1, rat TRPV1 O35433, human TFRC P02786, mouse TFRC
Q62351, rat TFRC Q99376, human PENK P01210. Transcripts are RefSeq NM_000902.5 (human
*MME*) and NM_008604.4 (mouse *Mme*). Percent identities are global Needleman–Wunsch
alignments [1] (match +2, mismatch −1, gap −1); the engineered insert was
translated from `engPENK_insert_annotated.gb` (CDS 13..879). siRNA off-target screening
used NCBI BLASTn against human refseq_rna (word size 7, no low-complexity filter,
*Homo sapiens* restricted); duplex asymmetry is the nearest-neighbour ΔG37 difference
between the guide 5'- and 3'-terminal tetramers. Every DOI below was verified against
Crossref rather than recalled. Lipid- and targeted-nanoparticle formulations for
formulation context: refs 8, 11.

## References

1. Needleman SB, Wunsch CD (1970). A general method applicable to the search for similarities in the amino acid sequence of two proteins. *Journal of Molecular Biology* **48**:443-453. doi:10.1016/0022-2836(70)90057-4
2. Comb M, Seeburg PH, Adelman J et al. (1982). Primary structure of the human Met- and Leu-enkephalin precursor and its mRNA. *Nature* **295**:663-666. doi:10.1038/295663a0
3. Noda M, Furutani Y, Takahashi H et al. (1982). Cloning and sequence analysis of cDNA for bovine adrenal preproenkephalin. *Nature* **295**:202-206. doi:10.1038/295202a0
4. Jefferies WA, Brandon MR, Hunt SV et al. (1984). Transferrin receptor on endothelium of brain capillaries. *Nature* **312**:162-163. doi:10.1038/312162a0
5. Friden PM, Walus LR, Musso GF et al. (1991). Anti-transferrin receptor antibody and antibody-drug conjugates cross the blood-brain barrier. *Proceedings of the National Academy of Sciences* **88**:4771-4775. doi:10.1073/pnas.88.11.4771
6. Kumar P, Wu H, McBride JL et al. (2007). Transvascular delivery of small interfering RNA to the central nervous system. *Nature* **448**:39-43. doi:10.1038/nature05901
7. Yu YJ, Zhang Y, Kenrick M et al. (2011). Boosting Brain Uptake of a Therapeutic Antibody by Reducing Its Affinity for a Transcytosis Target. *Science Translational Medicine* **3**. doi:10.1126/scitranslmed.3002230
8. Jayaraman M, Ansell SM, Mui BL et al. (2012). Maximizing the Potency of siRNA Lipid Nanoparticles for Hepatic Gene Silencing In Vivo. *Angewandte Chemie International Edition* **51**:8529-8533. doi:10.1002/anie.201203263
9. Cao E, Liao M, Cheng Y et al. (2013). TRPV1 structures in distinct conformations reveal activation mechanisms. *Nature* **504**:113-118. doi:10.1038/nature12823
10. Liao M, Cao E, Julius D et al. (2013). Structure of the TRPV1 ion channel determined by electron cryo-microscopy. *Nature* **504**:107-112. doi:10.1038/nature12822
11. Senzer N, Nemunaitis J, Nemunaitis D et al. (2013). Phase I Study of a Systemically Delivered p53 Nanoparticle in Advanced Solid Tumors. *Molecular Therapy* **21**:1096-1103. doi:10.1038/mt.2013.32
12. Niewoehner J, Bohrmann B, Collin L et al. (2014). Increased Brain Penetration and Potency of a Therapeutic Antibody Using a Monovalent Molecular Shuttle. *Neuron* **81**:49-60. doi:10.1016/j.neuron.2013.10.061
13. Bandrowski A, Brush M, Grethe JS et al. (RRID Initiative) (2015). The Resource Identification Initiative: A Cultural Shift in Publishing. *Neuroinformatics* **14**:169-182. doi:10.1007/s12021-015-9284-3
14. Yang Q, Lai SK (2015). Anti‐PEG immunity: emergence, characteristics, and unaddressed questions. *WIREs Nanomedicine and Nanobiotechnology* **7**:655-677. doi:10.1002/wnan.1339
15. Shimoni O, Shi B, Adlard PA et al. (2016). Delivery of Fluorescent Nanoparticles to the Brain. *Journal of Molecular Neuroscience* **60**:405-409. doi:10.1007/s12031-016-0833-5
16. The UniProt Consortium (2024). UniProt: the Universal Protein Knowledgebase in 2025. *Nucleic Acids Research* **53**:D609-D617. doi:10.1093/nar/gkae1010
