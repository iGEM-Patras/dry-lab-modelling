# Lock semantics in the Cycle 14 worker: read this before touching `locks14/`

Written after I corrupted the campaign's bookkeeping by assuming what the locks meant
instead of reading the worker. Nothing was lost, but only because the arithmetic that
should have stopped me also happened to be what diagnosed it.

## The lock is a claim AND a completion marker

```bash
mkdir "$LK/${LEG}_${w}"            # claim: atomic, succeeds for exactly one worker
...
if [ "$after" -ge 1500000 ]; then
    echo "    $w COMPLETE"         # lock RETAINED, deliberately
else
    rmdir "$LK/${LEG}_${w}"        # released only when unfinished
fi
```

A lock on a finished window is **not** a leak. It is what stops another worker
re-claiming it.

## Why the lock has to carry that job

The worker's completion test parses the step from the mdrun log:

```bash
grep -oE "^ *Step +[0-9]+" "$f" | tail -1 | awk '{print $2}'
```

**This never matches.** GROMACS does not write a `Step <n>` line; the step appears in a
two-line table with the header on one line and the values on the next. So `$last` is
always empty, `[ -n "$last" ] && ...` never fires, and the worker cannot tell a finished
window from an unstarted one by reading the log.

The lock is therefore the only completion state that exists.

## The invariant

```
locks held  ==  windows complete  +  windows actively running
```

Check this before concluding anything about the lock directory. When I looked at
**82 locks against 24 live workers** I read it as "58 orphans". The campaign had
**59 complete windows at the time**: 59 + 24 = 83. The invariant was holding to within
one window and I called it a stall.

## How to tell completion reliably

Not from the log. From the dH/dλ output:

```bash
tail -1 ${w}_run*.xvg | awk '{print $1+0}'      # >= 2999 ps means done
```

Verified against a window with `Finished mdrun` in its log where the step parser
returned nothing at all.

## If you must clean locks

1. Dry-run first and print the classification. Do not delete in the same pass.
2. Assert the leg directory exists. A wrong path makes every window look empty, which
   presents as "everything is orphaned": that is exactly what happened, the lock names
   already contain the `prod_` prefix, and building `$W/prod_$LEG` gave
   `$W/prod_prod_...`, so all 82 entries reported `step0` and age `999999s`.
3. Treat an impossible-looking unanimous result as a bug in the query, not a finding.

## Known real defect, not yet fixed

The worker has **no `trap`**, so a worker killed at its SLURM walltime leaks a genuine
claim lock. That window then needs manual release, distinguishable from a completion
marker by the dH/dλ test above. Worth fixing when the campaign is idle; not worth a
disruptive change mid-run.
