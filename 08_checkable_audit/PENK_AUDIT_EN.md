# Dry-lab audit and wet-lab handoff — engineered proenkephalin project

**Scope.** This report re-runs the project's computational audit against **HEK293T**, the cell line named in the wet-lab guide (*ΑΝΑΛΥΣΗ ΘΕΜΑΤΟΣ*), replacing an earlier analysis that had used cultured fibroblasts. It adds an MHC class I immunogenicity assessment of the engineered `YGGFEVVG` cassette, a construct-level check of all four plasmids, and an error list against the guide. Every quantitative claim is traceable to a named source; DOIs are in §7.

---

## 1. The cell line cannot process the precursor — and that is the experiment

The guide assumes transfected HEK293T will secrete processed enkephalin peptides. It will not.

| Gene | Role | HEK293 (nTPM) | Status |
|---|---|---|---|
| *PCSK1* | PC1/3 — endoproteolysis at dibasic sites | 0.1 | **absent** |
| *PCSK2* | PC2 — principal generator of small opioid peptides | 0.1 | **absent** |
| *SCG5* | 7B2 — obligate PC2 chaperone | 0 | **absent** |
| *PCSK1N* | proSAAS — endogenous PC1/3 inhibitor | 55.3 | present |
| *CPE* | carboxypeptidase E — trims C-terminal K/R | 73.7 | present |
| *PAM* | peptidylglycine alpha-amidating monooxygenase | 37.5 | present |
| *FURIN* | constitutive-pathway convertase (R-X-K/R-R) | 33 | present |
| *MME* | neprilysin — cuts Gly3-Phe4 | 0.7 | **absent** |
| *ANPEP* | aminopeptidase N — removes Tyr1 | 0.1 | **absent** |
| *PENK* | proenkephalin (endogenous background) | 0 | **absent** |
| *CTSL* | cathepsin L — alternative processing route | 35.5 | present |

HEK293 lacks **both** prohormone convertases and the obligate PC2 chaperone 7B2. This is a stronger result than the earlier fibroblast analysis, which had found only PC2 missing.

Three consequences, two of which are in your favour:

- **Stage 1 yields unprocessed proenkephalin.** No PC1/3, no PC2, no 7B2 means no endoproteolysis at the dibasic sites. Expect the intact precursor in the supernatant.
- **Stage 2 is therefore the whole experiment, not a confirmation.** The guide's plan — isolate the precursor, add convertase externally — is the only step that can generate peptides. Treat it as the primary endpoint and resource it accordingly.
- **Two things work in your favour.** *PAM* is abundant (37.5 nTPM), so C-terminal amidation is available. Endogenous *PENK* is 0.0 nTPM, so there is **no background**: anything you detect is construct-derived. This is a genuine advantage of HEK293T over a neuroendocrine line.

One arm is invalidated: *MME* (0.7 nTPM) and *ANPEP* (0.1 nTPM) are both absent, so the Cycle 5 knockdown has no endogenous target here (§4, finding ¶49).

![Audit overview]({{!artifact:art_707f0011-8d77-4de1-8caa-81b82deb2a31}})

**Figure 1.** (a) Processing machinery in HEK293, cell-line RNA in nTPM; open circles are genes with no detected transcript. Fibroblast values are in the accompanying table but are not plotted alongside, as GTEx tissue TPM and cell-line nTPM are not directly comparable units. (b) Architecture and defects of the four plasmids. (c) The 17 guide findings by protocol stage and severity.

---

## 2. Three of the four plasmids are unusable

Parsed directly from your SnapGene files; *PENK* was unannotated in all four, so open reading frames were translated and compared against UniProt P01210.

| Plasmid | ORF (aa) | YGGF cassettes | Matches P01210 | Signal peptide | Processing risk | Usable |
|---|---|---|---|---|---|---|
| `1_mEGFP_IRES_PENK` | 263 | 6/7 | **no** | N-terminal, native (Met1 intact) | SEVERE — cassette 7 ablated: 12-nt in-frame deletion, YGGFMRF -> YGF | **NO** |
| `2_mEGFP_P2A_PENK` | 523 | 7/7 | **no** | Met1 -> Pro (P2A-derived); h-region intact | none detected | **NO** |
| `3_PENK_IRES_mEGFP` | 267 | 7/7 | yes | N-terminal, native (Met1 intact) | none detected | **YES — only clean construct** |
| `4_PENK_P2A_mEGFP` | 523 | 7/7 | yes | N-terminal, native (Met1 intact) | SEVERE — 18-aa P2A remnant fused to cassette 7; MERF becomes YGGFMRF+ATNFSLLKQAGDVEENPG with NO dibasic site to remove it | **NO** |

