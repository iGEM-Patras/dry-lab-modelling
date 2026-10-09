#!/usr/bin/env python3
"""
Cycle 3b Stage-1 calibration gate, G1 / G2' / G3.

Reads per-replicate MM-GBSA dG_bind values and issues a single PASS/FAIL
verdict that authorises (or terminates) Stage 2.

Usage
-----
    gate.py evaluate <results.csv> [--out gate_verdict.json] [--sem-max 1.5]

Input CSV columns (one row per receptor x replicate):
    control   one of: deltorphin_II, deltorphin_I, endomorphin_1, met_enkephalin
    receptor  OPRD1 | OPRM1
    rep       integer replicate index
    dG_bind   MM-GBSA binding free energy, kcal/mol

ddG_sel is formed WITHIN a replicate index:  ddG_sel = dG(OPRM1) - dG(OPRD1).
Pairing within replicate (rather than averaging each receptor first) is
deliberate: replicate r of the mu system and replicate r of the delta system
share nothing physically, but pairing keeps the two arms balanced and makes
the replicate SD an honest estimate of run-to-run spread on the DIFFERENCE,
which is the quantity the gate thresholds.

Criteria
--------
G1  (sign + rank)  deltorphin II and I both positive, endomorphin-1 negative,
                   min(deltorphins) > endomorphin-1.
G2' (precision)    SEM of ddG_sel <= --sem-max (default 1.5 kcal/mol) on every
                   control.
G3  (calibration)  OLS of computed vs experimental ddG_sel has positive slope
                   with 95% CI excluding zero.

WHY G2' AND NOT THE PRE-REGISTERED G2
-------------------------------------
CYCLE3B_DESIGN.md wrote G2 as "replicate SD of ddG_sel <= 1.5 kcal/mol on
every control". That criterion is not passable by a correct method:

  * SD(ddG) = sigma_rep * sqrt(2). Requiring it <= 1.5 demands
    sigma_rep <= 1.06 kcal/mol -- below the 1-2 kcal/mol MM-GBSA uncertainty
    the SAME design document states as expected.
  * A 3-sample SD has 2 df. Even when the true SD is exactly at the limit,
    each control passes with p ~ 0.68, and requiring all four passes at
    0.68^4 = 0.21.
  * Monte-Carlo over the pre-registered anchors: a method with a PERFECT
    calibration slope of 1.0 passes all three gates 21% of the time at
    sigma_rep = 1.0 and 3% at sigma_rep = 1.5.
  * Decisively: power DECREASES with more replicates (0.076 at n=2 to 0.000
    at n=10, sigma_rep = 1.5). More sampling makes a correct method fail more
    often. That is an estimator defect, not a property of the method under
    test, so no amount of compute can rescue it.

G2' thresholds the SEM -- the precision of the reported estimate -- which is
what "can this method resolve the controls" actually means. It behaves as a
gate should: power RISES with replicates (0.21 at n=2 to 1.00 at n=10 at
sigma_rep = 1.5) while the false-pass rate against a null method stays at
~2%, indistinguishable from G2's own ~2%. The gate loses no strictness
against a method with no signal; it stops failing methods that do have one.

Evidence: gate_calibration.png / .csv, and AMENDMENT_G2.md for the
pre-registration amendment record. The amendment was filed BEFORE any Stage-1
dG_bind value existed, which is the only condition under which changing a
pre-registered criterion is legitimate.

A failed gate still terminates the cycle and reports a negative methodological
result, exactly as pre-registered. G1 and G3 are unchanged.
"""
from __future__ import annotations
import argparse, json, sys
import numpy as np

# Experimental ddG_sel anchors, kcal/mol (CYCLE3B_DESIGN.md Stage 1 table).
# Sign convention: ddG_sel = dG(mu) - dG(delta); positive = delta-preferring.
EXPERIMENTAL = {
    "deltorphin_II":  +5.39,   # delta, 8448x
    "deltorphin_I":   +5.70,   # delta, 14318x
    "endomorphin_1":  -2.99,   # mu, 150x (conservative)
    "met_enkephalin":  0.00,   # weakly delta, neutral reference
}
ORDER = ["deltorphin_II", "deltorphin_I", "endomorphin_1", "met_enkephalin"]
SEM_MAX_DEFAULT = 1.5


def load(path):
    """Read the results CSV into {control: {rep: {receptor: dG_bind}}}."""
    import csv
    data = {}
    with open(path) as fh:
        rdr = csv.DictReader(fh)
        need = {"control", "receptor", "rep", "dG_bind"}
        missing = need - set(rdr.fieldnames or [])
        if missing:
            sys.exit(f"FAIL: results CSV missing columns: {sorted(missing)}")
        for row in rdr:
            c = row["control"].strip()
            if c not in EXPERIMENTAL:
                sys.exit(f"FAIL: unknown control '{c}'; expected one of {ORDER}")
            r = row["receptor"].strip().upper()
            if r not in ("OPRD1", "OPRM1"):
                sys.exit(f"FAIL: receptor must be OPRD1 or OPRM1, got '{r}'")
            data.setdefault(c, {}).setdefault(int(row["rep"]), {})[r] = float(row["dG_bind"])
    return data


