# docs

Project-level narrative documents.

| File | What it is |
|---|---|
| `project_brief.pdf` | The full scientific narrative: rationale, results, and stated limitations. The best single entry point for a reader who wants the story rather than the data |
| `project_brief.md` | Markdown source of the above |
| `project_brief.html` | HTML rendering |
| `figures/` | Figures used in the brief |

## Related documents at the repository root

| File | What it is |
|---|---|
| `METHODS_GUIDE.md` | How each computational method works, how to read its output, and where it fails |
| `GLOSSARY.md` | Terminology, grouped by the task in which it arises |
| `methods_references.md` | Tool versions, force fields, database accessions and citations |
| `DRYLAB_DELIVERABLES_EN.md` | Bench-facing deliverables, English |
| `PARADOTEA_DRYLAB_EL.md` | Bench-facing deliverables, Greek |

The brief predates the later engineering cycles. Where it disagrees with a cycle document
in `06_engineering_cycles/`, the cycle document is authoritative, check
`git log -1 --format=%ad -- <file>` on both.
