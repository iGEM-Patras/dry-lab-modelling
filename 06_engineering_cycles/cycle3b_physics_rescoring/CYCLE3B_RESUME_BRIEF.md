# Cycle 3b, status 2026-08-27 00:45 CEST

## What happened to array 18122521: disk quota, not science

All 40 tasks FAILED after ~8.5 h each. Signature across the logs:

```
cp: error writing './system.top': Disk quota exceeded
Fatal error: XTC error. This indicates you are out of disk space, or a simulation
with major instabilities resulting in coordinates that are NaN or too large ...
```

GROMACS reports disk exhaustion and numerical blow-up through the **same** error
string. It was disk: a different project of the user's filled `/data`. Confirmed:
`/data` (GPFS `fs1`) now takes 2 GB at 1.1 GB/s, 368 TB free.

**Zero chirality discards, zero mount-race failures.** Both guards from the previous
session behaved. `exit 143` on job `cd089423` was my own `scancel`, expected.

## 35% of the sampling survived and is being reused

22 of 40 replicates hold a valid `prod.cpt` + `prod.tpr`:

| | steps |
|---|---|
| banked in checkpoints | 76.8 M of 220 M (35%) |
| remaining, resume path (22 reps) | 143.2 M |
| remaining, fresh path (18 reps) | 192.6 M |
| **total remaining** | **335.8 M** |
| if restarted from scratch | 428.0 M |

`prod.mdp` has `continuation = yes`, `gen-vel = no`, so `mdrun -cpi prod.cpt`
continues bit-reproducibly: velocities, box, thermostat and barostat state all
travel in the checkpoint. **Resuming saves 22% of total compute.** New script
`scripts/resume_prod.sh` resumes when a checkpoint exists and starts fresh
otherwise; it is idempotent, so a re-queued task never discards banked sampling.

## Disk guard added

`resume_prod.sh` writes and deletes a 3 GB probe file before doing anything else,
and exits 91 if it fails. The old array burned **40 x 8.5 h = 340 core-days** before
noticing the filesystem was full. A full 20 ns replicate needs ~1.1 GB of
trajectory; 40 runs need ~57 GB including `.edr`/`.log`/`.cpt`/`.tpr`.
Also deleted 15 GROMACS `#backup#` files (0.12 GB).

## Now running: split across BOTH partitions

**`pgpu` alone would have been slower than the CPU route**: it has exactly one node
(`binfservas30`, 2 GPUs, already shared with two other users). Measured:

| route | per-replicate | slots | makespan + queue |
|---|---|---|---|
| pgpu, 2 GPUs | 4.1 h @ 124 ns/day | 2 | 2.71 d + 1.0 = **3.71 d** |
| pibu 48c | 20.1 h @ 25.5 ns/day | 20 | 1.50 d + 0.2 = **1.70 d** |
| **both, work-balanced** | | 22 | **1.54 d** |

So both are in flight, split by *remaining* work (longest-first to the fast GPUs):

- **`18170461`**: `pgpu`, array 1-8%2, 8 cores + 1 GPU each, `prod_gpu.txt`.
  The 8 longest tasks (all `c3b_menk_*`, fresh starts, 10.7 M steps each).
- **`18170462`**: `pibu_el8`, array 1-32%20, 48 cores (12 ranks x 4 threads),
  `prod_cpu.txt`. 4 running at last check; 15 nodes currently have >=48 free cores
  so the remaining slots fill as tasks land.

Logs: `logs/gpu_18170461_<task>.out`, `logs/cpu_18170462_<task>.out`.
Verified in the live logs: correct rank topology, `FRESH START` on uncheckpointed
reps, no `FATAL`, disk guard silent.

## Next actions

1. `grep -l PROD_OK logs/{gpu,cpu}_1817046*_*.out | wc -l` should reach 40.
   Exit 4 = `INCOMPLETE`, safe to resubmit (it resumes). Exit 3 = **chirality
   inverted, discard that replicate, do not blindly rerun.** Exit 91 = disk.
2. **MM-GBSA rescoring still unvalidated on CPU.** `rescore_smoke.sh` is a byte-copy
   of `rescore.sh` including the >=90-frame guard, so it cannot validate against the
   old 21-frame pilots. Once a real 20 ns trajectory exists: run `rescore.sh <tag>
   <rep>` on **one** replicate, confirm `results_stage1.csv` gains a row, then fan
   out. GB solvation needs no GPU.
3. `collect_dg.py` -> ddG_sel per peptide pair with n=5 error bars.

## Facts worth keeping

- **`/home` is separately and nearly full**: 20381M of 20480M quota (99.5%). Top
  consumers `reference/` 5.5 G, `myenv/` 2.3 G, `ubelix_transfer_bundle.tar.gz`
  1.9 G. Nothing in the campaign writes there, but it will bite something else.
- 128-core exclusive requests never schedule on `pibu_el8` (nodes sit ~120/128 free).
  48 cores schedules promptly. Walltime does not affect the start estimate.
- Rank counts must stay composite: PME splitting must leave a PP count that
  factorises into a 3D grid (12 -> PP 8 or 9 fine; 30 -> PP 22 = 2x11 aborts).
- `pgpu` is one node, 2 GPUs, shared. Do not assume it is the fast route.
