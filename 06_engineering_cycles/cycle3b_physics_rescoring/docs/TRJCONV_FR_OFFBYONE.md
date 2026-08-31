# trjconv -fr frame numbering is 1-based — defect note

**Found:** 2026-08-31, first bound-mode run (c3b_dtII_MOR rep3).
**Severity:** would have scored the wrong frames, silently, with a plausible number.

## What happened

`rescore.sh` BOUND_MODE selects frames where the peptide is in the pocket, writes their
indices to an index file, and passes it to `gmx trjconv -fr`. The selection code emitted
0-based indices, matching the Python enumeration of the per-frame .xvg series.

`trjconv -fr` numbers frames **1-based**. Index 56 extracted t = 550 ps — the 56th frame —
not t = 560 ps, which is what index 56 means in the .xvg. Every scored frame was the one
immediately before the intended frame.

## Why it was caught

Not by the frame logic, which reported success. It was caught by the membrane
*verification* step: bound mode re-measures ligand–lipid distance on the extracted window
and refuses if any frame is in contact, because selection guarantees none are. It found
15/100 contacting frames and exited 5 with "selection is broken".

That check existed only because bound mode repurposed the original membrane gate from
filter to verification rather than deleting it as redundant. Had it been deleted, the run
would have completed and produced -70-something kcal/mol — indistinguishable from a
correct answer.

PBC treatment was ruled out as a cause by extracting with and without `-pbc mol` and
getting byte-identical distances.

## Fix

1. Emit `i + 1`, with the convention and the date it was verified written at the emit site.
2. Add a **direct** check: after extraction, compare the window's actual time column
   against the intended selection times, tolerance 1 ps, and exit 6 on mismatch.
   The contact gate infers an indexing error; this one names it.

## Generalizable lesson

Same shape as the collect_dg.py delta-parse defect (see COLLECT_DG_DELTA_BUG.md): a wrong
value that lands inside the plausible range is invisible to range checks. Both were caught
by a *relational* check — components must sum to the total; extracted times must equal
requested times — not by a plausibility check.

When an off-by-one is possible, do not reason about the convention. Extract one element and
compare it against what you asked for.
