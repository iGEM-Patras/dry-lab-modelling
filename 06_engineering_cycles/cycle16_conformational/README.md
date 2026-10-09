# Cycle 16: is the address graft enough? (RUN. Control gate failed.)

> **Outcome, 9 Oct 2026.** This cycle ran. **G1, the control-validity gate, FAILED**: a
> conformationally constrained peptide was indistinguishable from a flexible one, so the
> metric cannot detect constraint in this system. Following the pre-registered decision rule,
> our own payload was **not scored and not run**. Full verdict in [`VERDICT.md`](VERDICT.md).
> The pre-registration below is unchanged from before the trajectories were opened.


**The literature moved under this project's central assumption, and that is worth knowing
before 21 October.**

## The finding

*Mechanistic insights into ligand selectivity in μ- and δ-opioid receptors **beyond the
"message-address" conceptual framework***, Acta Pharm Sin B 2026,
doi:10.1016/j.apsb.2025.11.039.

That title names the framework this project's payload design rests on. From the abstract:

- EM-1's `Tyr-Pro-Trp-Phe` confers **>1500-fold** μ/δ selectivity, driven by **steric
  hindrance and a β-turn structure**
- **β-endorphin, with a more flexible sequence, binds non-selectively to both receptors**
- morphine binds through the **ECL2–TM5 cleft**, explaining its modest selectivity
- residues **2.63** and **3.29** are named selectivity determinants

Our payload `YGGFEVVG` is an all-L, unconstrained, free-acid peptide carrying deltorphin's
*address sequence* on enkephalin's message. The wiki already records why it must be so: a
gene cannot encode D-alanine or a C-terminal amide. **Deltorphin's δ-selectivity may depend
on the D-Ala² backbone constraint we were forced to drop, not only on the `-Val-Val-Gly`
address we kept.**

If so, this is not a sixth method failure. It is an *explanation* for the five:

| cycle | result |
|---|---|
| 1 | Δ_sel indistinguishable from zero (after correction) |
| 7 | +1.23 ± 1.76, interval spans zero |
| 8 | μ-preferring |
| 14 | replicates disagree by 17× the effect |

Every one of them says "no measurable δ-preference". A mechanism that predicts exactly that
is a better reading than five independent methodological failures.

## A correction to Cycle 15's residue choice

Cycle 15 mutated **W284 = 6.58**, chosen for being the largest chemical change in the pocket.
The paper names **2.63** and **3.29**. Mapping those by Ballesteros-Weinstein, validated
against the canonical Asp3.32 amine anchor (DOR D128 / MOR D149):

| position | δ (DOR) | μ (MOR) | |
|---|---|---|---|
| **2.63** | **K108** | **N129** | divergent, loses a formal charge |
| **3.29** | **L125** | **I146** | divergent |
| 3.32 | D128 | D149 | conserved, anchor, not a determinant |
| 6.58 | W284 | K305 | divergent, **not literature-named** |

**K108 was not even in Cycle 15's candidate set**: that selection began at residue 125.

## What Cycle 16 does

Measures whether the payload carries the *conformational* property, not just the address
*sequence*, using trajectories **already computed**. Full gates in
`data/cycle16_prereg.json`, written before any analysis.

The design has internal controls: deltorphin (D-Ala², constrained) and EM-1 (β-turn,
>1500×) against met-enkephalin (flexible, 3.7×). **G1 can fail**: if the constrained
peptides do not separate from the flexible one, the metrics do not capture constraint here
and nothing is claimed.

## What it cannot do

It cannot produce a δ/μ value for `YGGFEVVG`. It tests whether a structural *precondition*
is present. The cAMP assay remains the only thing that measures the quantity itself.
