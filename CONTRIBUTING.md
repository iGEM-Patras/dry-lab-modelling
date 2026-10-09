# Contributing

## The one rule that is not negotiable

**Predictions are committed and pushed before the test that could falsify them.**

Every engineering cycle in `06_engineering_cycles/` has a `*_DESIGN.md` containing its
hypothesis, its numeric predictions, and a **gate** (a pass/fail threshold fixed in
advance), pushed before the corresponding run starts. The matching `*_RESULTS.md` scores
every prediction as confirmed, falsified, or unresolved.

This is what makes the commit history evidence rather than narrative. A prediction added
or edited after seeing its result destroys that property for the whole repository, not
just for one cycle. If a prediction turns out to have been badly specified, say so in the
results document: do not revise the design document.

## Reporting results

- **Score every prediction**, including the ones that failed. Four methods in this
  repository are recorded as rejected; that is deliberate.
- **"Unresolved" is a distinct outcome from "falsified".** If an experiment could not
  settle a prediction either way, record it as unresolved and say why.
- **Never report a bound-state binding energy without its residency fraction.** The merge
  tooling refuses to emit one without the other; do not work around it.
- **Quote numbers from the saved file, not from memory or from a chat log.** Read the
  artifact back before writing a value into a document.

## Code

- Analysis scripts live in the relevant cycle's `scripts/` directory.
- Prefer a check that asserts the *value* you care about over one that asserts a step ran.
  Several failures in this project's history were checks that passed because a command
  exited zero while producing nothing.
- Validate a parser against a fixture whose content you control, not against live data
  that is still changing.
- If you add a dependency, record it in `methods_references.md` with its version.

## Data and file conventions

- Committed `.csv` and `.xvg` outputs are the reproduction path: analyses and figures
  should be regenerable from the repository without re-running any simulation.
- Large binary trajectories are not committed. Numeric outputs derived from them are.
- Cite reference sequences and compounds by stable accession (UniProt, ChEMBL, PDB)
  rather than by name.

## Licensing of contributions

Documentation, data and figures are contributed under CC BY 4.0; code under the MIT
Licence. See `LICENSE` and `LICENSE-CODE`.
