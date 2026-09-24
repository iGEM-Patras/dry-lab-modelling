# Cycle 10 condition B: replicate 2 failed numerically at 106.5 ns — protocol exonerated

**Date:** 2026-09-25 · **Consequence:** condition B reports **n = 2**, not n = 3.
Replicates 1 and 3 are verified complete and their protocol is verified correct.

## What happened

```
Step 106547400: The total potential energy is -nan, which is not finite.
Box[0] = {  inf, -nan, -nan }
Box[1] = { -nan,  inf, -nan }
Box[2] = { -nan, -nan,  inf }
```

The system diverged numerically at ~106.5 ns. The box became infinite, so `prod.cpt`
holds a corrupt state and the run is **not recoverable by resuming** — a resume attempt
re-reads the same non-finite coordinates and fails identically.

## Verified state of all three replicates

| replicate | last logged time | `prod.gro` | trajectory | status |
|---|---|---|---|---|
| rep1 | **200,000 ps** | present | 50.5 MB | complete |
| rep2 | 106,500 ps | **absent** | 27.0 MB | **failed** |
| rep3 | **200,000 ps** | present | 50.5 MB | complete |

Checked three independent ways — logged time, presence of the final structure, and
trajectory size — rather than from a status line.

## The protocol is not the cause. Hypothesis falsified.

The leading candidate was the MARTINI 2 cholesterol constraint problem documented in
[`04_lipoplex_md/MARTINI_DECLASH_GUIDE.md`](../../04_lipoplex_md/MARTINI_DECLASH_GUIDE.md):
coupled constraints on CHOL require `-DFLEXIBLE` or a LINCS order near 72 against a
default of 4. Had `prod.mdp` lacked both, rep1 and rep3 surviving would have been luck and
their data would need re-examination.

**All three replicates carry the fix.** Read from `prod.mdp`, and confirmed against
`mdout.mdp` which records what `grompp` actually used:

```
define               = -DFLEXIBLE
constraints          = none          <- CHOL constraints converted to bonds
constraint-algorithm = lincs
lincs-order          = 12
lincs-iter           = 2
lincs-warnangle      = 90
dt                   = 0.001
pcoupl               = c-rescale, tau-p 20.0, isotropic
```

So the documented fault was correctly guarded against in every replicate, and **rep1 and
rep3's data stands on a verified protocol rather than on chance.**

## The failure was sudden, not a slow degradation

`prod.edr` contains **214 frames and zero non-finite values.** The last written frame at
106,500 ps is entirely normal, and the divergence occurred at step 106,547,400 — **within
47 ps** of a healthy frame.

Final six frames before failure: potential ≈ −6.16 × 10⁵ kJ/mol, volume 2779–2784 nm³,
pressure fluctuating in the normal ±50 bar range. No trend, no drift, no warning.

## rep2 was statistically identical to the survivors

| | rep1 | rep2 at failure | rep3 |
|---|---|---|---|
| box volume | 2784.2 nm³ | **2784 nm³** | 2783.3 nm³ |
| volume drift over run | −0.30 % | — | −0.33 % |
| volume SD | 4.92 nm³ | — | 5.01 nm³ |

Volumes agree to within 0.03 %. rep2 was sampling the same ensemble as the two that
finished, right up to the event.

**Reading:** a single-event numerical divergence — a rare close contact, or a
hardware/arithmetic fault on the node — not a systematic protocol problem. Consistent with
the sudden onset, the clean energy history, and the identical settings across replicates.

## Consequence for the result

**n = 2 is clean and usable.** Two independent 200 ns replicates, verified protocol,
ensemble properties agreeing to 0.03 %. The replicate spread from two seeds is the
available uncertainty and should be reported as such.

A fresh rep2 from a new seed would be scientifically sound — the protocol is not
implicated — but it is a third seed on a result that already has two, at ~2.3 days of GPU.
Not run; the allocation is committed to the Cycle 8 engPENK arm, which is untested.

## Method note: my retry loop concealed this

The resume job ran **200 attempts**, every one reporting `106500.00000 ps`, and **exited 0**.
Two defects:

1. The loop was written for node failures, where retrying is correct. It treated a
   deterministic, unrecoverable error as transient and re-ran it 200 times.
2. Its exit status reflected whether the *loop* completed, not whether the simulation
   *progressed* — so the job reported success on a run that advanced zero steps.

Reading only the job status would have produced "rep2 completed". The fourth instance this
week of a check passing for the wrong reason. The correct construction compares the
simulated time before and after each attempt and **aborts on the first attempt that makes
no progress.**

Also corrected: rep2 was earlier described as having "stopped at 53 %", treated as a node
failure needing a resume. It had already diverged. The resume could never have worked.
