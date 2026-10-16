# PEG-lipid: not in any simulated system, buildable, blocked on one atomtype

**Date:** 2026-09-25 · Prompted by a wet-lab formulation note arguing for
`PEG(2000)-CerC8` at 5 mol%, which conflicts with this repo's own bench spec.

> **Resolved 16 Oct 2026.** The conflict is closed in favour of the wet lab, whose protocol
> and bench spec both specify **DMG-PEG2000 at 1.5 mol%**. `antibody_assessment.md` has been
> corrected. The CerC8 figures below are retained because they document what was modelled at
> the time, not what is being made.

## The gap

**No simulated system contains a PEG-lipid.** Read from the `[molecules]` blocks of every
topology found on disk:

| system | composition |
|---|---|
| `asm/sw_MC3_bonded.top` (the 200 ns reference) | DNA 1 · MC3T 120 · DOPE 80 · CHOL 40 · W 23934 · NA 370 · CL 432 |
| `cycle10/asmB2/top_L.top` (condition B) | DNA 1 · SI21 1 · MC3T 120 · DOPE 80 · CHOL 40 · W 20030 · NA 294 · CL 316 |
| `nochol/MC3.top` | DNA 1 · MC3T 120 · DOPE 80 · W 26003 |

Meanwhile `targeting/lipoplex_formulation_spec.csv` lists **DMG-PEG2000 at 1.5 mol%** in
arms B1 and B2, and labels B1 *"MC3 LNP, MD-matched + PEG"*. The "+ PEG" was never
modelled. That is a real gap between the bench spec and the simulations, and it is now
recorded rather than implied.

## Feasibility: buildable

`polyply 1.8.0` ships PEO in its **installed library** (not merely test fixtures):

- `polyply/data/martini2/PEO.martini.2.itp`
- `polyply/data/martini3/PEO.martini3.ff`

Generation was tested, not assumed:

```
polyply gen_params -lib martini2 -name PEO45 -seq PEO:45 -o peo45.itp
  -> 45 atoms, all bead type EO
```

45 EO beads ≈ PEG2000 (44.3 monomers at 44.05 g/mol). Topology kept as `peo45.itp`.

## The blocker: one missing atomtype

The generated chain uses bead type **`EO`**, and `EO` is **absent from the master table our
systems load**:

| table | `EO` atomtype |
|---|---|
| `martini_v2.1-dna.itp` (loaded by every system) | **0, absent** |
| `martini_v2.2.itp` (loaded by nothing) | 0, absent |

So `grompp` would reject a PEG-containing topology until the `EO` atomtype **and its full
`nonbond_params` row against all 111 existing types** are added. That is a force-field
extension, not a build step, and it must come from the published Grunewald/Rossi PEO
parameterisation rather than be invented, the paper polyply itself cites
(doi:10.1021/acs.jpcb.8b04760).

## Anchor chemistry

The two candidate PEG-lipids differ in anchor, and the wet-lab note's argument is about
exactly that: a short C8 anchor is claimed to desorb quickly after endocytosis, while C14
and C20 anchors hinder membrane engagement.

| lipid | anchor | precedent on this cluster |
|---|---|---|
| `DMG-PEG2000` (our bench spec) | C14 diacyl glycerol | none |
| `PEG2000-CerC8` (the note) | C8 ceramide | **`CER` exists in `martini_v2.0_lipids.itp`** |

So the lipid the note argues for has *more* topology precedent here than the one our own
spec lists. Neither is parameterised as a PEG-lipid; both would need the anchor joined to
the PEO chain, in the same analogy-model class as the existing MC3 and DOTAP topologies:
and carrying the same disclosure.

## Cost, if built

At 240 lipids in condition B:

| source | PEG mol% | PEG molecules | extra beads |
|---|---|---|---|
| bench spec | 1.5 % | 3.7 | ~164 |
| wet-lab note | 5.0 % | 12.6 | ~568 |

Negligible against 24k beads. Compute is not the constraint.

## Recommendation: a new arm, not a retrofit

**Do not add PEG to Cycle 10 condition B.** Its entire purpose is a like-for-like contrast
against the existing PEG-free 200 ns reference; adding PEG to one side confounds the one
comparison the cycle is built on.

If the C8-vs-C14 desorption question is worth testing, it is its own cycle: two systems
identical but for anchor length, with desorption as the pre-registered read-out. Until then
**the anchor recommendation is a bench decision with no dry-lab backing**, and should be
described that way in the PI briefing rather than as a modelled result.

## Method note: this check was wrong the first time

The first attempt searched `*peg*` across the filesystem and "found" `libnvjpeg.so`,
`jpegtran` and `America/Winnipeg`. It also queried polyply with `-list-lib` and
`-list-blocks`, neither of which exists, so polyply errored asking for `-seq`, leaving the
capability question **unanswered** while the output looked like a negative result. A third
search for a `library/` directory failed because polyply ships `data/`.

Had the first result been believed, the conclusion would have been "no PEG parameters
available" when PEO ships in the installed library for both force-field generations. Same
failure mode as the unpadded-glob window count and the `head -3` legend truncation
recorded in `cycle8_fep/CYCLE8_FIRST_RESULT.md`: **a limited instrument reporting absence,
read as evidence of absence.** Caught here only because "Winnipeg" is visibly absurd in a
force-field search.
