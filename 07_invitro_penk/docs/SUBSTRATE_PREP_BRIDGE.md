# Substrate preparation — from conditioned medium to digest tube

**Status:** dry-lab derived · written while the transfection is running · not yet wet-tested

**Why this document exists.** `PENK_INVITRO_PROTOCOL.md` reconstitutes the processing
enzymes on a substrate that is *supplied*. It does not say how the substrate gets there.
Now that the constructs are ordered, the substrate will come from the lab's own
conditioned medium, and nothing in this repo covered the recovery route. This is that
missing step. Every number below is calculated from the ordered v6 sequences.

---

## 1. What you are purifying

Calculated from the v6 coding sequences, after signal-peptide removal (residues 1–24).

| Construct | mature chain | mass | pI | A280 (1 mg/mL) | C-terminal end |
|---|---|---|---|---|---|
| `mEGFP_P2A_His_PENK` | 272 aa | 30.93 kDa | 5.19 | 1.063 | …YGGFEVVGRF |
| `mEGFP_IRES_His_PENK` | 272 aa | 30.93 kDa | 5.19 | 1.063 | …YGGFEVVGRF |
| `His_PENK_IRES_mEGFP` | 272 aa | 30.93 kDa | 5.19 | 1.063 | …YGGFEVVGRF |
| `His_PENK_P2A_mEGFP` | 291 aa | 32.90 kDa | 5.10 | 1.000 | …YGGFEVVGRF**ATNFSLLKQAGDVEENPGP** |

The His6 tag sits at the **N-terminus of the mature chain** (positions 1–6, immediately
after signal-peptide cleavage, followed by a GS linker). It is solvent-exposed and is the
IMAC handle. Three further His residues occur internally in the payload — 9 in total —
which is why the tag binds tightly enough to tolerate a stringent wash.

**A280 note.** Use the tabulated A280 values, not a Bradford or BCA assay, for the
purified protein. ε₂₈₀ = 32 890 M⁻¹cm⁻¹ (reduced) from 3 Trp + 11 Tyr.

---

## 2. Finding #1 — the engPENK-first P2A construct carries a dead tail

In `His_PENK_P2A_mEGFP`, engPENK is cistron 1, so the P2A peptide stays **fused to the
C-terminus** of the engPENK product after ribosome skipping: **19 extra residues**,
`ATNFSLLKQAGDVEENPGP`, immediately after the last cassette.

**That tail contains no dibasic site.** PC1/3 and PC2 cut at KR/RR/KK; the tail has a
single K at position 8 and no dibasic. Consequence: **cassette 7 of this construct cannot
be released as a short peptide.** It stays fused to 19 residues of P2A through the digest.

### This costs zero free octapeptide — do not re-order

Cassette 7 was **never** going to yield free `YGGFEVVG`. Its C-terminal context is `RF`,
ending at the stop codon, and CPE removes only C-terminal **basic** residues — it cannot
remove Phe. Cassette 7's product is `YGGFEVVGRF` in *every* construct: an extended
species, by design. It is the engineered equivalent of native PENK's terminal
`YGGFMRF` (Met-enkephalin-Arg-Phe, MERF), itself a naturally extended end-product.

Per-cassette fate, calculated from the ordered sequences:

| Cassette | position (proprotein) | C-terminal context | product |
|---|---|---|---|
| 1 | 100 | `KR` | **`YGGFEVVG`** free octapeptide |
| 2 | 110 | `KK` | **`YGGFEVVG`** free octapeptide |
| 3 | 142 | `KK` | **`YGGFEVVG`** free octapeptide |
| 4 | 195 | `RGL` | `YGGFEVVGRGL` extended (CPE cannot remove Leu) |
| 5 | 222 | `RR` | **`YGGFEVVG`** free octapeptide |
| 6 | 245 | `KR` | **`YGGFEVVG`** free octapeptide |
| 7 | 279 | `RF` (terminal) | `YGGFEVVGRF` extended (CPE cannot remove Phe) |

**Free-octapeptide yield is 5 of 7 cassettes, identical in all four constructs.** The five
octapeptide-yielding cassettes are all internal and unaffected by anything at the
C-terminus. The P2A tail changes one *minor extended species* into a different minor
extended species, in one of four constructs:

| Construct | cassette 7 product | length | [M+H]⁺ (monoisotopic) |
|---|---|---|---|
| the other three | `YGGFEVVGRF` | 10 aa | 1130.5629 |
| `His_PENK_P2A_mEGFP` | `YGGFEVVGRF` + P2A tail | 29 aa | 3098.5218 |

So: **nothing is lost that the experiment was measuring.** Add 3098.52 to the MS target
list for that one construct and treat it as a **free internal negative control** — a
species that should *not* be cleaved, sitting in the same tube as five that should. That
is a control the panel did not previously have.

This was not caught earlier because the cistron-order panel was designed for expression
comparison, not for digest yield — and, as it turns out, digest yield is not affected.

---

## 3. Finding #2 — the digest buffer sits on the substrate's pI

