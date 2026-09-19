# 08 · Checkable audit

An independent audit of the wet-lab bench guide. Every finding is stated so that it can be
checked against a cited source rather than taken on authority — hence "checkable".

| Contents | What it is |
|---|---|
| `tables/` | One CSV per finding class, each row carrying its own evidence and source |
| `figures/` | Supporting figures |

## Scope

17 findings, 5 of them classified critical. The audit covers claims made in the bench guide
about cell-line choice, processing competence, detection reagents, and the mapping between
the guide's engineering-cycle numbering and this repository's.

## The finding with the largest consequence

**HEK293T cannot process proenkephalin into small opioid peptides.** The prohormone
convertases `PCSK1` and `PCSK2` and the obligate chaperone `SCG5` (7B2) are all effectively
absent in that line (nTPM ≤ 0.1); `CPE` and `PCSK1N` are present. The competence claim has
to be made against the cell line actually used, not against a tissue that expresses the
full cascade.

This is why the cell-free processing assay in `07_invitro_penk/` exists: it supplies the
missing enzymes directly rather than relying on the host cell to provide them.

See `tables/hek293t_processing_competence.csv` for the per-gene expression evidence.

## Related findings

- No commercially available antibody detects the engineered peptide, because every cassette
  was recoded away from the native epitope. See `10_immunogenicity_antibody/`.
- The bench guide's cycle numbering does not map one-to-one onto the dry-lab cycles;
  the reconciliation is in `06_engineering_cycles/cycle_reconciliation.csv`.
