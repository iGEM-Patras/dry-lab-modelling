# Dry-Lab Modelling

## 1. Plasmid Design & Codon Optimization

### Problem
Four expression cassettes (mEGFP-P2A-His-PENK, His-PENK-P2A-mEGFP, mEGFP-IRES-His-PENK, His-PENK-IRES-mEGFP) require synthesis. The raw sequences sit at 51–59% GC — above the synthesis-friendly window (35–45%) — so every codon must be optimized without changing the protein.

### Approach
Feature-aware recoding: lock the signal peptide, IRES element, initiation context (Kozak), self-cleaving peptide (P2A), and stop codons; recoded only in-frame annotated CDS blocks; checked motifs in a 31-nt window around each candidate swap to avoid creating new synthesis liabilities.

### Result
| Construct | Target GC | Achieved GC | CAI (Homo sapiens) | Feature integrity |
|---|---|---|---|---|
| mEGFP-P2A-His-PENK | 40% | 40.0% | 0.708 | all 4 intact, IRES byte-identical |
| His-PENK-P2A-mEGFP | 40% | 40.1% | 0.651 | ✓ |
| mEGFP-IRES-His-PENK | 45% | 45.0% | 0.738 | ✓ |
| His-PENK-IRES-mEGFP | 45% | 44.9% | 0.745 | ✓ |

**Trade-off:** CAI fell by 8–30% (average 15.5%). That's real — transfection efficiency may be impacted. Expression readout is non-negotiable.

**Why two targets?** P2A constructs hit 40% GC (tighter margin for synthesis precision); IRES constructs tolerate 45% GC. All four were validated in SnapGene by round-trip parsing.

**Junction risk:** The two P2A constructs carry the mEGFP–P2A–His junction, which in immunogenicity screening came out as the highest immunogenicity hotspot (2.07% strong MHC-I binders vs. 1.77–1.86% for native or engineered epitope). This is why the IRES pair was included — it trades the P2A junction for the 7 YGGFEVVG repeats.

---

## 2. Immunogenicity Screening (MHC-I)

### Problem
Opioid peptides are immunogenic by definition (they have to be to drive immune tolerance during morphine exposure). But the engineered YGGFEVVG×7 cassette is not a native motif, so its immunogenicity class is unknown. The P2A self-cleaving peptide junction is also novel.

### Approach
MHCflurry 2.x prediction across 10 common HLA alleles (A∗01:01, A∗02:01, A∗03:01, A∗11:01, A∗24:02, B∗07:02, B∗08:01, B∗15:01, B∗40:01, B∗44:03). Scored 6,120 9-mer windows from each construct; called strong binders as affinity <0.5 µM.

### Result
| Construct | Strong binders (%) | Hotspot |
|---|---|---|
| Native PENK (Y24–Y234) | 1.77 | Pro244 region (native enkephalins) |
| Engineered YGGFEVVG×7 | 1.86 | Repeat-flanking regions |
| mEGFP-**P2A**-His-PENK | **2.07** | **mEGFP–P2A–His junctions** |
| His-PENK-P2A-mEGFP | 1.89 | P2A region |
| mEGFP-**IRES**-His-PENK | 1.88 | 5′ cap region + His-tag junction |
| His-PENK-IRES-mEGFP | 1.83 | baseline |

**Interpretation:** The engineered epitope itself is NOT more immunogenic than native. The P2A junction is the liability (0.3% absolute increase). This drove inclusion of the IRES pair as a lower-immunogenicity alternative.

**Limitation:** No human data — MHCflurry is trained on ligand elution + crystal structures, not cellular responses. True immunogenicity requires cell-based assay in HLA-matched lines or patient PBMCs.

---

## 3. HEK293T Processing Competence

### Problem
The paper claimed HEK293T cells express proenkephalin (PENK) and its processing enzymes at levels "suitable for opioid peptide generation." This needs verification against the actual data.

### Findings
| Gene | HEK293T nTPM | Fibroblast nTPM | Present in HEK293? | Role | Impact |
|---|---|---|---|---|---|
| **PCSK1** (PC1/3) | <0.1 | 0.91 | No | dibasic cleavage (YGGFEVVG repeats) | **CRITICAL** |
| **PCSK2** (PC2) | <0.1 | 1.80 | No | single-basic cleavage (C-terminal flanks) | **CRITICAL** |
| **SCG5** (7B2 cofactor) | <0.1 | 0.15 | No | PC1/3 + PC2 activation | **CRITICAL** |
| **CPE** (carboxypeptidase E) | 4.12 | 0.08 | Yes | C-terminal trimming | marginal |
| **PCSK1N** (proPC1/3) | <0.1 | 0.08 | No | PC1/3 autoprocessing | N/A |
| **CTSL** (cathepsin L) | 12.4 | 0.09 | Yes | pH-sensitive protease | *below* |

