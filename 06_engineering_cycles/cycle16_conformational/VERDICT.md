# Cycle 16 — G1 FAILS. No claim is made, and engPENK was not run.

**9 Oct 2026. Gates were committed in `4b3bdb5` before any trajectory was opened.**

## Result

β-turn occupancy of the message domain — fraction of frames with CA(i)–CA(i+3) < 7 Å,
the classic criterion, computed identically for all four peptides. 40 trajectories,
5 replicates × 2 receptors × 4 peptides, 20 ns each, matched protocol.

| peptide | selectivity | DOR occupancy | MOR occupancy | d(CA0–CA3) DOR |
|---|---|---|---|---|
| **EM-1** `YPWF`-NH₂ | **>1500× μ** | 0.181 ± 0.369 | **0.000 ± 0.000** | **0.776 nm** |
| deltorphin I | δ-selective | 1.000 ± 0.000 | 1.000 ± 0.000 | 0.562 nm |
| deltorphin II | δ-selective | 1.000 ± 0.000 | 0.601 ± 0.440 | 0.554 nm |
| met-enkephalin `YGGFM` | 3.7× δ | 0.999 ± 0.002 | 0.431 ± 0.415 | 0.521 nm |

## G1 — control validity: **FAIL**

Deltorphin (D-Ala², conformationally constrained) does **not** separate from met-enkephalin
(flexible). On DOR they are 1.000 versus 0.999 — indistinguishable. On MOR the deltorphin II
and met-enkephalin distributions overlap almost completely (0.601 ± 0.440 vs 0.431 ± 0.415).

Per the pre-registration: *"If it does not, these metrics do not capture backbone constraint
in this system and the analysis is UNINFORMATIVE — report that and stop."*

## G2 — **not a pass**

EM-1 separates from met-enkephalin strongly and reproducibly. But it is the **most extended**
peptide in the set (0.78–0.89 nm, occupancy ~0), not the most turn-like — the **opposite** of
what the β-turn hypothesis predicted. And G1 established no direction for G2 to agree with.

## G3 — **NOT SCORED. engPENK was not run.**

The decision rule said G3 is scored only if G1 and G2 pass. They did not. **No conformational
claim about `YGGFEVVG` is made, and the GPU time for its matched run was not spent.**

## Two faults in my own analysis, disclosed

1. **The radius-of-gyration column is invalid.** I passed `gmx gyrate` group 0 of an
   all-protein-CA index, so it measured the **receptor**, not the peptide — values of
   2.34–2.77 nm, where a 5–8 residue peptide is 0.5–0.8 nm. Excluded from scoring.
   The column is left in `data/c16_metrics.csv` marked invalid rather than deleted.
2. **Peptide lengths in the pre-registration were wrong.** Deltorphin carries an `NHE`
   amide cap as its own residue (8 residues, 7 CA, not 7/7) and EM-1 likewise (5/4, not 4/4).
   Caught by a verification pass before the analysis ran, not after.

## Why G1 most likely failed: the trajectories are not converged for this observable

Replicate scatter **within a single system**:

| | per-system SD across 5 replicates |
|---|---|
| DOR | dtI 0.000 · dtII 0.000 · menk 0.002 · **em1 0.369** |
| MOR | dtI 0.000 · em1 0.000 · **dtII 0.440** · **menk 0.415** |

On MOR, replicates of the *same* peptide span 0.00 to 1.00. Identical systems differing only
in seed give opposite answers. That is not a property of the peptide; **20 ns from a modelled
starting pose does not re-equilibrate a bound peptide's backbone conformation.** Where
occupancy is 0.000 or 1.000 with zero variance, the peptide never left its starting basin.

So this analysis cannot distinguish "these peptides genuinely have these conformations" from
"the docked starting poses dominate and the sampling never escaped them". That is precisely
what the control gate exists to detect, and it detected it.

## What would make it answerable

Far longer sampling, or enhanced sampling of the peptide backbone (metadynamics / replica
exchange on the φ/ψ space), started from multiple independent poses. That is a larger
undertaking than this cycle, and it should not begin before the cAMP assay — which measures
the quantity of interest directly and is subject to none of this.

## What stands

The literature finding is unaffected and remains the most useful thing from this round:
Acta Pharm Sin B 2026 reports selectivity arising from conformational constraint beyond the
message-address framework, and our payload was **forced** to drop both of deltorphin's
constraining features — D-Ala² and the C-terminal amide — because a gene can encode neither.
That remains a plausible explanation for four cycles of null selectivity results. **We have
not demonstrated it, and this cycle does not entitle us to claim it.**
