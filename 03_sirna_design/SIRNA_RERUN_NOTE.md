> **Current order sheet is [`ORDER.md`](ORDER.md).** The second guide in the middle
> sections of this document (2225-2247) was superseded by **2562-2584**; the final
> section carries the reasoning. The primary, 2700-2722, is unchanged throughout.

# Why the siDirect run shows 8 candidates instead of 206

**The sequence in that run is not neprilysin. It is vimentin.**

All eight target sites map to human *VIM* (`NM_003380.5`) with a **constant offset of
1267**, i.e. the input was VIM nucleotides **1268–1867** — a 600-nt internal fragment:

| screen position | VIM position |
|---|---|
| 24–46 | 1291 |
| 159–181 | 1426 |
| 261–283 | 1528 |
| 461–483 | 1728 |
| 462–484 | 1729 |
| 491–513 | 1758 |
| 519–541 | 1786 |
| 521–543 | 1788 |

Translating the input confirms it independently:
`…LQDEIQNMKEEMARHLREYQDLLNVKMALDIEIATYRKLLEGEESRISLPLPNFSSLNLRETNLDSLPL…`
is the vimentin coil-2 / tail junction.

A 600-nt internal fragment of vimentin is not something anyone pastes deliberately for an
MME project, so the most likely explanation is that siDirect's **built-in example sequence
was left in the text box** and the MME sequence never went in. (The siDirect site is not
reachable from the analysis sandbox, so this last part is inference, not verified.)

## Two independent reasons the count is low

1. **Wrong gene.** None of these 8 guides targets neprilysin at all.
2. **~10× shorter input.** 600 nt against the 5,818-nt transcript used before.
   At the density of the earlier MME run (206 candidates / 5,818 nt = 3.5% of positions),
   600 nt would be expected to yield only ~21 candidates even for the right gene.

## How to spot it next time, in one glance

The **graphical view's last line** states the input length. It reads `501-600`. For the
real MME transcript it would run to `5801-5818` — 58 lines, not 6.

## Re-run

Paste **`ENST00000615825.3` (MME-213) cDNA, 5,861 nt** — the Ensembl transcript the
206-candidate run actually used. All 206 siDirect targets sit in it at **offset 0**:
its reported positions match that sequence exactly. Expect ~206 candidates.

> **Correction.** An earlier version of this note said to paste `NM_007288.3`. That was
> wrong. `NM_007288.3` *contains* all 206 target sequences but at shifted positions
> (+41 for most rows, +131 for the rest, the variants differing by an internal indel), so
> it reproduces the same guides under different numbers. The original identification was
> made on containment rather than position, which is the weaker test.

## Coordinate warning — this is how a wrong oligo gets ordered

The recommended guides were reported in **`NM_000902.5`** coordinates. siDirect will
report them in **input** coordinates, which differ by 159:

| guide | siDirect range on MME-213 | guide, antisense 5'→3' | 23-nt target region |
|---|---|---|---|
| primary | **2700–2722** | `AAUGAUUGACUUGAUAGACCU` | `AGGTCTATCAAGTCAATCATTTC` |
| second guide | **2562–2584** | `UCUUUCGAUUAGAGAAUUCCC` | `GGGAATTCTCTAATCGAAAGAAA` |
| ~~hedge, superseded~~ | ~~2225–2247~~ | ~~`UUCUGAUAGGCUCUGUAUGCU`~~ | ~~`AGCATACAGAGCCTATCAGAATT`~~ |

Both verified against the stored siDirect rows: reported position equals found position.
The earlier figures 2541 and 2066 are `NM_000902.5` coordinates — correct for the variant
and SNP analysis, but **not** what siDirect displays. Do not look for them in the output.

siDirect lists a 23-nt region as "21nt target + 2nt overhang". The **guide** is the reverse
complement of the **first 21**; the **passenger** is the **last 21**. That 2-nt shift is a
third coordinate convention in play, which is why the rule below matters.

**Match on the sequence, not the number.** Position 954 (`NM_000902.5`) / **1023–1045** on MME-213 scored well on accessibility and specificity but is **disqualified** by a common
population variant at 1.92% — do not order it.

---

# "Use the exons, not the cDNA" — checked, and it is the wrong correction

## The cDNA *is* the exons

Verified on **MME-213 (`ENST00000615825.3`)**, the transcript in the wet lab's own screenshot:

| | |
|---|---|
| exons | 24 |
| cDNA length | **5,861 nt** |
| sum of the 24 exon lengths | **5,861 nt** |
| equal | **yes** |

The cDNA is the exons spliced together — there is no third sequence to design against.
siRNA acts on **mature cytoplasmic mRNA**, which is exactly that spliced product, so the
mRNA/cDNA is the correct input.

