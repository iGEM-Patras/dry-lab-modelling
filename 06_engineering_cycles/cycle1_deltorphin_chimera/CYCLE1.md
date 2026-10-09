# Cycle 1: Enkephalin–deltorphin chimera (`YGGFEVVG`)

**Status:** complete · **Outcome:** ~~δ-preference raised to 1.96× native~~ **see correction below** · **Decision:** carry forward as Cycle 2 baseline

This is a retrospective writeup: the design was built and tested before being formalised
as a DBTL cycle. Numbers below are the final matched-MSA production runs.

> ## ⚠ CORRECTION (issued during Cycle 2)
>
> **The headline "1.96× native" figure in this document is withdrawn.** It was computed
> from the single top-ranked diffusion sample (`model_0`) of each complex. Recomputing
> across all 5 samples that were generated:
>
> | Estimator | native `YGGFM` | C1 `YGGFEVVG` |
> |---|---|---|
> | `model_0` only (as originally reported) | +0.0199 | +0.0390 |
> | **all 5 samples (correct)** | **+0.0050 ± 0.0051** | **+0.0114 ± 0.0131** |
>
> C1's Δ_sel is smaller than its own uncertainty: indistinguishable from zero
> (Welch p = 0.43) and from native (p = 0.60).
>
> **Root cause:** the `MOR_eng` complex has an ipTM spread of 0.0280 across samples,
> 3× larger than any other complex in the study (range 0.9201–0.9850). `model_0` for
> that complex landed at 0.9328, near the floor of its own distribution. The apparent
> selectivity was substantially one unlucky μ sample, not a property of the peptide.
>
> **What survives:** the directional conclusion (the deltorphin address graft moves the
> peptide δ-ward relative to native) and the pose-convergence anomaly. **What does not:**
> any quantitative selectivity claim. Do not quote "1.96×".
>
> **Process change adopted from here on:** every reported metric is a mean ± SD over all
> diffusion samples, never a single model. Single-model numbers are not reported.

---

## DESIGN

### Concept

Opioid peptides are modular. They decompose into:

- a **message domain** (`Tyr¹-Gly²-Gly³-Phe⁴`) which triggers receptor activation and is
  required for activity at *all* opioid receptor subtypes. It is essentially non-negotiable.
- an **address domain** (the C-terminal residues) which determines *which* receptor
  subtype the peptide prefers.

Native Met-enkephalin is `YGGF` + `M`: message plus a minimal one-residue address, giving
only weak δ-preference.

The **deltorphins** (from the frog *Phyllomedusa bicolor*) are the most δ-selective natural
opioid peptides known. Deltorphin I is `Tyr-D-Ala-Phe-Asp-Val-Val-Gly-NH₂` and deltorphin II
is `Tyr-D-Ala-Phe-Glu-Val-Val-Gly-NH₂`, i.e. they carry the anionic/hydrophobic addresses
**`DVVG`** and **`EVVG`**.

**Design hypothesis:** fusing the deltorphin II address onto the intact enkephalin message
should transfer δ-preference onto an enkephalin scaffold that a PENK cassette can express.

```
   message      address
  ┌────────┐  ┌────────┐
   Y G G F    E  V  V  G      ← YGGFEVVG  (Cycle 1 payload)
   Y G G F    M                ← YGGFM     (native Met-enkephalin)
   Y a  F     E  V  V  G-NH2   ← deltorphin II (a = D-Ala; not DNA-encodable)
```

### Why the design deviates from true deltorphin II

| Deltorphin II feature | Cycle 1 payload | Reason |
|---|---|---|
| D-Ala at position 2 | `Gly-Gly` retained | D-amino acids are **not DNA-encodable** |
| C-terminal amide (`-NH₂`) | C-terminal `Gly` | Gly is the **PAM amidation signal** → amide formed *in vivo* |
| 7 residues | 8 residues | keeping `GG` preserves the native enkephalin message register |

The retained `Gly-Gly` is the key compromise: D-Ala² in natural deltorphins both rigidifies
the backbone and confers protease resistance. We cannot encode it, so Cycle 1 accepts a
more flexible message domain, and the protease problem is instead solved *at the systems
level* by the co-delivered anti-MME (neprilysin) siRNA.

---

## BUILD

