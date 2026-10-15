# DeorphaNN, revised after reading the source: one blocker dissolves

**15 Oct 2026. This CORRECTS my assessment of three days ago, which called Arpeggio-via-Docker
a blocker. Having read `deorphann/graph.py` rather than the README, it is not one.**

---

## What I got wrong

I wrote that the pipeline needs "Arpeggio contacts via Docker, which this cluster does not
permit", and treated that as fatal. That inference came from the README's preprocessing
list. The code says something different.

## What Arpeggio actually contributes: topology only

`load_contacts()` reads the Arpeggio TSV, then:

1. keeps only `INTER` rows (inter-chain),
2. **drops** the `Proximal`, `Clash`, `Covalent`, `VdW Clash` and `VdW` columns,
3. keeps a row if **any** remaining flag is 1 (Hydrogen Bond, Weak Hydrogen Bond, Halogen,
   Ionic, Metal Complex, Aromatic, Hydrophobic, Carbonyl, Polar, Weak Polar),
4. parses chain and residue number out of the atom strings,
5. offsets chain-B residues by the GPCR length, **drops duplicate residue pairs**,
6. returns a bare `(2, N)` integer array of residue indices.

**Every chemical label is discarded.** The ten interaction types serve only as a boolean
filter deciding whether a residue pair counts as an edge. Nothing about *which* interaction
reaches the model.

The edge *features* come from somewhere else entirely:

```python
edge_attrs = edge_features[nt, ns, :]          # 128-dim, from the AlphaFold pair representation
```

So the graph is: **nodes = pooled pair-representation vectors, edges = residue pairs in
contact, edge features = pair-representation slices.** Arpeggio supplies the adjacency and
nothing more.

**An adjacency matrix over an interface is a geometric calculation.** Biopython computes it
without Docker, without Arpeggio, in a few lines. The only question is how closely a
distance-and-chemistry criterion reproduces Arpeggio's `INTER` set, and that is testable.

## What remains genuinely hard

**AlphaFold-Multimer with the pair-representation tensor saved.** `process_pair_reps.py`
expects `.npy` files whose names contain `pair_repr`, each an `(L, L, 128)` array, which it
averages across models before pooling. 128 channels is the standard AlphaFold2 pair
dimension, so this is an ordinary AF2 internal rather than anything exotic, but ColabFold
does not write it by default. A patched run is needed.

That is the one real piece of engineering left.

## And step 1 is already done for us

The authors ship finished active-state templates for all three human opioid receptors
(`OPRD-HUMANactive.pdb`, `OPRM-HUMANactive.pdb`, `OPRK-HUMANactive.pdb`), so
`huhlim/alphafold-multistate` need not be run at all. That removes the heaviest GPU step.

## Revised pipeline status

| step | earlier verdict | after reading the source |
|---|---|---|
| 1. active-state GPCR template | needs alphafold-multistate | **already shipped for OPRD and OPRM** |
| 2. AF-Multimer + pair-rep dump | blocker | **the one real task**: patch ColabFold to save the pair tensor |
| 3. pool pair reps | fine | fine, script provided |
| 4. contacts | **blocker (Docker)** | **not a blocker**: reimplement as a geometric contact map |
| 5. score | fine | fine, CPU, 10-model ensemble |

## The validation loop, which is the thing to insist on

The authors ship 195 pair representations, 22,035 relaxed PDBs and 19 score tables. That is
everything needed to check our own contact reimplementation **without running AlphaFold at
all**:

1. take a pair where they provide both the pair representation and the relaxed PDB,
2. compute contacts with our geometric method instead of Arpeggio,
3. score with their pretrained ensemble,
4. **compare against their published score for that pair.**

If our contacts reproduce their score, the Arpeggio substitution is validated and only step 2
remains. If they do not, we learn that before spending any GPU time.

**This is a few hours of work and it uses no cluster time.** It is the correct first
milestone, and it is cheap enough to be worth doing even under deadline.

## What has not changed

- **DeorphaNN separates agonist from non-agonist.** Our question is delta-over-mu between
  receptors sharing 18 of 29 orthosteric pocket residues, outside its demonstrated scope.
- **The calibration panel must run first.** If it cannot rank 13 compounds of known
  delta/mu preference, it cannot rank ours.
- **It never produces a kcal/mol value**, so it cannot replace the cAMP assay.

The engineering is more tractable than I said. The scientific ceiling is exactly where it was.
