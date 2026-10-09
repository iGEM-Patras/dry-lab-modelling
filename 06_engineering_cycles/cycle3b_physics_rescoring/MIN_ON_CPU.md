# Moving minimisation off the GPU, and validating that it is equivalent

**Date:** 2026-08-12

## Why

`17970387` (GPU minimisation of 5 systems) was scheduled by SLURM to start
**2026-08-15T15:00**: a three-day wait behind another group's array job. But
`min.mdp` is:

```
integrator = steep
emtol      = 1000.0
nsteps     = 50000
```

Steepest descent to a convergence criterion, on 119,476 atoms. That is not
sampling; the GPU buys nothing that justifies a three-day queue. `build_system.sh`
now honours `MIN_NB=cpu` (default `gpu`, so existing behaviour is unchanged) and
selects `-nb cpu -ntmpi 1 -ntomp $SLURM_CPUS_PER_TASK`.

**Measured cost on 32 cores of `pshort_el8`: 1:30–2:08 per system.**
Three days of queue became two minutes of compute.

## Validation: measured, not assumed

Equivalence was tested rather than argued. `c3b_dtII_DOR`, the one system that
had been minimised on GPU, was re-minimised on CPU from the identical inputs in
a scratch directory (`xcheck2/`), and the interface gate was run on the result.

| | GPU (reference) | CPU (`-nb cpu`, 32 threads) | Δ |
|---|---|---|---|
| steps to Fmax<1000 | 3630 | 4056 | +11.7 % |
| Potential energy | −2.0416499e+06 | −2.0527742e+06 | −0.055 % |
| Max force | 8.0689435e+02 | 9.2713959e+02 | both < emtol |
| worst-clash atom | 5339 | 5339 | same atom |
| interface gate | pass | `XCHECK2_GATE_OK` | - |

The two backends land in the same basin: energies agree to 0.05 %, both satisfy
the same convergence criterion, and both identify the *same atom* (5339) as the
worst remaining force. The step-count difference is ordinary nonbonded-summation
ordering, not a different result.

Interface behaviour on the CPU-minimised structure:
```
interface relaxation: 2.75 -> 2.60 A (-0.15 A)
contacts OK (2.60 A >= 2.5 A)
```

## The first cross-check attempt was invalid, and looked like a physics failure

`17971195` reported no CPU numbers at all and died with
`FileNotFoundError: min.gro does not exist`. Cause:

```
line 17: gmx: command not found
line 18: gmx: command not found
```

The script called bare `gmx` while `PATH` pointed at the Boltz-2 env, which has no
GROMACS. `build_system.sh` itself does this correctly
(`GMX=/data/users/kzanaj/envs/gmxcuda/bin/gmx`), and the host notes for this
cluster document the trap explicitly: the envs have no `bin/activate` and
binaries must be called by absolute path. The rerun uses `$GMXBIN`.

Worth naming the failure mode: an empty results section plus a missing-file
traceback is indistinguishable at a glance from "the CPU minimisation diverged".
It was a `PATH` bug in the harness, not a result.

## `sacct` COMPLETED did not mean the minimisations succeeded

The array jobs ended with `echo "MIN_CPU_EXIT=$?"`, so the job's exit status
reflects the **echo**, not `build_system.sh`. All six showed `COMPLETED` whether
or not the science worked. They were re-audited from their own logs:

| system | PE | Fmax | min contact | gate |
|---|---|---|---|---|
| `c3b_dtII_MOR` | −1.1796715e+06 | 9.058e+02 | 2.76 Å | OK |
| `c3b_dtI_DOR` | −1.5448880e+06 | 9.520e+02 | 2.60 Å | OK |
| `c3b_dtI_MOR` | −1.4806315e+06 | 6.981e+02 | 2.61 Å | OK |
| `c3b_em1_DOR` | −1.2667408e+06 | 9.584e+02 | 2.64 Å | OK |
| `c3b_em1_MOR` | −1.1576044e+06 | 9.239e+02 | 2.78 Å | OK |
| `c3b_menk_MOR` | −1.2387839e+06 | 9.352e+02 | 2.69 Å | OK |

All six: `BUILD_OK`, `MIN_CPU_EXIT=0`, no pair below 2.6 Å. Genuinely fine, but
that was established by reading the logs, not by trusting the scheduler.

**Lesson for future array jobs: do not put a bare `echo` after the payload.**
Use `bash scripts/... ; rc=$?; echo "EXIT=$rc"; exit $rc` so the job state carries
the real status.

## One system was outside the array

`c3b_menk_DOR` finished its CPU stage at 19:28, eight minutes *after* the
minimisation array was submitted, so it was never in `TAGS`. Minimised separately
as `17974079`. This is the hazard of enumerating tags by hand at submit time while
other builds are still running.

## Chemistry check across all eight

```
c3b_dtII_DOR  dres=2    amide=yes      c3b_em1_DOR   dres=none amide=yes
c3b_dtII_MOR  dres=2    amide=yes      c3b_em1_MOR   dres=none amide=yes
c3b_dtI_DOR   dres=2    amide=yes      c3b_menk_DOR  dres=none amide=no
c3b_dtI_MOR   dres=2    amide=yes      c3b_menk_MOR  dres=none amide=no
```

Matches `CYCLE3B_DESIGN.md`: deltorphins D-Ala², endomorphin-1 all-L amidated,
met-enkephalin all-L **free acid**. The amidation binding introduced earlier is
doing its job: met-enkephalin built as the free acid without anyone remembering
to pass a flag.
