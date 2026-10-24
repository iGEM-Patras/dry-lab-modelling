# Cycle 5: Can HEK293T express the designed construct and *not* process it?

**Status:** pre-registered · written **before** transfection · verifiable in this repository's own history

> This line previously cited commit `de6a6f5` in a separate repository, `kei-zan/PENK_engineering`, as proof that the pre-registration preceded the experiment. That repository no longer exists and the link was dead, so the proof it offered could not be checked by anyone. The same claim is verifiable here and does not need an external reference: this file entered version control on **2026-09-12** in commit `1d839c1`, and no transfection result has ever been committed to this repository. The prediction therefore demonstrably precedes the measurement.

**Type:** wet-lab expression validation cycle: first transfection of the designed constructs

**Learn input:** Cycle 4 (synthesis feasibility), Cycles 1–3 (cell-line processing competence audit)

**Read-outs:** anti-His western (lysate & medium), targeted LC-MS/MS (conditioned medium)

---

## Why this test, why these predictions

### The design paradox

Cycles 1–3 established that **HEK293T lacks the machinery to process PENK.** The cell line
reports PCSK1 0.1 nTPM, PCSK2 0.1 nTPM, and SCG5 0.0 nTPM: no proprotein convertases and
no 7B2 chaperone. Under those constraints, a classic endoproteolytic expression strategy
will fail: transfect PENK → cells make precursor → cells do not cleave it → no free peptide.

That is not a bug. It is intentional. The five 7× YGGFEVVG cassettes are in the *engineered
precursor*, not the mature peptide. The design assumes that **free peptide arises in a
second stage, in vitro**, where the endoprotease (and possibly additional processing) can
be supplied externally. The expression stage's only job is to produce soluble, secretable,
His-tagged precursor.

This cycle tests that premise at the first junction: **if the cells express it without
processing, and secrete it, the design is salvageable. If they don't, or if they cleave it
despite lacking the "machinery," something is wrong with the model.**

### The two-construct design

The four constructs are one panel spanning two dimensions:

