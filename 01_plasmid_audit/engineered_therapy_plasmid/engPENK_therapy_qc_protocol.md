# Restriction-Digest QC — Engineered PENK Therapy Plasmid

**Construct:** `engPENK_therapy_plasmid` — engineered anionic-address PENK (7× YGGFEVVG)
cloned into the pcDNA3.1(+) backbone via **NheI/XhoI**.
**Total size:** 6,217 bp, circular.
**Backbone donor:** plasmid 4 (PENK-P2A-mEGFP) — chosen because it has single NheI and
single XhoI sites, giving a clean directional cassette swap. The native P2A–mEGFP cassette
(1,639 bp NheI→XhoI) was removed and replaced by the 885 bp engineered insert.

> **Why a new scheme?** The native-plasmid QC (Digest A = AflII + XbaI, Digest B = NcoI)
> does **not** transfer: the engineered insert carries **no AflII and no XbaI site**. The
> engineered therapy plasmid has **zero AflII sites** and its single XbaI site now sits in
> the backbone, so the native insert-release logic is gone. This scheme is purpose-built
> for the engineered construct.

## Diagnostic digests

| Digest | Enzyme(s) | Expected fragments (bp) | Purpose |
|---|---|---|---|
| **A — insert release** | NheI + XhoI | **5,338 + 879** | Confirms an insert of the correct size is present and excisable. The 879 bp band is the diagnostic signature. |
| **B — linearize** | NheI (single cutter) | 6,217 | Confirms total plasmid size / supercoil→linear. |
| **C — identity** | BglII | 5,144 + 1,073 | Two-band identity check (one BglII site in the insert at nt 192, one in the backbone). A clone with no insert loses the 1,073 bp band. |
| **D — fingerprint** | NcoI | 3,342 + 1,845 + 735 + 295 | Four-band fingerprint spanning insert + backbone; sensitive to gross rearrangement. |
| **E — fingerprint** | PstI | 4,117 + 1,544 + 447 + 109 | Independent four-band fingerprint (the 109 bp band runs off small gels — use a 1.5% gel). |

## Reading the gel

- **Correct clone:** Digest A gives **5,338 + 879 bp** (insert present, right size); Digest C
  gives 5,144 + 1,073 bp; NcoI and PstI give their four-band fingerprints.
- **Empty vector / failed ligation:** Digest A gives a single ~5,338 bp band (no 879 bp
  release); Digest C loses the 1,073 bp band.
- **Wrong-size insert:** the released band in Digest A departs from 879 bp.
- **Orientation:** not ambiguous here — NheI/XhoI is a directional clone, so the insert can
  only go in one way. NcoI/PstI fingerprints confirm the overall map.

## Bench recipe (per digest)

- 500 ng–1 µg plasmid DNA
- 1× enzyme buffer (use the manufacturer's recommended buffer; NheI+XhoI are compatible in
  a single buffer — check the double-digest finder)
- 5–10 U of each enzyme
- 37 °C, 1–2 h; heat-inactivate per enzyme
- Resolve on **1.0% agarose** (Digests A–D) or **1.5% agarose** (Digest E, to see the 109 bp
  band) with a 1 kb Plus ladder; 100 V, ~45 min; SYBR Safe or equivalent.

## Sanger confirmation (mandatory)

Restriction QC confirms size and map but **not sequence**. As with the native plasmids,
confirm the engineered CDS by Sanger sequencing across the insert — the seven YGGFEVVG cores
are synonymously distinct by design, so full-read coverage of the CDS is required to verify
all cores are intact (this is the engineered analogue of the plasmid-1 truncation lesson,
which a gel cannot see).

## Files
- `engPENK_therapy_plasmid.gb` / `.fasta` — annotated 6,217 bp circular therapy plasmid.
- `engPENK_therapy_qc_gel.png` — virtual gel of digests A–E vs 1 kb Plus ladder.
