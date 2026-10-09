# iGEM Model / Best Model: how the dry-lab package aligns

**iGEM Patras · dry-lab modelling** · a self-audit mapping our computational work to the iGEM judging framework, so the wiki and judging-form entries are targeted rather than generic.

---

## What changed in 2026 (why this matters)

Gold is **no longer a separate judge vote**. It is now inferred from the three
**Special Awards** a team selects on the Judging Form: each judge scores those
awards on their rubrics, and **all three selected awards must reach a "yes"**
for the Gold criterion to be met. Teams elect up to three awards, at least one
from each list plus a third from either. Selecting fewer than three forfeits
Gold eligibility.

**Implication for us:** if the team selects **Best Model** as one of its three,
the modelling work is not decoration: it is load-bearing for the medal. This
document is written so that selection is defensible.

> The per-question rubric wording is deliberately unpublished by iGEM (to stop
> teams "teaching to the test"). This alignment therefore maps our work to the
> **public** modelling expectations, not to any leaked score language.

---

## The three public modelling expectations, and our evidence

iGEM's public description of strong modelling asks teams to:

**(1) Model the system to understand performance and guide experiments.**

| Our work | How it guides the wet lab |
|---|---|
| **Lipoplex CG-MD** (3 formulations × 3 seeds) | Resolves the pH-dependent DNA-binding switch → tells the team to choose an **ionizable** lipid (MC3-type) over permanent-cation DOTAP. A design decision made *by the model*. |
| **siRNA design + accessibility** | Ranks 2,084 candidate sites → 4 orderable duplexes with a defensible priority (CDS1224 first). The model chooses the reagents. |
| **Plasmid audit** | Model-level sequence audit **found a real defect** (plasmid 1 truncated PENK) → removes a construct from the wet-lab plan before money is spent. |
| **Restriction-QC design** | Virtual digest predicts the exact gel the wet lab should see → converts modelling into a bench acceptance test. |

**(2) Show experimental validation in line with project goals.**

The model outputs are written as **testable predictions with named assays**, so
the wet lab can close the loop:
- siRNA → qPCR knockdown at 48 h (predicted ≥70%) + CD10/NEP-activity Western.
- Plasmid identity → the two-digest QC gel (predicted band table) + Sanger.
- Lipoplex → gel-shift / DLS at endosomal vs physiological pH should mirror the
  MD contact trend (MC3 binds low-pH, releases neutral; DOTAP binds both).

This is the modelling↔wet-lab **iterative loop** iGEM rewards: each model
output names the experiment that would confirm or refute it.

**(3) Consider future implementation: application, scalability, safety.**

- **Application:** **intranasal** lipoplex delivery for analgesia (stated, with the BBB
  rationale). *(Superseded: an earlier draft of this document said intrathecal.)*
- **Scalability:** the pipeline is a reusable code repository (below), not a
  one-off: any PENK/NEP construct can be re-audited.
- **Safety:** limitations are stated *by design*, not hidden; NEP off-target
  substrates (Aβ, substance P) motivate keeping knockdown local/transient; MD
  models are MARTINI analogies so conclusions are comparative, not affinities.

---

## Why this modelling is credible (the differentiators)

Judges reward modelling that is honest and reproducible over modelling that
overclaims. Our package is built to that standard:

1. **A real negative result.** The audit found and reported a genuine defect
   (plasmid 1) rather than rubber-stamping all constructs. Finding problems is
   evidence the audit is real.
2. **Error bars and convergence honesty.** MD metrics are reported as mean ± SEM
   over 3 seeds, and the large error bars are acknowledged (binding still
   nucleating at 50 ns), which is *why* the 200 ns extension was run, and it has since
   completed. We
   report uncertainty instead of a single pretty number.
3. **Stated model limitations.** MARTINI topologies are analogy models;
   accessibility folding ignores RNA-binding proteins; seed-level off-target
   frequency is flagged as a follow-up. Each caveat is written next to the
   result it qualifies.
4. **Full reproducibility.** Every method, force field, database, and design
   rule is traceable to a methods/references log, and the entire codebase is in
   a version-controlled repository (pushed to GitHub).

---

## Deliverables checklist for the Best Model wiki page

To convert this into a scoring wiki page and judging-form entry:

- [ ] **Model page** narrating the four workstreams as *models that made
      decisions* (lead with the plasmid-1 defect and the MC3-vs-DOTAP choice).
- [ ] Embed the figures: `restriction_qc_gel.png`, `sirna_design_v2_figure.png`,
      `lipoplex_md_50ns.png` (→ 200 ns when it lands).
- [ ] A **methods & reproducibility** section linking the GitHub repo and the
      methods log, reproducibility is a scored differentiator.
- [ ] The **model→experiment loop** table (expectation 2 above) shown
      explicitly, so judges see validation is planned, not hoped for.
- [ ] A **limitations** box: counterintuitively a *positive* signal to judges.
- [ ] 150-word judging-form description: lead with "our models made three
      concrete design decisions the wet lab acted on."

---

## One-paragraph pitch (drop-in for the 150-word form)

> Our dry-lab did not describe the system. It decided it. A sequence-level
> audit of four PENK cassettes found a real defect (a truncated enkephalin
> core) and selected the construct to build. A ViennaRNA-scored siRNA pipeline
> screened 2,084 sites to four orderable anti-neprilysin duplexes with a ranked
> priority. Coarse-grained MARTINI MD across three lipid formulations
> (triplicate seeds, mean ± SEM) resolved the pH-dependent DNA-binding switch
> that motivates our ionizable-lipid choice over a permanent cation. Every model
> output is written as a testable prediction with a named wet-lab assay, closing
> the design–build–test loop. Limitations: MARTINI analogy topologies, in-cell
> RNA structure, off-target seed frequency, are stated beside each result. The
> full pipeline is reproducible and version-controlled. The model is
> load-bearing: remove it and three wet-lab decisions lose their basis.
