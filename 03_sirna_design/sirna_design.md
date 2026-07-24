# Human anti-Neprilysin (MME) siRNA Design

## Rationale
Neprilysin (NEP / CD10 / enkephalinase, gene **MME**) is the principal peptidase
degrading enkephalins. Silencing it prolongs the half-life of the enkephalin
peptides produced by the PENK construct — the knockdown arm of the therapy.

## Target definition
- **Gene:** MME (membrane metalloendopeptidase), human.
- **Transcript variants screened:** NM_000902.5, NM_007287, NM_007288, NM_007289.
- **Key fact:** all four variants share an **identical 2,253 bp CDS** (they differ
  only in the 5′UTR / first exon). Any CDS-targeting siRNA therefore silences
  **every** isoform. All designs target the shared CDS.

## Pipeline
1. Enumerated all 2,084 possible 19-mer target sites across the CDS (excluding the
   first/last 75 nt).
2. **Sequence rules** (Reynolds + Ui-Tei): GC 30–52%, A/U-rich guide 5′ end,
   position-specific base preferences (pos1 G/C, pos19 A/U, pos10 U), no
   homopolymer runs ≥4, no GC stretch >9, no immunostimulatory motifs. → 228 pass.
3. **Thermodynamic asymmetry**: nearest-neighbour ΔΔG between the two duplex ends;
   positive ΔΔG (guide 5′ end less stable) favours correct guide-strand loading
   into RISC.
4. **Off-target screen**: NCBI blastn-short (word size 7) of a position-diverse
   11-candidate shortlist against human `refseq_rna` (txid9606). Ranked by number
   of near-full-length off-targets (≥17/19 identity — the band that risks
   silencing).

## Recommended siRNAs (all 19/19 on-target to MME; 0 off-targets ≥17/19)
| # | CDS pos | mRNA pos | Guide / antisense (5'→3') | Passenger / sense (5'→3') | GC% | ΔΔG | worst off-target |
|---|---------|----------|---------------------------|---------------------------|-----|-----|------------------|
| si-MME-1 | 759 | 854 | 5'-UUCCUGACGAAUCAAUCUGdTdT-3' | 5'-CAGAUUGAUUCGUCAGGAAdTdT-3' | 42.1 | +1.31 | 16/19 |
| si-MME-2 | 1032 | 1127 | 5'-UUCUGGAGCAUAAACAACCdTdT-3' | 5'-GGUUGUUUAUGCUCCAGAAdTdT-3' | 42.1 | +2.33 | 16/19 |
| si-MME-3 | 1224 | 1319 | 5'-AUAGUUUGCACAACGUCUCdTdT-3' | 5'-GAGACGUUGUGCAAACUAUdTdT-3' | 42.1 | +0.98 | 14/19 |
| si-MME-4 | 1590 | 1685 | 5'-UAUCCACUCAUCUUUGUCCdTdT-3' | 5'-GGACAAAGAUGAGUGGAUAdTdT-3' | 42.1 | +1.93 | 16/19 |

All strands carry standard **3′ dTdT** overhangs (19+2 format). Order as annealed
duplexes.

## Recommended validation
- **qPCR** of MME mRNA 48 h post-transfection (test all 4; expect ≥70% knockdown
  for ≥2 of them).
- **NEP activity assay** or Western (CD10) to confirm functional knockdown.
- Use **≥2 independent effective siRNAs** (or a validated pool) to control for
  off-target phenotypes.
- Non-targeting scrambled control + untreated.

## Caveat (recorded from project bibliography)
The bibliography includes a report that NEP silencing can have context-dependent
effects; the knockdown arm should be evaluated against that literature before
in-vivo use. This design provides the tool reagents; it does not settle the
biological strategy.
