# Restriction-Digest QC Protocol — Four PENK Cassette Plasmids

**Purpose:** Confirm construct identity (correct insert, linker type, and gene order)
and catch mis-assembly before transfection. Two-tier scheme.

## The four plasmids
| Lane | Plasmid | Size (bp) | Linker | Gene order |
|---|---|---|---|---|
| 1 | mEGFP-IRES-PENK | 7,500 | IRES | mEGFP first |
| 2 | mEGFP-P2A-PENK  | 6,971 | P2A  | mEGFP first |
| 3 | PENK-IRES-mEGFP | 7,512 | IRES | PENK first |
| 4 | PENK-P2A-mEGFP  | 6,971 | P2A  | PENK first |

---
## Digest A — insert release (screen all four in one master mix)
**Enzymes:** AflII + XbaI (double digest). Both single-cutters in all four plasmids.

Expected bands (bp):
| Plasmid | Backbone (const.) | Insert | Linker call |
|---|---|---|---|
| 1 mEGFP-IRES-PENK | 5,345 | 2,155 | IRES (~2.16 kb) |
| 2 mEGFP-P2A-PENK  | 5,345 | 1,626 | P2A  (~1.63 kb) |
| 3 PENK-IRES-mEGFP | 5,345 | 2,167 | IRES (~2.16 kb) |
| 4 PENK-P2A-mEGFP  | 5,345 | 1,626 | P2A  (~1.63 kb) |

- The **5,345 bp backbone band is constant across all four** → internal loading/complete-digestion control.
- Insert band reports **linker type**: ~2.16 kb = IRES, ~1.63 kb = P2A.
- **Limitation:** cannot distinguish the two IRES plasmids (2,155 vs 2,167 bp — 12 bp apart, unresolvable) or the two P2A plasmids (identical). Gene order needs Digest B.

## Digest B — identity fingerprint (confirm gene order / catch mis-assembly)
**Enzyme:** NcoI (single digest, 5 cuts each). Fingerprint is unique per plasmid.

Expected bands (bp):
| Plasmid | Bands |
|---|---|
| 1 mEGFP-IRES-PENK | 3,342 / 1,648 / 1,446 / 735 / 329 |
| 2 mEGFP-P2A-PENK  | 3,342 / 2,416 / 735 / 311 / 167 |
| 3 PENK-IRES-mEGFP | 3,342 / 2,749 / 735 / 357 / 329 |
| 4 PENK-P2A-mEGFP  | 3,342 / 2,226 / 735 / 357 / 311 |

- Shared 3,342 + 735 bp bands = common backbone/cassette landmarks.
- The **diagnostic band** is the second-largest: 1,648+1,446 doublet (P1) / 2,416 (P2) / 2,749 (P3) / 2,226 (P4) — resolves gene order.
- **The plasmid-1 truncation** (PENK missing its C-terminal core) will NOT change these gel bands (it's a point-level premature stop) — flag: gel QC passing does NOT clear plasmid 1; it must be confirmed by **Sanger sequencing** of the PENK 3' end.

---
## Bench recipe (per lane, adjust to your kit)
- 1 µg plasmid DNA
- 1× rCutSmart (or NEB buffer compatible with both enzymes; AflII+XbaI+NcoI all work in rCutSmart)
- 10 U each enzyme, 37 °C, 1 h
- 1% agarose, 1× TAE, 100 V ~45 min, 1 kb-plus ladder

## Interpretation logic
1. **Digest A**: every lane must show the 5,345 bp band + one insert band. Missing backbone band → incomplete digest. Wrong insert size → wrong linker.
2. **Digest B**: match the 5-band fingerprint to the table to confirm which plasmid is in the tube (gene order).
3. **Sanger** the PENK ORF (esp. plasmid 1 3' end) — gel cannot detect the single-core truncation.
