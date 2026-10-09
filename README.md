# PENK Dry-Lab Modelling: iGEM Patras 2026, project *Epione*

> Dry-lab repository for **Epione**, an intranasal DNA-encoded enkephalin therapy for chronic
> cancer pain. This repository holds the computational work only; it is linked from the team
> wiki, which carries the project narrative.
>
> | | |
> |---|---|
> | Engineering Success | [`05_presentation/WIKI_ENGINEERING.md`](05_presentation/WIKI_ENGINEERING.md): four Design–Build–Test–Learn cycles |
> | Registry parts | basic and composite part pages (see the wiki for accession numbers) |
> | **Safety: δ-agonist seizure liability** | [`DELTA_SEIZURE_SAFETY.md`](DELTA_SEIZURE_SAFETY.md): 12 references, assessed both directions |
> | How the methods work | [`METHODS_GUIDE.md`](METHODS_GUIDE.md) · [`GLOSSARY.md`](GLOSSARY.md) |
> | Every tool, version and citation | [`methods_references.md`](methods_references.md) |
> | Who did what | [`ATTRIBUTIONS.md`](ATTRIBUTIONS.md) |
>
> **Predictions in this repository were committed before the tests that judged them.** The
> ledger stands at **20 scored, 10 confirmed, 10 falsified**, and the falsifications are left
> visible beside their corrections rather than deleted. That is the point of the repository,
> not a disclaimer on it.

Computational audit and design work supporting an enkephalin-based analgesic strategy: **proenkephalin (PENK)** expression combined with a **neprilysin (NEP / MME)** knockdown arm, delivered by cationic / ionizable **lipoplexes**.

**[`METHODS_GUIDE.md`](METHODS_GUIDE.md)** explains how each computational method works, why it
was chosen, how to read its output, and where it fails: written for a reader who can program
but has no chemistry or bioinformatics background. **[`GLOSSARY.md`](GLOSSARY.md)** defines the
terminology used across the repository.

The full narrative (rationale, results, and honest limitations) is in **[`docs/project_brief.pdf`](docs/project_brief.pdf)**. Every tool version, force field, database accession, and published design rule is recorded in **[`methods_references.md`](methods_references.md)**.

## Workstreams

| Dir | Workstream | What it establishes |
|-----|-----------|---------------------|
| [`01_plasmid_audit/`](01_plasmid_audit/) | Audit of four PENK expression cassettes | Which construct to use (plasmid 3); which is defective (plasmid 1, truncated PENK) |
| [`02_restriction_qc/`](02_restriction_qc/) | Restriction-digest QC design + virtual gel | 2-digest scheme to confirm identity / gene order before transfection |
| [`03_sirna_design/`](03_sirna_design/) | Human anti-NEP (MME) siRNA design | 2 orderable human-exclusive duplexes with off-target + thermodynamic scoring |
| [`04_lipoplex_md/`](04_lipoplex_md/) | Lipoplex coarse-grained MD | pH-dependent DNA binding of the delivery vehicle across 3 formulations |
| [`05_presentation/`](05_presentation/) | Slides + wet-lab handouts | Bench-facing summaries of the above |
| [`06_engineering_cycles/`](06_engineering_cycles/) | Payload engineering (3 pre-registered DBTL cycles) | A **negative result**: no computational route ranks these designs; the wet-lab assay is required |
| [`07_invitro_penk/`](07_invitro_penk/) | Cell-free processing assay design | The cassette swap is predicted **neutral for convertases, adverse for cathepsin L**, a falsifiable bench test |
| [`08_checkable_audit/`](08_checkable_audit/) | Independent audit of the wet-lab guide | 17 findings (5 critical) against the Greek bench guide, each with a reference |
| [`09_codon_gc_design/`](09_codon_gc_design/) | GC recoding for synthesis | All four constructs at target GC, protein untouched, with the CAI cost stated |
| [`10_immunogenicity_antibody/`](10_immunogenicity_antibody/) | MHC-I prediction + antibody detectability | Engineered epitope ≈ native immunogenicity; **P2A junction is the worst of the three** |
| [`11_wetlab_protocols/`](11_wetlab_protocols/) | Amendments 1–5 (EN + GR) | Dry-lab findings translated into bench actions |
| [`99_provenance/`](99_provenance/) | Plans, resume briefs, as-received inputs | Traceability from request to result |

