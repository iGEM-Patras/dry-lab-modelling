# Results

This page reports what we established, what we failed to establish, and which claims are
still waiting on the bench. Results from the wet lab that had not returned at the time of
writing are marked **pending** rather than anticipated.

## 1 · Constructs designed and verified

**Four bicistronic constructs** were designed in silico as a two-by-two comparison of
linker strategy (IRES vs P2A) against reporter orientation, and sequence-verified by
alignment before synthesis.

| | |
|---|---|
| cassettes carrying the engineered payload | 7 × `YGGFEVVG` |
| carboxy-terminal product | `YGGFEVVGRF` (a decapeptide, preserved by tag placement) |
| purification tag | His₆ + GS linker, positioned not to disrupt processing |

Two rounds with the synthesis vendor were needed. The first ordering-ready set was rejected,
and the diagnosis **inverted our working assumption**: the fault was not in the recoded
payload but in two terminal flanking sequences that were exact reverse complements of each
other: a defect inherited from existing lab files and carried forward untested. We recorded
it as our own error, and the rule it produced: *inherited sequence is still untested
sequence.*

We then reverse-engineered the vendor's scoring from two rejection reports, **pre-registered
predicted scores for the corrected set**, and queried the vendor. Most predicted scores were
exact. The one miss revealed a secondary-structure rule our model never encoded, and it
overturned an earlier prediction we had scored as confirmed.

## 2 · Two parts submitted to the Registry

| part | length | status |
|---|---|---|
| basic: engineered PENK cassette | **867 bp** | clean for RFC10, RFC1000 and every Type IIS site after **8 silent changes**, protein byte-identical |
| composite: Kozak + basic part + IRES + mEGFP | **2,164 bp** | clean on both standards **without modification** |

The composite **contains the basic part verbatim**, so the relationship is verifiable with a
single search and the two read as one coherent submission. Both are designed sequences: the
DNA in our freezer is the His-tagged, differently codon-optimised construct, so bench
characterisation supports them by close correspondence rather than identity. We state this
on the part pages rather than leaving a judge to find it.

## 3 · The silencing arm

From **206 duplex candidates** against the neprilysin transcript, two were selected and
ordered. The selection survived four successive wet-lab objections, each resolved by
measurement rather than argument, including one round where the candidate set under
discussion proved to be from an entirely different gene, established by mapping it at a
constant offset and confirming by translation.

One error of ours is recorded in full: a frame offset meant we had been reading the efficacy
score of a **neighbouring candidate**. It invalidated two published claims, which we
corrected immediately and told the team to hold the order.

## 4 · Selectivity: the central question, unresolved

This is the project's primary pharmacological hypothesis, and our computational methods
could not settle it.

> **+1.23 ± 1.76 kcal/mol** δ-over-μ (≈7×): nominally δ-preferring, **not statistically
> separable from no preference**, and not separable from native Met-enkephalin.

That is the project's best calibrated estimate, from a model validated against 13 published
reference opioids (r = 0.805, signs correct on 12 of 13). Everything we did afterwards tried
to narrow that interval, and the interval is set by the accuracy floor of the available
methods, not by effort.

**Seven computational routes were attempted. Five of our own methods are recorded as
falsified against the public record**, each with its pre-registration and its verdict
committed to version control before the test ran:

| route | why it failed |
|---|---|
| co-folding confidence as a selectivity proxy | falsified against reference compounds |
| docking + physics rescoring | falsified |
| machine-learning affinity prediction | reported error exceeds the effect |
| alchemical free energy, original ladder | control failed; overlap diagnosed as the cause |
| alchemical free energy, re-spaced ladder | overlap **fixed**; reproducibility failed |
| residue-mutation free energy | blocked on tooling, and its published RMSE (1.61 kcal/mol) exceeds the effect (0.81) |
| conformational-constraint descriptor | control gate failed; trajectories not converged |

Two general lessons rule out classes rather than instances: anything anchored to published
affinities inherits a between-source disagreement larger than the effect, and anything
computing selectivity as a difference of two large absolute quantities accumulates
correlated bias.

**δ-preference remains a design goal, not a demonstrated result.** The functional cAMP assay
measures it directly and is subject to none of these constraints.

## 5 · Safety evidence

A δ-agonist seizure liability was raised and assessed against the primary literature across
twelve references. The concern **does not survive as a class claim**, and the strongest
counter-evidence is a gene-therapy vector expressing native preproenkephalin that completed
Phase 1 in our exact indication. Four gaps remain and are stated on the part pages: that
vector expressed the *native* precursor where ours is engineered, and was delivered
peripherally where ours is intranasal.

## 6 · Pending

| | |
|---|---|
| transfection: peptide produced and secreted | **pending** |
| quantitative expression yield (the dose model's only required input) | **pending** |
| neprilysin knockdown by qPCR | **pending** |
| δ/μ functional potency by cAMP | **pending** |
| intranasal dose model | blocked on the expression yield above |
