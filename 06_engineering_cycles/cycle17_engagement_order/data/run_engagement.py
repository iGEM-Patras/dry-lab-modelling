"""Classify every locally-available replica trajectory, in parallel across cores.

Writes one row per trajectory to engagement_all.csv. Safe to re-run as more
simulations land: trajectories already present in the output are skipped, so the
cost is paid once per trajectory rather than once per invocation.
"""
import os, sys, glob, csv, time
from multiprocessing import Pool
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engagement_order import classify_trajectory, load_reference, NATIVE_A

REF = "hpc/fabdd8ce-6391-4685-9159-dfdac22ba628/receptor_peptide.pdb"
PEPTIDE = {"deltorphin": "YAFEVVG", "engPENK": "YGGFEVVG"}
OUT = "engagement_all.csv"

_REF = {}


def _init():
    """Load the reference once per worker rather than once per trajectory."""
    for arm, pep in PEPTIDE.items():
        _REF[arm] = load_reference(REF, len(pep))


def _one(task):
    path, arm = task
    try:
        ref_rec, ref_pep = _REF[arm]
        r = classify_trajectory(path, PEPTIDE[arm], ref_rec, ref_pep)
    except Exception as e:
        return {"path": path, "arm": arm, "error": "%s: %s" % (type(e).__name__, str(e)[:90])}
    if r is None:
        return {"path": path, "arm": arm, "error": "no frames"}
    r["path"] = path
    r["arm"] = arm
    r["seed"] = os.path.basename(os.path.dirname(os.path.dirname(path)))
    return r


def main():
    done = set()
    if os.path.exists(OUT):
        with open(OUT) as fh:
            done = {row["path"] for row in csv.DictReader(fh)}
    tasks = []
    for p in sorted(glob.glob("traj/*/output_pdbs/replica_*.pdb")):
        if p in done:
            continue
        arm = "deltorphin" if "deltorphin" in p else "engPENK"
        tasks.append((p, arm))
    print("trajectories: %d new, %d already done" % (len(tasks), len(done)))
    if not tasks:
        return
    t0 = time.time()
    rows, errs = [], []
    with Pool(4, initializer=_init) as pool:
        for i, r in enumerate(pool.imap_unordered(_one, tasks), 1):
            (errs if "error" in r else rows).append(r)
            if i % 10 == 0:
                print("  %d/%d  %.0f s elapsed" % (i, len(tasks), time.time() - t0), flush=True)
    if errs:
        print("FAILURES: %d" % len(errs))
        for e in errs[:5]:
            print("   ", e["path"], e["error"])
    if not rows:
        print("CLASSIFIED NOTHING. Not a result: investigate the failures.")
        return
    cols = ["path", "arm", "seed", "file", "frames", "class",
            "first_message_frame", "first_address_frame", "best_rmsd", "best_rmsd_frame"]
    new = not os.path.exists(OUT)
    with open(OUT, "a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        if new:
            w.writeheader()
        w.writerows(rows)
    print("wrote %d rows in %.0f s" % (len(rows), time.time() - t0))


if __name__ == "__main__":
    main()
