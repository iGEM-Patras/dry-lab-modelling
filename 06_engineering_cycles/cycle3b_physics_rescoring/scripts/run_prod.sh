#!/bin/bash
# Cycle 3b Stage 1 - production replicate. One (system, replicate) pair per array task.
#
# Each replicate re-runs NVT+NPT from the SAME minimised structure but with a
# DIFFERENT velocity seed, then 20 ns production. Independent velocities are what
# make the three replicates independent samples; re-using one equilibration would
# give three correlated trajectories and a dispersion estimate that is too small.
#
# Chirality is asserted after minimisation, after NPT, and after production. A run
# whose D-centre inverted is DISCARDED, never averaged in -- ff14SB has no improper
# term on the sp3 alpha-carbon, so nothing else can detect it.
set -euo pipefail

TAG="${1:?usage: run_prod.sh <tag> <rep>}"
REP="${2:?usage: run_prod.sh <tag> <rep>}"

W=/data/users/kzanaj/boltz_dock/cycle3b
E=/data/users/kzanaj/envs/gmxmmpbsa
GMX=/data/users/kzanaj/envs/gmxcuda/bin/gmx
export AMBERHOME=$E
PY=$E/bin/python

SYS=$W/systems/$TAG
R=$SYS/rep$REP
mkdir -p "$R"; cd "$R"

for f in system.top system.gro index.ndx pepmeta.txt min.gro; do
  [ -f "$SYS/$f" ] || { echo "FAIL: $TAG missing $f -- build incomplete"; exit 1; }
done
cp $SYS/{system.top,index.ndx,pepmeta.txt} .
source $SYS/pepmeta.txt     # PEP_FIRST_RES PEP_LAST_RES PEP_NRES PEP_SEQ

# ---- pre-flight: assert the species is right --------------------------------
# AMIDE=yes for every control except met-enkephalin, which is natively a free acid.
AMIDE="${3:-yes}"
# DRES_REL is the D-residue index WITHIN THE PEPTIDE, or 'none' for all-L controls.
DRES_REL="${4:-none}"

$PY - "$SYS/system.top" "$AMIDE" "$PEP_FIRST_RES" "$PEP_LAST_RES" <<'PYEOF'
import sys, parmed as pmd
top, amide, first, last = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
res = pmd.load_file(top).residues
pep = [r.name for r in res[first-1:last]]
cterm = pep[-1]
print(f"  peptide in topology: {'-'.join(pep)}")
if amide == "yes" and cterm != "NHE":
    sys.exit(f"FAIL: expected a C-terminal NHE amide, found {cterm}. This system is "
             f"the FREE ACID -- the wrong chemical species. Rebuild it.")
if amide == "no" and cterm == "NHE":
    sys.exit("FAIL: this control is natively a free acid but carries an NHE cap.")
print(f"  C-terminus: {'primary amide (NHE)' if cterm=='NHE' else cterm + ' (free acid, as intended)'}")
PYEOF

# Absolute residue index of the D-centre, derived from the peptide's own offset.
if [ "$DRES_REL" = "none" ]; then
  DRES_ABS=none
else
  DRES_ABS=$(( PEP_FIRST_RES + DRES_REL - 1 ))
  echo "  D-centre: peptide residue $DRES_REL -> absolute $DRES_ABS"
fi

gate () {  # gate <stage> <coords.gro>
  local stage="$1" coords="$2"
  if [ "$DRES_ABS" = "none" ]; then echo "  [gate:$stage] no D-residue, skipped"; return 0; fi
  # Read coordinates from the .gro, NOT a PDB. At 270,287 atoms the PDB atom-serial
  # field overflows (99,999 max) and parmed rejects the file outright
  # ("Coordinate mismatch in model 1"). .gro has no such limit.
  #
  # The peptide is selected by residue-index range from system.top, because
  # editconf/trjconv do not preserve the topology's solvent ORDER -- addressing the
  # whole structure by absolute position landed on an Na+ ion instead of Ala2.
  $PY - "$coords" "$PEP_FIRST_RES" "$PEP_LAST_RES" "pep_${stage}.pdb" <<'PYEOF'
import sys, parmed as pmd
src, lo, hi, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
st = pmd.load_file("system.top")
st.coordinates = pmd.load_file(src).coordinates
pep = st[f":{lo}-{hi}"]
seq = "-".join(r.name for r in pep.residues)
assert len(pep.residues) == hi - lo + 1, f"selected {len(pep.residues)} residues, want {hi-lo+1}"
pep.save(out, overwrite=True)
print(f"  [gate] peptide extracted ({len(pep.atoms)} atoms): {seq}")
PYEOF
  [ -s "pep_${stage}.pdb" ] || { echo "FAIL: could not extract peptide at stage '$stage'"; exit 1; }
  $PY $W/scripts/chirality.py assert "pep_${stage}.pdb" "$DRES_REL" --by-position \
    || { echo "FAIL: chirality inverted or unreadable at stage '$stage' - DISCARD this run"; exit 3; }
  echo "  [gate:$stage] chirality OK"
}

SEED=$(( 20260728 + 1000*REP + $(echo "$TAG" | cksum | cut -d" " -f1) % 1000 ))
echo "=== $TAG rep$REP | seed $SEED | peptide $PEP_SEQ ==="

# ---- NVT with replicate-specific velocities --------------------------------
sed "s/^gen[-_]seed[[:space:]]*=.*/gen-seed = $SEED/" $W/scripts/nvt.mdp > nvt_r.mdp
grep -qE "^gen-seed[[:space:]]*=[[:space:]]*$SEED\b" nvt_r.mdp || { echo "FAIL: seed not set"; exit 1; }
$GMX grompp -f nvt_r.mdp -c $SYS/min.gro -p system.top -n index.ndx -o nvt.tpr -maxwarn 2
$GMX mdrun -deffnm nvt -nb gpu -ntmpi 1 -ntomp 8
gate "post-NVT" nvt.gro

$GMX grompp -f $W/scripts/npt.mdp -c nvt.gro -t nvt.cpt -p system.top -n index.ndx -o npt.tpr -maxwarn 2
$GMX mdrun -deffnm npt -nb gpu -ntmpi 1 -ntomp 8
gate "post-NPT" npt.gro

# ---- production ------------------------------------------------------------
$GMX grompp -f $W/scripts/prod.mdp -c npt.gro -t npt.cpt -p system.top -n index.ndx -o prod.tpr -maxwarn 2
$GMX mdrun -deffnm prod -nb gpu -ntmpi 1 -ntomp 8
gate "post-production" prod.gro

grep -E "Performance|ns/day" prod.log | tail -2
echo "PROD_OK $TAG rep$REP"
