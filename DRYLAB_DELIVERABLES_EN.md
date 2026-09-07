# Dry-Lab Deliverables — engineered PENK (iGEM Patras)

**For:** wet-lab team
**Date:** 2026-09-07
**Status:** everything below is a computational (dry-lab) result. Nothing has been measured
in-house.

---

## 0. The headline — the 7 cassettes are NOT broken

An external analysis told you the 7 cassettes are non-functional. **That is wrong**, and the
reason is specific: it applied the test *"is this native PENK?"*. The answer is no —
**deliberately**. That is the entire project.

The construct is not corrupted PENK. It is a **chimera of two natural opioid peptides**:

- The **message** segment `YGGF` is preserved intact from human PENK.
- The **address** segment `EVVG` comes from **deltorphin II**, a naturally occurring
  delta-selective amphibian skin peptide.

So both Met and Leu are replaced (native: 6x `YGGFM` + 1x `YGGFL`) by 7x `YGGFEVVG`. The mature
product is an **octapeptide (8 aa)**, not a pentapeptide.

### Why two cassettes "look" broken

Verified directly from `engPENK_insert_annotated.gb` (CDS translated, every flank enumerated):

| Cassette | aa | upstream | downstream | Verdict |
|---|---|---|---|---|
| 1 | 100 | KR | **KR**Y | dibasic — clean octapeptide |
| 2 | 110 | KR | **KK**M | dibasic — clean octapeptide |
| 3 | 142 | KR | **KK**D | dibasic — clean octapeptide |
| 4 | 195 | KR | RGL | monobasic — **extended, by design** |
| 5 | 222 | KR | **RR**V | dibasic, but **adrenorphin branch** — gives extended, not octapeptide |
| 6 | 245 | KR | **KR**F | dibasic — clean octapeptide |
| 7 | 279 | KR | RF* | monobasic — **extended, by design** |

All seven have **intact upstream KR**. Cassettes 4 and 7 carry monobasic downstream flanks — and
those are **exactly** the positions where native PENK deliberately makes *extended* peptides:
the octapeptide `YGGFMRGL` (MERGL) and the heptapeptide `YGGFMRF` (MERF). The construct
**reproduces native architecture**; it does not fail to be cleaved.

> **Predicted outcome: 4 clean octapeptides (`YGGFEVVG`, cassettes 1,2,3,6) + 3 extended
> species (cassettes 4, 5, 7).** NOT 7 identical peptides. If you see that pattern it is
> **success**, not partial failure.

Why cassette 5 gives an extended product despite a dibasic downstream flank (`RRV`): in native
PENK, core 5 does not release a pentapeptide — it enters the
**BAM-22 → BAM-20 → adrenorphin** route (`YGGFMRRV`-NH2). Engineered cassette 5 follows the
same route. See §3 for the four masses this produces.

*Formal record: the claim "cassettes 4 and 7 will not give clean product" was retracted by the
dry lab itself in `NATIVE_PENK_AMENDMENT2_WETLAB.md` §0.2.*

---

## 1. Deliverable: 4 plasmids, synthesis-ready

| Construct | bp | GC before | GC after | CAI before | CAI after | CAI loss |
|---|---|---|---|---|---|---|
| mEGFP-P2A-His-PENK | 1674 | 57.5% | 40.0% | 0.863 | 0.736 | −14.7% |
| His-PENK-P2A-mEGFP | 1671 | 51.6% | 40.0% | 0.767 | 0.733 | −4.4% |
| mEGFP-IRES-His-PENK | 2197 | 58.6% | 45.0% | 0.753 | 0.694 | −7.8% |
| His-PENK-IRES-mEGFP | — | 58.6% | 45.0% | 0.709 | 0.651 | −8.2% |

**Verified in all four:** protein **identical** in every cistron (no amino-acid change),
**7 copies** of `YGGFEVVG` present, **signal peptide untouched**, **Kozak untouched**, zero new
homopolymers >=6, zero AREs (`ATTTA`), zero cryptic polyA (`AATAAA`).

**The cost, stated honestly:** CAI drops. That is a real trade-off for reaching the synthesis GC
window; we are not hiding it.

**Why both P2A and IRES versions exist:** P2A leaves a ~21 aa remnant on the N-terminus of the
second peptide, and that junction is the strongest immunogenicity hotspot in the whole
construct — **not** the engineered epitope. The IRES pair is the alternative without that remnant.

---

## 2. Deliverable: HEK293T cannot do this on its own

This is the **most consequential** finding for experimental design.

| Enzyme | Role | HEK293 nTPM | Present? |
|---|---|---|---|
| **PCSK1** (PC1/3) | cleavage at dibasic sites | 0.1 | **NO** |
| **PCSK2** (PC2) | principal generator of small opioid peptides | 0.1 | **NO** |
| **SCG5** (7B2) | obligate PC2 chaperone | 0.0 | **NO** |
| CPE | trims C-terminal K/R | 73.7 | yes |
| PAM | alpha-amidation | 37.5 | yes |
| FURIN | constitutive convertase | 33.0 | yes |
| CTSL (cathepsin L) | alternative route | 35.5 | yes |
| PCSK1N (proSAAS) | **inhibitor** of PC1/3 | 55.3 | yes |

