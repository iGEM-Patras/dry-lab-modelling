# Engineering Cycles — δ-selective enkephalin payload

This directory documents the iterative **Design → Build → Test → Learn (DBTL)** engineering
of the analgesic peptide payload expressed from the engineered PENK therapy plasmid.

## Why iterate on the peptide at all?

The therapy delivers a proenkephalin (PENK) cassette so that transduced cells secrete
enkephalin locally, plus an siRNA that silences neprilysin (MME) so the secreted peptide
is not immediately degraded. Enkephalin acts at two opioid receptors:

| Receptor | Gene | Consequence of agonism |
|---|---|---|
| **δ (DOR)** | `OPRD1` | analgesia, anxiolytic; **much lower respiratory-depression and dependence liability** |
| **μ (MOR)** | `OPRM1` | analgesia, but also respiratory depression, constipation, tolerance, dependence |

Native Met-enkephalin (`YGGFM`) is only weakly δ-preferring. **Biasing the payload toward
δ is therefore a safety-driven design goal**, not a cosmetic one: it retains analgesia while
reducing the μ-mediated adverse-effect profile that makes conventional opioids dangerous.

## Cycle index

| Cycle | Design concept | Payload | Status | Result |
|---|---|---|---|---|
| **1** | Graft the **deltorphin II address** onto the enkephalin message | `YGGFEVVG` | ✅ complete | δ-preference **1.96×** native |
| **2** | Enhance address hydrophobicity / anionic residue (literature-guided) | 5 variants | 🔄 in progress | — |

- [`cycle1_deltorphin_chimera/CYCLE1.md`](cycle1_deltorphin_chimera/CYCLE1.md) — retrospective DBTL writeup
- [`cycle2_delta_selectivity/CYCLE2_DESIGN.md`](cycle2_delta_selectivity/CYCLE2_DESIGN.md) — pre-registered design + predictions

## Shared method

All peptide–receptor complexes are predicted with **Boltz-2** co-folding against the
full-length human receptor (UniProt canonical sequence), under identical settings:

```
boltz predict <complex>.yaml --use_msa_server \
  --subsample_msa --num_subsampled_msa 1024 \
  --recycling_steps 3 --diffusion_samples 5 --sampling_steps 200
```

Receptor chain uses a full MSA (1024 sequences); the peptide chain uses `msa: empty`
(a 5–8-mer has no meaningful alignment). **All cycles use identical settings**, so
cross-variant comparisons are internally controlled.

### Selectivity metric

$$\Delta_{sel} = \text{ipTM}(\text{DOR complex}) - \text{ipTM}(\text{MOR complex})$$

ipTM is Boltz's predicted interface TM-score — a **confidence** measure for the
peptide–receptor interface. A larger $\Delta_{sel}$ means the model is more confident about
the δ interface than the μ interface for that same peptide.

### ⚠ Interpretation limits (read before quoting any number here)

- **ipTM is not binding affinity.** It is a structural-confidence score. It ranks and
  triages designs; it does **not** predict $K_i$, $IC_{50}$, or fold-selectivity.
- Differences of ~0.01–0.02 ipTM are near the noise floor. We therefore report
  **mean ± SD across the 5 diffusion samples** and treat only separated distributions
  as meaningful.
- Boltz sees the **unamidated, linear L-amino-acid** peptide. It cannot represent
  D-amino acids or C-terminal amidation, both of which matter for real deltorphin
  pharmacology (see Cycle 2 design notes).
- **Wet-lab radioligand competition binding at DOR vs MOR is the only real test.**
  These predictions exist to choose which 2–3 variants are worth synthesising.

## Constraint that shapes every design

The payload is **expressed from a plasmid**, so it must be encodable in DNA:
**20 standard L-amino acids only**. This rules out the classic high-selectivity
opioid-peptide tricks — D-amino acids (D-Ala²), penicillamine cyclisation (DPDPE),
N-methylation — which is why the design space here is the *address domain sequence*
rather than backbone chemistry.

One partial exception is exploited deliberately: a **C-terminal Gly is the recognition
signal for peptidylglycine α-amidating monooxygenase (PAM)** in mammalian secretory
granules, so a `...VVG` payload can be post-translationally converted to the
`...VV-NH₂` amide *in vivo* — recovering the amidation that natural deltorphins require.
The terminal Gly in every design is therefore load-bearing and must be retained.
