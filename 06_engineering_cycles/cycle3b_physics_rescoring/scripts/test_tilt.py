#!/usr/bin/env python3
"""Ground-truth test for tilt.py. Run: python test_tilt.py

Builds synthetic 7-helix bundles rotated by a KNOWN angle and checks that tilt.py
recovers it. This is the only way to test an orientation tool honestly: on real
systems there is no ground truth to compare against, so a bug that reported every
system as upright would look like success.

Each case also carries the two contaminants that matter on real input:
  - a short peptide in chain B (must not bias the receptor axis)
  - 40 resname-DUM pseudo-atoms spread +/-60 A in xy, as memembed appends. These are
    far off-axis, so if the tool ever stopped excluding them the measured axis would
    swing towards the membrane plane and every system would read as badly tilted.
"""
import os, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TILT = os.path.join(HERE, "tilt.py")
OUT = os.path.join(HERE, "..", "test_out_tilt")


def synth(path, tilt_deg, nhel=7, nres=24, seed=0):
    rng = np.random.default_rng(seed)
    pts = []
    for h in range(nhel):
        ang = 2 * np.pi * h / nhel
        cx, cy = 9.0 * np.cos(ang), 9.0 * np.sin(ang)
        for i in range(nres):
            pts.append((cx + 0.3 * rng.normal(), cy + 0.3 * rng.normal(),
                        (i - nres / 2) * 1.5))
    P = np.array(pts)
    th = np.radians(tilt_deg)
    Rx = np.array([[1, 0, 0], [0, np.cos(th), -np.sin(th)], [0, np.sin(th), np.cos(th)]])
    P = P @ Rx.T
    pep = np.array([[0, 0, (nres / 2 + 3) * 1.5 + j * 1.5] for j in range(5)]) @ Rx.T
    lines, n = [], 0
    for k, (x, y, z) in enumerate(P):
        n += 1
        lines.append("ATOM  %5d  CA  ALA A%4d    %8.3f%8.3f%8.3f  1.00  0.00           C"
                     % (n, k + 1, x, y, z))
    for j, (x, y, z) in enumerate(pep):
        n += 1
        lines.append("ATOM  %5d  CA  GLY B%4d    %8.3f%8.3f%8.3f  1.00  0.00           C"
                     % (n, j + 1, x, y, z))
    for j in range(40):
        n += 1
        x, y = rng.uniform(-60, 60), rng.uniform(-60, 60)
        lines.append("ATOM  %5d  N   DUM C%4d    %8.3f%8.3f%8.3f  1.00  0.00           N"
                     % (n, j + 1, x, y, 0.0))
    open(path, "w").write("\n".join(lines) + "\nEND\n")


def run(*a):
    r = subprocess.run([sys.executable, TILT, *a], capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def measured(txt):
    return float(txt.split("TILT_DEG=")[1].split()[0])


def main():
    os.makedirs(OUT, exist_ok=True)
    fails = []

    # 1. recovery of a known tilt, across the range actually seen in the panel
    for true_t in (0.0, 3.0, 10.0, 24.0, 29.6, 35.0):
        p = os.path.join(OUT, "s%.0f.pdb" % true_t)
        synth(p, true_t)
        rc, o = run("measure", p, "--rec-chain", "A")
        m = measured(o)
        if abs(m - true_t) > 1.5:
            fails.append("measure true=%.1f got=%.2f" % (true_t, m))
        print("  measure true=%5.1f -> %6.2f (err %+.2f)" % (true_t, m, m - true_t))

    # 2. the gate must be correct AT the boundary, not just far from it
    for true_t, want_reject in ((3.0, False), (9.0, False), (11.0, True), (29.6, True)):
        p = os.path.join(OUT, "s%.0f.pdb" % true_t)
        synth(p, true_t)
        rc, _ = run("assert", p, "--rec-chain", "A", "--max-deg", "10")
        if (rc != 0) != want_reject:
            fails.append("assert tilt=%.1f rc=%d want_reject=%s" % (true_t, rc, want_reject))
        print("  assert  tilt=%5.1f -> exit %d (%s)"
              % (true_t, rc, "reject" if rc else "pass"))

    # 3. fix must land upright, keep every atom, and be a no-op when already upright
    for true_t in (29.6, 3.1, 0.0):
        src = os.path.join(OUT, "s%.0f.pdb" % true_t)
        dst = os.path.join(OUT, "f%.0f.pdb" % true_t)
        synth(src, true_t)
        rc, _ = run("fix", src, dst, "--rec-chain", "A")
        na = sum(l.startswith("ATOM") for l in open(src))
        nb = sum(l.startswith("ATOM") for l in open(dst))
        _, o2 = run("measure", dst, "--rec-chain", "A")
        after = measured(o2)
        if after > 0.5 or na != nb or rc != 0:
            fails.append("fix %.1f -> %.2f deg, atoms %d->%d, rc=%d" % (true_t, after, na, nb, rc))
        print("  fix     %5.1f -> %5.2f deg, atoms %d->%d" % (true_t, after, na, nb))

    # 4. DUM must stay excluded. Included, they would drag the axis into the xy plane.
    p = os.path.join(OUT, "s30.pdb")
    synth(p, 29.6)
    _, o = run("measure", p)
    if abs(measured(o) - 29.6) > 2.0:
        fails.append("DUM leaked into the axis: got %.2f" % measured(o))
    print("  DUM excluded by default -> %.2f deg (expect ~29.6)" % measured(o))

    # 5. too few CA atoms must fail loudly rather than return a meaningless axis
    tiny = os.path.join(OUT, "tiny.pdb")
    open(tiny, "w").write(
        "ATOM      1  CA  ALA A   1       0.000   0.000   0.000  1.00  0.00           C\nEND\n")
    rc, _ = run("measure", tiny)
    if rc == 0:
        fails.append("a 1-CA file did not fail")
    print("  1-CA file -> exit %d (must be non-zero)" % rc)

    print()
    if fails:
        print("FAIL (%d):" % len(fails))
        for f in fails:
            print("  -", f)
        sys.exit(1)
    print("ALL TILT TESTS PASSED")


main()
