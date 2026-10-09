# PENK Dry-Lab Modelling — Consolidated Project Brief

**iGEM Patras · Dry-Lab / Modelling**
Prepared as a consolidated audit and design record across four computational workstreams. All methods, force fields, databases, and design rules are traceable to the accompanying methods & references log.

---

## 0. Executive summary

This project supports an enkephalin-based analgesic strategy built on **proenkephalin (PENK)** expression plus a **neprilysin (NEP/MME) knockdown** arm, delivered by cationic/ionizable **lipoplexes**. The dry-lab work spans four independent but linked deliverables:

1. **Plasmid audit** of four PENK expression cassettes — identity, gene order, linker, and PENK ORF integrity verified against the native reference (UniProt P01210). **One real defect found** (plasmid 1, truncated PENK).
2. **Restriction-digest QC** — a two-tier digest scheme (insert release + identity fingerprint) with a virtual gel, designed to confirm construct identity before transfection.
3. **Human anti-NEP (MME) siRNA design** — a **human-exclusive** siRNA panel targeting the CDS shared by all MME transcript variants, with off-target, seed-divergence and thermodynamic scoring. The original four-duplex panel was **withdrawn**: it is cross-reactive with mouse *Mme* (one guide a perfect 19/19 match), which the wet lab's exclusivity requirement rules out (§3).
4. **Lipoplex CG-MD** — coarse-grained MARTINI simulations comparing three lipid formulations (permanent-cation DOTAP, protonated ionizable MC3-H⁺, neutral MC3⁰) across triplicate replicates, resolving the pH-dependent DNA-binding behaviour that motivates the ionizable-lipid choice.

**Two findings post-date the original four workstreams and change what should be ordered:**

- **No commercial antibody can detect the engineered product** (§2c). The construct recodes every enkephalin core to `YGGFEVVG`; all registry anti-enkephalin antibodies are raised against native `YGGFM` and will miss it. A custom anti-`YGGFEVVG` polyclonal must be raised, and it is on the critical path.
- **The original siRNA panel is mouse cross-reactive** (§3) and has been replaced by a human-exclusive panel. The corollary is that the exclusive guides cannot be validated in a mouse model, so a separate rodent surrogate is needed for any in-vivo work.

A fifth workstream was added after the first four: **payload engineering cycles** (§5b) — three pre-registered DBTL iterations attempting to bias the expressed peptide toward the δ opioid receptor. It returned a **negative result**, and is reported here in full because the negative result is load-bearing: it defines where the computational screen stops and the wet-lab assay must begin, and it forced the retraction of an earlier selectivity number. The final iteration (cycle 3b, physics rescoring) **completed on 2026-08-31 and also failed its calibration gate** — MM-GBSA gets the direction of δ/μ preference right but cannot resolve its magnitude at n=5 (§5b). All computational routes to ranking these designs are now exhausted; the recommendation to run radioligand competition binding on YGGFEVVG and YGGFDIIG is final rather than provisional.

**Scope note on the payload.** The four cassette plasmids carry the **native** human PENK sequence — they are the expression-system test-bed. The engineered anionic-address PENK (the therapy payload) is a separate construct: it currently exists as a **cloning-ready insert** (`engineered_PENK_GC-optimized.fasta` / `engPENK_insert_annotated.gb`), not yet assembled into an expression plasmid. It is audited here as the payload (§1) and kept out of the four-plasmid restriction QC (§2); §2b then assembles it into a therapy plasmid on the test-bed backbone with its own purpose-built QC.

---

**Lipoplex targeting (§4c, added 2026-08-12).** Of the receptor pairs proposed in the project
bibliography, `TfR + P2X3` is supported and `TfR + TRPV1` is not: P2X3 presents 70.3% of itself
extracellularly in one 279-residue loop against TRPV1's 6.7% across four short loops. P2X3's exposed
face is *more* conserved between human and rat (95.7%) than the protein average, so one reagent should
serve both model and human — unlike TfR itself at 75.3%. A registry-wide screen (103 P2X3 records) then found two reagents whose published immunogen sequence
could be verified directly against the ectodomain: **ABclonal A10232** (AB_2757757, immunogen aa 44–317,
essentially the whole ectodomain, listed rat, human 95.6% identical there) and **Atlas HPA057776**
(AB_2683526, aa 184–260, listed human, rat 92.2%). These supersede the earlier lead on epitope evidence —
PA5-77682's immunogen remains undisclosed, so its epitope is vendor-asserted rather than verified.
Neither new reagent is validated for live-cell binding, so the binding gate stands.

The reagent shortlist excludes the field's
most-cited P2X3 antibody (Alomone APR-016): its epitope maps to aa 383–397, the cytoplasmic tail.
No marketed P2X3 antibody is validated for live-cell surface binding, so a binding test gates all
formulation work.

## 1. Plasmid audit — four PENK cassettes

All four plasmids are pcDNA3.1(+)-type backbones carrying native human PENK and mEGFP, differing in **gene order** (which gene is cap-driven / first) and **linker** (EMCV IRES vs self-cleaving P2A).

