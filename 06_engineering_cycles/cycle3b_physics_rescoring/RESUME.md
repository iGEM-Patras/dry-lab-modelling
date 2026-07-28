# Cycle 3b — RESUME HERE

Stopped deliberately at a checkpoint to let compute usage recover. Nothing is
running that needs babysitting; the two build tasks still in the queue will fail
at the same known point (see below) and their expensive output is preserved.

## State

Repo: `90cd66f` + the `build_system.sh` fix in this commit.

| system | pose | packed+parametrized | amide | usable |
|---|---|---|---|---|
| c3b_dtII_DOR | yes | yes (rebuilt) | NHE | needs `--resume` |
| c3b_dtII_MOR | yes | yes | NHE | needs `--resume` |
| c3b_dtI_DOR  | yes | in flight → will exit 2 | NHE | needs `--resume` |
| c3b_dtI_MOR  | yes | yes | NHE | needs `--resume` |
| c3b_em1_DOR  | yes | in flight → will exit 2 | NHE | needs `--resume` |
| c3b_em1_MOR  | yes | yes | NHE | needs `--resume` |
| c3b_menk_DOR | **co-fold ran, pose not located** | no | free acid (correct) | blocked |
| c3b_menk_MOR | **co-fold ran, pose not located** | no | free acid (correct) | blocked |

## The species error, fixed

The benchmark had simulated `YaFEVVG-OH`, the **free acid** — `packmol-memgen
--parametrize` runs tleap, which defaults a bare C-terminus to the charged
carboxylate. That is the same wrong-species error this cycle exists to correct.
`amidate.py` now installs an NHE cap (verified: net charge 0.000 vs −1 for the
acid, tleap Errors=0 Warnings=0, D-centre intact) and `build_system.sh` asserts
NHE is in the final topology. All six rebuilt systems logged
`C-terminus: primary amide (NHE)`. BENCHMARK.md carries a correction notice.

Met-enkephalin is the one control that must stay a free acid — that is its native
form — hence `--no-amidate` for those two.

## Two open failures

**1. `BUILD_EXIT=2` with no error message — diagnosed, fixed in this commit.**
`packmol-memgen` actually *succeeded* (`DONE!`, `bilayer_complex_start_lipid.top`
+ `.crd` on disk). The script died on the very next line:

    PRM=$(ls *_lipid.top *.prmtop *.parm7 2>/dev/null | head -1)

`ls` exits **2** when any operand does not exist, and `set -o pipefail` propagates
that out of the command substitution, so `set -e` kills the script silently. I had
previously misdiagnosed this as a wrong glob pattern and "fixed" it by adding
`*_lipid.top` to the list — which could never work, because `*.prmtop` still fails
to match. Now replaced with a nullglob helper. **Every one of the 6 builds hits
this**, which is why no `system.top` exists yet.

Because the packing is ~30 min of CPU per system and the topology already on disk
is the correct amidated species, `build_system.sh` now takes `--resume` to skip
straight past packing.

**2. Met-enkephalin co-fold produced no structure.** Confirmed by inspection: the
output tree contains `msa/`, `processed/` and `lightning_logs/` but **no
`predictions/` directory whatsoever** — so this is not a filename or path-guessing
problem, Boltz genuinely wrote no model. It nevertheless exited 0, which is why the
job printed `MENK_FOLDS_OK` (the loop only tests the exit status). Investigate the
`menk_17816705.log` prediction stage before resubmitting; a 5-residue peptide
(`YGGFM`) is the shortest chain in the panel, so a minimum-length or MSA-depth
condition is the first thing to check. Separately: I
submitted the menk builds without `--dependency`, so they ran 3 s after submit,
before any pose could exist (`FAIL: no pose`) — use
`sbatch --dependency=afterok:<foldjob>` next time.

## Resume sequence

1. Deploy the fixed `build_system.sh`; confirm `bash -n` passes on the cluster.
2. Resubmit the 6 builds with `--resume` (fast — packing is skipped; expect
   minutes, not 30 min each). Confirm each logs `topology:`,
   `amide verified in final topology`, `Errors = 0`, and writes `system.top`,
   `system.gro`, `index.ndx`, `pepmeta.txt`.
3. Locate the menk poses (`find $W/out_c3b_menk_* -name "*model_0*"`), then build
   those two with `--no-amidate`.
4. Submit the 24 production replicates via `run_prod.sh <tag> <rep> <yes|no>
   <dres_rel|none>` — already written, syntax-checked, not yet run. It re-runs
   NVT+NPT per replicate with a distinct `gen_seed` (independent velocities, so
   the three replicates are genuinely independent), asserts the amide before
   starting, and gates chirality post-NVT / post-NPT / post-production, exiting 3
   to DISCARD an inverted replicate rather than averaging it in.
5. Then the G1/G2/G3 calibration gate. **Stage 2 stays unauthorised until it
   passes** — per the pre-registration, a failed gate terminates the cycle and
   reports a negative methodological result.

Budget unchanged: 71.5 ns/day measured → Stage 1 = 6.7 GPU-days (~3.4 d on 2 GPUs).
