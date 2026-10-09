# What is still checkable: PENK project audit

**Status:** all four original workstreams and the three engineering cycles are closed;
cycle 3b terminated on a negative methodological result. This memo asks what remains
*computationally checkable* and answers three of those questions with data.

Every number below is computed in this session from GTEx v8 (GENCODE v26/GRCh38) or from
files in this repository. Nothing is quoted from memory.

---

## 1. The unasked question: can the target cell actually process PENK?

The whole therapeutic chain assumes a transduced cell will cut proenkephalin into
enkephalin. Proenkephalin is not itself active: it is a proprotein, and the cut is
performed by the prohormone convertases PC1/3 (*PCSK1*) and PC2 (*PCSK2*), with PC2
requiring its obligate chaperone 7B2 (*SCG5*) to become catalytically competent. No
workstream in this repository has ever checked whether the intended target tissue
expresses that machinery.

It largely does not.

| tissue | PCSK1 | PCSK2 | SCG5 | PAM | competent? | limiting factor |
|---|---|---|---|---|---|---|
| Hypothalamus | 22.3 | 8.6 | 146.9 | 50.8 | yes | - |
| Cortex | 11.0 | 14.3 | 148.7 | 18.6 | yes | - |
| Pituitary | 19.7 | 1.3 | 563.2 | 69.3 | yes | - |
| Tibial nerve | 1.1 | 5.0 | 1.4 | 56.7 | yes | - |
| **Cultured fibroblasts** | 1.8 | **0.03** | 31.5 | 119.4 | **no** | **PCSK2 absent** |
| Spinal cord (cervical) | 0.5 | 1.1 | 126.5 | 11.5 | no | PCSK1 low |
| Skeletal muscle | 0.06 | 0.05 | 0.14 | 36.2 | no | both absent |
| Liver | 0.04 | 0.05 | 5.4 | 2.7 | no | both absent |
| Whole blood | 0.01 | 0.01 | 0.15 | 5.2 | no | both absent |

Median TPM, GTEx v8. Full table with all genes: `processing_competence_by_tissue.csv`.

**Cultured fibroblasts are the single worst case among the plausible targets.** PCSK2
median is 0.03 TPM and **91% of the 504 fibroblast samples fall below 1 TPM**, this is
absence, not low expression. Fibroblasts are also the cell type the lipoplex arm is
most likely to reach first.

This does not sink the strategy, but it converts an assumption into a design decision:

