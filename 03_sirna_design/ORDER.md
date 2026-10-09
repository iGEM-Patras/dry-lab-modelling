# siRNA order sheet: anti-neprilysin (MME)

**Single source of truth. Where any other document in this directory disagrees, this one
is current.** Revised after an error was found in the first DSIR lookup, see the
correction log at the end.

Coordinates are **MME-213 (`ENST00000615825.3`, 5,861 nt)**. **Order by sequence, never by
position number.**

---

## The decision, stated honestly

**No single guide is best on both axes, and the one that was is disqualified by a
population variant.** Predicted efficacy and measured specificity are close to independent
here, so a guide optimal for one is typically mid-pack on the other. The five efficacy
models also agree poorly with one another (mean pairwise Spearman **+0.26**; Katoh is
*anti*-correlated with the other four at -0.14 to -0.27), so no single efficacy number
deserves much weight. Specificity, by contrast, is counted rather than predicted.

**Order two guides spanning the trade-off and let qPCR decide.**

---

## 1: specificity-optimal  (recommended primary)
```
position (MME-213)  2700-2722
guide     (antisense, 5'->3')   AAUGAUUGACUUGAUAGACCU
passenger (sense,     5'->3')   GUCUAUCAAGUCAAUCAUUUC
```
Best specificity of the shortlist (mean rank **3.62** of 17) and **highest target
accessibility** (0.658). Only **2** off-targets at 3 mismatches, **423** 8mer seed
sites, seed-duplex Tm **13.7 °C**.

Predicted efficacy is mid-pack: DSIR **85.4** (rank 839 of 5,841, below the >90
'efficient' threshold), consensus efficacy rank 11.2 of 17.

## 2: efficacy-optimal  (recommended second)
```
position (MME-213)  2459-2481
guide     (antisense, 5'->3')   UUCAUGUAUGAAUUCUUGCGG
passenger (sense,     5'->3')   GCAAGAAUUCAUACAUGAAUC
```
**Best predicted efficacy of the shortlist on four of five models**: DSIR **100.8**
(rank 16 of 5,841), s-Biopredsi 0.881, iScore 81.9, Dharmacon 81.5;
consensus efficacy rank **2.2**.

Its cost is specificity: 18 off-targets at 3 mismatches, 859 8mer seed sites,
seed Tm 21.6 °C, accessibility 0.513.

**Include a scrambled control.** Nothing here measures knockdown; qPCR at 48 h does.

---

## Worth a decision: `1023-1045`
```
guide     (antisense, 5'->3')   UCGAUCUUCAGGUUUAGCCGU
passenger (sense,     5'->3')   GGCUAAACCUGAAGAUCGAAA
```
This is the only guide strong on **both** axes: efficacy rank 4.6, specificity rank 4.88,
DSIR 96.4, only 82 8mer seed sites and 3 off-targets.

It was excluded because a **common population variant (1.92% alternate-allele frequency)**
sits under the target site. That is a liability for a therapeutic, where a patient carrying
the variant would be a non-responder. **It is not a liability for a cell-line knockdown**:
HEK293T has one genotype, checkable in one sequencing read.

If the immediate goal is demonstrating knockdown, this guide is arguably the best choice
available. If the goal is a candidate that carries forward to the therapeutic, leave it out.
That is a project-strategy call, not a data call.

---

## Do NOT order

| position | reason |
|---|---|
| 2225-2247 | consensus efficacy rank 9.3, specificity rank 12.5: weak on both |
| 2562-2584 | lowest seed burden of all (91 8mer sites) but consensus efficacy rank 11.6, DSIR 77.8 (rank 2,076) |

---

## Correction log

**2026-10-03: the first DSIR figures in this directory were wrong.** Guides were matched
to the DSIR server output on the *sense 19-mer*, but DSIR's window is offset 2 nt from
siDirect's, so the score read belonged to a neighbouring siRNA. Caught by re-scoring
offline with the DSIR weights shipped in `nkvamaks/oligoshell_calc` and finding a
disagreement. The correct join is on the guide sequence itself; all 206 siDirect guides
then match a DSIR row, and the offline re-score agrees with the server to 0.000.

| guide | reported | correct |
|---|---|---|
| 2700-2722 | 92.6 | **85.4** |
| 2562-2584 | 91.5 | **77.8** |
| 435-457 | 76.7 | **83.7** |

Two claims built on those numbers are withdrawn: that 2700-2722 clears DSIR's >90
threshold (it does not), and that 2562-2584 should replace 435-457 because it clears the
threshold (the reverse is true: 435 scores higher). The specificity and accessibility
figures were never DSIR-derived and are unaffected.

## How each number was obtained

| criterion | source |
|---|---|
| functional rule, seed-duplex Tm, genome-wide specificity | siDirect (Ui-Tei; RefSeq release 230) |
| predicted efficacy, 5 models | `nkvamaks/oligoshell_calc`, validated against the DSIR server to 0.000 over 400 candidates |
| target accessibility | ViennaRNA RNAplfold, W=240 L=160 u=21 |
| seed-mediated off-target burden | 7mer-m8 / 8mer counted across 20,094 canonical human 3' UTRs (Ensembl BioMart); independently corroborated by OligoShell's POTS table at Spearman +0.89 |
| isoform coverage | all four MME RefSeq variants |
| population variants | Ensembl, alternate-allele frequency across gnomAD and 1000 Genomes |
| co-delivery safety | exhaustive match against the four engPENK plasmids, both strands, circular |

