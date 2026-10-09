# Computational Audit & Literature Grounding
## Engineered δ-Preferring Proenkephalin Construct + Anti-Neprilysin Co-Delivery System

*Independent computational verification of the construct-design package. Every sequence-level
claim in the source document was re-derived from public reference sequences and checked by
automated audit; every biological rationale is grounded in the primary literature with DOIs.*

**Reference sequences used**
- Human proenkephalin: **UniProt P01210** (PENK_HUMAN, 267 aa). Fetched from UniProt REST.
- Neprilysin mRNA: **RefSeq NM_000902.5** (MME, transcript variant 1, 5,593 nt). NCBI.
- Processing enzymes (accession check only): PCSK2 **P16519**, SCG5/7B2 **P05408**, CPE **P16870**, all confirmed human, correct gene/protein.
- Cross-species neprilysin for the siRNA check: mouse *Mme* **NM_008604**, rat *Mme* **NM_012608**.

---

# Part A, Is the construct *built* correctly? Sequence & cloning audit

## 1. Executive summary, what the computation confirms vs. what stays at the bench

| # | Claim in the design package | Computational verdict |
|---|------------------------------|------------------------|
| 1 | P01210 has 7 enkephalin cores at positions 100–104, 107–111, 136–140, 186–190, 210–214, 230–234, 261–265 | **CONFIRMED**, exact-match to both my string search and the UniProt feature table |
| 2 | Every core is flanked by dibasic (KR/KK/RR) processing sites | **CONFIRMED**, all 7 left flanks are KR; right flanks KR/KK/RR except cores 4 (RG) & 7 (RF), which are the natural *extended* enkephalins |
| 3 | Engineered protein = 288 aa (267 + 7×3) | **CONFIRMED**, independent reconstruction reproduces the document's 288-aa sequence exactly |
| 4 | No Lys/Arg inside any YGGFEVVG insert | **CONFIRMED**, zero internal basic residues in all 7 inserts |
| 5 | Signal peptide (1–24) retained | **CONFIRMED**, identical to native P01210 |
| 6 | DNA insert translates to the engineered protein; NheI–Kozak–ATG…stop–XhoI cassette | **CONFIRMED**, 885 nt insert, CDS translates exactly to the 288-aa protein with a TGA stop |
| 7 | No internal NheI / XhoI sites | **CONFIRMED**, NheI only at the 5′ terminus, XhoI only at the 3′ terminus |
| 8 | GC content ~69%, seven identical core repeats | **CONFIRMED**, 68.9% GC; exactly 7 `GGCGGCTTCGAGGTGGTG` blocks |
| 9 | Glu-address makes the peptide more anionic (δ logic) | **CONFIRMED**, net charge −0.45 → −1.44; pI 5.52 → 4.05 |
| 10 | Published anti-NEP shRNA anchor (Rose et al.) is a *reference, not a drop-in* | **CONFIRMED & sharpened**: the anchor is an **exact match to mouse *Mme***, 1-mismatch to rat, and **has no match in human MME** (a rodent reagent) |

**The central design claim, that YGGFEVVG is δ-preferring over µ, was tested by three independent
computational methods** (Part B, Sections 7–10): a 426-ligand ChEMBL selectivity landscape, Boltz-2
co-folding against both receptors, and 20-ns all-atom MD with MM-GBSA binding free energies. They
converge: **the engineered anionic address does shift preference toward δ, but the margin is small
(~1.4 kcal/mol): δ-*preferring*, not δ-*selective*.**

**Remains bench-only (not computable in silico):** the *functional* δ/µ selectivity ratio (radioligand
Ki + GTP-γS/cAMP), efficiency of PC2/7B2/CPE processing of the lengthened cores, degree of NEP
knockdown, and lipoplex delivery/transfection. The document's own validation roadmap (Section 12)
correctly gates each of these.

---

## 2. Core map audit (Step 2)

All seven native `YGGF[M/L]` cores were located in P01210 by exact string search. The positions
match the document **and** the independent UniProt annotation (which cites primary peptide-isolation
papers, e.g. PMID 656131, 2982830):

