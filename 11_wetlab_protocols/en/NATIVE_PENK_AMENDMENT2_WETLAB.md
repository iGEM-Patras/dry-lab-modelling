# Amendment 2 — the endogenous PENK background

**Supersedes:** two statements in `ENGPENK_AMENDMENT1_WETLAB.md` (see §0). Everything else in
Amendment 1, and in `ENGPENK_PEPTIDE_WETLAB.md`, stands.
**Basis:** UniProt P01210 (proenkephalin-A, 267 aa), analysed against the engineered insert.
**Date:** 2026-08-19. **Status:** dry-lab finding. Nothing here has been measured in-house.

---

## 0. Two corrections to Amendment 1

**0.1 — "Native PENK cores end in Met or Leu and are therefore not PAM substrates."**
True for the enkephalins, **wrong as a general statement**. Core 5 (`YGGFMRRVG`…) is trimmed by
CPE and amidated by PAM to **adrenorphin / metorphamide, `YGGFMRRV`-NH₂, [M+H]⁺ 984.5196**.
Native PENK does make an amidated product.

*This cuts in the construct's favour.* It is direct evidence that PAM is active in these
granules, on this precursor. The predicted amidation of the engineered `…VVG` cassette is on
firmer ground than Amendment 1 claimed, not weaker.

**0.2 — "Cassettes 4 and 7 will not give clean product."**
Too harsh. Positions 4 and 7 are exactly where **native** PENK deliberately makes extended
peptides — the octapeptide `YGGFMRGL` and the heptapeptide `YGGFMRF` come from those same
monobasic flanks. The engineered construct is reproducing native architecture, not failing.

What *is* genuinely open: the engineered extended species `YGGFEVVGRGL` and `YGGFEVVGRF` are
not natural ligands and have no published pharmacology. Characterise them; do not assume they
need to be engineered away.

---

## 1. The finding that changes the project's risk profile

Enkephalins are cleared in seconds, principally by **neprilysin (NEP)** — the same enzyme the
project's siRNA arm targets — and by aminopeptidase N. Counting susceptible bonds:

| Liability | Met-enkephalin (native) | `YGGFEVVG` | `YGGFEVV`-NH₂ |
|---|---|---|---|
| Aminopeptidase, Tyr1-Gly2 | 1 | 1 | 1 |
| **NEP internal sites** (P1′ hydrophobic) | **1** (Gly3-Phe4) | **3** (Gly3-Phe4, Glu5-Val6, Val6-Val7) | **2** |
| ACE (C-terminus open) | yes | yes | no |
| Met oxidation satellite | 1 | **0** | **0** |

**The engineered peptide is less protease-stable than native Met-enkephalin, not more.** The
two valines add NEP-susceptible bonds.

This is where the deltorphin analogy breaks. Deltorphin II is `Y`-**D-Ala**-`FEVVG`-NH₂, and
its metabolic stability comes principally from the **D-Ala at position 2** blocking
aminopeptidase attack at Tyr1-Xaa2. A ribosomally expressed peptide is all-L by construction
and **cannot reproduce that**. The cassette inherits deltorphin's δ-selectivity motif and none
of its protease resistance.

> **Consequence for the project plan.** The NEP siRNA is not an adjunct to the peptide arm —
> with 3 NEP sites against Met-enkephalin's 1, the knockdown is what makes the engineered
> peptide viable at all. **The two arms are coupled and must be evaluated together.** A
> peptide-only experiment will under-read the construct; a knockdown-only experiment will not
> show the peptide's benefit.

The one clear win for the engineered design: **no Met anywhere**, so no +16 Da oxidation
satellite on any construct product. That simplifies quantification and formulation stability.

---

## 2. What an untransfected cell already secretes

Native proenkephalin-A carries **7 opioid cores** (6 × `YGGFM`, 1 × `YGGFL`) at precursor
positions 100, 107, 136, 186, 210, 230, 261. All have a dibasic site upstream; the downstream
flanks differ, and that is what generates the native product set.

| Core | Pos | Downstream flank | Released product |
|---|---|---|---|
| 1 | 100 | KR | `YGGFM` Met-enkephalin |
| 2 | 107 | KK | `YGGFM` Met-enkephalin |
| 3 | 136 | KK | `YGGFM` Met-enkephalin |
| 4 | 186 | **RGL**KR | `YGGFMRGL` Met-enk-Arg-Gly-Leu |
| 5 | 210 | **RRV**GRPE… | `YGGFMRRV`-NH₂ adrenorphin, via BAM-22 → BAM-20 |
| 6 | 230 | KR | `YGGFL` Leu-enkephalin |
| 7 | 261 | **RF** (precursor C-term) | `YGGFMRF` Met-enk-Arg-Phe |

