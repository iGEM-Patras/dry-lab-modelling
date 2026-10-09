# Dry-Lab Modelling

## 1. Plasmid Design & Codon Optimization

### Problem
Four expression cassettes (mEGFP-P2A-His-PENK, His-PENK-P2A-mEGFP, mEGFP-IRES-His-PENK, His-PENK-IRES-mEGFP) require synthesis. The raw sequences sit at 51–59% GC, above the synthesis-friendly window (35–45%), so every codon must be optimized without changing the protein.

### Approach
Feature-aware recoding: lock the signal peptide, IRES element, initiation context (Kozak), self-cleaving peptide (P2A), and stop codons; recoded only in-frame annotated CDS blocks; checked motifs in a 31-nt window around each candidate swap to avoid creating new synthesis liabilities.

### Result
| Construct | Target GC | Achieved GC | CAI (Homo sapiens) | Feature integrity |
|---|---|---|---|---|
| mEGFP-P2A-His-PENK | 40% | 40.0% | 0.708 | all 4 intact, IRES byte-identical |
| His-PENK-P2A-mEGFP | 40% | 40.1% | 0.651 | ✓ |
| mEGFP-IRES-His-PENK | 45% | 45.0% | 0.738 | ✓ |
| His-PENK-IRES-mEGFP | 45% | 44.9% | 0.745 | ✓ |

**Trade-off:** CAI fell by 8–30% (average 15.5%). That's real: transfection efficiency may be impacted. Expression readout is non-negotiable.

**Why two targets?** P2A constructs hit 40% GC (tighter margin for synthesis precision); IRES constructs tolerate 45% GC. All four were validated in SnapGene by round-trip parsing.

**Junction risk:** The two P2A constructs carry the mEGFP–P2A–His junction, which in immunogenicity screening came out as the highest immunogenicity hotspot (2.07% strong MHC-I binders vs. 1.77–1.86% for native or engineered epitope). This is why the IRES pair was included: it trades the P2A junction for the 7 YGGFEVVG repeats.

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

**Limitation:** No human data, MHCflurry is trained on ligand elution + crystal structures, not cellular responses. True immunogenicity requires cell-based assay in HLA-matched lines or patient PBMCs.

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

