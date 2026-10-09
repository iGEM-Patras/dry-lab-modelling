#!/bin/bash
# Cycle 3b Stage-1 MM-GBSA rescoring, one run (one system, one replicate).
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

# ---- frame selection ----------------------------------------------------------
# Two modes.
#
#   default (BOUND_MODE unset): last 10 ns, 100 evenly spaced snapshots.
#
#   BOUND_MODE=1: select only frames in which the peptide is genuinely IN THE POCKET,
#     drawn from the WHOLE trajectory, then subsample 100 of them. This exists because
#     9 of 40 replicates were refused by the membrane gate below -- the peptide leaves
#     the site and touches the bilayer during the last-10ns window. An energy averaged
#     over frames where the ligand has left the pocket is not a binding energy under any
#     solvation model, so the refusal was correct; but the frames where it IS bound still
#     carry the information we want.
#
#     gmx_MMPBSA 1.5.0.3 registers memopt/mthick/mctrdz on the &pb namelist ONLY, so there
#     is no implicit-membrane GB. Rescoring the escaped runs in PB would put them on a
#     different energy scale from the GB results for every other arm, and a delta/mu
#     comparison mixing the two is meaningless. Conditional-GB keeps all 40 commensurable.
#     See docs/MEMBRANE_RESCORING_OPTIONS.md.
#
#     A conditional energy MUST be reported with the residency fraction. It answers
#     "how tight is the bound pose while it exists", not "how strong is the binding".
TEND=$($GMX check -f prod.xtc 2>&1 | awk '/Last frame/{print $NF}')
[ -n "$TEND" ] || { echo "FAIL: could not read trajectory end time"; exit 2; }

if [ "${BOUND_MODE:-0}" = "1" ]; then
  MEMB_CUT=${MEMB_CUT:-0.4}
  RMSD_CUT=${RMSD_CUT:-0.52}
  MEMB_XVG=$W/frameclass/${TAG}_r${REP}_memb.xvg
  RMSD_XVG=$W/frameclass/${TAG}_r${REP}_ligrmsd.xvg
  for f in "$MEMB_XVG" "$RMSD_XVG"; do
    [ -s "$f" ] || { echo "FAIL: missing $f -- run classify_frames.sbatch first"; exit 2; }
  done

  "$PY" - "$MEMB_XVG" "$RMSD_XVG" "$MEMB_CUT" "$RMSD_CUT" > .bound_frames.ndx <<'PYEOF'
import sys
mp, rp, mc, rc = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
def rd(p):
    o = []
    for ln in open(p):
        if ln.startswith(("#", "@")):
            continue
        f = ln.split()
        if len(f) >= 2:
            o.append((float(f[0]), float(f[1])))
    return o
m, r = rd(mp), rd(rp)
n = min(len(m), len(r))
if n == 0:
    sys.exit("FAIL: empty per-frame series")
