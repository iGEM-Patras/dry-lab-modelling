# GNN, PINN and energy models: what the literature supports, and one real reframe

**Searched 12 Oct 2026, Europe PMC, five query families. The honest summary is that the
energy route is still closed, but the search surfaced a different kind of method that
sidesteps the wall entirely.**

---

## 1. The filter, applied again

Every method in this project is tested the same way: **is the reported error smaller than
the effect we must resolve?** The effect is the published delta/mu selectivity of
met-enkephalin, **0.81 kcal/mol**. Our own 13-compound panel spans at most ~2.13 kcal/mol.

| method | reported error | vs the effect |
|---|---|---|
| **GULP**, GNN on interface graphs, doi:10.1021/acsphyschemau.6c00060 | **MAE 2.31 kcal/mol** (Pearson r 0.54) | **2.9x too large** |
| Perses protein-mutation FEP (assessed 9 Oct) | RMSE 1.61 kcal/mol | 2.0x too large |

**GULP fails, and it fails worse than anything assessed so far.** An MAE of 2.31 kcal/mol
corresponds to a 49-fold selectivity error; the most delta-selective compound in our entire
panel is ~31-fold. It is also protein-**protein** dG, not peptide-GPCR.

**That is the eighth energy-predicting route ruled out on the same criterion.**

---

## 2. PINNs: the search result IS the finding

Querying physics-informed neural networks against molecular/free-energy/thermodynamic terms
returned, almost entirely, **continuum and PDE problems**:

- soil temperature forecasting
- supersonic turbine stator blades
- water distribution systems
- wellbore trajectory deviation
- thermo-responsive hydrogel swelling
- phenolic resin ablation

**Exactly one molecular hit:** doi:10.1038/s41598-026-49635-4, solubility prediction with
thermodynamic constraints in the loss (RMSE 0.36 log units; 96.3% of predictions satisfy
energy conservation under 2 kJ/mol, against 67.4% for an unconstrained network).

That architecture is genuinely interesting: decompose solvation free energy into cavity,
electrostatic, van der Waals and hydrogen-bonding terms, then enforce their thermodynamic
relationships through custom loss functions. But it is **solubility, not binding
selectivity**, and no binding-selectivity implementation exists.

**PINNs earn their keep where a governing PDE constrains the solution.** Binding selectivity
is not that kind of problem: it is a difference of two ensemble averages, which is why our
Cycle 14 failure was statistical (correlated per-window bias) rather than a missing physical
constraint. A PINN does not address correlated sampling bias.

**So "GNN + PINN for binding free energy" is not an established area.** That is a real
finding from the search, not a gap in it.

---

## 3. The reframe that actually survives: stop predicting energy

Two methods in the search do not predict a free energy at all. They **classify**. Their
error metrics are AUCs, not kcal/mol, so the filter that killed the other eight does not
apply to them in the same form.

### DeorphaNN, Molecular Cell 2026, doi:10.1016/j.molcel.2026.07.006

A **graph neural network for peptide-GPCR agonist prioritisation**, built on AlphaFold
active-state complexes plus interatomic interactions and language-model embeddings.
Experimentally validated: it predicted agonists for two orphan GPCRs that were then
confirmed at the bench, and it generalised to annelid and human retrospective benchmarks.

**This is our exact molecule class and our exact receptor class.** Peptide agonists of a
class A GPCR. Nothing else assessed in this project has matched the problem that closely.

### Dynamic-GLEP, Brief Bioinform 2026, doi:10.1093/bib/bbag049

Dynamics-informed deep learning for **ligand efficacy** in class A GPCRs, explicitly built
because "most computational approaches still emphasize affinity prediction, with limited
capacity to capture the conformational dynamics driving efficacy". Uses multi-conformation
receptor-ligand complexes. AUC 0.74 on 5-HT1A cross-validation, 0.71 external, >0.85 on
adenosine A2A.

---

## 4. What this could and could not tell us

**Could:** whether `YGGFEVVG` is predicted to be an agonist of DOR, and whether that
prediction is stronger at DOR than at MOR. A *relative ranking* across the two receptors is
not a ddG, but it is an answerable question with a published, experimentally validated
method at the right molecule class.

**Could not:** give a selectivity value in kcal/mol. It never forms an energy.

**Three honest limits before anyone runs it:**

1. **Scope.** DeorphaNN was trained on C. elegans peptide-GPCR pairs with human retrospective
   validation. Discriminating between two human receptors that share 18 of 29 orthosteric
   pocket residues is beyond its demonstrated scope. A null result would not distinguish
   "no preference" from "beyond the method's resolution", which is the same ambiguity that
   limited Cycle 15.
2. **It needs a control, as everything here does.** Run it on the 13-compound calibration
   panel first. If it cannot rank compounds of known delta/mu preference, it cannot rank ours.
3. **Classification is weaker evidence than a number**, and the poster should say so. It
   would support "predicted agonist at DOR", not "delta-preferring by X-fold".

---

## 5. Recommendation for the ten days before freeze

**Do not start a GNN or PINN energy model.** Eight energy routes have now failed the same
filter, and the two new ones fail it by more than the methods already abandoned.

**If anything is run, run DeorphaNN against the calibration panel first**, as a control,
exactly as Cycle 16's design required. That is a cheap, bounded test of whether the method
can see delta/mu discrimination at all on compounds where the answer is known. If it
cannot, that is a one-day answer and the question is closed properly rather than left open.

**And the standing conclusion does not change:** the cAMP assay measures functional potency
at both receptors directly, in a day of bench time, subject to none of these constraints.
The poster wording `design goal, not demonstrated result` remains what the evidence supports.
