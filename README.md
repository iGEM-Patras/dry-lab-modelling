# PENK Dry-Lab Modelling

Computational audit and design work supporting an enkephalin-based analgesic strategy: **proenkephalin (PENK)** expression combined with a **neprilysin (NEP / MME)** knockdown arm, delivered by cationic / ionizable **lipoplexes**.

**[`METHODS_GUIDE.md`](METHODS_GUIDE.md)** explains how each computational method works, why it
was chosen, how to read its output, and where it fails — written for a reader who can program
but has no chemistry or bioinformatics background. **[`GLOSSARY.md`](GLOSSARY.md)** defines the
terminology used across the repository.

The full narrative — rationale, results, and honest limitations — is in **[`docs/project_brief.pdf`](docs/project_brief.pdf)**. Every tool version, force field, database accession, and published design rule is recorded in **[`methods_references.md`](methods_references.md)**.

## Workstreams

| Dir | Workstream | What it establishes |
|-----|-----------|---------------------|
| [`01_plasmid_audit/`](01_plasmid_audit/) | Audit of four PENK expression cassettes | Which construct to use (plasmid 3); which is defective (plasmid 1, truncated PENK) |
| [`02_restriction_qc/`](02_restriction_qc/) | Restriction-digest QC design + virtual gel | 2-digest scheme to confirm identity / gene order before transfection |
| [`03_sirna_design/`](03_sirna_design/) | Human anti-NEP (MME) siRNA design | 2 orderable human-exclusive duplexes with off-target + thermodynamic scoring |
| [`04_lipoplex_md/`](04_lipoplex_md/) | Lipoplex coarse-grained MD | pH-dependent DNA binding of the delivery vehicle across 3 formulations |
| [`05_presentation/`](05_presentation/) | Slides + wet-lab handouts | Bench-facing summaries of the above |
| [`06_engineering_cycles/`](06_engineering_cycles/) | Payload engineering (3 pre-registered DBTL cycles) | A **negative result**: no computational route ranks these designs; the wet-lab assay is required |
| [`07_invitro_penk/`](07_invitro_penk/) | Cell-free processing assay design | The cassette swap is predicted **neutral for convertases, adverse for cathepsin L** — a falsifiable bench test |
| [`08_checkable_audit/`](08_checkable_audit/) | Independent audit of the wet-lab guide | 17 findings (5 critical) against the Greek bench guide, each with a reference |
| [`09_codon_gc_design/`](09_codon_gc_design/) | GC recoding for synthesis | All four constructs at target GC, protein untouched — with the CAI cost stated |
| [`10_immunogenicity_antibody/`](10_immunogenicity_antibody/) | MHC-I prediction + antibody detectability | Engineered epitope ≈ native immunogenicity; **P2A junction is the worst of the three** |
| [`11_wetlab_protocols/`](11_wetlab_protocols/) | Amendments 1–5 (EN + GR) | Dry-lab findings translated into bench actions |
| [`99_provenance/`](99_provenance/) | Plans, resume briefs, as-received inputs | Traceability from request to result |

## Key results at a glance

- **Plasmid 3 (PENK-IRES-mEGFP) is the cleanest construct** — PENK cap-driven, intact signal peptide, byte-identical to UniProt P01210. **Plasmid 1 has a genuine defect** (truncated 7th enkephalin core) invisible on a gel — Sanger-verify or discard.
- **Two human-exclusive anti-MME siRNAs** (CDS303, CDS2101) target the CDS shared by all MME transcript variants. The **original four-duplex panel was withdrawn**: it is cross-reactive with mouse *Mme* (one guide a perfect 19/19 match). The corollary is that the exclusive guides cannot be validated in a mouse model — a separate rodent surrogate is needed for in-vivo work.
- **No commercial antibody detects the engineered product.** The construct recodes every enkephalin core to `YGGFEVVG`; registry anti-enkephalin antibodies are raised against native `YGGFM`. A custom anti-`YGGFEVVG` polyclonal must be raised and is on the critical path.
- **Lipoplex MD reproduces the ionizable-lipid pH switch** (200 ns × 3 seeds, mean ± SEM): protonated MC3-H⁺ binds DNA as tightly as permanent-cation DOTAP (~0.47 nm closest approach); neutral MC3⁰ holds DNA ~1.3 nm away with an RDF peak at the bulk value. Contacts plateau by ~100 ns, so the 100–200 ns analysis window is equilibrated.
- **The two processing routes are affected unequally by the cassette swap.** PC1/3 and PC2 cut C-terminal to the dibasic; cathepsin L/V cut N-terminal to it. The swap leaves the convertase scissile context identical at all 7 cassettes but moves the cathepsin P2 residue from Phe (7/7 within the preferred Leu/Trp/Phe/Tyr set) to Val (0/7). Separately, 5 of 7 engineered cassettes are Gly-extended PAM substrates where no native cassette is. Both are directly testable in the cell-free assay in `07_invitro_penk/`.
- **Payload δ-selectivity: three methods failed, two later passed calibration.** Cycles 1–3b returned negatives — 3b's MM-GBSA rescoring got the *direction* right but failed its magnitude gate at n=5. Cycles 7 and 9 then succeeded by calibrating against published reference opioids first: the co-folding affinity head cleared a pre-set correlation gate at n=13 (r = 0.805, p = 0.0009, signs correct 12/13), and the pose-convergence metric that Cycle 3a retired was rehabilitated in Cycle 9 (ρ = 1.000 against four peptides with published selectivity). **Current calibrated estimate for `YGGFEVVG`: +1.23 ± 1.76 kcal/mol δ-over-μ (~7×) — nominally δ-preferring but not statistically separable from native Met-enkephalin.** A rigorous free-energy (TI) campaign is running to settle the magnitude. Radioligand competition binding remains the recommended wet-lab arbiter.