**Consequence:** in HEK293T, engPENK will accumulate as **unprocessed precursor**. No small
opioid peptides will form. And it is not only that the enzymes are missing — the **inhibitor**
proSAAS is present at high level.

**Therefore:** "Stage 2" (adding recombinant convertases in vitro) is **not a confirmatory step
— it is the entire experiment.** Skip it and there is no experiment.

**Two further protocol consequences:**
1. **siRNA knockdown** of the degrading peptidases is not testable here: MME 0.7 and ANPEP 0.1
   nTPM — **already absent**. There is nothing to knock down; a null result is uninformative.
2. In plasmid 3, mEGFP is **IRES-driven** and systematically under-reads PENK (IRES second-gene
   expression: 6–100% of cap-dependent, typically 20–50%). Do not use it as a quantitative
   PENK readout.

**Good news, specific to HEK293T:** PENK is 0.0 nTPM — there is **no endogenous PENK
background** in this line. Amendment 2's general warning ("any cell line with an intact PENK
locus secretes all of this before you transfect anything") holds in general, but HEK293T is the
favourable exception. Untransfected controls remain **mandatory** — they will most likely just
be clean.

---

## 3. Deliverable: MS target list — what to look for

| Species | Sequence | C-term | [M+H]+ | From |
|---|---|---|---|---|
| Engineered mature | `YGGFEVVG` | free acid | **827.39** | cassettes 1,2,3,6 (the four "clean") |
| Engineered amidated | `YGGFEVV`-NH2 | amide | 769.39 | after PAM |
| Engineered extended | `YGGFEVVGRGL` | free acid | **1153.60** | cassette 4 (RGL) |
| Engineered extended | `YGGFEVVGRF` | free acid | **1130.56** | cassette 7 (RF) |
| Native MERGL | `YGGFMRGL` | free acid | 900.44 | native core 4 |
| Native MERF | `YGGFMRF` | free acid | 877.40 | native core 7 |

### New finding — 4 species MISSING from the list

Cassette 5's downstream is `RRVG`, which in native PENK is the
**adrenorphin/metorphamide** branch and, upstream of it, BAM-20 / BAM-22. The list carried the
**native** species there but **none** of the engineered counterparts:

| Engineered species | Sequence | [M+H]+ | Native counterpart |
|---|---|---|---|
| adrenorphin counterpart | `YGGFEVVGRRV`-NH2 | **1237.68** | `YGGFMRRV`-NH2 (984.52) |
| pre-PAM intermediate | `YGGFEVVGRRVG` | 1295.69 | `YGGFMRRVG` |
| BAM-20 counterpart | `YGGFEVVGRRVGRPEWWMDYQKR` | 2871.43 | BAM-20 (2618.27) |
| BAM-22 counterpart | `YGGFEVVGRRVGRPEWWMDYQKRYG` | 3091.51 | BAM-22 (2838.35) |

**Why it matters:** if cassette 5 routes down the adrenorphin branch and nobody is watching
those m/z values, its product is **invisible**. You would report "only 4 of 7 cassettes gave
product" when in fact 5 did and one went unmonitored.

**Mass-collision warning:** the engineered BAM-20 counterpart (2871.43) sits **1.09 Da** from
native BAM-22 +2ox (2870.34). This needs resolving power >2600 or MS2 confirmation, or the two
will be read as **one** peak.

### Sample handling — not optional
- **Acquisition range 550–3100 Da** (the original instruction was 550–2900; extended for the
  new species).
- **Untransfected + empty-vector controls**, same line and passage, **every run**.
- **Include the +16 oxidation satellites** — otherwise Met peptides will appear "lost" when they
  have only oxidised. Quantify **parent + sulfoxide as one pool**.
- Collect on ice, acidify immediately (0.1% formic acid), avoid freeze-thaw.

---

## 4. Deliverable: a negative result — Cycle 3b (and why we report it)

We tested whether a physics-based method (MM-GBSA) can **predict** delta/mu selectivity, using
**4 known** control peptides — not the engineered one.

| Control | n | Computed ΔΔG | SEM | Experimental |
|---|---|---|---|---|
| met-enkephalin | 5 | +26.38 | 1.46 | 0.00 |
| deltorphin I | 5 | +15.18 | 4.95 | +5.70 |
| deltorphin II | 5 | +7.48 | 3.24 | +5.39 |
| endomorphin-1 | 5 | −0.91 | 3.32 | −2.99 |

- **G1 PASS** — direction and ranking are correct.
- **G2' FAIL** — only met-enkephalin clears the 1.5 kcal/mol SEM threshold; the others are 3.2–5.0.
- **G3 FAIL** — slope 0.594, 95% CI [−1.024, 2.213], r = 0.179. The CI spans zero.