| # | Plasmid | Size (bp) | Architecture | PENK identity | Cores | Verdict |
|---|---------|-----------|--------------|---------------|-------|---------|
| 1 | mEGFP-IRES-PENK | 7,500 | CMV → mEGFP (cap) → IRES → PENK | **TRUNCATED (263 aa)** | 6 of 7 | **DEFECT** |
| 2 | mEGFP-P2A-PENK | 6,971 | CMV → mEGFP–P2A–PENK (single ORF) | full length (266 aa) | 7 | OK, caveat |
| 3 | PENK-IRES-mEGFP | 7,512 | CMV → PENK (cap) → IRES → mEGFP | full length (267 aa) | 7 | **OK — cleanest** |
| 4 | PENK-P2A-mEGFP | 6,971 | CMV → PENK–P2A–mEGFP (single ORF) | full length (267 aa) | 7 | OK |
| — | **engineered PENK (payload)** | 885 (insert) | NheI–Kozak–ATG–CDS–XhoI (cloning-ready insert) | **engineered** (288 aa) | **7 of 7** | OK — payload |

**Key findings**

- **Plasmid 3 (PENK-IRES-mEGFP) is the cleanest construct**: PENK is cap-dependent with an intact signal peptide (MARFLTLC…), byte-identical to the UniProt P01210 reference.
- **Plasmid 1 has a genuine defect**: a premature stop truncates the C-terminal **YGGFMRF** (the 7th enkephalin core), leaving 6 of 7 cores. This is a point-level lesion — **it will not change any restriction-gel band** and can only be caught by Sanger sequencing of the PENK 3′ end.
- **Plasmid 2 caveat**: PENK is downstream of P2A, so its N-terminus becomes P-ARFLTLC (loses initiator Met, gains a P2A-derived proline) — this may impair signal-peptide function and secretion. For a secreted peptide product, the secreted gene should be placed **first** (as in plasmids 3 and 4).

- **Engineered payload (therapy construct)**: the anionic-address PENK, in which all seven enkephalin cores are recoded YGGF[M/L] → **YGGFEVVG**. Verified from `engineered_PENK_GC-optimized.fasta`: 867 nt CDS → 288 aa, Met start, single clean stop, **7 of 7 engineered cores, 0 native cores**, GC 59.9%, no homopolymers, cores made synonymously distinct, and single flanking NheI/XhoI sites with **no internal cut sites** (cloning-clean for pcDNA3.1(+)). This is the construct that gives the therapy its function; it is **not yet in a backbone**, so it appears in the audit but not in the four-plasmid gel QC.

Full per-feature detail is in `plasmid_feature_audit.csv`.

---

## 2. Restriction-digest QC protocol

A two-tier scheme confirms both **linker type** and **gene order**, and is designed so a single defect (mis-assembly) is caught before transfection.

**Digest A — insert release (AflII + XbaI).** Releases a constant **5,345 bp backbone** band (loading / complete-digestion control) plus one insert band whose size reports the linker: **~2.16 kb = IRES**, **~1.63 kb = P2A**. Limitation: cannot distinguish the two IRES plasmids (12 bp apart) or the two P2A plasmids — gene order requires Digest B.

**Digest B — identity fingerprint (NcoI, 5 cuts).** A unique 5-band pattern per plasmid. Shared 3,342 + 735 bp landmarks; the **second-largest band is diagnostic** for gene order (1,648/1,446 doublet vs 2,416 vs 2,749 vs 2,226 bp).

**Critical limitation flagged in the protocol:** passing the gel QC does **not** clear plasmid 1 — the PENK truncation is invisible on a gel and must be confirmed by **Sanger sequencing**.

The virtual gel (`restriction_qc_gel.png`) shows both digests side-by-side against a 1 kb-plus ladder; the full bench recipe and interpretation logic are in `restriction_qc_protocol.md`.

**Applies to the four native plasmids only.** This scheme is native-PENK-specific: the engineered payload insert has **no AflII and no XbaI site** (it is cloned via NheI/XhoI), so it cannot be screened by Digest A and does not share a lane with the four plasmids. Once the engineered PENK is cloned into an expression backbone, that construct will need its **own restriction map** computed fresh.

---

## 2b. Engineered PENK therapy plasmid — in silico build + QC

The four native plasmids are the **test-bed**; the **engineered PENK is the intended therapeutic construct**. To make it a plasmid rather than a linear fragment, the engineered insert (NheI–Kozak–CDS–XhoI, 885 bp) was cloned in silico into the **pcDNA3.1(+)** backbone shared by the test-bed vectors.

**Assembly.** Backbone donor = plasmid 4 (PENK-P2A-mEGFP), chosen for its **single** NheI and **single** XhoI sites (a clean directional swap). The native P2A–mEGFP cassette (1,639 bp, NheI→XhoI) was excised and replaced by the engineered insert, giving a **6,217 bp circular plasmid**. Verified: single NheI + single XhoI, engineered CDS present exactly once (288 aa, **all 7 YGGFEVVG cores**), native cassette removed. Promoter (CMV), polyA (bGH), and selection (NeoR/AmpR) are held identical to the test-bed, so the therapy construct stays parallel to the validated expression system.

**Purpose-built QC.** The native Digest A/B scheme does not transfer — the engineered plasmid has **no AflII site**, and its only XbaI site is in the backbone. Five diagnostic digests replace it:

| Digest | Enzyme(s) | Expected bands (bp) | Purpose |
|---|---|---|---|
| A — insert release | NheI + XhoI | **5,338 + 879** | insert present & correct size |
| B — linearize | NheI | 6,217 | total size |
| C — identity | BglII | 5,144 + 1,073 | empty vector loses the 1,073 band |
| D — fingerprint | NcoI | 3,342 + 1,845 + 735 + 295 | rearrangement check |
| E — fingerprint | PstI | 4,117 + 1,544 + 447 + 109 | independent fingerprint |

