# 04 · Lipoplex coarse-grained MD

MARTINI 2 CG-MD asking whether the ionizable lipid's protonation state controls DNA binding as the delivery design assumes: **weak binding at physiological pH** (neutral, for circulation) vs **strong binding at endosomal pH** (protonated, for cargo condensation).

## System
A 60-bp CG B-DNA duplex + lipid membrane, cationic-lipid 120 : DOPE 80 : cholesterol 40, ~24k CG waters, 150 mM NaCl. Three formulations:

- **DOTAP** — permanent +1 (control for constitutive binding)
- **MC3-H⁺** (`MC3T`) — ionizable MC3 surrogate, protonated (endosomal-pH state)
- **MC3⁰** (`MC3N`) — same lipid, neutral (physiological-pH state)

**3 independent velocity-seed replicates per formulation** (9 runs), engine **GROMACS 2024.5**.

## Stage-1 results (50 ns × 3 seeds, mean ± SEM)

| Formulation | DNA–lipid contacts | Min dist (nm) | DNA Rg (nm) |
|-------------|-------------------:|--------------:|------------:|
| DOTAP | 21.2 ± 6.1 | 0.462 ± 0.005 | 4.00 ± 0.15 |
| MC3-H⁺ | 32.5 ± 15.1 | 0.579 ± 0.126 | 4.34 ± 0.03 |
| MC3⁰ | 9.6 ± 5.2 | 1.340 ± 0.874 | 4.24 ± 0.04 |

The **pH switch is reproduced qualitatively**. The large between-seed spread is not noise: within-replicate block errors are small (0.7–4.2), while cumulative-mean contacts are **still rising at 50 ns** — binding is a stochastic nucleation event that has not converged. This is the quantitative justification for the **200 ns extension** (running).

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
  md_replicate_metrics_full.json   per-replicate metrics (all 9)
  md_formulation_summary.json      mean±SEM per formulation
  xvg/<FORM>_r<n>/                 raw GROMACS outputs (4 metrics × 9 replicates)
figures/
  lipoplex_md_50ns.png             4-panel: RDF, contacts, min-dist, convergence
```

## Analysis method
`analyze_replicate.sh` defines DNA / cation / lipid groups via `gmx select` selection files (avoids shell-quoting issues), then computes: cation–DNA RDF (`gmx rdf`), DNA–lipid contacts within 0.6 nm (`gmx select`), minimum DNA–lipid distance (`gmx mindist`), and DNA radius of gyration (`gmx gyrate`). Reported metrics use the equilibrated second half of each trajectory.

> **Parameter-provenance caveat:** the DOTAP / MC3-H⁺ / MC3⁰ topologies are MARTINI-2 **analogy models** (built from DOPC/DUPC), not independently validated published parameters. Conclusions are qualitative / comparative only. More sampling improves convergence but cannot fix this — it is disclosed by design.