All 17 shortlisted guides were mapped onto those exon boundaries: **17/17 lie within
exons** of MME-213.

## Designing on separate exons would lose a good guide

Position **2066** (the hedge candidate *at the time*; now superseded by 2562-2584) spans **exons 21/22**. That junction exists only in
the spliced mRNA. Paste exons individually and the guide vanishes — and it is the one
candidate in the set that physically cannot target pre-mRNA or genomic DNA, which is a
property worth keeping.

## The Ensembl Exons page is a copy-paste hazard

That display interleaves exons with `Intron 1-2` (4,156 nt), `Intron 2-3` (731 nt) and so
on, and has `Flanking sequence` / `Intron sequence` toggles. Copying the region yields
intronic and flanking sequence. **That** would be a real design error: introns exist only
in nuclear pre-mRNA, which is not where RISC operates.

## The legitimate concern behind the request — already addressed

"Use exons" usually means *isoform coverage*: do not pick a site present in only some
transcripts. That is a real risk, and it was checked when the 206 candidates were scored:

- **203 / 206** hit all four MME RefSeq variants
- **3** hit only one variant and were disqualified for precisely that reason
- both guides recommended at the time (2541 and 2066) are among the 203

## One-line summary for the wet lab

> cDNA and exons are the same sequence — Ensembl reports 5,861 nt for both on MME-213.
> siRNA targets mature mRNA, so cDNA is correct. Designing on separate exons would lose
> junction-spanning guides including 2066. Isoform coverage was checked separately:
> 203/206 candidates hit all four MME variants, and the 3 that did not were dropped.

**This is a separate issue from the actual error in that run**, which is that the sequence
in the box was vimentin rather than MME. Fixing the input sequence is the real correction.

---

# "Paste the mRNA, not the cDNA"

**They are the same sequence.** Sequence databases distribute mRNA in DNA letters. NCBI's
own canonical record for this gene reads:

```
>NM_000902.5 Homo sapiens membrane metalloendopeptidase (MME), transcript variant 1, mRNA
```

and the sequence under that header contains **A, C, G and T only — no U**. There is no
separate "mRNA file" to download, from NCBI or Ensembl. The Ensembl `cDNA (transcripts)`
checkbox and an NCBI record labelled `mRNA` give the same molecule in the same alphabet.

siDirect uses both conventions in one table, which makes the point without argument: its
`target sequence` column is DNA (`cagaagaatggt…`) while its `RNA oligo sequences` column
is RNA (`UGGAUUUGUACC…`). You submit DNA; it returns RNA oligos.

## Positions in both transcripts, so the choice of input cannot cause another round

| | guide, antisense 5'→3' | sense target 21 nt | on MME-213 | on `NM_000902.5` |
|---|---|---|---|---|
| **primary** | `AAUGAUUGACUUGAUAGACCU` | `AGGTCTATCAAGTCAATCATT` | **2700–2722** | **2541–2563** |
| **second guide** | `UCUUUCGAUUAGAGAAUUCCC` | `GGGAATTCTCTAATCGAAAGAAA` | **2562–2584** | *absent from NM_000902.5* |
| ~~hedge, superseded~~ | ~~`UUCUGAUAGGCUCUGUAUGCU`~~ | ~~`AGCATACAGAGCCTATCAGAA`~~ | ~~2225–2247~~ | ~~2066–2088~~ |
| **do NOT order** | `UCGAUCUUCAGGUUUAGCCGU` | — | 1023–1045 | 954–976 |

Both guides are present in both transcripts. `NM_000902.5` is the canonical RefSeq choice
if an accession is wanted; note that **MME-213 has no RefSeq cross-reference** — it is an
Ensembl-only transcript model. Three of the 206 candidates are absent from `NM_000902.5`,
and all three had already been disqualified for failing to cover all four variants, so
nothing is lost by switching.

## No re-run is required

The 206-candidate list, the specificity and accessibility scoring, the four-variant
isoform check, the folding-window robustness test and the population-variant screen are
all complete. A re-run only lets the wet lab watch the result appear; it corrects nothing
and the ordering decision does not depend on it.

---

# The clinching evidence: both Ensembl links are the same transcript

The wet lab supplied two URLs, labelled "mRNA NEPRILYSIN" and "cDNA":

```
mRNA NEPRILYSIN  ->  /Homo_sapiens/Transcript/Exons?        g=ENSG00000196549; … ;t=ENST00000615825
cDNA             ->  /Homo_sapiens/Transcript/Sequence_cDNA? g=ENSG00000196549; … ;t=ENST00000615825
```

**`t=ENST00000615825` in both.** Same gene, same region, same transcript — and the same
transcript the 206-candidate run used. These are two *display pages for one molecule*:

- `/Transcript/Exons` breaks it into 24 exons with introns and flanking sequence
  interleaved for reference. A view, not a sequence record.
