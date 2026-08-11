# Caption text for the PENK presentation slides

The AlphaFold render is a **visual element**, and that is a legitimate use. The
only hard rule is that the caption must not claim something the model does not
show. Below is wording that is both presentable and defensible.

---

## Suggested order

1. **Native enkephalins** — what the natural gene makes: 6 Met-, 1 Leu-enkephalin
2. **Domain architecture** — what the engineered molecule is, where the cargo sits
3. **AlphaFold confidence** — folded anchor vs disordered cargo tail
4. **Processing** — the KR cuts releasing the octapeptide
5. **Receptor complex** — the released peptide bound, with the 12.05 Å callout

The narrative runs: floppy carrier → proteolytic release → bound conformation
that only exists after excision. That sequence is why the disorder in shot 2 is a
feature of the story rather than a weakness to explain away.

---

## Slide: the native enkephalins (`enkephalin_met_leu_overview.png`)

The opening shot — what the natural gene makes, before the engineered construct
is introduced.

**Say this:**

> Human proenkephalin is 267 residues and carries 6 copies of
> Met-enkephalin and exactly one Leu-enkephalin. The two peptides share the same
> Tyr-Gly-Gly-Phe message domain and differ only at residue 5.

**Verified values on this slide:**

| quantity | value |
|---|---|
| native proenkephalin length | 267 aa (NCBI PENK_HUMAN, P01210) |
| Met-enkephalin copies | 6, at residues 100, 107, 136, 186, 210, 261 |
| Leu-enkephalin copies | 1, at residue 230 |
| Met-enkephalin [M+H]+ | 574.23 Da |
| Leu-enkephalin [M+H]+ | 556.28 Da |
| mass difference | 17.96 Da |
| diagnostic fragment pair | y1 = 150.06 (Met) vs 132.10 (Leu) |

The mass-spectrometry point worth making on screen: b1–b4 are **identical**
between the two peptides because the first four residues are the same; every
y-ion differs. So the y-series, not the b-series, tells them apart.

**Do not say:** *"the engineered construct makes Met- and Leu-enkephalin."* It
does not — it replaces all seven cores with `YGGFEVVG` and contains neither
native core (verified: 0 copies of YGGFM, 0 of YGGFL). The native peptides are
context for the design, not its product.

**Leu-enkephalin structure:** there is currently **no** structural model for
Leu-enkephalin in this project. A co-fold of both peptides against both the
delta- and mu-opioid receptors is queued on the cluster (job 17958370, `pgpu`,
estimated start 2026-08-15). Until it lands, do not show a Leu-enkephalin
structure — the only way to produce one now would be to mutate the Met model's
side chain, which is not an independent prediction and must not be presented as
one.
---

## Slide: domain architecture (`slide_penk_domain_architecture.png`)

16:9, 2666 × 1500 px, drops straight onto a slide.

**Talk track:** "One folded domain, held by seven cysteines. Everything after it
is deliberately floppy — and that is where the seven copies of the therapeutic
peptide live, each one preceded by the KR site the cell's proteases cut."

> Wording note: say **preceded by KR**, not "flanked by KR or KK." All seven
> cores have KR immediately upstream, but the downstream pair varies (KR, KK,
> RG, RR, RF). "Flanked by KR or KK" overstates what the sequence shows — and
> the same correction applies to the native gene.

This slide carries the argument the AlphaFold render cannot: *where* the cargo is
and *why* the disorder is functional. Show it immediately before or after the
render.

Verified values on this slide: 7 × `YGGFEVVG` at residues 100, 110, 142, 195,
222, 245, 279; cysteines at 8, 26, 30, 33, 48, 52, 65; FoldIndex 70.5 % of the
chain disordered, 98.2 % of the 56 core residues disordered.

---

## Slide: the AlphaFold proprotein render

**Status: the corrected run is complete.** Values below are read from its own
output files and are cleared for use on screen. The earlier run — in which the
885-nt DNA cloning sequence was submitted in the protein field — is **superseded
and must not be shown**; A, C, G and T are all valid amino-acid letters, so it
returned a confident-looking model of a molecule that does not exist.

**Say this:**

> AlphaFold model of the engineered PENK proprotein (288 aa). A folded,
> cysteine-rich anchor at residues 1–77 carries a long disordered tail holding
> the seven enkephalin copies — which is how the carrier presents them to
> processing proteases.

**Do not say:**

- *"AlphaFold structure of the engineered enkephalin"* — the render is the
  **carrier**, 288 residues. The enkephalin is 8 of them, ×7. Calling the whole
  thing "the enkephalin" is the mistake the audience will catch.
- *"predicted binding conformation"* — there is no receptor in this model.
- *"the model is low confidence, so it failed"* — a low global pTM is the
  expected signature of a mostly-disordered carrier, not a bad prediction. The
  anchor is confidently folded; say so.

**On-screen numbers — verified, safe to display:**

| quantity | value | source |
|---|---|---|
| chain length | 288 aa | submitted sequence, identical to the stored construct |
| ordered anchor | residues 1–77, mean pLDDT **84** | per-residue pLDDT, model 0 |
| cargo tail | mean pLDDT **31** | per-residue pLDDT, model 0 |
| cysteines in anchor | **7 of 7** | sequence positions 8, 26, 30, 33, 48, 52, 65 |
| pTM | **0.26** | `summary_confidences_0.json` |
| fraction disordered | **0.83** | `summary_confidences_0.json` |
| steric clashes | none, all 5 ranked models | `summary_confidences_*.json` |
| MSA depth | 1126 unpaired / 2031 paired, 4 templates | run's own `msas/` and `templates/` |

Keep the two disorder methods distinct. AlphaFold's own figure is
`fraction_disordered` = **0.83**. The FoldIndex figure is **70.5 %** of the chain
— a different calculation. Cite whichever you use by name; never present one as
the other.

Assets: `slide_engPENK_alphafold_confidence.png` (16:9 domain bar over the pLDDT
trace), `engPENK_alphafold_per_residue_plddt.csv`,
`engPENK_alphafold_CORRECTED_model_0.cif`.

---

## Slide: the excised peptide in the receptor

Assets: `DOR_engPENK_complex_annotated.pdb`, plus the ChimeraX / PyMOL scripts.

**Say this:**

> The processed octapeptide bound in the δ-opioid receptor. Boltz-2 co-folded
> model — a different predictor from AlphaFold.

**Do not say:** *"AlphaFold confidence"* over this render. The colours are
Boltz-2 pLDDT, and they describe a **receptor-bound** peptide, not a free one.
The palette matches AlphaFold's so the shots cut together visually; the caption
must still name the right method.

The number worth putting on screen: the Tyr1-OH → Phe4-ring pharmacophore
distance, **12.05 Å engineered vs 8.05 Å native** — measured from the
coordinates, and a real visual difference between the two molecules.
