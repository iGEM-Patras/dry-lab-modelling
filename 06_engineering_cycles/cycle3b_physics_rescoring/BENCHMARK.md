# Cycle 3b: Stage 1 benchmark: measured, not estimated

Benchmark system: **c3b_dtII_DOR** (deltorphin II co-folded into DOR, embedded in a
POPC bilayer.

> **CORRECTION.** This benchmark ran the **free acid** (`YaFEVVG-OH`), not the amide.
> An earlier version of this file claimed the system "carries both the non-standard
> D-centre and the C-terminal amide" (the D-centre was installed and verified, but
> the amide was **not**: `packmol-memgen --parametrize` runs `tleap`, which defaults a
> bare C-terminus to the charged free acid, and nothing in the pipeline installed an
> NHE cap. The gate's own output shows it: the peptide was read as 7 residues ending
> in GLY, with no NHE.
>
> This is the same wrong-species error that Cycle 3b was created to correct,
> reproduced in the MD stage. It matters quantitatively: the free acid carries an
> extra **−1 charge on the pharmacophore that sets δ-selectivity** (verified NHE net
> charge 0.000 vs −1 for the acid), so a calibration built on it would be measuring
> the wrong molecule.
>
> **The timings and throughput below remain valid** (the amide adds 4 atoms to a
> 270,287-atom system, which does not change ns/day. The *chemistry* of this
> particular run does not, and it is not used for calibration. `amidate.py` now
> installs the cap, `build_system.sh` calls it by default, and the final topology is
> asserted to contain NHE. All Stage 1 systems are being rebuilt as the correct
> species.

## System (verified, not assumed)

| quantity | value |
|---|---|
| total atoms | 270,287 |
| POPC lipids | 531 (Lipid21-split into 531 PC + 531 OL + 531 PA residues) |
| TIP3P waters | 64,312 |
| ions | 161 Na+ / 173 Cl- (net neutral) |
| box | 145.1 x 144.4 x 156.3 A |
| receptor | 372 residues |
| peptide | 7 residues, 108 atoms, located by bonded-topology walk |
| tleap | **Errors = 0**, Warnings = 1067 (all expected lipid-splitting messages) |

## Measured timings

| stage | measured | hardware |
|---|---|---|
| co-fold (6 controls) | 26 min total, ~4.3 min each | RTX 2080 Ti |
| membrane build | 61 min per system | CPU (`pshort_el8`) |
| min + NVT 200 ps + NPT 1 ns | 37.4 min per system | RTX 2080 Ti |
| **production throughput** | **71.5 ns/day** | RTX 2080 Ti, 2 fs step |

## Budget: replaces the pre-registered guess

The pre-registration used a literature-typical ~10 ns/day for a system of this size.
The measured rate is **7.2x faster**, which changes the affordability conclusion:

| campaign | runs | GPU-days | wall-clock on 2 GPUs |
|---|---|---|---|
| Stage 1 gate (4 controls x 2 receptors x 3 reps) | 24 | 6.7 | 3.4 d |
| Stage 2 designs (5 x 2 receptors x 3 reps) | 30 | 8.4 | 4.2 d |
| both stages | 54 | **15.1** | 7.6 d |

Pre-registered estimate was 108 GPU-days for both stages; measured is 15.1.
**The 20 ns x 3-replicate design does not need trimming.**

Equilibration adds 0.62 GPU-days across 24 Stage-1 runs. Builds are CPU-only and
parallelise across the 5 idle `pshort_el8` nodes.

## Chirality gate: passed at every stage

The D-centre is measured as the signed improper volume
V = (N-CA) . [(C-CA) x (CB-CA)]; V < 0 is D, V > 0 is L.

| checkpoint | V | verdict |
|---|---|---|
| after co-fold + mirror (build) | -2.504 | D installed |
| after minimisation | -2.389 | D retained |
| after NPT equilibration | -2.156 | D retained |

This matters because **ff14SB is enantiomer-blind by construction**, no improper term
references the sp3 alpha-carbon type, so the force field cannot itself notice an
inversion. `test_chirality.sh` (8/8 passing locally and on the cluster) guards the
assertion itself.

## Bugs the assertions caught (rather than bad numbers reaching a result)

1. `*.prmtop` glob: `packmol-memgen --parametrize` writes `<input>_lipid.top/.crd`, so a
   successful 61-min build reported `EXIT=2`.
2. `tc-grps = Water_and_ions`: that group does not exist on this system; Lipid21 yields
   separate PA/PC/OL groups. Caught before `grompp`.
3. Selecting index groups by NUMBER: `make_ndx` emits more than 19 default groups here
   (20 is already `non-Water`), so `name 20 MEMB` silently renamed the wrong group. The
   partition assertion (Protein + MEMB + SOLV == System) refused it. Replaced by
   `make_index.py`, which writes groups from residue identity.
4. Chirality gate index: a peptide-relative index applied to the whole system first hit
   the receptor's CB-less residue 2, then an Na+ ion (because `editconf` does not preserve
   the topology's solvent ordering). Gate now extracts the peptide via `system.top`.
5. PDB atom-serial overflow: at 270,287 atoms a PDB cannot be parsed
   (`Coordinate mismatch in model 1`); the gate reads `.gro` instead.

Each of these would have been invisible in a pipeline without assertions: three would
have produced a plausible-looking trajectory of the wrong system.