**Verdict: FAIL. Stage 2 is not authorised.** Therefore **no computational claim about
`YGGFEVVG`'s selectivity is valid.** The only valid route is **radioligand competition binding**.

*We report this deliberately. The alternative — showing only the one control that passed —
would have sent you into an expensive assay on a method that cannot support it.*

---

## 5. What to do — in priority order

1. **NOW, before the plasmids arrive: order the custom anti-`YGGFEVVG` polyclonal.**
   KLH-conjugated, >=2 rabbits, **10–12 week** lead time. **No** commercial anti-enkephalin
   antibody recognises `YGGFEVVG` — all are raised against the native pentapeptide and most
   require the free C-terminal Met. **This is the bottleneck on the entire expression readout.**
   Confirm the immunogen is `YGGFEVVG` and not just the `YGGF` core.
2. **Synthesise the 4 constructs** from `PENK_order_sheet.csv`.
3. **Extend the MS list** with the 4 cassette-5 species (§3) and the range to 3100 Da.
4. **In vitro processing with recombinant enzymes** — not cells alone (§2).
5. **Radioligand binding** for `YGGFEVVG` and the `YGGFDIIG` variant (§4).

---

## 6. What remains OPEN — you should know

- The engineered extended species `YGGFEVVGRGL` and `YGGFEVVGRF` have **no published
  pharmacology**. They are novel, they are expected, and they should be **characterised** — not
  engineered away.
- `YGGFEVVG` is **less** stable than native Met-enkephalin, not more: 3 NEP-susceptible sites
  against 1. Deltorphin's stability comes from **D-Ala** at position 2, and D-amino acids
  **have no codon** — a ribosomally expressed peptide cannot reproduce it. We inherit the
  selectivity motif and **none** of the protease resistance. This is why the NEP-siRNA arm is
  **load-bearing**, not adjunct.
- **The cassette-5 table (§3) is my calculation** — not measured, and not reviewed by anyone else.

---

## References

All DOIs verified against CrossRef.

1. Comb M et al. (1982). Primary structure of the human Met- and Leu-enkephalin precursor and its mRNA. *Nature* 295:663-666. doi:10.1038/295663a0
2. Noda M et al. (1982). Cloning and sequence analysis of cDNA for bovine adrenal preproenkephalin. *Nature* 295:202-206. doi:10.1038/295202a0
3. Stern AS et al. (1979). Isolation of the opioid heptapeptide Met-enkephalin [Arg6,Phe7]. *PNAS* 76:6680-6683. doi:10.1073/pnas.76.12.6680
4. Kilpatrick DL et al. (1981). Identification of the octapeptide [Met]enkephalin-Arg6-Gly7-Leu8. *BBRC* 103:698-705. doi:10.1016/0006-291x(81)90506-4
5. Matsuo H et al. (1983). Novel C-terminally amidated opioid peptide in human phaeochromocytoma tumour. *Nature* 305:721-723. doi:10.1038/305721a0
6. Boarder MR et al. (1985). Metorphamide, a C-terminally amidated opioid peptide. *Regulatory Peptides* 12:75-83. doi:10.1016/0167-0115(85)90184-3
7. Paquet L et al. (1996). Peptide biosynthetic processing: distinguishing PC1 and PC2. *Mol Cell Endocrinol* 120:161-168. doi:10.1016/0303-7207(96)03834-8
8. Fricker LD, Snyder SH (1982). Enkephalin convertase: purification and characterization. *PNAS* 79:3886-3890. doi:10.1073/pnas.79.12.3886
9. Eipper BA et al. (1992). The biosynthesis of neuropeptides: peptide alpha-amidation. *Annu Rev Neurosci* 15:57-85. doi:10.1146/annurev.neuro.15.1.57
10. Roques BP et al. (1980). The enkephalinase inhibitor thiorphan shows antinociceptive activity in mice. *Nature* 288:286-288. doi:10.1038/288286a0
11. Erspamer V et al. (1989). Deltorphins: naturally occurring peptides with high affinity and selectivity for delta opioid binding sites. *PNAS* 86:5188-5192. doi:10.1073/pnas.86.13.5188
12. Chavkin C, Goldstein A (1981). Specific receptor for the opioid peptide dynorphin: structure-activity relationships. *PNAS* 78:6543-6547. doi:10.1073/pnas.78.10.6543

**Data sources:** UniProt P01210 (proenkephalin-A), UniProt P08473 (neprilysin/MME),
Human Protein Atlas cell-line RNA (nTPM, HEK293), GTEx v8.

**Repo files:** `04_plasmids/`, `07_invitro_penk/docs/PENK_INVITRO_PROTOCOL.md`,
`penk_ms_target_list.csv`, `06_engineering_cycles/cycle3b_physics_rescoring/docs/GATE_VERDICT_BOUND.md`,
`NATIVE_PENK_AMENDMENT2_WETLAB.md`, `dry_lab_modelling.md`
