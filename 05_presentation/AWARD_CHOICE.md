# Which Special Award to put forward: the evidence, not the impression

**Written 10 Oct 2026, from the repository record.**

The worry is that Best Model shows only failures. The record does not support that, and the
reason is that the failures are concentrated in **one of eleven workstreams**.

## What the repository actually contains

| | |
|---|---|
| dry-lab workstreams with committed results | **11** (`01` plasmid audit through `11` wet-lab protocols) |
| engineering cycles documented | **16** |
| pre-registered gates that **PASSED** | Cycle 7 (r = 0.805, p = 0.0009, n = 13, signs 12/13), Cycle 9 (ρ = 1.000), Cycle 14 overlap (0 of 56 intervals above threshold) |
| prediction ledger | **20 scored, 10 confirmed, 10 falsified**, every one committed before its test |

## Models that changed a decision, which is what the award actually asks for

1. **Plasmid audit found a real defect** (truncated 7th enkephalin core, invisible on a gel) and **removed a construct from the build before money was spent**.
2. **Vendor synthesis rules reverse-engineered** from rejection reports, predictions pre-registered, and **all four v6 constructs accepted and ordered**.
3. **siRNA selection**: 206 candidates to 2, including a self-targeting screen against our own cassette that **no design tool performs**, because the lipoplex co-packages both cargoes.
4. **Lipid choice**: the pH-dependent DNA-binding switch motivated an ionizable lipid over a permanent cation.
5. **HEK293T cannot process proenkephalin** (PCSK1, PCSK2, SCG5 effectively absent). This changed the assay design, not just a caveat.
6. **Immunogenicity**: engineered epitope is no worse than native (1.86 % vs 1.77 %), and the **P2A junction ranks highest**, an argument for the IRES cassettes.
7. **Restriction QC**: a virtual digest predicts the exact gel, turning a model into a bench acceptance test.
8. **Registry parts**: two sequences made standard-compliant by 8 silent changes, protein byte-identical.

**The δ-selectivity thread is item nine, and it is the only one that failed.** It failed
seven times, each documented with its pre-registration and its verdict.

## The validation question, which is where teams usually lose this award

Best Model asks for experimental validation. Our wet-lab data is not back. But the modelling
**is** validated against experiment, just not our own bench:

- Cycle 7 calibrated against **13 published reference opioids** and cleared a pre-set gate.
- Cycle 9 ranked **4 peptides with published selectivity** in exact agreement (ρ = 1.000).

That is validation against measured values someone else published, which is the standard
answer to "how do you know your model works" and is stronger than an uncalibrated model with
a wet-lab number attached.

## Against the two part awards

Both **Best New Basic Part** (867 bp) and **Best New Composite Part** (2,164 bp) are clean,
standard-compliant and well documented. Both have the same weakness, and it is decisive:

> **There is no characterisation data.** The parts exist in silico. The transfection has not
> returned, and `07_invitro_penk/data/` holds one file.

A part award judged on a design with no measurement competes poorly against teams submitting
characterised parts. Best Model is the **only one of the three where the absence of bench
data is survivable**, because a model can be judged on its methodology, its decisions, and
its validation against published values.

## Recommendation

**Put Best Model forward.** Not because the parts are weak, but because the parts need a
measurement we will not have, and the model does not.

**Keep the composite part as a second General Bio Engineering entry if a slot allows.** It
costs nothing extra: the part pages are written either way, no enkephalin part exists in the
Registry for anyone to have claimed first, and the composite contains the basic part verbatim
so the two read as one coherent submission.

**One framing point for the Model page.** Lead with the decisions, not the cycles. The
sentence that does the work is: *remove the model and eight wet-lab decisions lose their
basis, including one that found a real defect in a construct we were about to build.* The
falsification ledger is the credibility behind that sentence, not the headline.
