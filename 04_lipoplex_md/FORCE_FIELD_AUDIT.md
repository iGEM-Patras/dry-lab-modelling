# Force-field audit: why the version numbers differ, and why that is correct

**Date:** 2026-09-24 · Prompted by a reasonable observation that the topologies appear to
mix MARTINI 2.1 and 2.2 files. They do not. This records the evidence so the question does
not have to be re-litigated.

## Finding 1: there is no version mix. `martini_v2.2.itp` is never loaded.

Every `#include` line across all seven lipoplex and Cycle 10 topologies
(`nochol/DOTAP.top`, `nochol/MC3.top`, `asmB2/top_B.top`, `asmB2/top_L.top`,
`cycle10/condB.top`, and the three production replicates) resolves to one stack:

```
martini_v2.1-dna.itp          master table: defaults + atomtypes + nonbond_params
martini_v2.0_lipids.itp       DOPE and the phospholipid set
martini_v2.0_CHOL_bonded.itp  cholesterol (the -DFLEXIBLE variant)
MC3.itp / DOTAP.itp           ionisable and cationic lipids (analogy models)
water_ions.itp                NA, CL
dna_duplex.itp, si21.itp      the two cargoes
```

`martini_v2.2.itp` is present in `ff/` and included by **nothing**. It is an unused file
sitting beside the one in use, which is itself a hazard for the next reader.

## Finding 2: the two files are alternatives, not layers, and 2.1-dna strictly dominates

Both carry their own `[defaults]`, `[atomtypes]` and `[nonbond_params]`, so exactly one may
be loaded. Measured:

| | atomtypes | nonbond_params | `[defaults]` |
|---|---|---|---|
| `martini_v2.1-dna.itp` | **111** | **4774** | `1 2` |
| `martini_v2.2.itp` | 39 | 780 | `1 1` |

- **Atomtypes unique to 2.2: zero.** All 39 of its types are present in 2.1-dna.
- Atomtypes unique to 2.1-dna: **72** (including every nucleobase bead (`TA2 TA3 TG2 TG3
  TC1–TC5 TT2 TT3 TY2 TY3`), the virtual-site types (`v*`, `vS*`), the split
  donor/acceptor variants (`Pa Pd SPa SPd`), and `D`/`DUM`.

So switching everything to 2.2 would gain nothing and **lose the bead types both cargoes
are built from**. MARTINI 2.2 is the *protein* revision (Monticelli 2008, de Jong 2013); it
never defined nucleic-acid parameters.

The `[defaults]` line is a second, independent incompatibility: **combination rule 2 vs 1.**
Under GROMACS semantics that means 2.1-dna's `nonbond_params` are σ/ε while 2.2's are
C6/C12: the numbers are in different units. Loading the wrong table would not merely drop
types, it would misread every pair interaction.

A natural guard exists: `W` is defined in *both* master tables, so loading both makes
`grompp` fail on a duplicate moleculetype rather than silently proceed.

## Finding 3: no protein is present, so the protein-revision question does not apply

Condition B `[molecules]`, read from `asmB2/top_L.top`:

```
DNA 1 · SI21 1 · MC3T 120 · DOPE 80 · CHOL 40 · W 20030 · NA 294 · CL 316
```

No protein in any lipoplex or Cycle 10 system. The 2.1-vs-2.2 difference is entirely a
protein parameter difference, and the MARTINI IDP variants likewise have nothing to act on
here. A broad search (`*idp*`, `*2.2p*`, `*elnedyn*`) found **no MARTINI IDP parameter set
on the cluster** (the only `idp` hits were `IDP.pkl` / `A1IDP.pkl` in the structure
predictor's molecule cache, which are PDB ligand codes and unrelated.

**Where IDP parameters *would* matter:** engPENK is ~83 % disordered by our own pLDDT
analysis. Any future cycle modelling engPENK in solution, or packaged inside the lipoplex,
would over-collapse the chain under standard MARTINI 2 protein parameters, and the IDP
rescaling would then be the correct choice. That is a real future concern and not a defect
in anything that has run.

## Finding 4: molecule provenance, one file each

| molecule | defined in |
|---|---|
| DNA | `dna_duplex.itp` |
| SI21 | `cycle10/build/si21.itp` |
| MC3T | `MC3.itp` (analogy model) |
| DOPE | `martini_v2.0_lipids.itp` |
| CHOL | `martini_v2.0_CHOL_bonded.itp` (also in `martini_v2.0_CHOL.itp`, not included) |
| W | `martini_v2.1-dna.itp` |
| NA, CL | `water_ions.itp` |

## Conclusion

Uneven component version numbers on one shared interaction matrix is the conventional
MARTINI 2 arrangement: each component sits at its own latest published version. That is
categorically different from mixing MARTINI 2 with MARTINI 3, which is invalid, and which
is why the MARTINI 3 route stays closed until nucleic-acid and ionisable-lipid parameters
exist for it.

`methods_references.md` already records this correctly as *"v2.1 for DNA, v2.0 for
lipids/cholesterol"*. One cleanup applied: the Monticelli protein citation is now annotated
as table provenance rather than left implying protein parameters are in use.

## Recommended tidy-up (not yet done, would touch files a running job may read)

Move `ff/martini_v2.2.itp` and `ff/martini_v2.0_CHOL.itp` into `ff/unused/`. Both are
shadowed by the files actually included, and both are the kind of thing that invites exactly
this question again.