- If the target is a **non-neuroendocrine cell**, the construct should co-express a
  convertase, or the payload should be redesigned so it does not need one (e.g. a
  furin site (FURIN is 65.9 TPM in fibroblasts, ubiquitous) in place of the native
  PC1/3–PC2 dibasic.
- If the target is **neural tissue**, the machinery is present and the assumption holds.

The in vitro assay in `07_invitro_penk/` tests the *chemistry* with purified enzymes. It
cannot test this, because it supplies the enzymes the cell may not have.

### 1a. Amidation is the one thing that does work everywhere

*PAM* is 119.4 TPM in fibroblasts, higher than in any brain region measured here. The
5-of-7 Gly-extended engineered cassettes would be amidated in essentially any target
cell. Of the engineered design's two mechanistic bets, the amidation bet is robust to
cell type and the convertase bet is not.

---

## 2. The degradation arm silences one of two enkephalinases

Enkephalins are cleared by two zinc metallopeptidases in parallel: **neprilysin**
(NEP, *MME*, EC 3.4.24.11), which hydrolyses the Gly3–Phe4 bond, and **aminopeptidase N**
(APN, *ANPEP*, EC 3.4.11.2), which removes the N-terminal tyrosine at Tyr1–Gly2. Removing
Tyr1 abolishes opioid activity outright: the tyrosine is the pharmacophore.

The siRNA workstream targets *MME* only. In fibroblasts:

| peptidase | gene | fibroblast TPM | targeted by the siRNA arm |
|---|---|---|---|
| Neprilysin | *MME* | 640.5 | yes |
| **Aminopeptidase N** | ***ANPEP*** | **810.5** | **no** |
| DPP-4 | *DPP4* | 48.8 | no |
| ACE | *ACE* | 6.4 | no |

**ANPEP is expressed at least as highly as MME in 9 of the 11 tissues examined**
(ANPEP/MME ratio 41.5 in adrenal gland, 33.0 in skin, 10.6 in hypothalamus, 1.3 in
fibroblasts). The two exceptions are tibial nerve (0.99, the two are equal) and
skeletal muscle (0.19). Silencing NEP alone leaves the aminopeptidase route fully open
in every case.

And critically, the cassette engineering did not help here either:

```
Native Met-enkephalin   Y G G F | M
engPENK product         Y G G F | E V V G
                        ^   ^
                       APN  NEP        both sites inside the unchanged YGGF message
```

The engineering replaced the **address** (the C-terminal residues that select the
receptor) and left the **message** (YGGF, which carries both scissile bonds) untouched.
Every degradation liability of the native peptide is inherited by the engineered one.

**Checkable next:** extend the siRNA design pipeline (which already exists and is
validated) to *ANPEP*, using the same human-exclusivity and seed-divergence rules that
forced the withdrawal of the original MME panel. This is the highest-value remaining
dry-lab task: the method is built, only the target changes.

---

## 3. Residency: the one salvageable observable from cycle 3b

Cycle 3b's gate verdict recorded that MM-GBSA binding energy could not resolve
δ/µ selectivity, but noted that **fractional residency was measured rather than
modelled** and survived the negative result. Testing it properly:

| peptide | residency δ (%) | residency µ (%) | Δ (δ−µ) | ΔΔG_exp (kcal/mol) |
|---|---|---|---|---|
| Deltorphin I | 93.0 | 82.6 | +10.4 | +5.70 |
| Deltorphin II | 75.7 | 58.0 | +17.7 | +5.39 |
| Endomorphin-1 | 97.4 | 100.0 | −2.6 | −2.99 |
| Met-enkephalin | 100.0 | 100.0 | 0.0 | +0.41 |

Spearman ρ = **+0.80** (p = 0.20), Pearson r = **+0.92** (p = 0.085), n = 4 peptides.

**The direction is right and the evidence is worthless.** A bootstrap over the four
peptides gives a 95% CI on r of **[−1.00, +1.00]**: the correlation is entirely
unconstrained at n = 4. Two further problems:

- **Ceiling effect.** Met-enkephalin sits at 100% residency on both receptors, so the
  metric cannot express its (small, +0.41 kcal/mol) experimental preference at all.
- **Replicate noise.** Δ-residency has sd = 24% (deltorphin I) and 44% (deltorphin II)
  across 5 replicates. For the 95% CI to exclude zero would require **≈21 and ≈24
  replicates** respectively: a 4–5× increase over what cycle 3b ran.

So residency is a hypothesis, not a result. It is worth pre-registering only if the
replicate budget is quadrupled *and* the calibration set is expanded beyond four
peptides to break the ceiling.

### A data discrepancy found while checking this

`control_calibration_targets.csv` gives met-enkephalin ΔΔG_exp = **0.41** kcal/mol
(2-fold δ/µ preference), but the cycle 3b verdict table used **0.00**. The stored values
are internally consistent: all four reproduce exactly as RT·ln(K_i ratio) at
**T = 300 K** (max error 1×10⁻⁵ kcal/mol; 298.15 K and 310 K both fail). The verdict's
0.00 is therefore the erroneous value.

**It does not change the conclusion** (r = 0.915 vs 0.924; ρ = 0.800 either way), but
the calibration file should be treated as authoritative and T = 300 K recorded as the
convention, which is currently undocumented.

---

## 4. What else is checkable, ranked

1. **siRNA panel against *ANPEP*.** Method exists and is validated; only the target
   changes. Directly addresses the gap in §2. **Highest value.**
2. **Convertase co-expression or a furin-cleavable redesign.** §1 shows the native
   dibasic may not be cut in the target cell. FURIN is ubiquitous; a furin-site variant
   is a sequence-level design task with an existing junction-analysis pipeline.
3. **Extend the in vitro assay to a cell-lysate arm.** The purified-enzyme assay supplies
   what the cell may lack. A fibroblast-lysate arm would test §1 directly at the bench.
4. **Residency, only if re-powered.** ≈24 replicates and >4 calibration peptides,
   pre-registered. Otherwise leave cycle 3b closed.
5. **Not checkable here:** immunogenicity of the non-native YGGFEVVG epitope. No MHC
   binding-prediction tool is installed in this environment; this needs either a new
   tool or an external server.

---

## Sources

| # | source | used for |
|---|---|---|
| 1 | GTEx Consortium, GTEx v8 (GENCODE v26, GRCh38), via the GTEx Portal API | all expression values in §1, §1a, §2 |
| 2 | Repository file `06_engineering_cycles/cycle3b_physics_rescoring/results/bound_results_with_residency.csv` | residency values, §3 |
| 3 | Repository file `.../control_calibration_targets.csv` | ΔΔG_exp anchors and K_i ratios, §3 |
| 4 | UniProt P29120 (PCSK1), P16519 (PCSK2), P05408 (SCG5/7B2), P19021 (PAM), P08473 (MME), P15144 (ANPEP), P09958 (FURIN) | enzyme identity, EC numbers, chaperone dependence |
| 5 | Enzyme nomenclature EC 3.4.24.11 (neprilysin), EC 3.4.11.2 (aminopeptidase N) | cleavage-bond assignments in §2 |

Enkephalin cleavage-bond assignments (NEP at Gly3–Phe4, APN at Tyr1–Gly2) are the
standard characterisation of these two activities in the enkephalin-degradation
literature and are consistent across the primary sources on enkephalin catabolism.

*Prepared 2026-09-01. All values recomputed in-session; no figures quoted from memory.*
