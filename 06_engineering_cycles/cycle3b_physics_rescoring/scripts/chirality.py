#!/usr/bin/env python3
"""Chirality assertion / inversion for D-amino-acid residues.

WHY THIS EXISTS
---------------
ff14SB has no D-amino-acid templates, so a D-residue is built by MIRRORING the L
form. That is valid because no improper-torsion term in the parameter set
references the sp3 alpha-carbon type, so handedness carries NO energetic term and
the mirrored residue keeps identical parameters (verified: bonded topology is
byte-identical between L and D prmtops).

The direct consequence is that the topology is ENANTIOMER-BLIND: nothing in the
force field can notice if the D-centre inverts during minimisation or dynamics.
So chirality must be asserted EXTERNALLY, after every stage. A run whose centre
inverted is DISCARDED, never averaged in.

Handedness is measured as the signed volume of the improper
    V = (N - CA) . [ (C - CA) x (CB - CA) ]
L-amino acids give V > 0, D-amino acids V < 0 (Gly has no CB and is achiral).

USAGE
  chirality.py assert <pdb> <resid> [chain]   -> exit 0 if D, 2 if L, 1 on error
  chirality.py invert <pdb> <resid> [chain] <out.pdb>
<resid> is a residue NUMBER as written in the PDB (or 1-based position when
--by-position is given).
"""
import sys
import numpy as np

def parse(path):
    rows = []
    for l in open(path):
        if l.startswith(("ATOM", "HETATM")):
            rows.append(dict(
                line=l, name=l[12:16].strip(), resn=l[17:20].strip(),
                chain=l[21], resi=l[22:26].strip(),
                xyz=np.array([float(l[30:38]), float(l[38:46]), float(l[46:54])])))
    return rows

def pick(rows, resid, chain, by_position):
    if by_position:
        keys = []
        for r in rows:
            k = (r["chain"], r["resi"])
            if k not in keys:
                keys.append(k)
        if not 1 <= int(resid) <= len(keys):
            sys.exit(f"FAIL: position {resid} outside 1-{len(keys)}")
        want = keys[int(resid) - 1]
        return [r for r in rows if (r["chain"], r["resi"]) == want]
    sel = [r for r in rows if r["resi"] == str(resid)
           and (chain in (None, "", "-") or r["chain"] == chain)]
    if not sel:
        chains = sorted({r["chain"] for r in rows})
        sys.exit(f"FAIL: residue {resid} not found (chains present: {chains})")
    return sel

def volume(sel, resid):
    at = {r["name"]: r["xyz"] for r in sel}
    missing = [a for a in ("N", "CA", "C", "CB") if a not in at]
    if missing:
        resn = sel[0]["resn"]
        sys.exit(f"FAIL: residue {resid} ({resn}) lacks {missing} "
                 f"- Gly is achiral, or the wrong residue was addressed")
    v = np.dot(at["N"] - at["CA"],
               np.cross(at["C"] - at["CA"], at["CB"] - at["CA"]))
    return float(v), sel[0]["resn"]

def main():
    args = [a for a in sys.argv[1:] if a != "--by-position"]
    by_pos = "--by-position" in sys.argv
    if len(args) < 3:
        sys.exit(__doc__)
    mode, pdb, resid = args[0], args[1], args[2]
    rest = args[3:]

    if mode == "assert":
        chain = rest[0] if rest else None
        rows = parse(pdb)
        sel = pick(rows, resid, chain, by_pos)
        v, resn = volume(sel, resid)
        hand = "D" if v < 0 else "L"
        print(f"assert res{resid} ({resn}): V = {v:+.3f} -> {hand}", end="")
        if v < 0:
            print(" (ok)")
            sys.exit(0)
        print(" (EXPECTED D - run is invalid)")
        sys.exit(2)

    if mode == "invert":
        if not rest:
            sys.exit("FAIL: invert needs an output path")
        chain = rest[0] if len(rest) > 1 else None
        out = rest[-1]
        rows = parse(pdb)
        sel = pick(rows, resid, chain, by_pos)
        v0, resn = volume(sel, resid)
        # Refuse up front if the centre is ALREADY D. Inverting it would silently
        # produce an L residue, and a caller asking for that is confused about the
        # state of its own structure -- which is exactly the bug this file guards.
        if v0 < 0:
            sys.exit(f"FAIL: residue {resid} ({resn}) is already D "
                     f"(V = {v0:+.3f}); refusing to invert it back to L")
        at = {r["name"]: r["xyz"] for r in sel}
        # Reflect ONLY the CB substituent through the N-CA-C plane. This inverts the
        # centre while leaving the backbone -- and therefore the docked pose and every
        # other residue -- untouched.
        nrm = np.cross(at["C"] - at["CA"], at["N"] - at["CA"])
        nrm /= np.linalg.norm(nrm)
        moved = 0
        sidechain = [r for r in sel if r["name"] not in ("N", "CA", "C", "O", "OXT",
                                                         "H", "HA", "H1", "H2", "H3")]
        lines_out = []
        newxyz = {}
        for r in sidechain:
            d = r["xyz"] - at["CA"]
            r2 = at["CA"] + d - 2 * np.dot(d, nrm) * nrm
            newxyz[id(r)] = r2
            moved += 1
        for r in rows:
            if id(r) in newxyz:
                x, y, z = newxyz[id(r)]
                l = r["line"]
                lines_out.append(f"{l[:30]}{x:8.3f}{y:8.3f}{z:8.3f}{l[54:]}")
            else:
                lines_out.append(r["line"])
        open(out, "w").writelines(lines_out)
        v1, _ = volume(parse(out) and pick(parse(out), resid, chain, by_pos), resid)
        ok = abs(abs(v1) - abs(v0)) < 0.15 and v1 < 0 < v0
        print(f"invert res{resid} ({resn}): moved {moved} atoms | "
              f"V {v0:+.3f} -> {v1:+.3f} | magnitude preserved={abs(abs(v1)-abs(v0))<0.15} "
              f"-> {out}")
        sys.exit(0 if ok else 1)

    sys.exit(f"FAIL: unknown mode {mode!r}")

if __name__ == "__main__":
    main()
