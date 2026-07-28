# Cycle 3a — Results

**Status:** complete · 14/14 co-folds succeeded (job `1391bb2a`, 57 min on one RTX 2080 Ti)
**Held-out set:** 15 fresh diffusion samples per complex, seed 2026, 210 structures total
**Verdict:** **H3a REJECTED.** Pose convergence does not replicate as a selectivity proxy.

---

## Prediction scorecard

| # | Prediction | Result | Verdict |
|---|---|---|---|
| P1 | ρ(δ-convergence, Δ_sel) < 0 on held-out, permutation p < 0.05 | ρ = **−0.536**, p = **0.237** | ❌ **FALSIFIED** |
| P2 | Relationship survives dropping V1/V2 | ρ = **+0.300** (sign flips) | ❌ **FALSIFIED** |
| P3 | Convergence better-powered than ipTM | 11.3 vs 1.3 spread/noise | ✅ CONFIRMED |
| P4 | V4/V5 remain best-converged δ complexes | V5 (0.49 Å), V4 (0.84 Å) | ✅ CONFIRMED |
| P5 | The n=5 Δ_sel ranking is **unstable** | top-2 changed; SEM ↓ 53 % | ✅ CONFIRMED |

**3 of 5 confirmed — but the two that failed are the two that decide the hypothesis.**
The success criterion required **P1 *and* P2**. Neither held.

---

## Held-out data (n = 15, seed 2026)

| id | sequence | ipTM δ | ipTM μ | Δ_sel | SEM | p | conv δ (Å) | conv μ (Å) |
|---|---|---|---|---|---|---|---|---|
| C1-BASE | `YGGFEVVG` | 0.9670 | 0.9628 | **+0.0043** | 0.0046 | 0.37 | 1.88 | 4.29 |
| V4 | `YGGFDIIG` | 0.9693 | 0.9663 | +0.0030 | 0.0035 | 0.40 | **0.84** | 2.16 |
| V3 | `YGGFDVVG` | 0.9703 | 0.9694 | +0.0009 | 0.0036 | 0.80 | 2.10 | 3.58 |
| V5 | `YAFEVVG` | 0.9687 | 0.9684 | +0.0002 | 0.0042 | 0.96 | **0.49** | 6.12 |
| native | `YGGFM` | 0.9741 | 0.9751 | −0.0010 | 0.0031 | 0.75 | 1.45 | 2.00 |
| V1 | `YGGFEIIG` | 0.9646 | 0.9707 | −0.0061 | 0.0037 | 0.11 | 4.04 | 2.19 |
| V2 | `YGGFELLG` | 0.9644 | 0.9737 | **−0.0093** | 0.0032 | **0.008** | 4.42 | 2.66 |

---

## What went wrong with the hypothesis

**The correlation was carried entirely by V1 and V2.** In the discovery set those two
were extreme on both axes (δ-convergence 5.89 and 4.16 Å against ≤1.42 Å for everything
else, and the only negative Δ_sel values). A rank correlation over n = 7 with two joint
outliers is essentially a two-point fit. Remove them and the sign inverts: ρ = **+0.300**,
i.e. among the five well-behaved peptides, *better* δ-convergence goes with *less*
δ-preference — the opposite of H3a.

**Convergence itself is not reproducible at the peptide level.** V1's δ-convergence moved
5.89 → 4.04 Å and V3's 0.90 → 2.10 Å between sample sets. The metric has a large spread
*between* independent sample draws of the same complex, which is exactly what P3's
favourable spread/noise ratio failed to capture: P3 measured dispersion *within* one
sample set, not reproducibility *across* sets. **P3 is therefore confirmed but
uninformative** — a well-powered measurement of an unstable quantity.

That is the methodological lesson of this cycle: high spread-to-noise within a run is not
evidence of a reliable metric. Only replication on independent samples tests that, and
this is why the cycle was designed around held-out data rather than a bigger single run.

---

## P5 — our own Cycle 2 ranking was unreliable, as predicted

