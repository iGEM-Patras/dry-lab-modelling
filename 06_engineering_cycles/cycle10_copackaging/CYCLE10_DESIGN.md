# Cycle 10 — Do the two cargoes compete for the carrier?

**Status:** PRE-REGISTERED, **amended 2026-09-19 before any simulation was run**.
**Date:** 2026-09-19

> **Amendment 1 — corrected charge accounting.** The first version of this document computed
> every gate from a 60-**bp** duplex. The system's DNA is a **30-bp** duplex (60 *nucleotides*);
> `04_lipoplex_md/README.md` conflated the two and that error was inherited here. The bead
> count settles it independently: `dna_cg.gro` has 388 beads over 60 nucleotides = 6.47
> beads/nt, MARTINI 2's DNA resolution. Consequently the existing N/P is **2.00, not 1.00**,
> and the charge-proportional null is **41.2 %, not 25.9 %**, with a per-phosphate parity
> ratio of **0.700, not 0.350**. All gates below are the corrected values. Nothing had run
> when this was found — which is the reason the numbers were written down in advance.

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

> **Amendment 2 — phosphate count derived from the topology, not from base-pair arithmetic.**
> Amendment 1 corrected 60 bp to 30 bp but still computed charge as 2 phosphates per base
> pair. That over-counts: a **free 5′ terminus carries no phosphate**, which is visible in
> the bead counts (`DA5` has 6 beads where `DA` has 7 — the missing bead *is* the phosphate).
> Summing the charge column of each topology gives **construct −58, surrogate −40, total 98**,
> not 102. `genion` independently confirmed it by requesting exactly 22 counter-ions for a
> +120/−98 system, matching the derivation. Corrected values, used in the gates below:
>
> | | amendment 1 | **correct** |
> |---|---|---|
> | construct phosphates | 60 | **58** |
> | surrogate phosphates | 42 | **40** |
> | condition B N/P | 1.18 | **1.22** |
> | surrogate share of cargo charge | 41.2 % | **40.8 %** |
> | per-phosphate parity ratio | 0.700 | **0.690** |
>
> The shifts are ~1 % and change no gate outcome (P2 allows ±10 pp), but the pre-registration
> should describe the system that is actually simulated. Standing lesson: **derive gate
> parameters from the built topology, not from the design description.** Both amendments were
> arithmetic *about* the system rather than measurement *of* it, and both were caught only
> because the numbers were written down in advance.

## Design

Both conditions reuse the equilibrated `MC3P` (protonated, endosomal-pH) systems, which is
the state in which binding actually happens. Three velocity seeds each, matching the
existing protocol.

| | cationic lipids | phosphates | N/P | question |
|---|---|---|---|---|
| current, DNA only | 120 | 58 | 2.07 | *(reference, already run)* |
| **A — sufficient lipid** | **203** | 98 | **2.07** | do both bind when carrier is not scarce? |
| **B — limiting lipid** | **120** | 98 | **1.22** | who wins when it is? |

Condition B is the one that matters. Holding the lipid fixed while adding cargo forces the
competition that a real formulation faces.

**Charge accounting.** 30-bp construct duplex = 60 phosphates; 21-bp surrogate = 42
phosphates; total **102**. The surrogate therefore carries **41.2 %** of total cargo charge —
the two cargoes are far closer in charge than the raw base-pair counts suggest, which makes
the competition question sharper rather than weaker.

**What the construct fragment actually is.** `frag.fasta` reads
`AAGCGTTACGGTGGTTTCGAGGTCGTCGGT`, which translates to **`KR-YGGFEVVG`** — the dibasic
processing site followed by the engineered octapeptide. The DNA in these simulations is one
cassette of the real construct, not a generic duplex.

## Pre-registered predictions and gates

Every threshold below is fixed now. The null throughout is **charge-proportional binding**:
if the lipid does not discriminate, each cargo takes contacts in proportion to its
phosphate count, so the surrogate takes **41.2 %** of contacts and the per-phosphate ratio
`contacts_surrogate / contacts_construct` equals **0.700**.

| | Prediction | Gate (pass condition) |
|---|---|---|
| **P1** | Under sufficient lipid (A), **both** cargoes bind | both min-dist < 0.60 nm, mean over 3 seeds |
| **P2** | Under sufficient lipid, binding is near charge-proportional | surrogate share of contacts within **40.8 ± 10 pp** |
| **P3** | Under limiting lipid (B), the **larger** cargo is favoured per phosphate | per-phosphate ratio < **0.690** |
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

`pibu_el8` has **495 idle cores** at the time of writing, so all six 200 ns runs are
affordable. (An earlier reading of this document claimed the partition was heavily degraded;
that was a misreading of `sinfo` — 10 nodes are `down~` but 17 others are `mix`/`idle`.) The
fallback, should capacity change, is condition **B only** at three seeds, since B carries the
decision. It is recorded now so it cannot be presented later as the plan all along.

## Relationship to the rest of the project

This is the first lipoplex-arm work to be pre-registered. The existing 200 ns results are
sound but predate the convention, and that is noted on the Model wiki page rather than
glossed over.


---

## Build log — what it took to assemble condition B

Recorded because the failures are informative and because a later reader repeating this will
hit the same walls.

**Insertion into the equilibrated system is impossible.** The reference box is volumetrically
full: the lipid aggregate spans z 0.81–9.68 nm of a 14.82 nm box and the construct spans
5.78–16.91 nm (wrapping the boundary). The largest void anywhere offers **0.31 nm** clearance;
a 7 nm duplex needs far more. `gmx insert-molecules` reported `Added 0 molecules` while
`Replaced 398 residues` — a *destructive no-op* that deletes solvent and inserts nothing, and
exits 0. Caught by counting nucleotide beads (388, not the required 659) rather than trusting
the exit status.

**Both cargoes place cleanly into an empty box**, confirming the duplex was never too large —
the order of assembly is what matters. Condition B is therefore rebuilt from scratch with the
reference's box and lipid content, both cargoes placed before lipids and solvent.

**Names must be read, not assumed.** The cationic lipid's residue is `MC3T`; `MC3P` is only the
replicate *directory* name. Ion moleculetypes are `NA`/`CL`, not `NA+`/`CL-`. No coarse-grained
water template exists on the cluster, so one was built from the reference's own 23,934
equilibrated waters — a better template anyway, since it carries the right density for this
temperature and salt.

**`polyply gen_coords` returns bead-correct, geometry-wrong output.** It produced 271 beads for
the surrogate — the right number — but with base-pair bonds spanning a **median 7.16 nm** where
they should be 0.445 nm: the two strands were placed unpaired. The count assertion passed and
the structure was carried through four further steps before a geometric check caught it.
**Bead count is not geometry.** The remedy is what the original build already did for its own
duplex (`dna/em.mdp`, `dna/check.tpr`): minimise the bare duplex until the base-pair restraints
zip the strands together, and verify bond lengths before use.

A corollary worth stating: an intermediate check that can pass for the wrong reason is worse
than no check, because it licenses everything downstream. The count check did exactly that.
