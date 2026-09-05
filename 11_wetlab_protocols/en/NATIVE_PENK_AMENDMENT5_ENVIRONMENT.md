
# Native PENK Amendment 5 — the extracellular environment changes the analysis

**Scope:** native (unmodified) human proenkephalin, P01210, 267 aa. Companion to
Amendment 2, which covered granule processing only. **Basis:** the peptidase evidence
established in engPENK Amendment 4, applied to the native panel.

## §0 What changes, and why

Amendment 2 analysed native PENK as a **granule** problem: PC1/PC3 and PC2 cut at dibasic
sites, CPE trims basic residues, PAM amidates a Gly-extended precursor. That is correct and
stands. But it stops at the granule membrane. Once secreted, every product enters a
compartment with a different pH, no Ca²⁺ gradient, and a different enzyme set —
**NEP, ACE and APN on the cell surface**. Three consequences, none of which were in
Amendment 2:

1. The panel is not 25 peaks. It is **49**, because ACE generates a second tier of products.
2. Two enkephalin peaks are **route-ambiguous** — the same mass arises granule-side and
   extracellular-side.
3. The MS method needs a stated resolving power, because the extended panel contains a
   1.27 Da pair.

Amendment 2's own §0 retraction (core 5 *is* a PAM substrate; cassettes 4/7 are native
architecture) is unaffected.

## §1 The NEP site count, corrected

Amendment 2 inherited the flat rule — every bond followed by a hydrophobic residue counted
as a neprilysin site. That rule is wrong (see engPENK Amendment 4 §0 R1): the S1′ pocket is
shaped by Phe563 and prefers **aromatic** P1′ residues, and a valine at P1′ leaves an
unfavourable gap on binding (Sexton et al. 2012). Re-scored in tiers:

| species | canonical (aromatic P1′) | large aliphatic P1′ | Val P1′ (disfavoured) |
|---|---|---|---|
| Leu-enkephalin `YGGFL` | **1** | 0 | 0 |
| Met-enkephalin `YGGFM` | **1** | 0 | 0 |
| MERF `YGGFMRF` | **1** | 1 | 0 |
| MERGL `YGGFMRGL` | **1** | 1 | 0 |
| adrenorphin `YGGFMRRV`-NH₂ | **1** | 1 | 0 |
| Peptide F `YGGFMKRYGGFMKK` | **3** | 2 | 0 |
| BAM-8-22 | **4** | 1 | 0 |
| BAM-20 | **4** | 2 | 1 |
| BAM-22 | **5** | 2 | 1 |

The pentapeptides carry exactly one canonical site — `Gly3-Phe4`, the classical
enkephalinase bond. The **BAM peptides carry four to five**, which is the quantitative
reason they are short-lived extracellularly and why granule content and secreted content
are not the same population.

## §2 ACE doubles the panel

ACE is a dipeptidyl carboxypeptidase; it removes a C-terminal dipeptide, and it acts on
amidated substrates too (Bernstein et al. 2013). Applied to every native species:

| substrate | ACE removes | product | product [M+H]⁺ | identity |
|---|---|---|---|---|
| `YGGFMRF` (MERF) | Arg-Phe | `YGGFM` | 574.2330 | **Met-enkephalin — activating** |
| `YGGFMRGL` (MERGL) | Gly-Leu | `YGGFMR` | 730.3341 | novel fragment |
| `YGGFMRRV`-NH₂ | Arg-Val-NH₂ | `YGGFMR` | 730.3341 | novel fragment |
| `YGGFM` | Phe-Met | `YGG` | 296.1241 | inactive |
| `YGGFL` | Phe-Leu | `YGG` | 296.1241 | inactive |
| BAM-22 | Tyr-Gly | BAM-20 | 2618.2656 | **already in the panel** |
| BAM-8-22 | Tyr-Gly | `VGRPEWWMDYQKR` | 1750.8482 | novel fragment |
| Peptide F | Lys-Lys | `YGGFMKRYGGFM` | 1413.6442 | novel fragment |

The MERF→Met-enkephalin conversion is ACE-dependent *in vivo*, not a test-tube artefact:
ACE inhibition raises extracellular MERF specifically while leaving Met- and
Leu-enkephalin unaffected (Bhatt et al. 2025).

