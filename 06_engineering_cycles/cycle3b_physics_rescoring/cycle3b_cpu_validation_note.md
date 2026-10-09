# Cycle 3b: pipeline validation on CPU, and a disarmed-gate defect

**Date:** 14 August 2026 · **CPU job:** 17985511 (`pibu_el8`, node binfservas28, RUNNING)
**GPU twin:** 17974162 (`pgpu`, PENDING, reserved 15 Aug)

## Why a CPU job

`pgpu` has 2 GPUs and one was free, but the partition is reserved for
`afreiberg`'s array `17963664_[3-30]` (28 tasks × 5-day walltime, **CPU-only**)
(`gres=N/A`). Higher priority, so Slurm holds the node. Our `Reason=Priority`
was that reservation, not a GPU shortage.

Backfill (`sched/backfill`) could not slot us in because the job requests
**3 hours** for work that comparable runs finish in 8–17 min.

`pibu_el8` had ~880 idle CPUs and no contention, so the validation was rerouted
there instead of waiting two days.

## What had to change

All three `mdrun` calls in `scripts/run_prod.sh` hardcode `-nb gpu`, and `$GMX`
is a CUDA build (`envs/gmxcuda`, GPU support: CUDA). A CUDA-compiled GROMACS runs
fine on CPU, but only if `-nb cpu` is passed: env vars alone would have failed at
the first `mdrun`. There is no override hook, so:

- `scripts/run_prod_cpu.sh`, derived by `sed` from `run_prod.sh`. **Exactly 3 lines
  differ** (`diff` verified); `-nb gpu -ntmpi 1 -ntomp 8` → `-nb cpu -ntmpi ${GMX_NTMPI:-4}
  -ntomp ${GMX_NTOMP:-8}`. Original untouched, backed up at `scripts/.run_prod.sh.bak`.
- Runs as **rep99**, so it does not collide with the GPU twin's rep1. Both can run
  concurrently; the seed derives from the replicate number, giving an independent
  equilibration.
- **24 h walltime**, not 90 min: only *production* is truncated by `PROD_NSTEPS`.
  NVT (200 ps) and NPT (1 ns) run full length, 1.4 ns of 155,234-atom all-atom MD
  on CPU. A `pshort_el8` submission would have been killed mid-NPT.

## The defect worth keeping

`run_pipeline_validate.sh` line 18 calls:

    PROD_NSTEPS=100000 bash scripts/run_prod.sh c3b_dtII_DOR 1

Two positional arguments. `run_prod.sh` defaults `DRES_REL="${4:-none}"`, and
`gate()` begins:

    if [ "$DRES_ABS" = "none" ]; then echo "  [gate:$stage] no D-residue, skipped"; return 0; fi

So the job that claims to "exercise NVT -> NPT -> prod -> **all 3 chirality
gates**" skips all three. It would have reported the pipeline validated with its
stereochemical safety checks disarmed.

This is the same defect class `scripts/peptide_spec.sh` documents costing a full
build on 2026-07-30: the `c3b_dtII_DOR` pilot was built with `dres=none`, producing
the **all-L analogue** of deltorphin II, and nothing flagged it, because the gate
that would catch it is itself skipped when `DRES_REL=none`. Deltorphin II's
δ-selectivity rests entirely on that D-Ala².

`run_prod_job.sh` was already fixed to read chemistry from the design table.
`run_pipeline_validate.sh` was not.

The CPU wrapper reads the table instead of defaulting: `prod_all.txt` gives
`c3b_dtII_DOR 1 yes 2`, `chem.txt` records `BUILT_DRES=2`, the two are
cross-checked, and `dres=none` is a hard failure. Log confirms:

      spec[c3b_dtII_DOR]: dres=2 amide=yes  (from prod_all.txt)
      build/run chemistry agree: dres=2 amide=yes
      chirality gates ARMED on D-residue 2
      D-centre: peptide residue 2 -> absolute 374

## Recommended follow-up

Patch `run_pipeline_validate.sh` to source `peptide_spec.sh` the way
`run_prod_job.sh` does, so the GPU twin does not validate with skipped gates when
it eventually starts. Until then, **the GPU job's result should not be read as a
gate validation**, only the CPU run exercises them.

## Patch applied, 14 August 2026

