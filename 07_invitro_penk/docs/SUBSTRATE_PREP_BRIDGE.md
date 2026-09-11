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
C-terminus** of the engPENK product after ribosome skipping: 22 extra residues,
`ATNFSLLKQAGDVEENPGP` preceded by the last cassette.

**That tail contains no dibasic site.** PC1/3 and PC2 cut at KR/RR/KK; the tail has none.
Consequence: **the terminal cassette of this construct cannot be released as a free
peptide.** It will stay fused to 22 residues of P2A through the entire digest.

This affects **1 of 7 cassettes in 1 of 4 constructs** — the other six cassettes in that
construct are internal and release normally. It is not fatal, but it means:

- Expect a **~2.5 kDa C-terminal species** in this construct's digest that the other
  three do not produce (`YGGFEVVGRF` + P2A tail).
- For maximum free-peptide yield, the three **payload-downstream** constructs
  (`mEGFP_P2A_His_PENK`, and both IRES constructs) are the better substrates.
- The tail is a useful **internal negative control**: a species that should *not* be
  cleaved, in the same tube as species that should.

This was not caught earlier because the cistron-order panel was designed for expression
comparison, not for digest yield.

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

## 6. What this does not resolve

- **Yield is unknown.** Nothing here predicts how much protein comes off the column;
  that is what the transfection will tell you. If yield is low, the IRES constructs
  are the expected culprits (second-cistron efficiency).
- **The aggregation risk is calculated, not measured.** \|z\|/kDa is a heuristic. A
  dynamic light scattering read or a simple post-exchange spin-and-A280 (§4 step 5)
  settles it empirically in one afternoon.
- **Whether the His tag interferes with processing is untested.** It sits at the
  N-terminus, upstream of the first cassette, and the nearest dibasic is ~75 residues
  away, so interference is unlikely — but it is an assumption, not a result.
- **Disulfide state of the secreted protein is unknown.** Six Cys in a secreted protein
  passing through the ER will likely be oxidised; this has not been checked and affects
  only how accessible the N-terminal region is.

---

## 7. Files

- `tables/substrate_properties.csv` — per-construct mass, pI, charge, A280, C-terminal end
- `tables/purification_plan.csv` — the four buffer steps with rationale
- `tables/enzyme_compatibility_matrix.csv` — full pairwise co-incubation matrix
- `substrate_prep_bridge.png` — charge-vs-pH curve and enzyme staging

**Data sources.** Sequences: the ordered v6 FASTA files in
`06_engineering_cycles/cycle4_synthesizability/data/`. Mass, pI, ε₂₈₀: Biopython
`ProtParam` on the translated mature chain. Enzyme requirements: `enzyme_conditions.csv`
in this directory (Yoon 2022, UniProt P29120/P16519/P05408/P07711/P16870/P19021/P09958).
Net-charge curve: Henderson–Hasselbalch over standard side-chain pKa values — a model,
not a measurement.
