# 02 · Restriction-digest QC

A two-tier digest scheme to confirm construct identity (insert, linker type, gene order) and catch mis-assembly **before transfection**.

- **Digest A — AflII + XbaI (insert release):** constant **5,345 bp backbone** (loading / complete-digestion control) + one insert band reporting linker type (~2.16 kb = IRES, ~1.63 kb = P2A). Cannot resolve gene order.
- **Digest B — NcoI (identity fingerprint):** unique 5-band pattern per plasmid; the second-largest band is diagnostic for gene order.

**Critical limitation:** passing the gel does **not** clear plasmid 1 — its PENK truncation is a point-level lesion invisible on any gel and must be confirmed by **Sanger sequencing** of the PENK 3′ end.

## Files
- `restriction_qc_protocol.md` — full bench recipe, expected band tables, and interpretation logic.
- `restriction_qc_gel.png` — virtual agarose gel (both digests, all four plasmids, 1 kb-plus ladder).