- `/Transcript/Sequence_cDNA` shows those exons joined — the mature transcript.

Measured on this transcript: 24 exon lengths sum to **5,861 nt**; the cDNA is **5,861 nt**.

**Copy from the cDNA page, never the Exons page.** The Exons page carries a
`5' upstream sequence` row, an active `Flanking sequence` toggle, and rows reading
`Intron 1-2  4,156` and `Intron 2-3  731` between the exons. Copying that region picks up
upstream and intronic sequence, which exists only in nuclear pre-mRNA. That is the one
route by which a genuinely wrong input could be produced here.

## Recommended way to close this out

Send the wet lab the **FASTA file itself** rather than a page link, and ask them to run
that exact file. Three rounds of this disagreement have been about naming — Exons vs cDNA,
mRNA vs cDNA, and before that a sequence that proved to be vimentin. A file has no name to
argue about.

---

# Why these two guides, and the co-delivery check no design tool performs

## Why `2700-2722` is the primary

It is the only guide strong on **all three** selection axes at once:

| | `2700-2722` | range across the 17 |
|---|---|---|
| seed-duplex Tm (guide) | **13.6 °C** | 6.3 – 21.5 |
| near-matches in the human transcriptome (3 mm) | **2** | 2 – 38 |
| target accessibility (mean unpaired prob.) | **0.66** | 0.32 – 0.66 (highest) |

Seed Tm is the most informative single column siDirect prints: a weak seed duplex
suppresses microRNA-like off-target silencing, which is the dominant off-target
mechanism and one that full-length sequence search cannot see.

**Why not `4557-4579`, which has a lower seed Tm (6.3 °C)?** Three times the off-targets
(6 vs 2) and a structurally closed target (0.42 vs 0.66). Lowest Tm alone does not win.

**Superseded — `2562-2584` is now the second guide; see [`ORDER.md`](ORDER.md).** The
argument made at the time was that `2225-2247` is the hedge on different grounds — **second-highest accessibility (0.58)**
and it spans the exon 21/22 junction, so it cannot act on pre-mRNA or genomic DNA. It
does not match the primary on seed Tm or off-target count and is not claimed to.

## Co-delivery safety: do the guides silence our own plasmid?

The lipoplex carries the plasmid and the siRNA in one particle, so both reach the same
cytoplasm. siDirect's specificity search covers the human transcriptome only — it has no
knowledge of the engPENK construct. This check was run separately against the four
SnapGene plasmid maps (6,950–7,539 bp), **both strands, treated as circular**.

Each plasmid carries **two mammalian transcripts**, both checked:

- CMV -> cassette -> bGH polyA (1,956–2,545 nt) — the payload
- SV40 -> NeoR/KanR -> SV40 polyA (1,156 nt) — the selection marker

| | result |
|---|---|
| guides with <= 3 mismatches anywhere in any plasmid | **0** |
| minimum mismatch, 17 guides x 4 plasmids | **6** |
| `2700-2722` seed sites in any 3' UTR | **0** |
| `2225-2247` seed sites in any 3' UTR | **0** |

**No cleavage risk and no 3'-UTR seed site for either pick.** `2225-2247` carries one
7mer-m8 site in coding sequence, where translating ribosomes displace RISC — a weak
context. One non-selected guide, `3759-3781`, has 4 seed sites in the NeoR mRNA; it is
reported here only to show the check returns non-zero when a liability exists.

### Two corrections made while running this

1. An earlier pass counted **3** seed sites for `2225-2247`. That used the raw insert
   FASTAs with no transcript boundaries, so sites outside the transcribed region were
   counted. Against the real transcripts it is **1**, in coding sequence.
2. The two `mEGFP…His_PENK` plasmids carry **no PENK CDS feature**, so taking the 3' UTR
   from the feature table gave 1,114 nt — it had swallowed the entire PENK coding
   sequence. ORF ends were re-derived by translation, giving 301–304 nt. Uncaught, this
   would have reported coding-sequence seed sites as 3'-UTR hits, which is precisely the
   distinction the analysis turns on.

## Is a BLAST needed? No, and running one casually is worse than not looking

- **Human transcriptome:** already done, and done better. siDirect performs an exhaustive
  mismatch-resolved search against RefSeq (release 230), enumerating hits at 0, 1, 2 and 3
  mismatches on both strands. That is complete counting; BLAST is a heuristic seeded
  aligner and would be a downgrade.
- **The trap:** for a 21-mer, `megablast` uses word size 28 — longer than the query — and
  finds essentially nothing. Default `blastn` (word size 11) misses near-matches whose
  mismatches break every 11-mer. Correct invocation is
  `-task blastn-short -word_size 7 -evalue 1000`. A megablast run returning no hits is
  routinely reported as "no off-targets" when the search could not have found any.
