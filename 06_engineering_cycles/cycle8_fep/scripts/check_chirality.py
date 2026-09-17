
import sys, math
gro = sys.argv[1]
lines = open(gro).read().split("\n")
nat = int(lines[1])
atoms = []
for ln in lines[2:2+nat]:
    if len(ln) < 44: continue
    atoms.append({"resid": int(ln[0:5]), "resname": ln[5:10].strip(),
                  "name": ln[10:15].strip(), "idx": int(ln[15:20]),
                  "x": float(ln[20:28]), "y": float(ln[28:36]), "z": float(ln[36:44])})
byres = {}
for a in atoms:
    byres.setdefault((a["resid"], a["resname"]), {})[a["name"]] = (a["x"], a["y"], a["z"])
def sv(r):
    try: N, CA, C, CB = r["N"], r["CA"], r["C"], r["CB"]
    except KeyError: return None
    u = [N[i]-CA[i] for i in range(3)]
    v = [C[i]-CA[i] for i in range(3)]
    w = [CB[i]-CA[i] for i in range(3)]
    cr = [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
    return sum(cr[i]*w[i] for i in range(3))
vals = [(k, sv(r)) for k, r in byres.items() if sv(r) is not None]
ala = [(k, s) for k, s in vals if k[1] in ("ALA", "DAL", "ALAD")]
print("residues with a full N/CA/C/CB set:", len(vals))
print("alanine-like residues:", len(ala))
neg = sum(1 for _, s in vals if s < 0); pos = len(vals) - neg
print("signed-volume sign across ALL chiral residues: negative %d, positive %d" % (neg, pos))
print("  -> the majority sign is the L convention for this build")
maj = -1 if neg > pos else 1
odd = [(k, round(s, 4)) for k, s in vals if (s < 0) != (maj < 0)]
print("residues with the MINORITY (inverted) sign: %d" % len(odd))
for k, s in odd[:12]:
    print("     resid %-5d %-5s signed_volume %+.4f   <- D-configuration" % (k[0], k[1], s))
if not odd:
    print("     NONE -> no D-residue present in this structure")