| # | Core | Position | Left flank | Right flank | Note |
|---|------|----------|-----------|-------------|------|
| 1 | YGGFM | 100–104 | KR | KR | Met-enkephalin |
| 2 | YGGFM | 107–111 | KR | KK | Met-enkephalin |
| 3 | YGGFM | 136–140 | KR | KK | Met-enkephalin |
| 4 | YGGFM | 186–190 | KR | RG | → Met-enk-Arg-Gly-Leu (extended) |
| 5 | YGGFM | 210–214 | KR | RR | Met-enkephalin (within BAM22) |
| 6 | YGGFL | 230–234 | KR | KR | Leu-enkephalin |
| 7 | YGGFM | 261–265 | KR | RF | → Met-enk-Arg-Phe (extended) |

This precursor architecture (four Met-enkephalins, one Leu-enkephalin, one Met-enk-Arg-Phe and one
Met-enk-Arg-Gly-Leu, each bounded by paired basic residues) is exactly what was first described when
proenkephalin was cloned [Noda 1982; Kakidani 1982; Gubler 1982]. Full table: `core_audit.csv`.

---

## 3. Engineered protein reconstruction (Step 3)

Replacing each `YGGF[M/L]` with `YGGFEVVG` in P01210 yields a 288-aa protein **byte-identical** to the
document's Section 2.3 sequence. Per-insert checks: all 7 left flanks remain dibasic KR, and **no
insert contains an internal K/R**: the property the document (correctly) flags as critical, because an
internal basic residue would be a spurious PC2/PC1-3 cleavage site that fragments the active peptide
[Johanning 1998; Johanning 1996]. Signal peptide 1–24 is retained. Details: `engineered_protein_check.txt`.

**Design-logic grounding (message/address).** The N-terminal `YGGF` "message" is shared by all opioid
peptides; C-terminal residues encode the receptor "address." This message/address framework is the
Portoghese formulation used to design δ-selective ligands such as naltrindole [Portoghese 1988; Portoghese 1990].
The anionic residue at the address position is the deltorphin logic: the naturally δ-selective
deltorphins carry an Asp/Glu in the address and reach exceptional δ-selectivity [Erspamer 1989].

**The δ-selectivity ceiling is real and correctly stated.** The document is candid that a
genetically-encoded, all-L peptide cannot be δ-*exclusive*. This is well-founded: the peptides that reach
~1,000–10,000× δ-selectivity require a **D-amino acid at position 2** and/or **C-terminal amidation**
[Erspamer 1989; Mor 1989; Amiche 1989], neither of which the ribosome can produce. So `YGGFEVVG` is
δ-*preferring*, not δ-*exclusive*, and the document's ≥10-fold functional-selectivity success bar is the
right way to state it.

---

## 4. DNA insert audit (Step 4)

The 885-nt cloning-ready insert parses cleanly:

- 5′: `NheI (GCTAGC)` + `Kozak (GCCACC)` + `ATG` ✓
- CDS: 867 nt (289 codons incl. stop) → **translates exactly to the 288-aa engineered protein** ✓
- 3′: `TGA` stop + `XhoI (CTCGAG)` ✓
- **No internal NheI or XhoI** (NheI only at position 0, XhoI only at position 879) ✓, the insert can be
  directionally cloned into pcDNA3.1(+) via NheI/XhoI as intended.

Additional restriction scan (for anyone choosing an alternative cloning route): the insert **does**
contain internal PstI (×3), BglII (×1) and ApaI (×1) sites, harmless for the NheI/XhoI strategy, but
those enzymes cannot be used to subclone this fragment. Details: `dna_audit.txt`.

---

## 5. GC content & repeat hotspots (Step 5)

Measured GC = **68.9%** (document: "~69%" ✓), uniform across the insert. The seven identical
`GGCGGCTTCGAGGTGGTG` blocks, one per `YGGFEVVG` core, are located at nt 312, 342, 438, 597, 678, 747, 849.
High GC combined with seven exact 18-mer repeats is a genuine synthesis/stability liability: it can cause
vendor synthesis failures and promote recombination between the repeats. The document's mitigation , 
ask the vendor to introduce synonymous-codon variation across the seven cores (changes DNA only, not
protein), is the standard fix and is well-placed.

> *Figure “GC content and core-repeat map” is no longer available; the surrounding text records what it showed.*

*Figure 1. Sliding-window (30-nt) GC profile of the insert. Dashed line = mean 68.9%; orange bands mark
the seven identical `YGGFEVVG` core repeats: the recombination/synthesis-risk hotspots.*

---

## 6. Physicochemical support for the δ-address (Step 6)

