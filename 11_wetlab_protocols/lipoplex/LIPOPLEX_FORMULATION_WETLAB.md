# Lipoplex / LNP formulation specification: wet lab

**For:** co-delivery of the engineered PENK therapy plasmid (6,217 bp) and the
anti-*MME* (neprilysin) siRNA duplex (21-mer + 21-mer, 2-nt 3′ overhangs).
**Date:** 2026-08-06. **Status:** design specification, not yet validated in-house.

---

## 0. Read this first: what the modelling does and does not support

Our coarse-grained MD (MARTINI 2, 200 ns × 3 seeds per arm) established **one
comparative result**: the ionizable lipid's protonation state controls DNA
binding in the direction the delivery design assumes.

| Arm | DNA–lipid contacts | Min DNA–lipid distance (nm) | RDF peak *g(r)* |
|---|---:|---:|---:|
| DOTAP (permanent +) | 24.7 ± 5.5 | 0.460 ± 0.003 | 1.54 ± 0.12 |
| MC3-H⁺ (endosomal pH) | 34.4 ± 8.6 | 0.469 ± 0.013 | 1.57 ± 0.31 |
| MC3⁰ (physiological pH) | 8.1 ± 4.9 | 1.270 ± 0.563 | 1.04 ± 0.09 |

mean ± SEM, n = 3 velocity seeds, metrics from the equilibrated 100–200 ns window.

**Three limits you must not read past:**

1. **The lipid topologies are analogy models.** MC3 was represented by a
   surrogate MARTINI topology, not a validated parameterisation. The
   protonated-vs-neutral *contrast* is trustworthy; the absolute numbers are not.
2. **The simulation contains no PEG-lipid.** Composition was cationic 120 :
   DOPE 80 : cholesterol 40 (50 : 33.3 : 16.7 mol%). Real formulations need a
   PEG-lipid for size control and colloidal stability, so the compositions
   below **deliberately differ** from what was simulated. This is stated rather
   than hidden.
3. **Nothing here predicts transfection efficiency.** Charge ratio must be
   titrated empirically (§4). The MD narrows the design space; it does not
   pick the winner.

---

## 1. Components to order

| Component | MW (g/mol) | Charge | Role |
|---|---:|---:|---|
| DOTAP (chloride salt) | 698.54 | +1 (permanent) | cationic lipid, formulation A |
| DLin-MC3-DMA | 642.09 | ionizable, p*K*ₐ ≈ 6.4 | ionizable lipid, formulations B1/B2 |
| DOPE | 744.03 | 0 | fusogenic helper: cone geometry drives endosomal escape |
| DSPC | 790.15 | 0 | saturated structural helper (clinical LNP) |
| Cholesterol | 386.65 | 0 | membrane rigidity, stability |
| DMG-PEG2000 | 2509.2 | 0 | steric stabiliser: controls particle size, blocks aggregation |

Stocks: dissolve each lipid in absolute ethanol. Store at −20 °C under argon,
protect from light; DOPE and DLin-MC3-DMA are oxidation-sensitive.

---

## 2. The three compositions

### A: DOTAP/DOPE/cholesterol lipoplex (matches what we simulated)
**50 : 33.3 : 16.7 mol%, DOTAP : DOPE : cholesterol**

The direct experimental counterpart of the MD system. Simple hydration +
mixing, no special equipment. Use this as the **positive control for
constitutive binding**: it condenses cargo at all pH, so it validates the
assay before you test pH-responsiveness. DOTAP/DOPE is a long-established
transfection pair and the DOTAP:DOPE ratio is itself cell-type dependent, so
treat 1:0.67 as a starting point.

### B1: MC3 / DOPE / cholesterol / PEG (MD-matched + PEG)
**49.25 : 32.8 : 16.45 : 1.5 mol%, DLin-MC3-DMA : DOPE : cholesterol : DMG-PEG2000**

Keeps the simulated helper lipid and molar proportions, adds the minimum
PEG-lipid needed for a defined particle. This is the **bridge** between the
simulation and a real formulation: the arm whose behaviour our MD most
directly speaks to.

### B2: MC3 clinical benchmark
**50 : 10 : 38.5 : 1.5 mol%, DLin-MC3-DMA : DSPC : cholesterol : DMG-PEG2000**

