# Engineering Cycles, δ-selective enkephalin payload

This directory documents the iterative **Design → Build → Test → Learn (DBTL)** engineering
of the analgesic peptide payload expressed from the engineered PENK therapy plasmid.

## Why iterate on the peptide at all?

The therapy delivers a proenkephalin (PENK) cassette so that transduced cells secrete
enkephalin locally, plus an siRNA that silences neprilysin (MME) so the secreted peptide
is not immediately degraded. Enkephalin acts at two opioid receptors:

| Receptor | Gene | Consequence of agonism |
|---|---|---|
| **δ (DOR)** | `OPRD1` | analgesia, anxiolytic; **much lower respiratory-depression and dependence liability** |
| **μ (MOR)** | `OPRM1` | analgesia, but also respiratory depression, constipation, tolerance, dependence |

Native Met-enkephalin (`YGGFM`) is only weakly δ-preferring. **Biasing the payload toward
δ is therefore a safety-driven design goal**, not a cosmetic one: it retains analgesia while
reducing the μ-mediated adverse-effect profile that makes conventional opioids dangerous.

## Cycle index

| Cycle | Design concept | Payload | Status | Result |
|---|---|---|---|---|
| **1** | Graft the **deltorphin II address** onto the enkephalin message | `YGGFEVVG` | ✅ complete | Directionally δ-ward; **quantitative claim withdrawn** (see correction) |
| **2** | Enhance address hydrophobicity / anionic residue (literature-guided) | 5 variants | ✅ complete | **Primary hypothesis falsified**, 4 of 5 predictions wrong; V4/V5 retained |
| **3a** | Validate pose convergence as a selectivity metric | *no new sequences* | ✅ complete | **H3a rejected**, does not replicate; metric retired |
| **3b** | ~~Combine Cycle 2's two independent wins~~ → **change the observable**: explicit-solvent MD + MM-GBSA ΔΔG in kcal/mol | controls + 2 survivors, acid & amide | 📋 pre-registered, gated | Original premise **withdrawn** (V5's win within noise at n=20). Stage 1 must calibrate on experimental controls before the panel is run |
| **4** | **Can the cassette be manufactured?** Iteratively reverse-engineer the vendor's synthesis-complexity rules from its rejection reports | 4 constructs × 3 rounds (v4→v5→v6) | ✅ complete | v4 **denied 23.8** (inverted-repeat flanks, inherited from wet-lab files); v5 fixed 3 of 4; **v6 accepted, all four constructs ordered** |
| **5** | What should the first transfection actually produce? | *no new sequences* | 📋 pre-registered | Five falsifiable predictions committed before the bench runs; awaiting wet-lab data |
| **7** | Does the co-folding **affinity head** predict δ/μ selectivity, tested against published drugs? | *no new sequences* | ✅ **gate PASSED** | n=13, r = 0.805, p = 0.0009, signs correct 12/13. First calibrated number: `YGGFEVVG` **+1.23 ± 1.76 kcal/mol** (~7× δ), not separable from native |
| **8** | Rigorous **free-energy (TI)** ΔΔG for δ vs μ | controls + target | ✅ complete · **gate FAILED** | Control on native Met-enkephalin gives **−3.12 and +5.41 kcal/mol** across replicates, opposite signs from a seed change, so **no value is quoted for `YGGFEVVG`**. Diagnosed: 20–21 of 25 λ-intervals poorly overlapping. Graft shortcut **rejected by measurement** (`GRAFT_ROUTE_REJECTED.md`) |
| **9** | Re-test **pose convergence**, this time calibrated against experiment | *no new sequences* | ✅ **gate PASSED** | ρ = 1.000, ranks 4 reference peptides in exact agreement with published selectivity. Rehabilitates the metric Cycle 3a retired |
| **10** | Does the lipoplex **co-package** the plasmid and the siRNA, or do they compete? | *no new sequences* | ⏹ **abandoned, no result** | Coarse-grained build; a 21-bp surrogate duplex derived and verified against the reference build's own base-pair rule. Replicate-2 build failure documented (`REPLICATE2_FAILURE.md`). **`CYCLE10_DESIGN.md` records that the systems were never completed, no production run was started and no result exists.** Listed here as abandoned rather than open |
| **11** | Can a **QSAR** learn δ/μ selectivity from published affinities? | *no new sequences* | ✅ complete · **gates FAILED** | r = 0.77 in aggregate, but the prediction is a nearest-neighbour lookup and flips sign when neighbours are removed. Chirality objection tested and answered in an amendment, refit indistinguishable, so the conclusion stands but was **narrowed** to fingerprint methods |
| **12** | Is the co-folded pose that fed Cycle 8 **independently reproducible**? | *no new sequences* | ✅ complete · **gate FAILED** | Peptide-specific docking reproduces the met-enkephalin control at **1.63 Å** (inside the 2.5 Å gate) but reaches only 3.11 Å for `YGGFEVVG`, so the threshold is achievable and the payload pose is **not corroborated** in either receptor |
| **12b** | Does the pose disagree with **experimental** structures? *(was labelled Cycle 13)* | *no new sequences* | ✅ complete · **gates FAILED** | Against deltorphin–DOR (8F7S) and β-endorphin–MOR (8F7Q): 5.20 Å and 2.83 Å. Names a **specific missing interaction**, the address Glu makes a salt bridge to Lys214 (3.06 Å) in the experimental δ complex and **none** in ours |
| **8b** | Re-run the free-energy ladder **spaced for uniform overlap**, replicates from separate equilibrations *(was labelled Cycle 14)* | *no new sequences* | ✅ complete · **gates FAILED** | 27 → **57 windows** by equal thermodynamic length; gates committed before any window ran. **Outcome: the diagnosis was correct and the fix worked.** Overlap PASSED, 0 of 56 intervals above threshold against 20 to 21 of 25 on the old ladder. Reproducibility FAILED: **+0.72 ± 3.13** vs **+14.47 ± 3.28 kcal/mol**, a 13.75 spread against a combined error of 4.53. Doubling the windows doubled the accumulating terms, and the two legs drifted in opposite directions so the biases added |
| **15** | Mutate the **receptor** instead of decoupling the ligand twice, so the large absolute quantity is never formed | *no new sequences* | ❌ **blocked, then ruled out** | Hybrid residue built and charge-verified atom by atom (qA 13.000 → qB 14.000). Blocked on topology-format incompatibility in both directions. The resolution check we should have run first settles it regardless: the purpose-built method reports RMSE **1.61 kcal/mol** against an effect of **0.81**, recorded as our own error |
| **16** | Does the payload carry the **conformational constraint** newer literature attributes selectivity to, rather than only the address sequence? | *no new sequences* | ❌ **control gate FAILED** | 40 trajectories, 4 control peptides × 2 receptors × 5 replicates, 20 ns matched. A constrained peptide was indistinguishable from a flexible one (1.000 vs 0.999 on DOR) and the >1500× selective peptide was the **least** turn-like. Five replicates of one system span 0.00 to 1.00, so 20 ns does not re-equilibrate a bound backbone. Our payload was **not scored** |
| **17** | Does the payload engage the receptor in the same DOMAIN ORDER as deltorphin, whose address it carries? Lewandowski-style analysis on a crystal reference (PDB 8F7S) | *no new sequences* | ✅ complete · **G1 PASS, G2 FAIL, G3 unscored.** Blind docking recovered the crystal pose at **3.41 A** while an under-sampled control recovered nothing, so the protocol validates. But over the full 150-trajectory campaign the control did **not** reproduce the published engagement asymmetry: OR **1.20**, p 0.51 at 0.74 power, against a published OR near 4.4. G3 was therefore never scored. The engineered arm's partial data looked favourable at OR **2.78** and peaked at **6.75**; run to full size it collapsed to **1.07**, indistinguishable from the control and from no effect. Reporting the interim would have required a retraction |


