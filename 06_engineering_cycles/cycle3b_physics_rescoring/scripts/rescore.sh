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

# gmx_MMPBSA's find_progs() locates cpptraj/tleap/parmchk2/sander with
# shutil.which(path=os.environ['PATH']) -- it ignores the absolute paths used elsewhere
# in this script, so $E/bin MUST be on PATH or it aborts with
#   MMPBSA_Error: Could not find necessary program [cpptraj]
#
# ORDER IS LOAD-BEARING. find_progs uses ONE search path for every program, and it also
# picks up `gmx` from it. $E/bin ships GROMACS 2023.4, which CANNOT read a .tpr written
# by the 2024.5 build used for production (gmx check -s fails with "Error in user input").
# gmxcuda/bin must come FIRST so `gmx` resolves to 2024.5, with $E/bin behind it supplying
# the AmberTools binaries (verified above as not shadowed by gmxcuda/bin).
export PATH="$(dirname "$GMX"):$E/bin:$PATH"
command -v cpptraj >/dev/null || { echo "FAIL: cpptraj not on PATH after export"; exit 2; }
_gv=$(gmx --version 2>/dev/null | awk '/^GROMACS version/{print $3}')
case "$_gv" in
  2024.*|2025.*|2026.*) echo "  PATH gmx = $_gv (can read the production tpr)" ;;
  *) echo "FAIL: PATH gmx resolves to '$_gv'; cannot read the 2024.5 production tpr"; exit 2 ;;
esac

# Layout matches run_prod.sh exactly: SYS=$W/systems/$TAG, R=$SYS/rep$REP.
SYS=$W/systems/$TAG
RUN=$SYS/rep$REP
[ -d "$RUN" ] || { echo "FAIL: $RUN does not exist -- production has not run for $TAG rep$REP"; exit 2; }
cd "$RUN"

# A PROD_NSTEPS-truncated run is a pipeline test, not a replicate. Refuse it:
# rescoring a short trajectory would silently produce a plausible-looking dG.
if [ -f TRUNCATED_NOT_FOR_ANALYSIS ]; then
  echo "FAIL: $TAG rep$REP is a TRUNCATED validation run, not production:"
  cat TRUNCATED_NOT_FOR_ANALYSIS
  echo "Refusing to rescore. Delete the marker only if you re-ran full production."
  exit 3
fi
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
GREC=$(awk '/^\[ *Receptor *\]/{print n+0; f=1} /^\[/{n++} END{if(!f) exit 1}' mmgbsa.ndx)
GLIG=$(awk '/^\[ *Ligand *\]/{print n+0; f=1} /^\[/{n++} END{if(!f) exit 1}' mmgbsa.ndx)
[ -n "$GREC" ] && [ -n "$GLIG" ] || { echo "FAIL: Receptor/Ligand groups not found in mmgbsa.ndx"; exit 2; }
case "$GREC$GLIG" in *[!0-9]*) echo "FAIL: non-numeric group index (GREC='$GREC' GLIG='$GLIG')"; exit 2;; esac
[ "$GREC" != "$GLIG" ] || { echo "FAIL: Receptor and Ligand resolved to the same group index $GREC"; exit 2; }
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

# ---- membrane handling: measure, then reduce the topology ---------------------
# These are POPC-embedded GPCRs. gmx_MMPBSA's cleantop() drops water and ions from
# [ molecules ] but KEEPS the lipids, so system.top describes 274 POPC copies that
# mmgbsa.ndx does not contain, and it aborts with
#   "The complex index has fewer atoms than the topology."
#
# Implicit-solvent GB has no lipid phase, so keeping the bilayer would have it modelled
# as water anyway. Reducing the topology to the solute is only defensible while the
# peptide does not touch lipid -- so that is MEASURED here, per run, not assumed.
{ cat index.ndx; echo; sed -n '/^\[ *Ligand *\]/,$p' mmgbsa.ndx; } > .contact.ndx
"$GMX" mindist -f prod.xtc -s prod.tpr -n .contact.ndx -b "$TBEGIN" \
    -od .mindist.xvg -on .numcont.xvg -d 0.4 -group >/dev/null 2>&1 <<'SEL'
Ligand
MEMB
SEL
[ -s .mindist.xvg ] || { echo "FAIL: could not measure ligand-membrane distance"; exit 2; }

read -r MINDIST MEANDIST NFRD <<EOF
$(grep -v '^[#@]' .mindist.xvg | awk '{s+=$2; if(m==""||$2<m)m=$2; n++} END{printf "%.3f %.3f %d", m, s/n, n}')
EOF
read -r CFRAMES <<EOF
$(grep -v '^[#@]' .numcont.xvg | awk '{if($2>0)f++} END{print f+0}')
EOF
CPCT=$(python3 -c "print(f'{100.0*$CFRAMES/max($NFRD,1):.2f}')")
echo "  ligand-membrane: min ${MINDIST} nm, mean ${MEANDIST} nm over ${NFRD} frames; contacts<0.4nm in ${CFRAMES} (${CPCT}%)"
{ echo "# ligand-to-MEMB distance over the rescoring window, $TAG rep$REP"
  echo "# frames=$NFRD min_nm=$MINDIST mean_nm=$MEANDIST contact_frames_lt_0.4nm=$CFRAMES pct=$CPCT"
} > mindist_ligand_memb.txt

if [ "$(python3 -c "print(1 if $CPCT > 1.0 else 0)")" = "1" ]; then
  echo "FAIL: the peptide contacts the bilayer in ${CPCT}% of frames (min ${MINDIST} nm)."
  echo "      Reducing the topology to the solute would then discard interactions that do"
  echo "      NOT cancel between complex and free receptor. Rescoring refused for this run;"
  echo "      it needs a membrane-aware model (ipb/memopt), not a stripped topology."
  exit 4
fi

# Reduce to receptor+ligand only. The helper re-derives which molecules are solute from
# mmgbsa.ndx and aborts unless the kept set is EXACTLY the index, contiguous from atom 1.
"$PY" "$W/scripts/strip_membrane_top.py" system.top mmgbsa.ndx system_rescore.top \
  || { echo "FAIL: could not build the reduced rescoring topology"; exit 2; }

# ---- MM-GBSA ------------------------------------------------------------------
cp "$W/scripts/mmgbsa.in" ./mmgbsa.in
"$E/bin/gmx_MMPBSA" -O -nogui \
  -i mmgbsa.in \
  -cs prod.tpr -ci mmgbsa.ndx -cg "$GREC" "$GLIG" \
  -ct rescore_window.xtc -cp system_rescore.top \
  -o "${TAG}_r${REP}_FINAL.dat" -eo "${TAG}_r${REP}_perframe.csv" \
  > mmgbsa.log 2>&1 || { echo "FAIL: gmx_MMPBSA exited nonzero; see $RUN/mmgbsa.log"; tail -25 mmgbsa.log; exit 2; }

# 40 array tasks must not append to one CSV concurrently -- interleaved writes would
# corrupt lines. The array sets STAGE1_CSV per task; merged afterwards.
OUT="${STAGE1_CSV:-$W/results_stage1.csv}"
"$PY" "$W/scripts/collect_dg.py" "${TAG}_r${REP}_FINAL.dat" "$TAG" "$REP" >> "$OUT"
echo "RESCORE_OK $TAG rep$REP"
tail -3 "$OUT"
