> **SUPERSEDED IN PART — see [`ORDER.md`](ORDER.md) for the current order sheet.**
> The primary guide is unchanged (this document's position 2541 in `NM_000902.5` is
> 2700-2722 on MME-213). The **second guide has changed**: DSIR efficacy scoring and a
> direct count of seed sites across 20,094 human 3' UTRs, neither available when this was
> written, moved it to **2562-2584**. Everything else below stands.

# Anti-neprilysin siRNA — validation record

**Target:** human *MME* (neprilysin / CD10), the enzyme that degrades enkephalins.
Knocking it down extends the payload's half-life; it does not change receptor preference.
The pharmacology of inhibiting neprilysin is established — sacubitril is an approved
neprilysin inhibitor.

**Recommendation: position 2541** (= 2700-2722 on MME-213) — **still current**.

~~with position 2066 as the hedge~~ — **superseded.** The second guide is now
**2562-2584**, after DSIR efficacy scoring and a direct seed-site count across human
3' UTRs. See [`ORDER.md`](ORDER.md).

```
2541   guide      5'-AAUGAUUGACUUGAUAGACCU-3'
       passenger  5'-GUCUAUCAAGUCAAUCAUUUC-3'
```

Everything below is **predicted**. No number here is a measurement of knockdown. The
decisive test is a knockdown panel with qPCR against a scrambled control; the purpose of
this ranking is only to decide which two or three guides are worth that bench time.

---

## 1 · What the input already contained

The candidate file is **siDirect** output (206 guides, 21-mers). It had already applied:

| filter | threshold |
|---|---|
| Ui-Tei functional selection | pass required |
| seed-duplex Tm | ≤ 21.5 °C |
| genome-wide perfect matches | exactly 1 (the target itself) |
| genome-wide 1-mismatch off-targets | 0 |

So the specificity screen was done before we started. All 206 pass all four. That means
**no ranking signal is available from those columns** — they are constant across the set —
and the ranking has to come from checks siDirect does not perform.

---

## 2 · Filters we added — 206 → 17

| check | threshold | rationale | guides lost |
|---|---|---|---|
| transcript-variant coverage | must hit **all four** *MME* variants | a guide hitting only one variant misses the canonical transcript entirely | 3 |
| off-target stringency | minimum mismatch ≥ 3 | 2-mismatch off-targets can still silence | 164 |
| GC content | 30–52 % | outside this range loading and duplex stability degrade | 14 |
| nucleotide runs | no run of ≥ 4 identical bases | synthesis and structural liability | 7 |
| immunostimulatory motif | no `UGUGU` | interferon response | 1 |

Transcript variants checked by exact sequence match against
**NM_000902.5, NM_007287.4, NM_007288.3, NM_007289.4** fetched from NCBI. This also
identified the transcript siDirect was run on: **NM_007288.3** (5,818 nt), the only variant
containing all 206 target sites — the input was not the canonical transcript.

---

## 3 · Accessibility — and the one step that makes the numbers comparable

**Method.** RNAplfold local partition function (ViennaRNA 2.7.2) on **NM_000902.5**, window
**W = 240**, maximum base-pair span **L = 160**, unpaired-stretch length **u = 21**. Mean
per-nucleotide unpaired probability across the 21-nt site.

These are **not our parameters.** They were read out of this project's own
`sirna_design_v2.md` so that new numbers would land on the scale of the existing v2 design
rather than a parallel one.

**Validation.** Before computing anything new, we recomputed the accessibility of all
**11 guides from the v2 design** and compared against their published values.

> **All 11 reproduced exactly** — agreement to four decimal places, including the
> all-unpaired probabilities to the exponent, **r = 1.0000**.

That check is what licenses the comparison. Without it, "2541 is more accessible than your
best v2 guide" would be comparing two different scales.

**Result.** Position 2541 at **0.658** mean unpaired probability, against **0.608** for the
most accessible guide in the v2 design.

---

## 4 · Robustness — does the pick survive a different folding window?

Accessibility is window-dependent, so a guide that only wins at one setting is not a pick.
We re-folded the whole transcript at four (W, L) settings and re-ranked all 17.

| guide | W=240/160 | W=160/120 | W=320/200 | W=200/150 | worst-case rank |
|---|---|---|---|---|---|
| **2541** | **1** | **1** | **1** | **1** | **1** |
| 2066 | 2 | 2 | 2 | 3 | 3 |
| 954 | 3 | 3 | 2 | 2 | 3 |
| 2403 | 5 | 4 | 5 | 8 | 8 |