> **On the gaps in this numbering.** There is no cycle 6, 13 or 14 directory. Cycle 13
> was re-labelled **12b** and Cycle 14 was re-labelled **8b**, because under this project's own
> rule a new cycle requires a new Learn-to-Design edge, and both were further *rounds* of an
> existing question rather than new ones. Their directories keep the original names
> (`cycle12_pose_independence/`, `cycle14_respaced_ladder/`) so that git history stays
> continuous. Cycle 6 was never opened. The wet-lab guide uses a different numbering again,
> reconciled in [`cycle_reconciliation.csv`](cycle_reconciliation.csv).

- [`cycle1_deltorphin_chimera/CYCLE1.md`](cycle1_deltorphin_chimera/CYCLE1.md): retrospective writeup **+ correction notice**
- [`cycle2_delta_selectivity/CYCLE2_DESIGN.md`](cycle2_delta_selectivity/CYCLE2_DESIGN.md): pre-registration (committed before the runs)
- [`cycle2_delta_selectivity/CYCLE2_RESULTS.md`](cycle2_delta_selectivity/CYCLE2_RESULTS.md): results, prediction scoring, Cycle 1 correction
- [`cycle3a_convergence_metric/CYCLE3A_DESIGN.md`](cycle3a_convergence_metric/CYCLE3A_DESIGN.md): pre-registration
- [`cycle3a_convergence_metric/CYCLE3A_RESULTS.md`](cycle3a_convergence_metric/CYCLE3A_RESULTS.md): held-out replication, scorecard, recommendation
- [`cycle4_synthesizability/CYCLE4.md`](cycle4_synthesizability/CYCLE4.md): the vendor-rules cycle, with its pre-registration scored
- [`cycle5_expression_processing/CYCLE5_DESIGN.md`](cycle5_expression_processing/CYCLE5_DESIGN.md): pre-registration for the first transfection
- [`cycle7_calibration/CYCLE7_RESULTS.md`](cycle7_calibration/CYCLE7_RESULTS.md): the calibrated estimate and its three stated limits
- [`cycle8_fep/CYCLE8_DESIGN.md`](cycle8_fep/CYCLE8_DESIGN.md): protocol, measured throughput budget, gate dry-run
- [`cycle8_fep/GRAFT_ROUTE_REJECTED.md`](cycle8_fep/GRAFT_ROUTE_REJECTED.md), a negative result, including two invalid attempts of our own
- [`cycle9_convergence_metric/`](cycle9_convergence_metric/): the recalibrated metric that passed
- [`cycle8_fep/CYCLE8_ENGPENK_RESULT.md`](cycle8_fep/CYCLE8_ENGPENK_RESULT.md): the payload legs, and why no value is quoted
- [`cycle10_copackaging/CYCLE10_DESIGN.md`](cycle10_copackaging/CYCLE10_DESIGN.md): pre-registration; `REPLICATE2_FAILURE.md` is the documented build failure
- [`cycle11_selectivity_qsar/CYCLE11_RESULTS.md`](cycle11_selectivity_qsar/CYCLE11_RESULTS.md): gates, the diagnostic, **and the chirality amendment that narrowed our own conclusion**
- [`cycle11_selectivity_qsar/BINDPRED_REJECTED.md`](cycle11_selectivity_qsar/BINDPRED_REJECTED.md): four published methods assessed and rejected, each with the number that rejects it
- [`cycle12_pose_independence/CYCLE12_RESULTS.md`](cycle12_pose_independence/CYCLE12_RESULTS.md): the docking control that makes the payload's failure interpretable
- [`cycle12_pose_independence/`](cycle12_pose_independence/): also holds **12b**: `cycle13_verdict.json`, `cycle13_metrics.csv`, `cycle13_experimental.png`
- [`cycle14_respaced_ladder/`](cycle14_respaced_ladder/): **8b**: the 57-window ladder, its pre-registration, and the cost measured before committing

