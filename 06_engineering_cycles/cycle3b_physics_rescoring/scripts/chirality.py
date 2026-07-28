#!/usr/bin/env python3
"""Chirality assertion for D-amino-acid residues in Cycle 3b systems.

The Amber ff14SB topology is enantiomer-blind: parm10.dat contains no improper
torsion on the CX sp3 alpha-carbon, so nothing in the force field or in GROMACS
will warn if a D-centre inverts during minimisation or equilibration. This script
is therefore run as a hard gate after every minimisation and every equilibration
stage. Runs that invert are discarded, not analysed.

Convention: signed volume V = (r_N - r_CA) x (r_C - r_CA) . (r_CB - r_CA)
    V > 0  ->  L-residue
    V < 0  ->  D-residue
"""
import sys
import numpy as np

MOVE = ("HA", "CB", "HB1", "HB2", "HB3", "HB")


def load(path, chain=None):
    rows = []
    for l in open(path):
        if l.startswith(("ATOM", "HETATM")):
            if chain and l[21] != chain:
                continue
            rows.append(dict(raw=l, name=l[12:16].strip(), resn=l[17:20].strip(),
                             chain=l[21], resi=int(l[22:26]),
                             xyz=np.array([float(l[30:38]), float(l[38:46]), float(l[46:54])])))
    return rows


def signed_volume(rows, resi):
    d = {r["name"]: r["xyz"] for r in rows if r["resi"] == resi}
    if not {"N", "CA", "C", "CB"} <= set(d):
        return None  # Gly, or a cap: no CB, achiral
    return float(np.dot(np.cross(d["N"] - d["CA"], d["C"] - d["CA"]), d["CB"] - d["CA"]))


def invert(rows, resi):
    """Mirror the alpha-substituents through the N-CA-C plane -> flips chirality."""
    d = {r["name"]: r["xyz"] for r in rows if r["resi"] == resi}
    CA = d["CA"]
    nrm = np.cross(d["N"] - CA, d["C"] - CA)
    nrm /= np.linalg.norm(nrm)
    n = 0
    for r in rows:
        if r["resi"] == resi and r["name"] in MOVE:
            r["xyz"] = r["xyz"] - 2 * np.dot(r["xyz"] - CA, nrm) * nrm
            n += 1
    return n


def write(rows, path):
    with open(path, "w") as f:
        for r in rows:
            x, y, z = r["xyz"]
            f.write(r["raw"][:30] + f"{x:8.3f}{y:8.3f}{z:8.3f}" + r["raw"][54:])
        f.write("END\n")


def main():
    if len(sys.argv) < 4:
        sys.exit("usage: chirality.py {invert|assert} <pdb> <resi> [chain] [out.pdb]")
    mode, path, resi = sys.argv[1], sys.argv[2], int(sys.argv[3])
    chain = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] != "-" else None
    rows = load(path, chain)
    v0 = signed_volume(rows, resi)
    if v0 is None:
        sys.exit(f"FAIL residue {resi} has no CB (achiral) - wrong residue index?")

    if mode == "invert":
        n = invert(rows, resi)
        v1 = signed_volume(rows, resi)
        out = sys.argv[5] if len(sys.argv) > 5 else path.replace(".pdb", "_D.pdb")
        write(rows, out)
        ok = v1 < 0 and abs(abs(v1) - abs(v0)) < 1e-6
        print(f"invert res{resi}: moved {n} atoms | V {v0:+.3f} -> {v1:+.3f} | "
              f"magnitude preserved={abs(abs(v1)-abs(v0))<1e-6} -> {out}")
        sys.exit(0 if ok else 1)

    # assert mode: require D (V < 0)
    print(f"assert res{resi}: V = {v0:+.3f} -> {'D (ok)' if v0 < 0 else 'L (INVERTED!)'}")
    sys.exit(0 if v0 < 0 else 2)


if __name__ == "__main__":
    main()
