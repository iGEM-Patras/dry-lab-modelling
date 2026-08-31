# PENK Dry-Lab Modelling

Computational audit and design work supporting an enkephalin-based analgesic strategy: **proenkephalin (PENK)** expression combined with a **neprilysin (NEP / MME)** knockdown arm, delivered by cationic / ionizable **lipoplexes**.

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

## Key results at a glance

- **Plasmid 3 (PENK-IRES-mEGFP) is the cleanest construct** — PENK cap-driven, intact signal peptide, byte-identical to UniProt P01210. **Plasmid 1 has a genuine defect** (truncated 7th enkephalin core) invisible on a gel — Sanger-verify or discard.
- **Two human-exclusive anti-MME siRNAs** (CDS303, CDS2101) target the CDS shared by all MME transcript variants. The **original four-duplex panel was withdrawn**: it is cross-reactive with mouse *Mme* (one guide a perfect 19/19 match). The corollary is that the exclusive guides cannot be validated in a mouse model — a separate rodent surrogate is needed for in-vivo work.
- **No commercial antibody detects the engineered product.** The construct recodes every enkephalin core to `YGGFEVVG`; registry anti-enkephalin antibodies are raised against native `YGGFM`. A custom anti-`YGGFEVVG` polyclonal must be raised and is on the critical path.
- **Lipoplex MD reproduces the ionizable-lipid pH switch** (200 ns × 3 seeds, mean ± SEM): protonated MC3-H⁺ binds DNA as tightly as permanent-cation DOTAP (~0.47 nm closest approach); neutral MC3⁰ holds DNA ~1.3 nm away with an RDF peak at the bulk value. Contacts plateau by ~100 ns, so the 100–200 ns analysis window is equilibrated.
- **The two processing routes are affected unequally by the cassette swap.** PC1/3 and PC2 cut C-terminal to the dibasic; cathepsin L/V cut N-terminal to it. The swap leaves the convertase scissile context identical at all 7 cassettes but moves the cathepsin P2 residue from Phe (7/7 within the preferred Leu/Trp/Phe/Tyr set) to Val (0/7). Separately, 5 of 7 engineered cassettes are Gly-extended PAM substrates where no native cassette is. Both are directly testable in the cell-free assay in `07_invitro_penk/`.
- **Payload δ-selectivity engineering returned a negative result** across three pre-registered cycles. The final cycle (3b, MM-GBSA physics rescoring) **failed its calibration gate**: it gets the *direction* of δ/μ preference right (G1 pass) but cannot resolve the *magnitude* at n=5 (G2′ and G3 fail; regression CI spans zero). Recommendation: radioligand competition binding on `YGGFEVVG` and `YGGFDIIG`.

## Status

All dry-lab workstreams are **complete**. Cycle 3b terminated on 2026-08-31 per its pre-registration; see [`06_engineering_cycles/cycle3b_physics_rescoring/docs/GATE_VERDICT_BOUND.md`](06_engineering_cycles/cycle3b_physics_rescoring/docs/GATE_VERDICT_BOUND.md) for the terminal verdict. No further computational work is planned — the project's open questions are now wet-lab questions.

`07_invitro_penk/` is the first of those wet-lab questions worked up into a benchtop design. It is a **design, not a result**: no experimental data exists yet.

## Reproducibility

Coarse-grained MD used **GROMACS 2024.5** with the **MARTINI 2** force field. All-atom membrane MD and MM-GBSA rescoring (cycle 3b) used **GROMACS 2024.5** + **AmberTools**. Sequence work used **Biopython**; siRNA off-target screening used **NCBI BLAST+ (blastn-short)** against human `refseq_rna`. See `methods_references.md` for the complete list with citations. MD input files (`.mdp`, topology) and analysis scripts are under `04_lipoplex_md/` and `06_engineering_cycles/`.

## Caveats — stated by design

> **Lipoplex MD parameters.** The DOTAP / MC3 lipid topologies are **MARTINI-2 analogy models**, not independently validated published parameters. All MD conclusions are **qualitative / comparative** (relative ranking of DNA-condensing tendency across formulations and protonation states), not quantitative binding free energies.

> **Bound-state ΔG must never be quoted without its residency fraction.** Cycle 3b energies are *conditional* on the peptide occupying the pocket: they state how tight the pose is while it exists, not how strong binding is. Three runs have residency < 50% (deltorphin II at μ: 10.7%, 13.6%). The merge tooling refuses to emit a ΔG without its residency, and every downstream consumer must carry both.