The virtual gel (`engPENK_therapy_qc_gel.png`) shows all five digests vs a 1 kb-plus ladder; the protocol and bench recipe are in `engPENK_therapy_qc_protocol.md`, and the annotated plasmid is `engPENK_therapy_plasmid.gb`.

**Status.** In silico design. After bench cloning, Sanger sequencing across the CDS is mandatory — the seven cores are synonymously distinct by design and a gel cannot verify them (the engineered analogue of the gel-invisible plasmid-1 truncation).

---

## 2c. Detection reagents — no commercial antibody can see this construct's product

**This is the most wet-lab-actionable finding in the project and it has a procurement lead
time, so it is stated before the results that depend on it.**

The engineered therapy construct (§2b) recodes all seven enkephalin cores
`YGGF[M/L]` → **`YGGFEVVG`**. Verified from `engPENK_insert_annotated.gb` (885 nt, CDS 13..879,
288 aa ORF): **7 identical copies of `YGGFEVVG`, zero copies of `YGGFM` or `YGGFL`.** Native
human PENK (P01210) carries 6× `YGGFM` + 1× `YGGFL`.

Every anti-enkephalin antibody in the Antibody Registry is raised against the *native mature
pentapeptide*, so none of them can detect the engineered product:

| RRID | antibody | immunogen / epitope | verdict |
|---|---|---|---|
| AB_2530349 | anti-Met-enkephalin mAb 1194/334 | `YGGFM` pentapeptide | **will not detect** |
| AB_2492947 | anti-Met-enkephalin pAb | PENK aa 237–241 (= `YGGFM`) | **will not detect** |
| AB_3430419 | anti-Met-enkephalin | Met-enkephalin | **will not detect** |
| — | precursor-directed anti-PENK | PENK backbone | detects precursor only; **cannot show maturation** |
| — | **custom anti-`YGGFEVVG`–KLH** | the engineered octapeptide | **required — must be custom-raised** |

The shared `YGGF` N-terminal core is not sufficient rescue: anti-Met-enkephalin antibodies are
raised against the whole pentapeptide and typically require the free C-terminal Met, a residue
that does not exist in the product.

**Action.** Place the custom anti-`YGGFEVVG` polyclonal order now — it is on the critical path
for every expression and maturation readout, and a custom polyclonal is a multi-week lead item.
A precursor-directed anti-PENK is a useful companion (it confirms the protein is made) but
cannot distinguish precursor from processed octapeptide, which is precisely the question the
construct is designed to answer.

Full assessment, including the targeting-ligand analysis from `LIPOPLEX(1).docx`, is in
`antibody_assessment.md` / `.pdf`; the per-antibody verdict table is
`penk_epitope_check.csv`.

---

## 3. Human anti-NEP (MME) siRNA design

**Rationale.** Neprilysin (NEP / CD10, gene **MME**) is the principal enkephalin-degrading peptidase. Silencing it prolongs the half-life of the enkephalins produced by the PENK construct — the knockdown arm of the therapy.

**Target.** All four human MME transcript variants (NM_000902.5, NM_007287/288/289) share an **identical 2,253 bp CDS**; every design targets that shared CDS, so a single siRNA silences all isoforms.

> ### Superseded — the original panel is cross-reactive with mouse
>
> An earlier version of this section recommended four duplexes (`si-MME-1` … `si-MME-4`)
> selected on human on-target identity, thermodynamic asymmetry and human off-target load.
> They satisfy those criteria. They do **not** satisfy the wet lab's later-stated requirement
> that the siRNA be **exclusively human, with no mouse cross-reactivity**, and that constraint
> was not part of the original screen:
>
> | superseded | CDS pos | identity vs mouse *Mme* (NM_008604.4) | status |
> |---|---|---|---|
> | si-MME-1 | 759  | 18/19 | cross-reactive |
> | si-MME-2 | 1032 | 17/19 | cross-reactive |
> | si-MME-3 | 1224 | 16/19 | cross-reactive |
> | si-MME-4 | 1590 | **19/19 — perfect match** | fully cross-reactive |
>
> Across the full original panel, 8 of 11 guides retain ≥17/19 in mouse and two (CDS1590,
> CDS1616) are perfect mouse matches. **Do not order these.** They are retained here only so
> the record shows which reagents were withdrawn and why.

**Re-screen under the exclusivity constraint.** Rescreening the whole human CDS (751 codons,
2,253 nt) gives 307 composition- and asymmetry-filtered 19-mers, of which **26 fall to ≤15/19
against mouse *Mme***. Those were ranked on seed divergence (guide positions 2–8, where a
mismatch most reliably abolishes activity), human off-target burden (BLASTn vs human
`refseq_rna`, word size 7), duplex-end asymmetry, and GC content.

**Human-exclusive panel — order these instead:**