The standard four-component ionizable-lipid ratio used for the approved
siRNA-LNP product. Include it as the **externally-anchored reference**: if B1
underperforms B2, the problem is our composition, not our cargo or our hands.

> **Why both B1 and B2.** B1 is what we modelled; B2 is what the field has
> validated. Running only B1 leaves an underperformance uninterpretable:
> composition or cargo? Running both separates those.

---

## 3. Charge-ratio arithmetic (so you can rescale freely)

Nucleic acid carries **one negative charge per nucleotide**, MW ≈ 330 g/mol
per nucleotide, so:

**1 µg nucleic acid = 3.03 nmol phosphate = 3.03 nmol negative charge.**

This holds for the plasmid and the siRNA alike: per microgram they are
charge-equivalent, which is why the two cargoes can be pooled and treated as
one phosphate total.

Cationic/ionizable lipid needed:

```
nmol cationic lipid  =  ratio × 3.03 × (µg total nucleic acid)
nmol total lipid     =  nmol cationic lipid ÷ (mol fraction of cationic lipid)
```

Note the convention difference: **lipoplexes** are specified by charge ratio
(±), **LNPs** by N/P (ionizable nitrogen : phosphate). For a monovalent lipid
these are numerically the same; ranges differ by convention: lipoplex work
typically scans ±2–4, LNPs use N/P ≈ 6.

### Per 100 µg total nucleic acid

| Formulation | Ratio | Cationic (µg) | Helper (µg) | Chol (µg) | PEG (µg) | Total lipid | Lipid:NA (w/w) |
|---|---|---:|---:|---:|---:|---:|---:|
| A: DOTAP | ± 3 | 635.0 | 450.5 (DOPE) | 117.4 | N/A | 1202.9 µg | 12.0 : 1 |
| B1: MC3+DOPE | N/P 6 | 1167.4 | 900.9 (DOPE) | 234.8 | 139.0 | 2442.1 µg | 24.4 : 1 |
| B2: MC3 clinical | N/P 6 | 1167.4 | 287.3 (DSPC) | 541.3 | 136.9 | 2132.9 µg | 21.3 : 1 |

---

## 4. Titration series: do this first, it is not optional

Total lipid scales strictly linearly with charge ratio. Per **1 µg** nucleic acid:

| ratio (±  or N/P) | A (µg) | B1 (µg) | B2 (µg) |
|---:|---:|---:|---:|
| 1 | 4.01 | 4.07 | 3.55 |
| 2 | 8.02 | 8.14 | 7.11 |
| 3 | 12.03 | 12.21 | 10.66 |
| 4 | 16.04 | 16.28 | 14.22 |
| 6 | 24.06 | 24.42 | 21.33 |
| 8 | 32.08 | 32.56 | 28.44 |
| 10 | 40.10 | 40.70 | 35.55 |
| 12 | 48.12 | 48.84 | 42.66 |

**Screen A at ± 1, 2, 3, 4, 6 and B1/B2 at N/P 3, 4, 6, 8.** Charge ratio is
the single most influential variable and it is cell-line dependent, the
optimum cannot be transferred from another lab's paper, and our MD does not
predict it.

---

## 5. Co-delivery dose: 24-well, 500 µL

Two cargoes, dosed on different logic: the plasmid on a per-well mass basis,
the siRNA on final concentration.

| Cargo | Dose | Copies/well | Basis |
|---|---|---:|---|
| PENK plasmid | 0.50 µg | 7.3 × 10¹⁰ | standard 24-well plasmid dose |
| anti-*MME* siRNA | 12.5 pmol = 0.173 µg | 7.5 × 10¹² | 25 nM final in 500 µL |
| **Total nucleic acid** | **0.673 µg** | N/A | **2.04 nmol phosphate** |

Mass ratio plasmid:siRNA = 2.9 : 1. Copy ratio siRNA:plasmid ≈ 103 : 1, the
siRNA is in large molar excess despite the smaller mass, which is what you
want: catalytic knockdown needs many guide copies, the plasmid needs few.

Lipid per well at the ratios in §3:

| Formulation | Cationic | Helper | Chol | PEG | **Total** |
|---|---:|---:|---:|---:|---:|
| A (± 3) | 4.275 µg | 3.033 µg | 0.790 µg | N/A | **8.10 µg** |
| B1 (N/P 6) | 7.860 µg | 6.066 µg | 1.581 µg | 0.936 µg | **16.44 µg** |
| B2 (N/P 6) | 7.860 µg | 1.934 µg | 3.644 µg | 0.921 µg | **14.36 µg** |

**Also run single-cargo arms** (plasmid-only, siRNA-only) at matched lipid.
Co-formulation could impair either cargo, and without the single arms you
cannot tell which.

---

## 6. Assembly

**Formulation A (lipoplex): no equipment beyond a bench.**

1. Dry the lipid mix from ethanol under N₂, hydrate in 20 mM HEPES pH 7.4 to
   1 mM total lipid, vortex, then extrude 11× through 100 nm polycarbonate.
2. Dilute cargo in the same buffer at equal volume.
3. Add lipid to nucleic acid (this order, not the reverse), pipette-mix once,
   stand 20–30 min at room temperature. **Do not vortex after mixing**,
   shear breaks the complexes.

**Formulations B1/B2 (LNP): requires rapid mixing.**

1. Lipids in ethanol at 12.5 mM total.
2. Cargo in **25 mM acetate buffer, pH 4.0**: the low pH protonates MC3 so it
   can bind cargo during assembly. This is the step our MD is about.
3. Rapid-mix 1 volume ethanol : 3 volumes aqueous (microfluidic cartridge, or
   T-junction at matched flow ratio).
4. **Immediately** dialyse or buffer-exchange into PBS pH 7.4 (≥ 20 volumes).
   This raises the pH, MC3 deprotonates, and the particle surface turns neutral
   ; the circulation-competent state. Our MC3⁰ arm is the model of this state.

---

## 7. QC before any cell work

| Measurement | Method | Accept |
|---|---|---|
| Hydrodynamic diameter | DLS | 70–150 nm |
| Polydispersity | DLS | PDI ≤ 0.2 |
| Zeta potential | ELS | A: strongly positive; B at pH 7.4: near-neutral (−10 to +10 mV) |
| Encapsulation efficiency | RiboGreen / PicoGreen ± Triton | ≥ 80 % for B1/B2 |
| Cargo integrity | 0.8 % agarose, post-release | plasmid supercoiled band intact |
| pH-responsiveness | zeta at pH 7.4 vs pH 5.0 | B1/B2 shift positive at pH 5.0 |

**The last row is the experimental test of our MD prediction.** If the zeta
potential does not become more positive at endosomal pH, the mechanism the
formulation depends on is not operating: stop and diagnose before running
transfections.

---

## 8. References

Molar compositions and ratio conventions below are drawn from the published
literature; the per-component masses in §3–§5 were computed for this project's
specific cargo and are ours.

1. **Jayaraman M. et al.** (2012) *Angew Chem Int Ed* 51:8529; DLin-MC3-DMA
   discovery and optimisation; the p*K*ₐ ≈ 6.4 design principle.
2. **Akinc A. et al.** (2019) *Nat Nanotechnol* 14:1084; development of the
   approved MC3-based siRNA-LNP; the 50 : 10 : 38.5 : 1.5 composition (B2).
3. **Felgner P.L. et al.** (1987) *PNAS* 84:7413; original cationic
   lipid–DNA lipoplex transfection.
4. **Zuhorn I.S. et al.** (2002); DOTAP/DOPE ratio and cell type jointly
   determine transfection efficiency; basis for treating A's ratio as a
   starting point, not a fixed value.
5. **Marrink S.J. et al.** (2007) *J Phys Chem B* 111:7812; MARTINI CG force
   field used for the simulations in §0.
6. **Kulkarni J.A. et al.** (2018) *Nanoscale* 10:9023; LNP assembly by rapid
   ethanol–aqueous mixing at acidic pH followed by neutral-pH exchange (§6).

*Reference list to be completed with DOIs at manuscript stage; the composition
numbers used above are the ones stated in these sources.*

---

## 9. Decision this sheet does not make

Which formulation goes forward. That depends on the §4 titration and the §7
pH-responsiveness result, both of which are bench measurements. The modelling
says only that an ionizable lipid **can** deliver the pH switch the design
assumes, and that a permanent cation like DOTAP cannot, since it binds cargo
identically at both pH values.
