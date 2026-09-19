# Building and declashing Martini coarse-grained lipoplex systems

**Why this document exists.** A Cycle 10 build stalled for ten iterations at energy
minimisation with `Fmax = 5.4 × 10⁷` and 1,498 LINCS warnings. It was diagnosed as a packing
problem and was not one. The real cause is documented in the primary literature and the
remedy was already present in this project's own working configuration. This guide records
both so the next person does not repeat it.

---

## 1. The cholesterol constraint problem

**Symptom:** `Too many LINCS warnings`, a system that will not minimise, or — worse, because
it is silent — artificial temperature gradients in a run that otherwise looks fine.

**Cause.** LINCS enforces bond-length constraints by a truncated series expansion whose
`lincs_order` is the number of retained terms. Convergence depends on the largest eigenvalue
of the constraint-coupling matrix. Fábián, Thallmair & Hummer (2023) state it directly: slow
convergence *"is expected for any system with strongly coupled constraints. In Martini 2, this
includes sterols such as cholesterol."* In coupled triangles the third constraint away from a
given constraint is the constraint itself, so the expansion converges slowly or not at all.

**The number that matters:** the `lincs_order` required to properly constrain Martini 2
cholesterol **is 72**. The GROMACS default is **4**. The authors describe 72 as infeasible in
practice, which is why their paper introduces a virtual-site cholesterol whose requirement
drops from 72 to 16.

Martini 2 cholesterol in this project (`ff/martini_v2.0_CHOL_bonded.itp`) carries **11
constraints** in a coupled arrangement. Every other lipid here carries zero:

| molecule | constraints | bonds |
|---|---|---|
| **CHOL** | **11** | 17 |
| MC3T / MC3N | 0 | 10 |
| DOPE, DOPC, POPC, … | 0 | 9–13 |

So cholesterol is the *only* constraint source among the lipids. DNA carries constraints too
(210 in the 30-bp duplex).

## 2. How this project already solves it — use this, not a paper

The topology is written with a compile-time switch:

```
#ifdef FLEXIBLE
[ bonds ]            ; 11 stiff bonds, k = 20000 kJ/mol/nm²
#else
[ constraints ]      ; the same 11 distances, as hard constraints
#endif
```

**`define = -DFLEXIBLE` replaces all 11 cholesterol constraints with stiff bonds, so LINCS
never sees them and the order-72 requirement disappears.**

Every working mdp in `lipoplex/` uses it — not only during minimisation but **in production**:

| stage | file | `dt` | `define` |
|---|---|---|---|
| EM, initial | `asm/em0.mdp` | — | `-DFLEXIBLE`, `constraints = none` |
| EM, restrained | `asm/em1_rebuild.mdp` | — | `-DFLEXIBLE -DPOSRES` |
| EM, tight | `asm/em0_tight.mdp` | — | `-DFLEXIBLE -DPOSRES`, `emstep = 0.0001` |
| NVT warm-up | `asm/nvt_warm.mdp` | **0.001** | `-DFLEXIBLE` |
| NVT | `asm/nvt_prod.mdp` | 0.002 | `-DFLEXIBLE` |
| NPT | `asm/npt_prod.mdp` | 0.002 | `-DFLEXIBLE`, Berendsen |
| NPT rescue | `asm/npt_rescue.mdp` | 0.001 | `-DFLEXIBLE`, c-rescale, `tau-p = 20` |
| **production** | `replicates/*/prod.mdp` | **0.001** | **`-DFLEXIBLE`**, c-rescale |

Two consequences worth stating plainly:

1. **`-DFLEXIBLE` is never dropped.** Not for equilibration, not for production. Dropping it
   at any stage reinstates the 11 coupled constraints and LINCS fails at `lincs_order = 4`,
   which is what every mdp here uses.
2. **The timestep is 1–2 fs, not the 20 fs typical of Martini.** Stiff bonds at
   20000 kJ/mol/nm² have a vibrational period that a 20 fs step cannot resolve. This is the
   price of the `-DFLEXIBLE` route and it is why these runs are slow. It is a deliberate
   trade, not an oversight.

## 3. The declash ladder

`Fmax` that does not decrease at all over 100,000 steepest-descent steps means the structure
is pathological, not merely tight — usually beads at near-identical positions. More steps will
not help. The documented sequence (`asm/rescue_DOTAP.sh`, `em0 → em1_rebuild → em0_tight`):

1. **EM with `-DFLEXIBLE` and `constraints = none`**, `emstep = 0.001`, `emtol = 1000`
2. ~~**EM with `-DFLEXIBLE -DPOSRES`** — restrain the solutes~~ **Tested and it makes things
   worse.** See §3a. Skip straight to step 3.
3. **EM tight**, `emstep = 0.0001`, `emtol = 5000` — smaller steps, looser target
4. **NVT at `dt = 0.001`** with `-DFLEXIBLE`, a hard thermostat (`tau-t = 0.1`)
5. **NVT at `dt = 0.002`**
6. **NPT, Berendsen** — a weak-coupling barostat tolerates a box that is still adjusting
7. **NPT, c-rescale, `tau-p = 20`** — slow pressure coupling before production
8. **Production**, c-rescale

Wrap `mdrun` in a restart loop (`rescue_DOTAP.sh` retries up to 200 times with `-cpi`); on this
cluster a run can die from filesystem stalls rather than physics.

### 3a. Do not position-restrain the solutes in a randomly packed system

This guide originally recommended restraining the cargoes during early minimisation, by
analogy with `asm/em1_rebuild.mdp`. **That was tested on the Cycle 10 condition-B system and
it is wrong for this situation.** Measured `Fmax`:

| stage | restraints | `Fmax` |
|---|---|---|
| EM, `emstep = 0.0001` | cargoes at 1000 kJ/mol/nm² | 5.37 × 10⁷ |
| EM, `emstep = 0.001` | cargoes at 1000 kJ/mol/nm² | **2.63 × 10¹⁰** |
| EM, `emstep = 0.001` | **released** | **2.00 × 10²** (converged at `emtol = 200`) |

Restraining a solute that lipids have been packed *on top of* pins the overlap in place: the
restraint force opposes the very displacement that would relieve the clash, and the two fight
each other into a worse configuration. Restraints are useful when the solute's *pose* must be
preserved while a pre-formed environment settles around it — which is what `em1_rebuild.mdp`
was doing. They are harmful when the environment was generated by random insertion.

**Rule:** with randomly packed lipids, minimise everything free. If a pose must be protected,
restrain the *lipids* instead, or equilibrate the lipid phase before the solute is placed.

Note also that only one of the three defences applied here mattered. `-DFLEXIBLE` did the
work; `lincs-order = 12` was belt-and-braces; the restraints were actively harmful. Running
all three at once nearly hid that — had the ladder stopped after the restrained stages, the
conclusion would have been "the fix failed."

## 4. Assembly order

Do not insert a large solute into an already-equilibrated box. Measured on the reference
system: the lipid aggregate spans z 0.81–9.68 nm of a 14.82 nm box, the construct spans
5.78–16.91 nm wrapping the boundary, and **the largest void anywhere offers 0.31 nm of
clearance** — against the ~7 nm a 21-bp duplex needs. `gmx insert-molecules` then reports
`Added 0 molecules` while `Replaced 398 residues`: a destructive no-op that deletes solvent,
inserts nothing, and exits 0.

Place all solutes into an **empty** box first, then lipids, then solvate. Both cargoes place
first-try that way.

## 5. Checks that cannot pass for the wrong reason

- **Never accept a bead count as evidence of structure.** `polyply gen_coords` returned the
  correct 271 beads for a 21-bp duplex whose base-pair bonds spanned a **median 7.16 nm**
  against a 0.445 nm target — two unpaired strands. The count assertion passed and the broken
  structure propagated through four further steps.
- **Check bond lengths, per molecule, against that molecule's own distribution.** A 1.2 nm
  threshold calibrated on the surrogate produced a false positive on the construct, whose
  longest legitimate bond is 1.37 nm.
- **Verify insertion by counting the inserted species**, not by grepping the log.
- **A new duplex needs minimisation *and* short MD to pair.** Minimisation alone left base
  pairs at 0.58 nm; 1 ns of vacuum MD brought them to 0.50 nm (restraint 0.445).
- **`Fmax` converging *at* `emtol` is success; `Fmax` unchanged between runs is not.** The
  failed runs reported an identical 5.37 × 10⁷ twice, which reads as "stalled at step 0", not
  "minimised as far as possible".
- **Calibrate bond-length thresholds against the same molecule in a working system, and
  remember `-DFLEXIBLE` makes former constraints stretchy.** A distance that is fixed under
  `[constraints]` fluctuates thermally once it is a 20000 kJ/mol/nm² bond, so the reference's
  own equilibrated maximum — not the constrained value — is the right comparator.

## 6. Diagnostic order for "it will not minimise"

1. Is `-DFLEXIBLE` set in **every** stage? → if it is dropped anywhere, that is almost
   certainly the whole problem
2. Does any molecule carry `[ constraints ]`? → `awk` the topologies; cholesterol and DNA do
3. Is `Fmax` *unchanged* between runs? → pathological overlap. Do **not** reach for position
   restraints (§3a); check for duplicate coordinates and try releasing any restraints present
4. Is the longest bond in any molecule greater than half the box? → wrapped coordinates or a
   molecule that was never folded; check the standalone structure before blaming assembly
5. Only then consider raising `lincs_order`

## References

- Fábián B, Thallmair S, Hummer G. *Optimal Bond Constraint Topology for Molecular Dynamics
  Simulations of Cholesterol.* J Chem Theory Comput 2023;19(5):1592–1601.
  doi:10.1021/acs.jctc.2c01032 — mechanism, the order-72 result, virtual-site remedy
- Fábián B, Thallmair S, Hummer G. *Nonconverged Constraints Cause Artificial Temperature
  Gradients in Lipid Bilayer Simulations.* J Phys Chem B 2021;125(33):9537 — the silent
  failure mode
- Melo MN, Ingólfsson HI, Marrink SJ. *Parameters for Martini sterols and hopanoids based on a
  virtual-site description.* J Chem Phys 2015;143:243152 — virtual-site sterols
- Qi Y, Ingólfsson HI, Cheng X, Lee J, Marrink SJ, Im W. *CHARMM-GUI Martini Maker for
  Coarse-Grained Simulations with the Martini Force Field.* J Chem Theory Comput
  2015;11:4486 — standard staged equilibration
- Uusitalo JJ, Ingólfsson HI, Akhshi P, Tieleman DP, Marrink SJ. *Martini Coarse-Grained Force
  Field: Extension to DNA.* J Chem Theory Comput 2015;11:3932 — the DNA model used here

**Project sources, which override the papers where they differ:**
`lipoplex/asm/rescue_DOTAP.sh`, `lipoplex/asm/em0.mdp`, `em1_rebuild.mdp`, `em0_tight.mdp`,
`nvt_warm.mdp`, `npt_rescue.mdp`, `lipoplex/replicates/*/prod.mdp`,
`lipoplex/ff/martini_v2.0_CHOL_bonded.itp`