## Key results at a glance

- **Plasmid 3 (PENK-IRES-mEGFP) is the cleanest construct**, PENK cap-driven, intact signal peptide, byte-identical to UniProt P01210. **Plasmid 1 has a genuine defect** (truncated 7th enkephalin core) invisible on a gel, Sanger-verify or discard.
- **Anti-MME siRNA: order `2700–2722` and `2459–2481` on MME-213 (`ENST00000615825.3`), by sequence.** [`03_sirna_design/ORDER.md`](03_sirna_design/ORDER.md) is the single source of truth and carries its own correction log; earlier documents in that directory name superseded guides in a different coordinate system. The guides were screened on efficacy (five independent models), seed-duplex Tm, genome-wide specificity, target accessibility, all four MME transcript variants, population variants, and, a check no design tool performs, against the four engPENK plasmids, since the lipoplex co-packages both cargoes into the same cell. ~~Previously recommended: two human-exclusive guides (CDS303, CDS2101)~~ target the CDS shared by all MME transcript variants. The **original four-duplex panel was withdrawn**: it is cross-reactive with mouse *Mme* (one guide a perfect 19/19 match). The corollary is that the exclusive guides cannot be validated in a mouse model, a separate rodent surrogate is needed for in-vivo work.
- **No commercial antibody detects the engineered product.** The construct recodes every enkephalin core to `YGGFEVVG`; registry anti-enkephalin antibodies are raised against native `YGGFM`. A custom anti-`YGGFEVVG` polyclonal must be raised and is on the critical path.
- **Lipoplex MD reproduces the ionizable-lipid pH switch** (200 ns × 3 seeds, mean ± SEM): protonated MC3-H⁺ binds DNA as tightly as permanent-cation DOTAP (~0.47 nm closest approach); neutral MC3⁰ holds DNA ~1.3 nm away with an RDF peak at the bulk value. Contacts plateau by ~100 ns, so the 100–200 ns analysis window is equilibrated.
- **The two processing routes are affected unequally by the cassette swap.** PC1/3 and PC2 cut C-terminal to the dibasic; cathepsin L/V cut N-terminal to it. The swap leaves the convertase scissile context identical at all 7 cassettes but moves the cathepsin P2 residue from Phe (7/7 within the preferred Leu/Trp/Phe/Tyr set) to Val (0/7). Separately, 5 of 7 engineered cassettes are Gly-extended PAM substrates where no native cassette is. Both are directly testable in the cell-free assay in `07_invitro_penk/`.
- **Payload δ-selectivity: three methods failed, two later passed calibration.** Cycles 1–3b returned negatives, 3b's MM-GBSA rescoring got the *direction* right but failed its magnitude gate at n=5. Cycles 7 and 9 then succeeded by calibrating against published reference opioids first: the co-folding affinity head cleared a pre-set correlation gate at n=13 (r = 0.805, p = 0.0009, signs correct 12/13), and the pose-convergence metric that Cycle 3a retired was rehabilitated in Cycle 9 (ρ = 1.000 against four peptides with published selectivity). **Current calibrated estimate for `YGGFEVVG`: +1.23 ± 1.76 kcal/mol δ-over-μ (~7×), nominally δ-preferring but not statistically separable from native Met-enkephalin.** A rigorous free-energy campaign then **failed its own control**: native Met-enkephalin, whose selectivity is published, returned **−3.12 and +5.41 kcal/mol** across two replicates, opposite signs from a seed change. The cause was diagnosed as λ-spacing rather than sampling time. The re-spaced 57-window campaign has since **completed and failed its reproducibility gate**, so **no free-energy value for `YGGFEVVG` is quoted anywhere in this project**. Seven computational routes have now been attempted; the two that rule out whole classes are that anything anchored to published affinities inherits a between-source disagreement larger than the effect, and anything computing selectivity as a difference of two large absolutes accumulates correlated bias. **The wet lab's chosen arbiter is the cAMP assay.** One difference to carry into its interpretation: every dry-lab number here is a *binding* difference, while cAMP measures functional *potency*, so a disagreement could be ligand bias, and nothing computational here can distinguish the two.