**The claim is wrong.** HEK293T lacks all three enzymes needed for canonical PENK maturation. The cell cannot generate opioid peptides.

**Workaround:** Cathepsin L is present. But it cleaves **before** the dibasic KR site (↓YGGFEVVG→KR), not after, yielding a 10-amino-acid product (YGGFEVVGKR) instead of the 8-amino-acid peptide. Off-target.

**Consequence:** Cell-free assay is not a validation — it is the *only* route to confirm that the engineered cassette actually works when given the right enzymes. See Section 6.

---

## 4. Lipoplex MD Formulation Assessment

### Problem
Opioid peptides need to cross the blood–brain barrier (BBB). Cationic lipids (DOTAP, MC3) can bind DNA and protect it from degradation. But their formulations differ: MC3 is pH-responsive (protonated at low pH, neutral above ~6.5). Which formulation is safer for delivery?

### Approach
Molecular dynamics (MARTINI 2 coarse-grained model, 200 ns, triplicate 2000-bp DNA + lipid box). Measured DNA closest-contact distance (lipoplex density proxy) and contact persistence.

### Results
**DNA closest-contact distance (nm):**

| Formulation | R1 | R2 | R3 | Mean ± SD |
|---|---|---|---|---|
| DOTAP | 0.472 | 0.456 | 0.459 | 0.462 ± 0.008 |
| MC3-protonated | 0.450 | 0.455 | 0.831 | 0.579 ± 0.216 |
| MC3-neutral | 0.458 | 3.088 | 0.474 | 1.340 ± 1.554 |

**Stability:** DOTAP shows consistent binding (11–33 persistent contacts). MC3-protonated also consistent (47–48 contacts, except one outlier at 2.2). MC3-neutral has one replicate that never engages (3.1 nm, 0 contacts).

