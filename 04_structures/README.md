# 04 · Structures

Predicted three-dimensional structures of peptide–receptor complexes, and the inputs that
produced them.

| Contents | What it is |
|---|---|
| `enkephalin_cofolds/` | Boltz-2 co-folding inputs (`.yaml`) and outputs for enkephalin analogues against the δ- and μ-opioid receptors |
| `engPENK_alphafold_per_residue_plddt.csv` | Per-residue confidence for the engineered proenkephalin, used to establish that all cleavage sites lie in disordered regions |
| `engPENK_alphafold_CORRECTED_confidences.json` | Global confidence metrics for the same prediction |

## Reading the confidence scores

**ipTM** (0–1) measures confidence in how two chains are positioned relative to each other.
**pLDDT** (0–100) measures per-residue confidence in local structure.

Both are *confidence*, not correctness, and neither is a binding affinity. Two results in
this project depend on that distinction:

- Co-folds of our payload score ipTM ≈ 0.86 at δ and ≈ 0.87 at μ, high, and effectively
  identical. Cycle 7 accordingly **failed** its gate for using the confidence difference as
  a selectivity metric.
- The engineered proenkephalin's low pLDDT reflects genuine disorder by design, not model
  failure. `fraction_disordered` is 0.83, and the cleavage sites sit in that region, which
  is what makes them sterically accessible to the processing enzymes.

## A note on output formats

Boltz-2 writes **mmCIF** (`.cif`) by default, not PDB. Downstream tooling in
`06_engineering_cycles/cycle8_fep/` expects PDB and converts explicitly. A search for
`*.pdb` in a Boltz output tree will find nothing even when the prediction succeeded.

Declaring a peptide as a `ligand` (SMILES) rather than a `protein` chain yields correct
chemistry but no backbone topology, which force-field tools cannot parametrise. Cycle 7
used the ligand form; Cycle 8 required the protein-chain form and re-ran the co-folds.
