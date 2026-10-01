# Cycle 11 — Can a selectivity QSAR trained directly on ddG answer the engPENK question?

**Status: CLOSED. No ddG reported for YGGFEVVG.**

## Honest note on the pre-registration timestamp

`data/cycle11_prereg.json` was written and saved as a platform artifact **before** any SMILES
were fetched or any model fitted. It was **not** pushed to git before the fit, which is the
project convention and the thing that makes a pre-registration auditable. So this cycle's
timestamp evidence is weaker than cycles 4, 5, 7 and 8. Stated rather than glossed. The
file does contain a prior I got **wrong** (I predicted G3 would fail), which is at least
evidence it was not written after the fact.

## Why this was worth trying

Every selectivity method used in this project — ipTM, MM-GBSA, the affinity head,
alchemical free energy, BindPred — computes selectivity as the **difference of two separately
predicted affinities**, which inflates the error by sqrt(2). This cycle regressed on ddG
**directly**, which does not pay that penalty.

It became possible because SMILES input admits the D-amino-acid and N-methylated ligands that
span the selectivity axis. The sequence-based route (BindPred, evaluated the same day) could
encode only 5 compounds spanning 1.11 kcal/mol; SMILES admits 3,579 spanning 13.5.

## Gates, judged on a Bemis-Murcko scaffold-grouped 5-fold CV

| gate | threshold | all, n=3,579 | >=2 meas, n=227 |
|---|---|---|---|
| G1 correlation | r >= 0.50 | 0.769 PASS | **0.318 FAIL** |
| G1b resolution | RMSE <= 1.0 kcal/mol | **1.06 FAIL** | **1.67 FAIL** |
| G2 sign | > 50%, binomial p<0.05 | 82.1% PASS | 81.9% PASS |
| G3 applicability | Tanimoto >= 0.30 | 0.662 PASS | PASS |

The `>=2 measurements` tier was pre-registered as **primary**. It fails G1.

G1 was amended at pre-registration time: the p=0.05 critical r is 0.13 at n=227 and 0.033 at
n=3,584, so a significance-based gate passes automatically and tests nothing. Replaced with a
usefulness threshold of 0.50 and a separate resolution gate.

## The robustness test that settles it (not pre-registered)

Refitting with the 36 compounds at Tanimoto >= 0.50 plus the enkephalin scaffold family removed:

```
prediction WITH nearest neighbours  : +0.82 kcal/mol
prediction WITHOUT them             : -0.24 kcal/mol   <- SIGN FLIPS
```

The +0.82 is not a prediction about YGGFEVVG. It is a lookup of "the nearest database entry is
an enkephalin at +0.78". Run because the nearest-neighbour similarity looked suspiciously high.

## A drafting gap in our own decision rule, disclosed

The pre-registered decision rule named G1 and G2 but **not** G1b, which was added during
pre-registration. The all-compound tier passes G1 and G2, so a literal reading permits
reporting a number. We do not, because G1b's stated rationale was precisely that RMSE above
1.0 cannot resolve a ~1 kcal/mol effect. Exploiting a drafting omission is the opposite of
what a pre-registration is for.

## The diagnostic finding — this generalises beyond this cycle

Compounds at Tanimoto >= 0.30 to the payload (n=200) span **-7.01 to +5.17 kcal/mol**, with
sd **2.44** — *higher* than the full set's 1.66. Chemical similarity at Morgan r=2 resolution
carries **no** selectivity signal in this region of chemical space.

An earlier reading of this, based on the six nearest compounds only, said the neighbourhood was
"enkephalins, all mildly delta-preferring". That was wrong and is corrected here.

**Consequence:** any method that interpolates from chemically similar compounds will fail here
for the same reason — the local published data spans the entire selectivity range. That covers
fingerprint QSAR, language-model embeddings, and similarity-based screening generally. It is
consistent with the published fact that opioid peptide selectivity turns on single residues and
stereochemistry.

**This makes the physics route more load-bearing, not less.** Alchemical free energy is the only
method in the project that does not interpolate from neighbours, and on 2026-10-01 its
met-enkephalin control reproduced the published value (+0.97 +/- 1.00 vs +0.81, replicate 1).

## What the model IS good for

r = 0.769, 82% sign accuracy, RMSE 1.06 kcal/mol on a scaffold split across 3,579 compounds is
the best aggregate performance of any selectivity method in this project. It is usable for
**ranking structurally diverse small molecules**. It is not usable for this peptide.

`data/cycle11_dataset.csv` — 3,579 compounds with ddG, SMILES, Murcko scaffold and Tanimoto to
the payload — is reusable for any future selectivity work.