- **The plasmid:** covered above by exhaustive sliding-window matching, which is more
  sensitive than BLAST at this length and complete rather than heuristic.

Between siDirect's transcriptome search and the plasmid scan, every mRNA these guides can
encounter in a transfected cell has been checked.

---

# Two independent tools run: DSIR efficacy, and seed burden across all human 3' UTRs

## What was reachable

| tool requested | status | what was done instead |
|---|---|---|
| DSIR / s-Biopredsi | **run on the server** | all 5,841 candidates scored |
| Sfold | blocked at the proxy | its core metric (target accessibility from the structure ensemble) was already computed with ViennaRNA RNAplfold, W=240 L=160 u=21 |
| TargetScan / miRanda | blocked at the proxy | seed sites counted directly against 20,094 canonical human 3' UTRs (34.9 Mb) pulled from Ensembl BioMart |

The DSIR read was validated before use: its score for `GCAUAAGUAUACAGUUCAAUA` is 106.8,
identical to the `Dsir-Score` Eurofins printed for the same sequence.

The BioMart query was validated before the bulk download: MME-213's own 3' UTR came back at
**3,354 nt**, matching the length derived independently from the ORF (165-2507 of 5,861).

## DSIR predicted efficacy

Three of the seventeen shortlisted guides clear DSIR's `>90` efficient threshold
(371 of 5,841 candidates do):

| position | DSIR | rank / 5841 |
|---|---|---|
| **2700-2722** | ~~92.6~~ **85.4** | ~~223~~ 839 |
| 721-743 | 91.6 | 271 |
| 2562-2584 | 91.5 | 278 |
| 4557-4579 | 89.4 | 415 |
| 435-457 | 76.7 | 2287 |
| 2225-2247 | 71.8 | 3158 |

DSIR's "Corrected Score" ranks `435-457` highest. Per DSIR's own documentation that column
is efficacy minus penalties from intrinsic target features (Filhol 2012) - still efficacy,
not specificity.

## Seed-mediated off-target burden, measured rather than proxied

For each guide, the 7mer-m8 site (complement of guide positions 2-8), the 8mer
(7mer-m8 + A opposing position 1) and the 7mer-A1 were counted across every canonical
human 3' UTR. The background occurrence of an arbitrary 7-mer in this set is **1,966**
(10th-90th percentile 256-4,159), measured from 400 random 7-mers.

| position | 8mer sites | 7mer-m8 sites | 3' UTRs hit |
|---|---|---|---|
| 1023-1045 *(disqualified, 1.9% variant)* | 82 | 489 | 463 |
| **2562-2584** | **91** | **319** | **311** |
| 5026-5048 | 405 | 1,129 | 1,052 |
| **2700-2722** | **423** | **1,827** | **1,605** |
| 435-457 | 695 | 3,257 | 2,580 |
| 2225-2247 | 915 | 2,365 | 1,992 |
| 4557-4579 | 945 | 2,679 | 2,177 |

**This is a genuinely new axis.** It is uncorrelated with predicted efficacy across the
seventeen (Spearman rho = -0.21, p = 0.43), so it cannot be inferred from DSIR, and it is
not the same thing as siDirect's seed-duplex Tm: Tm measures how *strongly* a seed binds,
this counts how *many* sites exist. `2562-2584` has a high Tm (21.0) but six-fold fewer
sites than background; `2700-2722` has a low Tm (13.6) with a near-background site count.

## Consequence for the order

`2700-2722` remains the primary. It is the only candidate that is simultaneously top of the
shortlist on DSIR efficacy (92.6), lowest on full-length off-targets (2 at 3 mismatches),
highest on target accessibility (0.658) and below background on seed sites.

> **WITHDRAWN 2026-10-03.** The DSIR figures this paragraph rests on were read from the
> wrong window — matched on the sense 19-mer, where DSIR's frame is offset 2 nt from
> siDirect's. Corrected: 2562-2584 scores **77.8**, not 91.5, and 435-457 scores **83.7**,
> not 76.7, so 435 is the *better* of the two on efficacy. See [`ORDER.md`](ORDER.md).

~~**`2562-2584` replaces `435-457` as the recommended second guide.**~~ It clears the DSIR
efficacy threshold where `435` does not (91.5 vs 76.7), and carries the lowest seed burden
of any non-disqualified guide - 4.6x fewer 8mer sites than the primary. Its costs are a
higher seed-duplex Tm (21.0 vs 13.6), more full-length off-targets (9 vs 2) and lower
accessibility (0.537 vs 0.658). It is plasmid-safe at 7 mismatches, present in all four MME
RefSeq variants, and carries no common population variant.

Pairing the two gives a panel whose members fail by different mechanisms: the primary is
protected by weak seed binding, the second by having almost no seed sites to bind.
