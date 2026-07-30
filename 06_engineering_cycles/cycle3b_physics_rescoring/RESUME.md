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

## STATUS 2026-07-30 — three scaffolding defects fixed; single-pair pilot queued

Repo `0703ec9`. Fixed and deployed to the cluster (cluster copy is NOT a git repo —
files were pushed over the compute bridge, so verify by md5 after any edit):

1. `build_system.sh` never produced `index.ndx`, `pepmeta.txt`, `min.gro`. It ended at
   `system.top`/`system.gro`, but `run_prod.sh` pre-flights on those three files, so all
   18 replicates died in 3-5 s. NOW: after packing/parametrisation the build runs
   `make_index.py` (peptide location + thermostat groups) and then grompp+mdrun on
   `min.mdp` to produce `min.gro`. Order matters — `make_index.py` must run BEFORE the
   minimisation grompp, because that grompp takes `-n index.ndx`.
2. `tilt.py` was validated but never wired in. NOW asserted (`--max-deg 10 --rec-chain A`)
   immediately after a successful memembed and BEFORE packing, so a silently-mis-oriented
   bundle fails the build instead of consuming a GPU-day to measure reorientation.
3. `run_prod_job.sh` (new) wraps `run_prod.sh` and `exit $JOB_EXIT`, so `afterok`
   dependencies actually gate. Previously a job's last line echoed the status, which
   always exits 0 — every dependent wave was released regardless of failure, which is
   what made the canary gate inert.

PILOT IN FLIGHT (one receptor pair, not the full panel — deliberate, per the decision to
pilot before committing 6.7 GPU-days):
  build 17818362  c3b_dtII_DOR      3 h  pgpu --gres=gpu:1
  prod  17818363  c3b_dtII_DOR rep1 12 h afterok:17818362

SCHEDULER TRAP (cost two dead jobs, 17818360/61): `pgpu` has a QOS minimum on gres/gpu.
Submitting without `--gres=gpu:1` is accepted, returns a job id, and pends FOREVER with
reason `(QOSMinGRES)`. It looks identical to waiting for a busy node. Correct submission:
`sbatch -p pgpu -A kzanaj --gres=gpu:1 --cpus-per-task=8 --mem=32G --time=...`.
Always read the pending REASON, not just the STATE.

Walltimes are sized from measured throughput, not guesses: packmol-memgen 61 min CPU;
min+NVT 200 ps+NPT 1 ns = 37.4 min; production 20 ns at 71.5 ns/day = 6.7 h.

### What to check when the pilot lands
Build log must show: `topology:`, `amide verified in final topology`, `Errors = 0`,
`TILT_DEG` under 10, `min:` energies, and `BUILD_OK`. Then `systems/c3b_dtII_DOR/`
must contain all of `system.top system.gro index.ndx pepmeta.txt min.gro`.
Production log must reach `PROD_OK`; a chirality-discard exits 3 by design (D-centre
inverted) and that replicate must be discarded, not averaged in.
Only if the pilot is clean: fan out the remaining 5 systems x 3 reps.
**Stage 2 remains unauthorised until the G1/G2/G3 calibration gate passes.** A failed
gate terminates the cycle and is reported as a negative methodological result.

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

---

# UPDATE — checkpoint check, two blocking findings

## Builds all SUCCEEDED; the species fix holds

All 6 systems built with `RESUME_EXIT=0`, `tleap Errors=0`, and every log carries
`amide verified in final topology: 1 NHE residue(s)`. The `--resume` path worked:
builds took 45 s – 2:48 instead of ~30 min. The nullglob fix for the silent EXIT=2
is confirmed correct against real builds.

## BLOCKER 1 — build → production skipped a stage

`build_system.sh` writes only `system.top` + `system.gro`. The files `run_prod.sh`
needs (`index.ndx`, `pepmeta.txt`, `min.gro`) are produced by **`run_md.sh`**, which
the chain skipped. All 18 production tasks died in 3–5 s on
`FAIL: <tag> missing index.ndx -- build incomplete`. No GPU time lost.

Two fixes needed:
1. Add a `--prep-only` mode to `run_md.sh` that stops after minimisation (index +
   pepmeta + min.gro), and run it between build and production. Do NOT run full
   `run_md.sh` — it also does NVT/NPT/benchmark, which `run_prod.sh` redoes per
   replicate with its own seed, so that would waste ~37 min/system.
2. `run_prod_job.sh` ends with `echo "JOB_EXIT=$?"`, so the job ALWAYS exits 0.
   SLURM therefore marked all 18 `COMPLETED` and `--dependency=afterok` released the
   next wave anyway. The canary gate was inert. Signature to watch for:
   **`JOB_EXIT=1` in the log with sacct State=COMPLETED.** End the script with an
   explicit `exit $rc`.

## BLOCKER 2 — the panel is not size-comparable (fix before spending GPU)

| system | atoms | POPC | box x,y (nm) |
|---|---|---|---|
| c3b_dtII_MOR | 96,673 | 624 | 9.7 × 9.6 |
| c3b_em1_DOR | 119,841 | 909 | 11.2 × 11.2 |
| c3b_em1_MOR | 120,941 | 828 | 10.8 × 10.8 |
| c3b_dtI_MOR | 121,167 | 744 | 10.3 × 10.3 |
| c3b_dtI_DOR | 230,381 | 1,449 | 13.9 × 13.7 |
| **c3b_dtII_DOR** | **441,296** | **3,234** | **20.0 × 20.0** |

