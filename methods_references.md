# Methods & References — PENK Dry-Lab Modelling (iGEM Patras)

This file records every tool, force field, database, parameter, and published
rule used in the computational work, so the methods section is fully traceable.

## Software & versions
- **GROMACS 2024.5** (conda-forge build, CUDA 11.8), MD engine.
  Abraham MJ et al. (2015) *SoftwareX* 1–2:19–25. doi:10.1016/j.softx.2015.06.001
- **Biopython** (SeqIO / Seq) for sequence parsing & translation.
  Cock PJA et al. (2009) *Bioinformatics* 25(11):1422–3. doi:10.1093/bioinformatics/btp163
- **NCBI BLAST+ / URLAPI** (blastn-short) for siRNA off-target screening.
  Camacho C et al. (2009) *BMC Bioinformatics* 10:421. doi:10.1186/1471-2105-10-421

## Databases
- **NCBI RefSeq** — human MME mRNA variants NM_000902.5, NM_007287, NM_007288,
  NM_007289 (all share identical 2,253-bp CDS). O'Leary NA et al. (2016)
  *Nucleic Acids Res* 44:D733–45. doi:10.1093/nar/gkv1189
- **UniProt P08473** — human neprilysin (MME) protein reference.
- Off-target DB: NCBI **refseq_rna**, restricted to *Homo sapiens* (txid9606).

