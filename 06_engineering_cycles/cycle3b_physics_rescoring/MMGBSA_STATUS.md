# MM-GBSA rescoring, status 2026-08-31

## Bottom line

The rescoring path is **validated end-to-end** on a real 20 ns trajectory. Four defects were
found and fixed getting there; one of them was silently emitting the wrong number.

Full 40-run array **18202158** (pibu_el8, 40 tasks, 20 concurrent, ~12 min each) was
submitted at 2026-08-31T16:21 CEST. The login node became unreachable shortly after, so its
completion is **unconfirmed**, see "Next actions".

## Validated result (smoke test, c3b_dtII_DOR rep1)

    deltorphin_II,OPRD1,1,-67.480

Job 18202148, COMPLETED in 12 min on pshort_el8 at 8 cores / 48 GB. No GPU needed.

Component breakdown from the delta block (kcal/mol):

| term | value |
|---|---|
| dVDWAALS | -72.54 |
| dEEL | -180.33 |
| dEGB | +196.07 |
| dESURF | -10.69 |
| dGGAS | -252.87 |
| dGSOLV | +185.39 |
| **dTOTAL** | **-67.48** |

Per design this is an enthalpy-dominated effective energy, not a binding free energy: no
entropy term, so absolute values are not affinities. Only differences (ddG) are interpretable.

## The four defects

### 1. Group index read back as empty string (would have failed all 40 runs)
`rescore.sh` read group numbers with `awk '/^\[ *Receptor *\]/{print n} /^\[/{n++}'`.
`Receptor` is the FIRST group, so `n` was still uninitialised: awk printed an empty string,
not `0`, and the `[ -n "$GREC" ]` check rejected it. `Ligand` worked only by being second.
Fixed with `print n+0` plus an END-block existence check; the assertion now also requires
numeric and distinct indices.

### 2. gmx_MMPBSA could not find cpptraj
`find_progs()` locates cpptraj/tleap/parmchk2/sander via
`shutil.which(path=os.environ['PATH'])`, it ignores the absolute paths used everywhere else
in the script. Fixed by exporting the env bin onto PATH.

### 3. PATH order is load-bearing (subtle)
`find_progs` uses ONE search path for every program and also picks up `gmx` from it. The
MM-GBSA env ships GROMACS **2023.4**, which cannot read a 2024.5 `.tpr` (`gmx check -s` →
"Error in user input"). So gmxcuda/bin must come FIRST, with the MM-GBSA env behind it for
AmberTools. Verified gmxcuda/bin does not shadow any AmberTools binary. The script now
asserts the resolved gmx is 2024.x+ and exits if not.

### 4. THE DANGEROUS ONE: wrong number, silently
gmx_MMPBSA prints four total rows: Complex, Receptor, Ligand (plain `TOTAL`) and the binding
delta, labelled with a **Unicode delta glyph** (U+0394) as `dTOTAL`. `collect_dg.py` matched
`(?:DELTA\s+TOTAL|Delta\s+TOTAL|TOTAL)` and took the LAST hit, which never matches the
glyph, so it returned the **ligand's absolute energy, -123.33**, instead of dG_bind, -67.48.

It passed the physical-range guard, because a ligand's absolute GB energy falls in the same
range as a plausible binding energy. This is exactly the failure mode that guard was written
to prevent, and it would have propagated into every downstream comparison.

Fixed: anchor on the `Delta (Complex - Receptor - Ligand)` header, stop at the next block
header, accept `d?TOTAL`, require exactly one match, and **cross-check that the printed
components sum to the printed total** (tolerance 0.15). Both negative controls verified:
a file with the delta block removed is refused, and a file with one component corrupted is
refused.

The one pre-existing row carrying -123.33 was quarantined to
`results_stage1.csv.POISONED_ligand_absolute_*`.

## Membrane handling: a methodological decision, not a bug fix

These are POPC-embedded GPCRs. gmx_MMPBSA's `cleantop()` strips water and ions from
`[ molecules ]` but KEEPS lipids, so `system.top` describes 274 POPC copies absent from the
receptor/ligand index → "The complex index has fewer atoms than the topology."

Rather than force it through, the assumption was measured: over the rescoring window the
peptide's minimum approach to the bilayer is **0.488 nm, with 0 of 1001 frames inside
0.4 nm**. The peptide stays in the orthosteric pocket and never touches lipid. Implicit-solvent
GB has no lipid phase anyway, so the receptor's lipid-facing solvation term is essentially
identical in complex and free receptor and cancels in `G_com - G_rec - G_lig`.

`scripts/strip_membrane_top.py` therefore writes a solute-only topology. It re-derives which
molecules are solute from the index and refuses unless the kept set is exactly the index and
contiguous from atom 1 (kept system1 x1 + system2 x1 = 5865 atoms; dropped 274 POPC, 88 Na+,
101 Cl-, 37488 WAT). `rescore.sh` re-measures the distance **per run** and exits 4 if contacts
exceed 1% of frames, so this assumption is verified for every replicate, never inherited.

## Files changed on the cluster

    scripts/rescore.sh              awk fix, PATH block, membrane gate, per-task CSV routing
                                    backups: .bak_awkfix .bak_pathfix .bak_memb .bak_percsv
    scripts/collect_dg.py           parse_dat rewritten; backup .bak_deltafix
    scripts/strip_membrane_top.py   NEW
    scripts/rescore_one.sbatch      NEW  single-run harness (pshort, 8c/48G)
    scripts/array_rescore.sbatch    NEW  40-task array (pibu_el8, 8c/48G, 4h)

Each array task writes `results_parts/<TAG>_r<REP>.csv`: 40 concurrent appends to one CSV
would interleave lines. They must be merged into `results_stage1.csv` after the array.

