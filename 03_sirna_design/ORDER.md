# siRNA order sheet — anti-neprilysin (MME)

**This file is the single source of truth. Where any other document in this directory
disagrees, this one is current.**

Coordinates are **MME-213 (`ENST00000615825.3`, 5,861 nt)** — the transcript the wet lab
supplied and the one siDirect's 206-candidate run used, where its reported positions match
at offset 0. **Order by sequence, never by position number:** three coordinate systems have
been in circulation in this project and only the oligo sequence is invariant.

---

## Order these two

### 1 — PRIMARY
```
position (MME-213)  2700-2722
guide     (antisense, 5'->3')   AAUGAUUGACUUGAUAGACCU
passenger (sense,     5'->3')   GUCUAUCAAGUCAAUCAUUUC
target site on the mRNA         AGGTCTATCAAGTCAATCATTTC
```
DSIR efficacy **92.6** (clears the >90 threshold) · seed-duplex Tm **13.6 °C** ·
**2** off-targets at 3 mismatches · accessibility **0.658** (highest of 17) ·
**423** 8mer seed sites across 20,094 human 3' UTRs.

### 2 — SECOND GUIDE
```
position (MME-213)  2562-2584
guide     (antisense, 5'->3')   UCUUUCGAUUAGAGAAUUCCC
passenger (sense,     5'->3')   GAAUUCUCUAAUCGAAAGAAA
target site on the mRNA         GGGAATTCTCTAATCGAAAGAAA
```
DSIR efficacy **91.5** (clears the >90 threshold) · **91** 8mer seed sites —
the lowest of any non-disqualified guide, six-fold below the background of 1,966 for an
arbitrary 7-mer · seed-duplex Tm 21.0 °C · 9 off-targets · accessibility 0.537.

The pair fails by different mechanisms: the primary is protected by weak seed binding, the
second by having almost no seed sites to bind. Both are plasmid-safe at 7 mismatches,
present in all four MME RefSeq variants, and free of common population variants.

**Include a scrambled control.** Nothing above measures knockdown; qPCR at 48 h does.

---

## Do NOT order

| position (MME-213) | guide | why |
|---|---|---|
| 1023-1045 | `UCGAUCUUCAGGUUUAGCCGU` | common population variant at 1.92% under the target site |
| 2225-2247 | `UUCUGAUAGGCUCUGUAUGCU` | DSIR 71.8, well below the efficacy threshold; 915 8mer seed sites |

---

## Superseded recommendations in this directory

| document | what it says | status |
|---|---|---|
| `SIRNA_V3_SIDIRECT.md` | primary 2541, hedge 2066 / 2403 (`NM_000902.5` coords) | **superseded** — 2541 is this file's 2700-2722; the hedge changed twice since |
| `SIRNA_VALIDATION.md` | primary 2541, hedge 2066 | **superseded** — same primary, different hedge |
| `SIRNA_RERUN_NOTE.md` | primary 2700-2722, hedge 2225-2247 in its middle sections | **partly superseded** — its final section carries the current pair |

The primary has never changed; only its coordinate system and the choice of second guide
have. The second guide moved 2066/2225 -> 435-457 -> 2562-2584 as DSIR efficacy and
measured 3' UTR seed burden were added.

## How each number was obtained

| criterion | source |
|---|---|
| functional rule, seed-duplex Tm, genome-wide specificity | siDirect (Ui-Tei; RefSeq release 230) |
| predicted efficacy | DSIR server (Vert 2006), all 5,841 candidates scored |
| target accessibility | ViennaRNA RNAplfold, W=240 L=160 u=21, parameters from `sirna_design_v2.md` |
| seed-mediated off-target burden | 7mer-m8 / 8mer / 7mer-A1 counted across 20,094 canonical human 3' UTRs from Ensembl BioMart |
| isoform coverage | all four MME RefSeq variants |
| population variants | Ensembl, alternate-allele frequency across gnomAD and 1000 Genomes |
| co-delivery safety | exhaustive match against the four engPENK plasmids, both strands, circular |

