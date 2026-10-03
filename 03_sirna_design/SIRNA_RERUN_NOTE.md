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
| hedge | **2225–2247** | `UUCUGAUAGGCUCUGUAUGCU` | `AGCATACAGAGCCTATCAGAATT` |

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

Position **2066** (hedge candidate) spans **exons 21/22**. That junction exists only in
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
- both recommendations (2541 and 2066) are among the 203

## One-line summary for the wet lab

> cDNA and exons are the same sequence — Ensembl reports 5,861 nt for both on MME-213.
> siRNA targets mature mRNA, so cDNA is correct. Designing on separate exons would lose
> junction-spanning guides including 2066. Isoform coverage was checked separately:
> 203/206 candidates hit all four MME variants, and the 3 that did not were dropped.

**This is a separate issue from the actual error in that run**, which is that the sequence
in the box was vimentin rather than MME. Fixing the input sequence is the real correction.