Detail on each defect:

- **`1_mEGFP_IRES_PENK`** carries a **12-nt in-frame deletion** turning the C-terminal cassette `YGGFMRF` into `YGF`. This ablates cassette 7 and, critically, destroys the context `VPRMEKRYGGFMQ` — the **highest-kcat/Km PC2 site in the entire precursor** (9.4×10⁴ M⁻¹ s⁻¹, 39-fold above the weakest site in the same substrate series) [1].
- **`2_mEGFP_P2A_PENK`** places *PENK* downstream of P2A, so its initiator Met1 is replaced by the proline that terminates the P2A ribosome-skipping event. The signal peptide's h-region is intact, but a downstream position does not restore signal-peptide function — a signal sequence is still required, and being downstream of a 2A peptide does not supply one [3].
- **`4_PENK_P2A_mEGFP`** leaves an **18-aa P2A remnant** (`ATNFSLLKQAGDVEENPG`) fused to cassette 7, giving `YGGFMRF`+remnant with **no dibasic site** to excise it. The remnant is not removable by any convertase in the pathway. Note the annotated P2A in your files lacks the canonical GSG spacer, which reduces skipping efficiency [4].
- **`3_PENK_IRES_mEGFP`** is the **only clean construct** — byte-identical to P01210, native N-terminal signal peptide, no remnant. Its one limitation is the reporter: IRES-driven second-gene expression runs at 6–100% of cap-dependent levels, typically 20–50% [2], so mEGFP **under-reads** *PENK*.

**Action: sequence-verify all four before use, and build your primary experiments on plasmid 3.**

---

## 3. The engineered epitope swaps the immunopeptidome rather than enlarging it

MHCflurry 2.1 [5] was run on 612 peptides — 8–11-mers spanning the engineered `YGGFEVVG` cassettes, the native `YGGFM`/`YGGFL` cassettes as a matched comparator, and the P2A remnant junction — against 10 HLA supertype representatives (6,120 allele–peptide pairs).

![MHC immunogenicity]({{!artifact:art_7246e33c-63b3-4160-9215-cf26d6b7afd7}})

**Figure 2.** (a) Fraction of allele–peptide pairs at or below the 2nd presentation percentile, by group. (b) Overlap of strong-binding peptides between the native and engineered precursors. (c) The strongest neoepitopes requiring the engineered EVVG address, labelled peptide·allele.

- **The aggregate rate is unchanged.** 1.86% of engineered pairs vs 1.77% of native pairs are predicted presented (Fisher exact p = 0.84). On this measure the engineering is neutral.
- **But the epitope identity is completely different.** 44 engineered and 26 native peptides are strong binders, and **the intersection is empty**. The engineering does not add epitopes on net; it replaces one set with another that the recipient's immune system has never seen in this context.
- **21 neoepitopes require the engineered address**, spanning 7 of 10 alleles. The strongest are `FEVVGKRY` (HLA-B\*44:03, 73 nM, 0.19th percentile), `FEVVGKRF` (B\*44:03) and `RYGGFEVVGRF` (A\*24:02). Under Hardy-Weinberg with US-European allele frequencies, roughly 85% of individuals carry at least one affected allele — indicative only, as frequencies are population-specific.
- **Plasmid 4 carries additional epitope risk.** The P2A remnant junction generates 9 strong binders, including `GFMRFATNF` (A\*24:02, 0.13th percentile) which spans the junction itself and therefore exists only in that construct.

These are *in silico* binding and presentation predictions, not measured immunogenicity: MHC presentation is necessary but not sufficient for a T-cell response. The finding is a flag for a therapeutic trajectory, not a result about the current experiments.

---

## 4. Errors in the wet-lab guide

17 findings: **5 critical**, 9 moderate, 3 minor. Paragraph numbers refer to the guide's paragraph order.

### The five critical ones