# The AND is only meaningful if both series share a time base -- verify, do not assume.
# Tolerance is half a frame interval: that is tight enough to catch a genuine off-by-one
# or a different stride, while ignoring the last-digit differences the two .xvg writers
# produce for the same time (e.g. 14.800000 vs 14.800001).
dt = (m[-1][0] - m[0][0]) / max(1, n - 1)
tol = max(0.5 * abs(dt), 1e-4)
for i in range(0, n, max(1, n // 50)):
    if abs(m[i][0] - r[i][0]) > tol:
        sys.exit("FAIL: memb/rmsd series time bases differ at index %d (%.6f vs %.6f, "
                 "tolerance %.6f) -- different stride or frame offset"
                 % (i, m[i][0], r[i][0], tol))
idx = [i for i in range(n) if m[i][1] > mc and r[i][1] <= rc]
if not idx:
    sys.exit("FAIL: no bound frames under memb>%g nm and rmsd<=%g nm" % (mc, rc))
k = max(1, len(idx) // 100)
sel = idx[::k][:100]
sys.stderr.write("bound frames %d of %d (%.1f%%), subsampled to %d\n"
                 % (len(idx), n, 100.0 * len(idx) / n, len(sel)))
# trjconv -fr wants an INDEX FILE of frame NUMBERS, and that numbering is ONE-BASED:
# verified 2026-08-31 -- emitting the 0-based index 56 extracted t=550 ps, i.e. the 56th
# frame (0-based 55), not t=560 ps. Emitting i+1 is therefore required. The extracted
# times are cross-checked against .bound_times.txt after extraction, so a future change
# to this convention fails loudly instead of silently scoring the wrong frames.
with open(".bound_times.txt", "w") as fh:
    fh.write("\n".join("%.6f" % (m[i][0] * 1000.0) for i in sel) + "\n")
print("[ frames ]")
print("\n".join(str(i + 1) for i in sel))
PYEOF
  [ -s .bound_frames.ndx ] || { echo "FAIL: bound-frame selection produced nothing"; exit 2; }
  NSEL=$(grep -cv '^\[' .bound_frames.ndx)
  echo "BOUND_MODE: $NSEL frames selected (memb>${MEMB_CUT} nm, ligand RMSD<=${RMSD_CUT} nm)"

  echo System | $GMX trjconv -f prod.xtc -s prod.tpr -n index.ndx \
      -fr .bound_frames.ndx -pbc mol -o rescore_window.xtc >/dev/null 2>&1 \
      || { echo "FAIL: trjconv could not extract the selected bound frames"; exit 2; }
  # chirality checkpoints must sample the frames actually being scored
  TBEGIN=$(head -1 .bound_times.txt)
else
  TBEGIN=$(python3 -c "print(max(0.0, float('$TEND') - 10000.0))")
  echo "trajectory ends $TEND ps; rescoring window ${TBEGIN}-${TEND} ps (last 10 ns)"
  DT=$(python3 -c "print(round((float('$TEND')-float('$TBEGIN'))/100.0, 4))")
  echo System | $GMX trjconv -f prod.xtc -s prod.tpr -n index.ndx \
      -b "$TBEGIN" -e "$TEND" -dt "$DT" -pbc mol -o rescore_window.xtc >/dev/null 2>&1
fi

NFR=$($GMX check -f rescore_window.xtc 2>&1 | awk '/^Step/{print $2}')
echo "frames extracted: ${NFR:-unknown}"
if [ -n "${NFR:-}" ] && [ "$NFR" -lt 90 ]; then
  echo "FAIL: only $NFR frames extracted; expected ~100."
  echo "      A short/crashed run, or too few bound frames, must not be silently rescored."
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
  # Checkpoints must land INSIDE the extracted window. In bound mode the window is a
  # scattered subset of the trajectory, so interpolating TBEGIN..TEND would -dump times
  # that are absent; take the actual selected times instead.
  if [ "${BOUND_MODE:-0}" = "1" ]; then
    CHK_TIMES=$(awk 'NR==FNR{a[NR]=$1; n=NR; next} END{
        for (i=0; i<=4; i++) { k=int(i*(n-1)/4)+1; print a[k] } }' \
        .bound_times.txt .bound_times.txt)
  else
    CHK_TIMES=$(for FR in 0 25 50 75 100; do
        python3 -c "print(float('$TBEGIN') + ($FR/100.0)*(float('$TEND')-float('$TBEGIN')))"
      done)
  fi
  FR=0
  for T in $CHK_TIMES; do
    FR=$((FR+25))
    echo Ligand | $GMX trjconv -f rescore_window.xtc -s prod.tpr -n mmgbsa.ndx \
        -dump "$T" \
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
#
# In BOUND_MODE the contact measurement is made on rescore_window.xtc -- the frames
# actually being scored -- rather than on a time range of prod.xtc. Selection already
# excludes contacting frames, so this becomes a VERIFICATION of the selection rather
# than a filter: if it ever trips in bound mode, the selection logic is wrong.
{ cat index.ndx; echo; sed -n '/^\[ *Ligand *\]/,$p' mmgbsa.ndx; } > .contact.ndx
if [ "${BOUND_MODE:-0}" = "1" ]; then
  CONTACT_SRC=rescore_window.xtc
  CONTACT_B=""
else
  CONTACT_SRC=prod.xtc
  CONTACT_B="-b $TBEGIN"
fi
# shellcheck disable=SC2086
"$GMX" mindist -f "$CONTACT_SRC" -s prod.tpr -n .contact.ndx $CONTACT_B \
    -od .mindist.xvg -on .numcont.xvg -d 0.4 -group >/dev/null 2>&1 <<'SEL'
Ligand
MEMB
SEL
[ -s .mindist.xvg ] || { echo "FAIL: could not measure ligand-membrane distance"; exit 2; }

# In bound mode, .mindist.xvg was measured on the extracted window, so its time column IS
# the list of frames actually being scored. Compare it against the times we intended to
# select: this catches a frame-indexing error directly, instead of inferring it from a
# downstream contact count. (trjconv -fr is 1-based; an off-by-one here silently scores
# neighbouring frames, which is exactly the failure this check exists to surface.)
if [ "${BOUND_MODE:-0}" = "1" ]; then
  "$PY" - .mindist.xvg .bound_times.txt <<'PYEOF' || exit 6
import sys
got = [float(l.split()[0]) for l in open(sys.argv[1])
       if not l.startswith(("#", "@")) and l.split()]
want = [float(l) for l in open(sys.argv[2]) if l.strip()]
if len(got) != len(want):
    sys.exit("FAIL: window has %d frames but %d were selected" % (len(got), len(want)))
bad = [(i, w, g) for i, (w, g) in enumerate(zip(want, got)) if abs(w - g) > 1.0]
if bad:
    i, w, g = bad[0]
    sys.exit("FAIL: extracted frame times do not match the selection -- %d of %d differ; "
             "first at position %d (wanted %.3f ps, got %.3f ps). trjconv -fr indexing "
             "is wrong; the scored frames are NOT the bound frames."
             % (len(bad), len(want), i, w, g))
print("  frame selection verified: %d extracted times match the bound set" % len(got))
PYEOF
fi

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
  if [ "${BOUND_MODE:-0}" = "1" ]; then
    echo "FAIL: bound-frame selection kept ${CPCT}% contacting frames -- selection is broken."
    echo "      Frames were chosen with min-distance > ${MEMB_CUT} nm, so this must not happen."
    echo "      Do NOT relax this check; fix the selection."
    exit 5
  fi
  echo "FAIL: the peptide contacts the bilayer in ${CPCT}% of frames (min ${MINDIST} nm)."
  echo "      Reducing the topology to the solute would then discard interactions that do"
  echo "      NOT cancel between complex and free receptor. Rescoring refused for this run;"
  echo "      it needs a membrane-aware model (ipb/memopt), not a stripped topology."
  echo "      Conditional bound-state scoring is available: rerun with BOUND_MODE=1."
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
# Record which frame definition produced this number. A conditional bound-state energy
# and a last-10ns energy are NOT on the same footing and must never be pooled silently.
{ echo "# $TAG rep$REP mode=${BOUND_MODE:+bound}${BOUND_MODE:-full10ns} frames=${NFR}"
  [ "${BOUND_MODE:-0}" = "1" ] && echo "# bound_selection memb_cut=${MEMB_CUT} rmsd_cut=${RMSD_CUT} n_bound_total=${NSEL}"
} > rescore_mode.txt
echo "RESCORE_OK $TAG rep$REP mode=${BOUND_MODE:+bound}${BOUND_MODE:-full10ns}"
tail -3 "$OUT"
