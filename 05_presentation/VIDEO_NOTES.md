# Engineered PENK — structure assets for the video

## First, the correction that saves you a rebuild

**AlphaFold does not accept structure files.** AlphaFold Server, the AF database
and ColabFold all take a *sequence* and *produce* a structure. There is no input
field for a `.cif`. So the CIF files cannot be "put into AlphaFold" — but they
also don't need to be. They are already finished models; they go straight into a
viewer.

Use **ChimeraX** or **PyMOL** for the video. Both scripts here reproduce
AlphaFold's exact pLDDT colour scheme, so the shots cut together with your
existing AlphaFold footage seamlessly.

## What your screenshot actually is

The image you pasted is AlphaFold's prediction of the **288-aa engineered PENK
proprotein**: long extended coils, almost entirely orange and yellow, with one
small ordered region. That is not a failed prediction — it is correct, and it is
the most important scientific point in the whole video:

- **70 % of the proprotein is predicted disordered** (FoldIndex, 51-residue
  window, computed from the engineered CDS translation).
- **98 % of the residues inside the seven YGGFEVVG cores are disordered.**
- The one folded part is the N-terminal domain held by **7 cysteines**
  (positions 8, 26, 30, 33, 48, 52, 65) — that is the small ordered core visible
  in your screenshot, and the blue region at the left of the FoldIndex plot.

So the orange is the biology, not a modelling artifact. PENK is a disordered
carrier whose job is to be cut up.

## Why the proprotein alone can't tell the story

Each of the seven copies is flanked by dibasic protease sites — confirmed by
sequence, every core has **KR immediately upstream** and KR/KK/RR/RF downstream:

```
... KR | YGGFEVVG | KRY ...   (core at aa 100)
... KR | YGGFEVVG | KKM ...   (aa 110)
... KR | YGGFEVVG | KKD ...   (aa 142)
... KR | YGGFEVVG | RGL ...   (aa 195)
... KR | YGGFEVVG | RRV ...   (aa 222)
... KR | YGGFEVVG | KRF ...   (aa 245)
... KR | YGGFEVVG | RF  ...   (aa 279)
```

The mature octapeptide **never exists inside that fold**. It is cut out, secreted,
and only then adopts a conformation — when it binds a receptor. That is what the
CIF files show and what the proprotein prediction structurally cannot.

## Suggested three-shot sequence

| Shot | Asset | Beat |
|---|---|---|
| 1 | your existing AlphaFold proprotein render | "This is the gene product — mostly disordered, by design." |
| 2 | `engPENK_proprotein_vs_peptide.png` | "70 % disorder is the point. Seven cargo peptides on a floppy string, each flanked by protease sites." |
| 3 | `DOR_engPENK_complex_annotated.pdb` via either script | "Cut out and bound to its receptor, the peptide finally has a shape." |

Shot 3 is the payoff and it is the only shot with a real binding pose in it.

## The files

| File | Use |
|---|---|
| `DOR_engPENK_complex_annotated.pdb` | full δ-opioid receptor + peptide complex, 2888 atoms, pLDDT in B-factors, provenance in REMARK lines |
| `engPENK_video.cxc` | ChimeraX script — spin, focus pull to peptide, pharmacophore measurement |
| `engPENK_video.pml` | PyMOL script, same three shots, AF palette defined manually |
| `../peptide_structures_AFformat/*.cif` | the isolated peptides, AF-format mmCIF, for close-ups |

Both scripts end with the commented-out movie-encode line for your frame rate.

## Two things to get right on screen

**Colour honestly.** The pLDDT values in these files are **receptor-bound**
confidences (peptide mean 81.3, range 69.7–87.6). They are not free-peptide
confidences. If a caption says "AlphaFold confidence" over the peptide close-up,
that is wrong twice — wrong predictor (Boltz-2) and wrong context. "Model
confidence, receptor-bound" is accurate and just as short.

**Gly8 is the weakest residue at 69.7**, just below the conventional 70 cutoff,
and it will render yellow while everything else renders blue. That is not a
rendering bug — it is the C-terminal residue of the engineered extension, nearest
the processing site, and genuinely the least determined. If a viewer asks about
the one yellow residue, that is the honest answer.

## The measurement in shot 3

Both scripts draw the Tyr1-OH → Phe4-ring distance, the standard opioid
pharmacophore separation: **12.05 Å in the engineered peptide vs 8.05 Å in the
native**. It is a real, visual, one-number difference between the two molecules —
good on camera, and it is measured from the coordinates, not asserted.