| | ranking (best δ first) |
|---|---|
| n = 5 (discovery) | V4 > V5 > C1-BASE > native > V3 > V2 > V1 |
| n = 15 (held-out) | **C1-BASE > V4 > V3 > V5 > native > V1 > V2** |

V5 fell from 2nd to 4th; V3 rose from 5th to 3rd; the top-2 changed. Mean SEM fell 53 %
(0.0079 → 0.0037), confirming n = 5 was badly under-powered.

**Effect sizes shrank toward zero as n grew** — the signature of noise-driven estimates:

| peptide | Δ_sel n=5 | Δ_sel n=15 | pooled n=20 |
|---|---|---|---|
| C1-BASE | +0.0115 | +0.0043 | +0.0061 |
| V4 | +0.0152 | +0.0030 | +0.0060 |
| V5 | +0.0122 | +0.0002 | +0.0032 |
| V1 | −0.0162 | −0.0061 | −0.0086 |

At n = 20, **no peptide reaches Δ_sel > 0.007**, and the largest values (C1-BASE +0.0061,
V4 +0.0060) are indistinguishable from each other. The one surviving significant result is
still **V2 `YGGFELLG` preferring μ** (p = 0.008) — reproducing Cycle 2's direction with a
different variant, and reinforcing that added aliphatic bulk in the address biases μ-ward,
opposite to the D-Ala²-backbone literature.

---

## Consequences for the project

1. **No engineered payload in this series is demonstrably δ-selective.** Across 7 peptides
   and 20 samples each, every Δ_sel is ≤ 0.006 with SEM ≈ 0.004. Boltz-2 ipTM cannot
   resolve δ/μ selectivity at the magnitude our designs produce.
2. **Pose convergence is retired as a selectivity metric.** It stays in the record as a
   *diagnostic* — V1/V2's 4 Å δ-pose spread is a real sign the model cannot place those
   peptides confidently — but not as a selectivity readout.
3. **Cycle 3b's premise is undermined.** It was to combine V4's and V5's "independent
   wins". At n = 20, V5's win is +0.0032 ± 0.004 — not a win. Combining two effects that
   are themselves within noise is not a design rationale.
4. **The honest conclusion is that the in-silico screen has reached its resolution limit.**
   The next informative experiment is wet-lab, not another fold.

---

## Recommendation for Cycle 3b

**Do not run the combined variant as a selectivity screen.** Two options, both honest:

- **(a) Close the modelling line.** Take `YGGFEVVG` (C1, best at n=20 and already the
  built construct) and `YGGFDIIG` (V4, statistically tied) to radioligand competition
  binding at OPRD1/OPRM1. The screen's actual output is a shortlist of 2, which is what
  it was ever able to deliver.
- **(b) Change the observable.** If Cycle 3b is to stay in silico, it must measure
  something with more dynamic range than ipTM — e.g. MM-GBSA rescoring of the co-fold
  poses, or explicit-solvent MD of the peptide–receptor complexes with per-residue
  interaction energies. That is a new method, so it needs its own pre-registration.

Either way, **`YGGFDIIG` (V4) remains the one design with a mechanistic rationale that
survived**: Asp⁴ + Ile⁵'⁶ was predicted to be additive, and it is the only variant that
is both non-negative on Δ_sel at every n and tightly converged in the δ pocket.

---

## Files

| File | Contents |
|---|---|
| `data/cycle3a_results.csv` | held-out ipTM ± SD, Δ_sel, SEM, p, convergence, plus n=5 and pooled n=20 |
| `figures/cycle3a_replication.png` | discovery-vs-replication scatter + effect-size shrinkage |
| `CYCLE3A_DESIGN.md` | pre-registration (committed `ec7123d`, **before** job `1391bb2a`) |

## Standing limits (unchanged)

ipTM and pose convergence are structural-confidence measures, not binding affinity.
Radioligand competition binding at OPRD1/OPRM1 remains the only real test. Boltz-2 cannot
represent D-amino acids or C-terminal amidation, so all conclusions are conditional on the
all-L, free-acid approximation. All metrics are mean ± SD over all diffusion samples.
