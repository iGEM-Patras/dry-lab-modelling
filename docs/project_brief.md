# PENK Dry-Lab Modelling — Consolidated Project Brief

**iGEM Patras · Dry-Lab / Modelling**
Prepared as a consolidated audit and design record across four computational workstreams. All methods, force fields, databases, and design rules are traceable to the accompanying methods & references log.

---

## 0. Executive summary

This project supports an enkephalin-based analgesic strategy built on **proenkephalin (PENK)** expression plus a **neprilysin (NEP/MME) knockdown** arm, delivered by cationic/ionizable **lipoplexes**. The dry-lab work spans four independent but linked deliverables:

1. **Plasmid audit** of four PENK expression cassettes — identity, gene order, linker, and PENK ORF integrity verified against the native reference (UniProt P01210). **One real defect found** (plasmid 1, truncated PENK).
2. **Restriction-digest QC** — a two-tier digest scheme (insert release + identity fingerprint) with a virtual gel, designed to confirm construct identity before transfection.
3. **Human anti-NEP (MME) siRNA design** — four validated-in-silico siRNA duplexes targeting the CDS shared by all MME transcript variants, with off-target and thermodynamic scoring.
4. **Lipoplex CG-MD** — coarse-grained MARTINI simulations comparing three lipid formulations (permanent-cation DOTAP, protonated ionizable MC3-H⁺, neutral MC3⁰) across triplicate replicates, resolving the pH-dependent DNA-binding behaviour that motivates the ionizable-lipid choice.

**Scope note on the payload.** The four cassette plasmids carry the **native** human PENK sequence — they are the expression-system test-bed. The engineered anionic-address PENK (the therapy payload) is a separate construct: it currently exists as a **cloning-ready insert** (`engineered_PENK_GC-optimized.fasta` / `engPENK_insert_annotated.gb`), not yet assembled into an expression plasmid. It is audited here as the payload (§1) but is deliberately kept out of the four-plasmid restriction QC (§2) — see the note there.

---

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

## 3. Human anti-NEP (MME) siRNA design

**Rationale.** Neprilysin (NEP / CD10, gene **MME**) is the principal enkephalin-degrading peptidase. Silencing it prolongs the half-life of the enkephalins produced by the PENK construct — the knockdown arm of the therapy.

**Target.** All four human MME transcript variants (NM_000902.5, NM_007287/288/289) share an **identical 2,253 bp CDS**; every design targets that shared CDS, so a single siRNA silences all isoforms.

**Pipeline.** 2,084 candidate 19-mers enumerated across the CDS → **228** pass sequence rules (Reynolds + Ui-Tei: GC 30–52%, positional base preferences, no long homopolymer/GC runs) → ranked by thermodynamic duplex-end asymmetry (favouring guide-strand RISC loading) → off-target screened by NCBI blastn-short against human `refseq_rna`.

**Four recommended duplexes** (all 19/19 on-target, 0 off-targets ≥17/19; standard 3′ dTdT overhangs):

| # | CDS pos | Guide / antisense (5'→3') | GC% | ΔΔG | worst off-target |
|---|---------|---------------------------|-----|-----|------------------|
| si-MME-1 | 759 | UUCCUGACGAAUCAAUCUGdTdT | 42.1 | +1.31 | 16/19 |
| si-MME-2 | 1032 | UUCUGGAGCAUAAACAACCdTdT | 42.1 | +2.33 | 16/19 |
| si-MME-3 | 1224 | AUAGUUUGCACAACGUCUCdTdT | 42.1 | +0.98 | 14/19 |
| si-MME-4 | 1590 | UAUCCACUCAUCUUUGUCCdTdT | 42.1 | +1.93 | 16/19 |

Passenger strands, mRNA positions, and full scoring are in `sirna_design_table.csv`; the design figure is `sirna_design_figure.png`.

**Validation recommended:** qPCR of MME at 48 h (expect ≥70% knockdown for ≥2 duplexes) + NEP activity/CD10 Western; use ≥2 independent effective siRNAs to control for off-target phenotypes. A context-dependence caveat from the project bibliography is recorded — this design provides tool reagents, not a settled biological strategy.