**2541 ranks first under every setting tested.** The pick is not an artifact of the W=240
choice inherited from v2.

---

## 5 · SNP overlap — the check that changed the recommendation

A common variant under the guide abolishes silencing in carriers. This had **not** been
done in earlier rounds and is the reason this document exists.

**Method.** Each 21-mer was located in the Ensembl transcript **ENST00000360490** by exact
sequence match, then mapped to genomic coordinates via Ensembl's cDNA-to-genomic mapping,
then queried for overlapping variants.

Two methodological points, both of which would have produced wrong answers if skipped:

1. **Sequence match, not coordinate arithmetic.** The Ensembl transcript is 5,656 nt against
   RefSeq's 5,593 — a constant 63 nt offset from a longer 5′ UTR. Locating sites by sequence
   established that offset rather than assuming the two numbering systems agreed. All 17
   mapped with the full 21 nt accounted for.
2. **Alternate-allele frequency, not the maximum over alleles.** A first pass took the
   highest frequency across all population records and returned **1.0 for every variant** —
   that is the *reference* allele. The reference base is the first entry in the variant's
   allele string; frequencies must be taken over the non-reference alleles only.

**Result across the 17 sites:** 119 unique overlapping variants. Only 6 carry a minor allele
frequency in Ensembl's summary field, all ≤ 0.08 %. The remaining 113 have no frequency
estimate there, so for the four candidates in contention we queried per-population
(gnomAD / 1000 Genomes) records directly.

| guide | overlapping variants | with frequency data | max alternate-allele frequency | verdict |
|---|---|---|---|---|
| **2541** | 9 | 6 | **0.0087 %** (rs373943993) | clean |
| **2066** | 8 | 4 | **0.0076 %** (rs772109678) | clean |
| 954 | 8 | 8 | **1.92 %** (rs149431215) | **DISQUALIFIED** |
| 2403 | 12 | 12 | 0.057 % (rs1392465018) | clean |

**Position 954 carries rs149431215 at 1.92 % alternate-allele frequency.** It had ranked
2nd–3rd for accessibility under every folding window and was about to be recommended as the
hedge. Roughly 1 in 26 people carry that allele, and in them this guide would have a
central mismatch.

This is the single result that changed the output of the whole exercise.

**One incidental finding:** position 2066 spans an exon–exon junction. That is a point in its
favour — such a guide cannot target pre-mRNA or genomic DNA, only the mature transcript.

---

## 6 · What we could not do

**No positive control exists that we could find.** The strongest possible validation would be
to score published, experimentally-validated *MME* siRNAs through this pipeline and check
that it ranks known-working guides highly — the same gate structure used elsewhere in this
project. A literature search returned several studies that knock down neprilysin, but all
used commercial reagents and none of the abstracts disclose the guide sequence. **So this
ranking has not been tested against any guide of known efficacy.** That is a real limitation
and not a formality.

**Consequence:** the ranking is a prioritisation, not a prediction of knockdown. It answers
"which guides are worth testing" and not "how well will this work".

---

## 7 · Recommendation

**Order position 2541 and position 2066, plus a scrambled control.**

They fail differently, which is the point of ordering two: 2541 wins on whole-site
accessibility (0.658, rank 1 under every window), while 2066 has a more open seed region and
spans an exon junction. Both are clean on specificity, variant load, GC, runs and motifs.

**Do not order 954** despite its accessibility ranking — rs149431215 sits under it at 1.92 %.

**Decide by qPCR**, not by this table.

---

## Files

| file | contents |
|---|---|
| `mme_sirna_final_ranked.csv` | all 17 survivors with accessibility, seed openness, specificity, sequences |
| `mme_sirna_all206_annotated.csv` | all 206 with every filter result and variant coverage |
| `sirna_window_robustness.csv` | accessibility and rank of the 17 under four folding windows |
| `sirna_snp_overlap.csv` | variant counts per target site |
| `sirna_candidate_validation.csv` | the four-candidate comparison above |
| `sirna_2541_variants.csv` | per-variant alternate-allele frequencies at the recommended site |
| `sirna_variant_detail.json` | every overlapping variant, per site, with consequence |
| `sirna_lit_search.json` | the literature search behind §6 |
