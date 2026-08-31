#!/usr/bin/env python3
"""Merge bound-mode MM-GBSA results with residency fractions and build the gate input.

WHY THE RESIDENCY FRACTION IS MANDATORY HERE
  A bound-mode dG is CONDITIONAL: it is the energy of the pose while the peptide is in
  the site, averaged over only those frames. It says nothing about how often the peptide
  is in the site. Two replicates with identical dG but 13% vs 100% residency describe
  completely different molecules. Every consumer of this table must see both numbers,
  so they travel in the same row and this script refuses to emit one without the other.

  This is the same protocol (GB, same solvation model, same topology reduction) for all
  40 runs, so the values ARE mutually comparable -- which is the whole reason for
  recomputing the 31 already-scored runs instead of splicing 9 new ones into the old set.
"""
import argparse, csv, os, sys

def load_bound_counts(p):
    out = {}
    with open(p) as fh:
        for row in csv.DictReader(fh):
            out[(row["system"], int(row["rep"]))] = (
                int(row["n_bound"]), int(row["n_frames"]), float(row["pct_bound"]))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("results_dir", help="results_bound_parts/")
    ap.add_argument("bound_counts", help="bound_counts.csv")
    ap.add_argument("--out", required=True)
    ap.add_argument("--gate-out", required=True)
    a = ap.parse_args()

    bc = load_bound_counts(a.bound_counts)
    TAG = {("met_enkephalin","OPRD1"):"c3b_menk_DOR", ("met_enkephalin","OPRM1"):"c3b_menk_MOR",
           ("endomorphin_1","OPRD1"):"c3b_em1_DOR",   ("endomorphin_1","OPRM1"):"c3b_em1_MOR",
           ("deltorphin_I","OPRD1"):"c3b_dtI_DOR",    ("deltorphin_I","OPRM1"):"c3b_dtI_MOR",
           ("deltorphin_II","OPRD1"):"c3b_dtII_DOR",  ("deltorphin_II","OPRM1"):"c3b_dtII_MOR"}

    rows = []
    for fn in sorted(os.listdir(a.results_dir)):
        if not fn.endswith(".csv"):
            continue
        for line in open(os.path.join(a.results_dir, fn)):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            pep, rec, rep, dg = line.split(",")
            tag = TAG.get((pep, rec))
            if tag is None:
                sys.exit("FAIL: unknown peptide/receptor pair %s/%s" % (pep, rec))
            key = (tag, int(rep))
            if key not in bc:
                sys.exit("FAIL: no residency data for %s rep%s -- refusing to emit a "
                         "conditional energy without its residency fraction" % (tag, rep))
            nb, nf, pct = bc[key]
            rows.append(dict(peptide=pep, receptor=rec, replicate=int(rep),
                             dG_bound_kcal=float(dg), n_bound_frames=nb,
                             n_total_frames=nf, residency_pct=pct))
    if not rows:
        sys.exit("FAIL: no results found in %s" % a.results_dir)

    rows.sort(key=lambda r: (r["peptide"], r["receptor"], r["replicate"]))
    with open(a.out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)

    # gate.py input schema (from its load(): control, receptor, rep, dG_bind)
    with open(a.gate_out, "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["control","receptor","rep","dG_bind"])
        for r in rows:
            w.writerow([r["peptide"], r["receptor"], r["replicate"], "%.3f" % r["dG_bound_kcal"]])

    n_pairs = len({(r["peptide"], r["receptor"]) for r in rows})
    print("%d runs, %d arms" % (len(rows), n_pairs))
    lo = [r for r in rows if r["residency_pct"] < 50.0]
    if lo:
        print("residency < 50%% in %d runs -- report dG WITH residency for these:" % len(lo))
        for r in lo:
            print("  %-14s %s rep%d  dG=%8.2f  residency=%5.1f%%"
                  % (r["peptide"], r["receptor"], r["replicate"],
                     r["dG_bound_kcal"], r["residency_pct"]))

if __name__ == "__main__":
    main()
