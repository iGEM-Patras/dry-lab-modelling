# In vitro reconstitution of PENK processing

Cell-free assay design for comparing proteolytic processing of native human proenkephalin
(UniProt P01210) against the engineered construct engPENK. Everything here is computed
from the two sequences; no experimental data yet.

## What this answers

The engineered cassette replaces `YGGFM`/`YGGFL` with `YGGFEVVG` at all seven sites. That
swap has two consequences the wet lab can test in a tube:

1. **The two processing routes are affected unequally.** PC1/3 and PC2 cut C-terminal to
   the dibasic; cathepsin L and V cut N-terminal to it. The swap leaves the convertase
   scissile context identical at all 7 cassettes, but moves the cathepsin P2 residue from
   Phe (7/7 in the preferred Leu/Trp/Phe/Tyr set) to Val (0/7). Prediction: equal
   convertase processing, reduced cathepsin processing.
2. **Amidation is engineered-only.** 5 of 7 engPENK cassettes are Gly-extended and
   therefore PAM substrates; 0 of 7 native cassettes are.

## Layout

```
docs/     PENK_INVITRO_PROTOCOL.md / .pdf   the working protocol (8 pp, 4 figures)
figures/  fig_junction_map          all predicted cut sites, both constructs
          fig_cascade               staged order of addition
          fig_decision_tree         how to interpret the read-out
          fig_design_summary        the two-route divergence, amidation, pooling
tables/   junction_peptides_order   24 peptides, vendor-ready
          control_peptides_order    8 standards and reference substrates
          invitro_ms_targets        every observable species, m/z at z=1,2,3
          cleavage_predictions      site-by-site, tier-scored
          cassette_scissile_context per-cassette P2/P1/P1' for both routes
          pool_isotope_notes        per-pool resolution warnings
          enzyme_conditions         buffers, cofactors, pH per enzyme
          invitro_references        sources with DOI and access status
```

## Before you order anything

- **Normalise enzymes by activity units, not protein mass.** Specific activities across
  these enzymes span orders of magnitude; equal-mass loading produces a false negative on
  the least active arm.
- **The native arm is the positive control.** If it does not produce Met-enkephalin
  (574.2330) above background, no engPENK result is interpretable.
- **Read section 3 before combining buffers.** The cathepsin buffer's EDTA inhibits both
  downstream metalloenzymes; its reducing agent destroys the disulfide-dependent
  conformation that Stage 2 exists to test.
- Two standards must be ordered as C-terminal amides, not free acids: STD-ENGA
  (YGGFEVV-NH2) and STD-ADR (YGGFMRRV-NH2).
- Pool 6 carries an isotope-overlap caveat: N099 and N106 differ by 0.95 Da and have
  identical GRAVY, so they may co-elute. Deconvolute the isotope envelope and confirm by
  MS2.

## Caveats

Reference 2 (Dupuy 2003) was read from its abstract only — it is paywalled. Confirm before
publication. Reference 3 (Shennan 1995) reports zymogen *maturation* parameters, not
mature-enzyme turnover optima, and must not be used as an assay optimum.
