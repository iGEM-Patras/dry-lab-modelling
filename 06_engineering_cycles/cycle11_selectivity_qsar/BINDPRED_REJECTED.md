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