Same ~3,136-atom receptor, same 4–7 residue peptide class, all `--preoriented`, yet
a **4.6× spread in atoms and 5.2× in bilayer area**. `--dist 15 --dist_wat 20` pads
differently-oriented proteins to very different footprints.

Why this is disqualifying: the measurement is DOR vs MOR for the SAME peptide. With
dtII_DOR at 3,234 lipids and dtII_MOR at 624, a difference in contact metrics is
partly a difference in bilayer area, water-layer thickness and finite-size effects
rather than in binding. Also note this rebuild gave 441,296 atoms where the original
benchmark of the same system gave 270,287 from identical inputs — the geometry is not
reproducible run-to-run, so it cannot be treated as a fixed property of the system.

Budget consequence: 71.5 ns/day was measured at 270k atoms. The panel mean is now
well above that and dtII_DOR is 1.63× it, so Stage 1 costs materially more than
6.7 GPU-days as currently built.

**Fix:** pin identical box dimensions and per-leaflet lipid counts for all 8 systems
(explicit box + lipid numbers rather than letting `--dist` padding decide) and
rebuild. An identical bilayer across the panel makes the peptide/receptor pair the
only variable, which is what the comparison requires. Verify by asserting the atom
count and box vectors agree across systems to within a small tolerance before any
production run.

## Revised resume sequence

1. Pin box/lipid counts in `build_system.sh`; rebuild all 6 (+ menk when unblocked).
   Assert cross-system size agreement.
2. Add `--prep-only` to `run_md.sh`; generate index/pepmeta/min.gro per system.
3. Fix `exit $rc` in `run_prod_job.sh` so `afterok` actually gates.
4. Re-measure ns/day at the pinned size; update the budget.
5. Canary, then the remaining replicates, then G1/G2/G3.

Met-enkephalin remains blocked (co-fold wrote no `predictions/`), so Stage 1 is 18/24.

---

# UPDATE 2 — root cause found; two of my own claims were wrong

## CORRECTION 1: the budget claim was wrong

I wrote "the panel mean is well above 270k atoms, so Stage 1 costs materially more
than 6.7 GPU-days". That is false. Panel mean is **188,383 atoms = 0.70x** the
benchmark; median 121,054 = 0.45x. **Only dtII_DOR (441,296) exceeds the benchmark.**
Scaling throughput as 1/N, the 18 as-built runs cost **3.5 GPU-days**, and a panel
pinned at ~120k atoms costs **3.0 GPU-days for all 24 runs** — *cheaper* than the
pre-registered 6.7, not more expensive. Compute was never the problem.

## CORRECTION 2: the met-enkephalin hypothesis was wrong

I wrote "YGGFM is the shortest chain in the panel; check for a minimum-length
condition". Endomorphin-1 is `YPWF` — **4 residues, shorter than YGGFM's 5** — and
folded fine. Minimum length is ruled out. The log shows Boltz's own
`Number of failed examples: 1`, alongside `Found explicit empty MSA for some
proteins, will run these in single sequence mode` (expected for any short peptide,
including the ones that worked). No structural cause identified; treat as a
transient and simply resubmit before investigating further.

## ROOT CAUSE of the size spread: the receptor is MIS-ORIENTED in 4 of 6 systems

Principal axis of the CA atoms in `complex_start.pdb` vs the membrane normal (z),
same method for every system, same receptor:

| system | tilt to normal | verdict |
|---|---|---|
| c3b_em1_DOR | 3.0° | OK |
| c3b_dtII_MOR | 3.1° | OK |
| c3b_em1_MOR | 23.6° | mis-oriented |
| c3b_dtII_DOR | 29.6° | mis-oriented |
| c3b_dtI_DOR | 29.8° | mis-oriented |
| c3b_dtI_MOR | 34.8° | mis-oriented |

The result is **bimodal** — 2 systems at ~3°, 4 at 24–35°. Identical inputs and
identical method, so this is `memembed` succeeding on two and failing on four, not a
property of the receptor. Every build logged `orientation: --preoriented`, so the
build *believed* it was oriented and packed the bilayer around a tilted bundle.

This subsumes the box-size finding: a tilted bundle presents a wider xy footprint, so
`--dist 15` pads a larger bilayer. Size was the symptom; tilt is the cause.

**Why it invalidates the runs rather than just costing more:** with a 24–35° tilt the
TM hydrophobic belt does not align with the bilayer hydrophobic core, so TM residues
sit against headgroups and water. The protein will rotate during equilibration to
relieve that mismatch, which takes many ns — so a 20 ns production window would be
dominated by protein reorientation rather than by sampling the bound pose, and the
contact metrics would be measuring the relaxation, not the binding.

**Fix:** verify tilt as an assertion in `build_system.sh` (reject > ~10° and re-run or
fall back to memgen's internal orientation), then pin an explicit common box and
per-leaflet lipid count so all 8 systems are geometrically identical. Add the tilt
number to the build log. Rebuilds are CPU-only, ~30 min each, and 5 `pshort_el8` nodes
are idle, so all 8 fit in one wave.
