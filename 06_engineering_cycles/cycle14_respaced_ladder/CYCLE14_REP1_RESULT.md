# Cycle 14: replicate 1 of the met-enkephalin control

**Scored 7 Oct 2026, against gates committed in `data/cycle14_prereg.json` before the
campaign started.**

## The number

| | |
|---|---|
| decoupling, DOR | 2349.53 ± 10.84 kJ/mol |
| decoupling, MOR | 2346.53 ± 7.35 kJ/mol |
| **ΔΔG (δ over μ)** | **+0.72 ± 3.13 kcal/mol** |
| published met-enkephalin | **+0.81 kcal/mol** |
| deviation | 0.09 kcal/mol |

BAR over all 56 λ intervals, every trajectory segment per window (124 xvg files for
DOR, 87 for MOR). Both legs verified at 57/57 before BAR was run; the job was written
to refuse a partial ladder.

## Gates

| Gate | Criterion | Result |
|---|---|---|
| G1 | sign correct (positive = δ-preferring) | **pass** |
| G2 | interval covers the published value | **pass** |
| G3 | λ-interval overlap (property of the ladder) | pass by construction: predicted ~1.0 kT vs the old ladder's max 10.56 |
| G4 | replicate agreement | **not yet testable**: rep2 is incomplete |

## What this does and does not license

**Does.** The re-spaced ladder produced the correct sign and a central value 0.09
kcal/mol from the literature. The old 27-window ladder gave **−3.12 and +5.41** on this
same control, replicates differing only by thermostat seed. That is a real improvement
and it vindicates the diagnosis: the failure was λ spacing, not sampling time.

**Does not.** The uncertainty is **3.9× the effect being measured**. The interval runs
+3.85 to −2.41 kcal/mol: from 661-fold δ-preferring to 58-fold μ-preferring. An
agreement of 0.09 kcal/mol inside a window of ±3.13 is *consistent with* accuracy; it is
not evidence of it, and it is equally consistent with coincidence. One replicate cannot
distinguish the two.

**No value for `YGGFEVVG` may be quoted on the strength of this.** The pre-registration
requires G4, and G4 needs rep2. If the two replicates agree, the protocol has earned the
right to produce a number for the engineered peptide. If they disagree the way the old
ladder's did, the method is still not resolving this effect and the honest conclusion is
that the cAMP assay decides it.

## Operational note

The waiting analysis job hit its 11-hour limit at almost exactly the moment the last
DOR window finished, so it exited without computing. The number above came from a job
submitted directly afterwards. Recorded because the near-miss is the kind of thing that
otherwise gets remembered as "the automation worked".