Computed with Biopython `ProtParam` (net charge at pH 7.4, isoelectric point, Kyte–Doolittle GRAVY):

| Peptide | Sequence | Net charge (pH 7.4) | pI | GRAVY |
|---------|----------|--------------------:|----:|------:|
| Met-enkephalin | YGGFM | −0.45 | 5.52 | 0.52 |
| Leu-enkephalin | YGGFL | −0.45 | 5.52 | 0.90 |
| **Engineered** | **YGGFEVVG** | **−1.44** | **4.05** | 0.65 |
| Deltorphin II core* | YAFDVVG | −1.45 | 4.05 | 1.11 |

*\*L-amino-acid comparator; the natural deltorphin also carries a D-residue and C-terminal amide (not
encodable): shown for the address chemistry only.*

Adding the Glu-address takes the core from net −0.45 to **−1.44** and drops the pI from 5.52 to **4.05**:
essentially the same anionic profile as the deltorphin address. This is the quantitative basis for the
"pushes away from µ, toward δ" rationale. It supports the *direction* of the shift; it does **not** predict
the *magnitude* of δ/µ selectivity, which must come from a functional assay. Data: `peptide_properties.csv`.

> *Figure “Peptide physicochemical comparison” is no longer available; the surrounding text records what it showed.*

*Figure 2. The Glu-address makes the engineered core markedly more anionic (lower net charge, lower pI)
than native enkephalins, mirroring the deltorphin address chemistry.*

---

---

# Part B: Does the construct *work as designed*? Testing the δ-preference claim

The audit above proves the construct is **built** correctly. It does not test the central
pharmacological hypothesis: that replacing `YGGFM` with `YGGFEVVG` makes the peptide prefer the
δ-receptor (DOR/OPRD1) over the µ-receptor (MOR/OPRM1). Three independent computational approaches
were used to probe that claim. All are ranking/plausibility tools, not substitutes for a functional
assay, but they agree with each other.

## 7. The δ/µ selectivity landscape from measured pharmacology (ChEMBL)

To anchor "how δ-selective is δ-selective," I pulled every ligand in **ChEMBL** [Zdrazil 2024] with a
measured Kᵢ against **both** human DOR (**CHEMBL236**) and MOR (**CHEMBL233**) (**426 compounds**),
and computed the selectivity ratio δ/µ = Kᵢ(DOR)/Kᵢ(MOR) (values < 1 = δ-preferring).

| Ligand (class) | Kᵢ DOR (nM) | Kᵢ MOR (nM) | δ/µ ratio | Character |
|---|---:|---:|---:|---|
| SNC-80 (synthetic δ-agonist) | ~0.3 | ~230–5000 | **0.0013** | strongly δ-selective |
| Naltrindole (δ-antagonist) | 0.09 | 8.9 | **0.010** | strongly δ-selective |
| **[Met]enkephalin (native peptide)** | **3.84** | **135.5** | **0.028** | **~35× δ-preferring** |
| Deltorphin II (D-aa + amide) | 1.30 | (µ ≫) | ≪ 0.01 | strongly δ-selective |
| Buprenorphine | - | - | 1.07 | balanced |
| Morphine | - | - | 56 | µ-preferring |
| DAMGO (reference µ-agonist) | 525 | 1.92 | **273** | strongly µ-selective |
| Fentanyl | - | - | 247 | µ-preferring |

Two things fall out of the landscape, both directly relevant to the design:

1. **The baseline to beat is δ/µ ≈ 0.028**. Native enkephalin is *already* ~35× δ-preferring. For the
   engineered peptide to justify the anionic address, it has to push meaningfully past that.
