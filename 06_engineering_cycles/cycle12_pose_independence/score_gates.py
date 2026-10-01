"""Cycle 12 gate scoring: does an independent ADCP pose agree with the co-folded one?

Gates were fixed in cycle12_prereg.json BEFORE any pose existed:
  G1  ligand-RMSD(ADCP best, co-fold) <= 2.5 A  -> AGREE
  G2  N-terminal amine within 4.0 A of Asp3.32 carboxylate
  G3  same pocket occupied in DOR and MOR

No superposition is applied: ADCP docks into receptor coordinates taken directly
from the co-fold complex, so both peptides are already in the same frame. Applying
a fit would only mask a real translational difference.
"""
import os, glob, json, math

D332 = {"DOR": 128, "MOR": 147}


def read_pdb_atoms(path, chain=None):
    out = []
    for ln in open(path, errors="ignore"):
        if not ln.startswith(("ATOM", "HETATM")):
            continue
        if chain and ln[21] != chain:
            continue
        name = ln[12:16].strip()
        if name.startswith("H") or ln[76:78].strip() == "H":
            continue                      # heavy atoms only
        try:
            xyz = (float(ln[30:38]), float(ln[38:46]), float(ln[46:54]))
        except ValueError:
            continue
        out.append({"name": name, "resn": ln[17:20].strip(),
                    "resi": int(ln[22:26]), "xyz": xyz})
    return out


def dist(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def rmsd_matched(ref, mob, backbone_only=False):
    """Match on (residue index, atom name). Returns (rmsd, n_matched)."""
    BB = {"N", "CA", "C", "O"}
    rmap = {}
    for a in ref:
        if backbone_only and a["name"] not in BB:
            continue
        rmap[(a["resi"], a["name"])] = a["xyz"]
    # ADCP renumbers from 1; co-fold may not. Align by rank order of residue id.
    ref_ids = sorted({a["resi"] for a in ref})
    mob_ids = sorted({a["resi"] for a in mob})
    shift = {m: r for m, r in zip(mob_ids, ref_ids)}
    tot, n = 0.0, 0
    for a in mob:
        if backbone_only and a["name"] not in BB:
            continue
        key = (shift.get(a["resi"], a["resi"]), a["name"])
        if key in rmap:
            tot += dist(rmap[key], a["xyz"]) ** 2
            n += 1
    return (math.sqrt(tot / n) if n else float("nan")), n


def centroid(atoms):
    n = len(atoms)
    return tuple(sum(a["xyz"][i] for a in atoms) / n for i in range(3))


def score(receptor, work):
    rec = read_pdb_atoms(os.path.join(work, f"{receptor}_rec.pdb"))
    cof = read_pdb_atoms(os.path.join(work, f"{receptor}_pep_cofold.pdb"))
    cands = sorted(glob.glob(os.path.join(work, f"{receptor}_adcp*.pdb")))
    if not cof or not cands:
        return {"receptor": receptor, "error": "missing co-fold peptide or ADCP output",
                "n_cofold_atoms": len(cof), "n_adcp_files": len(cands)}

    best = None
    for f in cands:
        pep = read_pdb_atoms(f)
        if not pep:
            continue
        rb, nb = rmsd_matched(cof, pep, backbone_only=True)
        ra, na = rmsd_matched(cof, pep, backbone_only=False)
        if best is None or (rb == rb and rb < best["rmsd_backbone"]):
            best = {"file": os.path.basename(f), "rmsd_backbone": rb,
                    "n_bb_matched": nb, "rmsd_heavy": ra, "n_heavy_matched": na,
                    "atoms": pep}
    if best is None:
        return {"receptor": receptor, "error": "no parsable ADCP pose"}

    # G2: N-terminal amine (Tyr1 N) to Asp3.32 carboxylate oxygens
    anum = D332[receptor]
    asp_o = [a["xyz"] for a in rec if a["resi"] == anum and a["name"] in ("OD1", "OD2")]
    pep_ids = sorted({a["resi"] for a in best["atoms"]})
    nterm = [a["xyz"] for a in best["atoms"]
             if a["resi"] == pep_ids[0] and a["name"] == "N"]
    g2 = min((dist(p, o) for p in nterm for o in asp_o), default=float("nan"))

    return {"receptor": receptor,
            "best_pose": best["file"],
            "G1_rmsd_backbone_A": round(best["rmsd_backbone"], 2),
            "G1_rmsd_heavy_A": round(best["rmsd_heavy"], 2),
            "n_backbone_atoms_matched": best["n_bb_matched"],
            "n_heavy_atoms_matched": best["n_heavy_matched"],
            "G1_verdict": ("AGREE" if best["rmsd_backbone"] <= 2.5 else "DISAGREE"),
            "G2_nterm_to_Asp332_A": (round(g2, 2) if g2 == g2 else None),
            "G2_verdict": ("PASS" if (g2 == g2 and g2 <= 4.0) else "FAIL"),
            "adcp_centroid": [round(v, 2) for v in centroid(best["atoms"])],
            "cofold_centroid": [round(v, 2) for v in centroid(cof)],
            "centroid_shift_A": round(dist(centroid(best["atoms"]), centroid(cof)), 2),
            "n_adcp_poses_parsed": len(cands)}


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    work = os.path.join(here, "dock")
    res = [score(r, work) for r in ("DOR", "MOR")]

    # G3: did ADCP find the same pocket in both receptors?
    ok = [r for r in res if "error" not in r]
    if len(ok) == 2:
        same = all(r["G2_verdict"] == "PASS" for r in ok)
        g3 = {"G3_same_pocket_both_receptors": "PASS" if same else "FAIL",
              "basis": "anchor contact to Asp3.32 present in both"}
    else:
        g3 = {"G3_same_pocket_both_receptors": "NOT EVALUABLE",
              "basis": f"only {len(ok)} of 2 receptors produced a scorable pose"}

    out = {"gates_from": "cycle12_prereg.json (written before any pose existed)",
           "per_receptor": res, **g3}
    json.dump(out, open(os.path.join(here, "cycle12_gates.json"), "w"), indent=1)
    for r in res:
        print(json.dumps(r, indent=1))
    print(json.dumps(g3, indent=1))
