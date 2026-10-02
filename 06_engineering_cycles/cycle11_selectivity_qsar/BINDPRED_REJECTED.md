# BindPred evaluated and rejected on feasibility, before generating any prediction

BindPred (Bioinformatics 2026, doi:10.1093/bioinformatics/btag309) predicts binding affinity
from sequence alone using ESM2 embeddings plus gradient boosting, r = 0.86 on an 11,919-complex
benchmark. Structure-agnostic, so no pose dependence — genuinely attractive.

**Rejected, and the reason is structural rather than a failed fit.**

ESM2's alphabet is 20 L-amino acids. It has no token for a D-residue, an N-methylated backbone,
or a C-terminal amide. Opioid peptide delta-selectivity is largely *achieved* through exactly
those modifications.

Of 3,584 ChEMBL compounds with Ki at both OPRD1 and OPRM1, only **5** can be faithfully encoded
as standard L-peptide sequences (confirmed by exact canonical-SMILES match, not by name):

| peptide | ddG (kcal/mol) |
|---|---|
| alpha-neoendorphin | +0.86 |
| Leu-enkephalin | +0.78 |
| dynorphin A (1-17) | +0.28 |
| Met-enkephalin | +0.15 |
| dynorphin A (1-13) | -0.25 |

Span **1.11 kcal/mol**. The known between-source disagreement on a single compound in our own
records (endomorphin-1, -2.99 vs -4.82) is **1.83**. The panel's entire dynamic range sits below
the noise in its own reference axis. Critical |r| at n=5 is 0.878, against 0.553 at the n=13 we
achieved in Cycle 7. Four of the five share the YGGFL prefix.

The compounds that would supply dynamic range are excluded for the same structural reason:

| | ddG | why unencodable |
|---|---|---|
| DAMGO | -3.89 | R-configured alpha-carbon (D-Ala) + N-methylation |
| dermorphin | -3.78 | R-configured alpha-carbon (D-Ala) + N-methyl + C-terminal amide |

**Method note.** A first encodability test used RDKit `MolToSequence` on the ChEMBL SMILES and
returned zero sequences for all 128 peptides. Validating that function against a molecule built
from a known sequence showed it only works on molecules carrying residue metadata, which a bare
SMILES does not. The empty result said nothing about the molecules. The valid test is forward
matching: generate candidate sequences from the precursors, build them, compare canonical SMILES.

Also corrected in the same analysis: our sign convention had been inverted, making DAMGO appear
delta-preferring. Fixing it dissolved an apparent disagreement between the ChEMBL value for
Met-enkephalin (+0.15) and our stored +0.81 — same direction, magnitude differing by ordinary
between-source scatter.

## GPCRVS also checked, also not applicable

GPCRVS (IJMS 2025, doi:10.3390/ijms26052160) is GPCR-specific and takes SMILES, so it does not
have BindPred's encoding limitation. But "opioid" appears **once** in the paper, as a passing
mechanistic remark; OPRD/OPRM/OPRK appear **zero** times. Validation was on class B GPCRs and
chemokine CC/CXC receptors. Opioid receptors are class A. Not usable off the shelf.

Its SMILES-input design is what prompted Cycle 11.

---

# TrGPCR also checked, and rejected on its own reported error

TrGPCR (IEEE JBHI 2023, doi:10.1109/JBHI.2023.3307928) is dynamic deep transfer learning for
GPCR-ligand affinity: BindingDB as source domain, GLASS as target domain, with binding-pocket
secondary structure as an additional feature. No 3D structure required. It beats DeepDTA by
5.2% on RMSE.

It was the **best domain match of the four methods assessed**, and it is not excluded by the
Cycle 11 fingerprint finding, because it uses a learned representation rather than a fixed
fingerprint. GLASS also contains opioid receptors, unlike GPCRVS.

## It fails on resolution, by its own numbers

TrGPCR predicts **affinity**, not selectivity. A ddG is therefore a difference of two
predictions and inherits sqrt(2) x the per-prediction error.

