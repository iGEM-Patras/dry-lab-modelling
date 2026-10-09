# Where engPENK actually gets cut, and what the Nissl-body lumen does to it

Analysis of `engPENK_insert_annotated.gb` (288 aa proprotein) against native human PENK
(P01210). All numbers below are computed from the sequences, not quoted.

## The short answer: the Nissl body is not where it gets cut

"Nissl bodies" are stacks of rough ER plus free polyribosomes in the neuronal soma, the
basophilic granules are rRNA. That is the **synthesis and folding** compartment, and the
proprotein leaves it intact. Cleavage of the cassettes happens two compartments later.

| Compartment | pH | What happens to engPENK there |
|---|---|---|
| RER lumen (Nissl body) | 7.2 | signal peptide 1–24 removed by signal peptidase; disulfides formed; N-glycans transferred. **Cassettes untouched.** |
| cis/medial Golgi | 6.7 | glycan maturation. Cassettes untouched. |
| trans-Golgi network | 6.0 | PC1/3 becomes active; first dibasic cuts begin; sorting into immature granules |
| immature granule | 5.5 | PC2 (with 7B2) active; CPE trims basic residues; PAM active |
| mature granule | 5.1 | processing completes; peptides stored |

The reason is mechanistic, not incidental: the prohormone convertases that cut KR/KK sites are
themselves pro-enzymes in the ER. PC2 requires its 7B2 chaperone and an acidic, high-Ca²⁺ lumen
to remove its own propeptide, which does not happen until the TGN. So the ER lumen contains the
substrate and the enzymes, but the enzymes are not yet competent. **This is what the construct
needs**, seven tandem cassettes have to survive transit as one chain and be released only in
the granule.

## What the Nissl-body lumen *does* do to it

- **Signal peptide:** residues 1–24, removed co-translationally. Mature chain 264 aa.
- **Disulfides:** 1 Cys in the signal peptide, **6 in the mature chain → 3 disulfides**,
  same count as native. Formed here by PDI in the oxidizing ER; the cassettes contain no Cys,
  so the insertions cannot scramble the native pairing.
- **N-glycosylation:** two sequons, at N133 (NGS) and N161 (NSS). Both are the
  **native** sequons (N127/N152 in P01210), displaced only by the upstream cassette insertions.
  No new glycosylation liability was introduced.

## The charge shift is the real ER-side consequence

Each cassette replaces a Met-containing native core with `YGGFEVVG`, so the mature chain carries
41 Glu against 34 in native (and 5 Met against 11). Net charge at every compartment pH:

| Compartment | pH | engPENK | native PENK | Δ |
|---|---|---|---|---|
| RER (Nissl) | 7.2 | -15.4 | -8.4 | -7.0 |
| cis-Golgi | 6.7 | -14.6 | -7.6 | -7.0 |
| TGN | 6.0 | -12.9 | -6.0 | -6.9 |
| immature granule | 5.5 | -10.9 | -4.1 | -6.7 |
| mature granule | 5.1 | -7.9 | -1.5 | -6.4 |

Sorting into dense-core granules is driven by pH- and Ca²⁺-dependent self-aggregation in the TGN.
An extra 7 e of negative charge could plausibly go either way, more carboxylates to bridge with
Ca²⁺, or higher solubility that resists condensation. **This is a prediction, not a result**, and
it is measurable: compare secreted vs. cell-associated peptide, and check for constitutive
(unregulated) release, against a native-PENK control in the same cell line.

## The finding that changes the peptide identity

The cassette ends in **Gly**. Native PENK cores end in Met or Leu (6× YGGFM, 1× YGGFL) and are
therefore **not** PAM substrates. PAM (active in the same granules, pH ~5.5–6, Cu²⁺/ascorbate)
consumes a C-terminal Gly and amidates the residue before it. So in the granule:

```
YGGFEVVG  --PAM-->  YGGFEVV-NH2     (769.3879 [M+H]+)   a 7-mer, amide on Val
```

That is **not** the deltorphin-II-like species the docking and MD work scored. Deltorphin II is
`Y-a-F-E-V-V-G-NH2`, amide on Gly. To get the Gly-amide, the cassette would need a **second
Gly**: `YGGFEVVGG`.

Three species are therefore possible from the current construct:

| Species | [M+H]⁺ | Note |
|---|---|---|
| `YGGFEVVG` free acid | 827.3934 | what was docked/scored |
| `YGGFEVVG-NH2` | 826.4094 | requires the extra Gly in the cassette |
| `YGGFEVV-NH2` | 769.3879 | what PAM gives from the cassette as built |

**What to measure, and where the 0.98 Da actually bites.** Within a single construct the two
products are **58.01 Da apart**, so the amidation readout is unambiguous on any instrument:

| Construct | unamidated free acid | PAM product | separation |
|---|---|---|---|
| **as built** (`YGGFEVVG`) | 827.3934 | 769.3879 (`YGGFEVV-NH₂`) | 58.01 Da |
| **fixed** (`YGGFEVVGG`) | 884.4148 | 826.4094 (`YGGFEVVG-NH₂`, deltorphin-II geometry) | 58.01 Da |

The near-isobaric pair is **827.3934** (as-built free acid) vs **826.4094** (fixed-construct
amide): 0.98 Da apart, with the amide's ¹³C₁ peak 0.0193 Da (23 ppm) from the acid's
monoisotopic peak, needing **R ≈ 42,784 FWHM** to separate. Those two never coexist in one
construct, so this matters in exactly two situations:

1. **QC of a vendor synthetic standard**: free acid vs amide differ by 0.98 Da. If the vendor
   silently ships the amide (a common default), low-resolution MS will not catch it.
2. **Running as-built and fixed-construct supernatants in the same batch**: do not co-inject
   without high resolution.

## Two cassettes will not give a clean product

Every cassette has a dibasic KR upstream. Downstream differs:

| Cassette | downstream flank | product |
|---|---|---|
| 1, 2, 3, 5, 6 | KR / KK / RR | `YGGFEVVG` |
| 4 | R-G-L-K (monobasic) | `YGGFEVVGRGL` |
| 7 | R-F, C-terminal | `YGGFEVVGRF` |

Cassettes 4 and 7 sit at the native positions of the extended peptides (met-enkephalin-Arg-Gly-Leu
and -Arg-Phe), and they inherit those flanks. CPE removes the Arg but not Gly-Leu or Phe, so ~2/7
of the yield is C-terminally extended and pharmacologically distinct.

## What to do

1. **Decide the intended C-terminus.** If the deltorphin-II amide is the goal, the cassette must be
   `YGGFEVVGG`, a single codon insertion, cheap now, expensive after cloning.
2. **Fix cassettes 4 and 7** by giving them their own dibasic downstream flank if uniform product
   is wanted.
3. **Measure, don't assume, the C-terminus**: high-resolution MS/MS on granule-derived peptide;
   0.98 Da is the whole question.
4. The ER-side chemistry (signal cleavage, 3 disulfides, 2 native sequons) is unchanged from
   native. Nothing in the Nissl body needs redesign.
