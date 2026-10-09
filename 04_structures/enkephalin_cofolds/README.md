# Enkephalin co-folds, inputs

Boltz-2 co-folding of the two **native** enkephalins against both opioid receptors.
These are the reference structures the presentation captions refer to; before this
job ran there was **no structural model for Leu-enkephalin** in the project, and
`SLIDE_CAPTIONS.md` says so explicitly. Do not narrate a Leu-enkephalin binding
mode until these outputs exist and have been inspected.

| file | receptor | peptide |
|---|---|---|
| `DOR_Metenk.yaml` | OPRD1 (δ) | YGGFM (Met-enkephalin) |
| `DOR_Leuenk.yaml` | OPRD1 (δ) | YGGFL (Leu-enkephalin) |
| `MOR_Metenk.yaml` | OPRM1 (μ) | YGGFM |
| `MOR_Leuenk.yaml` | OPRM1 (μ) | YGGFL |

Both peptides are native **free acids**, no C-terminal amide. This is deliberate
and differs from the Cycle 3b design peptides, which are amidated.

`run_cofolds.sh` is the exact SLURM script submitted (job `17960676`):
15 diffusion samples, 3 recycling steps, MSA server on, PDB output.

Committed so the prediction is reproducible independently of cluster scratch , 
the first attempt (`17958370`) was cancelled with its inputs living only in a
temporary directory.
