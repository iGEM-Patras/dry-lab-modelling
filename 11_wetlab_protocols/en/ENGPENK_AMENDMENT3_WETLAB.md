# Amendment 3 — cassette 5 opens a second processing branch

**Supersedes:** two statements in Amendment 2 (`NATIVE_PENK_AMENDMENT2_WETLAB`). Everything else in
Amendments 1 and 2 stands. Triggered by Ozawa et al. 2007 (*Anal. Biochem.*), attached to this project.

---

## 0. Retractions

**0.1 — "No monoisotopic collision within 1.5 Da between any native and any construct peak."**
False. `VGRPEWWMDYQKRYG` (BAM-8-22) is produced by both the native precursor and the construct at
**Δm = 0.0000 Da**, because it lies entirely downstream of the swapped core. It is not resolvable
at any mass accuracy, any charge state, any isotope. Do not use it as a construct marker.
The corrected statement: *all construct-specific peaks are mass-resolved from native background;
one shared peak exists and is uninformative.*

**0.2 — the engineered product panel has 6 species.**
It has 11. Cassette 5 sits in a downstream context byte-identical to native core 5, so it follows the
BAM branch and yields five species the shipped target list omits.

---

## 1. Why: the construct is native PENK with the cores swapped

Sequence alignment of the engineered proprotein against UniProt P01210 gives 252 of 267 residues
shared in contiguous blocks, and **every downstream flank is byte-identical to its native
counterpart**. The construct therefore inherits native processing fate cassette-by-cassette:

| Fate class | Cassettes | Downstream flank | Consequence |
|---|---|---|---|
| clean dibasic | 1, 2, 3, 6 | `KR` / `KK` | octapeptide → amidated heptapeptide |
| extended monobasic | 4, 7 | `RGL`, `RF` | extended product (native architecture — see Amd 2 §0.2) |
| **BAM branch** | **5** | **`RRVGRPEWWMDYQKR…`** | **five additional species, previously unlisted** |

## 2. The five omitted species

| Species | Sequence | [M+H]⁺ | Note |
|---|---|---|---|
| `YGGFEVVGRRV`-NH₂ | adrenorphin analogue | 1237.6800 | PAM product of `…RRVG` |
| `YGGFEVVGRRVG` | pre-PAM acid | 1295.6855 | amidation substrate |
| engBAM-22 | `YGGFEVVGRRVGRPEWWMDYQKRYG` | 3091.5107 | 2 Met → +1/+2 ox satellites |
| engBAM-20 | `YGGFEVVGRRVGRPEWWMDYQKR` | 2871.4260 | 2 Met → +1/+2 ox satellites |
| BAM-8-22 | `VGRPEWWMDYQKRYG` | 1970.9330 | **shared with native — not a marker** |

Add all five to the method file. The first two are genuine construct-specific markers and are
independently useful: they are a **second, independent readout of PAM activity** on this precursor,
at a different cassette from the ones the octapeptide reports on.

## 3. What Ozawa 2007 lets us do about the standing option A / B decision

The amidation question has blocked the peptide order since Amendment 1: we predict PAM converts
`YGGFEVVG` → `YGGFEVV`-NH₂ but have never measured it. Ozawa et al. run the granule cascade
**in vitro as three separate reactions** — convertase, then carboxypeptidase, then amidation —
because the buffers required downstream inhibit the convertase, so the steps cannot be combined
in one tube. Each step is read by mass.

That is directly applicable here, and each step has a distinct diagnostic shift:

| Step | Option A product | [M+H]⁺ | Option B product | [M+H]⁺ |
|---|---|---|---|---|
| convertase only | `YGGFEVVGKR` | 1111.5894 | `YGGFEVVGGKR` | 1168.6109 |
| + carboxypeptidase | `YGGFEVVG` | 827.3934 | `YGGFEVVGG` | 884.4148 |
| + amidation | `YGGFEVV`-NH₂ | 769.3879 | `YGGFEVVG`-NH₂ | 826.4094 |

The amidation step is **−58.01 Da under both designs**, so a single synthetic peptide run through
the published cascade answers the option A / B question without committing the construct.

**Recommended:** order `YGGFEVVGKR` (or the 12-mer spanning the cassette-5 flank) as a synthetic
substrate, run the three-step in-vitro cascade, and read the −58.01 Da shift. That is a
peptide-synthesis order and three enzyme reactions, against a cloning round for the option B insert.

## 4. One caution the authors raise, which applies to us

Ozawa et al. state plainly that computational cleavage-site prediction is not reliable, and that
what confines processing to genuine sites is the limited specificity of the convertases themselves.
Every cassette-fate assignment in §1 is a prediction from flanking sequence. The in-vitro cascade is
the way to test them; it is not a formality.

## 5. Checklist

- [ ] Add the five cassette-5 species to the MS method file
- [ ] Strike BAM-8-22 from any construct-marker list; keep it as a native-background peak
- [ ] Order `YGGFEVVGKR` synthetic substrate for the in-vitro cascade
- [ ] Re-run the cascade on the cassette-5 flank peptide (`YGGFEVVGRRVG`) as an independent PAM readout
- [ ] Hold the option B cloning decision until the −58.01 Da shift is measured
