# 10, Immunogenicity & antibody detection

Two independent questions about the **engineered** product that the original design did not ask.

## 1. Can any commercial antibody detect it?

No. The construct recodes every enkephalin core to `YGGFEVVG`; every registry
anti-enkephalin antibody is raised against native `YGGFM`. `antibody_shortlist.csv`
records 11 candidates with RRIDs and a verdict for each. A **custom anti-`YGGFEVVG`
polyclonal is on the critical path**, the peptide exists (`10_immunogenicity_antibody`
cross-refs `04_structures`), but the antibody does not.

## 2. Is the engineered epitope predicted immunogenic?

MHC class I binding was predicted with **MHCflurry 2.x** over a common HLA-A/B/C panel
(`mhc_predictions_full.csv`, 6,120 allele-peptide pairs).

| Peptide group | pairs | peptides | strong binders | % strong | best %ile |
|---|---|---|---|---|---|
| engineered `YGGFEVVG` | 3,340 | 334 | 62 | 1.86 % | 0.020 |
| native `YGGFM/L` | 2,200 | 220 | 39 | 1.77 % | 0.060 |
| P2A remnant junction | 580 | 58 | 12 | 2.07 % | 0.126 |

**Reading:** the engineered epitope is not meaningfully more immunogenic than the native
one it replaces (1.86 % vs 1.77 % strong binders). The **P2A remnant junction is the highest
of the three**, a specific argument for preferring the IRES cassettes if immunogenicity of
a persistently expressed product matters, since P2A leaves a 21-residue remnant on the
upstream protein by design.

Class I prediction speaks to CD8 recognition of an intracellular product; it says nothing
about antibody responses to a secreted peptide. Treat this as a screen, not a clearance.
