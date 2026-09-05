# Lipoplex surface targeting: assessment of the bibliography's proposals

**Date:** 2026-08-12
**Trigger:** ΒΙΒΛΙΟΓΡΑΦΙΑ.docx, section «Antibodies on the lipoplex», proposing
two-level targeting `TfR + P2X3` and `TfR + TRPV1`.
**Scope:** targets never previously assessed in this project — P2X3, NaV1.7,
NaV1.8, TRPA1, INSR. TfR and TRPV1 were covered in `antibody_assessment.md`
and are re-computed here on the same footing for comparison.

## Method

For each target, three species (human / rat / mouse), reviewed UniProt entries
resolved by `gene_exact` + `organism_id` rather than by recalled accession —
three of my recalled accessions were wrong and were caught by a length check
before use.

1. **Surface availability.** Sum of UniProt `Topological domain = Extracellular`
   residues, as a fraction of full length. This is the quantity that decides
   whether an antibody can bind the protein *on an intact cell*.
2. **Cross-species epitope transfer.** Global Needleman-Wunsch identity
   (match +1, mismatch -1, gap -2) computed twice: over the full sequence, and
   over the concatenated extracellular segments only. The **difference** is the
   informative number — a reagent is raised against the ectodomain, not the
   average protein.

## Result

| target | role | % extracellular | largest ext. loop | identity full (h/rat) | identity **ectodomain** | Δ | verdict |
|---|---|---|---|---|---|---|---|
| TfR / TFRC | BBB crossing | 88.4% | 672 aa | 76.7% | 75.3% | −1.3 | B |
| INSR | BBB crossing | 66.9% | 731 aa | 94.4% | **95.5%** | +1.0 | **A** |
| P2X3 | nociceptor | 70.3% | 279 aa | 94.0% | **95.7%** | +1.7 | **A** |
| NaV1.7 / SCN9A | nociceptor | 16.9% | 79 aa | 93.1% | 90.0% | −3.1 | C |
| NaV1.8 / SCN10A | nociceptor | 14.2% | 69 aa | 83.2% | 65.6% | −17.6 | C |
| TRPV1 | nociceptor | 6.7% | 32 aa | 85.8% | 53.4% | −32.4 | D |
| TRPA1 | nociceptor | 4.8% | 28 aa | 79.7% | 60.7% | −18.9 | D |

Tiers: **A** ectodomain >50% and conserved >90%; **B** large ectodomain,
species-restricted; **C** limited surface; **D** not a viable antibody surface.

## What this decides

**`TfR + P2X3` is well founded. `TfR + TRPV1` is not.**

P2X3 presents **70.3% of its mass extracellularly in a single 279-residue
loop** — a genuine, contiguous, antibody-sized surface. TRPV1 presents 6.7%
across four loops whose largest is 32 aa. That is a tenfold difference in
available surface and it is the whole argument: an antibody cannot bind a
target that is inside the cell. This confirms, on independent evidence, the
existing assessment's rejection of TRPV1 as a surface-targeting handle.

**The conservation result is the useful surprise.** For every target that
fails, the ectodomain is *less* conserved than the protein average — TRPV1
loses 32 points, TRPA1 19, NaV1.8 18. For P2X3 it goes the other way: the
ectodomain is **more** conserved (95.7%) than the full protein (94.0%). The
practical consequence is direct — an anti-P2X3 reagent validated in rat should
transfer to human without re-raising, and the same construct serves both the
animal model and the eventual human target.

Note the contrast with **TfR itself at 75.3% ectodomain identity**, which is
exactly why the existing assessment records that anti-TfR clones are
species-specific and non-interchangeable. On this axis the nociceptor half of
the `TfR + P2X3` pair is the *better-behaved* component.

**INSR is a credible second BBB handle** on the same criteria (66.9%
extracellular, 95.5% ectodomain identity) and is worth carrying as an
alternative to TfR, particularly because it does not inherit TfR's
species-restriction problem.

## Literature support (PubMed counts, 2026-08-12)

| query | hits |
|---|---|
| P2X3 + antibody | 94 |
| P2X3 + antibody + flow cytometry / live cell / surface | 9 |
| P2X3 + extracellular + epitope/loop | 13 |
| P2X3 + nanoparticle / liposome / lipoplex | 13 |
| P2X3 + DRG / nociceptor | 283 |
| P2X3 antagonist / gefapixant + clinical trial | 52 |
| TRPV1 + antibody + flow / live cell / surface | 22 |
| TfR + antibody + brain delivery/transcytosis | 324 |