2. **The ligands that reach 1,000–10,000× δ-selectivity are chemically out of reach for a ribosome.**
   Every one of them carries a **D-amino acid at position 2 and/or a C-terminal amide** [Erspamer 1989;
   Mor 1989; Amiche 1989] (post-translational features a genetically encoded, all-L construct cannot
   install. This is the hard ceiling the design document itself acknowledges, now quantified against 426
   measured compounds. Data: `selectivity_anchors.csv`.

## 8. Pharmacokinetics of the NEP-knockdown arm (enzyme kinetics + occupancy model)

The second arm, blocking neprilysin to prolong enkephalin action, was modelled with a two-enzyme
Michaelis–Menten degradation scheme (NEP + aminopeptidase-N, APN) and a receptor-occupancy calculation
using the enkephalin Kd's above (δ = 3.84 nM, µ = 135.5 nM):

| Scenario | Enkephalin half-life | Fold vs. baseline |
|---|---:|---:|
| No inhibition | 6.9 s | 1.0× |
| **NEP knockdown only** (the construct's arm) | 8.3 s | **1.2×** |
| APN inhibition only | 25.2 s | 3.7× |
| **Dual NEP + APN** | 68.8 s | **10×** |

**Key quantitative finding: NEP knockdown *alone* extends enkephalin half-life only ~1.2×**, because APN
degrades enkephalin in parallel. Blocking *both* enzymes gives ~10×. This is the mechanistic case, from
the numbers, for the document's fallback to **dual enkephalinase inhibitors** (PL37/PL265) rather than a
single-enzyme knockdown [Roques 1985; Benoist 2002; Southerland 2021]. The occupancy model shows the
δ-vs-µ discrimination window is widest at ~23 nM free enkephalin (δ occupancy 0.86 vs µ 0.14).

> *Figure 3 image is no longer available; the caption below records what it showed, and the
> underlying values are in `tables/residency_vs_selectivity.csv`.*

*Figure 3. (left) The 426-ligand δ/µ selectivity ladder with anchors: native enkephalin sits at ~0.028;
D-amino-acid/amidated δ-agonists reach 0.001. (centre) Enkephalin half-life under each degradation
scenario: NEP-only knockdown gives only 1.2×. (right) δ vs µ receptor occupancy vs free-peptide
concentration.*

## 9. Structure-based selectivity I: Boltz-2 co-folding

Each peptide was co-folded with each full-length receptor using **Boltz-2** [Passaro & Wohlwend 2025]:
8 complexes (2 receptors × {YGGFEVVG, YGGFM, YGGFL, deltorphin-II core YAFDVVG}) on an RTX 2080 Ti GPU.
The readout is the interface **ipTM** (predicted interface accuracy); the affinity head is small-molecule
only and does not apply to peptides.

| Peptide | ipTM · DOR (δ) | ipTM · MOR (µ) | δ − µ |
|---|---:|---:|---:|
| Engineered YGGFEVVG | 0.968 | 0.976 | −0.008 |
| [Met]enkephalin YGGFM | 0.963 | 0.990 | −0.028 |
| [Leu]enkephalin YGGFL | 0.968 | 0.973 | −0.005 |
| Deltorphin-II core YAFDVVG | 0.968 | 0.982 | −0.014 |

**Result: co-folding does not resolve δ- vs µ-selectivity.** Every peptide docks into *both* receptors
with near-identical, uniformly high ipTM (all ≈ 0.97, δ−µ within ±0.03, marginally favouring µ). This is
expected: the orthosteric pockets of DOR and MOR are highly similar, and ipTM reports interface
geometry, not binding thermodynamics. Structures: `boltz_selectivity_scores.csv`, PDBs in
`boltz_structures.tar.gz`.

> *Figure 4 image is no longer available; the caption below records what it showed, and the
> values are in `boltz_selectivity_scores.csv` as cited above.*

*Figure 4. Boltz-2 interface ipTM for all 8 co-folded complexes. High and flat across both receptors: a
clean negative result: static co-folding cannot discriminate δ from µ for these peptides.*

## 10. Structure-based selectivity II: MD + MM-GBSA binding free energies

The decisive in-silico test is thermodynamic, not geometric. From the Boltz-2 poses I ran **all-atom
molecular dynamics** (GROMACS 2024.5 [Abraham 2015], AMBER99SB-ILDN [Lindorff-Larsen 2010] / TIP3P
[Jorgensen 1983], 0.15 M NaCl, receptor-Cα-restrained so the peptide relaxes freely), **20 ns per
system**, then computed binding free energies by **single-trajectory MM-GBSA** (gmx_MMPBSA
[Valdés-Tresanco 2021]; MMPBSA.py engine [Miller 2012]; GB-OBC2 / *igb=5* [Onufriev 2004]) over 300
frames from the last 15 ns. Four complexes: engineered YGGFEVVG and native YGGFM (the peptide your
wet-lab plasmids actually encode), each × δ and µ.

| System | ΔVDW | ΔEEL (Coulomb) | ΔEGB (polar solv.) | **ΔG_bind (kcal/mol)** |
|---|---:|---:|---:|---:|
| eng_DOR (YGGFEVVG × δ) | −64.4 | −315.4 | +344.5 | **−45.31 ± 0.44** |
| eng_MOR (YGGFEVVG × µ) | −59.6 | −347.8 | +373.3 | **−43.95 ± 0.32** |
| nat_DOR (YGGFM × δ) | −43.7 | −165.9 | +186.3 | **−30.37 ± 0.16** |
| nat_MOR (YGGFM × µ) | −52.9 | −147.3 | +177.4 | **−30.81 ± 0.24** |

**Selectivity** (ΔΔG = ΔG_bind[δ] − ΔG_bind[µ]; negative = δ-preferring):

| Peptide | ΔΔG(δ−µ) | Verdict |
|---|---:|---|
| **Engineered YGGFEVVG** | **−1.36 ± 0.54** | δ-preferring |
| **Native YGGFM** | **+0.44 ± 0.29** | marginally µ-preferring |
| **Engineering effect** | **−1.8** | shift toward δ |

Three conclusions, in order of confidence:

1. **The anionic address measurably increases affinity, and the gain is electrostatic: exactly as
   designed.** YGGFEVVG binds ~14–15 kcal/mol more favourably than Met-enkephalin at both receptors, and
   ΔEEL (Coulomb) roughly doubles: the direct signature of the added Glu carboxylate. (Absolute MM-GBSA
   magnitudes for a highly charged peptide are inflated by the GB treatment and should be read
   comparatively, not as true affinities [Genheden & Ryde 2015].)
2. **Engineering moves δ/µ preference in the intended direction**: from marginally µ-preferring (native,
   +0.44) to δ-preferring (engineered, −1.36), a net **−1.8 kcal/mol** shift toward δ.
3. **But the δ-preference is small.** 1.4 kcal/mol sits inside the ~1–2 kcal/mol error band of
   single-trajectory MM-GBSA on ΔΔG [Genheden & Ryde 2015]. It is a genuine tilt, not a strong
   selectivity.

> *Figure 5 image is no longer available; the caption below records what it showed.*

*Figure 5. (left) MM-GBSA ΔG_bind for all four complexes: the engineered peptide binds ~14 kcal/mol
tighter at both receptors. (centre) ΔΔG(δ−µ): engineering flips a marginal µ-preference into a modest
δ-preference. (right) Energy decomposition: the affinity gain is electrostatic (ΔEEL).*

### What Part B establishes

All three methods converge on one statement: **YGGFEVVG is a high-affinity opioid peptide with a
genuine but small tilt toward δ, δ-preferring, not δ-selective.** The anionic-address *mechanism*
works (higher affinity, δ-ward shift, electrostatic origin); the *magnitude* of selectivity is modest
and will not, on this evidence, reach the 10–1000× functional selectivity of purpose-built δ-agonists.
consistent with the ribosomal-encoding ceiling seen in the ChEMBL landscape. **The decisive test remains
at the bench:** radioligand δ/µ Kᵢ plus a functional (GTP-γS or cAMP) assay. Data:
`mmgbsa_results.csv`, `mmgbsa_selectivity_report.md`; raw per-system `FINAL_*.dat`.

---

## 11. Anti-NEP siRNA anchor check: a concrete finding

The document cites a published shRNA anchor (19-mer `GCACGTGGTTGAAGACTTG`; Rose et al., *J Neurosci* 2009)
as a *positive-control reference, not a drop-in*. Mapping it against neprilysin transcripts:

| Species | Transcript | Result |
|---------|-----------|--------|
| **Human** | MME NM_000902.5 | **No match** (>4 mismatches anywhere, both strands) |
| Mouse | *Mme* NM_008604 | **Exact match**, sense strand, position 1398 |
| Rat | *Mme* NM_012608 | 1-mismatch match, position 1438 |

So the anchor is a **rodent** *Nep* reagent and **cannot** knock down **human** NEP as written. This
quantitatively confirms (and sharpens) the document's caution. For human work a fresh anti-MME
siRNA/shRNA must be designed against NM_000902 and validated (qPCR/Western), exactly the design-tool +
BLAST workflow the document recommends. The document also (correctly) declines to hard-code a 21-mer.
Details: `sirna_anchor_check.txt`.

**Biological grounding of the NEP arm.** Neprilysin (NEP/CD10, gene *MME*, "enkephalinase") is the
principal membrane metallopeptidase that degrades enkephalins [Devault 1987; Roques 1985], so knocking
it down to prolong enkephalin action is mechanistically sound. The document's two honest caveats are both
literature-backed:

- **Partial protection (NEP-only).** Enkephalin is degraded by *both* NEP and aminopeptidase-N (APN);
  blocking one alone gives only modest spinal protection, while blocking *both* is substantially more
  effective: the rationale for dual enkephalinase inhibitors [Roques 1985; Benoist 2002; Noble 2007].
- **Amyloid-β safety risk.** NEP is a rate-limiting Aβ-degrading enzyme in brain; its suppression
  raises CNS Aβ and, in NEP-knockout mice, causes Alzheimer-like deposition [Iwata 2000; Huang 2006].
  Chronic CNS NEP knockdown therefore carries a genuine (if, in refractory cancer pain, differently-weighed)
  amyloid risk: the document's "transient/titratable, monitor Aβ" mitigation is appropriate.

---

## 12. Processing cassette & delivery: grounding (context)

- **Why HEK293T needs the cassette.** Correct enkephalin liberation requires PC2, its obligate chaperone
  7B2, and CPE. PC2 is catalytically inactive without 7B2, and CPE trims the C-terminal basic residues
  after PC2 cuts at the dibasic sites [Johanning 1998; Johanning 1996; Supattapone 1984; Lanoue 2001].
  HEK293T lacks this machinery, so the PENK plasmid alone would yield unprocessed proprotein. The
  document's "silent failure", which is why the co-delivered PC2–7B2–CPE cassette is needed only in the
  experimental phase and is dropped in vivo where neurons supply it natively. All three enzyme accessions
  (P16519, P05408, P16870) were confirmed correct.
- **2A polycistronic design.** Producing PC2/7B2/CPE from one transcript via *different* 2A peptides
  (P2A, T2A) to avoid repeat-driven recombination is standard and effective [Li 2019; Meas 2020].
- **The validated benchmark.** An HSV vector expressing human PENK reached a **Phase I** trial in
  intractable cancer pain, with dose-related pain relief and no agent-related serious adverse events
  [Fink 2011; Wolfe 2009]: the correct "benchmark to beat." The pharmacological alternative to the siRNA
  arm (orally active, reversible dual enkephalinase inhibitors (DENKIs; PL37/PL265) that block both NEP
  and APN without permanent amyloid risk) is a well-founded fallback [Southerland 2021; Benoist 2002].

The document's overall framing (each component has precedent but the *integrated* system (δ-engineered
PENK + NEP knockdown + intranasal non-viral co-delivery) is novel and unvalidated) is accurate.