| rank | CDS pos | Guide / antisense (5'→3') | GC% | mouse | seed MM | human off-targets ≥17/19 | composite |
|---|---|---|---|---|---|---|---|
| **1** | 303 | `AAAGUUGCCGUAACGGGAGdTdT` | 52.6 | 14/19 | 2 (pos 4,7) | **0** | 85.8 |
| 2 | 1307 | `UCCUCGACCACAUGUUUACdTdT` | 47.4 | 14/19 | 2 (pos 3,6) | 4 | 74.3 |
| 3 | 2101 | `UGGAGUUAACCGCAUACUCdTdT` | 47.4 | 15/19 | 3 (pos 2,5,8) | **0** | 61.6 |
| 4 | 412 | `UACAAGACCUGUACAAUGCdTdT` | 42.1 | 15/19 | 2 (pos 5,8) | 1 | 57.8 |
| 5 | 635 | `UGAAUUACAUGAUUCACAGdTdT` | 31.6 | 14/19 | 3 (pos 6,7,8) | 84 | 54.5 |

**Recommended lead: CDS303** — guide `AAAGUUGCCGUAACGGGAGdTdT`, passenger
`CUCCCGUUACGGCAACUUUdTdT`. 19/19 on human *MME*, 14/19 on mouse with two mismatches inside the
seed, zero human off-targets at ≥17/19, and ΔΔG = 4.20 kcal/mol favouring correct guide-strand
loading. **CDS2101** is the best three-seed-mismatch alternative and also carries zero ≥17/19
off-targets. Order both plus a scrambled control.

**Consequence — this must be said to the wet lab explicitly.** Exclusivity is a two-edged
requirement. Guides selected *not* to hit mouse *Mme* **cannot be tested in a mouse model**.
Knockdown validation has to be done in human cells, and any in-vivo rodent efficacy work needs a
separate, mouse-targeting surrogate siRNA designed and validated alongside it. Budget for two
reagent sets, not one.

Full scoring for both panels is in `sirna_human_exclusive_panel.csv` (new) and
`sirna_human_exclusivity.csv` (cross-reactivity audit of the superseded panel).

**Validation recommended:** qPCR of MME at 48 h (expect ≥70% knockdown for ≥2 duplexes) + NEP activity/CD10 Western; use ≥2 independent effective siRNAs to control for off-target phenotypes. A context-dependence caveat from the project bibliography is recorded — this design provides tool reagents, not a settled biological strategy.

---


## 4. Lipoplex coarse-grained MD

**Question.** Does the ionizable lipid's protonation state control DNA binding as the delivery design assumes — weak binding at physiological pH (neutral, for circulation), strong binding at endosomal pH (protonated, for cargo condensation)?

**Design.** MARTINI 2 CG-MD of a 60-bp CG B-DNA duplex with three lipid formulations, each cationic-lipid 120 : DOPE 80 : cholesterol 40 in ~24k CG waters, 150 mM NaCl:

- **DOTAP** — permanent +1 (control for constitutive binding)
- **MC3-H⁺** — ionizable MC3 surrogate, protonated (endosomal-pH state)
- **MC3⁰** — same lipid, neutral (physiological-pH state)

**3 independent velocity-seed replicates per formulation** (9 runs), analyzed with mean ± SEM.

### Final results (200 ns × 3 seeds)

All 9 replicates were extended from 50 ns to **200 ns** (each continued from its checkpoint); metrics use the equilibrated second half (100–200 ns).

| Formulation | DNA–lipid contacts | Min DNA–lipid dist (nm) | RDF peak g(r) | DNA Rg (nm) |
|-------------|-------------------:|------------------------:|--------------:|------------:|
| DOTAP (permanent +) | 24.7 ± 5.5 | 0.460 ± 0.003 | 1.54 ± 0.12 | 4.10 ± 0.13 |
| MC3-H⁺ (endosomal pH) | 34.4 ± 8.6 | 0.469 ± 0.013 | 1.57 ± 0.31 | 4.24 ± 0.07 |
| MC3⁰ (physiological pH) | 8.1 ± 4.9 | 1.270 ± 0.563 | 1.04 ± 0.09 | 4.18 ± 0.002 |

**The pH switch is reproduced, and the extension confirms it robustly.** At endosomal pH the protonated ionizable lipid (MC3-H⁺) binds DNA as tightly as the permanent-cation control DOTAP — both reach ~0.47 nm closest approach — condensing and protecting the cargo. At physiological pH the neutral form (MC3⁰) holds DNA ~1.3 nm away, with an RDF peak at the bulk value (~1.0) and one seed that never binds (0.08 contacts, 2.36 nm) — the release/circulation state.

### Convergence — the extension did its job

At 50 ns the between-seed spread was large **because binding is a stochastic nucleation event that had not finished** (cumulative-mean contacts still rising, first-half → second-half drift up to +200%, while within-replicate block error stayed small at 0.7–4.2 contacts — i.e. between-seed sampling, not thermal noise). The 200 ns extension resolved this:

- **MC3-H⁺ error bars collapsed** — contacts SEM 15.1 → 8.6, min-distance SEM 0.126 → 0.013 nm (≈10× tighter). The short run had caught nucleation mid-transient; the long run confirms genuine strong binding.
- **DOTAP** stayed strong and tightened further (contacts SEM 6.1 → 5.5) — constitutive binding, as expected for a non-titratable lipid.
- **MC3⁰** stayed weak throughout — the intended physiological-pH control.

Cumulative-mean contacts plateau by ~100 ns for all formulations, so the 100–200 ns analysis window is equilibrated. This was a genuine convergence requirement, not padding.

### Honest limitation (stated by design)

