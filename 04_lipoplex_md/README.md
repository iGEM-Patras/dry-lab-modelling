# 04 · Lipoplex coarse-grained MD

MARTINI 2 CG-MD asking whether the ionizable lipid's protonation state controls DNA binding as the delivery design assumes: **weak binding at physiological pH** (neutral, for circulation) vs **strong binding at endosomal pH** (protonated, for cargo condensation).

## System

> **Correction (2026-09-19):** this section previously described the cargo as a "60-bp
> duplex". It is a **30-bp duplex of 60 nucleotides** — base pairs and nucleotides were
> conflated. `dna/frag.fasta` is 30 nt and `polyply --dsdna` pairs it; `dna_cg.gro` has 388
> beads, i.e. 6.47 per nucleotide over 60 nucleotides, which is MARTINI 2's DNA resolution.
> The system's N/P ratio is therefore **2.0**, not 1.0. No result in this directory depends
> on the count — all metrics are per-system comparisons across formulations — but the
> charge ratio does, and Cycle 10's gates were initially derived from the wrong figure.

A **30-bp** CG B-DNA duplex (60 nucleotides, 388 CG beads) + lipid membrane, cationic-lipid 120 : DOPE 80 : cholesterol 40, ~24k CG waters, 150 mM NaCl. Three formulations:

- **DOTAP** — permanent +1 (control for constitutive binding)

The duplex sequence `AAGCGTTACGGTGGTTTCGAGGTCGTCGGT` translates to `KR-YGGFEVVG`: the dibasic
processing site plus the engineered octapeptide, i.e. one cassette of the real construct.
- **MC3-H⁺** (`MC3T`) — ionizable MC3 surrogate, protonated (endosomal-pH state)
- **MC3⁰** (`MC3N`) — same lipid, neutral (physiological-pH state)

**3 independent velocity-seed replicates per formulation** (9 runs), engine **GROMACS 2024.5**.

## Final results (200 ns × 3 seeds, mean ± SEM)

All 9 replicates extended from 50 ns to **200 ns** (each continued from its checkpoint). Metrics computed on the equilibrated second half (100–200 ns), identical pipeline to the 50 ns analysis.

| Formulation | DNA–lipid contacts | Min dist (nm) | RDF peak g(r) | DNA Rg (nm) |
|-------------|-------------------:|--------------:|--------------:|------------:|
| DOTAP | 24.7 ± 5.5 | 0.460 ± 0.003 | 1.54 ± 0.12 | 4.10 ± 0.13 |
| MC3-H⁺ | 34.4 ± 8.6 | 0.469 ± 0.013 | 1.57 ± 0.31 | 4.24 ± 0.07 |
| MC3⁰ | 8.1 ± 4.9 | 1.270 ± 0.563 | 1.04 ± 0.09 | 4.18 ± 0.002 |

**The pH switch is reproduced, and the extension confirms it robustly.** At endosomal pH the protonated ionizable lipid (MC3-H⁺) binds DNA as tightly as the permanent-cation DOTAP (~0.47 nm closest approach); at physiological pH the neutral form (MC3⁰) holds DNA ~1.3 nm away with an RDF peak at the bulk value (~1.0). The extension's key win is convergence: the large 50 ns between-seed spread for MC3-H⁺ (contacts SEM 15.1, min-dist SEM 0.126) **collapsed** at 200 ns (SEM 8.6 and 0.013) — the short run had caught the stochastic nucleation event mid-transient. See `RESULTS_200ns.md` for the full 50→200 ns convergence tables.

### Stage-1 results (50 ns × 3 seeds, mean ± SEM) — superseded

| Formulation | DNA–lipid contacts | Min dist (nm) | DNA Rg (nm) |
|-------------|-------------------:|--------------:|------------:|
| DOTAP | 21.2 ± 6.1 | 0.462 ± 0.005 | 4.00 ± 0.15 |
| MC3-H⁺ | 32.5 ± 15.1 | 0.579 ± 0.126 | 4.34 ± 0.03 |
| MC3⁰ | 9.6 ± 5.2 | 1.340 ± 0.874 | 4.24 ± 0.04 |

At 50 ns cumulative-mean contacts were still rising and the between-seed spread was large — the stochastic nucleation event had not converged, which motivated the 200 ns extension above.

## Layout
```
mdp/            GROMACS run parameters
  prod.mdp          production (per-replicate, dt=1fs, gen-vel per seed)
  prod_r.mdp        replicate production template
  prod_stable.mdp   stable production recipe (dt=1fs, flexible bonds)
  npt_prod.mdp      NPT equilibration
  npt_mc3n.mdp      MC3-neutral equilibration (post charge-swap)
topology/
  sw_MC3N_bonded2.top   MC3-neutral solvated topology (MC3T→MC3N swap, +120 Na)
scripts/
  analyze_replicate.sh  per-replicate analysis (RDF, contacts, mindist, gyration)
data/
  md_replicate_metrics_full.json      per-replicate metrics, 50 ns (all 9)
  md_formulation_summary.json         mean±SEM per formulation, 50 ns
  md_formulation_summary_200ns.json   mean±SEM + per-replicate, 200 ns (final)
  xvg/<FORM>_r<n>/                     raw GROMACS outputs, 50 ns (4 metrics × 9)
  xvg_200ns/<FORM>_r<n>/               raw GROMACS outputs, 200 ns (4 metrics × 9)
figures/
  lipoplex_md_200ns.png            4-panel, final: RDF, contacts, min-dist, convergence
  lipoplex_md_50ns.png             4-panel, Stage-1 (superseded)
RESULTS_200ns.md                   200 ns results + 50→200 ns convergence tables
```

## Analysis method
`analyze_replicate.sh` defines DNA / cation / lipid groups via `gmx select` selection files (avoids shell-quoting issues), then computes: cation–DNA RDF (`gmx rdf`), DNA–lipid contacts within 0.6 nm (`gmx select`), minimum DNA–lipid distance (`gmx mindist`), and DNA radius of gyration (`gmx gyrate`). Reported metrics use the equilibrated second half of each trajectory.

> **Parameter-provenance caveat:** the DOTAP / MC3-H⁺ / MC3⁰ topologies are MARTINI-2 **analogy models** (built from DOPC/DUPC), not independently validated published parameters. Conclusions are qualitative / comparative only. More sampling improves convergence but cannot fix this — it is disclosed by design.