1. **Cell count is not proenkephalin yield** (¶31). The guide picks the harvest timepoint by counting cells. Cell number and per-cell secretion are separate quantities, and Lipofectamine is cytotoxic, so the peak-count timepoint can be the *lowest*-expression timepoint. Measure the supernatant directly (mEGFP fluorescence normalised to viable cells, or an immunoassay), not the cell count.
2. **PC1/3 is prioritised over PC2** (¶33). The guide runs PC1/3 first and treats PC2, 7B2 and CPE as optional extras. PC2 is responsible for essentially all small-opioid-peptide generation from proenkephalin, and the strongest PC2 site in the whole precursor (`VPRMEKRYGGFMQ`, kcat/Km 9.4×10⁴ M⁻¹ s⁻¹) is 39-fold better than the weakest. Run PC2 + 7B2 as the primary reaction.
3. **The Cycle 1 conclusion is asserted independently of the data** (¶37). The text says that whatever the result, the literature already establishes that IRES changes expression. If the conclusion does not depend on the measurement, the measurement is not an experiment. State a falsifiable prediction with a threshold beforehand.
4. **The neprilysin knockdown has no target in this cell line** (¶49). HEK293 expresses MME at 0.7 nTPM and ANPEP at 0.1 nTPM — both effectively absent. There is nothing to knock down, so the siRNA arm cannot produce a signal. Either supply the peptidase exogenously to an in vitro reaction, or move this arm to a cell line that expresses it.
5. **The siRNA timepoints are far too early** (¶53). Readouts at 1 h and 2 h precede any protein depletion; RNAi requires transcript cleavage followed by turnover of pre-existing protein. Use 24, 48 and 72 h.

### Full list