`run_pipeline_validate.sh` now reads chemistry from the design table instead of
letting `run_prod.sh` default it. Two changes only (see `run_pipeline_validate.patch`):

1. A chemistry block spliced after `cd $W`: sources `scripts/peptide_spec.sh`,
   calls `load_peptide_spec c3b_dtII_DOR`, requires `chem.txt`, cross-checks
   `BUILT_DRES`/`BUILT_AMIDE` against `SPEC_DRES`/`SPEC_AMIDE`, and hard-fails on
   `dres=none` with the reason that it would skip all three gates.
2. Line 18 now passes four arguments:
   `bash scripts/run_prod.sh c3b_dtII_DOR 1 "$SPEC_AMIDE" "$SPEC_DRES"`

Original preserved at `.run_pipeline_validate.sh.bak`
(md5 `8b8e66d9d6099009fc8712da49a80887`; patched `a8a56ce49f57f486521547ccafd863ec`).

Tested before installing: the block resolves `dres=2 amide=yes` and prints
`chirality gates ARMED on D-residue 2`; an unknown tag exits 1 with
"refusing to default to all-L" rather than proceeding.

### The patch alone was not enough

**Slurm spools the batch script at submission.** Job 17974162 held the unpatched
two-argument copy, verified with `scontrol write batch_script`, so editing the
file on disk would not have reached it. It would still have run with all three
gates skipped, and its log would have read as a pass.

Cancelled and resubmitted as **17985540**. Its spooled copy was verified to carry
the patch (line 48 passes all four arguments). Still `Reason=Priority`, estimated
start 15 Aug, behind the same CPU-only array.

Anyone patching a script for an already-queued job must requeue it; the on-disk
file governs only future submissions.

## Both jobs COMPLETED, 14 August 2026

| Job | Route | Node | Elapsed | Walltime | Exit |
|---|---|---|---|---|---|
| `17985540` | GPU, `pgpu` | binfservas30 | 00:21:37 | 3:00:00 | 0:0 |
| `17985511` | CPU, `pibu_el8` | binfservas28 | 05:43:27 | 1-00:00:00 | 0:0 |

The GPU job did not wait until 15 Aug: it started and finished the same morning,
so the requeue cost nothing.

### The patched gates fired, on both routes

Both logs are identical on every gate marker:

```
spec[c3b_dtII_DOR]: dres=2 amide=yes  (from prod_all.txt)
build/run chemistry agree: dres=2 amide=yes
chirality gates ARMED on D-residue 2
D-centre: peptide residue 2 -> absolute 374
[gate:post-NVT] chirality OK
[gate:post-NPT] chirality OK
[gate:post-production] chirality OK
PROD_OK / RUN_PROD_EXIT=0
RESCORE_EXIT=3 (expected 3 = correctly refused)  GUARD_OK
```

So the patch did what it was for: chemistry is resolved from `prod_all.txt`, checked
against `chem.txt`, and all three stereochemistry gates ran on the correct residue.
The truncation guard also refused the short run with the distinct exit code 3.
Seeds differed as intended (rep1 20262587, rep99 20360587).

### Finding: the MM-GBSA scoring stage has never been executed

`RESCORE_PATHTEST_EXIT=2` is not a flake, it is structural, and it means
`gmx_MMPBSA` has still never run in this pipeline. Confirmed by grep: no
`gmx_MMPBSA`, `FINAL_RESULTS`, or `DELTA TOTAL` in either log, and no
`*_FINAL.dat` / `*_perframe.csv` in either replicate directory.

Cause, from `scripts/prod.mdp` and `scripts/rescore.sh`:

- `nstxout-compressed = 5000` at `dt = 0.002` → one frame per **10 ps**.
- `rescore.sh` requires **≥90 frames** in its scoring window (correctly, it refuses
  to score a crashed run on thin sampling).
- A 200 ps validation production can yield at most
  **21 frames**. It needs ≥0.9 ns just to clear the gate.

The validation therefore cannot reach the scoring stage by construction, no matter
how many times it is run. Everything downstream of that gate is still unexercised:
`make_mmgbsa_groups.py`, the Receptor/Ligand index derivation, the five mid-window
chirality checkpoints, `gmx_MMPBSA` itself, and `collect_dg.py`.