The DOTAP, MC3-H⁺ and MC3⁰ topologies are **MARTINI-2 analogy models** (built from DOPC/DUPC), **not** independently validated published parameters. Consequently all conclusions are **qualitative / comparative** — the relative ranking of DNA-condensing tendency across formulations and protonation states — **not** quantitative binding free energies. More sampling improves convergence but cannot fix a parameter-provenance limitation; this is disclosed rather than hidden.

Figure: `lipoplex_md_200ns.png` (RDF with replicate spread · contacts with individual seeds · closest approach · convergence). Per-replicate and summary metrics in `md_formulation_summary_200ns.json`; full 50→200 ns convergence tables in `04_lipoplex_md/RESULTS_200ns.md`. The Stage-1 50 ns figure/metrics are retained (`lipoplex_md_50ns.png`, `md_formulation_summary.json`) for provenance.

---

## 4b. Therapeutic delivery rationale — putting the two arms together

The four workstreams are not independent analyses; they are components of one system whose therapeutic logic is **endogenous opioid enhancement**: *make more enkephalin, degrade less of it, at the pain relay.*

**Mechanism.** The PENK construct produces proenkephalin, which is processed to enkephalins — endogenous opioid peptides acting on δ- (and μ-) opioid receptors to produce opioid-like analgesia without an exogenous opioid. Neprilysin (NEP / MME / CD10) is the principal enkephalin-degrading ectopeptidase, inactivating enkephalins in the synaptic space within seconds. Silencing NEP prolongs enkephalin action — the knockdown arm. The two arms are synergistic.

**Where the siRNA goes — co-formulation, not just co-expression.** NEP acts as a cell-surface ectoenzyme and enkephalin is degraded *extracellularly*, but siRNA silencing is **cell-autonomous** — it only affects the cells actually transfected. Secreted enkephalin then diffuses past the surfaces of many neighboring cells, and NEP on any of them will degrade it. Silencing NEP only in the enkephalin-producing cell is therefore insufficient. The design consequence: **co-formulate the NEP siRNA and the PENK plasmid in the same lipoplex, delivered to the same locus**, so the population of enkephalin-producing cells overlaps maximally with the population of NEP-silenced cells. This is precisely why the lipoplex CG-MD (§4) is load-bearing — the lipoplex is the vehicle that carries both nucleic acids into the same region, and the siRNA off-target screen (§3) is part of that same package.

**Where in the CNS.** Lipoplexes do not cross the blood–brain barrier, so delivery is local/regional to the analgesic circuit — principally **intranasal (nose-to-brain) delivery** *(superseded in this brief: earlier text said spinal dorsal horn / intrathecal)*, the first nociceptive synapse and rich in δ/μ opioid receptors; supraspinal targets (PAG, RVM) are alternatives. There is clinical precedent for the enkephalin-gene-therapy-for-pain concept (an HSV proenkephalin vector reached trials for cancer pain); the additions here are the NEP-knockdown arm and a non-viral lipoplex vehicle.

The two-arm concept and its dorsal-horn mechanism are shown in `therapy_delivery_schematic.png`.

**Honest caveats.** (i) The cell-autonomy mismatch is the central design risk — co-formulation plus local delivery mitigates but does not erase it. (ii) NEP has other substrates (substance P, bradykinin, natriuretic peptides, amyloid-β); broad chronic knockdown could impair Aβ clearance, so the knockdown is kept **local and transient** by using siRNA/lipoplex rather than a permanent vector. (iii) Sustained opioid tone raises tolerance/dependence considerations. (iv) siRNA and non-integrating plasmid expression are transient — adequate for proof-of-concept, but a chronic indication would want a durable vector.

---

## 4c. Lipoplex surface targeting — which receptor, which antibody

**Added 2026-08-12.** The project bibliography («Antibodies on the lipoplex») proposed two-level
targeting: a blood–brain-barrier handle plus a nociceptor handle, with `TfR + P2X3` and
`TfR + TRPV1` as the two candidate pairs. TfR and TRPV1 were already assessed
(`antibody_assessment.md`); **P2X3, NaV1.7, NaV1.8, TRPA1 and INSR had never been assessed.**
This section closes that gap.

**Method.** For each target, reviewed UniProt entries for human/rat/mouse were resolved by
`gene_exact` + `organism_id` — not by recalled accession; three recalled accessions were wrong and
were caught by a length check before use. Two quantities were computed: the fraction of the protein
annotated as extracellular (what an antibody can reach on an intact cell), and cross-species identity
computed twice — over the whole protein and over the concatenated extracellular segments only.
The **difference** between those two is the informative number, because a reagent is raised against
the ectodomain, not the average protein.

| Target | Role | % extracellular | Largest loop (aa) | Identity, full (h/rat) | Identity, **ectodomain** | Δ | Tier |
|---|---|---|---|---|---|---|---|
| TfR / TFRC | BBB crossing | 88.4% | 672 | 76.7% | 75.3% | −1.3 | B |
| INSR | BBB crossing | 66.9% | 731 | 94.4% | **95.5%** | +1.0 | **A** |
| **P2X3** | nociceptor | **70.3%** | **279** | 94.0% | **95.7%** | **+1.7** | **A** |
| NaV1.7 / SCN9A | nociceptor | 16.9% | 79 | 93.1% | 90.0% | −3.1 | C |
| NaV1.8 / SCN10A | nociceptor | 14.2% | 69 | 83.2% | 65.6% | −17.6 | C |
| TRPV1 | nociceptor | 6.7% | 32 | 85.8% | 53.4% | −32.4 | D |
| TRPA1 | nociceptor | 4.8% | 28 | 79.7% | 60.7% | −18.9 | D |