| ¶ | Severity | Issue | Why it is wrong | Correction | Reference |
|---|---|---|---|---|---|
| `[6]` | Moderate | Expects 'two DNA ladders' as the diagnostic-digest result | A ladder is the molecular-weight standard, not a result. The expected outcome is two insert-derived bands of predicted size per construct, compared against one ladder lane. | Restate as: two bands at predicted sizes, sized against a single ladder lane. Predicted sizes given in this report. | Standard practice; band sizes are computable from the plasmid maps (this report, Table 2) |
| `[7]` | Minor | Cell strain written as 'NHB10 E. coli' | NEB's chemically competent strain used with 10-beta/Stable Outgrowth Medium is NEB 10-beta; 'NHB10' does not correspond to a catalogue strain. The protocol quoted in [9]-[24] is NEB's 10-beta protocol. | Correct to 'NEB 10-beta'. Note the quoted protocol is NEB's own, so the strain name should match it. | NEB 10-beta competent E. coli (C3019); protocol text in [14],[17] names '10-beta/Stable Outgrowth Medium' |
| `[25]` | Minor | 'heat-activated FBS' | The standard treatment is heat-INACTIVATION (56 C, 30 min) to destroy complement. 'Heat-activated' inverts the meaning. | Change to 'heat-inactivated FBS (56 C, 30 min)'. | Routine cell-culture practice |
| `[26]` | Minor | Opti-MEM used only for the DNA+lipid complexes | That is correct for complex formation, but [27] then switches the CULTURE medium to Opti-MEM, which is a reduced-serum medium. Prolonged culture in Opti-MEM without serum slows growth and confounds the cell-count time course that [31] depends on. | Keep Opti-MEM for complexes. For the 24-72 h collection, either keep serum-free deliberately (and say so, because it aids supernatant analysis) or keep DMEM+FBS - but do not switch mid-series. | Thermo Fisher Lipofectamine 3000 protocol (complexes in Opti-MEM); Opti-MEM product documentation |
| `[27]` | Moderate | First fluorescence read at 24 h to choose the plasmid | Thermo's own Lipofectamine 3000 comparison data analyse GFP at 48 h post-transfection. A 24 h read is on the rising phase, and IRES vs P2A constructs differ in kinetics, so ranking them at 24 h can invert the ordering seen at 48 h. | Read at 24, 48 and 72 h - they already collect at those points - and rank on the 48 h value. | Thermo Fisher Lipofectamine 3000 product data (GFP analysed 48 h post-transfection) |
| `[31]` | Critical | 'cell count identifies the timepoint with the highest amount of proenkephalin' | Cell number and proenkephalin yield are different quantities. Cell count measures proliferation and lipoplex toxicity; it says nothing about per-cell PENK production. The two can move in opposite directions, because transfection reduces viability while expression rises. | Normalise: report PENK per viable cell (or per mg total protein). Use the cell count as the denominator and a toxicity control, not as the yield read-out. | Internal logic; Lipofectamine cytotoxicity documented in Thermo product FAQ |
| `[32]` | Moderate | Isolate PENK by size exclusion alone | Proenkephalin is ~31 kDa and will co-elute with abundant serum and medium proteins of similar size. SEC alone is a fractionation step, not a purification, and there is no affinity handle on these constructs. | Either add a C-terminal tag to the next-generation construct, or follow SEC with an anti-PENK immunoprecipitation / Western step. Note the tag must NOT sit at the C-terminus of cassette 7. | General chromatography; construct maps show no epitope tag (this report, Table 2) |
| `[33]` | Critical | PC1/3 as the primary in vitro convertase, with PC2/7B2/CPE only 'if there is time' | PC2 - not PC1/3 - is responsible for essentially all small-opioid-peptide generation from proenkephalin. Johanning et al. report that generation of small opioid peptides from intermediates is mediated almost entirely by PC2 rather than PC1, and that PC2-knockout brains are depleted of mature enkephalins by more than three quarters. With PC1/3 alone the expected product is intermediates, not enkephalins. | Invert the priority: PC2 + 7B2 is the essential arm, PC1/3 the secondary one. 7B2 is not optional - it is an obligate chaperone for PC2 activity (UniProt P16519/P05408). | Johanning et al. 1998, J Biol Chem 273:22672-80, doi:10.1074/jbc.273.35.22672 |
| `[33]` | Moderate | No CPE in the primary reaction | Convertase cleavage leaves C-terminal basic residues (K/R). Without carboxypeptidase E the products are Met-enk-Arg / Met-enk-Lys extended forms, not Met-enkephalin itself - so an MS or antibody assay targeting Met-enkephalin can read negative even when cleavage worked. | Include CPE in the primary reaction, or explicitly target the +K/+R extended masses in the read-out. | UniProt P16870 (CPE) function; standard proenkephalin processing pathway |
| `[35]` | Moderate | 'Chromatography to show different fragments arose' | Chromatography gives retention time, which does not identify a peptide. Two different products can co-elute, and the informative comparison here is a specific mass. | Use LC-MS and target the computed masses - Met-enkephalin [M+H]+ 574.2330 is already tabulated in invitro_ms_targets.csv from the earlier work. | This project's own in vitro protocol already computes exact target masses (07_invitro_penk) |
| `[37]` | Critical | 'regardless of the result, we can say from the literature that IRES gives different expression levels' | This states the conclusion independently of the data, which inverts the engineering cycle. The literature prediction is the hypothesis to be tested, not a substitute for the measurement. | Rewrite as a falsifiable prediction with a number: expect IRES-downstream expression at roughly 20-50% of the cap-dependent gene, and report the measured ratio whatever it is. | Mizuguchi et al. 2000, Mol Ther 1:376-82, doi:10.1006/mthe.2000.0050 (IRES second-gene expression 6-100%, mostly 20-50%, of cap-dependent first-gene expression) |
| `[38]` | Moderate | Assumes P2A constructs will give 'greater quantity of PENK' | Plausible on expression grounds, but both P2A constructs in this set carry defects that make the comparison non-equivalent: in mEGFP-P2A-PENK the PENK initiator Met is replaced by P2A's proline, and in PENK-P2A-mEGFP an 18-residue P2A remnant stays fused to cassette 7. | Compare total PENK by Western, but do not treat higher PENK as better unless the product is also correctly processed - measure peptide output, not precursor abundance. | Yan et al. 2010, Anal Biochem 399:144-6, doi:10.1016/j.ab.2009.11.032; Liu et al. 2017, Sci Rep 7:2193, doi:10.1038/s41598-017-02460-2; construct analysis in this report |
| `[40]` | Moderate | Cycle 2 duplicates Cycle 1's read-out | Cycle 1 ([37]-[38]) already compares the constructs' expression; Cycle 2 compares 'which of the 2 constructs expresses more' by fluorescence microscopy. Same question, different instrument. | Merge, or make Cycle 2 answer a different question - e.g. subcellular localisation, which microscopy can do and a plate reader cannot, and which is the actual test of secretion. | Internal duplication |
| `[49]` | Critical | siRNA against neprilysin in HEK293T, with a neprilysin-cDNA plasmid as the counterpart | HEK293 does not express neprilysin (MME 0.7 nTPM) or aminopeptidase N (ANPEP 0.1 nTPM). There is no endogenous target to knock down, so a knockdown experiment in this line has no measurable baseline. Their own workaround - co-transfecting MME cDNA - is the right instinct, but it must then be stated as an artificial reconstitution, not as knockdown of an endogenous enzyme. | Frame it explicitly as reconstitution: co-transfect MME cDNA to CREATE the degradation activity, then show siRNA removes it. Also note enkephalin is degraded by ANPEP as well as MME, so silencing MME alone is not sufficient in a tissue that has both. | Human Protein Atlas cell-line RNA (HEK293): MME 0.7, ANPEP 0.1 nTPM |
| `[53]` | Critical | siRNA timepoints at '1 h, 2 h, later' | RNAi acts by degrading mRNA; the protein must then turn over before any effect appears. At 1-2 h post-transfection no knockdown at the protein level is possible, so these timepoints are guaranteed to be negative for reasons unrelated to whether the siRNA works. | Move to 24, 48 and 72 h post-transfection and confirm knockdown at the mRNA level (RT-qPCR) as well as by the functional read-out. | Mechanism of RNAi (mRNA cleavage precedes protein depletion); standard siRNA practice is 24-72 h |
| `[51]-[54]` | Moderate | Cycle 5 read-out is 'fluorescence/expression' to test enkephalin persistence | mEGFP reports transfection and translation of the reporter; it does not report enkephalin concentration or its half-life. Neprilysin knockdown cannot change mEGFP fluorescence. | The read-out must be the peptide: LC-MS or ELISA on the supernatant at each timepoint. Use fluorescence only to normalise for transfection efficiency between wells. | Construct architecture - mEGFP is a separate translation product from PENK in all four plasmids (this report, Table 2) |
| `[36]-[56]` | Moderate | Six cycles here vs three in the dry-lab record | The guide's Cycles 1-6 do not map onto the repository's cycles 1-3b, which cover a different question entirely (binding-mode scoring). Two independent numbering schemes are in use for 'the engineering cycles' of one project. | Adopt one scheme. Suggested: keep the guide's wet-lab numbering as the project record and re-label the dry-lab work as computational sub-cycles, so 'Cycle 3' is unambiguous. | Repository 06_engineering_cycles (cycles 1, 2, 3, 3b) vs guide paragraphs [36]-[56] (cycles 1-6) |