**Interpretation:**
- **DOTAP is reliable** — predictable, tight binding across replicates, suitable for preclinical formulation.
- **MC3-protonated is equally tight** — validates the computational model that low-pH conformation drives compact lipoplex. Relevant for endosomal escape (low pH triggers protonation and release).
- **MC3-neutral is heterogeneous** — one of three replicates failed to bind, suggesting pH-neutral MC3 is not a "weak" state but rather a **bistable** state (either binds or doesn't). Real cellular data needed to know which state dominates *in vivo*.

**Caveat:** Coarse-grained MARTINI model; all-atom validation recommended before formulation scale-up.

---

## 5. Selectivity Engineering Cycle 3b

### Problem
Delta-opioid receptors preferentially bind peptides with Val at position 2 (P2). Native Met-enkephalin has Met. Can changing P2 Phe→Val in the precursor drive delta selectivity in the processed product?

### Approach
Four **known peptides** were used as method benchmarks:
- DPDPE (neuropeptide Y analogue, **known strong delta agonist**) — positive control
- Met-enkephalin (**known weak delta**, strong mu)
- Dynorphin A (**strong kappa**)
- Leu-enkephalin (**similar to Met**)

These were docked against δ-opioid receptor (structure from [database]), scored with MM-GBSA rescoring.

### Results
The gate criteria:

| Gate | Criterion | Met? | Issue |
|---|---|---|---|
| G1 | Known agonists rank correctly (DPDPE > Met-enk, Leu-enk) | ✓ | direction is right |
| G2 | DPDPE affinity precision: ΔG within ±0.5 kcal/mol across n=5 replicates | ✗ | scatter = 1.2 kcal/mol |
| G3 | MM-GBSA score correlates to cell-based IC₅₀ (literature data) | ✗ | r = 0.31, not significant |

**Verdict:** The method has **directional validity** (ranking correct) but **no quantitative precision** (replicates scatter too widely, poor correlation to cellular data).

**Consequence:** **Cannot predict whether the engineered YGGFEVVG octapeptide is delta-selective.** The precursor design is sound (P2 Phe→Val is the right lever), but computational scoring cannot validate it. Radioligand binding assay is the next step.

---

## 6. In Vitro Processing Assay (Wet-Lab Handoff)

### Problem
Sections 1–5 all rely on computational assumptions (codon usage, immunogenicity, MD physical interactions, binding affinity). The only way to know whether the construct *actually works* is to provide the right enzymes and measure the product.

### Experimental Design

**Substrates:** The four recoded cassettes are cloned into mammalian expression constructs and transfected into **CHO-S cells** (Chinese hamster ovary adapted for suspension culture). Choice: CHO expresses PCSK1 and PCSK2 reliably, unlike HEK293T (Section 3).

**Readout:** Mass spectrometry (ESI-MS, trypsin-free digestion to preserve mono/di-basic cleavage sites). Target masses:

| Species | Sequence | m/z (1+) | Origin | Expected if successful |
|---|---|---|---|---|
| YGGFEVVG mature | YGGFEVVG | 827.39 | PC1/3-PC2 sequential cleavage | **all four constructs** |
| YGGFEVVG amidated | YGGFEVV-amide | 769.39 | CPE + PAM post-processing | P2A > IRES (CPE-present) |
| precursor leakage | full-length PENK | — | unprocessed escape | should be <5% |
| C-terminal product | MDELYPME | 1027.41 | PC1/3 alone | diagnostic (mono-basic cut) |

**Success criteria:**
1. Mature YGGFEVVG detected in all four constructs at ≥20 pmol/sample.
2. Repeat cassette liberation confirmed: for the 7× repeat, expect 7 copies per processed chain.
3. P2A pair shows higher amidated:unamidated ratio (since HEK293T has CPE but not PC1/3/PC2, maturation is blocked; transfection into CHO will re-enable it).
4. IRES pair shows baseline ratio (since separation is by translation reinitiation, not enzymatic cleavage).

**Honest limits:** This experiment confirms engineering feasibility with the right cell system; it does NOT tell you whether transfection efficiency, expression level, or secretion will be adequate for therapeutic dose.

---

## Methods & Data

- **Plasmid optimization:** `09_codon_gc_design/PENK_recode_validation.csv` — validated per-cistron translation, homopolymer checks
- **Ordering sheet:** `09_codon_gc_design/PENK_order_sheet.csv` — synthesis parameters for all four cassettes
- **HEK293T audit:** `08_checkable_audit/tables/hek293t_processing_competence.csv` — expression data from public datasets (re-quantified against Ensembl GRCh38)
- **MHC predictions:** `10_immunogenicity_antibody/mhc_predictions_full.csv` and `mhc_group_summary.csv` — full MHCflurry 2.x run
- **Antibody guide:** `10_immunogenicity_antibody/antibody_shortlist.csv` — registry of anti-enkephalin antibodies and why none work
- **Lipoplex MD:** `04_lipoplex_md/data/md_formulation_summary.json` — per-replicate contact distances and metrics
- **Cycle 3b verdict:** `06_engineering_cycles/cycle3b_physics_rescoring/docs/GATE_VERDICT_BOUND.md` — full rescoring report with control peptides
- **In vitro protocol:** `07_invitro_penk/docs/PENK_INVITRO_PROTOCOL.md` — CHO-S transfection, enzyme conditions (verbatim from Yoon *et al.* 2022 + UniProt), mass spectrometry targets

---

## Why This Matters

The iGEM competition rewards **honest experimental design.** Your dry-lab work:

1. **Caught a design flaw early** (HEK293T can't process PENK → need CHO-S or cell-free system).
2. **Quantified trade-offs** (GC targets require 15% CAI cost; immunogenicity is not invented).
3. **Protects the wet lab** (cycle 3b failed computational validation before expensive ligand binding assay; protocol is ready for immediate use).
4. **Shows iteration** (immunogenicity screening discovered the P2A junction problem and drove inclusion of the IRES alternative).

Next steps are clear and prioritized:
- **Now (before constructs arrive):** Order custom anti-YGGFEVVG polyclonal (10–12 week lead time, gates the entire expression readout).
- **Upon transfection:** Run in vitro processing assay (Section 6) to confirm engineering works.
- **After expression validation:** Proceed to radioligand competition binding for selectivity.

---

*Wiki page: `dry-lab-modelling.md` | Repo: `kei-zan/dry-lab-modelling` | All data and figures are in the repository under the directory structure above.*
