# 09, Codon composition & GC recoding

Wet-lab request: bring the ordered constructs down to a synthesis-friendlier GC content
without touching the protein.

## What was done

All recoding is **synonymous**, every cistron translates to a byte-identical protein.
The optimiser is **feature-aware**: it recodes only in-frame annotated coding blocks and
treats the IRES, the Kozak context, the P2A element and the signal peptide as locked spans.
Motif checks (AT-runs, homopolymers, `ATTTA`, `AATAAA`) are evaluated in a local window
around each candidate substitution, not globally.

## Result (`PENK_order_sheet.csv`)

| Construct | Target GC | Final GC | CAI | Homopolymers ≥6 |
|---|---|---|---|---|
| mEGFP-P2A-His-PENK | 40 % | 40.02 % | 0.736 | 0 |
| His-PENK-P2A-mEGFP | 40 % | 39.98 % | 0.733 | 0 |
| mEGFP-IRES-His-PENK | 45 % | 45.02 % | 0.694 | 4 |
| His-PENK-IRES-mEGFP | 45 % | 44.99 % | 0.651 | 4 |

The four homopolymers in the IRES constructs are **pre-existing inside the locked IRES** , 
they are not introduced by recoding and cannot be removed without altering the element.

## The honest cost

CAI falls. That is the real trade for lower GC and it is not free: codon adaptation is one
of the correlates of expression level in mammalian cells. The direction of the effect is a
question a transfection and a blot answer far more cheaply than any further modelling.
`gc40_feasibility_floors.csv` gives the arithmetic floor per construct; `gc_rich_window_sources.csv`
shows most GC-rich windows trace to the reporter, not the engineered insert.

## Files

- `PENK_order_sheet.csv`, what to send the synthesis vendor
- `PENK_recode_validation.csv`, per-construct validation (per-cistron protein identity, locked-element integrity, epitope copy number)
- `recoded_constructs/*.dna`, SnapGene files, annotations preserved, round-trip verified
- `PENK_GC40_EL.pdf` / `PENK_GC40_EN.pdf`, referenced write-up (Greek / English)
- `figures/`, feasibility floors and where the GC actually sits
