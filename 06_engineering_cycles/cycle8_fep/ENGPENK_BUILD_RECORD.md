# engPENK system build: record and verification

**Date:** 2026-09-19 · **Status:** both systems built, minimised and verified · no GPU required

The two target systems for the free-energy campaign, `YGGFEVVG` bound to OPRD1 (δ) and OPRM1 (μ).

## Provenance of the starting poses

Cycle 7's co-folds declared the peptide as a **SMILES ligand**, which yields correct chemistry
but no backbone topology: `tleap` cannot parametrise it. Cycle 8 therefore re-ran the co-folds
with the peptide as a **protein chain**. Two practical notes for anyone repeating this:

- **Boltz-2 writes mmCIF, not PDB.** Four attempts were recorded as failures before it was noticed
  that a search for `*model_0.pdb` finds nothing in a successful Boltz output tree. Prediction had
  in fact succeeded in about 7 minutes once the sequence alignment was cached.
- Re-typing the peptide dropped interface confidence from **ipTM 0.958 (ligand form) to 0.863 (δ)
  and 0.874 (μ)**. Lower and more believable. δ and μ remain near-identical, which is a third
  independent line showing ipTM cannot discriminate these two receptors, consistent with Cycle 7's
  B2 gate failure.

## Chemistry declaration

Taken from the design table's own convention, not a default. `prod_all.txt` records all four
designed peptides as `amide=yes` and met-enkephalin (the neutral reference) as the single
`amide=no` entry. `YGGFEVVG` as released by the processing cascade is a **free acid**, so both
Cycle 8 tags are declared `amide=no, dres=none` in a separate `prod_cycle8.txt` via the
`PROD_TABLE` override, leaving Cycle 3b's table untouched as the record of what Cycle 3b ran.

The build **refused to run** when that table was absent: *"refusing to guess peptide chemistry"*,
which is correct behaviour, since amide and free acid are different molecules.

## Build

Stages 1–5 on `pshort_el8` (CPU), minimisation on `pibu_el8` with `MIN_NB=cpu`, the path documented
in [`MIN_ON_CPU.md`](../cycle3b_physics_rescoring/MIN_ON_CPU.md). **No GPU was used at any stage**,
so the `pgpu` outage never blocked this work.

| | c8_engPENK_DOR | c8_engPENK_MOR |
|---|---|---|
| system | 76,126 atoms, 16,345 residues | 96,951 atoms, 21,486 residues |
| bilayer | 540 POPC | 660 POPC |
| solvent | 15,357 waters, 28 Na⁺, 40 Cl⁻ | 20,316 waters, 48 Na⁺, 54 Cl⁻ |
| box (Å) | 89.9 × 89.9 × 121.1 | 97.5 × 97.7 × 128.4 |
| tleap | 0 errors | 0 errors |
| peptide | residues 373–380 | residues 401–408 |
| minimisation | PE −8.845 × 10⁵, F_max 985 | PE −1.155 × 10⁶, F_max 968 |
| interface, pre → post | **0.99 → 2.64 Å** | **1.95 → 2.68 Å** |
| pairs < 2.6 Å after min | **0** | **0** |

Minimisation took roughly 90 s per system on 16 cores. Steepest descent to `emtol = 1000` is a
convergence problem, not a sampling problem; the GPU buys nothing that justifies queueing for it.

## Verification

**C-terminus is a free acid.** The built topology carries both carboxylate oxygens on the terminal
glycine, `O` and `OXT`, both typed `O2`, with residue charge −1.

*Correction to an earlier check:* a post-build assertion reported `OXT present: 0` and was recorded
as a failure. It inspected `pep_chir.pdb` (the **pre-tleap** intermediate) whereas `tleap` adds
OXT during assembly. The property asserted was right; the file was wrong. `YGGFEVVG` has 58 heavy
atoms as predicted, 59 once OXT is added.

**The canonical pharmacophore formed without being asked for.** Post-minimisation contacts:

| contact | distance | |
|---|---|---|
| `ASP128:OD2, TYR373:N` (δ) | 2.65 Å | D3.32 anchoring the peptide's N-terminal amine |
| `ASP149:OD2, TYR401:N` (μ) | 2.68 Å | the equivalent residue in OPRM1 |
| `ARG192:NH1, GLY380:OXT` (δ) | 2.65 Å | the free-acid C-terminus in a salt bridge |

Asp3.32 is the conserved opioid-receptor residue that salt-bridges the protonated amine of every
opioid ligand. Its spontaneous formation in both systems is independent evidence the pose is sane.

**Chirality: all five chiral centres are L, in both systems.** This check is mandatory rather than
optional, because `build_system.sh` **skips its own chirality gate when `dres=none`**, correct for
an all-L peptide, and the same coupling that once allowed an all-L analogue of deltorphin II to pass
every downstream check. ff14SB has no D-amino-acid templates, so handedness carries no energetic
term: the force field is **enantiomer-blind** and cannot detect an inversion. Verification must be
external.

Confirmed two independent ways:

| residue | `chirality.py assert` | signed volume V (δ / μ) |
|---|---|---|
| Tyr1 | L (rc = 2) | +2.37 / +2.13 |
| Phe4 | L (rc = 2) | +1.82 / +2.13 |
| Glu5 | L (rc = 2) | +2.19 / +2.61 |
| Val6 | L (rc = 2) | +3.04 / +2.05 |
| Val7 | L (rc = 2) | +1.28 / +2.00 |

Gly2, Gly3 and Gly8 are achiral.

*Correction:* the first independent calculation reported **all five centres as D**, a catastrophic
result that would have condemned both systems. It was wrong. The triple product was correct but the
L/D test was inverted, against the convention stated in `chirality.py`'s own docstring (*"L-amino
acids give V > 0"*) which had been printed four lines earlier in the same output. Every measured V
was positive, i.e. L. The false alarm was caught only because the raw values were printed beside
the verdict.

## Standing lesson from this build

Three checks in this one build were wrong about the thing they were checking: a gate reported
`ORIENT_OK` on a system containing zero peptide atoms; an OXT assertion inspected the pre-tleap
intermediate; and a chirality test inverted its sign and condemned a correct structure. Each was
caught by a raw number printed next to the verdict, never by the verdict itself.

**Print the quantity, not just the conclusion.** A verdict cannot be cross-examined; a number can.

## Next

Equilibration, then the two engPENK legs join the λ-window queue. The control arm is unaffected
throughout.