- **The four ordered constructs sit at 46 to 50 % GC** (P2A pair 46.4 % and 49.5 %, IRES pair 50.2 % and 50.0 %, measured over the whole construct; the PENK cistron alone is 46.1 to 49.5 % and the recoded payload cassettes are 53 to 55 %). *Correction, 9 Oct 2026: this sentence previously read "40 % for the P2A pair, 45 % for the IRES pair". Those are the design targets preserved in the filenames* `GC40` *and* `GC45`*, not measurements of the delivered v6 sequences, which drifted during the vendor-driven repair rounds. No region of any of the four constructs is within 2 points of 40 % or 45 %.* with **every cistron's protein byte-identical** to before. The cost is codon adaptation (CAI 0.65–0.74), a real trade, not a free lunch, and one a transfection settles faster than more modelling. Order sheet: [`09_codon_gc_design/PENK_order_sheet.csv`](09_codon_gc_design/PENK_order_sheet.csv).
- **The engineered epitope is not more immunogenic than the native one it replaces** (1.86 % vs 1.77 % strong MHC-I binders across 6,120 allele-peptide pairs). The **P2A remnant junction ranks highest of the three groups** (2.07 %), an argument for the IRES cassettes if immunogenicity of a persistently expressed product matters. See [`10_immunogenicity_antibody/`](10_immunogenicity_antibody/).
- **HEK293T cannot process proenkephalin to small opioid peptides.** PCSK1, PCSK2 and SCG5 (7B2) are all effectively absent (nTPM ≤ 0.1); CPE and PCSK1N are present. The competence claim must be made against HEK293T, the cells actually used, not against fibroblasts. Table: [`08_checkable_audit/tables/hek293t_processing_competence.csv`](08_checkable_audit/tables/hek293t_processing_competence.csv).
- **The wet-lab guide's engineering-cycle numbering does not map onto the dry-lab cycles.** Six guide cycles vs four repo cycles, reconciled in [`06_engineering_cycles/cycle_reconciliation.csv`](06_engineering_cycles/cycle_reconciliation.csv), guide Cycle 3 *is* a dry-lab cycle but belongs to the lipoplex workstream, not `06_`.

## Status

*Last reviewed 2026-10-09. Individual cycle documents are the authority on their own status.
check `git log -1 --format=%ad -- <file>` before trusting any date here.*

Workstreams `01`–`05` and `08`–`11` are **complete**. Cycle 3b terminated on 2026-08-31 per its
pre-registration; see [`06_engineering_cycles/cycle3b_physics_rescoring/docs/GATE_VERDICT_BOUND.md`](06_engineering_cycles/cycle3b_physics_rescoring/docs/GATE_VERDICT_BOUND.md)
for the terminal verdict.

**Work has continued since. The full index is in
[`06_engineering_cycles/README.md`](06_engineering_cycles/README.md); the summary is:**

| Cycle | Status |
|---|---|
| **4**: synthesis manufacturability | ✅ **closed.** v4 vendor-rejected (inverted-repeat flanks inherited from wet-lab files); diagnosed, repaired, **v6 accepted and all four constructs ordered** |
| **5**, expression & processing | 📋 pre-registered, awaiting the wet lab's first transfection |
| **7**, affinity-head calibration | ✅ **gate passed** at n=13 (r = 0.805). First calibrated δ/μ number for `YGGFEVVG` |
| **8**, free-energy, first attempt | ❌ **control failed.** Replicates at −3.12 and +5.41 kcal/mol. No value quoted |
| **9**, convergence metric, recalibrated | ✅ **gate passed** (ρ = 1.000) |
| **10**, lipoplex co-packaging | 📋 pre-registered |
| **11**, selectivity QSAR | ❌ **closed negative.** Aggregate r = 0.77, but the prediction is a nearest-neighbour lookup and flips sign under scaffold-grouped CV |
| **12/13**, pose independence | ✅ **closed.** Independent peptide docking reproduced the matched control inside 2.5 Å but not our payload; compared against experimental cryo-EM structures |
| **14** (indexed as **8b**), re-spaced free-energy ladder | ❌ **closed, gates failed.** The diagnosis was right: the overlap gate **passed decisively** (0 of 56 intervals above threshold, against 20 to 21 of 25 on the old ladder). Reproducibility still failed: replicates at **+0.72 ± 3.13** and **+14.47 ± 3.28 kcal/mol**, a 13.75 spread against a combined error of 4.53. Doubling the windows to fix overlap doubled the number of accumulating terms |
| **15**, residue-mutation free energy | ❌ **blocked, then ruled out.** The hybrid residue was built and charge-verified, but the system's standalone topology is incompatible with the mutation toolchain in both directions. The literature check that should have come first settles it anyway: the purpose-built method reports RMSE 1.61 kcal/mol against an effect of 0.81 |
| **16**, conformational constraint | ❌ **control gate failed.** A constrained peptide was indistinguishable from a flexible one, and the most selective peptide was the least turn-like. Diagnosis: five replicates of one system span the whole metric, so 20 ns does not re-equilibrate a bound peptide backbone. Our own payload was **not scored and not run** |

