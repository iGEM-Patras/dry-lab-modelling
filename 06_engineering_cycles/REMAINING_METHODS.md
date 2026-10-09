# What is left to try, after six routes have failed

**Written 8 Oct 2026, after the Cycle 14 control failed its accuracy and reproducibility
gates.** Every method below was filtered against one number: it must resolve a **ΔΔG of
about 1 kcal/mol**, the size of the published met-enkephalin δ/μ preference.

---

## The two failure modes, which together rule out most of the field

**Mode 1, the published-affinity noise floor.** Four routes (BindPred, GPCRVS, TrGPCR,
our own fingerprint QSAR) calibrate against or interpolate from published affinities. Our
own records disagree by **1.83 kcal/mol** on a single compound measured by two sources.
That is larger than the effect. **Any method anchored to published affinity data is bounded
below by this, regardless of how good the model is.** This is a property of the data, not of
the algorithms, so it rules out the class rather than the instances.

**Mode 2: accumulation in a difference of large absolutes.** Cycle 14 computed the
selectivity as `ΔG(decouple from δ) − ΔG(decouple from μ)` = 2349.5 − 2346.5 kJ/mol: a
3 kJ/mol answer extracted from two ~2350 kJ/mol quantities. Measured per interval, the
per-window biases are small (max 3.5 kJ/mol, none above 5) but **correlated**: 40 of 55 and
40 of 56 intervals share their leg's sign, so they accumulate to ≈30 kJ/mol per leg rather
than cancelling. Roughly **7 kcal/mol of replicate variation in each absolute**, for an
effect of 0.81.

A method escapes only if it avoids **both**.

---

## The one route that escapes both: protein residue-mutation free energy

Instead of decoupling the peptide from each receptor and subtracting, **mutate the receptor**
and compute the free-energy change directly. The large absolute quantity is never formed, so
Mode 2 cannot occur; and nothing is calibrated against published affinities, so Mode 1
cannot either.

This is not speculative. It is the published strategy for exactly this problem:

- **Kinome-wide selectivity by free energy calculation**, Nature Communications 2025,
  doi:10.1038/s41467-025-62722-w: uses *protein residue mutation* free energy calculations
  to reduce off-target liability across a receptor family, the same shape of problem as
  δ versus μ.
- **Protein-mutation FEP benchmark**, J Mol Biol 2024, doi:10.1016/j.jmb.2024.168640:
  establishes reliability of relative binding-energy prediction for single point mutations.

### Is it tractable here? Measured, not assumed.

Aligning OPRD1 (P41143) and OPRM1 (P35372): **61.3% identity overall**, and of 29 orthosteric
pocket positions, **18 are conserved and 11 differ**:

| DOR | MOR | note |
|---|---|---|
| L125 | I146 | conservative |
| Q201 | T222 | polar swap |
| S204 | H225 | introduces imidazole |
| D210 | E231 | conservative |
| **W284** | **K305** | **aromatic → cationic, the largest single change** |
| T285 | A306 | loses hydroxyl |
| D293 | T313 | loses carboxylate |
| P294 | T314 | backbone flexibility |
| V297 | T317 | polar swap |
| A298 | V318 | conservative |
| L300 | W320 | introduces indole |

Eleven handles is a workable number, and they are chemically substantial rather than all
conservative.

### Cost, from this project's own measured throughput (155 ns/day)

| scope | mutations | windows | sampling | wall time |
|---|---|---|---|---|
| single-residue pilot (W284K) | 1 | 96 | 288 ns | **~1.9 days** |
| four most distinct residues | 4 | 384 | 1152 ns | ~7.4 days |
| all eleven | 11 | 1056 | 3168 ns | ~20 days |

### What it would and would not tell you

**Would:** which pocket differences actually drive δ/μ discrimination, as free energies with
replicate error bars, and whether the engineered `EVVG` address exploits any of them.

**Would not:** give a ΔΔG for `YGGFEVVG` itself. The quantity changes. This answers *why*
selectivity arises, not *how much* this peptide has.

**Caveat that must be stated first:** 18 of 29 pocket residues are conserved, so selectivity
may be substantially conformational rather than contact-chemical. Residue-mutation FEP would
miss that entirely, and a null result would not distinguish "no contact-chemical driver" from
"the method cannot see the driver".

---

## Also identified, lower priority

**Funnel-metadynamics on the opioid family**: J Chem Inf Model 2026,
doi:10.1021/acs.jcim.5c02403, "Identification of Subtype-Selective Binding Sites in the
Opioid Receptor Family", combines MD and funnel-metadynamics on μ, δ and κ specifically. It
computes absolute binding free energies with a funnel restraint, so it does not escape Mode 2,
but its error profile differs and the paper is directly on our receptors. Worth reading before
committing to anything.

---

## Recommendation

**Do not start any of this before the cAMP assay.** The wet-lab assay measures functional
potency at both receptors directly, is subject to neither failure mode, and answers the
question the project actually needs answered. Every computational route assessed has cost
days to weeks and returned either a failed gate or an uninterpretable number.

If a computational route is wanted *alongside* the assay, for mechanism rather than for the
answer, the **single-residue W284K pilot at ~1.9 days** is the right size: it tests whether
residue-mutation FEP reproduces a known selectivity determinant before anything larger is
committed, and it fails cheaply.
