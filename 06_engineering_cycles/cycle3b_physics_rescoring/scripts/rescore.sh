#!/bin/bash
# Cycle 3b Stage-1 MM-GBSA rescoring — one run (one system, one replicate).
#
# WHY THIS EXISTS
#   run_prod.sh ends at production MD. Nothing in the pipeline computed dG_bind,
#   so gate.py had no input. This is the missing step between them.
#
# WHAT IT DOES NOT DO
#   No entropy term (design: qh/IE both unreliable at this cost). The output is an
#   enthalpy-dominated effective energy, NOT a binding free energy. gate.py compares
#   DIFFERENCES (ddG_sel), where the systematic offset largely cancels; absolute
#   values are not interpretable as affinities.
#
# Usage: rescore.sh <TAG> <REP>   e.g. rescore.sh c3b_dtII_DOR 1
set -euo pipefail

TAG=${1:?TAG required}; REP=${2:?REP required}
W=/data/users/kzanaj/boltz_dock/cycle3b
E=/data/users/kzanaj/envs/gmxmmpbsa
GMX=/data/users/kzanaj/envs/gmxcuda/bin/gmx
PY=$E/bin/python
export AMBERHOME=$E

# Layout matches run_prod.sh exactly: SYS=$W/systems/$TAG, R=$SYS/rep$REP.
SYS=$W/systems/$TAG
RUN=$SYS/rep$REP
[ -d "$RUN" ] || { echo "FAIL: $RUN does not exist -- production has not run for $TAG rep$REP"; exit 2; }
cd "$RUN"
for f in prod.xtc prod.tpr system.top index.ndx pepmeta.txt; do
  [ -s "$f" ] || { echo "FAIL: $RUN/$f missing or empty"; exit 2; }
done

# ---- last 10 ns only (design: equilibration discarded) -----------------------
# Production is 15 ns; keep t >= 5000 ps. Do not assume frame counts -- read them.
TEND=$($GMX check -f prod.xtc 2>&1 | awk '/Last frame/{print $NF}')
[ -n "$TEND" ] || { echo "FAIL: could not read trajectory end time"; exit 2; }
TBEGIN=$(python3 -c "print(max(0.0, float('$TEND') - 10000.0))")
echo "trajectory ends $TEND ps; rescoring window ${TBEGIN}-${TEND} ps (last 10 ns)"

# 100 evenly spaced snapshots across that window
DT=$(python3 -c "print(round((float('$TEND')-float('$TBEGIN'))/100.0, 4))")
echo System | $GMX trjconv -f prod.xtc -s prod.tpr -n index.ndx \
    -b "$TBEGIN" -e "$TEND" -dt "$DT" -pbc mol -o rescore_window.xtc >/dev/null 2>&1

NFR=$($GMX check -f rescore_window.xtc 2>&1 | awk '/^Step/{print $2}')
echo "frames extracted: ${NFR:-unknown}"
if [ -n "${NFR:-}" ] && [ "$NFR" -lt 90 ]; then
  echo "FAIL: only $NFR frames in the last-10ns window; expected ~100."
  echo "      A short/crashed production run must not be silently rescored on fewer frames."
  exit 2
fi

# ---- receptor / ligand index groups ------------------------------------------
# index.ndx carries only System/Protein/MEMB/SOLV (thermostat groups). MM-GBSA needs
# the complex split into receptor and ligand. Built from pepmeta.txt, which located
# the peptide by bonded topology -- NOT by guessing residue numbers.
"$PY" "$W/scripts/make_mmgbsa_groups.py" system.top prod.tpr pepmeta.txt index.ndx mmgbsa.ndx

# group indices are read back from the file we just wrote, never hardcoded
GREC=$(awk '/^\[ *Receptor *\]/{print n} /^\[/{n++}' mmgbsa.ndx)
GLIG=$(awk '/^\[ *Ligand *\]/{print n} /^\[/{n++}' mmgbsa.ndx)
[ -n "$GREC" ] && [ -n "$GLIG" ] || { echo "FAIL: Receptor/Ligand groups not found"; exit 2; }
echo "index groups: Receptor=$GREC Ligand=$GLIG"

# ---- chirality across the rescored window, not just the MD endpoints ---------
# run_prod.sh gates post-NVT/NPT/production endpoints. The D-centre could invert
# mid-production and be restored by the final frame, so assert on frames drawn
# from the window actually being scored.
#
# chirality.py takes `assert <pdb> <resid> --by-position` on a peptide-only PDB
# (its --by-position index is 1-based WITHIN that file), matching run_prod.sh's
# gate(). DRES_REL is the D-residue index within the peptide, or the string
# 'none' for all-L controls (met-enkephalin) -- same sentinel run_prod.sh uses.
# It is a RUN PARAMETER, not a pepmeta.txt field: pepmeta.txt records only the
# peptide's identity and residue span, so the value is taken from peptide_spec.sh,
# the design table of record, exactly as run_prod.sh does.
. "$W/scripts/peptide_spec.sh"
load_peptide_spec "$TAG" || { echo "FAIL: refusing to rescore $TAG with unknown chemistry"; exit 2; }
DRES="$SPEC_DRES"
if [ "$DRES" != "none" ]; then
  for FR in 0 25 50 75 100; do
    echo Ligand | $GMX trjconv -f rescore_window.xtc -s prod.tpr -n mmgbsa.ndx \
        -dump "$(python3 -c "print(float('$TBEGIN') + ($FR/100.0)*(float('$TEND')-float('$TBEGIN')))")" \
        -o "chk_${FR}.pdb" >/dev/null 2>&1
    [ -s "chk_${FR}.pdb" ] || { echo "FAIL: could not extract peptide at ${FR}% of window"; exit 2; }
    "$PY" "$W/scripts/chirality.py" assert "chk_${FR}.pdb" "$DRES" --by-position \
      || { echo "FAIL: D-centre inverted at ${FR}% of the rescoring window -- run DISCARDED per design"; exit 3; }
  done
  echo "  chirality retained across the rescoring window (5 checkpoints)"
else
  echo "  no D-residue in this peptide (DRES_REL=0) -- chirality check not applicable"
fi

# ---- MM-GBSA ------------------------------------------------------------------
cp "$W/scripts/mmgbsa.in" ./mmgbsa.in
"$E/bin/gmx_MMPBSA" -O -nogui \
  -i mmgbsa.in \
  -cs prod.tpr -ci mmgbsa.ndx -cg "$GREC" "$GLIG" \
  -ct rescore_window.xtc -cp system.top \
  -o "${TAG}_r${REP}_FINAL.dat" -eo "${TAG}_r${REP}_perframe.csv" \
  > mmgbsa.log 2>&1 || { echo "FAIL: gmx_MMPBSA exited nonzero; see $RUN/mmgbsa.log"; tail -25 mmgbsa.log; exit 2; }

"$PY" "$W/scripts/collect_dg.py" "${TAG}_r${REP}_FINAL.dat" "$TAG" "$REP" >> "$W/results_stage1.csv"
echo "RESCORE_OK $TAG rep$REP"
tail -3 "$W/results_stage1.csv"
