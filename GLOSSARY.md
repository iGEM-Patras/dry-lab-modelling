# Glossary

Terminology used throughout this repository, grouped by the task in which it arises rather
than alphabetically. No biology background assumed.

---

## Biology: the molecules

| Term | What it means |
|---|---|
| **Amino acid** | The 20 building blocks of proteins. Written as one letter (`Y`, `G`, `F`…) or three (`Tyr`, `Gly`, `Phe`). |
| **Peptide** | A short protein, roughly under 50 amino acids. Our payload `YGGFEVVG` is 8. |
| **Residue** | One amino acid *within* a chain. "Residue 5" = the 5th position. |
| **Protein** | A long amino-acid chain that folds into a 3D shape and does a job. |
| **Enkephalin** | A natural human opioid peptide, 5 residues. Met-enkephalin is `YGGFM`. Made by your own body for pain relief. |
| **PENK / proenkephalin** | The precursor protein that contains several enkephalin copies, cut out later by enzymes. UniProt `P01210`. Our construct is an engineered version. |
| **Deltorphin** | A frog-skin peptide that is strongly δ-selective. We borrowed its "address" region for our design. |
| **Opioid receptor** | The cell-surface protein that opioids bind. Two matter here: **δ (DOR, gene `OPRD1`)** and **μ (MOR, gene `OPRM1`)`. |
| **Neprilysin / NEP / MME** | The enzyme that destroys enkephalin within seconds. The `03_sirna_design/` arm silences it. |
| **Prohormone convertase (PC1/3, PC2)** | Enzymes that cut precursor proteins at pairs of basic residues (`KR`, `KK`, `RR`). They release our cassettes. |
| **Carboxypeptidase E (CPE)** | Trims leftover basic residues off the end after a convertase cut. |
| **Cathepsin L** | An alternative cutting enzyme, with different sequence preferences. Relevant in `07_`. |
| **Signal peptide** | A short tag at the front of a protein meaning "export me from the cell". Cut off during secretion. Predicted with DeepSig. |
| **Epitope** | The specific patch of a protein that an antibody recognises. We changed ours, which is why no commercial antibody detects our product. |

## Biology: the DNA side

| Term | What it means |
|---|---|
| **Codon** | Three DNA letters coding one amino acid. Multiple codons per amino acid → redundancy. |
| **Synonymous recoding** | Changing DNA without changing the protein, by swapping in alternative codons. Used to fix synthesis problems. |
| **GC content** | Fraction of DNA letters that are G or C. Too high or too low and synthesis fails. We target 40–45 %. |
| **CAI** (codon adaptation index) | 0–1 score of how closely codon choice matches the host's preferences. Higher is usually better expressed. Recoding for GC costs CAI: a real trade-off. |
| **Plasmid** | A circular DNA molecule you can put into cells. Our constructs are delivered this way. |
| **Construct / cassette** | An engineered stretch of DNA designed to do one thing. We have four constructs; each carries seven peptide cassettes. |
| **Kozak sequence** | A short motif before a start codon telling the cell to begin translating here. |
| **P2A** | A short self-cleaving peptide. Put it between two genes and one mRNA makes two separate proteins. |
| **IRES** | An alternative way to get two proteins from one mRNA. Slower for the second gene but no leftover tag. |
| **mEGFP** | A green fluorescent protein. Included so you can see under a microscope whether the construct is working. |
| **His6 tag** | Six histidines added to a protein so it can be purified on a nickel column (**IMAC**). |
| **Restriction enzyme** | A protein that cuts DNA at a specific short sequence. Used for the QC test in `02_`. |
| **siRNA** | A short RNA that silences a specific gene. Our anti-`MME` duplexes. |

## Measurement and modelling

| Term | What it means |
|---|---|
| **Binding free energy (ΔG)** | How tightly two molecules stick, in kcal/mol. **More negative = tighter.** |
| **ΔΔG ("delta delta G")** | The *difference* between two binding energies. Our selectivity measure: δ versus μ. Positive = δ-preferring in our convention. |
| **1.36 kcal/mol** | Equals a 10-fold difference in binding. Handy for converting energies to "N-fold selective". |
| **Ki / IC50** | Experimentally measured binding strength. Lower = tighter. What published papers report. |
| **δ-selectivity** | Preferring the δ receptor over μ. The whole point of the payload design. |
| **Agonist** | A molecule that activates a receptor. Our peptides are agonists. |
| **Antagonist** | A molecule that blocks a receptor without activating it. Several of our calibration references are antagonists, which is why the panel calibrates *binding*, not *effect*. |
| **Co-folding** | Predicting the 3D structure of two molecules together, e.g. peptide inside receptor. Done with Boltz-2. |
| **ipTM** | Boltz-2's confidence in the *interface* between two chains. 0–1, higher better. **Confidence, not correctness.** |
| **pLDDT** | Per-residue structural confidence, 0–100. Low pLDDT often means genuinely floppy, not merely uncertain. |
| **MD (molecular dynamics)** | Simulating atoms moving under physical forces, in femtosecond steps. Expensive. |
| **Force field** | The parameter set defining how atoms interact in MD. We use `ff14SB` for protein, MARTINI 2 for coarse-grained lipids. |
| **MM-GBSA** | A fast, approximate binding-energy method. Tried in Cycle 3b; failed its calibration gate. |
| **FEP / TI** | Free-energy perturbation / thermodynamic integration. The rigorous, expensive way to get ΔΔG. Cycle 8. |
| **λ window** | One intermediate step in an FEP calculation, where the molecule is partly "switched off". We use 27 per leg. |
| **Replicate** | A repeat of the same simulation with different starting velocities. Needed to estimate error. |
| **QSAR** | Predicting activity from chemical structure using machine learning. Used in Cycle 7's variant screen. |
| **Applicability domain** | Whether a new molecule resembles a model's training data enough for its prediction to mean anything. Our peptide sits outside the small-molecule domain, stated explicitly. |

## Statistics and our conventions

| Term | What it means |
|---|---|
| **Pre-registration** | Writing down predictions and pass/fail thresholds *before* running the test, and committing them to git. Our core convention. |
| **Gate** | A numeric pass/fail criterion fixed in advance. E.g. Cycle 7's "correlation must exceed 0.553". |
| **Falsified** | A prediction the data contradicted. We record these deliberately. |
| **Unresolved** | A prediction the experiment could not settle either way, distinct from falsified, and recorded separately. |
| **r (Pearson)** | Linear correlation, −1 to +1. Cycle 7 achieved r = 0.805. |
| **ρ (Spearman)** | Rank correlation: does the ordering match? Cycle 9 achieved ρ = 1.000, i.e. perfect ranking. |
| **p-value** | Probability of seeing a result this strong by chance. Below 0.05 is conventionally "significant". |
| **SEM** | Standard error of the mean: the uncertainty on an average. |
| **Critical r** | The correlation you must exceed for significance at a given sample size. We compute it from n rather than picking a threshold. |
| **Residency fraction** | The proportion of a simulation during which the peptide actually stayed in the pocket. **A bound-state ΔG is meaningless without it**: enforced by the tooling. |
| **DBTL** | Design–Build–Test–Learn. The iGEM engineering cycle. One cycle = one Learn→Design edge, not one construct. |

## Lab and infrastructure

| Term | What it means |
|---|---|
| **Transfection** | Putting DNA into cultured cells so they express it. |
| **HEK293T** | A common human cell line. **Our finding: it lacks the enzymes needed to process our precursor.** |
| **Conditioned medium** | The liquid cells have been growing in (contains whatever they secreted). Our starting material. |
| **IMAC** | Nickel-column purification that captures His6-tagged proteins. |
| **LC-MS/MS** | Mass spectrometry. Identifies peptides by exact mass. How we will confirm the payload was released. |
| **In vitro** | In a tube, outside a living organism. Our processing assay. |
| **Lipoplex** | A fat droplet carrying DNA into cells. The delivery vehicle in `04_`. |
| **SLURM** | The cluster job scheduler. `sbatch` to submit, `squeue` to check. |
| **GROMACS file types** | `.mdp` config · `.gro`/`.pdb` coordinates · `.top` topology · `.xtc`/`.trr` trajectory · `.xvg` numeric output · `.cpt` checkpoint |
| **UniProt accession** | Stable ID for a reference protein, e.g. `P01210` (PENK), `P41143` (OPRD1), `P35372` (OPRM1). |
| **ChEMBL ID** | Stable ID for a compound or target in the ChEMBL bioactivity database, e.g. `CHEMBL236` (δ receptor). |

---

## Sequences you will see repeatedly

| Sequence | What it is |
|---|---|
| `YGGFM` | Met-enkephalin: the natural human peptide |
| `YGGFEVVG` | **Our engineered payload**, 8 residues |
| `YGGF` | The shared "message" region of all opioid peptides: triggers the receptor |
| `EVVG` | Our "address" region: tunes receptor preference |
| `YGGFEVVGRF` | What the 7th cassette releases (extended, by design) |
| `KR`, `KK`, `RR` | Dibasic motifs: where the convertases cut |
| `MARFLTLCTWLLLLGPGLLATVRA` | The signal peptide: "secrete this protein" |
| `ATNFSLLKQAGDVEENPGP` | The P2A self-cleaving peptide |