### Reading this index

**There is no `cycle6/` directory.** Cycle 6 was a calibration attempt at n = 4 that failed
all its gates; its data is kept in [`cycle7_calibration/data/`](cycle7_calibration/data/),
since Cycle 7 is the same experiment repeated at an adequate sample size.

**Cycle 3a rejected the pose-convergence metric and Cycle 9 accepted it.** Not a contradiction:
3a evaluated the metric without calibrating it against experimental values, 9 evaluated it
against four peptides with published selectivity. The difference is whether the metric was
anchored to experimental values before being relied on.

**Cycles are counted by their Learn→Design edge**, not by construct count: a parallel
multi-arm panel is one cycle, and only a genuinely sequential dependency splits into two.

**Two cycles were relabelled, and the directory names still carry the old numbers.**
Applying the rules stated below to the later cycles gives:

| index label | directory | why |
|---|---|---|
| **8b** | `cycle14_respaced_ladder/` | Same hypothesis and the same oracle as Cycle 8, with its design determined by Cycle 8's overlap diagnostic; the Cycle 4 rule makes that *rounds within one cycle*, not a new one |
| **12b** | files in `cycle12_pose_independence/` | Cycle 12's result determines what 12b tests against experiment; the same sequential dependency that splits Cycle 3 into 3a/3b |

