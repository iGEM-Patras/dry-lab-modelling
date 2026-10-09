# Engineered PENK peptide, wet-lab reference sheet

**Peptide:** engineered enkephalin analog **YGGFEVVG** (the octapeptide the
therapy plasmid is designed to release, ×7 per proprotein).
**Comparator:** native Met-enkephalin **YGGFM**.
**Date:** 2026-08-06. **Status:** design reference, peptide not yet synthesised or assayed in-house.

---

## 0. What this sheet is for

Three separate uses, and they need different things from it:

1. **Ordering synthetic standards**: §1 gives the sequences and the
   physicochemical properties a peptide vendor and your HPLC need.
2. **Detecting the peptide in transfected-cell supernatant**: §2 gives the MS
   transitions, and states which ones are useless.
3. **Structural figures / MD setup**: §3 covers the PDB files, and §4 states
   the limit on what they can be used for.

---

## 1. Synthetic standards to order

| | **Engineered** | **Native (comparator)** |
|---|---|---|
| Sequence (N→C) | H-Tyr-Gly-Gly-Phe-Glu-Val-Val-Gly-OH | H-Tyr-Gly-Gly-Phe-Met-OH |
| One-letter | `YGGFEVVG` | `YGGFM` |
| Length | 8 | 5 |
| Average MW | **826.90 Da** | 573.66 Da |
| Monoisotopic MW | **826.3861 Da** | 573.2257 Da |
| Isoelectric point | **3.29** | 5.94 |
| Net charge at pH 7.4 | **−1.01** | −0.01 |
| ε₂₈₀ | 1490 M⁻¹cm⁻¹ (1 Tyr) | 1490 M⁻¹cm⁻¹ (1 Tyr) |
| Termini | free amine / **free acid** | free amine / free acid |
| Stereochemistry | **all-L** | all-L |

**Order both.** The native peptide is not optional: it is the comparator every
δ-vs-µ selectivity claim in this project is made against, and it is also the
species already present in the cells you transfect.

### Three ordering details that are easy to get wrong

- **Free acid C-terminus, not amide.** The proprotein releases this peptide by
  proteolysis at a downstream dibasic site, which leaves a free carboxylate.
  Vendors default to C-terminal amide on many peptide syntheses; an amide would
  be a different molecule (−0.98 Da, and one fewer negative charge). Specify it.
- **All-L.** No D-amino acids anywhere. (Deltorphin-type analogs in the separate
  cycle-3b work do carry a D-residue at position 2, that is a *different*
  peptide, do not conflate the orders.)
- **No Met in the engineered peptide.** This is an advantage: the native
  pentapeptide's Met5 oxidises to the sulfoxide (+16 Da) on storage and during
  handling, and you will see it as a shoulder in the native standard's LC-MS.
  The engineered peptide has no oxidisable residue.

### Handling

Both are short, unstructured, and have no Cys, so no disulfide handling and no
refolding. Reconstitute in water or dilute aqueous buffer; the engineered peptide
is anionic at neutral pH (pI 3.29) so it stays soluble, but at pH ~3.3 it will be
at its solubility minimum: avoid formic-acid-heavy buffers for stock storage
(fine for the LC mobile phase). Aliquot and freeze; avoid repeated freeze-thaw.

Quantify by A₂₈₀ using ε = 1490 M⁻¹cm⁻¹ (**identical for both peptides**), since
both have exactly one Tyr and no Trp. Convenient: the same extinction
coefficient, different masses, so A₂₈₀ gives molar concentration directly and
comparably.

---

## 2. Detecting the peptide by LC-MS/MS

### Precursors

| Peptide | [M+H]⁺ | [M+2H]²⁺ |
|---|---|---|
| Engineered YGGFEVVG | **827.393** | 414.200 |
| Native YGGFM | **574.233** | 287.620 |

253.16 Da apart, trivially resolved at the precursor level.

### The critical constraint: b1–b4 are identical in both peptides

Both peptides begin `YGGF`. The b-ion series is therefore **numerically
identical** for the first four fragments:

| Fragment | Engineered | Native | Discriminating? |
|---|---|---|---|
| b1 | 164.071 | 164.071 | **no** |
| b2 | 221.092 | 221.092 | **no** |
| b3 | 278.114 | 278.114 | **no** |
| b4 | 425.182 | 425.182 | **no** |
| b5 | **554.225** | | yes |
| b6 | **653.293** | | yes |
| b7 | **752.362** | | yes |

