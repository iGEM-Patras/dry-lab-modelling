# Lipoplex CG-MD — 200 ns extended results

All 9 replicates (3 formulations × 3 seeds) extended from 50 ns to **200 ns**. Metrics computed on the equilibrated second half (100–200 ns), identical pipeline to the original 50 ns analysis. Values are mean ± SEM over 3 seeds.

## Formulation comparison (200 ns)

| Metric | DOTAP (perm. +) | MC3-H⁺ (endosomal) | MC3⁰ (physiol.) |
|---|---|---|---|
| DNA–lipid contacts | 24.7 ± 5.5 | 34.4 ± 8.6 | 8.1 ± 4.9 |
| Min. distance (nm) | 0.460 ± 0.003 | 0.469 ± 0.013 | 1.270 ± 0.563 |
| RDF peak g(r) | 1.543 ± 0.120 | 1.570 ± 0.309 | 1.044 ± 0.089 |
| DNA Rg (nm) | 4.101 ± 0.128 | 4.235 ± 0.065 | 4.175 ± 0.002 |

## 50 ns → 200 ns (convergence)

| Formulation | Contacts 50→200 | Min-dist 50→200 (nm) |
|---|---|---|
| DOTAP (permanent +) | 21.2 ± 6.1 → 24.7 ± 5.5 | 0.462 ± 0.005 → 0.460 ± 0.003 |
| MC3-H⁺ (endosomal pH) | 32.5 ± 15.1 → 34.4 ± 8.6 | 0.579 ± 0.126 → 0.469 ± 0.013 |
| MC3⁰ (physiol. pH) | 9.6 ± 5.2 → 8.1 ± 4.9 | 1.340 ± 0.874 → 1.270 ± 0.563 |

## Interpretation

- **DOTAP** (permanent cationic): strong DNA binding at both lengths (~0.46 nm contact), between-seed SEM tightened on extension — constitutive binding, as expected for a non-titratable lipid.
- **MC3-H⁺** (protonated, endosomal pH ~5–6): the large 50 ns spread (contacts SEM 15.1, min-dist SEM 0.126) **collapsed** at 200 ns (SEM 8.6 and 0.013) — binding is now robustly tight (~0.47 nm), matching DOTAP. The short run had caught nucleation mid-transient; the extension confirms genuine strong binding.
- **MC3⁰** (neutral, physiological pH ~7.4): weak binding throughout — 8.1 contacts, DNA held ~1.27 nm away, RDF peak ~1.0 (bulk). One seed does not bind at all (0.08 contacts, 2.36 nm).

**The pH-switch is reproduced:** the ionizable lipid binds DNA tightly when protonated (endosomal, condensation/protection) and releases it when neutral (physiological, circulation), while the permanent-cationic DOTAP holds on regardless.

> **Caveat:** coarse-grained MARTINI-2 analogy topologies. Conclusions are qualitative and comparative across formulations, not quantitative binding free energies.