**Any cell line with an intact PENK locus secretes all of this before you transfect anything.**
Treat it as assay background, not as construct output.

---

## 3. MS target list — 9 endogenous peptides, 20 peaks

6 of 7 native cores carry Met, and Met oxidises to the sulfoxide (**+15.9949 Da**) during
extraction, storage and ionisation. Every Met-containing product therefore appears as a
doublet — BAM-22 and BAM-20 carry two Met and give a triplet.

| Peptide | Sequence | [M+H]⁺ | +1 ox | +2 ox | Origin |
|---|---|---|---|---|---|
| `Met-enkephalin` | `YGGFM` | 574.2330 | 590.2279 | — | cores 1,2,3 direct; core 5 after full BAM processing |
| `Leu-enkephalin` | `YGGFL` | 556.2766 | — | — | core 6 |
| `Met-enk-Arg-Gly-Leu` | `YGGFMRGL` | 900.4396 | 916.4345 | — | core 4, monobasic downstream |
| `Met-enk-Arg-Phe` | `YGGFMRF` | 877.4025 | 893.3974 | — | core 7, precursor C-terminus |
| `Adrenorphin/metorphamide` | `YGGFMRRV` | 984.5196 | 1000.5145 | — | core 5, PAM product of ...RRVG |
| `BAM-22` | `YGGFMRRVGRPEWWMDYQKRYG` | 2838.3504 | 2854.3453 | 2870.3402 | core 5 intermediate |
| `BAM-20` | `YGGFMRRVGRPEWWMDYQKR` | 2618.2656 | 2634.2605 | 2650.2554 | core 5 intermediate |
| `BAM-8-22` | `VGRPEWWMDYQKRYG` | 1970.9330 | 1986.9279 | — | core 5, N-terminally trimmed (non-opioid) |
| `Peptide F (core1-2)` | `YGGFMKRYGGFMKK` | 1669.8341 | 1685.8290 | 1701.8240 | cores 1+2 unseparated intermediate |

Full list including the 5 construct species: `penk_ms_target_list.csv`.

**Collision check (computed).** Across all 25 species — 20 endogenous + 5 construct — there
are **no monoisotopic collisions within 1.5 Da between any native and any construct peak**.
The two panels are mass-resolved from each other; a quadrupole or ion trap can separate
construct output from endogenous background. The only near-isobaric pair in the whole panel is
`YGGFEVVG` free acid (827.3934) against `YGGFEVVG`-NH₂ (826.4094), and those belong to two
different construct versions that cannot co-occur in one sample.

---

## 4. What to run

1. **Untransfected control, same cell line and passage, every time.** Not optional. It defines
   the endogenous baseline for all 20 peaks above.
2. **Empty-vector control** alongside it, to separate transfection stress from construct output.
3. **Acquire the full 550–2900 Da range**, not a narrow window around the octapeptide. The BAM
   series sits at 2618–2870 and will be missed by a method tuned to the enkephalins.
4. **Include the +16 satellites in the target list**, or Met-enkephalin will appear to be lost
   when it has only oxidised.
5. **Report construct peptide as a ratio to endogenous Met-enkephalin** in the same sample.
   That internally controls for extraction efficiency and cell number, which absolute
   quantification does not.

---

## 5. Sample handling — because 6 of 7 native peaks oxidise

Met oxidation is an artefact of handling as much as of biology. To keep the +16 satellite from
becoming the dominant peak:

- Collect on ice; process without a freeze-thaw where possible.
- Acidify immediately (0.1 % formic acid) and keep samples cold and dark.
- Avoid metal surfaces and peroxide-containing solvents; use fresh, degassed mobile phase.
- Run oxidation-prone samples early in the sequence, not after a long queue.
- **Quantify parent + sulfoxide together** as one pool for each Met peptide. This is the
  robust readout — the parent alone drifts with handling.

---

## 6. Bench checklist

- ☐ Untransfected and empty-vector controls scheduled in the same cell line and passage (§4)
- ☐ MS method covers 550–2900 Da, not just the enkephalin window (§4)
- ☐ All 20 endogenous peaks plus their +16 satellites in the target list (§3)
- ☐ Construct peptide reported as a ratio to endogenous Met-enkephalin (§4)
- ☐ Cold/acidified/no-freeze-thaw handling in the SOP (§5)
- ☐ Met peptides quantified as parent + sulfoxide pool (§5)
- ☐ **Project-level:** peptide arm and NEP-siRNA arm evaluated together, not separately (§1)