Reported: *"RMSE and MAE values of 1.804 and 1.478 on Core 2016"* — their best figure. Units
are explicit in the paper: affinities are pKd, defined there as `pKd = -log10(Kd/1e9)`, so
RMSE is in **log10 units**.

| | |
|---|---|
| per-prediction error | 1.804 x 1.364 = **2.46 kcal/mol** |
| propagated to a ddG | **3.48 kcal/mol** |
| required to resolve 1.0 kcal/mol | <= 0.52 log10 units |
| margin | **fails by 3.5x** |

3.48 kcal/mol is **4.3x** the published met-enkephalin ddG (+0.81) and ~2.8x our own calibrated
engPENK estimate (+1.23). Their alternative reported setting (RMSE 1.994) is worse. Their
CNN-only ablation (2.787 -> 1.804) shows the architecture genuinely helps; the floor it reaches
is still far above what this question needs.

**Prediction error on our side, recorded.** Before reading the paper we estimated the plausible
RMSE range as 0.5-0.9 log units, extrapolating from DeepDTA's published performance on Davis
and KIBA. The actual figure is 1.804 — more than double the top of that range. Those benchmarks
are kinase sets with far denser data; GPCRs are the hard case, which is this paper's own stated
motivation. The lesson is not to extrapolate a benchmark figure across target families.

## Second, independent failure: the receptors are not there

`opioid`, `OPRD`, `OPRM` appear **zero** times in the paper. Their GPCR dataset is 356 proteins,
5,359 ligands and 15,343 interactions, and opioid receptors are never named. GLASS contains
them, but there is no evidence they are in the evaluated split — so using it here would mean
extrapolating on top of an error bar already 4x too large.

---

# Summary: four published methods, four distinct failure modes

| method | failure mode |
|---|---|
| BindPred (sequence + ESM2) | cannot **represent** D-residues or N-methylation; 5 encodable references spanning 1.11 kcal/mol against 1.83 of reference noise |
| GPCRVS (GPCR ML, SMILES) | opioid receptors absent; validated on class B and chemokine CC/CXC |
| TrGPCR (transfer learning + pockets) | ddG error 3.48 kcal/mol, 4.3x the effect; opioid receptors never named |
| Cycle 11 QSAR (ours, direct ddG) | r = 0.77 in aggregate but the payload prediction is a nearest-neighbour lookup; sign flips when the 36 neighbours are removed |

The common cause is not four unlucky methods. **The published affinity data cannot resolve a
~1 kcal/mol selectivity difference for a peptide in this region of chemical space.** Our own
records disagree by 1.83 kcal/mol on one compound measured by two sources — larger than the
effect itself.

**Consequence.** Alchemical free energy is the only method available that does not interpolate
from published values, and on 2026-10-01 its met-enkephalin control reproduced the published
value at +0.97 +/- 1.00 against +0.81 (replicate 1 of 2). It is the method that will settle
this, and the wet-lab cAMP assay is the arbiter.

> **CORRECTION, 2026-10-02.** The control value above is withdrawn -- it was computed on an
> incomplete leg (two windows ~1 ns short, on a status report that said the leg was complete).
> Verified-complete sampling gives **-3.12 +/- 2.29 kcal/mol, the wrong sign** against +0.81.
>
> The first clause stands: alchemical free energy is still the only route here that does not
> interpolate from published values, which is why the reference-data noise floor documented
> above does not bound it. The second clause does not: it is **not** the method that will
> settle this, because it currently gets the sign wrong on a known peptide. So the correct
> reading of this document is stronger than when it was written -- **five** methods have now
> failed to establish the direction of delta/mu preference for YGGFEVVG, four of them bounded
> by published-data resolution and the fifth by its own sign gate. The wet-lab cAMP assay is
> not the arbiter between computational predictions; it is the only measurement available.


---

# Fifth assessment: the npj Drug Discovery perspective (no new computational route)

