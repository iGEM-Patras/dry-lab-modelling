# Can δ-selectivity be supported computationally? What the literature says

**Searched 10 Oct 2026, Europe PMC. Four papers matter. Two change what we can write;
one offers a method we have not tried; one is a precedent for the delivery route.**

---

## 1. The mechanism paper: our design hypothesis is incomplete, and that is citable

**Acta Pharmaceutica Sinica B, 2026.** *Mechanistic insights into ligand selectivity in
μ- and δ-opioid receptors beyond the "message-address" conceptual framework.*
PMID 41909724, [doi:10.1016/j.apsb.2025.11.039](https://doi.org/10.1016/j.apsb.2025.11.039)

What it establishes, by chimeric receptors, mutagenesis, voltage-clamp fluorometry,
engineered zinc bridges and microscale thermophoresis:

- **Residue 2.63** determines morphine's μ/δ selectivity. **EM-1 uses 2.63 and 3.29 plus the
  N-terminus and extracellular loops.**
- **EM-1's `YPWF` confers over 1500-fold μ/δ selectivity, driven by steric hindrance and a
  β-turn**, not by address sequence alone.
- **β-endorphin, with a more flexible sequence, binds both receptors non-selectively.**

**Why this matters to us.** Our payload is gene-encoded and all-L, so it cannot carry either
feature that rigidifies the selective comparators: a D-amino acid or a C-terminal amide.
Both deltorphins in our own control set carry the amide; `YGGFEVVG` has a free acid. This is
a published, mechanistic explanation for why an address graft alone may not transfer
selectivity, and it is the strongest thing we can say in place of a number we could not
compute. **We have not demonstrated it for our peptide.**

## 2. Selectivity IS computationally tractable, for small molecules

**Journal of Chemical Information and Modeling, 2026.** *Identification of Subtype-Selective
Binding Sites in the Opioid Receptor Family.* PMID 41930899,
[doi:10.1021/acs.jcim.5c02403](https://doi.org/10.1021/acs.jcim.5c02403)

Combines molecular dynamics, **funnel-metadynamics** and charge-density analysis across μ,
δ and κ. Finds distinct conformational dynamics per receptor, and assigns roles to the
**orthosteric subpockets and extracellular loops** in stabilising ligand-bound states.

**Read honestly:** this is the paper to cite for *"subtype selectivity in this receptor
family is computationally addressable from an energetic perspective"*. It is **not** a
method that would have given us a ΔΔG for an octapeptide. It works on morphinan-scaffold
small molecules, and it characterises sites and dynamics rather than predicting a
selectivity value for a novel ligand.

## 3. The one untried method that fits our budget, and what it can answer

**Preprint, 2026.** *Order of Message and Address Domain Engagement Determines Productive
β-Endorphin Binding to the μ-Opioid Receptor.*
[doi:10.64898/2026.02.06.704327](https://doi.org/10.64898/2026.02.06.704327)

Uses **1,000 independent CABS-dock simulations with no prior binding-site knowledge** to
compare alternative binding pathways for an opioid peptide.

**Why this one is different from the seven routes we exhausted.** It does not compute a
ΔΔG at all, so it is immune to both failure modes that defeated us: it is not anchored to
published affinities, and it never forms a difference of two large absolute quantities.
It is coarse-grained and cheap, so 1,000 runs per receptor is affordable.

**What it could answer:** whether our engineered payload engages the δ receptor's address
site in the same *order* as a known δ-selective peptide, from an ensemble rather than one
pose. That is a mechanistic, falsifiable question we have never asked.

**What it cannot answer:** the δ/μ selectivity of `YGGFEVVG`. Nothing computational
available to us can, and the cAMP assay still decides.

## 4. Not about selectivity, and possibly the most useful of the four

**ASN Neuro, 2026.** *Intranasal Delivery of Proenkephalin-Expressing Differentiated
Mesenchymal Stem Cells Attenuates Morphine Dependence Behaviors and Modulates Neurotrophic
Factors in Rats.* PMC13644638,
[doi:10.1080/17590914.2026.2739826](https://doi.org/10.1080/17590914.2026.2739826)

**Intranasal delivery of proenkephalin-expressing cells, in vivo, with a functional effect.**
Attenuated morphine-induced place preference, reversed recognition-memory deficits, reduced
anxiety-like behaviour, and upregulated hippocampal BDNF.

**Why it matters.** Until now our strongest delivery precedent was an HSV proenkephalin
vector delivered peripherally. This is **our route and our payload class, in vivo, working.**

**The honest gaps**, which belong next to the citation and not omitted:
- different indication: morphine dependence, not cancer pain
- different vehicle: mesenchymal stem cells, not a non-viral lipoplex
- native proenkephalin, not an engineered cassette
- rats, single study

---

## What this changes

**Nothing about what we may claim for `YGGFEVVG`.** No new route produces a selectivity
number, and the position stands: design goal, not demonstrated result.

**Something about what we may write.** The δ-selectivity rationale can now be grounded in
published mechanism rather than only in our own failed attempts, and the intranasal route
has an in vivo precedent with the same payload class.