**Quantify on b5, b6, or b7 only.** A method built on b2/b3/b4 (which are the
strong, commonly-chosen fragments for enkephalins in the literature, cannot
distinguish the engineered peptide from the native background, and you will be
measuring the sum of both. This is the single most likely way to get a false
positive from this assay.

y-ions: no coincidences between the two peptides at all, so any y-ion is
discriminating. Engineered y-series: y7 664.330, y6 607.309, y5 550.287,
y4 403.219, y3 274.176, y2 175.108, y1 76.039.

*(All fragment m/z are singly-protonated monoisotopic, computed from sequence.
No modifications assumed.)*

### Antibody detection: a warning

The same logic applies, and worse. Commercial anti-Met-enkephalin antibodies are
raised against the `YGGF` message domain, because that is the conserved opioid
motif. Such an antibody **will detect both peptides** and cannot be used to show
that the engineered peptide was produced. If you need immunodetection, it has to
be against the `EVVG` C-terminal extension, which means a custom antibody, and
a 4-residue epitope is a hard ask. **MS is the correct method here, not ELISA.**

---

## 3. Structure files

Two PDB files accompany this sheet:

| File | Contents |
|---|---|
| `engPENK_octapeptide_YGGFEVVG_DORbound.pdb` | engineered octapeptide, 8 residues, 58 atoms |
| `native_MetEnkephalin_YGGFM_DORbound.pdb` | native pentapeptide, 5 residues, 39 atoms |

Both extracted from the Boltz-2 co-folded complexes with the human δ-opioid
receptor already generated in this project (chain B of each), renumbered 1..N,
chain A. Backbone verified contiguous (Cα–Cα 3.77–3.82 Å, no breaks). These are
the exact coordinates the reported binding energies were computed on.

Receptor-bound geometry:

| Metric | Engineered | Native |
|---|---|---|
| Tyr1-OH → Phe4 ring centroid | 12.05 Å | 8.05 Å |
| Cα end-to-end | 12.12 Å | 6.81 Å |
| Radius of gyration (Cα) | 4.31 Å | 3.38 Å |

The Tyr1–Phe4 spacing is the **message-domain pharmacophore distance**: the
geometry that determines opioid-receptor engagement. It differs by 4.0 Å between
the two bound poses, i.e. the engineered peptide adopts a substantially more
extended conformation in the same binding site. That is a model prediction, and
it is the structural correlate of the predicted selectivity shift.

Model confidence (parent complexes): ipTM 0.972 (engineered) / 0.979 (native);
peptide-chain pTM 0.981 / 0.983; interface pair ipTM 0.809 / 0.757.

---

## 4. Limits: read before using the structures

**A linear octapeptide has no structure in isolation.** Enkephalins are
canonically disordered ligands; the coordinates above are *receptor-bound*
conformations, one member of a broad solution ensemble. They are valid for
rendering the bound pose, measuring contacts, and as MD starting coordinates
**inside the receptor**. They are not "the structure of the engineered
enkephalin", not comparable to a solution NMR ensemble, and not a rigid body for
re-docking.

**The selectivity prediction is computational and untested.** The project's
MM-GBSA gave ΔΔG_sel ≈ +4.05 kcal/mol favouring δ over µ for the engineered
peptide. That is a prediction from a docked model, not a measurement. The bench
test is a δ/µ binding or functional assay against both synthetic peptides, see
§5.

**No µ-receptor structures exist in the artifact store.** Only the δ complexes
were saved. A structural δ-vs-µ comparison would need those models regenerated.

---

## 5. What the bench should measure

The modelling makes exactly two falsifiable claims about this peptide. Both are
cheap to test once the standards are in hand:

1. **The peptide is produced and secreted.** Transfect, collect supernatant,
   LC-MS/MS on the b5/b6/b7 transitions. *Accept:* engineered peptide detectable
   above the untransfected control. This tests the cassette, the signal peptide,
   and the processing sites all at once.
2. **It prefers δ over µ.** Radioligand competition or functional (cAMP / β-arrestin)
   assay at both receptors, engineered vs native peptide, same day, same cells.
   *Accept:* δ/µ ratio higher for engineered than native. *If it is not,* the
   central pharmacological hypothesis is wrong, that is a real result and should
   be reported as one, not re-run until it agrees.

Note that claim 1 can succeed while claim 2 fails, and they are worth separating
in the experimental record for exactly that reason.

---

## 6. Provenance

Sequences read from the coordinate files, not transcribed. Masses, pI, net
charge, ε₂₈₀ and all fragment m/z computed from sequence (average and
monoisotopic residue masses; Henderson–Hasselbalch with standard side-chain pKa
values). Geometry measured directly from the PDB files. Every number in this
sheet was verified programmatically against the computation before release.
Design intent and the ΔΔG values come from the project's computational audit.
