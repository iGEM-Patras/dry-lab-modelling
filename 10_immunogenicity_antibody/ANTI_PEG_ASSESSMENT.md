# Anti-PEG antibodies and the lipoplex: what the literature says, and one cheap change

**Written 11 Oct 2026. Europe PMC, five papers that bear on it. Read the caveats, two of
the conclusions cut against the repo's current text.**

---

## 0. First, the repo disagrees with itself about which PEG lipid we use

`10_immunogenicity_antibody/antibody_assessment.md` flags anti-PEG as a failure mode for
"the repeat-dosed **PEG(2000)-CerC8** formulation". But `04_lipoplex_md/peg/PEG_FEASIBILITY.md`
already recorded that this conflicts with the bench spec, which lists **DMG-PEG2000 at
1.5 mol%** (`targeting/lipoplex_formulation_spec.csv`), and the wet-lab protocol uses
DMG-PEG2000 too.

| source | PEG lipid | anchor | mol% |
|---|---|---|---|
| `antibody_assessment.md` | PEG(2000)-CerC8 | C8 ceramide | 5 |
| **bench spec + wet-lab protocol** | **DMG-PEG2000** | **C14 diacylglycerol** | **1.5** |

**The immunogenicity assessment is written about a formulation we are not making.** That
needs fixing before anyone cites it. Everything below is about DMG-PEG2000 at 1.5 mol%,
which is what the bench will actually use.

---

## 1. The actionable finding: the PEG *terminus*, not the lipid

**ACS Nano 2026, doi:10.1021/acsnano.6c07672**, 1,970 human blood samples.

- Pre-existing anti-PEG antibodies are widespread, including in people with no prior
  exposure to PEGylated drugs.
- Binding of pre-existing anti-PEG IgM to PEG is **modulated by the terminal chemistry**,
  with **methoxy groups enhancing** the interaction.
- **Methoxy is the only terminal configuration used in currently marketed PEGylated
  nanomedicines**, which is why this has gone largely unexamined.
- **Hydroxy-PEG (OH-PEG) significantly evaded binding** by pre-existing anti-PEG IgM across
  samples from three independent hospitals.
- Replacing MeO-PEG with OH-PEG **attenuated complement activation** of LNPs caused by
  pre-existing anti-PEG IgM, improving serum stability and reducing cargo leakage.

**DMG-PEG2000 is methoxy-terminated.** So is essentially every catalogue PEG-lipid. The
change this suggests is a *single reagent substitution*: hydroxyl-terminated PEG2000-DMG
in place of the methoxy form. Same lipid, same anchor, same 1.5 mol%, same protocol.

This is the one recommendation in this document that is cheap, specific and testable.

---

## 2. The population has changed, and our patients are in it

**Pharmaceutics 2026, doi:10.3390/pharmaceutics18070815.** mRNA-LNP vaccination has shifted
the population-level anti-PEG repertoire. Both pre-existing and vaccine-induced anti-PEG
antibodies may compromise PEGylated therapeutics, and the emergence of **high-avidity
anti-PEG IgG** after repeated vaccination is associated with increased risk of
complement activation-related pseudoallergy (CARPA) and anaphylaxis.

For a chronic-pain therapy intended for **repeat administration** in adults who have mostly
had multiple mRNA vaccine doses, that is the relevant population, not the pre-2020 one.

---

## 3. The route question is NOT answered, and I will not pretend it is

I expected to be able to report that accelerated blood clearance is a systemic phenomenon
and therefore less relevant to an intranasal route. **The literature search did not support
that.** Queries pairing ABC and anti-PEG with intranasal, nose-to-brain and mucosal routes
returned general delivery reviews, not evidence either way.

So the honest position is: **whether ABC applies to intranasal dosing is an open question**,
not a reassurance we can write on a poster. It is mechanistically plausible that limited
systemic exposure reduces splenic priming, and it is equally plausible that nasal-associated
lymphoid tissue provides its own priming route. Neither has been shown for this formulation.

**This is a gap to state, and it is a genuinely good question for the wet lab to have asked.**

---

## 4. Shedding: real, but not a free pass

**Small 2026, doi:10.1002/smll.75613** establishes PEG-lipids as dynamic components that
shed on contact with biological media, governed by lipid structure and carrier properties.
**ACS Nano 2026, doi:10.1021/acsnano.5c19757** shows PEG-lipid anchors strongly affect
protein corona and biodistribution (liver, spleen, bone marrow, lung) despite being minor
components by molar ratio.

DMG's C14 anchor sheds faster than an C18 DSPE anchor, which is one reason it is the
standard choice. But neither paper demonstrates that shedding abolishes anti-PEG
recognition, and **Pharmaceutics 2025, doi:10.3390/pharmaceutics17081074** reports ABC
occurring even where expected antibody elevation was not observed. Shedding is a mitigation,
not an exemption.

---

## 5. What to actually do

| | priority |
|---|---|
| **Fix the formulation inconsistency** in `antibody_assessment.md`: it assesses CerC8, the bench uses DMG-PEG2000 | do first, costs nothing |
| **Price hydroxyl-terminated PEG2000-DMG.** If available and affordable, it is a one-reagent change with published benefit against pre-existing IgM and complement activation | cheap, specific |
| **State the route gap** on the Safety page rather than claiming intranasal avoids ABC | honesty, and judges reward it |
| Sandwich ELISA with RM105 + B141M/B139M for surface PEG density | only if the formulation is being characterised anyway |

**What this does not do:** it does not measure anything. Every statement here is from the
literature, and the only way to know whether our particles are recognised by human
pre-existing anti-PEG antibodies is to test them against human serum.

---

## References used

| | |
|---|---|
| Hydroxyl vs methoxy terminus, 1,970 samples | doi:10.1021/acsnano.6c07672 (ACS Nano 2026) |
| Population anti-PEG repertoire after mRNA-LNP | doi:10.3390/pharmaceutics18070815 (2026) |
| Anti-PEG antibodies, review | doi:10.3390/pharmaceutics17081074 (2025) |
| PEG-lipid shedding determinants | doi:10.1002/smll.75613 (Small 2026) |
| PEG-lipid anchor effects on corona and biodistribution | doi:10.1021/acsnano.5c19757 (ACS Nano 2026) |