**pI = 5.19. The published digest buffer is pH 5.5.** That is 0.3 units away.

| pH | net charge z | \|z\|/kDa |
|---|---|---|
| 8.0 (IMAC bind/elute) | −17.9 | 0.58 |
| 6.0 | −9.8 | 0.32 |
| **5.5 (digest)** | **−5.8** | **0.19** |
| 5.19 (pI) | −2.6 | 0.08 |
| 5.0 | +0.0 | 0.00 |

Below roughly \|z\|/kDa ≈ 0.30 a protein has little electrostatic self-repulsion and
aggregation risk rises. At the digest pH this substrate is at **0.19** — inside that
window. It is a 31 kDa acidic protein with a disordered, highly charged payload, so it is
not a classic aggregator, but the margin is thin and the failure mode is silent: substrate
drops out of solution and the digest simply under-performs.

**Do not skip the mitigations in §4 step 4.** They cost nothing and remove the risk.

**Cannot be fixed by raising the pH.** All of PC1/3, PC2, cathepsin L and CPE have acidic
optima (pH 5.5) because they are granule enzymes. Running the digest at pH 7 to keep the
substrate happy would put every enzyme outside its optimum. The buffer is correct; the
substrate handling has to accommodate it.

---

## 4. Purification route

Standard His-tag IMAC, with the buffer choices justified rather than defaulted.

| Step | Buffer | Why |
|---|---|---|
| **1 · bind** | 50 mM NaH₂PO₄ **pH 8.0**, 300 mM NaCl, 10 mM imidazole | pH 8.0 holds the protein at z = −17.9, far from the pI. 300 mM NaCl suppresses non-specific ionic binding to the resin. 10 mM imidazole blocks weak binders. |
| **2 · wash** | same + 20–30 mM imidazole | 9 His residues total → tight binding → a stringent wash is affordable and worth it. |
| **3 · elute** | same + 250 mM imidazole | Single-step elution; no gradient needed for a His6 tag. |
| **4 · exchange** | → 50 mM Na-acetate **pH 5.5**, 5 mM CaCl₂, **100–150 mM NaCl** — spin desalt, 3–10 kDa MWCO | **This is the step that matters.** See below. |

### Step 4 in detail — the pH transition

The protein must cross its own pI to get from IMAC into digest buffer. Do it in the way
that spends least time near zero charge and lowest concentration:

1. **Exchange directly into digest buffer.** Do not elute, concentrate, and then acidify —
   that concentrates the protein *and* walks it through the pI at high concentration,
   which is the worst combination.
2. **Keep 100–150 mM NaCl in the digest buffer.** Screening ions substitute for the
   electrostatic repulsion the protein loses near its pI. The PC2 protocol already
   specifies 100 mM NaCl, so for the PC2 arm this is free; add it to the PC1/3 arm too.
3. **Stay dilute during the transition** — below ~0.5 mg/mL. Concentrate afterwards if
   the digest needs it, in the final buffer.
4. **Work at 4 °C** through the exchange; warm to 37 °C only when the enzyme goes in.
5. **Spin the substrate before adding enzyme** (10 min, 16 000 × g, 4 °C) and read A280 on
   the supernatant. If you lost material, you will see it here rather than blaming the
   enzyme later.

### Reducing agent — a decision, not a default

The mature chain has **6 cysteines, all in the N-terminal region (positions 10, 14, 17,
32, 36, 49 of the mature chain)**. This Cys-rich domain is inherited from native PENK,
not engineered.

- The **PC1/3 and PC2 arms** are published without reducing agent. Run them that way.
- The **cathepsin L arm requires 5 mM DTT** (it is a cysteine protease). That DTT will also
  reduce the substrate's own disulfides — acceptable, and possibly helpful, since a reduced
  substrate is more accessible. Just be aware the two arms present structurally different
  substrate.
- Do not add DTT "for safety" to the PC arms. It changes the substrate between arms and
  makes them non-comparable.

---

## 5. Enzyme staging — what can share a tube

Derived from the requirements already tabulated in `enzyme_conditions.csv`. Two hard
constraints: **pH** and **metal-vs-chelator**.

| Stage | Enzymes | Buffer | Notes |
|---|---|---|---|
| **1** | PC1/3 and/or PC2+7B2 | pH 5.5, 5 mM CaCl₂, 100 mM NaCl | **Can share a tube.** Both Ca²⁺-dependent, same pH. |
| **2** | CPE | pH 5.5, **no EDTA** | Zn²⁺ metalloenzyme. Can follow stage 1 directly with no exchange. |
| **3** | PAM (PHM→PAL) | pH 5.0, ascorbate + Cu²⁺ + O₂, catalase | **Buffer exchange required** (different pH, needs Cu²⁺/ascorbate). Only relevant to the Gly-terminated cassettes. |

**Cathepsin L is a parallel arm, never co-incubated with CPE or PAM.** It requires 1 mM
EDTA, which strips the Zn²⁺ that CPE needs and the Cu²⁺ that PAM needs. Run it as its own
tube from the same substrate pool.