Tiers: **A** ectodomain >50% and >90% conserved · **B** large ectodomain, species-restricted ·
**C** limited surface · **D** not a viable antibody surface.

**Result: `TfR + P2X3` is well founded; `TfR + TRPV1` is not.** P2X3 presents 70.3% of its mass
extracellularly in a single contiguous 279-residue loop. TRPV1 presents 6.7% across four loops whose
largest is 32 aa — a tenfold difference in available surface, independently confirming the existing
assessment's rejection of TRPV1 as a surface handle.

**The conservation result runs the other way for P2X3.** Every failing target is *less* conserved on
its exposed face than overall (TRPV1 loses 32 points, TRPA1 19, NaV1.8 18). P2X3's ectodomain is
*more* conserved (95.7%) than the whole protein (94.0%), so an anti-P2X3 reagent validated in rat
should transfer to human. Note the contrast with **TfR at 75.3%**, which is precisely why anti-TfR
clones are species-specific and non-interchangeable (§ shortlist, `antibody_assessment.md`). On this
axis the nociceptor half of the pair is better behaved than the BBB half. **INSR** is a credible
second BBB handle (66.9%, 95.5%) that does not inherit TfR's species restriction.

### Reagent shortlist — and a reagent that must not be used

The methods sections of 99 open-access P2X3 antibody papers were mined for cited RRIDs, each resolved
against the Antibody Registry. Five genuine anti-P2X3 reagents were found. Every vendor epitope was
checked against the P2X3 sequence; the ectodomain is **aa 44–322** of 397.

| Clone | RRID | Reacts | Verdict |
|---|---|---|---|
| **PA5-77682** | AB_2736292 | mouse, rat | **Lead** — only reagent explicitly raised against the extracellular domain |
| APR-016 | AB_2313760 | h/m/r | **Do not use for targeting** — epitope is cytoplasmic |
| PA5-115707 | AB_2900342 | h/m/r | Backup — epitope undisclosed |
| RA10109 | AB_2157931 | not stated | Caution — flow listed, whole antiserum, epitope undisclosed |
| H68.4 | AB_2533029 | h/m/r + | Detection only — binds TfR cytoplasmic tail |

> ### The most-cited P2X3 antibody cannot bind an intact cell
> **Alomone APR-016** is the field's most-used P2X3 antibody. Its vendor epitope
> `(C)VEKQSTDSGAYSIGH` was located in the sequence at **aa 383–397** — the C-terminal
> **cytoplasmic** tail, outside the 44–322 ectodomain. It cannot bind a live cell and is unusable as
> a targeting ligand, however many papers cite it; those papers use it for western blot and
> permeabilized IHC, which is valid. Separately, the listed peptide is the **rat** sequence — human
> P2X3 reads `AEKQSTDSGAFSIGH` at those positions (13/15 identical).

### Honest limitation — this application is unprecedented

PubMed: 283 papers on P2X3 as a nociceptor marker and 52 on clinical antagonists (the gefapixant
programme), but only **9** touching live-cell surface antibody work and **13** any nanoparticle
targeting. A further 97 open-access surface/live-cell papers were screened for any P2X3 catalogue
number used in an unpermeabilized context: **zero hits.** The biology is established and the topology
is favourable, but **P2X3 has never been used as a nanoparticle-targeting ligand.** That is a novelty
claim requiring validation, not a citable precedent. TfR, by contrast, carries 324 brain-delivery
papers.

Consequences, carried into the wet-lab handout: request immunogen sequences from the vendor for both
PA5 reagents before ordering (neither discloses one); the first experiment is a live-cell binding
test on unpermeabilized cells with a viability gate, with a permeabilized control in parallel so that
a negative is still informative; formulation work follows only after that gate passes. Also note P2X3
is not exclusively neuronal — bladder urothelium and airway expression is the mechanism behind
gefapixant's cough indication and taste side-effects, so a particle reaching systemic circulation has
off-target tissue. And as the bibliography already notes, a nociceptor marker is not the same thing as
a central pain compartment; whether P2X3+ peripheral terminals suit this delivery route is a separate
question this analysis does not address.

*Deliverables: `LIPOPLEX_TARGETING.md`, `lipoplex_targeting_assessment.csv`,
`antibody_shortlist_p2x3.csv`, `lipoplex_wetlab_handout.pdf`.*

## 5. What each deliverable establishes

| Workstream | Establishes | Actionable output |
|-----------|-------------|-------------------|
| Plasmid audit | Which construct to use (plasmid 3); which is defective (plasmid 1) | Use plasmid 3; Sanger-verify or discard plasmid 1 |
| Restriction QC | Identity/gene-order check before transfection | 2-digest protocol + virtual gel |
| siRNA design | Knockdown reagents for the NEP arm, **human-exclusive** | 2 orderable duplexes (CDS303, CDS2101) + scrambled control; separate rodent surrogate needed |
| Detection reagents | That **no commercial antibody detects the engineered product** | Custom anti-`YGGFEVVG`–KLH polyclonal — order now, long lead |
| Lipoplex CG-MD | pH-dependent DNA binding of the delivery vehicle | Formulation ranking + convergence-backed screen |
| Peptide engineering cycles | That δ-selectivity **cannot** be resolved by co-fold confidence at the effect sizes our designs produce | Shortlist of 2 payloads for radioligand binding |

