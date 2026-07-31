#!/usr/bin/env python3
"""Measure receptor-peptide heavy-atom contacts, and gate on them after minimisation.

Motivated by the 2026-07-30 panel pre-flight sweep, which found that the Boltz co-fold
poses carry very close receptor-peptide contacts -- as tight as 1.74 A (LYS108:NZ -
NHE5:N in c3b_em1_DOR), measured with hydrogens EXCLUDED so they are real geometry, not
H-placement artifacts. Minimisation is expected to relieve them. The problem was that
nothing checked whether it actually did: do_minimise() asserted min.gro exists and read
the potential energy, and a system that failed to relax would have entered a 20 ns
production run with a clash driving the first nanosecond of dynamics.

Potential energy cannot substitute for this check. It is a whole-system number dominated
by ~155k atoms of lipid and water; a single 1.7 A contact at the interface is far inside
its noise. The interface has to be measured directly.

Two modes:
  record  <top> <coords> <pepmeta> <out>   write a baseline before minimisation
  check   <top> <coords> <pepmeta> <base>  re-measure after, compare, exit non-zero on fail

Residue partitioning is taken from pepmeta.txt (written by make_index.py), NOT from chain
IDs -- tleap strips those. The peptide is residues PEP_FIRST_RES..PEP_LAST_RES; the
receptor is every earlier amino-acid residue.
"""
import sys, collections
import numpy as np
import parmed as pmd

# Heavy-atom contact policy. A hydrogen bond between heavy atoms sits around 2.6-3.0 A
# and can tighten to ~2.5 A when strong, so anything at or above HARD is chemically
# sensible. Below HARD there is no non-bonded interpretation: that is atom overlap.
HARD_A = 2.20   # post-min minimum below this = FAIL
WARN_A = 2.50   # post-min minimum below this = WARN (relaxed, but tight)
CLOSE  = [2.6, 3.0]   # reporting bins

AA = set("""ALA ARG ASN ASP CYS GLN GLU GLY HIS ILE LEU LYS MET PHE PRO SER THR TRP
TYR VAL HID HIE HIP CYX ASH GLH LYN NALA NARG NASN NASP NCYS NGLN NGLU NGLY NHIS
NILE NLEU NLYS NMET NPHE NPRO NSER NTHR NTRP NTYR NVAL CALA CARG CASN CASP CCYS
CGLN CGLU CGLY CHIS CILE CLEU CLYS CMET CPHE CPRO CSER CTHR CTRP CTYR CVAL
NHE NME ACE""".split())


def read_meta(path):
    m = {}
    for line in open(path):
        if "=" in line:
            k, v = line.strip().split("=", 1)
            m[k] = v
    return int(m["PEP_FIRST_RES"]), int(m["PEP_LAST_RES"])


def load(top, coords, pepmeta):
    """Return (receptor_atoms, peptide_atoms, box) as (labels, xyz) pairs, heavy only."""
    p = pmd.load_file(top, xyz=coords)
    first, last = read_meta(pepmeta)
    rec, pep = [], []
    for a in p.atoms:
        if a.residue.name not in AA:
            continue
        # Element from the topology, not the atom name: Amber names like CA/CB start
        # with C, but so does a chlorine, and name-prefix guessing is how hydrogens
        # leak back into a "heavy atom" selection.
        if a.atomic_number == 1:
            continue
        rnum = a.residue.idx + 1          # pepmeta is 1-based, parmed .idx is 0-based
        lab = f"{a.residue.name}{rnum}:{a.name}"
        (pep if first <= rnum <= last else rec).append((lab, a.xx, a.xy, a.xz))
    if not pep:
        sys.exit(f"FAIL: no peptide atoms found for residues {first}-{last} in {coords}")
    if not rec:
        sys.exit(f"FAIL: no receptor atoms found in {coords}")
    box = p.box  # [a, b, c, alpha, beta, gamma] in A/deg, or None
    return rec, pep, box