## Next actions

1. **Confirm array 18202158.** Once the login node responds:
   `sacct -j 18202158 -n -o State%12 | sort | uniq -c` and
   `grep -l RESCORE_OK logs/rescore_18202158_*.out | wc -l` (want 40).
2. **Merge the parts** into `results_stage1.csv`:
   `cat results_parts/*.csv | sort > results_stage1.csv`, then check it has 40 rows and
   8 distinct system/receptor pairs x 5 reps.
3. ~~**gate.py does not exist.**~~ **SUPERSEDED, it does exist**, at `scripts/gate.py`.
   This line was written before `RESUME_2.md` (2026-08-12) recorded it as already written
   and dry-run on synthetic data, and the gate was subsequently run to a verdict on
   2026-08-31 (`docs/GATE_VERDICT_BOUND.md`, verdict FAIL). Anyone reading this file for
   current state should read `GATE_VERDICT_BOUND.md` instead; this document predates the
   verdict. A stale "next action" was quoted as current on 2026-09-17 and led to a
   campaign being proposed that had already been run and had already failed.
4. Exit codes for triage: 2 = setup/consistency failure, 3 = chirality inverted (discard the
   run), 4 = peptide contacts bilayer (needs a membrane-aware model), 90 = /data not mounted,
   91 = disk guard.

## Still open from earlier

`/home` is at 20381M of 20480M (99.5%). Nothing in this pipeline writes there.


---

# UPDATE: array 18202158 complete

**31 of 40 runs scored. All 9 non-scored runs are the membrane gate (exit 4), no other
failure class.** Zero chirality discards, zero parse refusals, zero topology mismatches,
zero disk errors, zero mount races.

The gate turned out to measure something real rather than just protecting the method.

## The gate detected a binding-stability difference, not a pipeline fault

Escape into the bilayer is not random across systems: it is concentrated in the
peptide/receptor pairs that are pharmacologically mismatched:

| peptide | δ (OPRD1) mean contact | μ (OPRM1) mean contact | scored δ | scored μ |
|---|---|---|---|---|
| Met-enkephalin | 0.00% | 0.00% | 5/5 | 5/5 |
| Endomorphin-1 | 0.84% | 0.04% | 4/5 | 5/5 |
| Deltorphin I | 0.58% | 13.37% | 4/5 | 2/5 |
| Deltorphin II | 0.00% | 40.06% | 5/5 | 1/5 |

Deltorphins I and II are the δ-selective peptides in this panel. At δ they sit in the
orthosteric pocket for the whole window (deltorphin II: 0 of 5005 frames within 0.4 nm of
lipid). At μ they leave: deltorphin II rep3 spends **99.8%** of the window touching the
bilayer, rep1 93.1%. Met-enkephalin, which is not strongly selective, stays in the pocket at
both. Endomorphin-1, μ-preferring, stays at both.

So the failures are the *expected* result for a non-cognate pairing: the peptide is not held
in the pocket, drifts to the membrane, and MM-GBSA on a stripped topology becomes invalid:
correctly refused. This is informative, but note the direction of the bias it creates.

## Scored energies

| peptide | receptor | dG mean (kcal/mol) | SEM | n |
|---|---|---|---|---|
| Met-enkephalin | δ | -69.57 | 4.37 | 5 |
| Met-enkephalin | μ | -41.94 | 3.52 | 5 |
| Endomorphin-1 | δ | -54.95 | 4.81 | 4 |
| Endomorphin-1 | μ | -55.34 | 1.79 | 5 |
| Deltorphin I | δ | -65.95 | 2.19 | 4 |
| Deltorphin I | μ | -55.19 | 4.31 | 2 |
| Deltorphin II | δ | -66.72 | 0.89 | 5 |
| Deltorphin II | μ | -56.45 | (none) | 1 |

Selectivity (ddG = δ − μ; negative favours δ), computed only where both arms have n>=2:

| peptide | ddG | SEM |
|---|---|---|
| Met-enkephalin | -27.63 | 5.61 |
| Endomorphin-1 | +0.40 | 5.13 |
| Deltorphin I | -10.76 | 4.83 |
| Deltorphin II | not computable (n=1 at μ) |

## Read this with the survivorship bias in mind

**The deltorphin μ numbers are biased toward looking too good.** Only the μ replicates that
happened to stay in the pocket were scorable: 2 of 5 for deltorphin I, 1 of 5 for
deltorphin II. Those are the best-behaved tails of their own distributions, so the true
deltorphin ddG is very likely *more* δ-selective than the -10.76 above, not less. Do not
quote the deltorphin ddG as a point estimate.

Met-enkephalin and endomorphin-1 have complete 5/5 or 4/5 sampling on both arms and are not
affected by this. Met-enkephalin's -27.6 kcal/mol δ preference is the one clean selectivity
number in the set, and it is the largest effect here.

Also standing: these are enthalpy-dominated effective energies with no entropy term. Absolute
values are not affinities, and MM-GBSA systematically overestimates magnitudes. Only the
differences are interpretable, and only within this consistent protocol.

## Recommended next step

Escape is a **binding-stability observable in its own right** and it is already measured for
all 40 runs: `systems/*/rep*/mindist_ligand_memb.txt`. Reporting residency time alongside
ddG uses the 9 runs the energy pipeline had to discard, and it is the part of this result
least sensitive to MM-GBSA's known weaknesses.

If the deltorphin/μ energies are actually needed, they require a membrane-aware model
(gmx_MMPBSA `ipb`/membrane options) rather than a stripped topology, the gate is correct to
refuse them, and forcing them through would produce exactly the plausible-looking wrong
number that the parser fix was written to prevent.
