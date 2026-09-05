
# engPENK Amendment 4 — protease liability retracted, option B recommended

**Supersedes:** three statements in Amendments 1–3. **Basis:** five primary sources, cited inline.
**Status of prior amendments:** everything not named in §0 stands.

## §0 Retractions

**R1 — the NEP site count was wrong (Amendments 1, 2, 3).**
I counted every bond followed by a hydrophobic residue as a neprilysin site, which made
`YGGFEVVG` look like a 3-site peptide against Met-enkephalin's 1. Neprilysin's S1′ pocket
is shaped by Phe563 and imparts a preference for **aromatic** P1′ residues; a valine at P1′
is too small and leaves an unfavourable gap on binding (Sexton et al. 2012, PLoS ONE 7:e32343).
Val-P1′ bonds are therefore not equivalent sites.

Corrected count — **every species carries exactly one canonical NEP site, `Gly3-Phe4`, the same
bond as native enkephalin**:

| peptide | shipped count | canonical (aromatic P1′) | poor (Val P1′) |
|---|---|---|---|
| Met-enkephalin `YGGFM` | 1 | 1 | 0 |
| engPENK octapeptide `YGGFEVVG` | 3 | **1** | 2 |
| option A `YGGFEVV`-NH₂ | 2 | **1** | 1 |
| option B `YGGFEVVG`-NH₂ | 3 | **1** | 2 |
| engMERF `YGGFEVVGRF` | 3 | **1** | 2 |

**R2 — "amidation blocks ACE" was wrong (Amendment 1 table).**
ACE cleaves substrates whose C-terminus is amidated, including dipeptide release from
substance P and CCK-8 and tripeptide release from GnRH (Bernstein et al. 2013,
Pharmacol Rev 65:1). Amidation slows ACE; it does not confer immunity. Both option A and
option B are ACE substrates.

**R3 — "the cassette is less protease-stable than native enkephalin" does not survive R1+R2.**
With one canonical NEP site each and both species ACE-accessible, there is no evidence base
for a stability penalty. I am not replacing it with a claim of *greater* stability — the
Val-P1′ bonds are disfavoured, not proven inert, and no kinetics on these sequences exist.
The honest position: **NEP/ACE liability is comparable to native, and measuring it is a
wet-lab task, not a sequence-inspection task.**

## §1 Cassette 7 is an asset, not a defect

ACE is a dipeptidyl carboxypeptidase. On native MERF (`YGGFMRF`, core 7's product) it removes
Arg-Phe to give Met-enkephalin — an activating conversion. Applied to the cassette 7 analogue:

| substrate | ACE removes | product | [M+H]⁺ |
|---|---|---|---|
| `YGGFMRF` (native) | Arg-Phe | `YGGFM` | 574.2330 |
| `YGGFEVVGRF` (cassette 7) | Arg-Phe | **`YGGFEVVG`** | **827.3934** |

The cassette 7 product is converted by ACE into the target octapeptide, by the identical
chemistry that activates the native peptide. Independently, ACE inhibition raises extracellular
MERF specifically while leaving Met- and Leu-enkephalin unaffected (Bhatt et al. 2025,
Commun Biol), which means the MERF→enkephalin route is ACE-dependent *in vivo*, not a
test-tube artefact. Amendment 2 treated cassettes 4 and 7 as an open pharmacology question;
for cassette 7 the answer now leans positive.

## §2 Option B is the recommended cassette

Deltorphin II is `Tyr-D-Ala-Phe-Glu-Val-Val-Gly`-NH₂. Its δ-selectivity is attributed to a
C-terminal **address** sequence, named explicitly as `-Val-Val-Gly`-NH₂; appending that address
to an enkephalin message shifts receptor selectivity toward δ (Ciszewska et al. 2011,
Acta Biochim Pol 58:225 — a construct architecturally identical to this project's:
enkephalin message elongated by a deltorphin C-terminal fragment).

- **option B** `YGGFEVVG`-NH₂ — carries `-Val-Val-Gly`-NH₂ **intact**
- **option A** `YGGFEVV`-NH₂ — deletes the address glycine and relocates the amide onto Val

Option A does not merely shorten the peptide; it destroys the motif the δ-selectivity rationale
rests on. **Recommendation: option B.**

Two cautions. First, Ciszewska et al. note the selectivity shift generally arises from *losing*
μ affinity rather than gaining δ affinity — expect a selectivity ratio change, not a potency
gain. Second, deltorphin's message uses D-Ala²; the cassette necessarily uses the genetically
encodable `Tyr-Gly-Gly-Phe`, so the message domain is enkephalin's, not deltorphin's. Option B
is an enkephalin-message/deltorphin-address hybrid, which is exactly the class Ciszewska
characterised — but its affinities are unmeasured.

## §3 What this changes on the bench

1. **Order option B** (`YGGFEVVG`-NH₂, i.e. cassette encodes `...YGGFEVVGG-KR...`). The Gly is
   the PAM substrate *and* the address residue — one glycine serving both roles.
2. **Run the Ozawa 3-step cascade on `YGGFEVVGGKR`** (Amendment 3 §2), not `YGGFEVVGKR`. The
   −58.01 Da amidation readout is unchanged.
3. **Add an ACE arm to the MS panel.** Expect `YGGFEVVG` (827.3934) from the cassette 7 product
   and `YGGFEV` (671.3035) from over-digestion of the octapeptide itself.
4. **Do not report a stability advantage** for the cassette in any grant text or figure legend
   until NEP/ACE kinetics on `YGGFEVVG` are measured.

## §4 Checklist

- [ ] Peptide order switched to option B (`YGGFEVVG`-NH₂) and the +Gly cassette sequence
- [ ] Amendment 1 liability table reissued with the corrected NEP counts (R1) and ACE column (R2)
- [ ] Synthetic `YGGFEVVGGKR` ordered for the in-vitro cascade
- [ ] ACE (± captopril) arm added to the degradation protocol
- [ ] Any slide or draft claiming improved protease stability corrected

## References

1. Sexton T. et al. (2012) *PLoS ONE* 7:e32343 — NEP S1′ pocket, Phe563, P1′ preference. doi:10.1371/journal.pone.0032343
2. Bernstein K.E. et al. (2013) *Pharmacol Rev* 65:1 — ACE dipeptidyl carboxypeptidase; amidated substrates. doi:10.1124/pr.112.006809
3. Bhatt et al. (2025) *Commun Biol* — ACE inhibition raises MERF selectively. doi:10.1038/s42003-025-08790-6
4. Ciszewska M. et al. (2011) *Acta Biochim Pol* 58:225 — enkephalin/deltorphin hybrids; `-Val-Val-Gly`-NH₂ address. doi:10.18388/abp.2011_2269
5. Ozawa A. et al. (2007) *Anal Biochem* — in-vitro PC2/CPE/PAM cascade. (Amendment 3 ref.)
