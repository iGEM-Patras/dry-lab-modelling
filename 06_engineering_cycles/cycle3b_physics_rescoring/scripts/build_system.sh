#!/bin/bash
# Cycle 3b Stage 1 - build ONE control system end-to-end and benchmark it.
#
# Pipeline: extract co-folded complex -> (optional) install D-Ala2 by mirroring
#   -> orient in membrane normal (memembed) -> pack POPC bilayer + water + 0.15 M NaCl
#   -> parametrize ff14SB/Lipid21 -> minimise -> CHIRALITY GATE -> equilibrate
#   -> CHIRALITY GATE -> short production benchmark to measure ns/day.
#
# Usage: build_system.sh <tag> <dres|none>
#   tag  : e.g. c3b_dtII_DOR   (expects out_<tag>/ from the boltz run)
#   dres : residue index in the PEPTIDE chain to convert to D, or 'none'
set -euo pipefail

TAG="${1:?usage: build_system.sh <tag> <dres|none>}"
DRES="${2:-none}"

W=/data/users/kzanaj/boltz_dock/cycle3b
E=/data/users/kzanaj/envs/gmxmmpbsa
GMX=/data/users/kzanaj/envs/gmxcuda/bin/gmx
export AMBERHOME=$E
export PATH=$E/bin:$PATH
PY=$E/bin/python

SYS=$W/systems/$TAG
mkdir -p "$SYS"; cd "$SYS"

POSE=$(find $W/out_${TAG} -name "*model_0.pdb" | head -1)
[ -n "$POSE" ] || { echo "FAIL: no pose for $TAG"; exit 1; }
echo "pose: $POSE"

# ---- 1. split complex; strip Boltz artefacts -------------------------------
grep "^ATOM" "$POSE" | awk 'substr($0,22,1)=="A"' > rec_raw.pdb
grep "^ATOM" "$POSE" | awk 'substr($0,22,1)=="B"' > pep_raw.pdb
echo "receptor atoms: $(wc -l < rec_raw.pdb) | peptide atoms: $(wc -l < pep_raw.pdb)"

# ---- 2. install D-residue by geometric mirroring ---------------------------
if [ "$DRES" != "none" ]; then
  $PY $W/scripts/chirality.py invert pep_raw.pdb "$DRES" - pep_D.pdb
  $PY $W/scripts/chirality.py assert pep_D.pdb "$DRES" || { echo "FAIL: inversion did not take"; exit 1; }
  mv pep_D.pdb pep_chir.pdb
else
  cp pep_raw.pdb pep_chir.pdb
fi

# ---- 3. orient the COMPLEX along the membrane normal -----------------------
# IMPORTANT: orient receptor+peptide together as one rigid body. Orienting the
# receptor alone and re-appending the peptide would destroy the docked pose,
# because memembed applies a rotation+translation that the peptide must share.
cat rec_raw.pdb > complex_raw.pdb
echo "TER" >> complex_raw.pdb
cat pep_chir.pdb >> complex_raw.pdb
echo "END" >> complex_raw.pdb

ORIENT=""
if command -v memembed >/dev/null 2>&1; then
  if memembed -o complex_oriented.pdb complex_raw.pdb >memembed.log 2>&1; then
    # Verify the peptide survived: atom count preserved and the peptide is still
    # in contact with the receptor. A silent chain drop is the failure mode here.
    if $PY - <<PYEOF
import sys, numpy as np
def rd(f):
    A=[l for l in open(f) if l.startswith(("ATOM","HETATM"))]
    xyz=lambda l: np.array([float(l[30:38]),float(l[38:46]),float(l[46:54])])
    return A, {c: np.array([xyz(l) for l in A if l[21]==c]) for c in {l[21] for l in A}}
Ai,ci = rd("complex_raw.pdb"); Ao,co = rd("complex_oriented.pdb")
if len(Ai)!=len(Ao): print(f"  memembed changed atom count {len(Ai)}->{len(Ao)}"); sys.exit(1)
if set(ci)!=set(co):  print(f"  memembed changed chains {set(ci)}->{set(co)}"); sys.exit(1)
def mind(d):
    a,b=d["A"],d["B"]
    return float(np.sqrt(((a[:,None,:]-b[None,:,:])**2).sum(-1)).min())
d0,d1 = mind(ci), mind(co)
print(f"  min receptor-peptide distance: {d0:.2f} A -> {d1:.2f} A (rigid-body check)")
sys.exit(0 if abs(d0-d1) < 0.05 else 1)
PYEOF
    then cp complex_oriented.pdb complex_in.pdb; ORIENT="--preoriented"
    else echo "  memembed output rejected; letting memgen orient"; cp complex_raw.pdb complex_in.pdb
    fi
  else
    echo "  memembed failed; letting memgen orient"; cp complex_raw.pdb complex_in.pdb
  fi
else
  cp complex_raw.pdb complex_in.pdb
fi
echo "orientation: ${ORIENT:-memgen internal}"

# ---- 4. pack bilayer ------------------------------------------------------
packmol-memgen --pdb complex_in.pdb --lipids POPC --ratio 1 \
  --dist 15 --dist_wat 20 --salt --salt_c Na+ --saltcon 0.15 \
  --ffprot ff14SB --ffwat tip3p --parametrize --notprotonate \
  $ORIENT --overwrite --log memgen.log > memgen.out 2>&1 || {
    echo "FAIL: packmol-memgen"; tail -25 memgen.out; exit 1; }

PRM=$(ls *.prmtop 2>/dev/null | head -1); CRD=$(ls *.rst7 *.inpcrd 2>/dev/null | head -1)
[ -n "$PRM" ] && [ -n "$CRD" ] || { echo "FAIL: no topology produced"; tail -25 memgen.out; exit 1; }
echo "topology: $PRM | coords: $CRD"
$PY -c "
import parmed as pmd
p = pmd.load_file('$PRM', xyz='$CRD')
print(f'SYSTEM: {len(p.atoms)} atoms, {len(p.residues)} residues')
import collections
c = collections.Counter(r.name for r in p.residues)
print('  lipids POPC-units:', sum(v for k,v in c.items() if k in ('PC','OL','PA')))
print('  waters:', c.get('WAT',0), '| Na+:', c.get('Na+',0), '| Cl-:', c.get('Cl-',0))
print(f'  box: {p.box}')
p.save('system.top', overwrite=True); p.save('system.gro', overwrite=True)
print('  wrote GROMACS system.top + system.gro')
"
echo "BUILD_OK $TAG"