**Two route ambiguities follow directly.** A peak at 574.2330 is Met-enkephalin whether it
came from granule cores 1/2/3 or from ACE acting on secreted MERF. A peak at 2618.2656 is
BAM-20 whether it was a granule intermediate or ACE product of secreted BAM-22. Neither
can be resolved by mass. **Resolving them requires a captopril (± thiorphan) arm**, not a
better mass spectrometer.

## §3 The C-terminal region Amendment 2 omitted

Amendment 2's panel covered the opioid cores and BAM intermediates. It did not include the
precursor's C-terminal acidic region, which is a major secreted product:

| species | residues | [M+H]⁺ |
|---|---|---|
| enkelytin region, free acid | PENK(237-258) `FAEALPSDEEGESYSKEVPEME` | 2473.0599 |
| enkelytin, +1 phospho | " | 2553.0262 |
| enkelytin, +2 phospho | " | 2632.9925 |
| Peptide B | PENK(210-258) | 5893.7624 |

This region carries three Ser and one Tyr, so the phospho-forms are the species to expect,
not the free acid. **This is where the panel gets hard**: enkelytin+2P at 2632.9925 sits
**1.268 Da** from BAM-20+1ox at 2634.2605 — a
resolving power of **≈2100** at z=1, and the same requirement at z=2 and z=3. Any
instrument below that will merge the two. Every other pair in the 49-peak panel is
either resolved or a same-sequence duplicate.

## §4 What this means for the construct comparison

The engineered cassette is judged against native background, so the background matters:

- **Native Met-enkephalin has one canonical NEP site. So does every cassette product.**
  The earlier claim that the cassette was less stable was retracted in engPENK Amendment 4;
  this analysis confirms the native side of that comparison independently.
- **Both are ACE substrates and both give an activating conversion.** ACE turns native MERF
  into Met-enkephalin; it turns the cassette 7 analogue `YGGFEVVGRF` into the target
  octapeptide `YGGFEVVG` (827.3934). The same chemistry, on both sides.
- **BAM-8-22 remains the shared peak** (1970.9330, engPENK Amendment 3 §0) — it lies
  downstream of the swapped core and is produced identically by native and construct.
  Its ACE product `VGRPEWWMDYQKR` at 1750.8482 is shared for the same reason. Add it to
  the shared-peak list, not the marker list.

## §5 Bench actions

1. **Extend the MS target list to 49 peaks** — see `native_penk_extended_ms_panel.csv`.
   The 24 new entries are ACE products and the C-terminal/phospho forms.
2. **Specify R ≥ 3000** on the method (1.4× margin over the 2100 requirement) or exclude
   the 2620–2640 window from quantitation.
3. **Add a captopril arm** to any experiment quantifying Met-enkephalin or BAM-20.
   Without it, granule-derived and ACE-derived peaks are not separable.
4. **Add thiorphan** if BAM peptide recovery is low — four to five canonical NEP sites
   predicts rapid loss, and low recovery is expected rather than a handling failure.
5. **Look for the phospho-enkelytin forms**, not the free acid.

## §6 Checklist

- [ ] MS target list replaced with the 49-peak version
- [ ] Instrument resolving power confirmed ≥3000, or 2620–2640 excluded
- [ ] Captopril (ACE) arm added where Met-enkephalin or BAM-20 is quantified
- [ ] Thiorphan (NEP) arm available for BAM recovery troubleshooting
- [ ] BAM-8-22 **and** its ACE product moved to the shared-peak list
- [ ] Amendment 2's flat NEP counts superseded by §1

## References

1. Sexton T. et al. (2012) *PLoS ONE* 7:e32343 — NEP S1′ pocket, Phe563, aromatic P1′ preference. doi:10.1371/journal.pone.0032343
2. Bernstein K.E. et al. (2013) *Pharmacol Rev* 65:1 — ACE as dipeptidyl carboxypeptidase; amidated substrates. doi:10.1124/pr.112.006809
3. Bhatt et al. (2025) *Commun Biol* — ACE inhibition raises MERF selectively. doi:10.1038/s42003-025-08790-6
4. Ozawa A. et al. (2007) *Anal Biochem* — in-vitro PC2/CPE/PAM cascade.
