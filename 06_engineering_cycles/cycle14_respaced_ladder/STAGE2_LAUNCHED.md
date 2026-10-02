# Cycle 14 · Stage 2 launched

**2026-10-03.** 13 workers, 228 windows, 684 ns, CPU on `pibu_el8`. ~4.5 days.

| | |
|---|---|
| ladder | 57 states, equal thermodynamic length, corner at state 26 |
| predicted overlap | ~1.0 kT per interval, against a previous maximum of 10.56 |
| legs | met-enkephalin × {DOR, MOR} × {r1, r2} |
| replicates | independent equilibrations — fresh velocities **and** own NVT/NPT |
| hardware | CPU only, matching the comparator legs from Cycle 8 |

Gates were committed before any window ran: see `data/cycle14_prereg.json`. The
engPENK stage runs **only** if this control clears its sign and accuracy gates
against the published **+0.81 kcal/mol**.

---

## Two verification failures of mine, caught before launch

### 1 · The first window generation inherited the wrong peptide's protocol

All 228 windows built cleanly — from `c3b_menk_*` structures but with the production
protocol of **`c3b_em1_DOR_rep1`**, the endomorphin-1 leg, for all four met-enkephalin
legs.

My path candidates were `cycle8_prod/${S}_r1/w00.mdp`. The completed campaign's
directories are named `_rep1`; my equilibration directories are named `_r1`. Both
candidates missed, and a `find` fallback took the **first** `w00.mdp` on disk among
sixteen production directories.

Those 228 inputs were deleted and rebuilt from explicitly named per-receptor sources
with no fallback.

**It would probably have produced correct physics by coincidence** — the endomorphin-1
protocol declares `couple-moltype = system2`, and `system2` is also the peptide in the
met-enkephalin topologies, because both were built by the same pipeline. That is luck,
not a protocol, and nothing in the check would have caught a source whose `couple-moltype`
pointed at a differently-numbered moleculetype.

### 2 · The check meant to catch it could not

The generation job ran `gmx dump -s w00.tpr | grep -iE "couple|init-lambda-state"` and
printed `nsttcouple` and `nstpcouple` — but **not** `couple-moltype`, because `gmx dump`
does not emit that directive. This was already established earlier in this campaign by
running the same query against a known-good file and finding it absent there too.

I wrote a verification that cannot verify, and it passed.

**Identity is now settled by counting atoms in the fully-included topology:**

| moleculetype | DOR | MOR | |
|---|---|---|---|
| `system1` | 5,755 | 6,309 | receptor |
| **`system2`** | **75** | **75** | **met-enkephalin `YGGFM`** ← coupled |
| `system3` | 134 | 134 | membrane lipid |

75 atoms is met-enkephalin with hydrogens. The lipid at 134 is the molecule an atom-count
*range* matched alongside the peptide earlier in this campaign, which is why identity is
settled by exact count rather than a window.

---

## What the worker fixes, from failures this campaign already paid for

**It holds a claimed window to completion.** The original workers gave each window a
fixed two-hour stint, released it, and exited after one pass — which is why the first
campaign reached 51.6% of its sampling with only 6 of 108 windows closed. This loops
until nothing is left to claim.

**It refuses a leg with fewer than 57 inputs.** A partial window set is how that same
campaign spread effort across windows it could never finish.

**The progress gate aborts rather than retries.** A window that advances no simulated
time has failed deterministically; a retry loop treating it as transient is how an
earlier run reported success on a window that made no progress. Exit 95, naming the
window.

**48 cores rank-heavy**, per the provider notes. The 8-core configuration carried over
from the GPU partition is substantially suboptimal on this partition.
