#!/usr/bin/env python3
"""Score the Cycle 8 TI campaign against the gates pre-registered in CYCLE8_DESIGN.md.

Gates are evaluated in order and C5 is refused unless C1-C4 all pass. Usage:
    gate_ti.py <ti_results.csv> <fep_controls.csv> [--out verdict.json]

ti_results.csv columns required:
    system, receptor, replicate, dG_kcal, dG_sem, min_overlap
"""
import sys, json, argparse
import numpy as np, pandas as pd
from scipy import stats

TARGET = "engPENK_YGGFEVVG"
RC_N7 = 0.754          # critical |r| for p<0.05 at n=7, from the pre-registration
OVERLAP_MIN = 0.03
REP_TOL = 1.5

def ddg_per_system(df):
    """delta - mu, averaged over replicates; SEM from replicate spread when n>1."""
    rows = []
    for sysname, g in df.groupby("system"):
        d = g[g.receptor == "OPRD1"]; m = g[g.receptor == "OPRM1"]
        if d.empty or m.empty:
            rows.append({"system": sysname, "ddG": np.nan, "ddG_sem": np.nan,
                         "n_rep": 0, "note": "missing a receptor arm"}); continue
        per_rep = []
        for rep in sorted(set(d.replicate) & set(m.replicate)):
            dv = d[d.replicate == rep].dG_kcal.mean()
            mv = m[m.replicate == rep].dG_kcal.mean()
            per_rep.append(dv - mv)
        per_rep = np.array(per_rep, dtype=float)
        sem = (per_rep.std(ddof=1) / np.sqrt(len(per_rep))) if len(per_rep) > 1 else np.nan
        rows.append({"system": sysname, "ddG": float(per_rep.mean()),
                     "ddG_sem": float(sem) if sem == sem else None,
                     "n_rep": len(per_rep), "rep_spread": float(np.ptp(per_rep)) if len(per_rep) > 1 else None,
                     "note": ""})
    return pd.DataFrame(rows)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("results"); ap.add_argument("controls")
    ap.add_argument("--out", default="verdict_ti.json")
    a = ap.parse_args()
    R = pd.read_csv(a.results); C = pd.read_csv(a.controls)
    need = {"system","receptor","replicate","dG_kcal","min_overlap"}
    missing = need - set(R.columns)
    if missing:
        sys.exit(f"results file lacks required columns: {sorted(missing)}")

    D = ddg_per_system(R)
    ref = dict(zip(C.name, C.ddG_exp))
    D["ddG_exp"] = D.system.map(ref)
    ctl = D[D.ddG_exp.notna() & D.ddG.notna()].copy()
    v = {"n_controls_scored": int(len(ctl)), "gates": {}}

    # C1 - signs
    ctl["sign_ok"] = np.sign(ctl.ddG) == np.sign(ctl.ddG_exp)
    n_ok = int(ctl.sign_ok.sum())
    v["gates"]["C1_signs"] = {"pass": bool(n_ok >= 6), "correct": n_ok, "of": int(len(ctl)),
                              "required": "at least 6 of 7"}
    # C2 - correlation
    if len(ctl) >= 3:
        r, p = stats.pearsonr(ctl.ddG, ctl.ddG_exp)
        rho, prho = stats.spearmanr(ctl.ddG, ctl.ddG_exp)
    else:
        r = p = rho = prho = float("nan")
    v["gates"]["C2_correlation"] = {"pass": bool(abs(r) > RC_N7), "pearson_r": None if r != r else round(float(r),4),
        "p": None if p != p else round(float(p),4), "spearman_rho": None if rho != rho else round(float(rho),4),
        "required": f"|r| > {RC_N7}"}
    # C3 - lambda overlap across EVERY window of EVERY leg, controls and target alike
    worst = float(R.min_overlap.min())
    bad = R[R.min_overlap < OVERLAP_MIN][["system","receptor","replicate","min_overlap"]]
    v["gates"]["C3_overlap"] = {"pass": bool(worst >= OVERLAP_MIN), "worst_overlap": round(worst,4),
        "required": f">= {OVERLAP_MIN} everywhere", "failing_legs": bad.to_dict("records")[:10]}
    # C4 - replicate agreement, controls only (target has no reference to check against)
    spread = ctl[["system","rep_spread"]].dropna()
    worst_sp = float(spread.rep_spread.max()) if len(spread) else float("nan")
    v["gates"]["C4_replicates"] = {"pass": bool(worst_sp < REP_TOL) if worst_sp == worst_sp else False,
        "worst_spread_kcal": None if worst_sp != worst_sp else round(worst_sp,3),
        "required": f"< {REP_TOL} kcal/mol for every control"}

    gated = all(g["pass"] for k, g in v["gates"].items())
    tgt = D[D.system == TARGET]
    if gated and len(tgt):
        row = tgt.iloc[0]
        v["C5_target"] = {"reported": True, "system": TARGET, "ddG": round(float(row.ddG),3),
            "ddG_sem": row.ddG_sem, "n_rep": int(row.n_rep),
            "interpretation": ("delta-preferring" if row.ddG > 0 else "mu-preferring"),
            "caveat": "binding preference only; says nothing about agonist efficacy"}
    else:
        v["C5_target"] = {"reported": False,
            "reason": "one or more of C1-C4 failed; per pre-registration the target ddG is withheld",
            "failed_gates": [k for k, g in v["gates"].items() if not g["pass"]]}
    v["verdict"] = "PASS" if gated else "FAIL"
    D.to_csv(a.out.replace(".json", "_per_system.csv"), index=False)
    with open(a.out, "w") as f: json.dump(v, f, indent=2)
    print(json.dumps(v, indent=2))
    return 0 if gated else 3

if __name__ == "__main__":
    sys.exit(main())
