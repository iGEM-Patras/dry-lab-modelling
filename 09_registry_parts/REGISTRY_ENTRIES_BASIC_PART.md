# Registry documentation entries, basic part

**Three separate entries, matching the form's Type selector. Paste each into its own
submission. Markdown only, no HTML, no tables with merged cells.**

Entries to create: **Design**, **Discussion**, and later **Characterisation**.
Do **not** create Characterisation yet. Reasons in the last section.

---
---

# ENTRY 1 of 2 — Type: **Design**

**Title:** `Engineered proenkephalin: recoding seven payload cassettes while keeping native processing`

**Affiliation:** Patras UPAT (2026)

---

## The problem this part addresses

Chronic pain is managed largely with systemic opioids that act everywhere in the body,
producing tolerance, dependence and respiratory depression. The endogenous opioid system
solves this differently: enkephalins are released locally, act briefly, and are degraded
within seconds. Our aim is a part that raises local enkephalin tone rather than flooding the
system.

## Why a precursor rather than a peptide

Enkephalins cannot be expressed directly. The native route is a **precursor protein**,
preproenkephalin, carrying several copies of the payload separated by dibasic recognition
sites. Proprotein convertases cut at those sites inside secretory granules, liberating the
mature peptides at the point of release.

We kept that architecture exactly and changed only the payload identity.

## What was changed, and what was deliberately not

**Changed.** All seven enkephalin cores are recoded from the native `YGGFM` / `YGGFL` to
`YGGFEVVG`, which carries the deltorphin C-terminal address on the enkephalin message. The
intent is a shift toward delta-opioid receptor preference, since delta agonism is associated
with analgesia carrying less respiratory risk than mu.

**Deliberately not changed:**

- the native signal peptide, residues 1 to 24
- all **12 dibasic processing sites**, at native spacing
- the cysteine positions and overall precursor length

Keeping the scaffold means the host's own convertases do the processing. No engineered
release mechanism is required, and the part behaves as a drop-in replacement for the native
precursor in any cell type that already processes it.

## Sequence facts

Computed from the submitted sequence, not from a design file.

- length **867 bp**, 289 codons
- product **288 aa**
- **7 copies** of `YGGFEVVG`
- GC content **59.2 %**
- C-terminal product `YGGFEVVGRF`, a decapeptide, matching the native heptapeptide
  architecture where the terminal cassette carries a C-terminal extension

## Assembly standard compliance

The submitted sequence is clean for **RFC10** (EcoRI, XbaI, SpeI, PstI, NotI) and
**RFC1000** (BsaI, SapI), scanned on **both strands**.

Reaching that took **8 synonymous single-base changes**. The encoded protein is identical
before and after, and all seven payload cassettes are intact.

We deliberately widened the enzyme panel beyond what either standard requires, so the part
is usable by teams working in other assembly systems. That surfaced additional sites,
including some nested inside longer recognition motifs that a check for the longer motif
alone would have missed, and some on the reverse strand that reading forward would not have
caught.

## Relationship to our composite part

Our composite part contains this basic part **verbatim**, beginning at nucleotide 7
immediately after the Kozak sequence:

```
composite (2164 bp) = Kozak (6) + THIS BASIC PART (867) + IRES (574) + mEGFP (717)
```

Anyone can verify that with a single substring search. The two submissions are one coherent
pair.

---
---

# ENTRY 2 of 2 — Type: **Discussion**

**Title:** `What we can and cannot claim for the engineered proenkephalin payload`

**Affiliation:** Patras UPAT (2026)

---

## The headline limitation

**Delta-receptor preference is a design goal, not a demonstrated result.**

Our selectivity model, calibrated against **13 published reference opioids**
(r = 0.805, p = 0.0009, correct sign on 12 of 13), estimates the released peptide at
**+1.23 +/- 1.76 kcal/mol** delta-over-mu.

**That interval includes zero.** The payload is not statistically separable from native
Met-enkephalin on this measure. We report it because the calibration is honest and the
method is documented, not because it supports a selectivity claim.

A free-energy calculation run later gave a mu-preferring estimate and then failed its own
reproducibility gate, with two replicates disagreeing by far more than their combined error.
We treat that calculation as uninformative rather than as evidence in either direction.

## Can the payload actually be released?

This is the question that matters most for a precursor part, and we tested it.

We predicted structures of both the engineered precursor and native preproenkephalin and
measured solvent accessibility at all 12 dibasic processing sites. Across the 12
corresponding sites, mean relative accessibility was **0.411 native versus 0.343 engineered,
difference 0.068, p = 0.160**. No evidence that recoding systematically buries the
processing sites.

**We are reporting that as a weak negative and nothing more.** The predicted structures had
mean pLDDT of 43 and 37, below the threshold at which per-residue burial is interpretable,
and in the native control the site-to-site variation was *smaller* than the scatter between
repeated predictions of the same sequence. Three engineered sites appeared less accessible,
but that apparent signal does not survive the variance check, so we are not reporting those
sites as flagged.

**The bench settles this directly.** LC-MS/MS on transfection supernatant shows which
cassettes were cleaved, with no modelling assumption.

## Immunogenicity

Predicted MHC class I binding for the engineered epitope versus the native one it replaces,
across **6,120 allele-peptide pairs**: **1.86 % strong binders versus 1.77 %**. The
engineered payload is not meaningfully more immunogenic than the sequence it replaces.

This is a screen, not a clearance. Class I prediction speaks to CD8 recognition of an
intracellular product and says nothing about antibody responses to a secreted peptide.

## Safety context

Delta-opioid agonism carries a literature-reported seizure liability. We reviewed 12
references and found this does **not** hold as a class claim. The closest precedent, a viral
vector expressing *native* preproenkephalin, completed Phase 1 in the same indication with
published safety data.

Two gaps remain and we state them rather than omit them:

1. that precedent expressed the **native** precursor, where this part is engineered
2. it was delivered **peripherally**, where our intended route is intranasal

## The honest correspondence caveat

**This part is a designed sequence and has not been characterised at the bench.**

The DNA in our freezer is the His-tagged, differently codon-optimised construct. This part
is that construct's coding sequence minus the purification tag. When bench characterisation
arrives it will support this part by **close correspondence rather than identity**, and we
would rather state that than have a reader discover it.

## What would change our claims

- **Functional cAMP assay at both receptors** with selective antagonists. This is the only
  instrument that measures the quantity our selectivity claim is about, and it settles in
  one experiment what no computation here has settled.
- **LC-MS/MS of the supernatant** for processing and the actual C-terminus.
- **Quantitative expression yield**, which also unblocks our intranasal dose model.

---
---

# Why no Characterisation entry yet

The form offers Characterisation for *"quantitative or qualitative data on how the part
behaves under particular conditions."* Everything we have is **predicted**, not measured.

Filing modelling output under Characterisation would read as overclaiming to any judge who
looks closely, and it is the single easiest thing for them to catch. The modelling belongs
in Design (why we built it this way) and Discussion (what it does and does not support).

**Create the Characterisation entry when the transfection returns**, and put the cAMP and
LC-MS/MS data in it.

# Mechanical notes for the form

- **Markdown only.** No HTML tags; the editor rejects them.
- Images go in via the **Insert Image** button, not a Markdown image link to an external URL.
- If any dataset is large, upload to **Zenodo** and cite the DOI in the entry.
- Everything defaults to **CC-BY-4.0**.
- Affiliation is **Patras UPAT (2026)** on both entries.
