# Native PENK plasmids: one of the four is missing a payload

**17 Oct 2026.** Audit of the four as-received native proenkephalin plasmids, run while
extracting a coding sequence for the native Registry part. The files supplied on 17 October
are byte-identical in sequence to the copies already in `01_plasmid_audit`, confirmed by
SHA-256 on the extracted sequence of each, so this applies to both sets.

---

## The finding

**`mEGFP-IRES-PENK` encodes a proenkephalin that has lost its terminal
Met-enkephalin-Arg-Phe.** The other three constructs carry it intact.

| construct | PENK length | Met cores | terminal YGGFMRF |
|---|---|---|---|
| mEGFP-IRES-PENK | 263 aa | 5 | **absent** |
| mEGFP-P2A-PENK | 267 aa within the fusion | 6 | intact |
| PENK-IRES-mEGFP | 267 aa | 6 | intact |
| PENK-P2A-mEGFP | 267 aa within the fusion | 6 | intact |

## What the difference is, at nucleotide level

The two IRES constructs are identical for the first 786 bp of coding sequence and then
diverge:

```
PENK-IRES-mEGFP   ATG GAA AAA AGA TAC GGA GGA TTT ATG AGA TTT TAA    M E K R Y G G F M R F *
mEGFP-IRES-PENK   ATG GAA AAA AGA TAC GGA         TTT TAA            M E K R Y G     F *
```

Twelve bases, four codons, are missing: the `GGA TTT ATG AGA` encoding Gly-Phe-Met-Arg. What
remains reads `YGF` followed immediately by a stop, where the native precursor ends
`YGGFMRF`.

The reading frame is otherwise undisturbed and the stop codon is genuine, with 4,476 bp of
plasmid downstream of it, so this is a clean deletion in the coding sequence rather than a
frameshift or a sequence that merely runs off the end of a supplied fragment. That
distinction was checked explicitly, because a truncation at the edge of a linear fragment
would have looked identical in a translation and meant nothing.

## Why it matters

Proenkephalin's carboxy terminus is itself one of the seven opioid products. The whole reason
the engineered constructs carry their purification tag at the amino terminus is that a
carboxy-terminal tag would be carried into Met-enkephalin-Arg-Phe and destroy it. In this
construct that peptide is destroyed anyway, by a deletion rather than by a tag.

So `mEGFP-IRES-PENK` expresses a precursor yielding **six** opioid peptides rather than
seven. It is still a valid expression and secretion test, and still a valid reporter control.
It is **not** a valid substrate for the maturation work if the digest is assessed by looking
for all seven products, and it is not the construct to use for any comparison of product
yield against the engineered payload.

## What was done about it

The native Registry part was derived from **`PENK-IRES-mEGFP`**, which carries the intact
267-residue precursor whose translation matches UniProt P01210 exactly. That choice was made
before this discrepancy was noticed, on the grounds that it is the orientation matching the
engineered composite, so the submitted part is unaffected.

## What we have not established

Whether the deletion arose in design, in synthesis, or in the file. Answering that needs the
vendor's own sequencing record for that construct, or Sanger sequencing across the 3' end of
the coding sequence. Either settles it in one read, and until then this is an observation
about the file rather than a confirmed property of the DNA in the freezer.