Su, Liggett, Kim, Kim & Goddard, *npj Drug Discovery* 2026;3:13, doi:10.1038/s44386-026-00046-5.
An integrated GPCR discovery workflow: computational modelling, functional cell assays, and
**FLOWER** (Frequency Locked Optical Whispering Evanescent Resonator) for label-free direct
binding measurement. Case studies are bitter (TAS2R) and sweet (T1R2/T1R3) taste receptors —
not opioid receptors, though the authors state the approach is generalizable.

## It contains no computational method that passes our resolution filter

Named: GEnSeMBLE, DarwinDock, NAMD/CHARMM36m, and Allosite / PASSer for allosteric pockets.
These are structure-generation, docking and MD tools. The paper reports **no selectivity
benchmark for any of them** — no RMSE, no correlation against measured ddG. They do not fail
our 0.52 log-unit requirement so much as never state a number against which it could be
applied. Allosite and PASSer target hidden allosteric pockets, which does not apply to an
orthosteric peptide. NAMD/CHARMM36m is MD, which this project already runs.

## Its actual thesis agrees with our conclusion, reached independently

*"FLOWER provides direct, label-free quantification of receptor-ligand binding affinity under
near-physiological conditions, enabling computational predictions of binding strength and
selectivity to be tested against experimentally determined equilibrium constants (Kd) without
the use of tags."*

The paper's answer to computational ambiguity is not a better model — it is direct experimental
binding measurement. That is the same place the four assessments above arrived from the
opposite direction.

## WET-LAB PLANNING NOTE: potency is not affinity

This is the transferable point, and it is a note for planning rather than a recommendation.
The decision is the wet lab's.

The paper's Fig. 1 workflow turns on *"when rank order of potencies and affinities agree"*, and
flags that *"atypical FLOWER- or cell-based data require investigation with advanced molecular
dynamics or other approaches"*. It treats functional potency (cell-based) and binding affinity
(Kd) as **two different measurements** whose agreement is a checkpoint.

**Every dry-lab selectivity number in this project is a ddG of BINDING:** Cycle 7's +1.23 +/-
1.76, Cycle 8's -8.75 +/- 3.19, the met-enkephalin control (-3.12 and +5.41 across its two
replicates -- see the correction above; this paragraph originally cited the withdrawn
+0.97 +/- 1.00), the MM-GBSA directions, and all five published methods assessed.

**The planned arbiter, cAMP, measures functional POTENCY.**

Consequence: if the cAMP delta/mu ratio disagrees with the predicted binding ddG, that may be
**ligand bias** rather than a wrong prediction — and without a binding measurement there is no
way to tell which. cAMP is the right assay for "does it work" and for the therapeutic claim,
but it cannot strictly validate or refute the dry-lab selectivity predictions; it answers an
adjacent question. Worth knowing before a judge asks.

## Access

FLOWER is the Su lab's instrument (Wyant College of Optical Sciences, Arizona) and is not
accessible to this project. The generic requirement is any direct binding measurement:

- **Radioligand displacement** — previously considered and set aside in favour of cAMP. Yields
  Ki at each receptor, hence an experimental ddG directly comparable to every dry-lab number.
  This paper is an argument for revisiting it IF the delta/mu question specifically matters.
- **SPR / BLI** at a core facility — label-free Kd on standard instruments, but GPCRs are
  membrane proteins requiring nanodiscs or virus-like particles to immobilise, which is
  precisely why FLOWER is notable. Likely out of scope for this timeline.

## Running total: five published approaches, none able to resolve the effect

Three fail for lack of the right data or receptors (BindPred, GPCRVS, this perspective), one
on its own reported error (TrGPCR, 3.48 kcal/mol on a ddG against a ~1 kcal/mol effect), and
one of ours reduces to a nearest-neighbour lookup (Cycle 11). The fifth paper's own
recommendation is to stop computing it and measure binding directly.

This is a documented position, not a run of failures: we do not claim delta-selectivity, we
have recorded why five computational routes cannot settle it, and we have named the
measurement that can.
