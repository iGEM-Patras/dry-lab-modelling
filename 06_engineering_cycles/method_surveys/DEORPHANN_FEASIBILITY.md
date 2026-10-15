# DeorphaNN: assessed by running it, not by reading about it

**12 Oct 2026. Asked to "run it and we will see". Here is what looking actually found.**

---

## The verdict first

**Do not start this before the 21 Oct freeze.** The scorer is trivially installable; the
*input pipeline* is a 2+ day build whose critical step has never been run by anyone who
published it. Recorded here so next season starts from step 2 rather than step 1.

---

## What is genuinely available

| | |
|---|---|
| code | `github.com/Zebreu/DeorphaNN`, **MIT licence**, 264 KB |
| weights | 10-model ensemble, auto-downloaded from HuggingFace, **reachable from our sandbox** |
| scorer dependencies | six: numpy, pandas, torch, torch-geometric, numpy-indexed, requests |
| scorer hardware | **CPU only** |
| authors' dataset | 22,504 files: 22,035 relaxed PDBs, 195 pair representations, 168 active-state templates |

## The shortcut worth recording

The dataset ships **active-state templates for all three human opioid receptors**:

```
active-state_templates__unprocessed/Human_GPCRs/OPRD-HUMANactive.pdb
active-state_templates__unprocessed/Human_GPCRs/OPRM-HUMANactive.pdb
active-state_templates__unprocessed/Human_GPCRs/OPRK-HUMANactive.pdb
```

That is **preprocessing step 1 already done for exactly our receptors** (AlphaFold-multistate
active-state prediction plus pLDDT/DeepTMHMM trimming). Anyone picking this up skips it.

## What is NOT available

**The authors did not score the opioid receptors.** The 19 published score tables are orphan
GPCRs (GPR132, GPR146, GPR15, GPR151, GPR152, GPR176, GPR19, GPR25, GPR3, GPR32, GPR33,
GPR39, GPR68, GPR83, MRGPRX3, NPR-33-1, NPR-34-1, NPR-44-1, SEB-2-1). There is no
ready-made answer for DOR or MOR to lift.

## The blocker

Per peptide-receptor pair, DeorphaNN needs four inputs: `*_gpcr_T.npy`, `*_pep_T.npy`,
`*_interaction.npy` and a `.contacts` file. Producing them requires:

1. **AlphaFold-Multimer with the internal pair-representation tensor saved.** This is not
   standard ColabFold output; it needs a patched run that dumps the pair representations.
2. **Arpeggio contacts via Docker.** Our cluster does not permit Docker.

The one public wrapper that promises this (`rrolli93/agonist-predict`) is commendably honest
in its own README: the fold-and-extract step is **"VERIFY-ON-GPU, written to spec, not run
here (no local GPU)"**. So the only available implementation of the step we need is itself
untested.

**With the calibration-panel control this project requires, that is 28 AlphaFold-Multimer
runs** (13 reference compounds + our payload, x 2 receptors) through an unverified pipeline.

### A third friction, read directly from the two sources

The authors' 195 shipped pair representations are **`.h5` files**
(`pair_representations/AEX-2-1_gpcr_T.h5`), but `deorphann_batch.py` globs for
`*gpcr_T.npy`, `*pep_T.npy`, `*interaction.npy` and `*.contacts`. **The authors' own example
data does not drop straight into the authors' own batch script**; a format conversion sits
between them, and the `.contacts` files are not in the dataset at all.

That is not a criticism of the work, it is a measurement of setup cost. It means the first
milestone for anyone resuming is not "score our peptide" but **"reproduce one published
score from the authors' own inputs"**, and even that requires writing a loader.

## Why the ceiling is lower than it looks

DeorphaNN discriminates **agonist from non-agonist**. Our question is delta-over-mu
preference between two human receptors sharing **18 of 29 orthosteric pocket residues**.
That is outside the method's demonstrated scope, and it was trained on C. elegans
peptide-GPCR pairs with human retrospective validation.

A null result would not distinguish "no preference" from "beyond the method's resolution",
which is exactly the ambiguity that limited Cycle 15. This is why the control (run the
13-compound panel first) is not optional: if it cannot rank compounds of known delta/mu
preference, it cannot rank ours.

## If it is ever picked up

1. Pull `OPRD-HUMANactive.pdb` and `OPRM-HUMANactive.pdb` from the authors' dataset.
2. Get AlphaFold-Multimer pair-representation extraction working on **one known pair from
   the authors' own data first**, and reproduce their published score for it. Until that
   reproduces, nothing downstream means anything.
3. Replace Arpeggio with a non-Docker contact calculator, or secure Docker/Apptainer.
4. Run the 13-compound calibration panel. **Only then** our payload.
