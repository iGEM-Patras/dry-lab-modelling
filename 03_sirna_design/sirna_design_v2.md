# Anti-Neprilysin (MME) siRNA — deepened design (v2)

This extends the v1 sequence/thermodynamic/off-target design with two
independent lines of evidence that v1 did not include:

1. **Target-site accessibility** — whether the mRNA region is structurally
   open for RISC to reach, computed by local RNA secondary-structure folding.
2. **A composite ranking** that integrates accessibility, thermodynamic
   asymmetry, and the v1 specificity score into one transparent number, plus
   the explicit **guide seed** (positions 2–8) for downstream seed-match
   off-target checking.

## Methods added in v2

**Accessibility (ViennaRNA local folding).** The full MME reference mRNA
(NM_000902.5, 5,593 nt) was folded with RNAplfold-style local partition-function
folding (window W=240, averaging span L=160). For each candidate 19-mer target
site we report:
- `accessibility_P_unpaired` — probability the entire 19-nt site is
  simultaneously single-stranded (a stringent all-or-nothing metric; all values
  are small, so it is informative only as a *ranking*).
- `mean_unpaired_19nt` — mean per-nucleotide unpaired probability across the
  site (the interpretable accessibility measure; higher = more open).
- `seed_region_unpaired` — mean unpaired probability over the target nucleotides
  contacted by the guide seed. Seed accessibility is the region most predictive
  of cleavage initiation.

**Composite score (0–100).** Transparent weighted sum, min–max normalised:
- 35 × specificity (v1 blastn specificity score / 100)
- 25 × accessibility (mean unpaired, normalised)
- 20 × thermodynamic asymmetry (ΔΔG, normalised)
- 10 × Reynolds/Ui-Tei design score
- 10 × seed-region accessibility (normalised)

**Guide seed.** Positions 2–8 of each guide are reported; the reverse
complement is the mRNA site a seed-mediated (miRNA-like) off-target would
present in its 3′UTR. This is the metric that governs seed-driven off-targeting,
which full-length identity screens miss.

## Result — the v1 recommendation holds

Adding accessibility did **not** overturn the v1 choice; it re-prioritised
within it. The four v1-recommended guides remain the top four by composite
score:

| new rank | guide | CDS pos | composite | mean P(unpaired) | seed P(unpaired) | ΔΔG | specificity | off-targets ≥17/19 | guide seed (2–8) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | CDS1224 | 1224 | 68.6 | 0.43 | 0.58 | +0.98 | 100 | 0 | UAGUUUG |
| 2 | CDS1590 | 1590 | 65.1 | 0.61 | 0.47 | +1.93 | 26 | 0 | AUCCACU |
| 3 | CDS1032 | 1032 | 59.6 | 0.35 | 0.59 | +2.33 | 58 | 0 | UCUGGAG |
| 4 | CDS759  | 759  | 52.4 | 0.39 | 0.34 | +1.31 | 68 | 0 | UCCUGAC |

**CDS1224 rises to the top** — it combines perfect specificity (0 off-targets at
any identity band) with good accessibility, making it the single best
first-choice guide.

**CDS1590 has the most open target site** (mean P_unpaired 0.61) but a modest
specificity score; it remains a strong second because its off-target hits are
all below the ≥17/19 silencing-risk band.

One screened-but-rejected guide, CDS1907, ties CDS759 on composite because its
site is highly accessible — but it carries **17 near-full-length off-targets**
and is correctly kept out of the recommended set by the specificity weight.
Accessibility never overrides specificity here.

## Recommendation

Order the same four guides as v1, now with a defensible priority order:
**CDS1224 (first choice) ≥ CDS1590 > CDS1032 > CDS759.** Validate ≥2 by qPCR as
before. The accessibility layer strengthens the case that these sites are
physically reachable, not just sequence-valid.

## Limitations

- Local folding approximates accessibility from sequence alone; it does not
  model RNA-binding proteins or in-cell structure. It is a prioritisation aid,
  not a guarantee.
- A full transcriptome-wide **seed-match frequency** count (how many human
  3′UTRs carry each guide's seed site) was not run here — it needs a 3′UTR
  database scan that the shared login node could not sustain. The seed sequences
  are reported so this can be run directly (e.g. against a UTR FASTA or with a
  seed-match tool) as a follow-up.
