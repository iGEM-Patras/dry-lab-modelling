# Amendment 1: engPENK peptide identity and granule processing

**Supersedes:** §1 "Three ordering details that are easy to get wrong" of
`ENGPENK_PEPTIDE_WETLAB.md` (2026-08-06). Everything else in that sheet stands.
**Construct:** `engPENK_therapy_plasmid`, 7× `YGGFEVVG` cassette in pcDNA3.1(+).
**Date:** 2026-08-16. **Basis:** sequence analysis of `engPENK_insert_annotated.gb` vs native PENK (P01210).
**Status:** dry-lab finding. Nothing here has been measured in-house.

---

## 0. Why you are getting this sheet

The original reference sheet told you to order the **free acid** because the proprotein
releases the peptide by proteolysis, which leaves a free carboxylate. That reasoning is
correct for the *convertase* step and it is **incomplete**: the cassette ends in **Gly**,
and the same granules that do the cutting also contain **PAM**
(peptidylglycine α-amidating monooxygenase). PAM consumes a C-terminal Gly and amidates
the residue in front of it.

Native PENK cores end in Met or Leu (`YGGFM`, `YGGFL`) and are therefore **not** PAM
substrates. This is the one respect in which the engineered cassette behaves differently
from native PENK, and it changes the identity of the product.

```
cassette as built:   ...KR-YGGFEVVG-KR...
  convertase + CPE ->  YGGFEVVG        free acid, 827.3934 [M+H]+
  then PAM         ->  YGGFEVV-NH2     769.3879 [M+H]+   <-- 7-mer, amide on VAL
```

The MD and docking work in this project scored a **deltorphin-II-like** ligand, which is
`Y-a-F-E-V-V-G-NH2`: amide on **Gly**. The cassette as built cannot produce that geometry.

---

## 1. Decision required before any cloning proceeds

| Option | Cassette | Granule product | Consequence |
|---|---|---|---|
| **A: leave as built** | `YGGFEVVG` | `YGGFEVV-NH₂` (769.3879) | 7-mer, amide on Val. Not the species that was modelled; the δ-selectivity predictions do not transfer without re-scoring. |
| **B: add one Gly** | `YGGFEVVGG` | `YGGFEVVG-NH₂` (826.4094) | Matches deltorphin-II C-terminal geometry. **One codon.** Cheap now, expensive after cloning. |

This is a design decision, not a bench decision, but it gates the peptide order, so it has
to be made first. If B is chosen, the insert must be re-synthesised and the QC protocol
fragment sizes in `engPENK_therapy_qc_protocol.md` shift by 3 bp per cassette (21 bp total).

---

## 2. Corrected peptide order

Order **three** peptides, not two. All all-L, no D-residues anywhere.

| # | Sequence | C-terminus | Monoisotopic [M+H]⁺ | Why you need it |
|---|---|---|---|---|
| 1 | `YGGFEVVG` | **free acid** | 827.3934 | unamidated fraction, the species already docked/scored |
| 2 | `YGGFEVV` | **amide** | 769.3879 | the PAM product from the cassette as built |
| 3 | `YGGFM` | free acid | 574.2330 | native Met-enkephalin comparator, and present in your cells |

If option B is taken, add `YGGFEVVG`-**NH₂** (826.4094) as #4.

> **Vendor trap, this is where the 0.98 Da bites.** Free acid and amide of the *same*
> sequence differ by only 0.98 Da. The amide's first ¹³C peak (827.4127) sits
> 0.0193 Da from the free acid's monoisotopic peak (827.3934), **R ≈ 42,784 FWHM**
> to separate them. Many vendors default to C-terminal amide. Specify the terminus in
> writing on the order, and QC the delivered standard on a high-resolution instrument
> (Orbitrap or high-end TOF), a quadrupole or ion trap **cannot** tell you which one arrived.

---

## 3. What to expect in transfected-cell supernatant

Five species from the construct as built. Within a single construct the amidation readout is
a clean **58.01 Da** shift, unambiguous on any instrument. The high-resolution
requirement above applies to *standards*, not to this measurement.

| Species | [M+H]⁺ | Origin |
|---|---|---|
| `YGGFEVV-NH₂` | 769.3879 | cassettes 1,2,3,5,6 after PAM |
| `YGGFEVVG` | 827.3934 | cassettes 1,2,3,5,6, PAM-incomplete fraction |
| `YGGFEVVGRF` | 1130.5629 | **cassette 7**, monobasic flank, extended |
| `YGGFEVVGRGL` | 1153.6000 | **cassette 4**, monobasic flank, extended |
| `YGGFM` | 574.2330 | endogenous native Met-enkephalin |

**Cassettes 4 and 7 will not give clean product.** All seven cassettes have a dibasic KR
upstream, but 4 and 7 sit at the native positions of Met-enkephalin-Arg-Gly-Leu and
-Arg-Phe and inherit those monobasic downstream flanks. CPE removes the Arg but not Gly-Leu
or Phe, so roughly **2 of 7** of the yield is C-terminally extended and pharmacologically
distinct. Expect these peaks; they are not contamination. Fixing them means giving cassettes
4 and 7 their own dibasic downstream flank.

---

## 4. What does *not* need changing

Verified against native PENK, computed from the sequences:

- **Signal peptide** residues 1–24, removed co-translationally. Mature chain 264 aa.
- **Disulfides:** 6 Cys in the mature chain → **3 disulfides, same count as native**.
  The cassettes contain no Cys, so they cannot scramble native pairing.
- **N-glycosylation:** two sequons, N133 (NGS) and N161 (NSS), both **native** sequons,
  displaced only by the upstream insertions. No new glycosylation liability.
- **Where cleavage happens:** trans-Golgi onward, not the ER. PC1/3 and PC2 (with 7B2) are
  themselves pro-enzymes in the ER and only mature in the acidic, high-Ca²⁺ TGN. The
  proprotein transits the rough ER intact, which is what a 7-cassette tandem construct
  needs.

---

## 5. One thing worth measuring that nobody has asked for yet

Each cassette replaces a Met-containing native core with an acidic one, so the mature chain
carries **41 Glu against 34** in native: **−15.4 e vs −8.4 e at pH 7.2**, holding ~7 e more
negative at every compartment pH along the pathway.

Dense-core granule sorting runs on pH- and Ca²⁺-dependent self-aggregation in the TGN. Extra
carboxylates could bridge Ca²⁺ better *or* raise solubility and resist condensation, it
could go either way. **This is a prediction, not a result.** The experiment is cheap:

1. Transfect engPENK and native-PENK in the same cell line, same passage.
2. Split supernatant vs. cell lysate; quantify peptide in both by the MS method above.
3. Compare the **secreted : cell-associated** ratio between constructs.
4. Check for constitutive (unregulated) release, secretion without a secretagogue.

A construct that mis-sorts will show up as high constitutive release and low
cell-associated peptide, and that would be a formulation problem, not a peptide problem.

---

## 6. Bench checklist

- ☐ **Design decision A or B made and recorded** (§1), blocks everything else
- ☐ Peptide order placed with **C-terminus specified in writing** (§2)
- ☐ Delivered standards QC'd on high-resolution MS before use (§2)
- ☐ MS method includes all five expected species, not just the octapeptide (§3)
- ☐ Sorting experiment scheduled with native-PENK control in the same cell line (§5)
- ☐ If option B: insert re-synthesised, QC fragment sizes recomputed (§1)
