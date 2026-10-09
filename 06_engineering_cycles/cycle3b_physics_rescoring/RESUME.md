# Cycle 3b: RESUME HERE

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

The benchmark had simulated `YaFEVVG-OH`, the **free acid** (`packmol-memgen
--parametrize` runs tleap, which defaults a bare C-terminus to the charged
carboxylate. That is the same wrong-species error this cycle exists to correct.
`amidate.py` now installs an NHE cap (verified: net charge 0.000 vs −1 for the
acid, tleap Errors=0 Warnings=0, D-centre intact) and `build_system.sh` asserts
NHE is in the final topology. All six rebuilt systems logged
`C-terminus: primary amide (NHE)`. BENCHMARK.md carries a correction notice.

Met-enkephalin is the one control that must stay a free acid, that is its native
form: hence `--no-amidate` for those two.

## Two open failures

**1. `BUILD_EXIT=2` with no error message: diagnosed, fixed in this commit.**
`packmol-memgen` actually *succeeded* (`DONE!`, `bilayer_complex_start_lipid.top`
+ `.crd` on disk). The script died on the very next line:

    PRM=$(ls *_lipid.top *.prmtop *.parm7 2>/dev/null | head -1)

`ls` exits **2** when any operand does not exist, and `set -o pipefail` propagates
that out of the command substitution, so `set -e` kills the script silently. I had
previously misdiagnosed this as a wrong glob pattern and "fixed" it by adding
`*_lipid.top` to the list, which could never work, because `*.prmtop` still fails
to match. Now replaced with a nullglob helper. **Every one of the 6 builds hits
this**, which is why no `system.top` exists yet.

Because the packing is ~30 min of CPU per system and the topology already on disk
is the correct amidated species, `build_system.sh` now takes `--resume` to skip
straight past packing.

**2. Met-enkephalin co-fold produced no structure.** Confirmed by inspection: the
output tree contains `msa/`, `processed/` and `lightning_logs/` but **no
`predictions/` directory whatsoever** (so this is not a filename or path-guessing
problem, Boltz genuinely wrote no model. It nevertheless exited 0, which is why the
job printed `MENK_FOLDS_OK` (the loop only tests the exit status). Investigate the
`menk_17816705.log` prediction stage before resubmitting; a 5-residue peptide
(`YGGFM`) is the shortest chain in the panel, so a minimum-length or MSA-depth
condition is the first thing to check. Separately: I
submitted the menk builds without `--dependency`, so they ran 3 s after submit,
before any pose could exist (`FAIL: no pose`): use
`sbatch --dependency=afterok:<foldjob>` next time.

## STATUS 2026-07-30: three scaffolding defects fixed; single-pair pilot queued

Repo `0703ec9`. Fixed and deployed to the cluster (cluster copy is NOT a git repo,
files were pushed over the compute bridge, so verify by md5 after any edit):

1. `build_system.sh` never produced `index.ndx`, `pepmeta.txt`, `min.gro`. It ended at
   `system.top`/`system.gro`, but `run_prod.sh` pre-flights on those three files, so all
   18 replicates died in 3-5 s. NOW: after packing/parametrisation the build runs
   `make_index.py` (peptide location + thermostat groups) and then grompp+mdrun on
   `min.mdp` to produce `min.gro`. Order matters: `make_index.py` must run BEFORE the
   minimisation grompp, because that grompp takes `-n index.ndx`.
2. `tilt.py` was validated but never wired in. NOW asserted (`--max-deg 10 --rec-chain A`)
   immediately after a successful memembed and BEFORE packing, so a silently-mis-oriented
   bundle fails the build instead of consuming a GPU-day to measure reorientation.
3. `run_prod_job.sh` (new) wraps `run_prod.sh` and `exit $JOB_EXIT`, so `afterok`
   dependencies actually gate. Previously a job's last line echoed the status, which
   always exits 0: every dependent wave was released regardless of failure, which is
   what made the canary gate inert.

## MY DEFECT, NOT THE PIPELINE'S: overwrote a script while a job was running it

Job 17826633 (c3b_cpu_dtII_DOR) ran 01:43:27 -> 02:24:14 and FAILED at 40 min with:

    scripts/build_system.sh: line 241: syntax error near unexpected token `}'

Line 241 is inside a Python heredoc and is perfectly valid. `bash -n` passes on the file.
The build had already done everything right before dying: dres=2 from the table, D-centre
V=-2.504 confirmed, NHE amide, tilt 29.40 -> 0.00 deg, rec-pep 2.75 -> 2.75 A.

CAUSE: build_system.sh mtime = 02:09:20, i.e. INSIDE the job's run window. I deployed the
contacts.py wiring while 17826633 was executing that very file. Bash does not slurp a
script; it reads it incrementally BY BYTE OFFSET. The file grew 18003 -> 19054 bytes
under the running shell, so bash resumed at a now-stale offset, landed mid-construct and
reported a syntax error at a line that was never wrong. Both dependents then died
DependencyNeverSatisfied.

Note the trap: `bash -n` after the fact CANNOT reproduce this. The file on disk is valid.
The corruption existed only in the running shell's read position.

FIX -- deployment is now ATOMIC. Write to scripts/.NAME.new then os.replace() onto the
target. rename(2) swaps the directory entry; a running bash holds the ORIGINAL inode and
keeps reading the original bytes to completion, so an in-flight job finishes on the
version it started with and only new invocations pick up the new file. Also verify a
sha256 of every deployed file, and check `squeue | grep c3b_` before deploying at all.

NEVER write in place to a script on this cluster. In-place is what broke this run.

Relaunched clean (17826633's partial systems/c3b_dtII_DOR removed first):
  cpu 17836485 -> gpu 17836486 (afterok) -> prod 17836487 (afterok)

## POST-MIN CONTACT GATE ADDED, 2026-07-31 (closes the gap FINDING 2 opened)

New `scripts/contacts.py`, two modes:
  record  <top> <coords> <pepmeta> <out>    baseline the interface BEFORE minimisation
  check   <top> <coords> <pepmeta> <base>   re-measure AFTER, compare, exit 1 on fail

Wired into build_system.sh: `record` runs right after make_index.py (CPU stage, writes
contacts_pre.txt); `check` runs at the end of do_minimise() (GPU stage). contacts_pre.txt
was added to BOTH stage handoff validation lists so a missing baseline fails immediately
with a clear cause instead of 20 min later inside the gate.

Thresholds: HARD_A=2.20 (FAIL), WARN_A=2.50 (warn). A heavy-atom H-bond sits at 2.6-3.0 A
and tightens to ~2.5 A when strong, so >=2.5 A is chemically sensible; below 2.2 A there
is no non-bonded interpretation, that is overlap.

WHY POTENTIAL ENERGY CANNOT SUBSTITUTE: do_minimise already read Potential Energy and
Maximum force from md_min.log. Both are whole-system numbers over ~155k atoms of lipid
and water. A single 1.7 A contact at the receptor-peptide interface is far inside their
noise. The interface must be measured directly.

TWO IMPLEMENTATION DETAILS THAT MATTER:
- Minimum-image convention is applied. min.gro comes back from GROMACS with coordinates
  wrapped into the box; a receptor-peptide pair straddling a boundary would otherwise
  measure across the whole cell (~100 A) and a real clash would read as a pass.
- Heavy atoms are selected by atomic_number, not by name prefix. Amber names CA/CB start
  with C -- so does chlorine -- and name-prefix guessing is how hydrogens leak back into
  a "heavy atom" selection.

GATE TESTS (jobs 17826639, 17826640, 17826641 on pshort_el8):
  T1 record on real c3b_dtII_MOR -> min 2.29 A, GLN126:OE1-VAL406:CG2, 4 pairs <2.6
     INDEPENDENT CROSS-CHECK: identical to the sweep's value, which came from a separate
     PDB-parsing code path. Two implementations agree on the same number.
  T2 unchanged coords         -> WARN + exit 0 (2.29 is above the 2.2 floor: correct)
  T4 peptide -1.0 A into rec  -> 1.75 A, FAIL exit 1
  T7 missing baseline         -> clean FAIL message, exit 1 (was a raw traceback; fixed)
  T8 truncated baseline       -> clean FAIL message, exit 1
  T3/T6 FAILED AS TESTS, NOT AS GATE: displacing the peptide "away from the receptor
     centroid" (T3) and "+4 A along the membrane normal" (T6) BOTH made contacts worse
     (2.06 A and 0.54 A). The orthosteric pocket is enclosed laterally AND capped from
     above by the receptor N-terminal tail (TRP31, SER30 are the atoms hit). There is no
     guessable "out" vector. T9 replaced guessing with a measured scan over +-5..25 A on
     each axis, picking the displacement that maximises the min distance.

## PANEL PRE-FLIGHT SWEEP, 2026-07-30 (job 17826637, 46 s wall, all 6 tags PASS)

New `STAGE=orient` mode in build_system.sh: runs stages 1-3b (spec -> chirality -> amide
-> memembed -> tilt fix/assert) then stops before packing. Emits ORIENT_OK, NOT
BUILD_OK/BUILD_CPU_OK: a pre-flight dir has no topology and nothing runnable, so it can
never be mistaken for a usable system. New `SYSROOT` env var redirects output (scripts,
envs, prod_all.txt still resolve under $W) so a sweep cannot touch systems/ or a build in
flight. Sweep driver: sweep_orient.sh. Costs ~8 s/tag vs ~40 min for a full build.

FINDING 1: memembed mis-orientation is SYSTEMATIC, not a one-off:

  tag             tilt_pre  tilt_post   min rec-pep (pre -> post)   D-centre
  c3b_dtI_MOR       36.43     0.00        2.09 -> 2.09 A            V=-2.481 D ok
  c3b_dtI_DOR       35.25     0.00        2.60 -> 2.60 A            V=-2.502 D ok
  c3b_em1_MOR       24.76     0.00        2.01 -> 2.01 A            all-L by design
  c3b_em1_DOR       22.95     0.00        1.74 -> 1.74 A            all-L by design
  c3b_dtII_DOR      18.28     0.00        2.75 -> 2.75 A            V=-2.504 D ok
  c3b_dtII_MOR      17.38     0.00        2.29 -> 2.29 A            V=-2.498 D ok

6/6 exceeded the 10 deg gate (17.4-36.4 deg), EVERY ONE with memembed exiting 0 and the
build recording "orientation: --preoriented". Never trust that exit code. The fix took
all six to 0.00 deg with min rec-pep distance unchanged to 0.00 A in every case, rigid
rotation now confirmed panel-wide, not just on the pilot. Chemistry resolved from
prod_all.txt correctly for all six: dtI/dtII -> dres=2 (D-centre asserted), em1 -> none
(reported as not applicable rather than silently skipped).

This supersedes the earlier "4 of 6" reading at the bottom of this file: it is 6 of 6.

FINDING 2: several systems carry very close receptor-peptide contacts. Measured on
heavy atoms with hydrogens EXCLUDED, so these are real, not H-placement artifacts.
Worst pair per tag:

  c3b_em1_DOR   1.74 A  LYS108:NZ  - NHE5:N      4 pairs <2.6,  14 <3.0
  c3b_dtI_MOR   2.09 A  TRP320:NE1 - GLY7:O      8 pairs <2.6,  17 <3.0
  c3b_em1_MOR   2.01 A  TRP31:CZ3  - NHE5:N      5 pairs <2.6,  10 <3.0
  c3b_dtII_MOR  2.29 A  GLN126:OE1 - VAL6:CG2    4 pairs <2.6,  10 <3.0
  c3b_dtI_DOR   2.60 A  TYR129:CE1 - TYR1:N      1 pair  <2.6,   3 <3.0
  c3b_dtII_DOR  2.75 A  TYR129:CE1 - TYR1:N      0 pairs <2.6,   2 <3.0

These are Boltz co-fold artifacts, NOT introduced by the tilt fix (distances unchanged
through it). 1.74 A between an amide N and a charged Lys NZ is well inside vdW contact.
Minimisation should relieve them, so this is a WATCH not a blocker, but it means the
post-min check must RE-MEASURE these contacts, otherwise a system that failed to relax
enters production with a clash driving the first ns of dynamics. NOT YET IMPLEMENTED;
do this before authorising the full panel.

Artifacts: cycle3b_preflight_sweep.csv, cycle3b_preflight_sweep.png

## WRONG MOLECULE BUILT, 2026-07-30: the worst class of bug in this pipeline

The tilt-corrected build (17818367/68) COMPLETED CLEANLY and was the wrong molecule.
Its log read: `peptide: TYR-ALA-PHE-GLU-VAL-VAL-GLY-NHE`. Deltorphin II is
Tyr-**D-Ala**-Phe-Glu-Val-Val-Gly-NH2. The build was launched with dres=`none`, so the
D-Ala2 inversion never ran and the 155,323-atom system was the ALL-L analog. Every
downstream check passed: tilt 0.00 deg, tleap Errors=0, groups partitioning exactly,
min.gro written. Caught only by reading the peptide sequence in the log against the
design table. Production 17818369 was cancelled while still PENDING: no GPU time lost.

WHY NOTHING CAUGHT IT. `run_prod.sh` has a per-stage chirality gate, and it is SKIPPED
when DRES_REL=none (run_prod.sh:64). Both build_system.sh (`DRES="${2:-none}"`) and
run_prod_job.sh (`DRES_REL="${4:-none}"`) defaulted the argument that ARMS that gate.
A silent default on a safety gate's own input disables the gate. And `none` is a
LEGITIMATE value for part of the panel (c3b_em1_* are endomorphin-1, all-L), so a
defaulted `none` is indistinguishable from a correct one by inspection.

FIX: chemistry now comes from the design table, never the command line:
  scripts/peptide_spec.sh   new. load_peptide_spec <tag> reads DRES+AMIDE from
                            prod_all.txt (the table of record) and hard-FAILS on an
                            unknown tag or inconsistent replicate rows.
  build_system.sh           DRES defaults to `auto` (= from table). An explicit value
                            is cross-checked and must AGREE, else FAIL.
                            Writes chem.txt recording what it actually built with.
  run_prod_job.sh           positional defaults REMOVED; reads the table, then
                            cross-checks chem.txt. Missing chem.txt => refuse to run
                            (older build, chemistry unverifiable).

Guards verified on the cluster against the real prod_all.txt: unknown tag -> exit 1;
`dres=none` for c3b_dtII_DOR -> exit 1 with the contradiction named; all six panel tags
resolve (dtI/dtII x DOR/MOR = dres 2, em1 x DOR/MOR = none, all amide=yes).

STANDING CHECK for every future build: read the `peptide:` line in the build log and
confirm the sequence against prod_all.txt. Clean tleap output proves the system is
physically valid, NOT that it is the intended molecule.

Chain relaunched (all-L system deleted): cpu 17826633 -> gpu 17826634 -> prod 17826635.

## TILT GATE FIRED ON THE FIRST REAL SYSTEM, 2026-07-30 (the gate earned its keep)

Run 17818364 FAILED in 14 s at the tilt gate: `TILT_DEG=19.65` on c3b_dtII_DOR, from 372
receptor CA atoms, while memembed exited 0 and the build logged `orientation:
--preoriented`. This is EXACTLY the silent memembed failure the gate was written for. The
rigid-body and chain-preservation checks all passed; only the orientation was wrong, so
nothing upstream would have caught it. Without the gate this system would have packed a
bilayer around a 20 deg-tilted bundle and the 20 ns window would have measured the
receptor righting itself, not the peptide binding. SLURM then marked the two dependent
jobs `DependencyNeverSatisfied`: correct behaviour, and proof the afterok wiring works.

FIX (verified on the real failing file before relaunch, not assumed):
`tilt.py fix` is now wired in ahead of the assert. Measured on the actual c3b_dtII_DOR
complex: 19.65 -> 0.00 deg; min receptor-peptide distance 2.754 -> 2.754 A (docked pose
untouched, rotation genuinely rigid); z-centre -0.82 -> -0.92 A (solute stays where
memembed put it, so --preoriented bilayer placement is still valid); z-extent 111.5 ->
121.6 A. That last number is the independent physical check: straightening a tilted
bundle MUST lengthen its projection on the membrane normal. If z-extent ever DECREASES,
the rotation went the wrong way and the "fix" is wrong; do not trust the 0.00 deg alone.

SECOND BUG found while fixing this: the gate asserted on `complex_oriented.pdb` but
packing consumes `complex_start.pdb` (DUM-stripped). Same tilt value either way (DUM
atoms are not CAs and never enter the measurement), so it was harmless TODAY, but
validating a file the pipeline does not consume is how a gate goes stale silently. The
gate now measures, fixes, re-asserts, and re-checks the pose all on complex_start.pdb.

PILOT IN FLIGHT (one receptor pair, not the full panel, deliberate, per the decision to
pilot before committing 6.7 GPU-days). SPLIT-STAGE build. Superseded chains: 17818362/63
(combined build: queued the CPU hour behind the contended GPU), 17818364/65/66 (died at
the tilt gate above). CURRENT:
  cpu  17818367  c3b_cpu_dtII_DOR   2 h  pshort_el8 (NO gpu, 5 idle nodes) -> BUILD_CPU_OK
  gpu  17818368  c3b_gpu_dtII_DOR  30 m  pgpu --gres=gpu:1  afterok:cpu    -> BUILD_OK
  prod 17818369  c3b_prod_..._r1   12 h  pgpu --gres=gpu:1  afterok:gpu    -> PROD_OK

WHY SPLIT: only the minimisation needs a GPU; stages 1-5 (pack/parametrise/index) are
CPU-only and were making the whole build wait on the saturated 2-GPU pgpu node behind a
higher-priority pending job (est. up to ~1.5 d). pshort_el8 has 5 idle nodes and no GPU
contention, so the CPU stage starts in minutes; only a ~5-min GPU minimisation then
competes for the scarce card. build_system.sh gained a STAGE switch (all|cpu|gpu);
minimisation is factored into one do_minimise() so both paths run IDENTICAL code. The CPU
stage emits BUILD_CPU_OK (NOT BUILD_OK: the latter asserts min.gro, which only the GPU
stage produces). Guards verified locally: bad STAGE value and STAGE=gpu with missing
inputs both FAIL+exit 1.

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
2. Resubmit the 6 builds with `--resume` (fast: packing is skipped; expect
   minutes, not 30 min each). Confirm each logs `topology:`,
   `amide verified in final topology`, `Errors = 0`, and writes `system.top`,
   `system.gro`, `index.ndx`, `pepmeta.txt`.
3. Locate the menk poses (`find $W/out_c3b_menk_* -name "*model_0*"`), then build
   those two with `--no-amidate`.
4. Submit the 24 production replicates via `run_prod.sh <tag> <rep> <yes|no>
   <dres_rel|none>`: already written, syntax-checked, not yet run. It re-runs
   NVT+NPT per replicate with a distinct `gen_seed` (independent velocities, so
   the three replicates are genuinely independent), asserts the amide before
   starting, and gates chirality post-NVT / post-NPT / post-production, exiting 3
   to DISCARD an inverted replicate rather than averaging it in.
5. Then the G1/G2/G3 calibration gate. **Stage 2 stays unauthorised until it
   passes**: per the pre-registration, a failed gate terminates the cycle and
   reports a negative methodological result.

Budget unchanged: 71.5 ns/day measured → Stage 1 = 6.7 GPU-days (~3.4 d on 2 GPUs).

---

# UPDATE: checkpoint check, two blocking findings

## Builds all SUCCEEDED; the species fix holds

All 6 systems built with `RESUME_EXIT=0`, `tleap Errors=0`, and every log carries
`amide verified in final topology: 1 NHE residue(s)`. The `--resume` path worked:
builds took 45 s – 2:48 instead of ~30 min. The nullglob fix for the silent EXIT=2
is confirmed correct against real builds.

## BLOCKER 1: build → production skipped a stage

`build_system.sh` writes only `system.top` + `system.gro`. The files `run_prod.sh`
needs (`index.ndx`, `pepmeta.txt`, `min.gro`) are produced by **`run_md.sh`**, which
the chain skipped. All 18 production tasks died in 3–5 s on
`FAIL: <tag> missing index.ndx -- build incomplete`. No GPU time lost.

Two fixes needed:
1. Add a `--prep-only` mode to `run_md.sh` that stops after minimisation (index +
   pepmeta + min.gro), and run it between build and production. Do NOT run full
   `run_md.sh`: it also does NVT/NPT/benchmark, which `run_prod.sh` redoes per
   replicate with its own seed, so that would waste ~37 min/system.
2. `run_prod_job.sh` ends with `echo "JOB_EXIT=$?"`, so the job ALWAYS exits 0.
   SLURM therefore marked all 18 `COMPLETED` and `--dependency=afterok` released the
   next wave anyway. The canary gate was inert. Signature to watch for:
   **`JOB_EXIT=1` in the log with sacct State=COMPLETED.** End the script with an
   explicit `exit $rc`.

## BLOCKER 2: the panel is not size-comparable (fix before spending GPU)

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
benchmark of the same system gave 270,287 from identical inputs: the geometry is not
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

# UPDATE 2: root cause found; two of my own claims were wrong

## CORRECTION 1: the budget claim was wrong

I wrote "the panel mean is well above 270k atoms, so Stage 1 costs materially more
than 6.7 GPU-days". That is false. Panel mean is **188,383 atoms = 0.70x** the
benchmark; median 121,054 = 0.45x. **Only dtII_DOR (441,296) exceeds the benchmark.**
Scaling throughput as 1/N, the 18 as-built runs cost **3.5 GPU-days**, and a panel
pinned at ~120k atoms costs **3.0 GPU-days for all 24 runs**, *cheaper* than the
pre-registered 6.7, not more expensive. Compute was never the problem.

## CORRECTION 2: the met-enkephalin hypothesis was wrong

I wrote "YGGFM is the shortest chain in the panel; check for a minimum-length
condition". Endomorphin-1 is `YPWF` (**4 residues, shorter than YGGFM's 5**) and
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

The result is **bimodal**: 2 systems at ~3°, 4 at 24–35°. Identical inputs and
identical method, so this is `memembed` succeeding on two and failing on four, not a
property of the receptor. Every build logged `orientation: --preoriented`, so the
build *believed* it was oriented and packed the bilayer around a tilted bundle.

This subsumes the box-size finding: a tilted bundle presents a wider xy footprint, so
`--dist 15` pads a larger bilayer. Size was the symptom; tilt is the cause.

**Why it invalidates the runs rather than just costing more:** with a 24–35° tilt the
TM hydrophobic belt does not align with the bilayer hydrophobic core, so TM residues
sit against headgroups and water. The protein will rotate during equilibration to
relieve that mismatch, which takes many ns, so a 20 ns production window would be
dominated by protein reorientation rather than by sampling the bound pose, and the
contact metrics would be measuring the relaxation, not the binding.

**Fix:** verify tilt as an assertion in `build_system.sh` (reject > ~10° and re-run or
fall back to memgen's internal orientation), then pin an explicit common box and
per-leaflet lipid count so all 8 systems are geometrically identical. Add the tilt
number to the build log. Rebuilds are CPU-only, ~30 min each, and 5 `pshort_el8` nodes
are idle, so all 8 fit in one wave.

---

# GATE EVALUATOR + PRE-REGISTRATION AMENDMENT: 2026-07-31

## The pre-registered G2 is unpassable; amended to G2' before any data existed

Writing the gate evaluator surfaced a defect in the pre-registered criterion.
G2 ("replicate SD of ddG_sel <= 1.5 kcal/mol on every control") demands
sigma_rep <= 1.06 kcal/mol -- below the 1-2 kcal/mol MM-GBSA uncertainty
CYCLE3B_DESIGN.md states as expected. Monte-Carlo over the pre-registered
anchors: a method with a PERFECT calibration slope passes all three gates 21%
of the time at sigma_rep=1.0, 3% at 1.5.

The decisive diagnostic: power FALLS as replicates rise (0.076 at n=2 to 0.000
at n=10, sigma_rep=1.5). More sampling makes a correct method fail more often.
That is an estimator defect, not a property of the method under test, so no
compute budget rescues it.

**G2' thresholds the SEM instead of the SD.** Power rises with replicates
(0.21 at n=2 to 1.00 at n=10) while the false-pass rate against a null method
is unchanged at ~2%. Not a weakening -- the threshold value stays at 1.5;
only the statistic changed. Relaxing the threshold instead would have raised
the false-pass rate, which is why that route was rejected.

Filed BEFORE any Stage-1 dG_bind value existed. That timing is the only
condition under which amending a pre-registered criterion is legitimate.
Full argument, power table, and the two honest readings of a pass/fail at
n=3: `AMENDMENT_G2.md`. Evidence: `gate_calibration.png` / `.csv`.

## scripts/gate.py

`gate.py evaluate <results.csv> [--out gate_verdict.json] [--sem-max 1.5]`

Input: one row per control x receptor x replicate, columns
`control,receptor,rep,dG_bind`. ddG_sel is formed WITHIN a replicate index
(dG(OPRM1) - dG(OPRD1)), not by averaging each receptor arm first -- this
keeps the arms balanced and makes the replicate spread an honest estimate on
the difference. A replicate present for only one receptor (e.g. a
chirality-discarded run, run_prod.sh exit 3) is DROPPED with a note, never
averaged in.

Exits 0 on a clean evaluation regardless of verdict: a FAIL is a result, not
an error. Callers read `gate_verdict.json`.

Verified against five synthetic cases with known verdicts before any real
data: clean pass, null method, sign-flipped, too-noisy, and one with a
deliberately dropped replicate (confirmed n=3 for that control while the
others keep 4). All five matched; G1/G2'/G3 observably fire independently.

## STILL OUTSTANDING

**The pipeline has no MM-GBSA scoring stage.** `run_prod.sh` produces
trajectories and stops; nothing converts them to dG_bind. `gate.py` consumes
a CSV that nothing currently writes. That stage is the next thing to build --
gmx_MMPBSA is installed at /data/users/kzanaj/envs/gmxmmpbsa (verified in the
software probe), but the run script, the index groups it needs, and the
per-replicate CSV writer do not exist yet.

**Recommendation, not authorised:** extend Stage 1 to n=5 (40 runs, ~5.8
GPU-days, still under the pre-registered 6.7 GPU-day budget) to lift G2' power
from 35% to 85%. Separate decision; the amendment does not take it.
