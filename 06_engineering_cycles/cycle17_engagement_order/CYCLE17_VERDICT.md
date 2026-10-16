# Cycle 17 verdict: G1 passes, G2 FAILS, G3 not scored

**16 Oct 2026. Gates committed in `cycle17_prereg.json` before any simulation ran.**

---

## The gates, scored in the order they were registered

| gate | question | outcome |
|---|---|---|
| **G1** | can blind docking recover the deltorphin crystal pose without the membrane term? | **PASS**, 3.41 A, 4 of 32 models under 5 A, under-sampled control recovered nothing |
| **G2** | does the control reproduce the published address-first productivity asymmetry? | **FAIL**, OR 1.20, p = 0.51 at the full n = 150 |
| **G3** | does the engineered payload engage in the same order? | **NOT SCORED**, as the pre-registration requires |

## G2 in detail: the effect decayed as evidence accumulated

| n | OR | p | address-first | message-first |
|---|---|---|---|---|
| 80 | 2.00 | 0.46 | 11.1 % | 5.9 % |
| 100 | 0.83 | 0.75 | 11.5 % | 13.6 % |
| 120 | 1.07 | 0.61 | 11.8 % | 11.1 % |
| 140 | 1.09 | 0.58 | 13.1 % | 12.1 % |
| **150** | **1.20** | **0.51** | **13.8 %** | **11.8 %** |

The campaign ran to its full pre-registered size, 15 seeds and 150 trajectories, so no
appeal to truncation or sample size is available. The last four increments bounced between
0.83 and 1.20 with no trend: noise around unity.

Published reference for beta-endorphin at the mu receptor: **18.8 % versus 5.0 %, p < 0.001**,
corresponding to an odds ratio near **4.4**.

Our control converges on **1.20**. Address-first and message-first trajectories reach a
native-like pose at indistinguishable rates.

**Power is 0.74** for the published effect, so this is not simply an underpowered null. A
real effect of the published magnitude would have been detected roughly three times in four,
and the point estimate is sitting on 1.0 rather than somewhere between.

## A premature claim of mine, corrected

At n = 130 I reported the estimate as "stable over the last 90 trajectories" and predicted
the remaining seeds would not change the verdict. **Ten more trajectories moved the odds
ratio from 1.41 to 1.09.** The direction of my conclusion held, but the stability claim was
wrong when I made it, and I should have said the estimate was still moving.

The final seed moved it again, 1.09 to 1.20. Checking rather than assuming was therefore the
right call both times; it simply did not change the verdict on the second occasion.

## G3 is not scored, and the engineered arm looks better

This is the part worth being explicit about. The engineered arm reached 50 trajectories and
its numbers are **18.2 % versus 7.4 %, OR 2.78** , larger than the control and in the
published direction.

It is not reported as a result, because the instrument failed its calibration. A measurement
from a method that could not detect the effect on a positive control is not weaker evidence,
it is not evidence. That is precisely the circumstance the gate ordering was registered to
handle, and the fact that the unscored number happens to favour our own construct is the
reason the ordering was written down in advance rather than decided now.

## What can be claimed

**The docking machinery works.** G1 is a clean, controlled positive: blind docking recovered
a crystallographic pose at 3.41 A while a deliberately under-sampled run of the same pipeline
recovered nothing, which rules out a selection artefact.

**The engagement-order analysis built on it did not validate.** No claim is made about the
order in which `YGGFEVVG` engages the delta-opioid receptor.

## Candidate explanations, none tested

- The published analysis used a membrane term this installation does not provide, one of the
  four deviations declared before the run.
- CABS cannot represent deltorphin's D-alanine or its C-terminal amide, so the control is
  modelled stripped of two features the literature credits for its rigidity. This was flagged
  as the most damaging deviation at the outset.
- The published work studied a different peptide at a different receptor, and the asymmetry
  may not generalise.
- Coarse-grained replica-exchange sampling may not preserve the approach-path information the
  measure depends on.

Distinguishing these is a season's work, not five days'.

## A confound that would have produced a false finding

The two arms split very differently by engagement class: deltorphin is address-first in 76 %
of trajectories, the engineered peptide in 37 %. That looks like a dramatic behavioural
difference.

**It is at least partly geometric.** `YGGFEVVG` has a four-residue message domain against
deltorphin's three, so it carries more atoms and more chance of first contact for no
biological reason. Between-arm class splits are **not comparable**. Within an arm the
comparison stands, because the same peptide is on both sides.

## Two bugs in the analysis, fixed before any number above was produced

1. **The chain split silently returned the wrong molecule.** The crystal reference models
   deltorphin as eight residues, the NH2 amide cap being its own, while CABS simulates seven.
   No chain matched, and a fallback meant to tolerate rewritten chain IDs returned the last
   seven **receptor** residues as the peptide. Every RMSD was measured against receptor and
   nothing in the output looked wrong. The split is now strict and raises.
2. **Productivity was read from each replica's final frame.** CABS derives poses by
   clustering, so a final frame is wherever that replica stopped. All 40 trajectories scored
   28 to 46 A while clustered models from the same run reached 3.41 A, which is what exposed
   it. Productivity is now the minimum RMSD reached at any frame.

## Cost

26 simulations at roughly 3.2 h on 4 cores each, about 333 core-hours, plus the 4 that
survived the earlier run-clock error. Spent on a question that returned a null, which is
what the budget was authorised for.