- **The four ordered constructs now sit at synthesis-friendly GC** (40 % for the P2A pair, 45 % for the IRES pair) with **every cistron's protein byte-identical** to before. The cost is codon adaptation (CAI 0.65–0.74) — a real trade, not a free lunch, and one a transfection settles faster than more modelling. Order sheet: [`09_codon_gc_design/PENK_order_sheet.csv`](09_codon_gc_design/PENK_order_sheet.csv).
- **The engineered epitope is not more immunogenic than the native one it replaces** (1.86 % vs 1.77 % strong MHC-I binders across 6,120 allele-peptide pairs). The **P2A remnant junction ranks highest of the three groups** (2.07 %) — an argument for the IRES cassettes if immunogenicity of a persistently expressed product matters. See [`10_immunogenicity_antibody/`](10_immunogenicity_antibody/).
- **HEK293T cannot process proenkephalin to small opioid peptides.** PCSK1, PCSK2 and SCG5 (7B2) are all effectively absent (nTPM ≤ 0.1); CPE and PCSK1N are present. The competence claim must be made against HEK293T — the cells actually used — not against fibroblasts. Table: [`08_checkable_audit/tables/hek293t_processing_competence.csv`](08_checkable_audit/tables/hek293t_processing_competence.csv).
- **The wet-lab guide's engineering-cycle numbering does not map onto the dry-lab cycles.** Six guide cycles vs four repo cycles, reconciled in [`06_engineering_cycles/cycle_reconciliation.csv`](06_engineering_cycles/cycle_reconciliation.csv) — guide Cycle 3 *is* a dry-lab cycle but belongs to the lipoplex workstream, not `06_`.

## Status

*Last reviewed 2026-09-19. Individual cycle documents are the authority on their own status —
check `git log -1 --format=%ad -- <file>` before trusting any date here.*

Workstreams `01`–`05` and `08`–`11` are **complete**. Cycle 3b terminated on 2026-08-31 per its
pre-registration; see [`06_engineering_cycles/cycle3b_physics_rescoring/docs/GATE_VERDICT_BOUND.md`](06_engineering_cycles/cycle3b_physics_rescoring/docs/GATE_VERDICT_BOUND.md)
for the terminal verdict.

**Work has continued since, in five further cycles:**

| Cycle | Status |
|---|---|
| **4** — synthesis manufacturability | ✅ **closed.** v4 rejected by the vendor (inverted-repeat flanks inherited from wet-lab files); diagnosed and repaired; **v6 accepted, all four constructs ordered** |
| **5** — expression & processing | 📋 pre-registered, awaiting the wet lab's first transfection |
| **7** — affinity-head calibration | ✅ **gate passed** at n=13 (r = 0.805). First calibrated δ/μ number for `YGGFEVVG` |
| **8** — free-energy (TI) campaign | 🔄 **running.** 13 CPU workers; the graft shortcut was rejected by measurement and is written up |
| **9** — convergence metric, recalibrated | ✅ **gate passed** (ρ = 1.000). The metric Cycle 3a retired, rehabilitated with proper calibration |

The open questions are now **mostly** wet-lab questions — the exception being Cycle 8, whose
free-energy result is the one remaining computational deliverable.

**What the wet lab should do next**, in order of what unblocks the most: (1) order the four
recoded constructs from `09_codon_gc_design/PENK_order_sheet.csv`; (2) commission the custom
anti-`YGGFEVVG` polyclonal — nothing downstream can be detected without it; (3) run the
cell-free processing assay in `07_invitro_penk/`, which is where HEK293T's missing convertases
stop being a modelling caveat and start being a measurement; (4) radioligand competition
binding on `YGGFEVVG` and `YGGFDIIG`, since cycle 3b established no computational route ranks
them. Amendments 1–5 in `11_wetlab_protocols/` state each of these as a bench-actionable change.

`07_invitro_penk/` is the first of those wet-lab questions worked up into a benchtop design. It is a **design, not a result**: no experimental data exists yet.

## Licence and citation

Documentation, data, figures and protocols are released under **[CC BY 4.0](LICENSE)**;
source code under the **[MIT Licence](LICENSE-CODE)**. Cite this repository using
[`CITATION.cff`](CITATION.cff). Contribution conventions — in particular the requirement
that predictions are committed before the tests that could falsify them — are in
[`CONTRIBUTING.md`](CONTRIBUTING.md).

## Reproducibility

Coarse-grained MD used **GROMACS 2024.5** with the **MARTINI 2** force field. All-atom membrane MD and MM-GBSA rescoring (cycle 3b) used **GROMACS 2024.5** + **AmberTools**. Sequence work used **Biopython**; siRNA off-target screening used **NCBI BLAST+ (blastn-short)** against human `refseq_rna`. See `methods_references.md` for the complete list with citations. MD input files (`.mdp`, topology) and analysis scripts are under `04_lipoplex_md/` and `06_engineering_cycles/`.

## Caveats — stated by design

> **Lipoplex MD parameters.** The DOTAP / MC3 lipid topologies are **MARTINI-2 analogy models**, not independently validated published parameters. All MD conclusions are **qualitative / comparative** (relative ranking of DNA-condensing tendency across formulations and protonation states), not quantitative binding free energies.

> **Bound-state ΔG must never be quoted without its residency fraction.** Cycle 3b energies are *conditional* on the peptide occupying the pocket: they state how tight the pose is while it exists, not how strong binding is. Three runs have residency < 50% (deltorphin II at μ: 10.7%, 13.6%). The merge tooling refuses to emit a ΔG without its residency, and every downstream consumer must carry both.
