# What is on GitLab and what is not

**25 Oct 2026.** The public iGEM software-tools repository on GitLab holds a deliberately
reduced subset of this repository: 697 files against 738 here. This note records which 41
files are absent and why that matters for the wiki's deep links.

## Correction to commit 078e211

That commit's message states the GitLab export is "an OLDER snapshot" of this repository.
**That was wrong, and the evidence was available when it was written.** The original wording
is left in the history rather than rewritten.

A stale export would show a cutoff date: everything missing would postdate everything
present. Counting the month each file entered version control shows no such boundary.

| month added | missing from GitLab | present on GitLab |
|---|---|---|
| 2026-07 | 7 | 166 |
| 2026-08 | 1 | 56 |
| 2026-09 | 22 | 290 |
| 2026-10 | 11 | 185 |

July files are missing while 166 other July files are present. The subset was curated, not
truncated by time.

## The curation is coherent

The excluded set has a clear shape, and it is the right shape for a repository whose purpose
is to let judges reach specific technical files quickly:

- **All of `99_provenance/`**, 10 files, mostly multi-megabyte archives and session records
- **All Greek-language wet-lab documents** in `11_wetlab_protocols/gr/`, 5 files
- **Most of `05_presentation/`**, 15 files: slides, handouts, video notes, captions
- **Greek audit documents** in `08_checkable_audit/`

Presentation material, second-language duplicates and provenance archives are exactly what a
reader with limited time does not need, and excluding them makes the remaining files easier
to find. No objection to any of it.

## Three exclusions worth a second look

These are the only ones where the choice may cost something, because each is a plausible
target for a link from the wiki:

| file | why it may matter |
|---|---|
| `ATTRIBUTIONS.md` | Attributions are a judging requirement. If any wiki page links here for detail rather than carrying it inline, the link fails |
| `DELTA_SEIZURE_SAFETY.md` | The seizure-liability evidence, 12 references. A natural target for a Safety page citation |
| `docs/project_brief.pdf` | This repository's own README calls it "the best single entry point for a reader who wants the story rather than the data" |

A fourth, `11_human_practices/IHP_CEID_PROFESSOR.md`, entered version control on 17 October
and is the newest missing file. It may simply postdate the export rather than having been
excluded.

## What to check, and it is quick

Every wiki link that points into the GitLab repository should resolve. The list above is the
set of paths that exist here and not there, so any wiki link whose target appears in it will
return a 404 for a judge who clicks it. Checking means searching the wiki source for
`ATTRIBUTIONS`, `DELTA_SEIZURE`, `project_brief` and `IHP_CEID`, which is four searches.

Nothing needs changing if the wiki carries that content inline rather than linking to it.
