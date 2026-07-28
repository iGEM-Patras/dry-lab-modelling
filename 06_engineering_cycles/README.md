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
| **1** | Graft the **deltorphin II address** onto the enkephalin message | `YGGFEVVG` | ✅ complete | Directionally δ-ward; **quantitative claim withdrawn** (see correction) |
| **2** | Enhance address hydrophobicity / anionic residue (literature-guided) | 5 variants | ✅ complete | **Primary hypothesis falsified** — 4 of 5 predictions wrong; V4/V5 retained |
| **3a** | Validate pose convergence as a selectivity metric | *no new sequences* | ✅ complete | **H3a rejected** — does not replicate; metric retired |
| **3b** | Combine Cycle 2's two independent wins | `YAFDIIG` | ⛔ premise withdrawn | V5's "win" is within noise at n=20 — see 3a recommendation |

- [`cycle1_deltorphin_chimera/CYCLE1.md`](cycle1_deltorphin_chimera/CYCLE1.md) — retrospective writeup **+ correction notice**
- [`cycle2_delta_selectivity/CYCLE2_DESIGN.md`](cycle2_delta_selectivity/CYCLE2_DESIGN.md) — pre-registration (committed before the runs)
- [`cycle2_delta_selectivity/CYCLE2_RESULTS.md`](cycle2_delta_selectivity/CYCLE2_RESULTS.md) — results, prediction scoring, Cycle 1 correction
- [`cycle3a_convergence_metric/CYCLE3A_DESIGN.md`](cycle3a_convergence_metric/CYCLE3A_DESIGN.md) — pre-registration
- [`cycle3a_convergence_metric/CYCLE3A_RESULTS.md`](cycle3a_convergence_metric/CYCLE3A_RESULTS.md) — held-out replication, scorecard, recommendation

## What counts as a cycle here

A cycle is defined by its **Learn → Design edge**, not by the number of constructs it
contains. Variants that were all designed from the *same* Learn output, tested in
parallel, and interpreted against each other are **one cycle with a multi-arm panel** —
Cycle 2's five variants are controls for one another (V3 is the Asp-without-Ile control
for V4; V2 isolates β-branching from bulk in V1) and are meaningless in isolation.

Splitting a parallel panel into one "cycle" per variant would produce loops with
identical Design inputs and no Learn edges between them. That inflates cycle count while
reducing cycle depth. Conversely, Cycle 3 **is** split into 3a and 3b because 3a's
result determines what metric 3b is judged on — a genuine sequential dependency.

## Track record

Predictions are committed and pushed **before** the corresponding runs are launched, so
the falsification record is auditable in the git history.

| Cycle | Predictions made | Confirmed | Falsified | Pre-registration commit |
|---|---|---|---|---|
| 2 | 5 | 1 | **4** | `f2d6ade` (before job `ac2c837e`) |
| 3a | 5 | 3 | **2** (both decisive) | `ec7123d` (before job `1391bb2a`) |

**Cumulative: 10 predictions, 4 confirmed, 6 falsified.** The two Cycle 3a falsifications
rejected the cycle's own hypothesis; the three confirmations include P5, which predicted
that our *previous* cycle's ranking was unreliable — and it was.

A high falsification rate is the intended outcome of honest pre-registration, not a
failure of the project.

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