---

## 5b. Payload engineering cycles — δ-selectivity (three DBTL iterations)

Native Met-enkephalin (`YGGFM`) is only weakly δ-preferring, and δ (DOR/`OPRD1`) agonism
carries **much lower respiratory-depression and dependence liability** than μ
(MOR/`OPRM1`). Biasing the payload δ-ward is therefore a safety-driven design goal, and it
was pursued over three pre-registered Design→Build→Test→Learn cycles. Predictions were
committed and pushed to git **before** each run, so the falsification record is auditable.

| Cycle | Question | Outcome |
|---|---|---|
| **1** | Does grafting the deltorphin II address onto the enkephalin message bias δ? | Directionally δ-ward; **quantitative claim withdrawn** (see correction below) |
| **2** | Can address hydrophobicity / an anionic residue improve it? | **Primary hypothesis falsified** — 4 of 5 predictions wrong |
| **3a** | Is pose convergence a better-powered selectivity proxy than ipTM? | **Hypothesis rejected** — does not replicate on held-out samples |

**Cumulative track record: 10 predictions, 4 confirmed, 6 falsified.**

### A retracted number, and why it is reported here

Cycle 1 originally reported the engineered payload as **1.96× more δ-preferring** than
native. **That figure is withdrawn.** It was computed from the single top-ranked diffusion
sample. Recomputed across all samples, the engineered payload's δ-preference is
+0.0114 ± 0.0131 — indistinguishable from zero (p = 0.43) and from native (p = 0.60). Root
cause: the engineered μ complex has ~3× the sample spread of any other complex, and the
top-ranked model happened to land near that distribution's floor, so the apparent
selectivity was largely one unlucky sample. A process change followed: **every metric in
this project is now a mean ± SD over all samples, never a single model.**

### Final state of the screen

Across 7 peptides × 2 receptors at 20 diffusion samples each (280 structures), **no design
achieves meaningful δ-selectivity**: every Δ_sel ≤ 0.007 with SEM ≈ 0.004, and the two
leading payloads — `YGGFEVVG` (the built construct) and `YGGFDIIG` — are statistically
tied. The only result reaching significance points the *wrong* way (`YGGFELLG` prefers μ,
p = 0.008), reproducing a consistent finding that added aliphatic bulk in the address
biases μ-ward on our Gly-Gly backbone — opposite to the published deltorphin literature,
which measured those substitutions on a D-Ala² backbone we cannot encode in DNA.

**The honest conclusion is that the in-silico screen has reached its resolution limit.**
Boltz-2 ipTM is a structural-confidence score, not binding affinity, and it cannot resolve
δ/μ preference at the magnitude these designs produce. The screen's real deliverable is a
**shortlist of two payloads for radioligand competition binding at OPRD1/OPRM1**, which
remains the only real test.

### Constraint that shaped every design

The payload is **expressed from a plasmid**, so it must be DNA-encodable: 20 standard
L-amino acids only. This excludes the classic high-selectivity opioid-peptide chemistry
(D-amino acids, penicillamine cyclisation, N-methylation), which is why the design space
was the address-domain *sequence*. One exception is exploited deliberately — a C-terminal
Gly is the recognition signal for **peptidylglycine α-amidating monooxygenase (PAM)**, so a
`...VVG` payload can be amidated to `...VV-NH₂` *in vivo*; the terminal Gly in every design
is load-bearing.

![δ vs μ co-folds](figures/cycle2_selectivity.png)

### Cycle 3b — physics rescoring (COMPLETE — negative result, 2026-08-31)

Because the co-fold confidence score cannot resolve δ/μ preference at the magnitude these
designs produce, cycle 3b replaced it with a physics-based readout: explicit-solvent membrane
MD of each peptide–receptor complex followed by MM-GBSA interaction energetics.

**Outcome: the Stage-1 calibration gate FAILED. Stage 2 was never authorised, and per the
pre-registration cycle 3b terminates as a negative methodological result.** The project
recommendation is unchanged: radioligand competition binding on YGGFEVVG and YGGFDIIG.

The gate ran on the complete panel — 4 control peptides × 2 receptors × 5 replicates = 40
production runs, all scored:

| control | computed ΔΔG (μ−δ) | SEM | experimental | 
|---|---:|---:|---:|
| met-enkephalin (non-selective) | +26.38 | 1.46 | 0.00 |
| deltorphin I (δ-selective) | +15.18 | 4.95 | +5.70 |
| deltorphin II (δ-selective) | +7.48 | 3.24 | +5.39 |
| endomorphin-1 (μ-selective) | −0.91 | 3.32 | −2.99 |

- **G1 PASS** — every sign and ranking check holds. The method gets the *direction* right:
  both deltorphins δ-preferring, endomorphin-1 μ-preferring, deltorphins ranked above
  endomorphin-1.
- **G2′ FAIL** — only met-enkephalin (SEM 1.46) falls under the 1.5 kcal/mol threshold;
  the others are 3.2–5.0.
- **G3 FAIL** — computed-vs-experimental slope 0.594, 95% CI [−1.024, 2.213], r = 0.179.
  The CI spans zero, so the correlation is not distinguishable from none.