def distances(rec, pep, box):
    """Pairwise receptor-peptide distances under the minimum-image convention.

    PBC matters here: min.gro comes back from GROMACS with coordinates wrapped into the
    box, so a receptor-peptide pair that straddles a boundary would otherwise be
    measured across the whole cell and read as a comfortable ~100 A -- silently turning
    a real clash into a pass.
    """
    R = np.array([a[1:] for a in rec], dtype=float)
    P = np.array([a[1:] for a in pep], dtype=float)
    d = R[:, None, :] - P[None, :, :]
    if box is not None:
        a, b, c = float(box[0]), float(box[1]), float(box[2])
        ang = [float(x) for x in box[3:6]]
        if all(abs(x - 90.0) < 1e-3 for x in ang):
            L = np.array([a, b, c])
            d -= L * np.round(d / L)
        else:
            print(f"  note: non-orthorhombic box (angles {ang}); minimum image not "
                  f"applied, distances are raw", file=sys.stderr)
    return np.sqrt((d ** 2).sum(-1))


def summarise(rec, pep, D, topn=5):
    flat = np.argsort(D, axis=None)[:topn]
    pairs = []
    for f in flat:
        i, j = np.unravel_index(f, D.shape)
        pairs.append((rec[i][0], pep[j][0], float(D[i, j])))
    return dict(
        min=float(D.min()),
        n_lt=[int((D < c).sum()) for c in CLOSE],
        pairs=pairs,
        n_rec=len(rec), n_pep=len(pep),
    )


def report(tag, s):
    print(f"  {tag}: min {s['min']:.2f} A | "
          + " ".join(f"{n} pairs <{c}A" for n, c in zip(s["n_lt"], CLOSE))
          + f" | {s['n_rec']} rec / {s['n_pep']} pep heavy atoms")
    for r, p, d in s["pairs"][:3]:
        print(f"      {r:>18s} - {p:<14s} {d:5.2f} A")


def main():
    if len(sys.argv) < 5:
        sys.exit(__doc__)
    mode, top, coords, pepmeta = sys.argv[1:5]
    rec, pep, box = load(top, coords, pepmeta)
    D = distances(rec, pep, box)
    s = summarise(rec, pep, D)

    if mode == "record":
        out = sys.argv[5]
        with open(out, "w") as fh:
            fh.write(f"PRE_MIN_A={s['min']:.3f}\n")
            for c, n in zip(CLOSE, s["n_lt"]):
                fh.write(f"PRE_N_LT_{str(c).replace('.', 'p')}={n}\n")
            fh.write(f"PRE_WORST={s['pairs'][0][0]}|{s['pairs'][0][1]}\n")
        report("pre-min contacts", s)
        return 0

    if mode == "check":
        base = sys.argv[5]
        b = {}
        try:
            for line in open(base):
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    b[k] = v
        except OSError as e:
            sys.exit(f"FAIL: no pre-minimisation baseline at {base} ({e.strerror}). "
                     f"The build's record step must run before this check; without a "
                     f"baseline there is nothing to compare relaxation against.")
        if "PRE_MIN_A" not in b:
            sys.exit(f"FAIL: baseline {base} has no PRE_MIN_A entry (truncated or "
                     f"from an older format).")
        pre = float(b["PRE_MIN_A"])
        report("post-min contacts", s)
        print(f"  interface relaxation: {pre:.2f} -> {s['min']:.2f} A "
              f"({s['min'] - pre:+.2f} A)")

        if s["min"] < HARD_A:
            print(f"FAIL: closest receptor-peptide heavy-atom contact is {s['min']:.2f} A "
                  f"after minimisation (hard floor {HARD_A} A).")
            print( "      Minimisation did not relieve the co-fold clash. Do NOT run "
                   "production on this system:")
            print( "      the first ns would be dominated by the clash relaxing, not by "
                   "peptide binding.")
            return 1
        if s["min"] < WARN_A:
            print(f"  WARN: {s['min']:.2f} A is above the {HARD_A} A floor but tight "
                  f"(< {WARN_A} A). Watch the first ns of production.")
        else:
            print(f"  contacts OK ({s['min']:.2f} A >= {WARN_A} A)")
        return 0

    sys.exit(f"FAIL: mode must be record|check (got '{mode}')")


if __name__ == "__main__":
    sys.exit(main())