Two things in the guide that are **correct** and should not be changed: Lipofectamine 3000 is a real product (cat. L3000001), and it is one of the reagents suitable for co-transfecting siRNA with plasmid DNA, which is what Cycle 5 requires.

---

## 5. The two cycle numbering schemes are disjoint

The guide's Cycles 1–6 and the repository's Cycles 1–3b **share no questions**. The guide's cover wet-lab construct/expression work (1, 2), the delivery vehicle (3, 4), the degradation arm (5) and safety (6). The repository's cover the deltorphin chimera, delta-selectivity, and selectivity-metric validation. Zero overlap.

The practical hazard: **"Cycle 3" is ambiguous** — lipoplex modelling in one scheme, selectivity-metric validation in the other. Prefix them (`W1`–`W6` for wet-lab, `D1`–`D3b` for dry-lab) before the two records are read side by side.

---

## 6. What I should do to support the wet lab

Ordered by what unblocks them soonest.

1. **Deliver expected digest band sizes for all four plasmids** — computable now from the maps, and it converts ¶6's "two ladders" into a specific pass/fail. *(Blocks nothing else; do first.)*
2. **Deliver exact target masses and expected fragment sets** for the PC2 + 7B2 + CPE reaction, per plasmid, so ¶35's chromatography becomes identification rather than a retention-time observation. The in vitro protocol in `07_invitro_penk` already computes these — they need to be handed over as a bench sheet.
3. **Specify the Stage 2 reaction conditions** — enzyme:substrate ratio, buffer, pH, Ca²⁺, time course, and the paired controls (no-enzyme, no-substrate, native-PENK positive). `enzyme_conditions.csv` holds these.
4. **Re-plan Cycle 5.** With no *MME* or *ANPEP* in HEK293T, propose the in vitro alternative: purified peptidase added to synthetic peptide, ± inhibitor, with degradation half-life as the readout.
5. **Provide a quantitative read-out plan for Cycles 1 and 2** with a pre-registered threshold, replacing ¶37's data-independent conclusion.
6. **Flag the immunogenicity finding into the project's safety record** for Cycle 6, with the neoepitope list attached.

