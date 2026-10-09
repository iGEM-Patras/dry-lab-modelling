# Native PENK, what the unmodified precursor actually makes

Computed from `P01210_native_PENK.fasta` (UniProt P01210, 267 aa precursor).
Chain coordinates are UniProt's; masses are computed, not quoted.

## Seven opioid cores, not one

Native proenkephalin-A carries **7 YGGF[ML] cores**: 6 × `YGGFM` and
1 × `YGGFL`, at precursor positions 100, 107, 136, 186, 210, 230, 261.
All seven have a dibasic KR/KK site immediately upstream. Downstream flanks differ, and that
is what produces the native product diversity:

| Core | Position | Downstream flank | Released product |
|---|---|---|---|
| 1 | 100 | KR | `YGGFM` Met-enkephalin |
| 2 | 107 | KK | `YGGFM` Met-enkephalin |
| 3 | 136 | KK | `YGGFM` Met-enkephalin |
| 4 | 186 | **RGL**KR | `YGGFMRGL` Met-enk-Arg-Gly-Leu (octapeptide) |
| 5 | 210 | **RRV**GRPE… | `YGGFMRRV`-NH₂ adrenorphin, via BAM-22 → BAM-20 |
| 6 | 230 | KR | `YGGFL` Leu-enkephalin |
| 7 | 261 | **RF** (precursor C-term) | `YGGFMRF` Met-enk-Arg-Phe (heptapeptide) |

Cores 4, 5 and 7 are *designed* to be extended, those flanks are the native source of the
octapeptide, heptapeptide and the BAM series. In the engineered construct the same two
positions (4 and 7) were flagged as producing "unclean" extended product. **That framing was
too harsh: extension at those positions is the native behaviour, not a construct defect.**
What is new in the engineered construct is that the extended products are
`YGGFEVVGRGL` / `YGGFEVVGRF`, which are not natural ligands and have not been characterised.

## Core 5 is a PAM substrate, native PENK does amidate

The amendment sheet stated that native cores end in Met or Leu and are therefore not PAM
substrates. That holds for the *enkephalin* products, but **core 5 is the exception**:
`YGGFMRRVG`… is trimmed by CPE to `YGGFMRRVG` and amidated by PAM to **adrenorphin
(metorphamide), `YGGFMRRV`-NH₂, [M+H]⁺ 984.5196**, a genuine amidated native product.
So amidation machinery is demonstrably active in these granules on this precursor, which
*strengthens* the prediction that the engineered `…VVG` cassette will be amidated.

## Every Met product has a +16 Da shadow

6 of 7 native cores carry Met. Met oxidises to the sulfoxide (+15.9949 Da)
during extraction, storage and ionisation, so each native product appears as a doublet:

- Met-enkephalin 574.2330 → sulfoxide 590.2279
- Met-enk-Arg-Phe 877.4025 → 893.3974
- BAM-22 carries **two** Met → up to +31.99 Da

The engineered cassette has **no Met**. This is a real and underrated advantage of the
engineered construct: it removes the oxidation satellite entirely, which simplifies both
quantification and formulation stability.

## The protease trade the engineering actually makes

Enkephalins are cleared in seconds, principally by neprilysin (NEP, the same enzyme the
project's siRNA targets) and aminopeptidase N; ACE contributes for C-terminally open peptides.
Counting susceptible bonds:

| Liability | Met-enkephalin | `YGGFEVVG` | `YGGFEVV`-NH₂ |
|---|---|---|---|
| Aminopeptidase (Tyr1-Gly2) | 1 | 1 | 1 |
| NEP internal sites (P1′ hydrophobic) | 1 (Gly3-Phe4) | **3** (Gly3-Phe4, Glu5-Val6, Val6-Val7) | **2** |
| ACE (C-terminus open) | yes | yes | **no** |
| Met oxidation | 1 | **0** | **0** |

**The engineered cassette is not more protease-stable than native Met-enkephalin, it is
less.** The two extra valines add NEP-susceptible bonds. Amidation removes the ACE liability
but not the NEP or aminopeptidase ones.

This is the point where the deltorphin analogy breaks down. Deltorphin II is
`Y-D-Ala-F-E-V-V-G`-NH₂; its metabolic stability comes principally from the **D-Ala at
position 2**, which blocks aminopeptidase attack at the Tyr1-Xaa2 bond. A ribosomally
expressed peptide is all-L by construction and **cannot reproduce that**. The engineered
cassette inherits deltorphin's δ-selectivity motif but none of its protease resistance.

## Consequences

1. **The NEP siRNA is doing more work than assumed.** With the engineered peptide carrying
   3 NEP sites against Met-enkephalin's 1, knocking down NEP is not an adjunct to the
   construct, it is what makes the construct viable at all. Those two arms are coupled.
2. **Native PENK output is the assay background.** Any transfected cell already secretes
   Met-enkephalin, Leu-enkephalin, the octa- and heptapeptides, and the BAM series from its
   endogenous locus. The MS method needs all of them, plus their sulfoxides, or endogenous
   peptide will be mistaken for construct output.
3. **Reconsider whether the cassette should be enkephalin-like at all.** If protease
   resistance is the goal, extending the C-terminus (as native cores 4/5/7 do) protects the
   scissile region better than the bare octapeptide does.
4. **Cores 4 and 7 in the engineered construct are less anomalous than reported**, they
   reproduce native flank architecture. The open question is pharmacological
   characterisation of the extended engineered species, not whether to eliminate them.
