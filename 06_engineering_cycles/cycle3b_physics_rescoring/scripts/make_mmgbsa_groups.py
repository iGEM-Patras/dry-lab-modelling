#!/usr/bin/env python3
"""Write mmgbsa.ndx containing Receptor and Ligand groups.

index.ndx (from make_index.py) holds only the THERMOSTAT partition --
System/Protein/MEMB/SOLV. MM-GBSA needs the complex split into its two binding
partners, which is a different question and must not be answered by guessing
residue ranges.

The peptide was already located once, by walking bonded topology, and written to
pepmeta.txt. This script reuses that answer rather than re-deriving it, so the
rescoring and the chirality gate cannot disagree about which residues are the ligand.
"""
import sys
import parmed as pmd

top, tpr, pepmeta, base_ndx, out_ndx = sys.argv[1:6]

meta = {}
for line in open(pepmeta):
    if "=" in line:
        k, v = line.strip().split("=", 1)
        meta[k] = v

first, last = int(meta["PEP_FIRST_RES"]), int(meta["PEP_LAST_RES"])
nres = int(meta["PEP_NRES"])
if last - first + 1 != nres:
    sys.exit(f"FAIL: pepmeta inconsistent: {first}-{last} is not {nres} residues")

p = pmd.load_file(top)
AA_ONLY = [r for r in p.residues]

lig, rec = [], []
for r in p.residues:
    rid = r.idx + 1
    atoms = [a.idx + 1 for a in r.atoms]
    if first <= rid <= last:
        lig += atoms
    elif r.name in ("PA", "PC", "OL", "WAT", "HOH", "TIP3",
                    "Na+", "Cl-", "NA", "CL"):
        continue                      # solvent/membrane are stripped by MM-GBSA
    else:
        rec += atoms

if not lig:
    sys.exit("FAIL: ligand group is empty")
if not rec:
    sys.exit("FAIL: receptor group is empty")

# the peptide sequence in the topology must match what pepmeta recorded
seq_top = "-".join(p.residues[i - 1].name for i in range(first, last + 1))
if seq_top != meta["PEP_SEQ"]:
    sys.exit(f"FAIL: peptide identity drifted.\n"
             f"  pepmeta: {meta['PEP_SEQ']}\n  topology: {seq_top}")

print(f"  ligand  : {seq_top}  ({len(lig)} atoms, residues {first}-{last})")
print(f"  receptor: {len(rec)} atoms")
if len(set(lig) & set(rec)):
    sys.exit("FAIL: receptor and ligand groups overlap")

with open(out_ndx, "w") as fh:
    for name, idxs in (("Receptor", rec), ("Ligand", lig)):
        fh.write(f"[ {name} ]\n")
        for i in range(0, len(idxs), 15):
            fh.write(" ".join(f"{x:6d}" for x in idxs[i:i + 15]) + "\n")
print(f"  wrote {out_ndx}")
