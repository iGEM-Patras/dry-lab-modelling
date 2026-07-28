#!/usr/bin/env python3
"""Write index.ndx and locate the D-residue, WITHOUT guessing make_ndx group numbers.

Two bugs motivated this file:

1. `make_ndx` on this Amber/Lipid21 system emits MORE default groups than the 19 I
   assumed -- group 20 is already "non-Water". So `name 20 MEMB` renamed non-Water,
   and `name 21 SOLV` renamed my lipid union. The thermostat groups came out
   scrambled (MEMB=77351=non-Water, SOLV=71154=lipids) and the partition assertion
   correctly refused them. Hardcoding group numbers is unfixable in general; this
   script writes the groups directly instead.

2. The chirality gate was handed residue index 2 of the whole Protein group, i.e.
   the RECEPTOR's residue 2, which has no CB. The D-residue is residue 2 of the
   PEPTIDE, whose absolute index is (n_receptor_residues + 2). tleap also strips the
   chain IDs the gate was relying on, so the peptide is located by topology instead:
   it is the last covalently-connected molecule made of amino acids.
"""
import sys, collections
import parmed as pmd

top, gro, out_ndx, out_meta = sys.argv[1:5]
p = pmd.load_file(top, xyz=gro)

AA = set("""ALA ARG ASN ASP CYS GLN GLU GLY HIS ILE LEU LYS MET PHE PRO SER THR TRP
TYR VAL HID HIE HIP CYX ASH GLH LYN NALA NARG NASN NASP NCYS NGLN NGLU NGLY NHIS
NILE NLEU NLYS NMET NPHE NPRO NSER NTHR NTRP NTYR NVAL CALA CARG CASN CASP CCYS
CGLN CGLU CGLY CHIS CILE CLEU CLYS CMET CPHE CPRO CSER CTHR CTRP CTYR CVAL
NHE NME ACE""".split())
LIP = {"PA", "PC", "OL"}
SOL = {"WAT", "HOH", "TIP3", "Na+", "Cl-", "NA", "CL"}

groups = collections.OrderedDict()
groups["System"]  = [a.idx + 1 for a in p.atoms]
groups["Protein"] = [a.idx + 1 for a in p.atoms if a.residue.name in AA]
groups["MEMB"]    = [a.idx + 1 for a in p.atoms if a.residue.name in LIP]
groups["SOLV"]    = [a.idx + 1 for a in p.atoms if a.residue.name in SOL]

unclassified = sorted({a.residue.name for a in p.atoms
                       if a.residue.name not in AA | LIP | SOL})
if unclassified:
    sys.exit(f"FAIL: unclassified residues would fall outside every thermostat "
             f"group: {unclassified}")

n = {k: len(v) for k, v in groups.items()}
part = n["Protein"] + n["MEMB"] + n["SOLV"]
print(f"  Protein {n['Protein']} + MEMB {n['MEMB']} + SOLV {n['SOLV']} = {part} "
      f"/ System {n['System']}")
if part != n["System"]:
    sys.exit(f"FAIL: thermostat groups do not partition the system "
             f"({part} != {n['System']})")
print("  groups partition the system exactly")

# ---- locate the peptide: last chain of amino acids, 3-12 residues long ----------
prot_res = [r for r in p.residues if r.name in AA]
# split into covalently connected molecules by walking bonds between consecutive residues
mols, cur = [], [prot_res[0]]
for a, b in zip(prot_res, prot_res[1:]):
    linked = any(bd.atom2.residue is b or bd.atom1.residue is b
                 for at in a.atoms for bd in at.bonds
                 if bd.atom1.residue in (a, b) and bd.atom2.residue in (a, b))
    if linked and b.idx == a.idx + 1:
        cur.append(b)
    else:
        mols.append(cur); cur = [b]
mols.append(cur)
sizes = [len(m) for m in mols]
pep = next((m for m in reversed(mols) if 3 <= len(m) <= 12), None)
print(f"  protein molecules by residue count: {sizes}")
if pep is None:
    sys.exit(f"FAIL: no peptide-sized chain found among {sizes}")
print(f"  peptide: {'-'.join(r.name for r in pep)}  (residues "
      f"{pep[0].idx+1}-{pep[-1].idx+1}, 1-based over the whole system)")

with open(out_meta, "w") as fh:
    fh.write(f"PEP_FIRST_RES={pep[0].idx+1}\nPEP_LAST_RES={pep[-1].idx+1}\n"
             f"PEP_NRES={len(pep)}\n"
             f"PEP_SEQ={'-'.join(r.name for r in pep)}\n")
    for i, r in enumerate(pep, start=1):
        fh.write(f"PEP_RES{i}={r.name}:{r.idx+1}\n")

with open(out_ndx, "w") as fh:
    for name, idxs in groups.items():
        fh.write(f"[ {name} ]\n")
        for i in range(0, len(idxs), 15):
            fh.write(" ".join(f"{x:6d}" for x in idxs[i:i+15]) + "\n")
print(f"  wrote {out_ndx} ({len(groups)} groups) and {out_meta}")