**Reading.** The failure is replicate scatter, not a broken pipeline: per-replicate ΔΔG within
a single control spans 27 kcal/mol for deltorphin I. Met-enkephalin is the informative case —
it has the *tightest* replicate agreement and is also the *most wrong* (+26.4 computed vs 0.0
experimental). A reproducible large error is a systematic one, consistent with these being
enthalpy-dominated effective energies with no entropy term; met-enkephalin is the smallest and
most flexible of the four, so the missing configurational-entropy penalty should hit it hardest.

**Method amendment, disclosed.** Nine of the 40 runs were initially refused by a membrane-
proximity gate — the peptide had left the pocket and contacted the bilayer, where a
non-membrane implicit-solvent model is invalid. Implicit-membrane GB is not available
(`memopt`/`mthick` are `&pb`-only), and rescoring those arms in PB would place them on a
different energy scale from the other 31. Instead **all 40 runs were recomputed** on a single
conditional bound-state frame definition (frames with ligand–lipid distance > 0.4 nm AND
ligand RMSD to docked pose ≤ 0.52 nm). Recomputing all 40 rather than splicing in 9 was
deliberate: the two frame definitions are different quantities and must not be pooled. Where
both exist, they agree to a median 1.04 kcal/mol — inside MM-GBSA's own uncertainty.

**Mandatory caveat when quoting any single value.** A bound-state ΔG describes how tight the
pose is *while it exists*, not how strong binding is. Three runs have residency < 50%
(deltorphin II at μ: 10.7%, 13.6%). The merge tooling refuses to emit a ΔG without its
residency fraction.

**Residency is itself a reportable observable** and does not depend on the failed energy model:
deltorphin II holds the δ pocket in 82–100% of frames but the μ pocket in as little as 10.7%.
That is the right direction for a δ-selective peptide, and it is measured rather than modelled.

Five build-time defects were found and gated during Stage 1, each of which would have produced
a clean-looking but meaningless result:

| defect | why the existing checks missed it | gate installed |
|---|---|---|
| receptor mis-embedded in the bilayer (tilt up to 29.4°) | the embedding tool exits 0 while leaving the protein tilted | tilt measured from receptor Cα inertia; hard-fail > 10° |
| **wrong stereoisomer built** — D-Ala² inversion silently skipped | parametrisation reported 0 errors; an all-L analog is chemically valid, just not the intended molecule | chirality asserted post-build; per-tag chemistry read from the design table, never defaulted |
| interface clashes < 2.1 Å surviving minimisation | minimiser reports whole-system energy over ~155k atoms; one bad contact is inside its noise | interface contact measured directly, before and after minimisation |
| a panel-wide mis-orientation, not a one-off | only one system had been examined | pre-flight sweep across all six poses, as a mode of the production build |
| **energy parser returned the ligand's absolute energy, not ΔG** | the wrong value (−123 kcal/mol) is physically plausible and passed the range check | parser anchored on the Δ-block header and cross-checked against the component sum |

A sixth defect was caught during the bound-state recomputation: GROMACS `trjconv -fr` takes
**1-based** frame indices, so 0-based selection scored the frame *before* each intended one —
silently, with a plausible result. It was caught only because the membrane check had been
repurposed from filter to *verification*: frame selection guarantees zero lipid contact, the
re-measurement found 15%, and the run refused itself. Had that check been deleted as redundant
once it stopped filtering, the wrong numbers would have shipped.

Full state, thresholds, defect log, and the terminal verdict are in
`06_engineering_cycles/cycle3b_physics_rescoring/` (`GATE_VERDICT_BOUND.md`,
`bound_results_with_residency.csv`, `bound_gate_summary.png`).

Full per-cycle pre-registrations, results, and prediction scorecards are in
`06_engineering_cycles/`.

---

## 6. Reproducibility

Every tool version, force field, database accession, and published design rule is recorded in `methods_references.md`. The full analysis code, input topologies, protocols, and figures are versioned in the accompanying Git repository. The MD parameter-provenance caveat is stated in both the methods log and the results above.

*This brief reports the final 200 ns MD results (all 9 replicates converged).*

**Revision, 2026-08-12.** This edition supersedes the 2026-07-31 brief. Change: **§4c added** —
lipoplex surface-targeting assessment (P2X3, NaV1.7, NaV1.8, TRPA1, INSR, none previously assessed),
resolving the bibliography's `TfR + P2X3` vs `TfR + TRPV1` proposals in favour of the former, with a
reagent shortlist that excludes the field's most-cited P2X3 antibody on epitope-location grounds.
All other sections unchanged.

**Revision, 2026-07-31.** That edition superseded the 2026-07-24 brief. Changes: §2c added
(no commercial antibody detects the engineered product — custom reagent required); §3 siRNA
panel replaced after the original four duplexes were found cross-reactive with mouse *Mme*;
§5b extended with cycle 3b physics-rescoring status and its four gated build defects. The
plasmid audit (§1, §2, §2b) and lipoplex MD (§4) results are unchanged.

*Update on the peptide–receptor co-folds: these **did** complete. An earlier version of this
brief recorded them as blocked by a cluster disk-quota limit during MSA generation; that
was resolved, and the root cause of the subsequent GPU memory failures turned out to be the
prediction tool auto-loading an uncapped MSA rather than a hard hardware limit. All four
μ/δ × native/engineered complexes were produced at matched full MSA depth (1024 sequences),
then extended to a 7-peptide panel at 20 diffusion samples each (§5b). Structures and
confidence files are in `06_engineering_cycles/*/data/`.*