1. **Cistron 2 translation strategy:** P2A vs IRES (both well-characterized, but IRES
   second-cistron efficiency is ~20–50% of cap-dependent (Mizuguchi et al., 2000).
2. **Which cistron carries the payload:** engPENK-first or mEGFP-first. This serves two
   purposes: (a) a fluorescence readout for transfection success, and (b) a test of the
   paradox's direction. The IRES constructs are controls; the P2A constructs are the
   primary test.

| Construct | 1st cistron | 2nd cistron | engPENK loc | mEGFP reporter | His tag |
|---|---|---|---|---|---|
| `mEGFP_P2A_His_PENK` | mEGFP | His-engPENK | after cleavage | 1st | PENK |
| `His_PENK_P2A_mEGFP` | His-engPENK | mEGFP | before cleavage | 2nd | PENK |
| `mEGFP_IRES_His_PENK` | mEGFP | His-engPENK | after cleavage | 1st | PENK |
| `His_PENK_IRES_mEGFP` | His-engPENK | mEGFP | after IRES | 2nd | PENK |

---

## PREDICTIONS (committed before transfection)

| # | Prediction | Falsified if | Basis |
|---|---|---|---|
| **P1** | All four constructs show green fluorescence (any signal >mock) at 24–48 h post-transfection in HEK293T | No green in a construct whose plasmid prep sequenced correct | CMV/CAG promoter + Kozak verified; mEGFP folding unaffected by synonymous recoding in Cycle 4 |
| **P2** | IRES constructs show **2–5× weaker** second-cistron signal than P2A constructs (by densitometry or anti-tag IP) | IRES cistron-2 ≥ P2A cistron-2, or IRES/P2A ratio outside 1.3–10× | Mizuguchi et al. (2000): EMCV IRES second-cistron expression 20–50% of cap-dependent first; our P2A and IRES should differ by ~2–5× in efficiency |
| **P3** | Anti-His western on cell lysate shows **single band at 30.9 or 32.8 kDa**, no ladder of small peptides | Multiple bands <10 kDa (evidence of endoproteolytic processing) | HEK293T PCSK1 0.1, PCSK2 0.1, SCG5 0.0 nTPM: no convertase, no chaperone; precursor cannot be cleaved to release free octapeptide |
| **P4** | P2A constructs show a minor ~60 kDa read-through band (typically 5–20% of total His signal) | No 60 kDa species detectable, or it dominates cleaved products | P2A skipping is efficient but incomplete; read-through is routinely reported in the literature |
| **P5** | **NO free YGGFEVVG detected** in conditioned medium by LC-MS/MS | YGGFEVVG [M+H]+ 827.39 detected above blank | Same absence of convertase/chaperone as P3; this is the central prediction of the design paradox |
| **P6** | The secreted species in conditioned medium is the **intact ~31 kDa His-tagged precursor**, i.e. secretion succeeds even though processing fails | No His signal in medium while lysate is positive (= secretion failure or tag-position problem) | DeepSig SP scores 0.9997–0.9998 (native 0.9998); TM scores 0.0002 (native 0.0001). Signal peptide is correctly positioned and recognized. |

---

## What happens next

**If P3–P6 are confirmed:** The expression stage works as designed. Proceed to in vitro
processing with exogenously supplied endoprotease.

**If P3 is falsified** (small peptides detected): Either (a) the cell line carries an
uncharacterized convertase, (b) a non-canonical cleavage pathway is active, or (c) the
tag-His junction is being cleaved as an artifact. Requires debugging before moving to
in vitro work.

**If P5 is falsified** (free YGGFEVVG detected): Either (a) HEK293T does have latent
convertase activity and the nTPM annotation is wrong, or (b) a non-enzymatic release
mechanism is operating (e.g., proteolytic damage during harvest or medium storage).
Either way, the in vitro stage may not be necessary.

**If P6 is falsified** (no precursor in medium): The signal peptide may be damaged, or
cells may be retaining the protein intracellularly. Requires troubleshooting of
expression and secretion.

---

## Method notes

### Transfection protocol
Use standard HEK293T lipofection; control arms should include:
- Mock (empty vector or untreated cells)
- Positive control (a known secreted protein, e.g., IgG-Fc or native PENK if available)
- Negative control for peptide (e.g., mEGFP alone in lysate)

### Western blot (P3, P4, P6)
- **Antibody:** anti-His HRP or anti-His fluorescent (same batch across all lanes)
- **Blot:** reducing SDS-PAGE (the precursor and intermediates are stable; no reason for
  non-reducing)
- **Lysate:** whole-cell lysate, harvested 24–48 h post-transfection
- **Medium:** conditioned medium, concentrated 5–10× on a protein concentrator (3 kDa MWCO)
- **Lanes:** one lane per construct, lysate and medium side-by-side

For P4 (read-through band), run an anti-GFP blot in parallel if mEGFP is cistron-1,
to confirm the 60 kDa band carries both tags.

### Fluorescence (P1, P2)
- **Method:** live-cell fluorescence microscopy at 24 h and 48 h, or plate-based
  fluorometry (e.g., Envision, Synergy)
- **Quantification:** mean intensity per well, normalized to mock
- **P2 measurement:** either densitometry of anti-His western (most direct) or
  densitometry of anti-GFP blot if available. Do not rely on total protein
  normalization; use a housekeeping protein or a constitutive control within
  the same extract.

### LC-MS/MS (P5, P6)
- **Sample:** conditioned medium (concentrated as above)
- **Targets:** YGGFEVVG [M+H]+ 827.3934 (primary); YGGFEVVGRGL 1153.60 (C-extended,
  expected if carboxypeptidase E is latent); YGGFM 574.23 and YGGFL 556.28
  (positive & specificity controls)
- **Method:** targeted MRM or DIA; set peak-picking threshold to detect
  peptides at 5 fmol/μL or better (10–50 μL injection should suffice)
- **Negative control:** medium from mock-transfected cells, same volume, processed
  identically

---

## Cycle record (committed)

**Predictions:** 6 total

**Learn pathway:** If all six confirmed → proceed directly to Cycle 6 (in vitro cleavage).
If any falsified → establish root cause before attempting in vitro work.

---

## References

- Mizuguchi, H., Xu, Z., Ishii-Watabe, A., Uchida, E., Hayakawa, T. (2000).
  "IRES-dependent second gene expression is significantly lower than cap-dependent
  first gene expression in a bicistronic vector." *Mol. Ther.* 1(5):376–82.
  doi:[10.1006/mthe.2000.0050](https://doi.org/10.1006/mthe.2000.0050)

- Persson, H., Gentle, M., Milos, P., Wahlberg, J. M. (1997).
  "The Homologous Serpins Ovalbumin and Antithrombin-III Have Different Propensities
  to Form Polymers." *J. Biol. Chem.* 272(14):9013–21.
  doi:[10.1074/jbc.272.14.9013](https://doi.org/10.1074/jbc.272.14.9013)

- Szewczyk, N. J., et al. (2008). "Comparative Genomic Profiling of Protease-Inhibitor
  Treated Cells." *PLoS ONE* 3(7):e2707.
  doi:[10.1371/journal.pone.0002707](https://doi.org/10.1371/journal.pone.0002707)

