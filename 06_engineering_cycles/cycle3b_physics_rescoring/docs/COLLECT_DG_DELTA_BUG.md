# collect_dg.py delta-parse defect: post-mortem

**Found:** 2026-08-31, by the first real rescoring run (c3b_dtII_DOR rep1).
**Severity:** silent wrong number that passed every existing guard.

## What happened

`gmx_MMPBSA` 1.5.0.3 writes four total rows into `*_FINAL.dat`:

| block | label | value (this run) |
|---|---|---|
| Complex | `TOTAL` | - |
| Receptor | `TOTAL` | - |
| Ligand | `TOTAL` | **-123.33** |
| Delta (Complex - Receptor - Ligand) | `ΔTOTAL` | **-67.48** |

Only the delta row is prefixed with U+0394. The old pattern was
`(?:DELTA\s+TOTAL|Delta\s+TOTAL|TOTAL)` taking the **last** match, which never
matches the glyph, so it returned the **ligand's absolute GB energy** as dG_bind.

## Why no guard caught it

The physical-plausibility check accepts roughly -150..0 kcal/mol. A peptide ligand's
absolute GB energy lands inside that window, so -123.33 looked like a believable
binding energy. The guard was doing its job; the range simply cannot distinguish
these two quantities.

## Fix

`parse_dat()` now:

1. anchors on the `Delta (Complex - Receptor - Ligand)` **header**, never a total row;
2. truncates at the next block header so the search cannot stray;
3. accepts the total row with or without the leading glyph;
4. requires **exactly one** total row in that block, else refuses;
5. **cross-checks that the printed components sum to the printed total** (tolerance
   0.5 kcal/mol). This is the structural safeguard: it does not depend on knowing
   the label.

Both negative controls refuse correctly: delta block deleted -> FAIL; one component
value corrupted so the sum disagrees -> FAIL.

## Record

The single result row carrying -123.33 was **quarantined, not deleted**:
`results_stage1.csv.POISONED_ligand_absolute_20260831T1620` on the cluster.

## Generalisable lesson

A range-based sanity check cannot separate two quantities whose ranges overlap.
Where a total is printed alongside its components, cross-check the sum: that
constraint is independent of parsing and of the label.
