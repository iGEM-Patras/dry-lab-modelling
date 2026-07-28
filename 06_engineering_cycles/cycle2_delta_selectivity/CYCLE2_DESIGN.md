# Cycle 2 — Address-domain optimisation for δ-selectivity

**Status:** pre-registered · written **before** any Cycle 2 fold was run
**Baseline:** Cycle 1 `YGGFEVVG`, Δ_sel = +0.0390 (1.96× native)
**Goal:** increase Δ_sel further **and** improve address pose convergence

> This document states the hypotheses, the variant panel, and the falsifiable predictions
> *in advance*. Results go in `CYCLE2_RESULTS.md`. Predictions are not edited after the fact —
> if they fail, the failure is recorded as the cycle's finding.

---

## Where Cycle 2's design comes from

Cycle 1 produced one anomaly: the engineered address does not converge to a single pose
(5.08 Å peptide shift across MSA depths, vs 0.32 Å for native; lower pLDDT at DOR).
One explanation is entropic floppiness of the `EVVG` tail — the deficiency that
D-Ala² fixes in natural deltorphins but which we cannot encode in DNA.

The deltorphin structure–activity literature points at the same region from a completely
independent direction. Binding studies on `[D-Ala²]`deltorphin II established that the
**hydrophobic Val⁵ and Val⁶ residues are important for δ-affinity and selectivity**, and that
**enhancing hydrophobicity at those positions** yields analogs far more δ-selective than
deltorphin II itself — `[Ile⁵,⁶]`, `[norleucine⁵,⁶]` and `[γ-methyl-leucine⁵,⁶]` analogs, with
`[Ile⁵,⁶]`deltorphin II reaching reported δ-selectivity ratios of **2400 and 18000**.

Two independent lines therefore converge on the **same two residues** — the `VV` pair of the
address. Of the proposed substitutions, only **Ile** is a standard amino acid (norleucine and
γ-methyl-leucine are non-proteinogenic), so Ile is the DNA-encodable route to that result.

Ile adds a methyl group (more hydrophobic) **and** is β-branched (restricts backbone
φ/ψ freedom). That single substitution addresses the literature's affinity/selectivity lever
and Cycle 1's convergence anomaly at once — which is why V1 is the primary hypothesis, and
why V2 exists to tell those two effects apart.

---

## Hypotheses

| # | Hypothesis | Tested by |
|---|---|---|
| **H1** | Increasing address hydrophobicity at the `VV` pair increases δ-selectivity | V1, V2 |
| **H2** | The benefit requires **β-branching** (conformational restriction), not bulk alone | V1 vs V2 |
| **H3** | Asp and Glu addresses (deltorphin I vs II) are not equivalent on this chimeric scaffold | V3 |
| **H4** | The two levers (anionic residue, hydrophobic pair) are additive | V4 vs V1, V3 |
| **H5** | Shortening `GG`→`A` to restore true deltorphin register helps despite L-chirality | V5 |

---

## Variant panel

All variants keep the **`YGGF` message intact** (Cycle 1's F4L idea was rejected — Phe⁴ is
part of the message domain and mutating it abolishes activity at *both* receptors rather
than biasing selectivity). All keep the **terminal Gly** (PAM amidation signal). All are
encodable in the PENK cassette.

| ID | Sequence | Modification | Rationale |
|---|---|---|---|
| `C1-BASE` | `YGGFEVVG` | — | Cycle 1 baseline, already measured |
| **`V1`** | `YGGFEIIG` | Val→Ile ×2 | **PRIMARY.** DNA-encodable analog of `[Ile⁵,⁶]`deltorphin II. More hydrophobic **and** β-branched |
| `V2` | `YGGFELLG` | Val→Leu ×2 | **Control for H2.** Same added bulk/hydrophobicity as V1 but *not* β-branched |
| `V3` | `YGGFDVVG` | Glu→Asp | Deltorphin **I** address instead of II. Both natural, both highly δ-selective |
| `V4` | `YGGFDIIG` | Glu→Asp + Val→Ile | Combinatorial: tests additivity (H4) |
| `V5` | `YAFEVVG` | `GG`→`A`, 7-mer | True deltorphin register/length. Natural peptide has **D**-Ala²; only L-Ala is encodable, so this measures the chirality penalty |

10 new co-folds (5 variants × 2 receptors), identical settings to Cycle 1.

---

## Pre-registered predictions

**Ranking of Δ_sel** (most to least δ-selective):

```
V4  ≳  V1  >  V2  ≈  V3  >  C1-BASE  >  V5
```

Specific falsifiable calls:

1. **V1 > C1-BASE** on Δ_sel. If the Ile substitution does *not* beat baseline, the
   deltorphin `[Ile⁵,⁶]` result does not transfer to a `GG`-containing chimeric scaffold —
   a genuinely informative negative.
2. **V1 > V2.** If V1 ≈ V2, the benefit is bulk/hydrophobicity alone and β-branching is
   irrelevant here (H2 falsified). If V2 > V1, flexibility is *preferred*, contradicting
   the Cycle 1 rigidification reading.
3. **V1 shows tighter pose convergence than C1-BASE** (lower cross-sample spread, higher
   pLDDT). This is the direct test of Cycle 1's "floppy address" reading and is
   **independent of the selectivity result** — V1 could improve convergence without
   improving Δ_sel, or vice versa.
4. **V5 will lose δ-preference** relative to C1-BASE. L-Ala² cannot substitute for D-Ala²;
   predicted to confirm the chirality constraint is real rather than incidental.
5. **Δ_sel gains will be small in absolute terms** (order 0.01–0.05 ipTM). ipTM is a
   confidence score, not affinity — a 2400× binding ratio does **not** appear as a 2400×
   ipTM change. Rank order is the usable signal, not magnitude.

**Success criterion for the cycle:** at least one variant with Δ_sel > C1-BASE whose
peptide pose is *also* better converged. A variant that gains Δ_sel while getting floppier
is **not** carried forward.

---

## What this cycle cannot establish

- **No affinity prediction.** ipTM ranks; it does not give Kᵢ or fold-selectivity.
  The 2400×/18000× figures are wet-lab radioligand values for chemically-synthesised
  D-Ala² peptides and will not be reproduced by these scores.
- **No functional efficacy.** Nothing here distinguishes agonist from antagonist, or
  predicts G-protein vs β-arrestin bias — and biased agonism is central to opioid
  side-effect profiles.
- **No amidation or D-chirality.** Boltz sees linear, unamidated, all-L peptides. Real
  payload is amidated *in vivo* by PAM, so predictions are of the un-amidated precursor.
- **In-vivo stability is out of scope** — addressed by the co-delivered anti-MME siRNA,
  not by peptide chemistry.

**Required next step regardless of outcome:** competition radioligand binding at
DOR vs MOR for the top 2–3 variants. The purpose of this cycle is to decide *which*
variants earn that assay.

---

## References

- Erspamer et al. (1989) *PNAS* **86**:5188 — Deltorphins: naturally occurring peptides with
  high affinity and selectivity for δ opioid binding sites.
- Sasaki et al. (1991) *Biochem Biophys Res Commun* — `[D-Ala²]`deltorphin II analogs with high
  affinity and selectivity for the δ-opioid receptor (`[Ile⁵,⁶]` and related).
- Stewart & Hammond (1992) — Spinal antinociceptive effects of `[D-Ala²]`deltorphin II.
