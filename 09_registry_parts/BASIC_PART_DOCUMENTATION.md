# Basic Part documentation: engineered proenkephalin coding sequence

**Ready to paste into the iGEM Registry part page. 867 bp, accepted.**
Everything below is computed from the submitted sequence, not from a design file.

---

## Short description (one line, for the part header)

Engineered human proenkephalin coding sequence in which all seven enkephalin cores are
recoded to the delta-preferring octapeptide `YGGFEVVG`.

---

## Sequence facts

| | |
|---|---|
| length | **867 bp**, 289 codons |
| product | **288 aa** preproenkephalin variant |
| payload copies | **7 x `YGGFEVVG`** |
| GC content | 59.2 % |
| native signal peptide | retained, residues 1-24 (`MARFLTLCTWLLLLGPGLLATVRA`) |
| processing sites | **12 dibasic sites** preserved at native spacing |
| C-terminal product | `YGGFEVVGRF` (decapeptide), matching native heptapeptide architecture |

**Assembly standards.** Clean for **RFC10** (EcoRI, XbaI, SpeI, PstI, NotI) and **RFC1000**
(BsaI, SapI) on **both strands**, after 8 synonymous single-base changes. The encoded
protein is byte-identical to the pre-fix sequence and all 7 payload cassettes are intact.
The enzyme panel was deliberately widened beyond what either standard requires, so the part
is usable by teams working in other assembly systems.

---

## Design rationale

The native human preproenkephalin precursor carries six copies of Met-enkephalin
(`YGGFM`) and one of Leu-enkephalin, released by proprotein convertases at dibasic sites.
This part keeps that architecture exactly and changes only the payload identity: every core
becomes `YGGFEVVG`, which carries the deltorphin C-terminal address (`FEVVG`) on the
enkephalin message.

Keeping the native scaffold is the point. The signal peptide, the dibasic spacing, the
cysteine positions and the precursor length are all unchanged, so the part is processed by
the host's own machinery rather than requiring an engineered release mechanism.

---

## Characterisation status, stated honestly

**This is a designed sequence and has not yet been characterised at the bench.**

What exists:

| | |
|---|---|
| sequence verified by alignment before synthesis | yes |
| assembly-standard compliance, both strands | yes, computed |
| MHC-I immunogenicity screen | yes: **1.86 %** strong binders for the engineered epitope vs **1.77 %** for the native one it replaces, across 6,120 allele-peptide pairs |
| modelled selectivity of the released peptide | **+1.23 +/- 1.76 kcal/mol** delta-over-mu, from a model calibrated against 13 published reference opioids (r = 0.805, p = 0.0009, signs correct on 12 of 13) |
| wet-lab expression, processing, potency | **pending** |

**The interval on the selectivity estimate includes zero.** Delta-preference is a design
goal, not a demonstrated result, and the part page should say exactly that.

**One thing a judge will notice if we do not say it first:** the DNA in our freezer is the
His-tagged, differently codon-optimised construct. This part is that construct's coding
sequence minus the purification tag. Bench characterisation will therefore support this part
by close correspondence rather than by identity. Stating this is much better than having it
found.

---

## Relationship to our composite part

The composite part **contains this basic part verbatim**, beginning at nt 7 of the
composite (immediately after the Kozak sequence). Anyone can verify the relationship with a
single substring search. The two submissions are one coherent pair, not two unrelated
entries:

```
composite (2,164 bp) = Kozak (6) + THIS BASIC PART (867) + IRES (574) + mEGFP (717)
```

---

## Safety notes for the part page

- The product is a **peptide agonist precursor**, not an enzyme or a toxin.
- Delta-opioid agonism carries a literature-reported seizure liability. Our assessment of 12
  references found this does **not** hold as a class claim, and the closest precedent, a
  vector expressing *native* preproenkephalin, completed Phase 1 in the same indication with
  published safety data. Two gaps remain and belong on the page: that precedent expressed
  the native precursor where this part is engineered, and it was delivered peripherally
  where our route is intranasal.
- MHC-I prediction is a screen, not a clearance, and speaks only to CD8 recognition of an
  intracellular product.

---

## What still needs filling in on the Registry page

1. The part number, once assigned.
2. A sequence feature map (signal peptide, 7 cassettes, 12 dibasic sites) as an image.
3. Wet-lab characterisation, when the transfection returns.