---

## 4. Lipoplex coarse-grained MD

**Question.** Does the ionizable lipid's protonation state control DNA binding as the delivery design assumes — weak binding at physiological pH (neutral, for circulation), strong binding at endosomal pH (protonated, for cargo condensation)?

**Design.** MARTINI 2 CG-MD of a 60-bp CG B-DNA duplex with three lipid formulations, each cationic-lipid 120 : DOPE 80 : cholesterol 40 in ~24k CG waters, 150 mM NaCl:

- **DOTAP** — permanent +1 (control for constitutive binding)
- **MC3-H⁺** — ionizable MC3 surrogate, protonated (endosomal-pH state)
- **MC3⁰** — same lipid, neutral (physiological-pH state)

**3 independent velocity-seed replicates per formulation** (9 runs), analyzed with mean ± SEM.

### Stage 1 results (50 ns × 3 seeds)

| Formulation | DNA–lipid contacts | Min DNA–lipid dist (nm) | DNA Rg (nm) |
|-------------|-------------------:|------------------------:|------------:|
| DOTAP (permanent +) | 21.2 ± 6.1 | 0.462 ± 0.005 | 4.00 ± 0.15 |
| MC3-H⁺ (endosomal pH) | 32.5 ± 15.1 | 0.579 ± 0.126 | 4.34 ± 0.03 |
| MC3⁰ (physiological pH) | 9.6 ± 5.2 | 1.340 ± 0.874 | 4.24 ± 0.04 |

**The pH switch is reproduced qualitatively:** the protonated ionizable lipid binds DNA strongly; the neutral form does not reliably bind (one seed stayed 3.09 nm away with zero contacts); the permanent-cation control binds most reproducibly.

### Convergence — why the error bars are large, and why that matters

The between-seed spread is large **because binding is a stochastic nucleation event that has not finished in 50 ns**. The diagnostics make this explicit and honest:

- Cumulative-mean contact number is **still rising** at the end of most runs (first-half → second-half drift up to +200%).
- Within-replicate block-averaged standard error is **small** (0.7–4.2 contacts) — so the variability is *between-seed sampling*, not thermal noise.

This is the quantitative justification for the **200 ns production extension** now running (each replicate continued from its checkpoint). It is a genuine convergence requirement, not padding.

### Honest limitation (stated by design)

The DOTAP, MC3-H⁺ and MC3⁰ topologies are **MARTINI-2 analogy models** (built from DOPC/DUPC), **not** independently validated published parameters. Consequently all conclusions are **qualitative / comparative** — the relative ranking of DNA-condensing tendency across formulations and protonation states — **not** quantitative binding free energies. More sampling improves convergence but cannot fix a parameter-provenance limitation; this is disclosed rather than hidden.

Figure: `lipoplex_md_50ns.png` (RDF with replicate spread · contacts with individual seeds · closest approach · convergence). Per-replicate and summary metrics in `md_replicate_metrics_full.json` / `md_formulation_summary.json`.

---

## 5. What each deliverable establishes

| Workstream | Establishes | Actionable output |
|-----------|-------------|-------------------|
| Plasmid audit | Which construct to use (plasmid 3); which is defective (plasmid 1) | Use plasmid 3; Sanger-verify or discard plasmid 1 |
| Restriction QC | Identity/gene-order check before transfection | 2-digest protocol + virtual gel |
| siRNA design | Knockdown reagents for the NEP arm | 4 orderable duplexes + validation plan |
| Lipoplex CG-MD | pH-dependent DNA binding of the delivery vehicle | Formulation ranking + convergence-backed screen |

---

## 6. Reproducibility

Every tool version, force field, database accession, and published design rule is recorded in `methods_references.md`. The full analysis code, input topologies, protocols, and figures are versioned in the accompanying Git repository. The MD parameter-provenance caveat is stated in both the methods log and the results above.

*This brief covers the initial (50 ns) MD stage; the MD section will be refreshed with the 200 ns extended-run results when those runs complete.*
