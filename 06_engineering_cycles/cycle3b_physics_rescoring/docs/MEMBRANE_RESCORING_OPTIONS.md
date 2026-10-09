# Implicit membrane for the escaped deltorphin/mu replicates: what is and is not possible

**Question:** can we recover MM-GBSA energies for the 9 replicates the membrane gate
refused (deltorphin I at mu 3/5, deltorphin II at mu 4/5, endomorphin-1 at delta 1/5)?

## Finding: `memopt` is PB-only in gmx_MMPBSA 1.5.0.3

Read from `GMXMMPBSA/input_parser.py` in the installed environment. The implicit-membrane
keywords are registered on the **`&pb`** namelist exclusively:

    input_file.addNamelist('pb', 'pb', [
        ...
        ['memopt',   int,   0,    'Use PB optimization for membrane'],
        ['mprob',    float, 2.70, 'Membrane probe radius in A'],
        ['mthick',   float, 40.0, 'Membrane thickness'],
        ['mctrdz',   float, 0.0,  'Distance to offset membrane in Z direction'],
        ['poretype', int,   1,    'Use exclusion region for channel proteins'],
    ])

The `&gb` namelist (trigger `gbrun`) has no membrane option. There is no implicit-membrane
Generalised Born model available here.

## Consequence

Switching the escaped runs to PB+memopt would make them **incommensurable with the 31 GB
results already computed.** GB and PB effective energies differ systematically in both
magnitude and, for charged ligands, sometimes in rank order. A ddG built from a GB delta arm
and a PB mu arm is not a ddG of anything.

Making the comparison valid via PB would require **re-running all 40 replicates in PB with
memopt**, at substantially higher cost per frame than GB, and would invalidate the
already-passed validation of the GB path.

## Chosen route instead: bound-frame-restricted GB

The reason those runs were refused is not a solvation-model deficiency. It is that the
peptide **is not in the binding site for much of the window** (deltorphin II rep3 spends
99.8% of frames touching lipid. A binding energy averaged over frames where the ligand has
left the pocket is not a binding energy under any solvation model.

So the defensible estimate is the **conditional bound-state energy**: restrict the scoring
window to frames where the peptide is genuinely in the pocket, and score those with the
*same validated GB protocol* used for every other arm. This keeps all 40 numbers on one
scale, and it splits the observable honestly into two reportable parts:

1. **residency**: what fraction of the trajectory the peptide stays bound (already measured
   for all 40 runs);
2. **conditional dG_bind**: how tightly it binds while it is bound.

Neither is the whole story alone; together they are.

## Bound-frame criterion

A frame is *bound* when **both** hold:

- minimum ligand-lipid distance > 0.4 nm (no bilayer contact), and
- ligand RMSD from the docked pose (receptor-superposed) below the per-system threshold.

Both are computed for every frame of all 40 production trajectories by
`scripts/classify_frames.sbatch`.

## Honest limitation

A conditional estimate is conditioned on a state the peptide occupies only part of the time,
and the frames selected are not an unbiased sample of that state. It must always be reported
**with** the residency figure, never as a standalone affinity proxy. It answers "how tight is
the bound pose when it exists", not "how strong is the binding".