- Payload codon-optimised and embedded in the engineered PENK cassette
  (see [`../../01_plasmid_audit/engineered_payload/`](../../01_plasmid_audit/engineered_payload/)).
- Delivered as a lipoplex co-formulated with the anti-MME siRNA
  (see [`../../04_lipoplex_md/`](../../04_lipoplex_md/)).
- Plasmid identity and insert release verified by virtual restriction digest
  (see [`../../02_restriction_qc/`](../../02_restriction_qc/)).

---

## TEST

Boltz-2 co-folds of `YGGFM` (native) and `YGGFEVVG` (Cycle 1) against full-length
human OPRD1 (δ) and OPRM1 (μ). Matched settings: MSA = 1024, 5 diffusion samples.

| Peptide | Receptor | ipTM | complex pLDDT | confidence |
|---|---|---|---|---|
| `YGGFM` native | MOR (μ) | 0.9587 | 0.8089 | 0.8389 |
| `YGGFM` native | DOR (δ) | 0.9786 | 0.8613 | 0.8848 |
| `YGGFEVVG` C1 | MOR (μ) | 0.9328 | 0.8127 | 0.8367 |
| `YGGFEVVG` C1 | DOR (δ) | 0.9718 | 0.8304 | 0.8587 |

### Selectivity

| Peptide | Δ_sel = ipTM(DOR) − ipTM(MOR) | vs native |
|---|---|---|
| `YGGFM` native | **+0.0199** | 1.00× |
| `YGGFEVVG` C1 | **+0.0390** | **1.96×** |

### MSA-robustness control

The DOR complexes were additionally run at a degraded MSA (64 sequences) and superposed
onto the full-MSA (1024) structures on the receptor core (297 CA, middle 80%, flexible
GPCR termini excluded):

| Complex | core-receptor fit RMSD | peptide-in-pocket RMSD |
|---|---|---|
| DOR + `YGGFM` | 0.62 Å | **0.32 Å** |
| DOR + `YGGFEVVG` | 1.45 Å | **5.08 Å** |

---

## LEARN

**1. The address graft worked.** `YGGFEVVG` roughly doubles the δ-over-μ confidence gap
relative to native Met-enkephalin (+0.0390 vs +0.0199). The mechanism is as designed:
the gain comes from *losing* μ confidence (0.959 → 0.933) while δ is nearly preserved
(0.979 → 0.972). The deltorphin address de-prioritises μ rather than super-charging δ.

**2. Both receptors are still confidently engaged.** All four ipTM values ≥ 0.93. Cycle 1
is δ-*preferring*, not δ-*selective*: this remains a dual agonist with a δ bias. Achieving
genuine selectivity is the goal of Cycle 2.

**3. ⚠ The engineered peptide's pose is less converged than native's.** This is the most
important finding. Between MSA depths the native peptide moved 0.32 Å while the Cycle 1
peptide moved **5.08 Å** in the same pocket, and its complex pLDDT is lower at DOR
(0.830 vs 0.861). Two readings, not yet distinguished:

- *(a) Genuine flexibility*: the `GG` + 4-residue tail is entropically floppy, exactly the
  role D-Ala² plays in real deltorphins (backbone rigidification). This would be a real
  liability of the DNA-encodable compromise.
- *(b) Prediction uncertainty*: Boltz has abundant natural-enkephalin-like training data
  but few enkephalin–deltorphin chimeras, so the address may simply be under-determined.

**4. Direct consequence for Cycle 2 design.** Reading (a) predicts that *rigidifying or
better anchoring the address* should improve both selectivity and pose convergence
simultaneously. This is precisely what **β-branched residues (Ile) in the address** would
do, and the deltorphin literature independently reports that `[Ile⁵,⁶]`-deltorphin II
achieves dramatically higher δ-selectivity than deltorphin II itself. Cycle 2's primary
hypothesis follows directly from this cycle's anomaly.

**5. Method note.** Report pose convergence (multi-sample spread, cross-MSA RMSD) alongside
ipTM in all future cycles. A design that scores well but does not converge is not a win:
Cycle 1 would have looked unambiguously successful on ipTM alone.

---

## Files

| File | Contents |
|---|---|
| `data/cycle1_confidence.csv` | the four ipTM / pLDDT / confidence values above |
| `../../docs/figures/` | `dor_mor_fullMSA_comparison.png` (matched-MSA bar comparison) |