## siRNA design rules
- **Reynolds et al. (2004)** *Nat Biotechnol* 22(3):326–30 — rational siRNA
  sequence criteria (GC 30–52%, positional base preferences, low internal
  stability at guide 5' end). doi:10.1038/nbt936
- **Ui-Tei et al. (2004)** *Nucleic Acids Res* 32(3):936–48 — guide 5'
  A/U, 3' G/C, GC-stretch ≤9 rule. doi:10.1093/nar/gkh247
- **Khvorova/Schwarz asymmetry** — thermodynamic duplex-end asymmetry favours
  guide-strand RISC loading. Schwarz DS et al. (2003) *Cell* 115:199–208;
  Khvorova A et al. (2003) *Cell* 115:209–16.
- Nearest-neighbour RNA ΔG parameters: **Turner & Mathews (2010)** / Xia et al.
  (1998) *Biochemistry* 37:14719–35 (NN free-energy set).
- 3' **dTdT overhangs**, 19+2 format: Elbashir SM et al. (2001) *Nature*
  411:494–8. doi:10.1038/35078107

## Coarse-grained MD (lipoplex)
- **MARTINI 2** force field (v2.1 for DNA, v2.0 for lipids/cholesterol).
  - Marrink SJ et al. (2007) *J Phys Chem B* 111:7812–24 (MARTINI 2.0 lipids).
    doi:10.1021/jp071097f
  - Monticelli L et al. (2008) *J Chem Theory Comput* 4:819–34 (MARTINI proteins) —
    cited for provenance of the shared bead-type table only. **No protein is present in
    any coarse-grained system here**; `martini_v2.2.itp` is not included by any topology.
    See [`04_lipoplex_md/FORCE_FIELD_AUDIT.md`](04_lipoplex_md/FORCE_FIELD_AUDIT.md).
  - **martini_v2.1-dna**: Uusitalo JJ et al. (2015) *J Chem Theory Comput*
    11:3932–45 — MARTINI DNA. doi:10.1021/acs.jctc.5b00286
- **Lipid models (analogy parameters, this project):**
  - **DOTAP** — permanent +1 quaternary-ammonium head; built by analogy to
    MARTINI DOPC (head Q0 +1, phosphate removed). NOT an independently validated
    parameter set; documented as an analogy model in DOTAP.itp header.
  - **MC3T** — ionizable DLin-MC3-DMA-type surrogate, PROTONATED (+1, Qd head),
    di-linoleyl tails (DUPC architecture). Endosomal-pH (~5–6) state.
  - **MC3N** — neutral reference (P4, charge 0 head) = physiological-pH (7.4)
    state of the same lipid. Both are MARTINI-2 analogy models (MC3.itp header),
    NOT the published validated DLin-MC3-DMA parameters.
    Reference chemistry: Jayaraman M et al. (2012) *Angew Chem* 51:8529–33
    (DLin-MC3-DMA); pKa ~6.4.
- **System composition** (each box): 1 × 60-bp CG B-DNA duplex, cationic lipid
  120 : DOPE 80 : cholesterol 40, ~23,900 MARTINI waters, 150 mM NaCl
  (NA 370 / CL 432 for MC3-protonated; neutralising counts per formulation).
- **Simulation protocol:** reaction-field electrostatics (epsilon_r=15,
  rcoulomb=rvdw=1.1 nm), v-rescale thermostat (ref-T 310 K, tau-t 1.0 ps),
  c-rescale/berendsen barostat (ref-P 1 bar). Production: prod_stable.mdp,
  dt = 1 fs with -DFLEXIBLE (chosen for numerical stability of this system),
  50 ns per run. EM (steep) → NVT → NPT equilibration → production.
- **Analysis (GROMACS tools):** gmx rdf (cation–DNA RDF, 0.02 nm bins),
  gmx mindist (DNA–lipid min distance & contact count, 0.6 nm cutoff),
  gmx gyrate (DNA / complex radius of gyration), gmx clustsize (aggregation).

## Replicate campaign (this step)
- 3 formulations × 3 independent replicates = 9 production runs.
- **MC3-neutral system build:** MC3T->MC3N swap removes the +120 lipid head
  charge, so the box net charge becomes -120. Re-neutralized with genion
  (+120 Na, replacing 120 waters -> W 23,814 / NA 490 / CL 432), energy-
  minimized (steep, final |F| ~ 7.1 kJ/mol/nm), then 2 ns NPT equilibration
  (dt = 1 fs, fresh velocities) from the protonated-MC3 equilibrated box.
  Stability note: production and equilibration use -DFLEXIBLE (flexible bonds
  replace constraints), which requires dt = 1 fs; a dt = 2 fs trial with
  flexible bonds diverges (bond energy -> 1e11 kJ/mol).
- Replicates differ by random velocity-generation seed (gen-vel = yes,
  gen-seed = distinct per replicate) from the shared equilibrated NPT
  structure — standard practice for independent CG-MD replicates to estimate
  statistical uncertainty (mean ± SEM across replicates).

## Robustness & convergence (iGEM Best Model)
- **Two-stage sampling:** (1) 50 ns × 3 replicates × 3 formulations as an initial
  comparative screen and convergence checkpoint; (2) extension of each replicate
  from its checkpoint to 200 ns (~800 ns effective at MARTINI's ~4× speedup) to
  demonstrate convergence of the contact/RDF metrics.
- **Convergence diagnostics:** block averaging (Flyvbjerg-Petersen block-error),
  running-mean of contact number and cation-DNA coordination, and comparison of
  first-half vs second-half metric means per replicate. Reported alongside
  between-replicate SEM.
- **Statistical treatment:** each metric reported as mean ± SEM across the 3
  independent-seed replicates; formulations compared by non-overlap of SEM
  intervals (and effect size), not single-trajectory values.
- **Explicit parameter-provenance caveat (stated in results):** the DOTAP, MC3T,
  and MC3N lipid topologies are MARTINI-2 *analogy* models built from DOPC/DUPC,
  NOT independently validated published parameters (per each .itp header).
  Consequently all conclusions are **qualitative/comparative** (relative ranking
  of DNA-condensing tendency across formulations and protonation states), not
  quantitative binding free energies. Extending sampling does not remove this
  limitation — it is a parameter-provenance issue, disclosed by design.

## MD results — 50 ns stage (n=3 seeds/formulation)
- Metrics (mean ± SEM, equilibrated 2nd half): analysis groups defined via
  `gmx select` selection FILE with semicolons + a `"System" all` group (required
  by trjconv). Cation resname per system: DOTAP / MC3T (protonated) / MC3N (neutral).
  - DNA–lipid contacts (beads within 0.6 nm): DOTAP 21.2±6.1, MC3-H⁺ 32.5±15.1, MC3⁰ 9.6±5.2
  - min DNA–lipid distance (nm): DOTAP 0.462±0.005, MC3-H⁺ 0.579±0.126, MC3⁰ 1.340±0.874
  - DNA Rg (nm): DOTAP 4.00±0.15, MC3-H⁺ 4.34±0.03, MC3⁰ 4.24±0.04
- **pH-switch signature reproduced qualitatively:** protonated MC3 binds DNA
  strongly; neutral MC3 does not reliably bind (one seed stayed 3.09 nm away,
  zero contacts). DOTAP (permanent cation) binds most reproducibly.
- **Convergence diagnostic (decisive):** cumulative-mean contacts still RISING at
  50 ns in most seeds (1st-half→2nd-half drift up to +200%). Within-replicate
  block-averaged SE is small (0.7–4.2), so the large between-seed SEM reflects
  incomplete SAMPLING of the binding/nucleation event, not thermal noise.
  → motivates the 200 ns extension (jobs 6fcf036f DOTAP / b2da9b07 MC3P /
  82ab2b2b MC3N, convert-tpr -extend 150000, mdrun -cpi from checkpoint).
- Figure: lipoplex_md_50ns.png (RDF+spread, contacts, min-dist, convergence).
- Data pulled from cluster via base64 tar (harvest layer unreliable for large files).

## Plasmid audit
- Reference: native human proenkephalin **UniProt P01210** (267 aa).
- Cassette backbone: pcDNA3.1-type (CMV, T7, bGH polyA, NeoR/KanR, AmpR, f1/SV40 ori).
- Restriction enzymes: AflII, XbaI, NcoI (recognition sites per REBASE).
  Roberts RJ et al. (2015) *Nucleic Acids Res* 43:D298–9 (REBASE).
