# Do not use `fold_2026_07_19_20_17`: it modelled the DNA, not the protein

**Verified from the run's own `fold_2026_07_19_20_17_job_request.json`**, not inferred
from the picture. The submitted `proteinChain.sequence` was:

```
GCTAGCGCCACCATGGCTCGT ... GGTCGTTTCTGACTCGAG      (885 characters)
```

That string is **bit-identical to `engineered_PENK_cloning_ready_GC59.9pct`**, the
885-nt `NheI–Kozak–CDS–XhoI` DNA construct. It was submitted to a field that
expects amino acids.

## Why no error was raised

`A`, `C`, `G` and `T` are all valid one-letter amino-acid codes: Ala, Cys, Gly,
Thr. A DNA string is therefore a *syntactically valid* protein sequence. AlphaFold
accepted it silently, built an MSA, ran 10 recycles, and returned five ranked
models with confidence scores. Nothing in the output announces the mistake.

## The output's own numbers reject it

| Quantity | Value | Reading |
|---|---|---|
| Residues modelled | 885 | 3.07× the real protein's 288 |
| Distinct residue types | 4 (A/C/G/T only) | a real protein uses ~20 |
| Cys content | 207 residues, 23.4 % | chemically absurd |
| MSA depth | **1** | no homolog exists, because the molecule doesn't |
| Mean pLDDT | 32.1 (97 % below 50) | "very low" across essentially the whole chain |
| pTM | 0.16 – 0.18, all 5 models | no reliable global fold |
| `fraction_disordered` | 0.13 – 0.56 | AlphaFold's own disorder call, on nonsense |

MSA depth 1 is the single most diagnostic number. PENK is a well-conserved
vertebrate gene with abundant homologs; a real PENK submission returns a deep
alignment. Depth 1 means the search found nothing resembling the query.

## Submit this instead

`engPENK_proprotein_FOR_ALPHAFOLD.fasta` (the 288-aa translation of the CDS):

```
MARFLTLCTWLLLLGPGLLATVRAECSQDCATCSYRLVRPADINFLACVMECEGKLPSLK
IWETCKELLQLSKPELPQDGTSTLRENSKPEESHLLAKRYGGFEVVGKRYGGFEVVGKKM
DELYPMEPEEEANGSEILAKRYGGFEVVGKKDAEEDDSLANSSDLLKELLETGDNRERSH
HQDGSDNEEEVSKRYGGFEVVGRGLKRSPQLEDEAKELQKRYGGFEVVGRRVGRPEWWMD
YQKRYGGFEVVGKRFAEALPSDEEGESYSKEVPEMEKRYGGFEVVGRF
```

All seven `YGGFEVVG` cores present, no internal stop codons, correct signal
peptide at the N-terminus.

Note also that the DNA construct contains the **NheI site, the Kozak sequence and
the stop codon**: cloning scaffolding that is not part of the protein under any
interpretation. Even read as DNA it is not purely coding sequence.

## Two checks on the replacement run

1. **Length must read 288.** If the summary says anything else, the wrong string
   went in again.
2. **MSA depth should be in the hundreds or thousands.** Depth 1 a second time
   means the submission is still wrong. Do not proceed to render.

Expect genuinely low pLDDT over much of the correct protein too: PENK really is
largely disordered. But it will be *high* over the cysteine-rich N-terminal
domain (7 Cys at positions 8, 26, 30, 33, 48, 52, 65), and the MSA will be deep.
Both of those distinguish a correct result from this one.

## What this does not invalidate

- The **Boltz-2 δ-opioid-receptor complexes** and the excised peptide CIF files
  are unaffected: those were built from the correct 8-residue peptide sequence,
  verified by reading the sequence back out of the coordinates.
- The **FoldIndex disorder analysis** (70 % of the proprotein, 98 % within the
  peptide cores) was computed from the correct 288-aa translation and stands.

What must not happen is presenting a disorder claim on screen backed by this run.
Use AlphaFold's own output on the correct sequence, or cite the FoldIndex
calculation, not a model of an 885-residue Ala/Cys/Gly/Thr polymer.
