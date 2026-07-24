# 01 · Plasmid audit

Feature-level audit of four PENK expression cassettes (pcDNA3.1(+)-type backbones), differing in **gene order** and **linker** (EMCV IRES vs self-cleaving P2A). All carry the **native** human PENK sequence — they are the expression-system test-bed, not the engineered anionic-address payload.

| # | Plasmid | Size (bp) | PENK identity | Verdict |
|---|---------|-----------|---------------|---------|
| 1 | mEGFP-IRES-PENK | 7,500 | **TRUNCATED (263 aa, 6/7 cores)** | DEFECT — Sanger-verify or discard |
| 2 | mEGFP-P2A-PENK | 6,971 | full (266 aa) | OK, but PENK is downstream of P2A → altered N-terminus, may impair secretion |
| 3 | PENK-IRES-mEGFP | 7,512 | full (267 aa) | **cleanest — recommended** |
| 4 | PENK-P2A-mEGFP | 6,971 | full (267 aa) | OK |

**Reference:** UniProt **P01210** (human proenkephalin). Plasmid 3's PENK is byte-identical to the reference; plasmid 1 carries a premature stop truncating the C-terminal YGGFMRF (7th enkephalin core).

## Engineered payload (therapy construct)

The anionic-address PENK — the construct that gives the therapy its function — recodes all seven enkephalin cores **YGGF[M/L] → YGGFEVVG**. It currently exists as a **cloning-ready insert** (NheI/XhoI), **not yet in an expression backbone**, so it is audited here but is deliberately kept out of the four-plasmid gel QC.

Verified (867 nt CDS → 288 aa): Met start, single clean stop, **7 of 7 engineered cores, 0 native cores**, GC 59.9%, no homopolymers, cores made synonymously distinct, single flanking NheI/XhoI with **no internal cut sites**.

> **QC implication:** the engineered insert has **no AflII or XbaI site** — the native-plasmid Digest A/B scheme does not apply. Once cloned into a backbone, the engineered plasmid needs its own restriction map computed fresh.

## Files
- `plasmid_feature_audit.csv` — per-construct, per-feature audit (four native plasmids + engineered payload): sizes, ORFs, linker, PENK integrity, enkephalin-core count.
- `engineered_payload/engineered_PENK_GC-optimized.fasta` — GC-optimized CDS + cloning-ready (NheI-Kozak-CDS-XhoI) sequences.
- `engineered_payload/engPENK_insert_annotated.gb` — annotated GenBank insert (features: cores, signal peptide, cloning sites).

The source SnapGene `.dna` files for the four native plasmids are tracked as project artifacts (not in this repo).
