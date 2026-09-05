# Cycle 3b resume state — 2026-08-12 ~19:25 CEST

## Cluster access

`login8.hpc.binf.unibe.ch` went unresponsive around 18:00 CEST: two consecutive
commands (a multi-line audit, then a bare `cat` of one log) each hung past 20 min
and were force-cleared. Earlier commands the same evening returned in 20-90 s.
**Nothing was lost** — every SLURM job had already reached a terminal state before
the node degraded. Retry `c.call_command("hostname")` first; if that hangs, the
node is still down, and other login nodes may be reachable.

## What is CONFIRMED (read directly from sacct/logs before the hang)

| job | what | result |
|---|---|---|
| `17958523` | user's `PRJNA845531_run` | **COMPLETED** 20:36:14, ended 2026-08-12T13:15:29 — the 3-week GPU bottleneck is gone |
| `17962083_[0-4]` | CPU rebuild, 5 systems | COMPLETED, all `BUILT_DRES=2 BUILT_AMIDE=yes` |
| `17962082` | menk co-fold refold, corrected flags | COMPLETED — `c3b_menk_DOR` 2869 atoms, `c3b_menk_MOR` 3175 atoms, **PDB** |
| `17970386_[0-1]` | menk CPU builds | COMPLETED — `c3b_menk_MOR` chem.txt = `BUILT_DRES=none BUILT_AMIDE=no` (free acid, correct) |
| `17971194_[0-5]` | CPU minimisation, 6 systems | COMPLETED, 1:30-2:08 each |
| `17971195` | CPU-vs-GPU minimisation cross-check | COMPLETED in 0:42 — **LOG NOT YET READ** |
| `17959496` | benchmark | FAILED on `DRES: unbound variable`, fixed in `a1b1dd0` |
| `17970387` | GPU minimisation | CANCELLED by me — superseded by the CPU path |

## THE OPEN ITEM — read this log first

```
/data/users/kzanaj/boltz_dock/cycle3b/minxcheck_17971195.log
```

It re-minimises `c3b_dtII_DOR` (the one system minimised on GPU) on CPU in
`$W/xcheck_min_cpu/`, and prints CPU vs GPU potential energy, Fmax, step count,
and the interface gate result. **Do not treat the CPU-minimised systems as valid
until this is read.** GPU reference to compare against:

```
Steepest Descents converged to Fmax < 1000 in 3630 steps
Potential Energy  = -2.0416499e+06
Maximum force     =  8.0689435e+02 on atom 5339
```

Expect agreement (steepest descent to a convergence criterion is backend-
independent in principle) but it is measured, not assumed. Look for
`XCHECK_GATE_OK`. If CPU and GPU disagree materially, the 6 CPU-minimised systems
must be re-minimised on GPU — now cheap, since pgpu is free.

## Why minimisation moved to CPU

`17970387` was scheduled to start **2026-08-15T15:00** — a 3-day wait behind
`afreiberg`'s `tStatAI` array and `mbotos`'s 2-day `scvi_oar`. min.mdp is
`integrator=steep`, `emtol=1000`, 119k atoms: a convergence criterion, not
sampling. `build_system.sh` now honours `MIN_NB=cpu` (default `gpu`, unchanged).
Actual CPU cost: ~2 min/system on 32 cores of `pshort_el8`. Backup:
`scripts/build_system.sh.bak_nbgpu`. **This patch is not yet committed to git.**

## Next actions, in order

1. Read `minxcheck_17971195.log`; confirm agreement + `XCHECK_GATE_OK`.
2. Audit all 8 systems for `min.gro` + chem.txt. menk must be `amide=no dres=none`;
   the other 6 must be `amide=yes dres=2`.
3. Commit the `MIN_NB` patch to `build_system.sh` with the cross-check numbers.
4. Re-run the benchmark (`17959496`'s successor) with the `DRES_REL` fix — pgpu is
   free now. It must pass the chirality gate **in-line**, not retrospectively.
5. Then launch the 24-run Stage 1 campaign (`prod_all.txt`, 24 rows, 8 tags).

## Defect ledger (three of one family, all caught by gates)

1. `DRES` positional default built the all-L analog and disarmed its own check.
2. `AMIDATE` hardcoded `yes`; chem.txt recorded the table value, not the built one.
3. `$DRES` undefined at run_prod.sh:84 — killed a run *after* 200 ps, inside the gate.

Each was a chemistry parameter reaching a safety gate by a path never exercised
end-to-end. Worth a fourth look before the campaign: any other variable that
crosses the build/production boundary by name rather than by file.

## Benchmark number that survived the failure

**68.075 ns/day** NVT on `c3b_dtII_DOR` (119,476 atoms, 1 GPU, 8 OpenMP threads)
— above the 40-50 ns/day the design assumed. Peptide extracted as
`TYR-ALA-PHE-GLU-VAL-VAL-GLY-NHE`; retrospective assert on the leftover
`pep_post-NVT.pdb` gave `res2 (ALA): V = -2.561 -> D (ok)`. D-Ala2 survived 200 ps.
