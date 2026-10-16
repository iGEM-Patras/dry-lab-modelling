# What each wiki page should say

Derived on 16 Oct 2026 from the measured structure of 2025 team wikis, not from
recollection. Twelve Engineering pages and twenty-one Model, Description and Results pages
were read directly from `2025.igem.wiki`.

**Sampling limitation, stated first.** These pages could not be filtered to gold-medal or
Best Wiki winners: iGEM publishes no public awards or teams API, and the results pages are
a client-rendered application that returns the same 3,487-byte shell for every path,
including its own `/api/` routes. This is evidence of **convention**, not of what wins.

---

## The conventions that are near-universal

| | measured |
|---|---|
| Engineering page lives at `/engineering/` | 12 of 12 |
| Engineering page at `/engineering-success/` | 0 of 12 |
| literal "Engineering Success" as a heading | 1 of 12 |
| Design/Build/Test/Learn as explicit subheadings | 9 of 12 |
| cycles given **descriptive titles**, not bare numbers | 4 of 4 teams that number them |

Cycle counts among teams that number them: **2, 8, 8, 10**. Four is below the median, so the
question is never "do we have enough cycles" but "is each one a real Learn step".

Teams with no numbered cycles are not ignoring the criterion. Heidelberg carries **360** DBTL
subheadings organised by workstream; Cambridge organises purely by experiment with no DBTL
labels at all.

---

## Engineering

**Status: written.** `WIKI_ENGINEERING.md`.

Four cycles, in the wet lab's own numbering and its own `Re-Design / Re-Build / Re-Test /
Re-Learn` labels, each with a descriptive title. An Overview table opens the page, which
XMU-China, Marburg and Patras 2025 all do.

**The rule this page follows:** it is the **wet lab's** record. Dry-lab work appears inside
the relevant cycles as support, never as a cycle of its own. An Engineering page carrying
seventeen modelling cycles tells a judge the team's engineering *is* modelling.

**Its strongest content is the failures**, and they should not be softened:

- two coding sequences back to back translate as one fused protein, caught in silico before
  any DNA was ordered
- size exclusion cannot isolate a 30 kDa precursor from host proteins of the same size, and
  fixing it turned a purification decision into a **construct** decision
- the cobalt that carboxypeptidase E requires **inhibits** the convertase that must act
  first, found on paper before a single reaction was set up
- the first-generation constructs carried **no affinity tag at all**, recorded by the wet lab
  against itself

## Model

**Status: written.** `WIKI_MODEL.md`.

The strong 2025 Model pages share four features that a results-only page lacks. All four are
now present:

| feature | seen in | our section |
|---|---|---|
| assumptions stated **before** results | Cambridge "Our Assumptions", Tsinghua "Pre-assumptions" | §2, and three of five are marked falsified |
| explicit guidance given to the wet lab | Tsinghua "Model Conclusions and Guidance for Wet Lab Experiments" | §7, eight bench decisions traced to a cycle |
| complete parameter and variable list | Tsinghua "Complete List of Variables, Parameters" | §8, with where each threshold came from |
| code published and reusable | Tsinghua "Complete MATLAB code", KCL "Take our work further" | §9 |

**What makes this page defensible rather than just long:** calibration comes before
prediction, every number carries the interval that bounds it, and where a method failed its
own control the page says so instead of quoting what it produced. The free-energy campaign
and cycle 17 are both reported as failures.

## Results

**Status: draft exists** (`WIKI_RESULTS.md`), **needs the wet lab's data.**

The convention is Problem to evidence to limits. What this page can carry now is the
computational record; what it cannot carry is the bench. It should state plainly which rows
are predictions awaiting measurement, and it should not promote a prediction to a result by
putting it in a table that looks like data.

## Description

**Status: not written. This is team copy, not dry lab.**

The convention is tight and worth following exactly. Across KCL-UK, Tsinghua and XMU-China
the order is the same:

1. **The problem**, in human terms before biological ones
2. **Current treatments and why they fall short**
3. **The breakthrough**, the one idea that is new
4. **The project**, the system design
5. **Safety / biosafety**
6. **The future**, broader application

For Epione that maps to: chronic cancer pain and the undertreatment gap, why systemic opioids
and intrathecal pumps fail, the local-production idea with a degradation brake, the
bicistronic construct plus the silencing arm plus intranasal delivery, the seizure-liability
assessment, and cargo-agnostic delivery.

## Safety

**Status: content exists, page not written.**

`DELTA_SEIZURE_SAFETY.md` already carries 12 references assessed in both directions, four
caveats, and a gene-therapy precedent in the same indication. The anti-PEG assessment adds
carrier immunogenicity. Both should be stated with their gaps intact: the precedent expressed
the **native** precursor where ours is engineered, and it was delivered peripherally where
ours is intranasal.

## Parts

**Status: entry written** (`09_registry_parts/REGISTRY_DESIGN_ENTRY.md`).

One entry, Type **Design**, because the submission form takes one Type per entry. No
Characterisation entry should be filed while everything available is predicted rather than
measured; the form defines that type as data on how the part behaves, and filing modelling
there is the easiest thing for a judge to catch.

---

## Two things to carry across every page

**Voice.** Wiki pages are first person, "we calibrated", "we withdrew". Every 2025 team wiki
examined uses team voice. The **repository** is the opposite: third person and descriptive.
These are different documents with different readers.

**Consistency with the repo.** The wiki and the repository must not disagree on selectivity,
enzymes, delivery route or cycle count. The repository is the auditable record; if a wiki
sentence cannot be traced to a file in it, either the file is missing or the sentence is
wrong.
