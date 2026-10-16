# Registry parts

Sequences and documentation submitted to the iGEM Registry for project *Epione*.

## Contents

| file | what it is |
|---|---|
| `engPENK_basic_RFC_clean.fasta` | basic part, 867 bp. Engineered proenkephalin coding sequence, all seven opioid cassettes recoded to the payload motif |
| `engPENK_composite_RFC_clean.fasta` | composite part, 2,164 bp. The basic part plus Kozak, EMCV IRES and mEGFP |
| `composite_components.csv` | component table for the composite, with coordinates |
| `rfc_fixes.csv` | the eight synonymous single-base changes that cleared assembly-standard sites, with the codon before and after |
| `REGISTRY_DESIGN_ENTRY.md` | **the basic part entry to paste.** A single Design-type submission |
| `REGISTRY_COMPOSITE_ENTRY.md` | **the composite part entry to paste.** Also Design type |
| `REGISTRY_PARTS.md` | sequence provenance and the assembly-standard scan |
| `REGISTRY_ENTRIES_BASIC_PART.md` | superseded two-entry draft, retained for the record. Do not use |

## Relationship between the two parts

The composite contains the basic part **verbatim**, beginning at nucleotide 7. A reader can
verify this with a single substring search, and the two submissions are intended to be read
as one pair rather than as unrelated entries.

## Standards

Both sequences were scanned on **both strands** against RFC10 (EcoRI, XbaI, SpeI, PstI,
NotI) and RFC1000 (BsaI, SapI), and against a wider Type IIS panel beyond what the standards
require. The basic part needed eight synonymous changes; the translated protein is
byte-identical before and after. The composite required none.

The EMCV IRES carries internal sites that were deliberately **not** recoded: its function
depends on RNA secondary structure rather than a reading frame, so no synonymous change
exists there. None of those enzymes is forbidden by either standard.

## Characterisation status

**Neither part has bench characterisation data.** The engineered sequence was ordered as a
linear gene fragment rather than a complete plasmid, because full plasmid synthesis would not
have returned within the season, and it entered no expression, purification or maturation
experiment. The DNA held by the wet lab is the His-tagged, differently codon-optimised
construct, so any future characterisation supports these parts by close correspondence rather
than identity.
