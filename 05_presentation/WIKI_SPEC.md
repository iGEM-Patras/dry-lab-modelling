# What each wiki page should say

> **Revised 16 Oct 2026, after reading the team's own wiki texts.** An earlier version of
> this document said the Description page was unwritten and treated several pages as gaps.
> That was wrong: the team has `DESCRIPTION` at 2,519 words, `EXPERIMENTS` at 5,873,
> `SAFETY` at 1,918 and `ENGINEERING` at 2,451, plus Contribution, Integrated Human
> Practices, Inclusivity and Entrepreneurship. The wiki is largely written. What follows is
> corrected to say where the dry lab adds something and where it should stay out of the way.

## Where the dry lab actually adds something

| page | who owns it | dry-lab contribution |
|---|---|---|
| Description | team, written | none needed |
| Engineering | wet lab, written | `WIKI_ENGINEERING.md` is a presentation layer over their four cycles, same cycles in the same order, with descriptive titles added because 4 of 4 benchmarked teams that number cycles also title them |
| Experiments | wet lab, written | none needed |
| Safety | wet lab, written | `WIKI_SAFETY.md` is an insert, not a replacement. Their section covers the lab and the delivery device and contains no mention of seizure liability, anti-PEG or MHC immunogenicity |
| **Model** | **dry lab** | `WIKI_MODEL.md`. No Model section exists in the team's documents, and this is the Best Model submission |
| Results / Tests | open | the team's `RESULTS` section is empty and their build notes rename it **Tests**. `WIKI_RESULTS.md` carries the computational record; the bench rows are still pending |

## House style, measured from the team's own documents

Rather than guess, these were measured from `WET.docx` and the Contribution page.

| | team | target |
|---|---|---|
| mean sentence | 20.4 to 21.0 words | match it |
| words in bold | 2.0 % to 6.9 % | stay inside |
| bold span length | median 2 words, 79 % at 4 or fewer, 90th pct 6 | emphasise terms, numbers and verdicts, never clauses |
| tables | yes, 8 in `WET.docx`, 3 to 5 rows each | small and frequent beats large and rare |
| voice | first person plural throughout | "we found", never "the team found" |

The Human Practices register is different again: flowing narrative, longer paragraphs, the
reasoning explained conversationally. Technical pages are tighter. Both are first person.


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

## Results, to be renamed Tests

**Status: draft exists** (`WIKI_RESULTS.md`), **needs the wet lab's data.** The team's build
notes rename this page **Tests**, and their own `RESULTS` section is currently empty.

The convention is Problem to evidence to limits. What this page can carry now is the
computational record; what it cannot carry is the bench. It should state plainly which rows
are predictions awaiting measurement, and it should not promote a prediction to a result by
putting it in a table that looks like data.

## Description

**Status: written by the team, 2,519 words.** No dry-lab action. The structure below is
retained only as a record of the convention it already follows.

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

**Status: written.** `WIKI_SAFETY.md`.

Five sections: organisms and containment, the seizure question, the carrier, the product,
and what remains unresolved. One block is marked **to be completed by the wet lab**, the
institutional biosafety level, committee approval reference and waste handling, because
those are facility facts the dry lab cannot supply.

`DELTA_SEIZURE_SAFETY.md` already carries 12 references assessed in both directions, four
caveats, and a gene-therapy precedent in the same indication. The anti-PEG assessment adds
carrier immunogenicity. Both should be stated with their gaps intact: the precedent expressed
the **native** precursor where ours is engineered, and it was delivered peripherally where
ours is intranasal.

## Parts

**Status: both entries written.** `09_registry_parts/REGISTRY_DESIGN_ENTRY.md` for the basic
part and `09_registry_parts/REGISTRY_COMPOSITE_ENTRY.md` for the composite.

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