### Second hazard, in the same area

`collect_dg.py` appends `control,receptor,rep,avg` to `results_stage1.csv` and records
**nothing about run length or truncation**. If the guard were ever bypassed on a short
run that did clear the frame gate, the resulting row would be indistinguishable from
production. `results_stage1.csv` does not exist yet, so nothing is polluted today, but
any MM-GBSA smoke test must be pointed at a scratch results file, not the real one.

### Runtime model (validated against measured elapsed)

Predicted vs measured for the 1.4 ns validation: GPU 0.29 h vs
0.36 h measured; CPU 5.67 h vs 5.72 h.
Per-stage GPU speedup: NVT 12.8×, NPT 23.2×,
production 12.1×.

Extrapolated to a full replicate (0.2 ns NVT + 1 ns NPT + 20 ns production):
**4.13 h on GPU, 52.08 h on CPU**. For the 24 replicates in
`prod_all.txt`: **~99.1 GPU-hours, or ~52.1 days of
serial CPU time.** The campaign is GPU-bound; the CPU route is a correctness twin, not
a production path.

## Defect found while staging the smoke test: 14 August 2026

`run_pipeline_validate.sh` line 60 (and the CPU variant's line 62) does:

```
rm -f systems/c3b_dtII_DOR/rep1/TRUNCATED_NOT_FOR_ANALYSIS
bash scripts/rescore.sh c3b_dtII_DOR 1
```

**`rep1` is a production slot** (`prod_all.txt` plans reps 1, 2, 3 for every system.
The path test therefore stripped the truncation guard from a real replicate directory
and left it that way. Verified after the runs: `rep1` held a 21-frame (200 ps)
trajectory with the marker **ABSENT**. The only thing that stopped it being scored as
production was the ≥90-frame gate downstream, a second line of defence, not the one
that was supposed to catch this.

Re-armed by hand:

```
PROD_NSTEPS=100000  truncated=yes  re-armed by audit 2026-08-14T17:26:13+02:00 -- path test
```

Before rep1/rep2/rep3 are run for real, that directory must be deleted, not reused:
its NVT/NPT/prod files came from a truncated run with a different seed.

**Fix for the validation scripts:** point the path test at a scratch rep number, never
a planned one. The smoke test below uses `rep777` for exactly this reason.

## MM-GBSA reachability smoke test: job 18005610 (staged)

The cheapest run that reaches `gmx_MMPBSA`: **1 ns production = 500000 steps**, giving
~101 frames against the ≥90 gate (`prod.mdp` emits one frame per 10 ps).

Staged as `run_smoke_mmgbsa.sh`, SBATCH header inherited from the validated
`run_pipeline_validate.sh` (pgpu, 1 GPU, 8 cpus, 32G) with only job-name, `--time=02:00:00`,
and output path changed. Sequence:

1. Chemistry resolved from `prod_all.txt` and cross-checked against `chem.txt` (same
   block as the patch), gates ARMED on D-residue 2.
2. 1 ns production into **scratch `rep777`** (cannot collide with planned reps 1-3).
3. Frame count read back from `prod.xtc`.
4. `rescore_smoke.sh` called with the marker in place, must exit 3 (guard still works).
5. Marker cleared **on the scratch rep only**, then rescored for real: expect exit 0,
   `gmx_MMPBSA` reached, `make_mmgbsa_groups.py` + the five mid-window chirality
   checkpoints + `collect_dg.py` all exercised for the first time.

`scripts/rescore_smoke.sh` differs from `rescore.sh` in **two lines only**, both the
results target (`results_smoke_rep777.csv` instead of `results_stage1.csv`), see
`rescore_smoke.diff`. This matters because `collect_dg.py` records no run-length field,
so a smoke row in the real results file would be indistinguishable from production.

Pre-flight checks before submitting: `gmx_MMPBSA v1.5.0.3` runs (`--version` exit 0);
the guard exits 2 (not a crash) on an absent rep; all six inputs `run_prod.sh` needs
are present in `systems/c3b_dtII_DOR/`; `rep777` did not already exist; 364 T free on
`/data`; `results_stage1.csv` still does not exist, so nothing is polluted.

Spooled script verified to carry `PROD_NSTEPS=500000` and rep `777` after submission.
