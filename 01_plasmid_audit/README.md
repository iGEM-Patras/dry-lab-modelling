# 01 · Plasmid audit

Feature-level audit of four PENK expression cassettes (pcDNA3.1(+)-type backbones), differing in **gene order** and **linker** (EMCV IRES vs self-cleaving P2A). All carry the **native** human PENK sequence — they are the expression-system test-bed, not the engineered anionic-address payload.

| # | Plasmid | Size (bp) | PENK identity | Verdict |
|---|---------|-----------|---------------|---------|
| 1 | mEGFP-IRES-PENK | 7,500 | **TRUNCATED (263 aa, 6/7 cores)** | DEFECT — Sanger-verify or discard |
| 2 | mEGFP-P2A-PENK | 6,971 | full (266 aa) | OK, but PENK is downstream of P2A → altered N-terminus, may impair secretion |
| 3 | PENK-IRES-mEGFP | 7,512 | full (267 aa) | **cleanest — recommended** |
| 4 | PENK-P2A-mEGFP | 6,971 | full (267 aa) | OK |

**Reference:** UniProt **P01210** (human proenkephalin). Plasmid 3's PENK is byte-identical to the reference; plasmid 1 carries a premature stop truncating the C-terminal YGGFMRF (7th enkephalin core).

## Files
- `plasmid_feature_audit.csv` — per-plasmid, per-feature audit (sizes, ORFs, linker, PENK integrity, enkephalin-core count).

The source SnapGene `.dna` files and the annotated engineered insert are tracked as project artifacts (not in this repo).