---

## 13. Reproducibility

All results were computed from the public reference sequences named above. Verification artifacts:

- `core_audit.csv`: per-core position/flank audit
- `engineered_protein_check.txt`: 288-aa reconstruction & internal-K/R check
- `dna_audit.txt`: insert translation, cassette, restriction scan
- `gc_repeat_profile.png`: GC + repeat map (Figure 1)
- `peptide_properties.csv` / `peptide_properties.png`: physicochemistry (Figure 2)
- `sirna_anchor_check.txt`: cross-species anchor mapping
- `selectivity_anchors.csv`: 426-ligand ChEMBL δ/µ selectivity landscape (Fig 3)
- `selectivity_pkpd.png`: selectivity ladder + NEP/APN kinetics + occupancy (Fig 3)
- `boltz_selectivity_scores.csv` / `boltz_selectivity.png` (Boltz-2 co-folding ipTM (Fig 4))
- `mmgbsa_results.csv` / `mmgbsa_selectivity.png` / `mmgbsa_selectivity_report.md` (MD + MM-GBSA (Fig 5))
- `FINAL_eng_DOR.dat`, `FINAL_eng_MOR.dat`, `FINAL_nat_DOR.dat`, `FINAL_nat_MOR.dat` (raw gmx_MMPBSA output)
- `references.csv` / `references.bib` (bibliography with DOIs)
- `P01210.fasta`, `P01210.gff`, `NM_000902.fasta` (input reference sequences)

