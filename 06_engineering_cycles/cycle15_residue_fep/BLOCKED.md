# Cycle 15 — blocked on tooling, not on science

**9 Oct 2026. The W284K hybrid residue is built and verified. It cannot be run in this
system, for a reason that has nothing to do with the free-energy method.**

## What was achieved

| step | status |
|---|---|
| pmx installed (from source; absent from PyPI) | done |
| force field identified as **AMBER ff14SB** | done |
| target residue verified as TRP284 in the coordinates | done |
| W284K dual-topology hybrid residue built | **done — 37 atoms** |
| both side chains confirmed present | TRP ring + `DCG DCD DCE DNZ` + `HV1–HV9` |
| B-state charges verified atom by atom | `qA 13.000 -> qB 14.000`, Δ = +1 |
| coordinates spliced into the membrane system | **done — 76,139 atoms** |
| topology accepted by GROMACS | **BLOCKED** |

The hybrid itself is correct. `DNZ` carries `N3, q = -0.3854` with three `HV` hydrogens at
`+0.340` each — a genuine lysine ammonium, and the net charge changes by exactly +1 as a
real W→K must.

## Why it is blocked

The system was built with **Amber tooling and converted by ParmEd into a standalone GROMACS
topology** — every bonded parameter written out explicitly, no `#include`, no `[bondtypes]`
tables. pmx produces a pdb2gmx-style topology that looks parameters up by atom type. The two
formats cannot be combined, and both routes out are closed:

**Route 1 — include the force field's bonded tables alongside the inlined parameters.**
Fails: `Unknown bond_atomtype CM`. `ffbonded.itp` references bonded-type names declared in
the force field's own `[atomtypes]`, which a ParmEd topology neither declares nor has a
column for.

**Route 2 — merge at the ParmEd Structure level, where both sides are explicit.**
Fails: `MoleculeError: Cannot bond two virtual sites/extra points together`. The dummy atom
types have atomic number zero, so ParmEd classifies them as virtual sites — and a
dual-topology hybrid requires precisely what it forbids, the dummy lysine chain bonded to
itself. **ParmEd has no representation for alchemical dual topologies.** This is not a
setting.

## What would unblock it, and what it costs

| option | work | risk |
|---|---|---|
| Rebuild the system with a GROMACS-native, include-based toolchain | days — effectively redoing the membrane system build | moderate; a new system is not the equilibrated one the other cycles used |
| Hand-construct B-states for 37 atoms inside a 56,000-line topology, converting type-lookup bonded parameters to explicit ones | ~1 day of careful scripting | **high, and silent** — a wrong dihedral would run cleanly and return a plausible wrong number |
| Run the mutation without the membrane | ~0.5 day | the receptor distorts without a bilayer; a ΔΔG from a deformed receptor is not interpretable |

## Recommendation

**Stop here.** Not because the method is wrong — it is the right method, and it is the one
route that escapes both failure modes that killed the previous five. But:

1. The blocker is the **provenance of this particular system**, and every way around it
   either rebuilds the system or hand-edits parameters where an error would be invisible.
2. Even complete success answers *which pocket residues drive δ/μ discrimination* — **not
   what `YGGFEVVG` does.** No computational route now available answers that.
3. A wet-lab cAMP assay measures the quantity directly, in a day of bench time, subject to
   none of this.

The hybrid residue, the verified charges and the setup procedure are all recorded. If the
system is ever rebuilt with an include-based toolchain, this cycle resumes from a validated
starting point rather than from scratch.
