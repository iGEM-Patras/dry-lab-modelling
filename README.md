# PENK Dry-Lab Modelling

Computational audit and design work supporting an enkephalin-based analgesic strategy: **proenkephalin (PENK)** expression combined with a **neprilysin (NEP / MME)** knockdown arm, delivered by cationic / ionizable **lipoplexes**.

The full narrative — rationale, results, and honest limitations — is in **[`docs/project_brief.pdf`](docs/project_brief.pdf)**. Every tool version, force field, database accession, and published design rule is recorded in **[`methods_references.md`](methods_references.md)**.

## Workstreams

| Dir | Workstream | What it establishes |
|-----|-----------|---------------------|
| [`01_plasmid_audit/`](01_plasmid_audit/) | Audit of four PENK expression cassettes | Which construct to use (plasmid 3); which is defective (plasmid 1, truncated PENK) |
| [`02_restriction_qc/`](02_restriction_qc/) | Restriction-digest QC design + virtual gel | 2-digest scheme to confirm identity / gene order before transfection |
| [`03_sirna_design/`](03_sirna_design/) | Human anti-NEP (MME) siRNA design | 4 orderable siRNA duplexes with off-target + thermodynamic scoring |
| [`04_lipoplex_md/`](04_lipoplex_md/) | Lipoplex coarse-grained MD | pH-dependent DNA binding of the delivery vehicle across 3 formulations |

## Key results at a glance

- **Plasmid 3 (PENK-IRES-mEGFP) is the cleanest construct** — PENK cap-driven, intact signal peptide, byte-identical to UniProt P01210. **Plasmid 1 has a genuine defect** (truncated 7th enkephalin core) invisible on a gel — Sanger-verify or discard.
- **Four validated-in-silico anti-MME siRNAs** target the CDS shared by all four transcript variants — 19/19 on-target, 0 off-targets ≥17/19.
- **Lipoplex MD reproduces the ionizable-lipid pH switch** (50 ns × 3 seeds): protonated MC3-H⁺ binds DNA strongly, neutral MC3⁰ does not reliably bind, permanent-cation DOTAP binds most reproducibly. Convergence diagnostics justify a 200 ns extension (running).

## Status

This repository reflects the **initial 50 ns MD stage**. The 200 ns extended-run results will be folded into `04_lipoplex_md/` and the brief when those runs complete.

## Reproducibility

Coarse-grained MD used **GROMACS 2024.5** with the **MARTINI 2** force field. Sequence work used **Biopython**; siRNA off-target screening used **NCBI BLAST+ (blastn-short)** against human `refseq_rna`. See `methods_references.md` for the complete list with citations. MD input files (`.mdp`, topology) and the analysis script are under `04_lipoplex_md/`.

> **Important caveat (stated by design):** the DOTAP / MC3 lipid topologies are **MARTINI-2 analogy models**, not independently validated published parameters. All MD conclusions are **qualitative / comparative** (relative ranking of DNA-condensing tendency across formulations and protonation states), not quantitative binding free energies.
