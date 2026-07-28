#!/usr/bin/env python3
"""Install a C-terminal primary amide (-NH2) by appending an Amber NHE residue.

WHY THIS EXISTS
---------------
The bioactive species of every deltorphin/endomorphin control -- and of our own
payload -- is C-terminally AMIDATED, because PAM recognises the terminal Gly.
Boltz-2 cannot represent a C-terminal amide, which is one of the two reasons
Cycle 3b moved to force-field rescoring in the first place (the other is the
D-centre). But packmol-memgen --parametrize just runs tleap on whatever PDB it is
given, and tleap defaults a bare C-terminus to the CHARGED FREE ACID (-COO-).

So without this step the MD silently simulates the wrong chemical species: a free
acid carrying an extra negative charge exactly at the pharmacophore that
determines delta-selectivity. That is the very error this cycle exists to correct,
and it is invisible in the output -- the run completes and looks healthy.

METHOD
------
Delete the terminal carboxylate's second oxygen (OXT/OT2/O2) and any acid proton,
then append an NHE residue whose N sits where that oxygen was (1.335 A from C along
the original C->OXT direction, which is the correct amide C-N bond length). tleap
builds HN1/HN2 from the template in amino12.lib.

USAGE
  amidate.py <in.pdb> <out.pdb>            # amidate the LAST residue
  amidate.py <in.pdb> <out.pdb> --check    # report whether input is already amidated
"""
import sys
import numpy as np

DROP = {"OXT", "OT2", "O2", "HXT", "HO", "H2"}   # second carboxylate O and acid H

def read(path):
    return [l for l in open(path) if l.startswith(("ATOM", "HETATM"))]

def xyz(l):
    return np.array([float(l[30:38]), float(l[38:46]), float(l[46:54])])

def resid_key(l):
    return (l[21], l[22:27])

def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    src, out = sys.argv[1], sys.argv[2]
    check_only = "--check" in sys.argv

    atoms = read(src)
    if not atoms:
        sys.exit(f"FAIL: no ATOM records in {src}")

    keys = []
    for l in atoms:
        k = resid_key(l)
        if k not in keys:
            keys.append(k)
    last = keys[-1]
    last_atoms = [l for l in atoms if resid_key(l) == last]
    last_name = last_atoms[0][17:20].strip()

    if last_name in ("NHE", "NME"):
        print(f"already amidated: C-terminal residue is {last_name}")
        if check_only:
            sys.exit(0)
        open(out, "w").writelines(atoms)
        sys.exit(0)
    if check_only:
        print(f"NOT amidated: C-terminal residue is {last_name} (free acid)")
        sys.exit(1)

    at = {l[12:16].strip(): l for l in last_atoms}
    if "C" not in at:
        sys.exit(f"FAIL: C-terminal residue {last_name} has no backbone C")

    # the oxygen to replace: prefer an explicit OXT, else the one further from CA
    cand = [n for n in ("OXT", "OT2", "O2") if n in at]
    if cand:
        oname = cand[0]
    elif "O" in at and "CA" in at:
        oname = "O"   # only one carbonyl O present; place N opposite it across C
    else:
        sys.exit(f"FAIL: cannot find a carboxylate oxygen on {last_name}")

    C = xyz(at["C"])
    if cand:
        direction = xyz(at[oname]) - C
    else:
        # no second oxygen: put the amide N in the sp2 plane, opposite the carbonyl O
        O, CA = xyz(at["O"]), xyz(at["CA"])
        direction = -( (O - C) / np.linalg.norm(O - C) + (CA - C) / np.linalg.norm(CA - C) )
    direction = direction / np.linalg.norm(direction)
    N = C + 1.335 * direction          # amide C-N bond length

    kept = [l for l in atoms if not (resid_key(l) == last
                                     and l[12:16].strip() in DROP)]
    ndrop = len(atoms) - len(kept)

    serial = max(int(l[6:11]) for l in kept) + 1
    chain = last[0]
    resnum = int(last[1].strip()) + 1
    nhe = (f"ATOM  {serial:5d}  N   NHE {chain}{resnum:4d}    "
           f"{N[0]:8.3f}{N[1]:8.3f}{N[2]:8.3f}  1.00  0.00           N\n")

    with open(out, "w") as fh:
        fh.writelines(kept)
        fh.write(nhe)
        fh.write("TER\nEND\n")

    print(f"amidated {last_name}{last[1].strip()}: dropped {ndrop} atom(s) "
          f"({oname} replaced), NHE N at {np.linalg.norm(N-C):.3f} A from C "
          f"-> {out}")

if __name__ == "__main__":
    main()