Two things I should **not** do: claim the P2A constructs will give more *PENK* (the analysis says the opposite for plasmids 2 and 4), and let the reporter stand as a proxy for peptide yield — mEGFP is a separate translation product from *PENK* in all four plasmids.

---

## 7. References

1. Johanning K, Juliano MA, Juliano L, Lazure C, Lamango NS, Steiner DF, Lindberg I. *Specificity of prohormone convertase 2 on proenkephalin and proenkephalin-related substrates.* J Biol Chem 1998;273(35):22672–22680. doi:[10.1074/jbc.273.35.22672](https://doi.org/10.1074/jbc.273.35.22672)
2. Mizuguchi H, Xu Z, Ishii-Watabe A, Uchida E, Hayakawa T. *IRES-dependent second gene expression is significantly lower than cap-dependent first gene expression in a bicistronic vector.* Mol Ther 2000;1(4):376–382. doi:[10.1006/mthe.2000.0050](https://doi.org/10.1006/mthe.2000.0050)
3. Yan L, Kaplan FS, Shore EM, Xu M. *Signal sequence is still required in genes downstream of “autocleaving” 2A peptide for secretary or membrane-anchored expression.* Anal Biochem 2010;399(1):144–146. doi:[10.1016/j.ab.2009.11.032](https://doi.org/10.1016/j.ab.2009.11.032)
4. Liu Z, Chen O, Wall JBJ, Zheng M, Zhou Y, Wang L, Ruth Vaseghi H, Qian L, Liu J. *Systematic comparison of 2A peptides for cloning multi-genes in a polycistronic vector.* Sci Rep 2017;7:2193. doi:[10.1038/s41598-017-02460-2](https://doi.org/10.1038/s41598-017-02460-2)
5. O'Donnell TJ, Rubinsteyn A, Laserson U. *MHCflurry 2.0: improved pan-allele prediction of MHC class I-presented peptides by incorporating antigen processing.* Cell Syst 2020;11(1):42–48.e7. doi:[10.1016/j.cels.2020.06.010](https://doi.org/10.1016/j.cels.2020.06.010)
6. Uhlén M, Fagerberg L, Hallström BM, et al. *Tissue-based map of the human proteome.* Science 2015;347(6220):1260419. doi:[10.1126/science.1260419](https://doi.org/10.1126/science.1260419) — Human Protein Atlas cell-line RNA data (HEK293), [proteinatlas.org](https://www.proteinatlas.org)
7. UniProt Consortium. *UniProt: the Universal Protein Knowledgebase in 2025.* Nucleic Acids Res 2025;53(D1):D609–D617. doi:[10.1093/nar/gkae1010](https://doi.org/10.1093/nar/gkae1010) — accessions P01210 (PENK), P29120 (PCSK1), P16519 (PCSK2), P05408 (SCG5/7B2), P16870 (CPE)
8. GTEx Consortium. *The GTEx Consortium atlas of genetic regulatory effects across human tissues.* Science 2020;369(6509):1318–1330. doi:[10.1126/science.aaz1776](https://doi.org/10.1126/science.aaz1776)

---

## 8. Data files

All values in this report are reproducible from these tables.

| File | Contents |
|---|---|
| `hek293t_processing_competence.csv` | Per-gene HEK293 nTPM, fibroblast TPM, role, source |
| `construct_risk_table.csv` | Per-plasmid ORF, cassette count, signal peptide, P2A remnant, risk |
| `guide_error_audit.csv` | All 17 findings with severity, reason, correction, reference |
| `mhc_predictions_full.csv` | All 6,120 allele–peptide predictions |
| `mhc_engineered_neoepitopes.csv` | The 21 EVVG-dependent neoepitopes |
| `mhc_group_summary.csv` | Per-group binding summary |
| `cycle_reconciliation.csv` | Guide vs repository cycle mapping |
| `hek293t_design_paradox.csv` | Stage-by-stage assumption vs computed reality |

*Predictions are computational. MHC binding predictions indicate presentation likelihood, not measured immunogenicity. Expression values are transcript-level and do not guarantee protein abundance or activity.*
