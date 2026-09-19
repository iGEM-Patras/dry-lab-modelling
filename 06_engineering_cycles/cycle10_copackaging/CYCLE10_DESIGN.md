# Cycle 10 — Do the two cargoes compete for the carrier?

**Status:** PRE-REGISTERED. Written and pushed before any simulation is run.
**Date:** 2026-09-19

## Why this cycle exists

Epione delivers two nucleic acids in one particle: the engineered PENK construct
(1,699–2,223 bp) and an siRNA against neprilysin. Every simulation in
[`04_lipoplex_md/`](../../04_lipoplex_md/) contains **DNA alone**. Whether both cargoes can
occupy the same lipoplex, or whether one excludes the other, has never been asked.

It is not an idle question. Cationic lipid is finite, both cargoes are polyanions competing
for the same binding partner, and they differ roughly threefold in charge. If the larger
construct monopolises the lipid, the siRNA arm is under-delivered and the knockdown fails —
a formulation problem that would present in the wet lab as "the siRNA doesn't work".

## The honest limitation, stated before the result

**No MARTINI RNA parameter set is installed on our cluster.** The only nucleotide
parameters available are `martini_v2.1-dna.itp`. We therefore model the siRNA as a **21-bp
DNA duplex**, and we call it a **charge surrogate**, not an siRNA.

What that surrogate can and cannot answer:

- **Can answer:** whether two polyanions of different size compete for a limited pool of
  cationic lipid, and which one wins. At coarse-grained resolution this is dominated by
  phosphate charge density and multivalency, both of which the surrogate reproduces.
- **Cannot answer:** anything RNA-specific. Real siRNA is A-form, with different helical
  rise and phosphate spacing from B-form DNA, and carries 2′-OH groups absent from this
  model. Any claim that depends on RNA chemistry is out of scope.

This sits on top of the parameter caveat already disclosed for the lipid topologies, which
are MARTINI-2 analogy models. Conclusions are comparative, never absolute affinities.

## Design

Both conditions reuse the equilibrated `MC3P` (protonated, endosomal-pH) systems, which is
the state in which binding actually happens. Three velocity seeds each, matching the
existing protocol.

| | cationic lipids | phosphates | N/P | question |
|---|---|---|---|---|
| current, DNA only | 120 | 120 | 1.00 | *(reference, already run)* |
| **A — sufficient lipid** | **162** | 162 | **1.00** | do both bind when carrier is not scarce? |
| **B — limiting lipid** | **120** | 162 | **0.74** | who wins when it is? |

Condition B is the one that matters. Holding the lipid fixed while adding cargo forces the
competition that a real formulation faces.

**Charge accounting.** 60-bp duplex = 120 phosphates; 21-bp duplex = 42 phosphates; total
162. The siRNA surrogate therefore carries **25.9 %** of the total cargo charge.

## Pre-registered predictions and gates

Every threshold below is fixed now. The null throughout is **charge-proportional binding**:
if the lipid does not discriminate, each cargo takes contacts in proportion to its
phosphate count, so the surrogate takes 25.9 % of contacts and the per-phosphate ratio
`contacts_siRNA / contacts_DNA` equals **0.350**.

| | Prediction | Gate (pass condition) |
|---|---|---|
| **P1** | Under sufficient lipid (A), **both** cargoes bind | both min-dist < 0.60 nm, mean over 3 seeds |
| **P2** | Under sufficient lipid, binding is near charge-proportional | surrogate share of contacts within 25.9 ± 10 pp |
| **P3** | Under limiting lipid (B), the **larger** cargo is favoured per phosphate | per-phosphate ratio < 0.350 |
| **P4** | The surrogate is **not** fully excluded even when lipid is limiting | surrogate min-dist < 0.80 nm |
| **P5** | Adding a second cargo does not detach the first | DNA min-dist in B within 0.10 nm of the DNA-only reference (0.469 nm) |

**Direction of the substantive prediction:** P3 says the 60-bp duplex outcompetes the
surrogate per unit charge, because multivalent binding favours the longer polyanion — more
simultaneous contacts, slower off-rate. If P3 is **falsified** and the surrogate competes
equally or better, that is the more interesting result and the more consequential one for
formulation: it would mean the small cargo can displace the large one.

**What falsification would change.** If P4 fails — the surrogate is excluded below
detection under limiting lipid — the recommendation becomes *formulate the two cargoes in
separate particles*, which is a real, actionable design change and would need to reach the
wet lab before any co-formulation is attempted.

## Metrics and analysis

Identical pipeline to the existing arm (`analyze_replicate.sh`), so the numbers are
comparable to the published 200 ns results: DNA–lipid contacts within 0.6 nm
(`gmx select`), minimum distance (`gmx mindist`), cation–cargo RDF (`gmx rdf`), radius of
gyration (`gmx gyrate`). Metrics computed on the equilibrated second half only.

Contacts are reported **separately for each cargo** and **normalised per phosphate**, since
the raw count is confounded by size — that normalisation is the whole point of P3.

## Sampling, and a constraint on it

The existing arm needed **200 ns** before between-seed spread converged: at 50 ns the
MC3-H⁺ closest-approach SEM was ±0.126 nm, collapsing to ±0.013 nm at 200 ns because
binding nucleates stochastically and a short window catches seeds in different states.
Cycle 10 therefore targets 200 ns and **will not report a verdict from a 50 ns snapshot**,
whatever it appears to show.

`pibu_el8` is currently heavily degraded (10 nodes `down~`). If capacity does not allow six
200 ns runs, the fallback is condition **B only** at three seeds, since B carries the
decision. That choice is recorded now so it cannot be presented later as the plan all along.

## Relationship to the rest of the project

This is the first lipoplex-arm work to be pre-registered. The existing 200 ns results are
sound but predate the convention, and that is noted on the Model wiki page rather than
glossed over.