def ddg_per_replicate(data):
    """{control: array of ddG_sel, one per replicate present in BOTH receptors}."""
    out = {}
    for c, reps in data.items():
        vals = []
        for rep in sorted(reps):
            both = reps[rep]
            if "OPRD1" in both and "OPRM1" in both:
                vals.append(both["OPRM1"] - both["OPRD1"])
            else:
                have = sorted(both)
                print(f"  note: {c} rep{rep} has only {have} -- dropped "
                      f"(a discarded replicate must not be averaged in)")
        out[c] = np.asarray(vals, float)
    return out


def evaluate(dd, sem_max=SEM_MAX_DEFAULT):
    from scipy import stats
    present = [c for c in ORDER if c in dd and dd[c].size]
    missing = [c for c in ORDER if c not in present]
    if missing:
        return {"verdict": "FAIL", "reason": f"missing controls: {missing}",
                "G1": None, "G2p": None, "G3": None}

    per = {}
    for c in present:
        v = dd[c]
        n = v.size
        sem = float(v.std(ddof=1) / np.sqrt(n)) if n > 1 else float("nan")
        per[c] = {"n": int(n), "mean": float(v.mean()),
                  "sd": float(v.std(ddof=1)) if n > 1 else float("nan"),
                  "sem": sem, "experimental": EXPERIMENTAL[c],
                  "values": [round(float(x), 3) for x in v]}
    if any(per[c]["n"] < 2 for c in present):
        return {"verdict": "FAIL", "reason": "a control has < 2 usable replicates; "
                "SEM undefined", "per_control": per, "G1": None, "G2p": None, "G3": None}

    m = {c: per[c]["mean"] for c in present}
    g1_checks = {
        "deltorphin_II > 0":  m["deltorphin_II"] > 0,
        "deltorphin_I > 0":   m["deltorphin_I"] > 0,
        "endomorphin_1 < 0":  m["endomorphin_1"] < 0,
        "deltorphins ranked above endomorphin-1":
            min(m["deltorphin_II"], m["deltorphin_I"]) > m["endomorphin_1"],
    }
    G1 = all(g1_checks.values())

    g2_checks = {c: per[c]["sem"] <= sem_max for c in present}
    G2p = all(g2_checks.values())

    x = np.concatenate([np.full(dd[c].size, EXPERIMENTAL[c]) for c in present])
    y = np.concatenate([dd[c] for c in present])
    lr = stats.linregress(x, y)
    df = y.size - 2
    tcrit = float(stats.t.ppf(0.975, df))
    lo, hi = lr.slope - tcrit * lr.stderr, lr.slope + tcrit * lr.stderr
    G3 = bool(lo > 0)

    verdict = "PASS" if (G1 and G2p and G3) else "FAIL"
    return {
        "verdict": verdict,
        "G1": {"pass": bool(G1), "checks": {k: bool(v) for k, v in g1_checks.items()}},
        "G2p": {"pass": bool(G2p), "sem_max": sem_max,
                "checks": {c: bool(v) for c, v in g2_checks.items()},
                "sem": {c: round(per[c]["sem"], 3) for c in present}},
        "G3": {"pass": bool(G3), "slope": round(float(lr.slope), 4),
               "ci95": [round(float(lo), 4), round(float(hi), 4)],
               "r": round(float(lr.rvalue), 4), "n_points": int(y.size), "df": int(df)},
        "per_control": per,
        "note": "G2' is the amended criterion (SEM); see AMENDMENT_G2.md. "
                "G1 and G3 are exactly as pre-registered.",
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    ev = sub.add_parser("evaluate")
    ev.add_argument("results_csv")
    ev.add_argument("--out", default="gate_verdict.json")
    ev.add_argument("--sem-max", type=float, default=SEM_MAX_DEFAULT)
    a = ap.parse_args()

    res = evaluate(ddg_per_replicate(load(a.results_csv)), sem_max=a.sem_max)
    with open(a.out, "w") as fh:
        json.dump(res, fh, indent=2)

    print(f"=== Cycle 3b Stage-1 calibration gate ===")
    if res.get("per_control"):
        print(f"{'control':16s} {'n':>2s} {'mean':>7s} {'SD':>6s} {'SEM':>6s} {'exp':>7s}")
        for c in ORDER:
            p = res["per_control"].get(c)
            if p:
                print(f"{c:16s} {p['n']:2d} {p['mean']:7.2f} {p['sd']:6.2f} "
                      f"{p['sem']:6.2f} {p['experimental']:7.2f}")
    for k in ("G1", "G2p", "G3"):
        v = res.get(k)
        if isinstance(v, dict):
            print(f"  {k:4s} {'PASS' if v['pass'] else 'FAIL'}"
                  + (f"  slope {v['slope']} CI {v['ci95']}" if k == "G3" else ""))
    print(f"VERDICT: {res['verdict']}")
    if res["verdict"] != "PASS":
        print("Stage 2 is NOT authorised. Per the pre-registration, cycle 3b terminates\n"
              "and reports a negative methodological result. The project recommendation\n"
              "stands unchanged: radioligand competition binding on YGGFEVVG and YGGFDIIG.")
    # exit 0 on a clean evaluation regardless of verdict; a FAIL is a RESULT, not
    # an error. Callers read gate_verdict.json. Exit 2 only if evaluation itself broke.
    sys.exit(0)


if __name__ == "__main__":
    main()
