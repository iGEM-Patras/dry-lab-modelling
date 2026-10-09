# Cycle 3b: resume state, 2026-08-12

Supplements `RESUME.md`. Nothing here changes the science; it records where the
work physically is and one dispatch failure mode that cost a day.

## Jobs in flight

| job | what | dir | limit |
|---|---|---|---|
| `17959496` | Stage-1 **benchmark**, `c3b_dtII_DOR` rep 1 | `cycle3b/` | 8 h |
| `17960676` | 4 enkephalin co-folds (`DOR/MOR × Met/Leu`) | `boltz_dock/enk_cofold/` | 4 h |

Both `PENDING (Priority)`. `pgpu` is a **single node**, both GPUs allocated, and
an unrelated 9-day job of ours (`17958523`, `PRJNA845531_run`) holds it. Neither
job competes with the other; both wait on partition capacity. This is a
scheduling constraint, not a defect: do not "fix" it by editing the scripts.

## Dispatch failure that must not be repeated

Job `17958370` (the first co-fold attempt) shows `CANCELLED`, `Elapsed 00:00:00`,
ended at exactly the moment an agent-side wait window expired. It never ran.

**Cause:** it was submitted through a managed dispatch path that ties the job's
lifetime to a bounded wait. On a partition where queueing time is unbounded, the
wait expires first and the job is cancelled while still `PENDING`.

**Rule going forward: submit Cycle 3b work with plain `sbatch`.** A job must
survive with nobody watching it. `17960676` was resubmitted that way and writes
its own outputs to a persistent project directory.

## The seed defect (fixed, commit `b78f2fa`)

`run_prod.sh` substituted `gen_seed` while the `.mdp` files write `gen-seed`, so
the substitution never matched and the guard correctly refused to start. Now
accepts either spelling on input and writes the canonical form. Verified
byte-identical to the copy running on the cluster.

## What is still missing before a verdict exists

The pipeline **ended at production MD**: nothing computed the ΔG the gate reads.
That gap is now filled by `rescore.sh` + `make_mmgbsa_groups.py` + `collect_dg.py`
(this commit). Order of operations:

    run_prod.sh <tag> <rep>     ->  prod.xtc
    rescore.sh  <tag> <rep>     ->  appends a row to results_stage1.csv
    gate.py evaluate results_stage1.csv

`gate.py` was already written and is unchanged. It has now been **dry-run on
synthetic data** (`cycle3b_gate_dryrun.png`): a well-behaved method passes G1/G2'/G3
and a noisy one fails all three, with the pre-committed termination text emitted.
The criteria were exercised **before** any real ΔG existed, so they cannot be
tuned to the result afterwards.

## Interfaces that were assumed wrong once (check, don't recall)

* `chirality.py`: `assert <peptide.pdb> <resid> --by-position`. Positional. It
  reads a **single-residue-indexable PDB**, not a trajectory.
* `DRES_REL`: a **run parameter**, not a field in `pepmeta.txt`. Obtained by
  sourcing `peptide_spec.sh` and calling `load_peptide_spec "$TAG"`, which sets
  `SPEC_DRES`/`SPEC_AMIDE` from `prod_all.txt`. Sentinel for all-L is the string
  `none`, not `0`. That helper exists because a silently defaulting positional
  argument once built the all-L analog of deltorphin II *and* disarmed the
  chirality gate meant to catch it.
* run directory: `systems/<TAG>/rep<REP>`, not `runs/<TAG>_r<REP>`.
* `PBRadii`: gmx_MMPBSA's default is `3` (mbondi2). The design specifies
  **mbondi3**, which is `PBRadii = 4`. Confirmed against the installed package's
  own mapping, not from memory.
