# Cycle 14 · Gate G4 — replicate independence

**Status: PASSED.** Scored 2026-10-03, before any production window ran.

| receptor | solute RMSD (r2 vs r1) | Protein atoms | residues |
|---|---|---|---|
| DOR | **0.319 nm** | 5,830 | 377 |
| MOR | **0.331 nm** | 6,384 | 405 |

Both fall in the 0.1–0.3 nm band stated in advance as the expected range for independent
equilibrations begun from a shared minimised structure. The replicates are genuinely
independent: fresh velocity generation **and** independent NVT and NPT, rather than Cycle
8's pair which shared one equilibrated structure and differed only by thermostat seed.

**Peptide identity verified, not assumed.** The last five residues of the Protein group
render as `YGGFM` in both receptors — met-enkephalin, numbering restarting at 1 — so the
RMSD selection is the intended solute.

---

## A gate-design flaw, found while scoring it

The first evaluation applied the pre-registered 0.05 nm threshold to **all atoms** and
returned:

```
DOR  mean atom displacement 5.6503 nm   (median 5.84, max 18.05)
MOR  mean atom displacement 5.4724 nm   (median 5.48, max 16.55)
VERDICT: both pairs diverged -- proceed to stage 2
```

**That verdict was discarded.** The solute is 4% of the system: 5,830 protein atoms against
45,426 membrane and 84,575 solvent. Bulk water diffuses several nm per nanosecond and
periodic wrapping scatters it, so the metric measured solvent diffusion, not structural
divergence. The giveaway is a maximum displacement of 18 nm in a box roughly 15 nm across,
between two runs started from the *same* minimised structure.

Against solvent, 0.05 nm is unreachable in the failing direction — **any** two independent
runs clear it by two orders of magnitude. The same structures measured both ways:

| metric | value |
|---|---|
| all 135,831 atoms | 5.65 nm |
| solute only, 5,830 atoms | **0.319 nm** |
| ratio | **17.7×** |

**The defect is in the pre-registration, not the execution.** G4 named a threshold without
naming an atom selection, and an unspecified selection means everything — which for a
membrane system is overwhelmingly solvent. A gate that cannot fail is not evidence, and
this one would have gone into the record as passed.

This is the failure mode Cycle 14 exists to correct, one level up. Cycle 8's replicate
spread of 8.53 kcal/mol looked like uncertainty while measuring thermal noise inside a
single basin; a vacuous G4 would have looked like validation while being incapable of
returning a negative.

**Rule for future gates in this project: a threshold must name the quantity *and* the
selection it applies to.**

---

## Measured GPU equilibration throughput

Equilibration was moved from `pibu_el8` to `pgpu` partway through. Unlike the production
windows — where GROMACS keeps PME and the perturbed nonbonded terms on CPU under
free-energy perturbation — equilibration is plain MD, so both offload to GPU.

| stage | system | ns/day |
|---|---|---|
| NVT | MOR, 101k atoms | 156.4 |
| NPT | MOR, 101k atoms | 173.7 |
| NVT | DOR, 136k atoms | 117.7 |
| NPT | DOR, 136k atoms | 124.1 |
| NPT | DOR, resume | 121.6 |

Against ~46 ns/day on 16–24 CPU cores that is about **3×**, and about 4.5× the 31.2 ns/day
measured for FEP windows on the same card. **Future equilibrations in this project belong
on `pgpu`; production stays on CPU** where the comparator legs ran.

## What this licenses

Stage 2 — the 57-window re-spaced ladder — may run, and its replicate spread will measure
structural plus thermal variation rather than thermostat seed alone.

## What it does not

Nothing about whether the method can resolve the effect. The pre-registered overlap, sign
and accuracy gates against the published **+0.81 kcal/mol** are still ahead. G4 is a
precondition, not a result.
