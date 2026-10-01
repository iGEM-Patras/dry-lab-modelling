# Cycle 12 — is the engPENK binding pose independently reproducible?

**Question.** Cycle 8 returned ddG = -8.91 +/- 3.34 kcal/mol for engPENK (met-enkephalin-
anchored), implying ~3.4 million-fold mu-preference against ~7,700-fold for the most
mu-preferring of 3,579 measured opioid ligands. The met-enkephalin control PASSED
(+0.97 +/- 1.00 vs +0.81 published), which localises the fault to the engPENK legs
rather than to the method. The starting pose is the leading suspect.

**Test.** Dock YGGFEVVG into both receptors with AutoDock CrankPep — a method independent
of the co-folding predictor that produced the TI pose — and ask whether it reproduces that
pose. Gates were fixed in `cycle12_prereg.json` before ADCP was installed.

Protocol: 50 replicas x 300,000 steps per receptor, into the **equilibrated** receptor
conformers the TI sampled from. The docking box was defined from receptor pocket residues,
never from the pose under test, so agreement could not be built in.

## Result

| peptide | receptor | closest pose over all sampled | 2.5 A gate |
|---|---|---|---|
| met-enkephalin (control) | DOR | 1.63 A | **pass** |
| met-enkephalin (control) | MOR | **0.93 A** | **pass** |
| engPENK | DOR | 3.11 A | fail |
| engPENK | MOR | 3.10 A | fail |

Not one of 9,461 sampled engPENK conformations met the gate in either receptor.

**G2 (anchor contact) passed**, which is what makes the failure interpretable. The
equilibrated reference makes a textbook salt bridge from the peptide N-terminal amine to
Asp3.32 (2.71 A in DOR, 2.74 A in MOR) and ADCP finds it independently (2.35 / 2.36 A),
with 25-29% of near poses making the contact. The docking works; its disagreement is a
measurement, not noise.

## The matched control is what makes this conclusive

A first reading of the engPENK data alone suggested the MOR leg was the suspect one,
because the DOR message tetrapeptide superimposed at 1.77 A while MOR's deviation was
global and displaced the anchor residue by 5.09 A. That inference had an untested
alternative: ADCP might simply perform worse on MOR.

It does not. On met-enkephalin ADCP reaches **0.93 A in MOR — its best result of the
four**. The engPENK MOR failure is specific to engPENK.

**The control also corrects the first reading.** With a correct pose this protocol reaches
0.93-1.63 A overall and 0.90-1.48 A on the message tetrapeptide. Against that benchmark
engPENK's 3.11 A in DOR is also a failure, and the DOR pose is **not** corroborated either.
The DOR/MOR asymmetry is real and still points at MOR being worse, but the corrected
conclusion is that **both engPENK poses are suspect**.

## Consequence

This is the strongest support so far for the pose hypothesis behind the implausible -8.91.
An independent method reproduces the control peptide's poses to ~1 A in both receptors and
reproduces neither engPENK pose. The co-folded engPENK poses are the leading suspect for
the whole Cycle 8 engPENK result.

**Recommended action:** re-run one engPENK TI leg from an ADCP pose rather than the
co-folded one. The pre-registration named DOR rep1. An earlier draft of this document
argued for switching to MOR; the control shows both legs are equally affected, so the
original choice stands and **that deviation is withdrawn**.

## What this does NOT show

- ADCP predicts geometry, not affinity. Its scores (-16.8 DOR, -11.0 MOR best) are **not**
  free energies and must never be compared with any ddG in this project.
- A pose this method cannot reproduce is not thereby proven wrong. engPENK is a different
  peptide and may genuinely be harder to dock. The defensible claim is that the evidence
  which corroborates the control's poses does not corroborate engPENK's.

## Side result — the extended cassette species

Cassettes 4 and 7 release `YGGFEVVGRGL` and `YGGFEVVGRF` rather than free octapeptide.
Docked into the same receptors and scored on their shared YGGFEVVG core, all four make the
Asp3.32 anchor (2.2-2.6 A) but deviate further from the octapeptide pose than engPENK does
— worst for the 11-mer in DOR at 4.70 A. The C-terminal extension perturbs the binding
mode, which is relevant to interpreting the in vitro digest, where these species are
present.

## Reproducing this

`env.sh`, `run_dock.sh` and `score_gates.py` are in this directory. The install and input
traps are documented in the `adcp-peptide-docking` skill; the two that silently produce
wrong answers rather than errors are:

- A receptor without hydrogens yields a PDBQT with **zero HD atom types**, so every H-bond
  donor is invisible and the Asp3.32 salt bridge is unmodelled. Assert HD count > 50.
- **MOR's Asp3.32 is residue 149 here, not the canonical 147.** Positions were mapped by
  alignment to DOR; the offsets are 21 for five pocket residues and 20 for the sixth, so a
  fixed-offset shortcut would have placed the box on the wrong residue while looking normal.
