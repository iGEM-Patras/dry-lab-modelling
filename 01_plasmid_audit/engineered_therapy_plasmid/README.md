# Engineered PENK Therapy Plasmid (in silico assembly)

The therapeutic construct: the engineered anionic-address PENK (7× YGGFEVVG) cloned into the
**pcDNA3.1(+)** backbone via **NheI/XhoI**. Assembled in silico from the validated test-bed
vector so the therapy construct is parallel to the expression system.

- **Backbone donor:** plasmid 4 (PENK-P2A-mEGFP), single NheI, single XhoI → clean directional swap.
- **Assembly:** native P2A–mEGFP cassette (1,639 bp, NheI→XhoI) excised; 885 bp engineered
  insert (NheI–Kozak–CDS–XhoI) ligated in.
- **Product:** 6,217 bp circular plasmid. Verified: single NheI + single XhoI, engineered CDS
  present exactly once (288 aa, all 7 YGGFEVVG cores), native cassette removed.

## QC scheme (purpose-built)
The native-plasmid QC does **not** apply, the engineered plasmid has **no AflII site** and
its XbaI site is in the backbone. See `engPENK_therapy_qc_protocol.md` for the five diagnostic
digests (insert release NheI+XhoI → 5,338+879; identity BglII; NcoI & PstI fingerprints) and
`engPENK_therapy_qc_gel.png` for the virtual gel.

## Files
- `engPENK_therapy_plasmid.gb` / `.fasta`, annotated 6,217 bp circular plasmid.
- `engPENK_therapy_qc_protocol.md`, restriction QC protocol + Sanger confirmation note.
- `engPENK_therapy_qc_gel.png`: virtual gel (digests A–E vs 1 kb Plus ladder).

> Status: in silico design. Not yet built at the bench. Sanger sequencing across the CDS is
> mandatory after cloning: the seven cores are synonymously distinct and a gel cannot verify them.