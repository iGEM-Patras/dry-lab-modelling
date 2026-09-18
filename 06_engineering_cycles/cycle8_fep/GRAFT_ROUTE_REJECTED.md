# The graft route is not viable — measured, after two invalid attempts

**2026-09-18.** Recorded so nobody repeats it, and so the two ways I got it wrong are on file.

## What was proposed

`YGGFEVVG` and met-enkephalin `YGGFM` share `YGGF`, the message domain that occupies the
orthosteric pocket. Cycle 3b has validated, equilibrated `YGGFM`–receptor systems (5
replicates each, 41 trajectories total). The idea: keep the donor's `YGGF` coordinates,
extend `E-V-V-G` into the address region, and obtain an engPENK system **without a GPU
co-fold** — which matters because `pgpu` has been down for >24 h and is the cluster's only
GPU partition.

It would also have been scientifically preferable: the message-domain pose would be
identical *by construction* to the calibrated control, so any ΔΔG difference would come
from the address region rather than from co-folding noise between two independent
predictions.

## Why it fails

The met-enkephalin C-terminus is **enclosed by receptor**. Rays cast from the peptide's
C-terminal atom in 1000 near-uniform directions, stepping 1.5→14 Å, measured against the
equilibrated `npt.gro` structure with a verified atom selection:

| receptor | 2.5 Å clearance | 3.0 Å | 3.5 Å |
|---|---|---|---|
| OPRD1 (δ) | **0.0 %** | **0.0 %** | **0.0 %** |
| OPRM1 (μ) | 5.7 % | 3.8 % | 1.1 % |

A ΔΔG needs **both** receptors. δ has no exit at all, so the route fails there regardless
of μ's narrow 3.8 %.

This is physically sensible: met-enkephalin is a **5-mer** that terminates in that pocket.
An 8-mer cannot place its `YGGF` where the 5-mer's sits, because the extra three residues
have nowhere to go. The bound pose of `YGGFEVVG` must have `YGGF` shifted or rotated so the
address region exits along a groove — which is exactly what a co-folding model determines
and what cannot be derived from a 5-mer template.

**Caveat, stated rather than hidden:** straight-line rays are a necessary but not
sufficient test — a real chain can curve around an obstacle. 0.0 % at δ even at 2.5 Å
clearance makes a curved path very unlikely, but this is not a proof of impossibility.

## Two invalid attempts first, both mine

**Attempt 1 — raw co-fold pose. Reported 0.0 % open. Invalid.** The donor pose had
pre-existing hard clashes (δ Gly3 **1.28 Å**, δ Met5 **1.65 Å**, μ Tyr1 **1.19 Å**; see
`data/donor_pose_contacts.csv`). Raw co-fold output interpenetrates slightly and
minimisation relieves it. A test demanding 3.0 Å clearance against a 1.2 Å-clashing
structure can only return zero. **It reached the right conclusion for an invalid reason** —
and I was one commit away from publishing it as established.

**Attempt 2 — equilibrated structure, residue heuristic. Reported 23.8 % (δ) and 62.7 %
(μ). Invalid.** `gmx select` found **75** peptide atoms; the last-five-residues heuristic
extracted **45**. Thirty peptide atoms were assigned to the "receptor" set, so the reported
"min distance 1.34 Å" was a **covalent bond** between atoms split across the two groups,
not a contact.

**Attempt 3 — valid.** Peptide selected by GROMACS index file, with
`assert size == 75 and selections disjoint` executed **before** any distance arithmetic, so
a bad selection aborts the job instead of producing a plausible number. Equilibrated
min distance 1.70 Å (δ) / 1.80 Å (μ) — consistent with hydrogen-bond H···acceptor
distances, as expected for a structure containing hydrogens.

Three dihedral-space searches (random sampling, then greedy outward growth) also failed,
but they ran against the clashing raw pose and are **not** valid evidence either way.

## Standing lessons

1. **Verify input identity before computing on it.** Two of three attempts failed on atom
   selection, not geometry, and in both cases the flaw was visible in a number printed
   beside the conclusion (75 vs 45; a 1.34 Å "contact").
2. **Assert the selection, don't inspect it afterwards.** The valid attempt differs from
   the invalid ones only in having `assert` before the arithmetic.
3. **A result that matches expectation gets checked less.** "No exit vector" agreed with my
   story for why the searches failed, so I nearly committed it on invalid evidence.
4. **A raw co-fold pose is not a structure.** It needs minimisation before any geometric
   measurement. Same lesson as reading thermostat groups from `prod.tpr` rather than
   assuming them.

## Correction carried from earlier notes

`YGGFEVVG` has **59** heavy atoms (Y12 G4 G4 F11 E9 V7 V7 G4+OXT), not 57. The post-build
check criterion in `CYCLE8_DESIGN.md` §9 said 57 and is wrong.

## Consequence

The engPENK TI arm **requires a GPU co-fold** and is blocked until `pgpu` returns. The
control arm is unaffected: 216/216 λ-window inputs built and integration-ready.
