#!/usr/bin/env python3
"""Measure -- and if asked, correct -- the tilt of a TM bundle vs the membrane normal.

WHY THIS EXISTS
---------------
memembed silently failed to orient 4 of 6 otherwise-identical systems in the first
Stage 1 build wave: tilts came out bimodal at ~3 deg (2 systems) and 24-35 deg (4
systems), from the same receptor and the same command. Every build still logged
"orientation: --preoriented", so the pipeline believed it had succeeded and packed a
bilayer around a tilted bundle.

That is not merely a cosmetic problem. At 24-35 deg the TM hydrophobic belt is not
aligned with the bilayer hydrophobic core, so TM residues sit against headgroups and
water. The protein then rotates during equilibration to relieve the mismatch, over
many ns -- so a 20 ns production window measures the reorientation, not the bound
pose, and the contact metrics report the relaxation instead of the binding.

METHOD
------
The TM bundle of a class-A GPCR is a bundle of 7 roughly parallel helices, so the
principal axis of its CA coordinates (largest-eigenvalue eigenvector of the CA
covariance) runs along the bundle. The angle between that axis and z is the tilt.
This is orientation-only and sign-agnostic: |cos| is used, so a bundle pointing -z
reads the same as +z. Whether the extracellular side faces +z is a SEPARATE question
that this tool does not answer (see --check-topology).

CAVEAT on which atoms to use: the principal axis must be computed from the RECEPTOR
alone. Including the peptide biases the axis, and including the bilayer-marker
pseudo-atoms memembed appends (resname DUM) would dominate it outright. Pass
--rec-chain, or rely on the default which drops DUM and any HETATM.

Usage:
  tilt.py measure  IN.pdb [--rec-chain A]            -> prints TILT_DEG=<x>
  tilt.py assert   IN.pdb --max-deg 10 [--rec-chain A]
  tilt.py fix      IN.pdb OUT.pdb [--rec-chain A]    -> rigid-body rotate to 0 deg
"""
import sys, argparse
import numpy as np

def read_pdb(path):
    """Return (lines, coords array, per-line index map). Keeps every line verbatim."""
    lines = open(path).read().splitlines()
    idx, xyz = [], []
    for i, l in enumerate(lines):
        if l.startswith(("ATOM", "HETATM")) and len(l) >= 54:
            idx.append(i)
            xyz.append((float(l[30:38]), float(l[38:46]), float(l[46:54])))
    return lines, np.array(xyz), idx

def receptor_ca(lines, rec_chain=None):
    """CA coordinates of the receptor only: no DUM pseudo-atoms, no HETATM."""
    ca = []
    for l in lines:
        if not l.startswith("ATOM") or len(l) < 54:
            continue
        if l[17:20].strip() == "DUM":
            continue
        if l[12:16].strip() != "CA":
            continue
        if rec_chain and l[21] != rec_chain:
            continue
        ca.append((float(l[30:38]), float(l[38:46]), float(l[46:54])))
    return np.array(ca)

def principal_axis(ca):
    X = ca - ca.mean(0)
    w, v = np.linalg.eigh(np.cov(X.T))
    return v[:, int(np.argmax(w))]

def tilt_deg(axis):
    # orientation, not direction: a bundle along -z is as upright as one along +z
    return float(np.degrees(np.arccos(min(1.0, abs(float(axis[2]))))))

def rotation_to_z(axis):
    """Rotation matrix taking `axis` onto +z (Rodrigues; handles both degenerate cases)."""
    a = axis / np.linalg.norm(axis)
    if a[2] < 0:            # pick the sense that needs the smaller rotation
        a = -a
    z = np.array([0.0, 0.0, 1.0])
    v = np.cross(a, z)
    s = np.linalg.norm(v)
    if s < 1e-8:
        return np.eye(3)
    c = float(np.dot(a, z))
    K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]]) / s
    return np.eye(3) + np.sin(np.arccos(c)) * K + (1 - c) * (K @ K)

def write_pdb(lines, xyz, idx, out):
    for k, i in enumerate(idx):
        l = lines[i]
        lines[i] = f"{l[:30]}{xyz[k,0]:8.3f}{xyz[k,1]:8.3f}{xyz[k,2]:8.3f}{l[54:]}"
    open(out, "w").write("\n".join(lines) + "\n")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["measure", "assert", "fix"])
    ap.add_argument("inp"); ap.add_argument("out", nargs="?")
    ap.add_argument("--rec-chain", default=None)
    ap.add_argument("--max-deg", type=float, default=10.0)
    a = ap.parse_args()

    lines, xyz, idx = read_pdb(a.inp)
    ca = receptor_ca(lines, a.rec_chain)
    if len(ca) < 50:
        sys.exit(f"FAIL: only {len(ca)} receptor CA atoms found in {a.inp} -- "
                 f"wrong --rec-chain, or the file is not a receptor complex")
    ax = principal_axis(ca)
    t = tilt_deg(ax)
    print(f"TILT_DEG={t:.2f}  (from {len(ca)} receptor CA atoms)")

    if a.mode == "measure":
        return
    if a.mode == "assert":
        if t > a.max_deg:
            sys.exit(f"FAIL: tilt {t:.2f} deg exceeds {a.max_deg} deg -- receptor is "
                     f"NOT aligned to the membrane normal. Do not pack a bilayer "
                     f"around this; re-orient first.")
        print(f"  tilt OK ({t:.2f} <= {a.max_deg} deg)")
        return

    # fix: rigid-body rotate EVERY atom about the receptor CA centroid
    if not a.out:
        sys.exit("FAIL: fix mode needs an output path")
    if t <= 0.05:
        print("  already upright; copying unchanged")
        write_pdb(lines, xyz, idx, a.out)
        return
    R = rotation_to_z(ax)
    cen = ca.mean(0)
    new = (xyz - cen) @ R.T + cen

    # the rotation must be rigid: check it preserved internal geometry exactly
    def rg(P):
        return float(np.sqrt(((P - P.mean(0)) ** 2).sum(1).mean()))
    assert abs(rg(new) - rg(xyz)) < 1e-6, "rotation changed Rg -- not rigid"
    d0 = np.linalg.norm(xyz[0] - xyz[-1]); d1 = np.linalg.norm(new[0] - new[-1])
    assert abs(d0 - d1) < 1e-6, "rotation changed an interatomic distance -- not rigid"

    write_pdb(lines, new, idx, a.out)
    # re-measure from the written file, not from memory: the only honest check
    lines2, _, _ = read_pdb(a.out)
    t2 = tilt_deg(principal_axis(receptor_ca(lines2, a.rec_chain)))
    print(f"  rotated {t:.2f} -> {t2:.2f} deg, Rg preserved -> {a.out}")
    if t2 > 0.5:
        sys.exit(f"FAIL: still {t2:.2f} deg after rotation")

main()
