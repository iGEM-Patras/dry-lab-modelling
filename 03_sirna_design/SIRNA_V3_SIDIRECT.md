> **SUPERSEDED IN PART — see [`ORDER.md`](ORDER.md) for the current order sheet.**
> The primary guide is unchanged (this document's position 2541 in `NM_000902.5` is
> 2700-2722 on MME-213). The **second guide has changed**: DSIR efficacy scoring and a
> direct count of seed sites across 20,094 human 3' UTRs, neither available when this was
> written, moved it to **2562-2584**. Everything else below stands.

# Anti-neprilysin siRNA — v3, siDirect candidates screened and placed on the v2 scale

**Input.** 206 siDirect candidates (21-nt guide + 21-nt passenger), supplied by the wet lab.
siDirect had already applied: Ui-Tei functional selection, seed-duplex Tm <= 21.5 C, and a
genome-wide specificity check. All 206 have exactly one perfect-match hit (the target
itself) and **zero** 1-mismatch off-targets.

**Parsing note.** The sheet contains an unlabelled blank column, so every field from the Tm
onward is shifted by one. A naive read puts the passenger Tm in the minimum-mismatch column
and silently inverts the ranking.

## Isoform coverage — three candidates must be excluded

The siDirect input was **NM_007288.3** (5,818 nt; transcript variant 3), not the canonical
NM_000902.5 (5,593 nt). Checking all 206 against all four MME transcript variants:

- **203 of 206 hit all four variants** — good coverage.
- **3 hit only NM_007288** and would miss the canonical transcript. Excluded.

## Screening — four filters siDirect does not apply

| filter | remaining |
|---|---|
| siDirect output | 206 |
| hits all four MME variants | 203 |
| no off-target closer than 3 mismatches | 39 |
| GC 30-52% | 25 |
| no run of >=4 identical nt | 18 |
| no immunostimulatory motif | **17** |

## The two pipelines disagree, and that is informative

The v2 design (`sirna_design_v2.md`) optimised accessibility, strand asymmetry and
cross-species exclusivity. siDirect optimises the Ui-Tei rule, seed-duplex Tm and
genome-wide specificity. Their rankings **anti-correlate**:

| v2 pick | v2 composite | outcome under the siDirect screen |
|---|---|---|
| CDS1224 | 68.6 (best) | excluded by siDirect itself (Ui-Tei / seed Tm) |
| CDS1590 | 65.1 | fails: run of >=4 nt |
| CDS1032 | 59.6 | fails: off-target at 2 mismatches |
| CDS266 | 39.6 (2nd worst) | survives every filter |

Five of eleven v2 guides never entered the 206 at all. This is not an error in either
pipeline — a site can be highly accessible yet carry a stable seed duplex, or vice versa.

## Resolution — accessibility computed on the v2 scale

The 17 survivors were folded with the **identical** protocol used in v2 (NM_000902.5,
RNAplfold local partition function, W=240, L=160).

**Validation first:** the reimplementation reproduces all 11 published v2 accessibility
values exactly (max |difference| 0.0000, r = 1.0000), including the all-unpaired
probabilities to the exponent. The new numbers therefore sit on the existing scale.

**14 of 17 beat the v2 median (0.412). One beats the best v2 guide (0.608).**

### Recommended guide — position 2541 (NM_000902.5)

```
guide      5'-AAUGAUUGACUUGAUAGACCU-3'
passenger  5'-GUCUAUCAAGUCAAUCAUUUC-3'
```

| property | value |
|---|---|
| mean unpaired probability | **0.658** (best v2 guide: 0.608) |
| seed-region unpaired | 0.569 |
| seed-duplex Tm (guide) | 13.6 C — second lowest of the 17 |
| off-targets at 0 / 1 / 2 mismatches | 0 / 0 / 0 |
| minimum mismatches to any off-target | 3 |
| MME variants hit | 4 of 4 |
| GC | 33.3% |
| runs >=4 nt, immunostimulatory motifs | none |
| guide 5' / passenger 5' | A / G (correct loading asymmetry) |

It is more accessible than every guide in the v2 set **and** cleaner on specificity than
any of them — the combination neither pipeline alone could find. It was absent from the v2
shortlist because that search never considered it, and unremarkable to siDirect because
siDirect does not compute accessibility.

### Hedging

Accessibility and seed-region openness do not track together. Position 2541 has the best
whole-site accessibility but a mid-range seed (0.569); positions 2066 and 2403 have more
open seeds (0.73) with lower overall accessibility. Taking 2541 plus one of those gives two
candidates that fail differently.

## Limitation

Every number here is predicted. This ranking is a filter, not evidence. The decisive test
is a knockdown panel with qPCR on the top three plus a scrambled control; the ranking's
only job was to decide which three are worth the bench time.