Read this honestly. P2X3 is **well validated as a nociceptor marker** (283) and
**clinically drugged** (52 — the gefapixant programme), but has only 9 papers
touching live-cell surface antibody work and 13 on nanoparticle targeting.
So the topology is favourable and the biology is established, but **P2X3 has
not been used as a nanoparticle-targeting ligand before**. That is a novelty
claim, not a de-risked path — and it means the surface-binding step needs its
own validation rather than a citation.

TfR, by contrast, has 324 brain-delivery papers: the BBB-crossing half of the
pair rests on established ground.

## Caveats, stated plainly

- **UniProt topology is annotation, not structure.** For P2X3 the single large
  loop is supported by the trimeric P2X architecture, but the exact epitope
  accessibility in a membrane, and whether it is occluded by glycosylation,
  is not answered here.
- **Ectodomain identity is not epitope identity.** 95.7% over 279 residues
  still allows ~12 substitutions, and a clone's specific epitope could sit on
  one of them. This screens *out* impossible targets reliably; it does not
  guarantee any specific clone transfers.
- **Your own annotation stands.** The bibliography already notes that
  nociceptor markers are not synonymous with central pain regions. Nothing
  here addresses whether P2X3+ peripheral terminals are the right
  compartment for an intranasally delivered lipoplex — that is a separate
  question from whether P2X3 is bindable.
- **P2X3 is not exclusively neuronal.** It is expressed on bladder urothelium
  and in the airway (the mechanism of gefapixant's cough indication, and of
  its taste side-effects). A P2X3-targeted particle reaching systemic
  circulation has off-target tissue.

## Recommendation

1. Carry **`TfR + P2X3`** forward as the lead targeting pair. Drop
   `TfR + TRPV1` — the surface is not there.
2. Carry **INSR** as the alternative BBB handle, since it avoids the
   species-restriction that forces a clone swap between rat and human work.
3. Treat P2X3 surface-targeting as **unprecedented and requiring validation**:
   the first experiment is live-cell binding on a P2X3-expressing line, not a
   formulation study.
4. NaV1.7 is not excluded outright (16.9%, 90.0% conserved) but its largest
   loop is 79 aa; it is a distant third and not worth pursuing while P2X3 is
   available.

## Files

- `lipoplex_targeting_assessment.csv` — full table, all three species
- `lipoplex_targeting_assessment.png` — the two decisive axes
- `uniprot_targets.json` — raw UniProt records as fetched

### Registry-wide screen (added 2026-08-12, superseding the literature-only search)

The literature-mining route above found only reagents that papers happened to cite. A direct
registry query returned **103 P2X3 records / 93 unique reagents** — the full commercial landscape.
Four publish a full immunogen sequence; each was located in the human and rat sequences and tested
against the 44–322 ectodomain:

| RRID | Vendor / cat | Immunogen position | Verdict |
|---|---|---|---|
| **AB_2757757** | ABclonal A10232 | **44–317** (274 aa) | **Extracellular** — essentially the entire ectodomain |
| **AB_2683526** | Atlas HPA057776 | **184–260** (77 aa) | **Extracellular** — PrEST, wholly inside the ectodomain |
| AB_2759812 | ABclonal A12965 | 328–397 | Cytoplasmic — not for targeting |
| AB_2759770 | ABclonal A12924 | 328–397 | Cytoplasmic — not for targeting |

This changes the recommendation. **A10232 (AB_2757757)** now has the strongest verified epitope of
any P2X3 reagent — its immunogen *is* the ectodomain, confirmed against the sequence rather than
inferred. It is listed for rat, but the human sequence over those same positions is **95.6%**
identical, consistent with the ectodomain conservation computed above. **HPA057776 (AB_2683526)** is
the human-listed counterpart (aa 184–260; 92.2% identical in rat), so the two together cover both
species with verified extracellular epitopes.

Neither is validated for live-cell surface binding — A10232 lists WB only, HPA057776 IHC only. The
binding gate in the protocol still applies; these are better *starting* reagents, not a shortcut past
validation.

Separately, the **Bioss bs-4249R series** is the only P2X3 reagent listing **flow cytometry**
(1:20–100) and ships in 14 pre-conjugated variants (FITC, PE, Cy3, Cy5, Cy7, biotin, …), which would
remove a conjugation step. Its epitope is undisclosed — request it before relying on it.

*Screen: `p2x3_registry_epitope_screen.csv`. Note the earlier lead, PA5-77682, remains valid but its
immunogen is still undisclosed, so its epitope is asserted by the vendor rather than verified here.*
