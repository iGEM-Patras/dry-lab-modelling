#!/bin/bash
# Cycle 3b - equilibrate ONE control system and MEASURE ns/day on the pgpu GPU.
#
# min -> CHIRALITY GATE -> NVT(200ps,1fs) -> NPT(1ns,2fs) -> CHIRALITY GATE
#     -> production benchmark (-resethway) -> report measured ns/day
#
# The chirality gate is mandatory: the ff14SB topology is enantiomer-blind, so
# nothing else in this pipeline can detect a D-centre that inverted.
set -uo pipefail

TAG="${1:?usage: run_md.sh <tag> <dres|none> [bench_steps]}"
DRES="${2:-none}"
BENCH_STEPS="${3:-50000}"        # 100 ps at 2 fs

W=/data/users/kzanaj/boltz_dock/cycle3b
E=/data/users/kzanaj/envs/gmxmmpbsa
GMX=/data/users/kzanaj/envs/gmxcuda/bin/gmx
PY=$E/bin/python
S=$W/systems/$TAG
cd "$S"

[ -f system.gro ] && [ -f system.top ] || { echo "FAIL: no system.gro/system.top in $S"; exit 1; }
nvidia-smi --query-gpu=name --format=csv,noheader

# ---- index groups -----------------------------------------------------------
printf 'q\n' | $GMX make_ndx -f system.gro -o index.ndx >mk.log 2>&1
echo "=== index groups ==="; grep -oE "^ *[0-9]+ [A-Za-z_+-]+" mk.log | head -20
for g in Protein Other Water_and_ions; do
  grep -qE "[0-9]+ $g " mk.log || { echo "FAIL: group '$g' missing -> fix tc-grps"; exit 1; }
done

gate () {  # gate <stage> <structure>
  local stage="$1" struct="$2"
  [ "$DRES" = "none" ] && { echo "  [gate:$stage] no D-residue, skipped"; return 0; }
  $GMX editconf -f "$struct" -o "gate_${stage}.pdb" -n index.ndx >/dev/null 2>&1 <<< "1"
  $PY $W/scripts/chirality.py assert "gate_${stage}.pdb" "$DRES" B || {
      echo "FAIL: chirality inverted at stage '$stage' - DISCARD this run"; exit 3; }
}

# ---- 1. minimise ------------------------------------------------------------
$GMX grompp -f $W/scripts/min.mdp -c system.gro -p system.top -o min.tpr -n index.ndx -maxwarn 5 >grompp_min.log 2>&1 \
  || { echo "FAIL grompp min"; tail -25 grompp_min.log; exit 1; }
$GMX mdrun -deffnm min -nb gpu >md_min.log 2>&1 || { echo "FAIL mdrun min"; tail -20 md_min.log; exit 1; }
echo "min: $(grep -E 'Potential Energy|Maximum force' md_min.log | tail -2 | tr '\n' ' ')"
$GMX editconf -f min.gro -o min.pdb >/dev/null 2>&1
gate min min.pdb

# ---- 2. NVT ----------------------------------------------------------------
$GMX grompp -f $W/scripts/nvt.mdp -c min.gro -p system.top -o nvt.tpr -n index.ndx -maxwarn 5 >grompp_nvt.log 2>&1 \
  || { echo "FAIL grompp nvt"; tail -25 grompp_nvt.log; exit 1; }
$GMX mdrun -deffnm nvt -nb gpu -pme gpu -update gpu >md_nvt.log 2>&1 \
  || { echo "FAIL mdrun nvt"; tail -20 md_nvt.log; exit 1; }
echo "NVT perf: $(grep -A1 'Performance' md_nvt.log | tail -1)"

# ---- 3. NPT ---------------------------------------------------------------
$GMX grompp -f $W/scripts/npt.mdp -c nvt.gro -t nvt.cpt -p system.top -o npt.tpr -n index.ndx -maxwarn 5 >grompp_npt.log 2>&1 \
  || { echo "FAIL grompp npt"; tail -25 grompp_npt.log; exit 1; }
$GMX mdrun -deffnm npt -nb gpu -pme gpu -update gpu >md_npt.log 2>&1 \
  || { echo "FAIL mdrun npt"; tail -20 md_npt.log; exit 1; }
echo "NPT perf: $(grep -A1 'Performance' md_npt.log | tail -1)"
$GMX editconf -f npt.gro -o npt.pdb >/dev/null 2>&1
gate npt npt.pdb

# ---- 4. production BENCHMARK ----------------------------------------------
# -resethway discards the first half's timings so setup/load-balancing is excluded.
$GMX grompp -f $W/scripts/prod.mdp -c npt.gro -t npt.cpt -p system.top -o bench.tpr -n index.ndx -maxwarn 5 >grompp_bench.log 2>&1 \
  || { echo "FAIL grompp bench"; tail -25 grompp_bench.log; exit 1; }
$GMX mdrun -deffnm bench -nsteps "$BENCH_STEPS" -resethway -nb gpu -pme gpu -update gpu >md_bench.log 2>&1 \
  || { echo "FAIL mdrun bench"; tail -20 md_bench.log; exit 1; }

echo "=== BENCHMARK RESULT ==="
grep -E "^ *Time:|Performance:" md_bench.log | tail -3
NSDAY=$(grep "Performance:" md_bench.log | tail -1 | awk '{print $2}')
NATOMS=$($PY -c "print(open('system.gro').readlines()[1].strip())")
echo "atoms: $NATOMS"
echo "MEASURED_NS_PER_DAY=$NSDAY"
$PY - <<PYEOF
ns = float("${NSDAY:-0}") or None
if ns:
    per_run = 20.0/ns
    print(f"  20 ns production per replicate: {per_run:.2f} GPU-days")
    print(f"  Stage 1 (8 systems x 3 reps = 24 runs): {24*per_run:.1f} GPU-days")
    print(f"  Stage 2 (30 runs):                     {30*per_run:.1f} GPU-days")
PYEOF
echo "MD_OK $TAG"
