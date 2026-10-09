# PENK Project: Wet-Lab Decision Sheet

**iGEM Patras · from the dry-lab modelling team** · one page, four decisions

---

## 1 · Which plasmid to use → **Plasmid 3 (PENK-IRES-mEGFP)**

| Use | Avoid | Why |
|---|---|---|
| **Plasmid 3**: cleanest | **Plasmid 1**: defective | Plasmid 3 has PENK cap-driven, full-length, signal peptide intact, byte-identical to reference. Plasmid 1 is missing the 7th enkephalin core (YGGFMRF truncated). |

- **Plasmid 2** works but PENK sits behind P2A → loses its start Met, gains a proline → may impair secretion. Fine as backup, not first choice.
- **Plasmid 4** is OK (gene order correct); second choice after 3.

> ⚠️ **The plasmid-1 defect is invisible on a gel.** It is a point truncation. Only **Sanger sequencing of the PENK 3′ end** catches it. Do not clear plasmid 1 on gel QC alone.

---

## 2 · Before you transfect → **run the 2-digest QC gel**

| Digest | Enzymes | What it tells you |
|---|---|---|
| **A: insert release** | AflII + XbaI | Linker type: **~2.16 kb band = IRES**, **~1.63 kb = P2A**. Constant 5,345 bp backbone = loading control. |
| **B: identity fingerprint** | NcoI (5 cuts) | Gene order: read the **second-largest band** (see gel figure). |

- Run both per prep against a **1 kb Plus ladder**. Match to the virtual gel in the protocol.
- Full recipe + band table: `restriction_qc_protocol.md`, `restriction_qc_gel.png`.
- **Then Sanger-sequence** the PENK ORF (mandatory for plasmid 1; recommended for all).

---

## 3 · Order these siRNAs (NEP / MME knockdown arm)

All target the CDS shared by **all four MME variants** → one duplex silences every isoform. Standard **3′ dTdT** overhangs; order as annealed duplexes.

| Priority | Name | Guide / antisense (5'→3') |
|---|---|---|
| **1st choice** | si-MME-3 (CDS1224) | `AUAGUUUGCACAACGUCUCdTdT` |
| 2nd | si-MME-4 (CDS1590) | `UAUCCACUCAUCUUUGUCCdTdT` |
| 3rd | si-MME-2 (CDS1032) | `UUCUGGAGCAUAAACAACCdTdT` |
| 4th | si-MME-1 (CDS759) | `UUCCUGACGAAUCAAUCUGdTdT` |

- **Validate ≥2** by qPCR of MME at 48 h (expect ≥70% knockdown) + a NEP-activity or CD10 Western.
- Always include a **non-targeting scrambled control**.
- Priority order reflects added accessibility scoring (`sirna_design_v2.md`); si-MME-3 has perfect specificity + open target site.

---

## 4 · How to deliver → **co-formulate siRNA + plasmid in ONE lipoplex**

- **Do not deliver them separately.** NEP is degraded extracellularly but silencing is cell-autonomous, the enkephalin-producing cells and the NEP-silenced cells must be the **same** cells. Co-package both nucleic acids in the same lipoplex, same locus.
- **Lipid choice:** an **ionizable lipid (MC3-type)** is preferred over permanent-cation (DOTAP), the MD shows it binds DNA at endosomal pH but releases at physiological pH (needed for circulation + endosomal escape). DOTAP binds constitutively (harder to release).
- **Where:** local/regional delivery, **intranasal (nose-to-brain)** is the primary target. *(Superseded: earlier versions of this handout said intrathecal/spinal dorsal horn.)* Lipoplexes do not cross the blood–brain barrier.

---

### One-line summary
**Use plasmid 3, QC it by 2-digest gel + Sanger, order si-MME-3 (+ one more), and co-formulate siRNA + plasmid in an ionizable-lipid lipoplex delivered **intranasally**.**

*Full rationale, methods, and caveats: consolidated project brief (`project_brief.pdf`).*
