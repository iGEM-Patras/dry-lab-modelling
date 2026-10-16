# How 2025 teams structure their Engineering page

**Read 15 Oct 2026 from twelve live 2025 team wikis. Sampling limitation stated first.**

## What I could not do

**I could not filter this sample to gold-medal or Best Wiki winners.** iGEM publishes no
public awards or teams API, and the competition results pages are a client-rendered
application that serves the same 3,487-byte shell for every path, including its own
`/api/` routes. The parts registry API carries no team field either.

So this is **twelve 2025 team Engineering pages that are reachable and substantial**
(2,657 to 30,004 words), not an award-filtered sample. Treat it as evidence of general
convention, not of what wins.

## What the pages actually do

| finding | count |
|---|---|
| page lives at `/engineering/` | **12 of 12** |
| page lives at `/engineering-success/` | **0 of 12** |
| literal "Engineering Success" heading | **1 of 12** (XMU-China) |
| Design/Build/Test/Learn as explicit subheadings | **9 of 12** |
| present numbered cycles at all | 4 of 12 |
| of those, cycles carry a DESCRIPTIVE title not a bare number | **4 of 4** |

Cycle counts among the four teams that number them: **2, 8, 8, 10** (median 8).

## The dominant pattern

Two teams show it most clearly. XMU-China:

```
Engineering Success
  Overview
  Part 1: Engineering LMT signal peptide for improving secretion
    Cycle 1: Identifying sequence features of LMT signal peptide
      Design and Build / Test / Learn
    Cycle 2: Enhancing the hydrophobicity of the H-region
      Design / Build / Test / Learn
```

ETH-Zurich groups the same way under a subsystem ("Bioreactor Design"), with
Goal / Design / Build / Learn beneath each named cycle.

Teams with no numbered cycles are not ignoring the criterion: Heidelberg carries **360**
DBTL subheadings and Tsinghua 84, organised by workstream rather than by a flat series.
Cambridge organises purely by experiment (Extraction, Gel Optimisation, Isopropanol) with
no DBTL labels at all.

## What this says about four cycles

**Four is not too many. It is below the median of teams that number cycles.** The concern
that prompted this check was the wrong variable: the problem with the earlier draft was
never the count, it was that seventeen of nineteen cycles were dry-lab modelling on a page
judges read as the wet lab's engineering record.

Concretely, the current Epione page already matches convention on every measured axis:
four cycles with descriptive titles (convention: 4 of 4 use titles), DBTL as explicit
subheadings (9 of 12), at `/engineering/` (12 of 12).

**Two changes worth making**, both small:

1. Add an **Overview** at the top. XMU-China, Marburg and Patras 2025 all open with one,
   and it is where a judge decides whether to keep reading.
2. **Do not rename the page "Engineering Success."** Only one of twelve does. The
   convention is a page titled Engineering whose content demonstrates the success.

## One finding about Patras 2025

The team's own 2025 Engineering page is **267 words with six headings**, and it lists
**"4th engineering cycle" before "1st Engineering Cycle"**. There is no house convention
to inherit here, and almost anything complete is an improvement.
