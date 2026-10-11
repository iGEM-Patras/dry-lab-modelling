# Cycle 17: engagement-order docking. Tooling works, no gate scored yet.

**11 Oct 2026. Honest status, written because the work stopped on a cluster outage
rather than on a result.**

## What was achieved

| | |
|---|---|
| Native reference found | **PDB 8F7S**, delta-opioid receptor with deltorphin. Verified from the deposited coordinates: chains R/D receptor, P/Q peptide `TYR1 DAL2 PHE3 GLU4 VAL5 VAL6 GLY7 NH2` |
| Shared with our payload | **`FEVVG`**, five residues. `YGGFEVVG` vs `YAFEVVG`. **The first time in this project that a computational question about the payload has had an experimental bound reference** |
| CABS-dock ported | Python 2 (2019) to Python 3: **eleven** distinct fixes, documented in `PORT_NOTES.md` |
| Engine verified running | A tiny simulation reached **99.1% and completed in 7 s** |
| Cost measured | Full protocol is **~1.5-3 h per simulation**. The preprint's 1,000 simulations is therefore 1,750-3,000 core-hours per peptide, and two peptides are needed |

## What was NOT achieved

**No gate was scored.** G1 (can blind docking re-find the crystal pose?) has never run at
real sampling. The last verification run's output could not be read back: the login node
returned empty after 26 minutes.

## The porting bugs worth knowing about

Two would have been silent rather than loud:

- `szip` returns a `zip` object. Python 3 exhausts it on first use, so the second `filter`
  over it returns nothing: a wrong secondary-structure assignment with no error.
- The default `gfortran -O2` **emitted a binary alongside `relocation overflow` link
  errors**. A binary produced with errors in the link is not trustworthy; rebuilt with
  `-mcmodel=medium -std=legacy`.

And one cost a full diagnostic round: a py2 `exception.message` handler **masked the real
error**, so one attempt reported only that something had failed.

## Honest accounting of why this took so long

Six failures were mine, not the method's: inputs read from the wrong directory; a compiler
called missing when it was an unloaded module; the masked exception; and **three separate
occasions where I killed a run with my own timeout and read the result as a failure**. The
last of those is the worst: the progress bar reads the engine's `PROGRESS` file and swallows
a partial read as `0`, so a working simulation displayed `0.0%` for 105 minutes and I
believed it was hung.

## Standing limits, unchanged

Three deviations from the published protocol, all declared before anything ran:

1. **No membrane term.** Not in the public release.
2. **No DSSP.** Receptor modelled without assigned secondary structure.
3. **No D-amino acid or C-terminal amide.** CABS is coarse-grained on L-amino-acid
   statistics, so the deltorphin control is L-Ala free-acid: stripped of exactly the two
   features the Cycle 16 literature attributes its rigidity to. **This is the most damaging
   of the three** and would have to sit beside any result.

**And the ceiling has not moved.** Even complete success answers which domain engages first.
It does not give a delta/mu selectivity value for `YGGFEVVG`, and nothing computational
available to this project does. The cAMP assay remains the only instrument for that.

## Recommendation

Run **G1 only**, deltorphin only, 100 simulations: about 200 core-hours, which is a fraction
of the full study. If blind docking without the membrane term cannot re-find a crystal pose,
the question is settled cheaply. Do not commit to the full two-peptide study before that
gate passes.
