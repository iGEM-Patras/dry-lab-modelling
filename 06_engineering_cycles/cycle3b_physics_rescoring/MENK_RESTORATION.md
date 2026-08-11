# Restoring met-enkephalin: the missing control

**Date:** 2026-08-11
**Trigger:** the question "so we just wait for the GPU jobs to finish". No.
Waiting alone would have ended in an automatic FAIL.

## The failure that was queued up

`gate.py` requires four controls and returns, *before evaluating any criterion*:

```
verdict: FAIL
reason:  missing controls: ['met_enkephalin']
```

`prod_all.txt` contained 18 rows covering 6 tags. `CYCLE3B_DESIGN.md` specifies
**8 systems x 3 replicates = 24 runs**, with met-enkephalin as the neutral
reference (`ddG ~ 0`) anchoring the low end of a ~8.4 kcal/mol range.

So Stage 1 could have completed all 18 runs perfectly, consumed the full GPU
budget, and produced a negative methodological result caused by a bookkeeping
gap rather than by the physics. The gate would have been *correct* to fail:
without a zero-anchor there is no test that the method places a weak binder
near zero.

## Why met-enkephalin was missing: a missing flag, not a modelling failure

The two met-enkephalin co-folds ran on 2026-07-29 and **succeeded**
(`menk_17816705.log`: "Number of failed examples: 0"). But `build_system.sh`
reported `FAIL: no pose for c3b_menk_DOR`.

Cause: the 6 working controls and the 2 failures used *different commands*.

| flag | `run_c3b_folds.sh` (6 OK) | `run_menk.sh` (2 failed) |
|---|---|---|
| `--output_format` | `pdb` | omitted -> **CIF default** |
| `--seed` | `2026` | omitted |
| `--diffusion_samples` | `15` | omitted |
| `--msa_pairing_strategy` | `greedy` | omitted |
| `--max_msa_seqs` | `1024` | omitted |

`build_system.sh` line 108 searches `find $W/out_${TAG} -name "*model_0.pdb"`.
Boltz had written `.cif`. The pose existed and was invisible.

Audit of what is actually on disk (corrected -- an earlier audit used broken
nested quoting and returned a listing of the wrong directory; it was discarded):

```
c3b_dtII_DOR  pdb=yes  c3b_em1_DOR  pdb=yes
c3b_dtII_MOR  pdb=yes  c3b_em1_MOR  pdb=yes
c3b_dtI_DOR   pdb=yes  c3b_menk_DOR pdb=NO  cif=NO   <- never produced
c3b_dtI_MOR   pdb=yes  c3b_menk_MOR pdb=NO  cif=yes  <- CIF only
```

## A second, worse defect found while fixing the first

`build_system.sh` hardcoded:

```sh
AMIDATE=yes   # "the free acid is the wrong species for every peptide in this panel"
```

That comment is true of the four *designed* peptides. It is false for
met-enkephalin, which the design specifies as **free acid** (`CYCLE3B_DESIGN.md`
line 79). Restoring met-enkephalin under the old script would have silently
built the amidated analog of the one control whose entire job is to sit at
ddG ~ 0.

This is the DRES incident of 2026-07-30 repeating in a different variable --
and in one respect worse. `AMIDATE` drives the chemistry (lines 152, 311), but
`chem.txt` recorded `SPEC_AMIDE`, the *table* value. If the two disagreed, the
build used one species and the provenance file claimed the other. Nothing
downstream could have detected it.

Fix (all three parts):
1. `AMIDATE=auto`, resolved from the design table via `load_peptide_spec`.
2. An explicit `--no-amidate` is cross-checked against the table and hard-fails
   on disagreement -- identical treatment to `DRES`.
3. `chem.txt` now records `$AMIDATE`, the value actually used, not the table value.

## Why the other five systems were stuck

Not GPU contention. Their 2026-07-29 build died at:

```
build_system.sh: line 176: syntax error near unexpected token `('
BUILD_EXIT=2
```

They retain `system.top` + `system.gro` but no `index.ndx`, `pepmeta.txt`, or
`contacts_pre.txt` -- all three required by `STAGE=gpu`. The syntax error is long
since fixed; they need the CPU stage re-run, which needs no GPU at all.

## Actions taken

| # | action | job |
|---|---|---|
| 1 | `prod_all.txt` 18 -> 24 rows; met-enkephalin as `amide=no dres=none`; all 8 tags verified to resolve through `load_peptide_spec` | - |
| 2 | `build_system.sh` amidation patch (3 changes above); installed on cluster, md5-verified identical, `bash -n` clean | - |
| 3 | met-enkephalin co-folds re-run with the *same* flags as the working six | `17962082` (pgpu) |
| 4 | CPU-stage rebuild of the five stalled systems | `17962083_[0-4]` (pshort_el8) |

Backups kept on cluster: `prod_all.txt.bak_18row`,
`scripts/build_system.sh.bak_amidebug`.

## Note on scheduling

`pshort_el8` had 4 idle nodes while everything waited on the single contended
`pgpu` node. The CPU array queued as `(None)` rather than `(Priority)` -- it is
not competing with `PRJNA845531_run`. The build work that does not need a GPU
should not have been sitting behind one.
