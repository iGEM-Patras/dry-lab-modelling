# Benchmark failure 17959496: `DRES: unbound variable`

**Date:** 2026-08-12
**Job:** `17959496` `c3b_bench_dtII_DOR_r1`, FAILED after 00:06:03, ExitCode 1:0

## What happened

The benchmark ran NVT to completion and then aborted inside the chirality gate:

```
starting mdrun 'Generic title'
200000 steps,    200.0 ps.
Writing final coordinates.
Performance:       68.075 ns/day
  [gate] peptide extracted (110 atoms): TYR-ALA-PHE-GLU-VAL-VAL-GLY-NHE
run_prod.sh: line 84: DRES: unbound variable
```

`run_prod.sh` defines `DRES_REL` (peptide-relative index, arg 4) and derives
`DRES_ABS` (whole-system residue number). Line 84 referenced **`$DRES`**, which is
defined nowhere in the script. `set -euo pipefail` (line 12) turned the
undefined reference into a hard abort.

Note where it aborted: *after* 200 ps of MD, inside the safety gate itself. The
run was thrown away at the point where it was about to be validated.

## Which variable is correct

`chirality.py --by-position` indexes residues **within the file it is handed**,
and the gate hands it a peptide-only PDB (8 residues). So the peptide-relative
index is correct. Verified against the actual file the failed run left behind:

```
$ chirality.py assert pep_post-NVT.pdb 2 --by-position     # DRES_REL
assert res2 (ALA): V = -2.561 -> D (ok)

$ chirality.py assert pep_post-NVT.pdb 331 --by-position   # DRES_ABS
FAIL: position 331 outside 1-8
```

`DRES_ABS` would have tripped the bounds check on every run.

## The result that survives

The gate's own output proves the science was fine: the peptide extracted as
`TYR-ALA-PHE-GLU-VAL-VAL-GLY-NHE` -- correct sequence, correctly amidated (NHE)
-- and the retrospective assert shows **V = -2.561, D-configured**. The D-Ala2
survived 200 ps of NVT. Only the variable name was wrong.

Useful number obtained despite the failure: **68.075 ns/day** for NVT on this
system, close to the 40-50 ns/day the design assumed.

## Fix

`run_prod.sh` line 84: `"$DRES"` -> `"$DRES_REL"`. Backup on cluster:
`scripts/run_prod.sh.bak_dresunbound`.

This is the third defect of the same family in this pipeline (after the DRES
positional default and the AMIDATE hardcode): a chemistry parameter reaching a
safety gate by a path that was never checked end-to-end. The gates themselves
keep working correctly -- each of these was caught by a gate, not by a result
looking wrong.
