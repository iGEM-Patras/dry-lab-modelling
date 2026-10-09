# 03 · Human anti-NEP (MME) siRNA design

Silencing **neprilysin (NEP / CD10, gene MME)**, the principal enkephalin-degrading peptidase, prolongs the half-life of the enkephalins produced by the PENK construct. This is the knockdown arm of the therapy.

**Target:** all four human MME transcript variants (NM_000902.5, NM_007287/288/289) share an **identical 2,253 bp CDS**; every design targets that shared CDS, so a single siRNA silences all isoforms.

**Pipeline:** 2,084 candidate 19-mers → 228 pass sequence rules (Reynolds + Ui-Tei) → ranked by thermodynamic duplex-end asymmetry → off-target screened by NCBI blastn-short vs human `refseq_rna`.

**Four recommended duplexes** (19/19 on-target, 0 off-targets ≥17/19; 3′ dTdT overhangs):

| # | CDS pos | Guide (5'→3') | GC% | ΔΔG |
|---|---------|---------------|-----|-----|
| si-MME-1 | 759 | UUCCUGACGAAUCAAUCUGdTdT | 42.1 | +1.31 |
| si-MME-2 | 1032 | UUCUGGAGCAUAAACAACCdTdT | 42.1 | +2.33 |
| si-MME-3 | 1224 | AUAGUUUGCACAACGUCUCdTdT | 42.1 | +0.98 |
| si-MME-4 | 1590 | UAUCCACUCAUCUUUGUCCdTdT | 42.1 | +1.93 |

**Validation:** qPCR of MME at 48 h (expect ≥70% knockdown for ≥2 duplexes) + NEP activity / CD10 Western; use ≥2 effective siRNAs to control for off-target phenotypes.

## Files
- `sirna_design_table.csv`: full candidate scoring: guide + passenger strands, mRNA/CDS positions, GC, ΔΔG, off-target counts.
- `sirna_design.md`: design rationale and method notes.
- `sirna_design_figure.png`: target positions, off-target load, and guide-loading asymmetry vs GC.