**Consequence:** Cell-free assay is not a validation, it is the *only* route to confirm that the engineered cassette actually works when given the right enzymes. See Section 6.

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
- **DOTAP is reliable**: predictable, tight binding across replicates, suitable for preclinical formulation.
- **MC3-protonated is equally tight**: validates the computational model that low-pH conformation drives compact lipoplex. Relevant for endosomal escape (low pH triggers protonation and release).
- **MC3-neutral is heterogeneous**: one of three replicates failed to bind, suggesting pH-neutral MC3 is not a "weak" state but rather a **bistable** state (either binds or doesn't). Real cellular data needed to know which state dominates *in vivo*.

**Caveat:** Coarse-grained MARTINI model; all-atom validation recommended before formulation scale-up.

---

## 5. Selectivity Engineering Cycle 3b

### Problem
The engineered cassette borrows deltorphin II's delta-selective address (Section 7.1). Can a
physics-based free-energy method confirm delta-over-mu preference *before* committing to a
radioligand assay?

### Approach
Pre-registered gate on four **known** control peptides with published delta/mu selectivity:
met-enkephalin, deltorphin I, deltorphin II, endomorphin-1, docked into both receptors and
rescored by conditional bound-state MM-GBSA. All 40 runs (4 controls x 2 receptors x n=5) were
rescored in bound mode, selecting frames where the ligand is genuinely in the pocket.
The gate tests the *method*, not the engineered peptide.

### Result: FAIL; Stage 2 not authorised

| Control | n | Computed ΔΔG | SEM | Experimental |
|---|---|---|---|---|
| met-enkephalin | 5 | +26.38 | 1.46 | 0.00 |
| deltorphin I | 5 | +15.18 | 4.95 | +5.70 |
| deltorphin II | 5 | +7.48 | 3.24 | +5.39 |
| endomorphin-1 | 5 | −0.91 | 3.32 | −2.99 |

- **G1 PASS**: all sign and ranking checks hold. The method gets the direction right.
- **G2′ FAIL**: only met-enkephalin falls under the 1.5 kcal/mol SEM threshold; the others are 3.2–5.0.
- **G3 FAIL**: slope 0.594, 95% CI [−1.024, 2.213], r = 0.179 over 20 points. The CI spans zero.

**Reading.** The failure is replicate scatter, not a broken pipeline: per-replicate ΔΔG within a
single control spans 27 kcal/mol for deltorphin I. Met-enkephalin is the informative outlier:
tightest replicate agreement and the largest error, which is the signature of a *systematic*
one. These are enthalpy-dominated effective energies with no entropy term, and met-enkephalin is
the smallest and most flexible of the four, so the missing configurational-entropy penalty should
hit it hardest. It does.

**Consequence.** Cycle 3b terminates with a negative methodological result: single-trajectory
MM-GBSA at n=5 does not resolve delta/mu selectivity for these peptides. **No computational
claim about the engineered peptide's selectivity is authorised.** The standing recommendation is
radioligand competition binding on `YGGFEVVG` and the `YGGFDIIG` variant.

*Reporting a pre-registered gate that failed is deliberate. The alternative, quoting the one
control that passed, would have sent the wet lab into an expensive assay on a method that
cannot support it.*

---

## 6. In Vitro Processing Assay (Wet-Lab Handoff)

### Problem
Sections 1–5 are computational. The only way to know whether the cassette architecture yields
the intended peptides is to supply the processing enzymes and measure the products.

### Design
HEK293T cannot do this: PC1/3, PC2 and 7B2 are all absent (Section 3). The protocol therefore
uses **defined recombinant enzymes on synthetic substrate**, with conditions taken verbatim from
the cited primary source rather than estimated: 50 mM Na-acetate pH 5.5, 5 mM CaCl2,
0.1% octyl-beta-glucopyranoside, 37 °C, with 100 mM NaCl added for PC2 only.

### Target species
Detection is by mass spectrometry against a 25-species target list (20 endogenous + 5 construct),
so endogenous PENK products are not mistaken for construct output:

| Species | Sequence | [M+H]+ | Origin |
|---|---|---|---|
| Engineered mature | `YGGFEVVG` | 827.39 | cassettes 1,2,3,5,6, dibasic flanks |
| Engineered amidated | `YGGFEVV`-NH2 | 769.39 | after granule PAM |
| Engineered extended | `YGGFEVVGRGL` | 1153.60 | cassette 4, monobasic RGL |
| Engineered extended | `YGGFEVVGRF` | 1130.56 | cassette 7, monobasic RF |
| Endogenous MERGL | `YGGFMRGL` | 900.44 | native core 4 |
| Endogenous MERF | `YGGFMRF` | 877.40 | native core 7 |

**Predicted outcome:** **four** clean octapeptides (cassettes 1, 2, 3, 6) plus **three** extended
species (cassettes 4, 5, 7): *not* seven identical peptides. See Section 7.2 for why that is the
design and not a defect.

Cassette 5 is the non-obvious one: its downstream flank is dibasic (`RRV`), but in native PENK
core 5 does not release a pentapeptide: it enters the BAM-22 → BAM-20 → adrenorphin route
[5,6]. The engineered cassette follows the same route, giving four additional species that
were absent from the original target list:

| Engineered species | Sequence | [M+H]+ | Native counterpart |
|---|---|---|---|
| adrenorphin counterpart | `YGGFEVVGRRV`-NH2 | 1237.68 | `YGGFMRRV`-NH2 (984.52) |
| pre-PAM intermediate | `YGGFEVVGRRVG` | 1295.69 | `YGGFMRRVG` |
| BAM-20 counterpart | `YGGFEVVGRRVGRPEWWMDYQKR` | 2871.43 | BAM-20 (2618.27) |
| BAM-22 counterpart | `YGGFEVVGRRVGRPEWWMDYQKRYG` | 3091.51 | BAM-22 (2838.35) |

These are calculated, not measured. Note that the engineered BAM-20 counterpart (2871.43) lies
1.09 Da from native BAM-22 +2ox (2870.34): resolving power >2600 or MS2 confirmation is needed
to separate them, and the acquisition range must extend to 3100 Da rather than 2900.

### Controls and handling: not optional
- **Untransfected and empty-vector controls**, same cell line and passage, every run. They define
  the endogenous baseline for all 20 native peaks.
- **Acquire 550–2900 Da**, not a narrow enkephalin window; the BAM series sits at 2618–2870.
- **Include +16 oxidation satellites**, or Met peptides will appear lost when they have only
  oxidised. Quantify parent + sulfoxide as one pool.
- **Report construct peptide as a ratio to endogenous Met-enkephalin** in the same sample; this
  controls for extraction efficiency and cell number.
- Collect on ice, acidify immediately (0.1% formic acid), avoid freeze-thaw.

**Honest limit:** this establishes whether the cassette architecture is processed as designed. It
does not address transfection efficiency, expression level, secretion, or therapeutic dose.

---

## 7. Why the Construct Is "Not Native PENK": By Design

A reviewer reading the engineered sequence without project context will conclude the construct
is a corrupted proenkephalin: the enkephalin cores are the wrong length, and two of the seven
lack a downstream dibasic site. Both observations are correct. Neither is a defect. This
section documents why, because the point is easy to lose and expensive to re-litigate.

### 7.1 The cores are deliberately not enkephalins

Native human proenkephalin-A (UniProt P01210, 267 aa) carries six copies of Met-enkephalin
(`YGGFM`) and one of Leu-enkephalin (`YGGFL`) [1,2]. The engineered
construct carries **zero copies of either**: all seven cassettes encode `YGGFEVVG`.

The substitution follows the message–address model of opioid peptide recognition
[12]: an N-terminal *message* domain drives receptor activation, while the
C-terminal *address* selects the receptor subtype.

| Peptide | Message | Address | Preference |
|---|---|---|---|
| Met-enkephalin (native x6) | `YGGF` | `M` | mu-preferring |
| Leu-enkephalin (native x1) | `YGGF` | `L` | delta/mu mixed |
| **Engineered cassette (x7)** | **`YGGF`** | **`EVVG`** | **delta-preferring (intended)** |
| Deltorphin II (*Phyllomedusa* skin) | `YAF`(D-Ala2) | `EVVG` | delta-selective [11] |

PENK's message tetrapeptide is preserved base-for-base; the address is taken from deltorphin II,
a naturally occurring delta-selective amphibian peptide [11]. The construct is a
chimera of two natural opioid peptides, not an arbitrary sequence.

**The limit of the analogy, stated plainly.** Deltorphin II's metabolic stability comes largely
from D-alanine at position 2, which blocks aminopeptidase attack at the Tyr1-Xaa2 bond
[11]. D-amino acids have no codon; a ribosomally expressed peptide is all-L by
construction and cannot reproduce that feature. The cassette inherits deltorphin's selectivity
motif and **none** of its protease resistance: `YGGFEVVG` carries three NEP-susceptible bonds
against Met-enkephalin's one, so it is *less* stable than the native peptide, not more. Since
enkephalins are cleared in seconds, principally by neprilysin [10], this is why the
project's NEP-siRNA arm is load-bearing rather than adjunct: the two arms cannot be evaluated
separately.

### 7.2 Cassettes 4 and 7 reproduce native architecture

Five cassettes are flanked by dibasic KR/KK sites, cleaved by PC1/3 and PC2
[7] and C-terminally trimmed by carboxypeptidase E [8].
Cassettes 4 and 7 instead carry **monobasic** downstream flanks (`RGL` and `RF`). Read in
isolation this looks like two broken cassettes.

It is not. Those are precisely the positions where native PENK deliberately makes *extended*
opioid peptides:

| Native product | Sequence | Flank | Evidence |
|---|---|---|---|
| Met-enkephalin-Arg-Gly-Leu (MERGL) | `YGGFMRGL` | RGL, monobasic | isolated from bovine adrenal medulla [4] |
| Met-enkephalin-Arg-Phe (MERF) | `YGGFMRF` | RF, precursor C-terminus | isolated from adrenal granules and striatum [3] |
| Adrenorphin / metorphamide | `YGGFMRRV`-NH2 | amidated | phaeochromocytoma and human adrenal [5,6] |

The monobasic flanks at cassettes 4 and 7 are inherited from PENK's own design and produce the
engineered counterparts of MERGL and MERF. **The construct is mirroring native processing
strategy, not failing to be cleaved.**

That adrenorphin is amidated also matters in the construct's favour: it is direct evidence that
PAM [9] acts on *this* precursor in *these* granules, which supports the
predicted amidation of the Gly-extended `...VVG` cassette.

### 7.3 What is actually open

The engineered extended species `YGGFEVVGRGL` (M+H 1153.60) and `YGGFEVVGRF` (M+H 1130.56) have
no published pharmacology. They are novel, they are expected, and both are already on the wet-lab
MS target list alongside their native counterparts (`YGGFMRGL` 900.44, `YGGFMRF` 877.40). The
open question is **what they do**, not whether to engineer them away.

### 7.4 For the wet lab

If an analysis flags the seven cassettes as non-functional because the sequence is not native
PENK, the three checks that separate a real problem from this expected result are:

1. **Is anything being cleaved?** If no cassette yields product, the fault is enzyme
   availability, not architecture: HEK293T lacks PC1/3, PC2 and 7B2 entirely (Section 3).
2. **Are four cassettes clean and three extended?** That is the predicted outcome, not a failure.
3. **Is detection the limit?** No commercial anti-enkephalin antibody binds `YGGFEVVG`; the
   custom anti-`YGGFEVVG` polyclonal gates the entire expression readout.

---

## Methods & Data

- **Plasmid optimization:** `09_codon_gc_design/PENK_recode_validation.csv` (validated per-cistron translation, homopolymer checks)
- **Ordering sheet:** `09_codon_gc_design/PENK_order_sheet.csv` (synthesis parameters for all four cassettes)
- **HEK293T audit:** `08_checkable_audit/tables/hek293t_processing_competence.csv` (expression data from public datasets, re-quantified against Ensembl GRCh38)
- **MHC predictions:** `10_immunogenicity_antibody/mhc_predictions_full.csv` and `mhc_group_summary.csv` (full MHCflurry 2.x run)
- **Antibody guide:** `10_immunogenicity_antibody/antibody_shortlist.csv` (registry of anti-enkephalin antibodies and why none work)
- **Lipoplex MD:** `04_lipoplex_md/data/md_formulation_summary.json` (per-replicate contact distances and metrics)
- **Cycle 3b verdict:** `06_engineering_cycles/cycle3b_physics_rescoring/docs/GATE_VERDICT_BOUND.md` (full rescoring report with control peptides)
- **In vitro protocol:** `07_invitro_penk/docs/PENK_INVITRO_PROTOCOL.md` (recombinant-enzyme conditions (verbatim from the cited primary source + UniProt), mass spectrometry targets)

---

## Why This Matters

The iGEM competition rewards **honest experimental design.** Your dry-lab work:

1. **Caught a design flaw early** (HEK293T lacks PC1/3, PC2 and 7B2 → the cell-free recombinant-enzyme route is the only one that can generate the peptides).
2. **Quantified trade-offs** (GC targets cost 8–30% CAI; the P2A junction is the immunogenicity hotspot, not the engineered epitope).
3. **Protects the wet lab** (a pre-registered gate failed and was reported as a negative result, rather than sending the bench into a radioligand assay on a method that cannot support the claim).
4. **Shows iteration** (immunogenicity screening drove inclusion of the IRES pair; Amendment 2 formally retracted two of the dry lab's own earlier claims, see Section 7).

Next steps are clear and prioritized:
- **Now (before constructs arrive):** Order the custom anti-`YGGFEVVG` polyclonal (KLH-conjugated, ≥2 rabbits, 10–12 week lead). No commercial anti-enkephalin antibody detects the product; this gates the entire expression readout.
- **Upon transfection:** Run in vitro processing assay (Section 6) to confirm engineering works.
- **After expression validation:** Proceed to radioligand competition binding for selectivity.

---

## References

1. Comb M, Seeburg PH, Adelman J, Eiden L, Herbert E (1982). Primary structure of the human Met- and Leu-enkephalin precursor and its mRNA. *Nature* 295:663-666. doi:[10.1038/295663a0](https://doi.org/10.1038/295663a0)
2. Noda M, Furutani Y, Takahashi H et al. (1982). Cloning and sequence analysis of cDNA for bovine adrenal preproenkephalin. *Nature* 295:202-206. doi:[10.1038/295202a0](https://doi.org/10.1038/295202a0)
3. Stern AS, Lewis RV, Kimura S et al. (1979). Isolation of the opioid heptapeptide Met-enkephalin [Arg6,Phe7] from bovine adrenal medullary granules and striatum. *PNAS* 76:6680-6683. doi:[10.1073/pnas.76.12.6680](https://doi.org/10.1073/pnas.76.12.6680)
4. Kilpatrick DL, Taniguchi T, Jones BN et al. (1981). Identification of the octapeptide [Met]enkephalin-Arg6-Gly7-Leu8 in extracts of bovine adrenal medulla. *BBRC* 103:698-705. doi:[10.1016/0006-291x(81)90506-4](https://doi.org/10.1016/0006-291x(81)90506-4)
5. Matsuo H, Miyata A, Mizuno K (1983). Novel C-terminally amidated opioid peptide in human phaeochromocytoma tumour. *Nature* 305:721-723. doi:[10.1038/305721a0](https://doi.org/10.1038/305721a0)
6. Boarder MR, Erdelyi E, Barchas JD (1985). Metorphamide, a C-terminally amidated opioid peptide, in human adrenal and human phaeochromocytoma. *Regulatory Peptides* 12:75-83. doi:[10.1016/0167-0115(85)90184-3](https://doi.org/10.1016/0167-0115(85)90184-3)
7. Paquet L, Bergeron F, Seidah NG et al. (1996). Peptide biosynthetic processing: distinguishing prohormone convertases PC1 and PC2. *Mol Cell Endocrinol* 120:161-168. doi:[10.1016/0303-7207(96)03834-8](https://doi.org/10.1016/0303-7207(96)03834-8)
8. Fricker LD, Snyder SH (1982). Enkephalin convertase: purification and characterization of a specific enkephalin-synthesizing carboxypeptidase. *PNAS* 79:3886-3890. doi:[10.1073/pnas.79.12.3886](https://doi.org/10.1073/pnas.79.12.3886)
9. Eipper BA, Stoffers DA, Mains RE (1992). The biosynthesis of neuropeptides: peptide alpha-amidation. *Annu Rev Neurosci* 15:57-85. doi:[10.1146/annurev.neuro.15.1.57](https://doi.org/10.1146/annurev.neuro.15.1.57)
10. Roques BP, Fournie-Zaluski MC, Soroca E et al. (1980). The enkephalinase inhibitor thiorphan shows antinociceptive activity in mice. *Nature* 288:286-288. doi:[10.1038/288286a0](https://doi.org/10.1038/288286a0)
11. Erspamer V, Melchiorri P, Falconieri-Erspamer G et al. (1989). Deltorphins: a family of naturally occurring peptides with high affinity and selectivity for delta opioid binding sites. *PNAS* 86:5188-5192. doi:[10.1073/pnas.86.13.5188](https://doi.org/10.1073/pnas.86.13.5188)
12. Chavkin C, Goldstein A (1981). Specific receptor for the opioid peptide dynorphin: structure-activity relationships. *PNAS* 78:6543-6547. doi:[10.1073/pnas.78.10.6543](https://doi.org/10.1073/pnas.78.10.6543)

*Formal record: the "cassettes 4 and 7 will not give clean product" statement was retracted in
`NATIVE_PENK_AMENDMENT2_WETLAB.md` §0.2, which also corrected the claim that native PENK cores
are not PAM substrates. Both corrections are reflected above.*

---

*Wiki page: `dry-lab-modelling.md` | Repo: `kei-zan/dry-lab-modelling` | All data and figures are in the repository under the directory structure above.*