**Four published selectivity methods were assessed and rejected**, each for a documented and
different reason, in [`06_engineering_cycles/cycle11_selectivity_qsar/BINDPRED_REJECTED.md`](06_engineering_cycles/cycle11_selectivity_qsar/BINDPRED_REJECTED.md).
The common cause is not the algorithms: published affinities for these receptors disagree with
each other by more than the effect being measured.

**Prediction ledger: 20 scored, 10 confirmed, 10 falsified.** Every prediction was committed to
this repository before the test that judged it, so the record is checkable against `git log`
rather than taken on trust.

The open questions are now **wet-lab questions**. The computational selectivity question is
closed: every available method's reported error exceeds the 0.81 kcal/mol effect, so the
project's best estimate remains Cycle 7's calibrated **+1.23 ± 1.76 kcal/mol**, whose interval
includes zero. The one dry-lab deliverable still outstanding is the **intranasal dose model**,
which is blocked on a quantitative expression yield from the first transfection.

**What the wet lab should do next**, in order of what unblocks the most: (1) ~~order the four
recoded constructs~~, **done, all four v6 constructs accepted by the vendor and ordered**; order the two anti-MME siRNA duplexes named in [`03_sirna_design/ORDER.md`](03_sirna_design/ORDER.md) by sequence; (2) commission the custom
anti-`YGGFEVVG` polyclonal, nothing downstream can be detected without it; (3) run the
cell-free processing assay in `07_invitro_penk/`, which is where HEK293T's missing convertases
stop being a modelling caveat and start being a measurement; (4) radioligand competition
binding on `YGGFEVVG` and `YGGFDIIG`, since cycle 3b established no computational route ranks
them. Amendments 1–5 in `11_wetlab_protocols/` state each of these as a bench-actionable change.

`07_invitro_penk/` is the first of those wet-lab questions worked up into a benchtop design. It is a **design, not a result**: no experimental data exists yet.

## Licence and citation

Documentation, data, figures and protocols are released under **[CC BY 4.0](LICENSE)**;
source code under the **[MIT Licence](LICENSE-CODE)**. Cite this repository using
[`CITATION.cff`](CITATION.cff). Contribution conventions, in particular the requirement
that predictions are committed before the tests that could falsify them, are in
[`CONTRIBUTING.md`](CONTRIBUTING.md).

## Reproducibility

Coarse-grained MD used **GROMACS 2024.5** with the **MARTINI 2** force field. All-atom membrane MD and MM-GBSA rescoring (cycle 3b) used **GROMACS 2024.5** + **AmberTools**. Sequence work used **Biopython**; siRNA off-target screening used **NCBI BLAST+ (blastn-short)** against human `refseq_rna`. See `methods_references.md` for the complete list with citations. MD input files (`.mdp`, topology) and analysis scripts are under `04_lipoplex_md/` and `06_engineering_cycles/`.

## Caveats: stated by design

> **Lipoplex MD parameters.** The DOTAP / MC3 lipid topologies are **MARTINI-2 analogy models**, not independently validated published parameters. All MD conclusions are **qualitative / comparative** (relative ranking of DNA-condensing tendency across formulations and protonation states), not quantitative binding free energies.

> **Bound-state ΔG must never be quoted without its residency fraction.** Cycle 3b energies are *conditional* on the peptide occupying the pocket: they state how tight the pose is while it exists, not how strong binding is. Three runs have residency < 50% (deltorphin II at μ: 10.7%, 13.6%). The merge tooling refuses to emit a ΔG without its residency, and every downstream consumer must carry both.