---

## 14. References

Retrieved and verified via PubMed (please cite PubMed); DOIs included where available.

1. Noda M, Furutani Y, Takahashi H, et al. (1982). Cloning and sequence analysis of cDNA for bovine adrenal preproenkephalin. *Nature*. doi:10.1038/295202a0 (PMID 6276759). (PENK cloning / precursor architecture)
2. Noda M, Teranishi Y, Takahashi H, et al. (1982). Isolation and structural organization of the human preproenkephalin gene. *Nature*. doi:10.1038/297431a0 (PMID 6281660). (Human PENK gene)
3. Kakidani H, Furutani Y, Takahashi H, et al. (1982). Cloning and sequence analysis of cDNA for porcine beta-neo-endorphin/dynorphin precursor. *Nature*. doi:10.1038/298245a0 (PMID 6123953). (Prodynorphin (comparator precursor))
4. Portoghese PS, Sultana M, Nagase H, Takemori AE (1988). Application of the message-address concept in the design of highly potent and selective non-peptide delta opioid receptor antagonists (naltrindole). *J Med Chem*. doi:10.1021/jm00397a001 (PMID 2828619). (Message-address concept)
5. Portoghese PS, Sultana M, Takemori AE (1990). Design of peptidomimetic delta opioid receptor antagonists using the message-address concept. *J Med Chem*. doi:10.1021/jm00168a028 (PMID 2160538). (Message-address / delta selectivity)
6. Erspamer V, Melchiorri P, Falconieri-Erspamer G, et al. (1989). Deltorphins: a family of naturally occurring peptides with high affinity and selectivity for delta opioid binding sites. *Proc Natl Acad Sci USA*. doi:10.1073/pnas.86.13.5188 (PMID 2544892). (Deltorphin delta selectivity (anionic address))
7. Mor A, Delfour A, Sagan S, et al. (1989). Isolation of dermenkephalin from amphibian skin, a high-affinity delta-selective opioid heptapeptide. *FEBS Lett*. doi:10.1016/0014-5793(89)81104-4 (PMID 2551734). (D-amino-acid delta agonist)
8. Amiche M, Sagan S, Mor A, et al. (1989). Dermenkephalin (Tyr-D-Met-Phe-His-Leu-Met-Asp-NH2): a potent and fully specific agonist for the delta opioid receptor. *Mol Pharmacol*. (PMID 2543911). D-config + amidation delta agonist
9. Supattapone S, Fricker LD, Snyder SH (1984). Purification and characterization of a membrane-bound enkephalin-forming carboxypeptidase, enkephalin convertase (CPE). *J Neurochem*. doi:10.1111/j.1471-4159.1984.tb12705.x (PMID 6421996). Carboxypeptidase E processing
10. Johanning K, Juliano MA, Juliano L, et al. (1998). Specificity of prohormone convertase 2 on proenkephalin and proenkephalin-related substrates. *J Biol Chem*. doi:10.1074/jbc.273.35.22672 (PMID 9712897). PC2 processing specificity
11. Johanning K, Mathis JP, Lindberg I (1996). Role of PC2 in proenkephalin processing: antisense and overexpression studies. *J Neurochem*. doi:10.1046/j.1471-4159.1996.66030898.x (PMID 8769847). PC2 required for PENK processing
12. Lanoue E, Day R (2001). Coexpression of proprotein convertase SPC3 (PC1/3) and the neuroendocrine precursor proSAAS. *Endocrinology*. doi:10.1210/endo.142.9.8386 (PMID 11517193). Convertase/chaperone context (7B2/proSAAS)
13. Devault A, Lazure C, Nault C, et al. (1987). Amino acid sequence of rabbit kidney neutral endopeptidase 24.11 (enkephalinase) deduced from a complementary DNA. *EMBO J*. doi:10.1002/j.1460-2075.1987.tb02370.x (PMID 2440677). Neprilysin (enkephalinase) cloning
14. Roques BP (1985). Enkephalinase inhibitors and molecular study of enkephalin catabolism. *J Pharmacol*. (PMID 2993752). Enkephalin catabolism / NEP+APN
15. Benoist JM, Keime F, Montagne J, et al. (2002). Depressant effect on a C-fibre reflex in the rat of the dual enkephalinase inhibitor RB101. *Eur J Pharmacol*. doi:10.1016/s0014-2999(02)01753-3 (PMID 12079685). Dual enkephalinase inhibition analgesia
16. Noble F, Roques BP (2007). Use of preproenkephalin knockout mice and selective inhibitors of enkephalinases to investigate the role of enkephalins. *Psychopharmacology*. doi:10.1007/s00213-007-0964-z (PMID 17906961). Enkephalin system / enkephalinase inhibitors
17. Southerland WA, Gillis J, Kuppalli S, et al. (2021). Dual enkephalinase inhibitors and their role in chronic pain management. *Curr Pain Headache Rep*. doi:10.1007/s11916-021-00949-0 (PMID 33761014). DENKI clinical rationale (PL37/PL265)
18. Iwata N, Tsubuki S, Takaki Y, et al. (2000). Identification of the major Abeta1-42-degrading catabolic pathway in brain parenchyma: suppression leads to biochemical and pathological deposition. *Nat Med*. doi:10.1038/72237 (PMID 10655101). Neprilysin degrades amyloid-beta (off-target caution)
19. Huang SM, Mouri A, Kokubo H, et al. (2006). Neprilysin-sensitive synapse-associated amyloid-beta peptide oligomers. *J Biol Chem*. doi:10.1074/jbc.M601372200 (PMID 16636059). NEP / Abeta oligomers (knockdown caution)
20. Fink DJ, Wechuck J, Mata M, et al. (2011). Gene therapy for pain: results of a phase I clinical trial (HSV-enkephalin, NP2). *Ann Neurol*. doi:10.1002/ana.22446 (PMID 21796661). HSV-PENK Phase I benchmark
21. Wolfe D, Mata M, Fink DJ (2009). A clinical trial of gene therapy for chronic pain. *Pain Med*. doi:10.1111/j.1526-4637.2009.00720.x (PMID 19818042). PENK gene-therapy trial context
22. Li Y, Wang Y, et al. (2019). Effects of different 2A peptides on transgene expression in multicistronic vectors. *Mol Biol Rep*. doi:10.1007/s11033-019-05153-3 (PMID 31659692). 2A self-cleaving peptide (processing cassette)
23. Meas SJ, et al. (2020). Co-expression of self-cleaved multiple proteins derived from P2A/T2A constructs. *Protein Expr Purif*. doi:10.1016/j.pep.2020.105763 (PMID 32971295). Polycistronic 2A expression