Directory names were deliberately **not** renamed: they are cited in commit messages and
in the pre-registration history, and renaming them would break the audit trail that makes
the track record checkable. Where this document says 8b or 12b, look in `cycle14_…` and
`cycle12_…` respectively.

## What counts as a cycle here

A cycle is defined by its **Learn → Design edge**, not by the number of constructs it
contains. Variants that were all designed from the *same* Learn output, tested in
parallel, and interpreted against each other are **one cycle with a multi-arm panel**:
Cycle 2's five variants are controls for one another (V3 is the Asp-without-Ile control
for V4; V2 isolates β-branching from bulk in V1) and are meaningless in isolation.

Splitting a parallel panel into one "cycle" per variant would produce loops with
identical Design inputs and no Learn edges between them. That inflates cycle count while
reducing cycle depth. Conversely, Cycle 3 **is** split into 3a and 3b because 3a's
result determines what metric 3b is judged on: a genuine sequential dependency.

By the same rule, Cycle 4's three rounds (v4 → v5 → v6) are **one cycle**, not three. Each
round's design is determined by the previous round's rejection report, so they form a
sequential chain, but they share one hypothesis ("this cassette is manufacturable") and
one oracle. They are documented as rounds *within* Cycle 4 rather than as Cycles 4/5/6.

Cycle 4 is also the first **wet–dry** loop here: its Test step is an external
manufacturer's feasibility engine, not a simulation. The Learn edge crosses the
dry/wet boundary, which is what the project needs to demonstrate.

## Track record

Predictions are committed and pushed **before** the corresponding runs are launched, so
the falsification record is auditable in the git history.

| Cycle | Predictions made | Confirmed | Falsified | Pre-registration commit |
|---|---|---|---|---|
| 2 | 5 | 1 | **4** | `f2d6ade` (before job `ac2c837e`) |
| 3a | 5 | 3 | **2** (both decisive) | `ec7123d` (before job `1391bb2a`) |
| 4 (v4) | 1 | 0 | **1** | (not pre-registered; see below) |
| 4 (v5) | 4 | 3 | **1** | (not pre-registered; see below) |
| 4 (v6) | 5 | 3 | **2** | `cycle4_predictions.csv`, committed before vendor submission |

**Cumulative: 20 predictions scored, 10 confirmed, 10 falsified**, nothing pending.

v6's two falsifications are both informative. One construct scored 1.0 instead of the
predicted 0.0, from a **hairpin rule** our two-rule model of the vendor never encoded, and
that motif is structurally an inverted repeat, the same class that caused the v4 denial,
scored far more leniently when internal than when terminal. The other is P5, which we had
**initially scored as confirmed and then retracted**: it had been confirmed by inferring a
rule's absence from an aggregate verdict that would look identical under either outcome,
which violates this cycle's own rule that a prediction must name a read-out the experiment
produces either way. The original scoring is left visible beneath its correction in
`data/v6_scoring_verdict.json`.

**Scope of this table.** It counts *individual pre-registered predictions*, and those exist
for Cycles 2, 3a and 4. Cycles 7 onward were pre-registered as **pass/fail gates** rather
than itemised predictions: a different unit that cannot be summed into the rows above.
Each of those outcomes lives in its own verdict file, and the index above states each
gate's result:

| cycle | gate record |
|---|---|
| 7 | [`cycle7_calibration/data/cycle7_verdict.json`](cycle7_calibration/data/cycle7_verdict.json) |
| 8 | [`cycle8_fep/CYCLE8_GATE_VERDICT.md`](cycle8_fep/CYCLE8_GATE_VERDICT.md) |
| 11 | [`cycle11_selectivity_qsar/data/cycle11_verdict.json`](cycle11_selectivity_qsar/data/cycle11_verdict.json) |
| 12 | [`cycle12_pose_independence/data/cycle12_verdict.json`](cycle12_pose_independence/data/cycle12_verdict.json) and `cycle12_control_verdict.json` |
| 12b | [`cycle12_pose_independence/cycle13_verdict.json`](cycle12_pose_independence/cycle13_verdict.json) |
| 8b | [`cycle14_respaced_ladder/data/cycle14_prereg.json`](cycle14_respaced_ladder/data/cycle14_prereg.json) (gates committed, outcome pending) |

Cycle 4's first two rounds were **not** pre-registered: the v4 and v5 predictions were
made informally in conversation and only written down after the vendor had answered. They
are recorded in the scorecard for honesty, but they do not carry the same evidential
weight as a committed prediction and are marked as such. v6 is the first round of this
cycle to follow the project's own rule. This is itself a finding: the cheapest, fastest
oracle in the project was the one where pre-registration discipline slipped first. The two Cycle 3a falsifications
rejected the cycle's own hypothesis; the three confirmations include P5, which predicted
that our *previous* cycle's ranking was unreliable, and it was.

A high falsification rate is the intended outcome of honest pre-registration, not a
failure of the project.

## Shared method

All peptide–receptor complexes are predicted with **Boltz-2** co-folding against the
full-length human receptor (UniProt canonical sequence), under identical settings:

```
boltz predict <complex>.yaml --use_msa_server \
  --subsample_msa --num_subsampled_msa 1024 \
  --recycling_steps 3 --diffusion_samples 5 --sampling_steps 200
```

Receptor chain uses a full MSA (1024 sequences); the peptide chain uses `msa: empty`
(a 5–8-mer has no meaningful alignment). **All cycles use identical settings**, so
cross-variant comparisons are internally controlled.

### Selectivity metric

$$\Delta_{sel} = \text{ipTM}(\text{DOR complex}) - \text{ipTM}(\text{MOR complex})$$

ipTM is Boltz's predicted interface TM-score: a **confidence** measure for the
peptide–receptor interface. A larger $\Delta_{sel}$ means the model is more confident about
the δ interface than the μ interface for that same peptide.

### ⚠ Interpretation limits (read before quoting any number here)

- **ipTM is not binding affinity.** It is a structural-confidence score. It ranks and
  triages designs; it does **not** predict $K_i$, $IC_{50}$, or fold-selectivity.
- Differences of ~0.01–0.02 ipTM are near the noise floor. We therefore report
  **mean ± SD across the 5 diffusion samples** and treat only separated distributions
  as meaningful.
- Boltz sees the **unamidated, linear L-amino-acid** peptide. It cannot represent
  D-amino acids or C-terminal amidation, both of which matter for real deltorphin
  pharmacology (see Cycle 2 design notes).
- **Wet-lab radioligand competition binding at DOR vs MOR is the only real test.**
  These predictions exist to choose which 2–3 variants are worth synthesising.

## Constraint that shapes every design

The payload is **expressed from a plasmid**, so it must be encodable in DNA:
**20 standard L-amino acids only**. This rules out the classic high-selectivity
opioid-peptide tricks: D-amino acids (D-Ala²), penicillamine cyclisation (DPDPE),
N-methylation, which is why the design space here is the *address domain sequence*
rather than backbone chemistry.

One partial exception is exploited deliberately: a **C-terminal Gly is the recognition
signal for peptidylglycine α-amidating monooxygenase (PAM)** in mammalian secretory
granules, so a `...VVG` payload can be post-translationally converted to the
`...VV-NH₂` amide *in vivo* (recovering the amidation that natural deltorphins require).
The terminal Gly in every design is therefore load-bearing and must be retained.