**Furin** (pH 6.0) is the comparison arm and is also its own tube.

The full pairwise matrix is in `tables/enzyme_compatibility_matrix.csv`.

---

## 6. Steric accessibility of the seven cleavage sites — checked, passes

**Question:** the payload is intrinsically disordered by design, but is every dibasic site
actually accessible to PC1/3 and PC2, or does any of them sit buried in the one folded
domain the protein has?

**Source of the answer:** the corrected AlphaFold run already in this repo
(`04_structures/engPENK_alphafold_per_residue_plddt.csv`, 288-aa proprotein — the run
validated in `cycle3b_physics_rescoring/ALPHAFOLD_RESUBMIT_NOTE.md` after the earlier
DNA-submitted run was rejected). No new prediction was needed. AlphaFold's own
`fraction_disordered` for this model is **0.83**, pTM 0.26.

The protein has exactly two structural regions:

| Region | residues | mean pLDDT | reading |
|---|---|---|---|
| **folded anchor** | 1–77 | **84.4** | signal peptide + the Cys-rich domain (all 6 Cys) |
| **disordered payload** | 78–288 | **~30** | the seven cassettes and every dibasic site |

Per-site, over a 10-residue window centred on each scissile bond:

| Cassette | site (proprotein) | pLDDT at N-terminal dibasic | pLDDT across cassette | accessible |
|---|---|---|---|---|
| 1 | 98–99 | 26.8 | 28.2 | yes |
| 2 | 108–109 | 29.6 | 28.3 | yes |
| 3 | 140–141 | 25.9 | 24.8 | yes |
| 4 | 193–194 | 33.2 | 32.8 | yes |
| 5 | 220–221 | 34.8 | 33.7 | yes |
| 6 | 243–244 | 35.6 | 31.9 | yes |
| 7 | 277–278 | 36.3 | 25.6 | yes |

**All 7 of 7 sites are at pLDDT 26–36 — deeply disordered, far below the 50 threshold.**
Not one lies inside the folded anchor; the first dibasic site sits **21 residues past** the
anchor's C-terminal boundary. A disordered site is an extended site, which is the
conformation PC1/3 and PC2 require. There is no steric reason for any cassette to
under-cut.

**What this does and does not license.** It says no site is *occluded*. It does not predict
*rates* — pLDDT is a confidence measure, not a free energy, and cleavage kinetics depend on
sequence context and enzyme concentration, which this does not model. If a cassette
under-performs in the digest, the cause is kinetic or compositional, not steric, and the
per-site sequence context in `cleavage_predictions.csv` is where to look.

**Corollary for the His tag.** The tag sits at the mature N-terminus, i.e. at the start of
the *folded* anchor, and the nearest dibasic site is 66 residues downstream with the whole
anchor in between. Processing interference is therefore implausible. But note the pLDDT run
was done **without** the tag, so it says nothing about whether appending His6-GS perturbs
the anchor's own fold — that is a solubility/folding question, not a processing one, and it
is still open.

---

## 7. What this does not resolve

- **Yield is unknown.** Nothing here predicts how much protein comes off the column;
  that is what the transfection will tell you. If yield is low, the IRES constructs
  are the expected culprits (second-cistron efficiency).
- **The aggregation risk is calculated, not measured.** \|z\|/kDa is a heuristic. A
  dynamic light scattering read or a simple post-exchange spin-and-A280 (§4 step 5)
  settles it empirically in one afternoon.
- **Whether appending His6-GS perturbs the folded anchor is untested.** Processing
  interference is ruled out in §6; the anchor's own fold with the tag on it is not.
- **Cleavage *rates* are not predicted.** §6 rules out steric occlusion only.
- **Disulfide state of the secreted protein is unknown.** Six Cys in a secreted protein
  passing through the ER will likely be oxidised; this has not been checked and affects
  only how accessible the N-terminal region is.

---

## 8. Files

- `tables/substrate_properties.csv` — per-construct mass, pI, charge, A280, C-terminal end
- `tables/purification_plan.csv` — the four buffer steps with rationale
- `tables/enzyme_compatibility_matrix.csv` — full pairwise co-incubation matrix
- `substrate_prep_bridge.png` — charge-vs-pH curve and enzyme staging
- `tables/cassette_fate.csv` — per-cassette C-terminal context and product
- `tables/cassette_yield_accounting.csv` — free-octapeptide yield per construct
- `tables/cassette_accessibility.csv` — per-site pLDDT windows
- `cassette_accessibility.png` — pLDDT profile with cleavage sites, and cassette fate

**Data sources.** Sequences: the ordered v6 FASTA files in
`06_engineering_cycles/cycle4_synthesizability/data/`. Mass, pI, ε₂₈₀: Biopython
`ProtParam` on the translated mature chain. Enzyme requirements: `enzyme_conditions.csv`
in this directory (Yoon 2022, UniProt P29120/P16519/P05408/P07711/P16870/P19021/P09958).
Net-charge curve: Henderson–Hasselbalch over standard side-chain pKa values — a model,
not a measurement.