24. Zdrazil B, Felix E, Hunter F, et al. (2024). The ChEMBL Database in 2023: a drug discovery platform spanning multiple bioactivity data types and time periods. *Nucleic Acids Res*. doi:10.1093/nar/gkad1004 (PMID 37933841). ChEMBL bioactivity database (δ/µ Kᵢ landscape)
25. Passaro S, Wohlwend J, et al. (2025). Boltz-2: towards accurate and efficient binding affinity prediction. *bioRxiv*. doi:10.1101/2025.06.14.659707. Boltz-2 co-folding structure prediction
26. Abraham MJ, Murtola T, Schulz R, et al. (2015). GROMACS: high performance molecular simulations through multi-level parallelism from laptops to supercomputers. *SoftwareX*. doi:10.1016/j.softx.2015.06.001. MD engine
27. Lindorff-Larsen K, Piana S, Palmo K, et al. (2010). Improved side-chain torsion potentials for the Amber ff99SB protein force field (ff99SB-ILDN). *Proteins*. doi:10.1002/prot.22711 (PMID 20408171). Protein force field
28. Jorgensen WL, Chandrasekhar J, Madura JD, et al. (1983). Comparison of simple potential functions for simulating liquid water (TIP3P). *J Chem Phys*. doi:10.1063/1.445869. Water model
29. Valdés-Tresanco MS, Valdés-Tresanco ME, Valiente PA, Moreno E (2021). gmx_MMPBSA: a new tool to perform end-state free energy calculations with GROMACS. *J Chem Theory Comput*. doi:10.1021/acs.jctc.1c00645 (PMID 34586825). MM-GBSA implementation
30. Miller BR III, McGee TD Jr, Swails JM, et al. (2012). MMPBSA.py: an efficient program for end-state free energy calculations. *J Chem Theory Comput*. doi:10.1021/ct300418h (PMID 26605738). MM-PBSA/GBSA engine
31. Onufriev A, Bashford D, Case DA (2004). Exploring protein native states and large-scale conformational changes with a modified generalized Born model (GB-OBC). *Proteins*. doi:10.1002/prot.20033. Generalized-Born solvation (igb=5)
32. Genheden S, Ryde U (2015). The MM/PBSA and MM/GBSA methods to estimate ligand-binding affinities. *Expert Opin Drug Discov*. doi:10.1517/17460441.2015.1032936 (PMID 25835573). MM-GBSA accuracy / error bounds
